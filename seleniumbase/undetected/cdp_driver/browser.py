"""CDP-Driver is based on NoDriver"""
from __future__ import annotations
import asyncio
import atexit
import http.cookiejar
import json
import logging
import os
import pickle
import pathlib
import shutil
import urllib.parse
import urllib.request
import warnings
from collections import defaultdict
from typing import List, Set, Tuple, Union
import mycdp as cdp
from . import cdp_util as util
from . import tab
from ._contradict import ContraDict
from .config import PathLike, Config, is_posix
from .connection import Connection

logger = logging.getLogger(__name__)


def get_registered_instances():
    return __registered__instances__


def deconstruct_browser():
    import time

    for _ in __registered__instances__:
        if not _.stopped:
            _.stop()
        for attempt in range(5):
            try:
                if _.config and not _.config.uses_custom_data_dir:
                    shutil.rmtree(_.config.user_data_dir, ignore_errors=False)
            except FileNotFoundError:
                break
            except (PermissionError, OSError) as e:
                if attempt == 4:
                    logger.debug(
                        "Problem removing data dir %s\n"
                        "Consider checking whether it's there "
                        "and remove it by hand\nerror: %s",
                        _.config.user_data_dir,
                        e,
                    )
                    break
                time.sleep(0.15)
                continue
        logging.debug("Temp profile %s was removed." % _.config.user_data_dir)


