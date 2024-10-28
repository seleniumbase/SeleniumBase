import logging
import os
import re
import requests
import subprocess
import sys
import time
import selenium.webdriver.chrome.service
import selenium.webdriver.chrome.webdriver
import selenium.webdriver.common.service
import selenium.webdriver.remote.command
from contextlib import suppress
from .cdp import CDP
from .cdp import PageElement
from .dprocess import start_detached
from .options import ChromeOptions
from .reactor import Reactor
from .webelement import WebElement

__all__ = (
    "Chrome",
    "ChromeOptions",
    "Patcher",
    "Reactor",
    "CDP",
    "find_chrome_executable",
)
IS_POSIX = sys.platform.startswith(("darwin", "cygwin", "linux"))
logger = logging.getLogger("uc")
logger.setLevel(logging.getLogger().getEffectiveLevel())


class Chrome(selenium.webdriver.chrome.webdriver.WebDriver):
    """Controls chromedriver to drive a browser.
    The driver gets downloaded automatically."""
    _instances = set()
    session_id = None
    debug = False

    def __init__(
        self,
        options=None,
        user_data_dir=None,
        driver_executable_path=None,
        browser_executable_path=None,
        port=0,
        enable_cdp_events=False,
        log_level=0,
        headless=False,
        patch_driver=True,
        version_main=None,
        patcher_force_close=False,
        suppress_welcome=True,
        use_subprocess=True,
        debug=False,
        **kw,
    ):
        """
        Starts the Chrome service and creates a new instance of chromedriver.

        Parameters
        ----------

        options: (default: None)
            Takes an instance of ChromeOptions to customize browser behavior.

        user_data_dir:
            None (default) Create a temp profile directory for the browser.
            If user_data_dir is a path to a valid Chrome profile directory,
            use it and turn off the automatic removal mechanism at exit.

        driver_executable_path:
            None (default) Downloads and patches the new binary.

        browser_executable_path:
            None (default) Use find_chrome_executable().
            (If not specified, make sure Chrome is on the PATH.)

        port: (default: 0)
            Port you would like the service to run.
            If left as 0, a free port will be found.

        enable_cdp_events: (default: False)
            This enables the handling of wire messages.
            When enabled, you can subscribe to CDP events by using:

                driver.add_cdp_listener("Network.dataReceived", yourcallback)
                # yourcallback: callable that accepts exactly 1 dict parameter.

        log_level: (default: adapts to python global log level)

        headless: (default: False)
            Use headless mode.
            (Already handled by seleniumbase/core/browser_launcher.py)

        patch_driver: (default: True)
            Patches uc_driver to be undetectable if not already patched.

        version_main: (default: None)
            Overrides the browser version for older versions of Chrome.
            Eg: version_main=96
            (Useful when you have a newer driver, but an older browser.)

        patcher_force_close: (default: False)
            Instructs patcher to access the chromedriver binary.
            If the file is locked, it will force shutdown all instances.
            Setting this is not recommended, unless you know the implications.

        suppress_welcome: (default: True)
            Suppress the Chrome welcome screen that appears on first-time runs.

        use_subprocess: (default: True)
            Subprocess chromedriver/python: Don't make Chrome a parent process.
        """
        self.debug = debug
        self.patcher = None
        import fasteners
        from seleniumbase.fixtures import constants
        if patch_driver:
            uc_lock = fasteners.InterProcessLock(
                constants.MultiBrowser.DRIVER_FIXING_LOCK
            )
            with uc_lock:
                from .patcher import Patcher
                self.patcher = Patcher(
                    executable_path=driver_executable_path,
                    force=patcher_force_close,
                    version_main=version_main,
                )
                self.patcher.auto()
        if not options:
            options = ChromeOptions()
        try:
            if hasattr(options, "_session") and options._session is not None:
                # Prevent reuse of options.
                # (Probably a port overlap. Quit existing driver and continue.)
                logger.debug("You cannot reuse the ChromeOptions object")
                with suppress(Exception):
                    options._session.quit()
        except AttributeError:
            pass
        options._session = self
        debug_host = "127.0.0.1"
        debug_port = 9222
        special_port_free = False  # If the port isn't free, don't use 9222
        try:
            res = requests.get("http://127.0.0.1:9222", timeout=1)
            if res.status_code != 200:
                raise Exception("The port is free! It will be used!")
        except Exception:
            # Use port 9222, which outputs to chrome://inspect/#devices
            special_port_free = True
        sys_argv = sys.argv
        arg_join = " ".join(sys_argv)
        from seleniumbase import config as sb_config
        if (
            (("-n" in sys.argv) or (" -n=" in arg_join) or ("-c" in sys.argv))
            or (hasattr(sb_config, "multi_proxy") and sb_config.multi_proxy)
            or not special_port_free
        ):
            debug_port = selenium.webdriver.common.service.utils.free_port()
        if hasattr(options, "_remote_debugging_port"):
            # The user chooses the port. Errors happen if the port is taken.
            debug_port = options._remote_debugging_port
        if not options.debugger_address:
            options.debugger_address = "%s:%d" % (debug_host, debug_port)
        if enable_cdp_events:
            options.set_capability(
                "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
            )
        options.add_argument("--remote-debugging-host=%s" % debug_host)
        options.add_argument("--remote-debugging-port=%s" % debug_port)
        if user_data_dir:
            options.add_argument("--user-data-dir=%s" % user_data_dir)
        language, keep_user_data_dir = None, bool(user_data_dir)
        # See if a custom user profile is specified in options
        for arg in options.arguments:
            if "lang" in arg:
                m = re.search("(?:--)?lang(?:[ =])?(.*)", arg)
                try:
                    language = m[1]
                except IndexError:
                    language = "en-US,en;q=0.9"
            if "user-data-dir" in arg:
                m = re.search("(?:--)?user-data-dir(?:[ =])?(.*)", arg)
                try:
                    user_data_dir = m[1]
                    keep_user_data_dir = True
                except IndexError:
                    pass
        if not user_data_dir:
            if hasattr(options, "user_data_dir") and getattr(
                options, "user_data_dir", None
            ):
                options.add_argument(
                    "--user-data-dir=%s" % options.user_data_dir
                )
                keep_user_data_dir = True
            else:
                import tempfile
                user_data_dir = os.path.normpath(tempfile.mkdtemp())
                keep_user_data_dir = False
                arg = "--user-data-dir=%s" % user_data_dir
                # Create a temporary folder for the user-data profile.
                options.add_argument(arg)
        if not language:
            with suppress(Exception):
                import locale
                language = locale.getlocale()[0].replace("_", "-")
            if (
                not language
                or "English" in language
                or "United States" in language
            ):
                language = "en-US"
        options.add_argument("--lang=%s" % language)
        if not options.binary_location:
            binary_location = (
                browser_executable_path or find_chrome_executable()
            )
            if binary_location:
                options.binary_location = binary_location
            else:
                # Improve the default error message in this situation.
                # Setting options.binary_location to None results in:
                #    "TypeError: Binary Location Must be a String"
                raise Exception("Chrome not found! Install it first!")
        self._delay = constants.UC.RECONNECT_TIME
        self.user_data_dir = user_data_dir
        self.keep_user_data_dir = keep_user_data_dir
        if suppress_welcome:
            options.arguments.extend(
                [
                    "--no-default-browser-check",
                    "--no-first-run",
                    "--no-service-autorun",
                    "--password-store=basic",
                    "--profile-directory=Default",
                ]
            )
        options.add_argument(
            "--log-level=%d" % log_level
            or divmod(logging.getLogger().getEffectiveLevel(), 10)[0]
        )
        if hasattr(options, 'handle_prefs'):
            options.handle_prefs(user_data_dir)
        with suppress(Exception):
            import json
            with open(
                os.path.join(
                    os.path.abspath(user_data_dir),
                    "Default",
                    "Preferences",
                ),
                encoding="utf-8",
                mode="r+",
                errors="ignore",
            ) as fs:
                config = json.load(fs)
                if (
                    "exit_type" not in config["profile"].keys()
                    or config["profile"]["exit_type"] is not None
                ):
                    config["profile"]["exit_type"] = None
                fs.seek(0, 0)
                fs.truncate()
                json.dump(config, fs)
        creationflags = 0
        if "win32" in sys.platform:
            creationflags = subprocess.CREATE_NO_WINDOW
        self.options = options
        uc_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.DRIVER_FIXING_LOCK
        )
        with uc_lock:
            if not use_subprocess:
                self.browser_pid = start_detached(
                    options.binary_location, *options.arguments
                )
            else:
                gui_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.PYAUTOGUILOCK
                )
                with gui_lock:
                    browser = subprocess.Popen(
                        [options.binary_location, *options.arguments],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        close_fds=IS_POSIX,
                        creationflags=creationflags,
                    )
                    self.browser_pid = browser.pid
            service_ = None
            log_output = subprocess.PIPE
            if patch_driver:
                service_ = selenium.webdriver.chrome.service.Service(
                    executable_path=self.patcher.executable_path,
                    service_args=["--disable-build-check"],
                    port=port,
                    log_output=log_output,
                )
            else:
                service_ = selenium.webdriver.chrome.service.Service(
                    executable_path=driver_executable_path,
                    service_args=["--disable-build-check"],
                    port=port,
                    log_output=log_output,
                )
            if hasattr(service_, "creationflags"):
                setattr(service_, "creationflags", creationflags)
            if hasattr(service_, "creation_flags"):
                setattr(service_, "creation_flags", creationflags)
            super().__init__(options=options, service=service_)
            self.reactor = None
            if enable_cdp_events:
                if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                    logging.getLogger(
                        "selenium.webdriver.remote.remote_connection"
                    ).setLevel(20)
                reactor = Reactor(self)
                reactor.start()
                self.reactor = reactor
            self._web_element_cls = WebElement

    def __getattribute__(self, item):
        if not super().__getattribute__("debug"):
            return super().__getattribute__(item)
        else:
            import inspect
            original = super().__getattribute__(item)
            if inspect.ismethod(original) and not inspect.isclass(original):
                def newfunc(*args, **kwargs):
                    return original(*args, **kwargs)
                return newfunc
            return original

    def __dir__(self):
        return object.__dir__(self)

    def _get_cdc_props(self):
        cdc_props = []
        with suppress(Exception):
            cdc_props = self.execute_script(
                """
                let objectToInspect = window,
                    result = [];
                while(objectToInspect !== null)
                { result = result.concat(
                    Object.getOwnPropertyNames(objectToInspect)
                  );
                  objectToInspect = Object.getPrototypeOf(objectToInspect); }
                return result.filter(i => i.match(/^[a-z]{3}_[a-z]{22}_.*/i))
                """
            )
        return cdc_props

    def _hook_remove_cdc_props(self, cdc_props):
        if len(cdc_props) < 1:
            return
        cdc_props_js_array = "[" + ", ".join(
            '"' + p + '"' for p in cdc_props
        ) + "]"
        self.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": cdc_props_js_array + (
                    ".forEach(p => delete window[p]);"
                )
            },
        )

    def remove_cdc_props_as_needed(self):
        cdc_props = self._get_cdc_props()
        if len(cdc_props) > 0:
            self._hook_remove_cdc_props(cdc_props)
            time.sleep(0.05)

    def get(self, url):
        self.remove_cdc_props_as_needed()
        return super().get(url)

    def add_cdp_listener(self, event_name, callback):
        if (
            self.reactor
            and self.reactor is not None
            and isinstance(self.reactor, Reactor)
        ):
            self.reactor.add_event_handler(event_name, callback)
            return self.reactor.handlers
        return False

    def clear_cdp_listeners(self):
        if self.reactor and isinstance(self.reactor, Reactor):
            self.reactor.handlers.clear()

    def window_new(self, url=None):
        self.execute(
            selenium.webdriver.remote.command.Command.NEW_WINDOW,
            {"type": "window"},
        )
        if url:
            self.remove_cdc_props_as_needed()
            return super().get(url)
        return None

    def tab_new(self, url):
        """Open url in a new tab."""
        if not hasattr(self, "cdp"):
            self.cdp = CDP(self.options)
        self.cdp.tab_new(str(url))

    def tab_list(self):
        if not hasattr(self, "cdp"):
            self.cdp = CDP(self.options)

        retval = self.get(self.cdp.endpoints["list"])
        return [PageElement(o) for o in retval]

    def reconnect(self, timeout=0.1):
        """This can be useful when sites use heavy detection methods:
        - Stops the chromedriver service that runs in the background.
        - Starts the chromedriver service that runs in the background.
        - Recreates the session."""
        if hasattr(self, "service"):
            with suppress(Exception):
                if self.service.is_connectable():
                    self.stop_client()
                    self.service.stop()
            if isinstance(timeout, str):
                if timeout.lower() == "breakpoint":
                    breakpoint()  # To continue:
                    pass  # Type "c" & press ENTER!
            else:
                time.sleep(timeout)
            with suppress(Exception):
                self.service.start()
        with suppress(Exception):
            self.start_session()
        with suppress(Exception):
            if self.current_url.startswith("chrome-extension://"):
                self.close()
                if self.service.is_connectable():
                    self.stop_client()
                    self.service.stop()
                self.service.start()
                self.start_session()
        self._is_connected = True

    def disconnect(self):
        """Stops the chromedriver service that runs in the background.
        To use driver methods again, you MUST call driver.connect()"""
        if hasattr(self, "service"):
            with suppress(Exception):
                if self.service.is_connectable():
                    self.stop_client()
                    self.service.stop()
            self._is_connected = False

    def connect(self):
        """Starts the chromedriver service that runs in the background
        and recreates the session."""
        if hasattr(self, "service"):
            with suppress(Exception):
                self.service.start()
        with suppress(Exception):
            self.start_session()
        with suppress(Exception):
            if self.current_url.startswith("chrome-extension://"):
                self.close()
                if self.service.is_connectable():
                    self.stop_client()
                    self.service.stop()
                self.service.start()
                self.start_session()
        self._is_connected = True

    def start_session(self, capabilities=None):
        if not capabilities:
            capabilities = self.options.to_capabilities()
        super().start_session(capabilities)

    def quit(self):
        try:
            logger.debug("Terminating the UC browser")
            os.kill(self.browser_pid, 15)
            if "linux" in sys.platform:
                os.waitpid(self.browser_pid, 0)
                time.sleep(0.02)
            else:
                time.sleep(0.04)
        except (AttributeError, ChildProcessError, RuntimeError, OSError):
            time.sleep(0.05)
        except TimeoutError as e:
            logger.debug(e, exc_info=True)
        except Exception:
            pass
        if hasattr(self, "service") and getattr(self.service, "process", None):
            logger.debug("Stopping webdriver service")
            with suppress(Exception):
                self.stop_client()
                self.service.stop()
        with suppress(Exception):
            if self.reactor and isinstance(self.reactor, Reactor):
                logger.debug("Shutting down Reactor")
                self.reactor.event.set()
        if (
            hasattr(self, "keep_user_data_dir")
            and hasattr(self, "user_data_dir")
            and not self.keep_user_data_dir
        ):
            import shutil
            for _ in range(5):
                try:
                    shutil.rmtree(self.user_data_dir, ignore_errors=False)
                except FileNotFoundError:
                    pass
                except (RuntimeError, OSError, PermissionError) as e:
                    logger.debug(
                        "When removing the temp profile, a %s occured: "
                        "%s\nRetrying..."
                        % (e.__class__.__name__, e)
                    )
                else:
                    logger.debug(
                        "Successfully removed %s" % self.user_data_dir
                    )
                    break
                time.sleep(0.1)
        # Dereference Patcher so that it can start cleaning up as well.
        # This must come last, otherwise it will throw "in use" errors.
        self.patcher = None

    def __del__(self):
        with suppress(Exception):
            if "win32" in sys.platform:
                self.stop_client()
                self.command_executor.close()
            else:
                super().quit()
        with suppress(Exception):
            self.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reconnect(timeout=self._delay)

    def __hash__(self):
        return hash(self.options.debugger_address)