class Browser:
    """
    The Browser object is the "root" of the hierarchy
    and contains a reference to the browser parent process.
    There should usually be only 1 instance of this.
    All opened tabs, extra browser screens,
    and resources will not cause a new Browser process,
    but rather create additional :class:`Tab` objects.
    So, besides starting your instance and first/additional tabs,
    you don't actively use it a lot under normal conditions.
    Tab objects will represent and control:
     - tabs (as you know them)
     - browser windows (new window)
     - iframe
     - background processes
    Note:
    The Browser object is not instantiated by __init__
    but using the asynchronous :meth:`Browser.create` method.
    Note:
    In Chromium based browsers, there is a parent process which keeps
    running all the time, even if there are no visible browser windows.
    Sometimes it's stubborn to close it, so make sure that after using
    this library, the browser is correctly and fully closed/exited/killed.
    """
    _process: asyncio.subprocess.Process
    _process_pid: int
    _http: HTTPApi = None
    _cookies: CookieJar = None
    config: Config
    connection: Connection

    @classmethod
    async def create(
        cls,
        config: Config = None,
        *,
        user_data_dir: PathLike = None,
        headless: bool = False,
        incognito: bool = False,
        guest: bool = False,
        browser_executable_path: PathLike = None,
        browser_args: List[str] = None,
        sandbox: bool = True,
        host: str = None,
        port: int = None,
        **kwargs,
    ) -> Browser:
        """Entry point for creating an instance."""
        if not config:
            config = Config(
                user_data_dir=user_data_dir,
                headless=headless,
                incognito=incognito,
                guest=guest,
                browser_executable_path=browser_executable_path,
                browser_args=browser_args or [],
                sandbox=sandbox,
                host=host,
                port=port,
                **kwargs,
            )
        instance = cls(config)
        await instance.start()
        return instance

    def __init__(self, config: Config, **kwargs):
        """
        Constructor. To create a instance, use :py:meth:`Browser.create(...)`
        :param config:
        """
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            raise RuntimeError(
                "{0} objects of this class are created "
                "using await {0}.create()".format(
                    self.__class__.__name__
                )
            )
        self.config = config
        self.targets: List = []
        self.info = None
        self._target = None
        self._process = None
        self._process_pid = None
        self._keep_user_data_dir = None
        self._is_updating = asyncio.Event()
        self.connection: Connection = None
        logger.debug("Session object initialized: %s" % vars(self))

    @property
    def websocket_url(self):
        return self.info.webSocketDebuggerUrl

    @property
    def main_tab(self) -> tab.Tab:
        """Returns the target which was launched with the browser."""
        return sorted(
            self.targets, key=lambda x: x.type_ == "page", reverse=True
        )[0]

    @property
    def tabs(self) -> List[tab.Tab]:
        """Returns the current targets which are of type "page"."""
        tabs = filter(lambda item: item.type_ == "page", self.targets)
        return list(tabs)

    @property
    def cookies(self) -> CookieJar:
        if not self._cookies:
            self._cookies = CookieJar(self)
        return self._cookies

    @property
    def stopped(self):
        if self._process and self._process.returncode is None:
            return False
        return True
        # return (self._process and self._process.returncode) or False

    async def wait(self, time: Union[float, int] = 1) -> Browser:
        """Wait for <time> seconds. Important to use,
        especially in between page navigation.
        :param time:
        """
        return await asyncio.sleep(time, result=self)

    sleep = wait
    """Alias for wait"""
    def _handle_target_update(
        self,
        event: Union[
            cdp.target.TargetInfoChanged,
            cdp.target.TargetDestroyed,
            cdp.target.TargetCreated,
            cdp.target.TargetCrashed,
        ],
    ):
        """This is an internal handler which updates the targets
        when Chrome emits the corresponding event."""
        if isinstance(event, cdp.target.TargetInfoChanged):
            target_info = event.target_info
            current_tab = next(
                filter(
                    lambda item: item.target_id == target_info.target_id, self.targets  # noqa
                )
            )
            current_target = current_tab.target
            if logger.getEffectiveLevel() <= 10:
                changes = util.compare_target_info(
                    current_target, target_info
                )
                changes_string = ""
                for change in changes:
                    key, old, new = change
                    changes_string += f"\n{key}: {old} => {new}\n"
                logger.debug(
                    "Target #%d has changed: %s"
                    % (self.targets.index(current_tab), changes_string)
                )
                current_tab.target = target_info
        elif isinstance(event, cdp.target.TargetCreated):
            target_info: cdp.target.TargetInfo = event.target_info
            from .tab import Tab

            new_target = Tab(
                (
                    f"ws://{self.config.host}:{self.config.port}"
                    f"/devtools/{target_info.type_ or 'page'}"
                    f"/{target_info.target_id}"
                ),
                target=target_info,
                browser=self,
            )
            self.targets.append(new_target)
            logger.debug(
                "Target #%d created => %s", len(self.targets), new_target
            )
        elif isinstance(event, cdp.target.TargetDestroyed):
            current_tab = next(
                filter(
                    lambda item: item.target_id == event.target_id,
                    self.targets,
                )
            )
            logger.debug(
                "Target removed. id # %d => %s"
                % (self.targets.index(current_tab), current_tab)
            )
            self.targets.remove(current_tab)

    async def get(
        self,
        url="about:blank",
        new_tab: bool = False,
        new_window: bool = False,
    ) -> tab.Tab:
        """Top level get. Utilizes the first tab to retrieve given url.
        Convenience function known from selenium.
        This function detects when DOM events have fired during navigation.
        :param url: The URL to navigate to
        :param new_tab: Open new tab
        :param new_window: Open new window
        :return: Page
        """
        if new_tab or new_window:
            # Create new target using the browser session.
            target_id = await self.connection.send(
                cdp.target.create_target(
                    url, new_window=new_window, enable_begin_frame_control=True
                )
            )
            connection: tab.Tab = next(
                filter(
                    lambda item: item.type_ == "page" and item.target_id == target_id,  # noqa
                    self.targets,
                )
            )
            connection.browser = self
        else:
            # First tab from browser.tabs
            connection: tab.Tab = next(
                filter(lambda item: item.type_ == "page", self.targets)
            )
            # Use the tab to navigate to new url
            frame_id, loader_id, *_ = await connection.send(
                cdp.page.navigate(url)
            )
            # Update the frame_id on the tab
            connection.frame_id = frame_id
            connection.browser = self
        await connection.sleep(0.25)
        return connection

    async def start(self=None) -> Browser:
        """Launches the actual browser."""
        if not self:
            warnings.warn(
                "Use ``await Browser.create()`` to create a new instance!"
            )
            return
        if self._process or self._process_pid:
            if self._process.returncode is not None:
                return await self.create(config=self.config)
            warnings.warn(
                "Ignored! This call has no effect when already running!"
            )
            return
        # self.config.update(kwargs)
        connect_existing = False
        if self.config.host is not None and self.config.port is not None:
            connect_existing = True
        else:
            self.config.host = "127.0.0.1"
            self.config.port = util.free_port()
        if not connect_existing:
            logger.debug(
                "BROWSER EXECUTABLE PATH: %s",
                self.config.browser_executable_path,
            )
            if not pathlib.Path(self.config.browser_executable_path).exists():
                raise FileNotFoundError(
                    (
                        """
                    ---------------------------------------
                    Could not determine browser executable.
                    ---------------------------------------
                    Browser must be installed in the default location / path!
                    If you are sure about the browser executable,
                    set it using `browser_executable_path='{}` parameter."""
                    ).format(
                        "/path/to/browser/executable"
                        if is_posix
                        else "c:/path/to/your/browser.exe"
                    )
                )
        if getattr(self.config, "_extensions", None):  # noqa
            self.config.add_argument(
                "--load-extension=%s"
                % ",".join(str(_) for _ in self.config._extensions)
            )  # noqa
        exe = self.config.browser_executable_path
        params = self.config()
        logger.info(
            "Starting\n\texecutable :%s\n\narguments:\n%s",
            exe,
            "\n\t".join(params),
        )
        if not connect_existing:
            self._process: asyncio.subprocess.Process = (
                await asyncio.create_subprocess_exec(
                    # self.config.browser_executable_path,
                    # *cmdparams,
                    exe,
                    *params,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    close_fds=is_posix,
                )
            )
            self._process_pid = self._process.pid
        self._http = HTTPApi((self.config.host, self.config.port))
        get_registered_instances().add(self)
        await asyncio.sleep(0.25)
        for _ in range(5):
            try:
                self.info = ContraDict(
                    await self._http.get("version"), silent=True
                )
            except (Exception,):
                if _ == 4:
                    logger.debug("Could not start", exc_info=True)
                await self.sleep(0.5)
            else:
                break
        if not self.info:
            raise Exception(
                (
                    """
                    --------------------------------
                    Failed to connect to the browser
                    --------------------------------
                    Possibly because you are running as "root".
                    If so, you may need to use no_sandbox=True.
                    """
                )
            )
        self.connection = Connection(
            self.info.webSocketDebuggerUrl, _owner=self
        )
        if self.config.autodiscover_targets:
            logger.info("Enabling autodiscover targets")
            self.connection.handlers[cdp.target.TargetInfoChanged] = [
                self._handle_target_update
            ]
            self.connection.handlers[cdp.target.TargetCreated] = [
                self._handle_target_update
            ]
            self.connection.handlers[cdp.target.TargetDestroyed] = [
                self._handle_target_update
            ]
            self.connection.handlers[cdp.target.TargetCrashed] = [
                self._handle_target_update
            ]
            await self.connection.send(
                cdp.target.set_discover_targets(discover=True)
            )
        await self
        # self.connection.handlers[cdp.inspector.Detached] = [self.stop]
        # return self

    async def grant_all_permissions(self):
        """
        Grant permissions for:
            accessibilityEvents
            audioCapture
            backgroundSync
            backgroundFetch
            clipboardReadWrite
            clipboardSanitizedWrite
            displayCapture
            durableStorage
            geolocation
            idleDetection
            localFonts
            midi
            midiSysex
            nfc
            notifications
            paymentHandler
            periodicBackgroundSync
            protectedMediaIdentifier
            sensors
            storageAccess
            topLevelStorageAccess
            videoCapture
            videoCapturePanTiltZoom
            wakeLockScreen
            wakeLockSystem
            windowManagement
        """
        permissions = list(cdp.browser.PermissionType)
        permissions.remove(cdp.browser.PermissionType.FLASH)
        permissions.remove(cdp.browser.PermissionType.CAPTURED_SURFACE_CONTROL)
        await self.connection.send(cdp.browser.grant_permissions(permissions))

    async def tile_windows(self, windows=None, max_columns: int = 0):
        import math
        try:
            import mss
        except Exception:
            from seleniumbase.fixtures import shared_utils
            shared_utils.pip_install("mss")
            import mss
        m = mss.mss()
        screen, screen_width, screen_height = 3 * (None,)
        if m.monitors and len(m.monitors) >= 1:
            screen = m.monitors[0]
            screen_width = screen["width"]
            screen_height = screen["height"]
        if not screen or not screen_width or not screen_height:
            warnings.warn("No monitors detected!")
            return
        await self
        distinct_windows = defaultdict(list)
        if windows:
            tabs = windows
        else:
            tabs = self.tabs
        for _tab in tabs:
            window_id, bounds = await _tab.get_window()
            distinct_windows[window_id].append(_tab)
        num_windows = len(distinct_windows)
        req_cols = max_columns or int(num_windows * (19 / 6))
        req_rows = int(num_windows / req_cols)
        while req_cols * req_rows < num_windows:
            req_rows += 1
        box_w = math.floor((screen_width / req_cols) - 1)
        box_h = math.floor(screen_height / req_rows)
        distinct_windows_iter = iter(distinct_windows.values())
        grid = []
        for x in range(req_cols):
            for y in range(req_rows):
                try:
                    tabs = next(distinct_windows_iter)
                except StopIteration:
                    continue
                if not tabs:
                    continue
                tab = tabs[0]
                try:
                    pos = [x * box_w, y * box_h, box_w, box_h]
                    grid.append(pos)
                    await tab.set_window_size(*pos)
                except Exception:
                    logger.info(
                        "Could not set window size. Exception => ",
                        exc_info=True,
                    )
                    continue
        return grid

    async def _get_targets(self) -> List[cdp.target.TargetInfo]:
        info = await self.connection.send(
            cdp.target.get_targets(), _is_update=True
        )
        return info

    async def update_targets(self):
        targets: List[cdp.target.TargetInfo]
        targets = await self._get_targets()
        for t in targets:
            for existing_tab in self.targets:
                existing_target = existing_tab.target
                if existing_target.target_id == t.target_id:
                    existing_tab.target.__dict__.update(t.__dict__)
                    break
            else:
                self.targets.append(
                    Connection(
                        (
                            f"ws://{self.config.host}:{self.config.port}"
                            f"/devtools/page"  # All types are "page"
                            f"/{t.target_id}"
                        ),
                        target=t,
                        _owner=self,
                    )
                )
        await asyncio.sleep(0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type and exc_val:
            raise exc_type(exc_val)

    def __iter__(self):
        self._i = self.tabs.index(self.main_tab)
        return self

    def __reversed__(self):
        return reversed(list(self.tabs))

    def __next__(self):
        try:
            return self.tabs[self._i]
        except IndexError:
            del self._i
            raise StopIteration
        except AttributeError:
            del self._i
            raise StopIteration
        finally:
            if hasattr(self, "_i"):
                if self._i != len(self.tabs):
                    self._i += 1
                else:
                    del self._i

    def stop(self):
        try:
            # asyncio.get_running_loop().create_task(
            #     self.connection.send(cdp.browser.close())
            # )
            asyncio.get_event_loop().create_task(self.connection.aclose())
            logger.debug(
                "Closed the connection using get_event_loop().create_task()"
            )
        except RuntimeError:
            if self.connection:
                try:
                    # asyncio.run(self.connection.send(cdp.browser.close()))
                    asyncio.run(self.connection.aclose())
                    logger.debug("Closed the connection using asyncio.run()")
                except Exception:
                    pass
        for _ in range(3):
            try:
                self._process.terminate()
                logger.info(
                    "Terminated browser with pid %d successfully."
                    % self._process.pid
                )
                break
            except (Exception,):
                try:
                    self._process.kill()
                    logger.info(
                        "Killed browser with pid %d successfully."
                        % self._process.pid
                    )
                    break
                except (Exception,):
                    try:
                        if hasattr(self, "browser_process_pid"):
                            os.kill(self._process_pid, 15)
                            logger.info(
                                "Killed browser with pid %d "
                                "using signal 15 successfully."
                                % self._process.pid
                            )
                            break
                    except (TypeError,):
                        logger.info("typerror", exc_info=True)
                        pass
                    except (PermissionError,):
                        logger.info(
                            "Browser already stopped, "
                            "or no permission to kill. Skip."
                        )
                        pass
                    except (ProcessLookupError,):
                        logger.info("Process lookup failure!")
                        pass
                    except (Exception,):
                        raise
            self._process = None
            self._process_pid = None

    def __await__(self):
        # return ( asyncio.sleep(0)).__await__()
        return self.update_targets().__await__()

    def __del__(self):
        pass


__registered__instances__: Set[Browser] = set()


class CookieJar:
    def __init__(self, browser: Browser):
        self._browser = browser

    async def get_all(
        self, requests_cookie_format: bool = False
    ) -> List[Union[cdp.network.Cookie, "http.cookiejar.Cookie"]]:
        """
        Get all cookies.
        :param requests_cookie_format: when True,
         returns python http.cookiejar.Cookie objects,
         compatible with requests library and many others.
        :type requests_cookie_format: bool
        """
        connection = None
        for _tab in self._browser.tabs:
            if _tab.closed:
                continue
            connection = _tab
            break
        else:
            connection = self._browser.connection
        cookies = await connection.send(cdp.storage.get_cookies())
        if requests_cookie_format:
            import requests.cookies

            return [
                requests.cookies.create_cookie(
                    name=c.name,
                    value=c.value,
                    domain=c.domain,
                    path=c.path,
                    expires=c.expires,
                    secure=c.secure,
                )
                for c in cookies
            ]
        return cookies

    async def set_all(self, cookies: List[cdp.network.CookieParam]):
        """
        Set cookies.
        :param cookies: List of cookies
        """
        connection = None
        for _tab in self._browser.tabs:
            if _tab.closed:
                continue
            connection = _tab
            break
        else:
            connection = self._browser.connection
        cookies = await connection.send(cdp.storage.get_cookies())
        await connection.send(cdp.storage.set_cookies(cookies))

    async def save(self, file: PathLike = ".session.dat", pattern: str = ".*"):
        """
        Save all cookies (or a subset, controlled by `pattern`)
        to a file to be restored later.
        :param file:
        :param pattern: regex style pattern string.
                any cookie that has a  domain, key or value field
                which matches the pattern will be included.
            default = ".*"  (all)
            Eg: the pattern "(cf|.com|nowsecure)" will include cookies which:
                - Have a string "cf" (cloudflare)
                - Have ".com" in them, in either domain, key or value field.
                - Contain "nowsecure"
        :type pattern: str
        """
        import re

        pattern = re.compile(pattern)
        save_path = pathlib.Path(file).resolve()
        connection = None
        for _tab in self._browser.tabs:
            if _tab.closed:
                continue
            connection = _tab
            break
        else:
            connection = self._browser.connection
        cookies = await connection.send(cdp.storage.get_cookies())
        # if not connection:
        #     return
        # if not connection.websocket:
        #     return
        # if connection.websocket.closed:
        #     return
        cookies = await self.get_all(requests_cookie_format=False)
        included_cookies = []
        for cookie in cookies:
            for match in pattern.finditer(str(cookie.__dict__)):
                logger.debug(
                    "Saved cookie for matching pattern '%s' => (%s: %s)",
                    pattern.pattern,
                    cookie.name,
                    cookie.value,
                )
                included_cookies.append(cookie)
                break
        pickle.dump(cookies, save_path.open("w+b"))

    async def load(self, file: PathLike = ".session.dat", pattern: str = ".*"):
        """
        Load all cookies (or a subset, controlled by `pattern`)
        from a file created by :py:meth:`~save_cookies`.
        :param file:
        :param pattern: Regex style pattern string.
               Any cookie that has a  domain, key,
               or value field which matches the pattern will be included.
            Default = ".*"  (all)
            Eg: the pattern "(cf|.com|nowsecure)" will include cookies which:
                - Have a string "cf" (cloudflare)
                - Have ".com" in them, in either domain, key or value field.
                - Contain "nowsecure"
        :type pattern: str
        """
        import re

        pattern = re.compile(pattern)
        save_path = pathlib.Path(file).resolve()
        cookies = pickle.load(save_path.open("r+b"))
        included_cookies = []
        connection = None
        for _tab in self._browser.tabs:
            if _tab.closed:
                continue
            connection = _tab
            break
        else:
            connection = self._browser.connection
        for cookie in cookies:
            for match in pattern.finditer(str(cookie.__dict__)):
                included_cookies.append(cookie)
                logger.debug(
                    "Loaded cookie for matching pattern '%s' => (%s: %s)",
                    pattern.pattern,
                    cookie.name,
                    cookie.value,
                )
                break
        await connection.send(cdp.storage.set_cookies(included_cookies))

    async def clear(self):
        """
        Clear current cookies.
        Note: This includes all open tabs/windows for this browser.
        """
        connection = None
        for _tab in self._browser.tabs:
            if _tab.closed:
                continue
            connection = _tab
            break
        else:
            connection = self._browser.connection
        cookies = await connection.send(cdp.storage.get_cookies())
        if cookies:
            await connection.send(cdp.storage.clear_cookies())


class HTTPApi:
    def __init__(self, addr: Tuple[str, int]):
        self.host, self.port = addr
        self.api = "http://%s:%d" % (self.host, self.port)

    @classmethod
    def from_target(cls, target):
        ws_url = urllib.parse.urlparse(target.websocket_url)
        inst = cls((ws_url.hostname, ws_url.port))
        return inst

    async def get(self, endpoint: str):
        return await self._request(endpoint)

    async def post(self, endpoint, data):
        return await self._request(endpoint, data)

    async def _request(self, endpoint, method: str = "get", data: dict = None):
        url = urllib.parse.urljoin(
            self.api, f"json/{endpoint}" if endpoint else "/json"
        )
        if data and method.lower() == "get":
            raise ValueError("get requests cannot contain data")
        if not url:
            url = self.api + endpoint
        request = urllib.request.Request(url)
        request.method = method
        request.data = None
        if data:
            request.data = json.dumps(data).encode("utf-8")

        response = await asyncio.get_running_loop().run_in_executor(
            None, lambda: urllib.request.urlopen(request, timeout=10)
        )
        return json.loads(response.read())


atexit.register(deconstruct_browser)