def find_chrome_executable():
    from seleniumbase.core import detect_b_ver
    binary_location = detect_b_ver.get_binary_location("google-chrome", True)
    if os.path.exists(binary_location) and os.access(binary_location, os.X_OK):
        return os.path.normpath(binary_location)

    candidates = set()
    if IS_POSIX:
        for item in os.environ.get("PATH").split(os.pathsep):
            for subitem in (
                "chromium",
                "google-chrome",
                "chromium-browser",
                "chrome",
                "google-chrome-stable",
                "google-chrome-beta",
                "google-chrome-dev",
                "google-chrome-unstable",
            ):
                candidates.add(os.sep.join((item, subitem)))
        if "darwin" in sys.platform:
            gc = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            candidates.update(
                [
                    gc, "/Applications/Chromium.app/Contents/MacOS/Chromium"
                ]
            )
    else:
        for item in map(
            os.environ.get,
            (
                "PROGRAMFILES",
                "PROGRAMFILES(X86)",
                "LOCALAPPDATA",
                "PROGRAMW6432",
            ),
        ):
            for subitem in (
                "Google/Chrome/Application",
                "Google/Chrome Beta/Application",
                "Google/Chrome Canary/Application",
            ):
                candidates.add(os.sep.join((item, subitem, "chrome.exe")))
    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return os.path.normpath(candidate)
    return None  # Browser not found!
