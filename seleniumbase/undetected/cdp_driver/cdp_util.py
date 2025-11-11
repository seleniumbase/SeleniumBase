"""CDP-Driver is based on NoDriver"""
from __future__ import annotations
import asyncio
import fasteners
import logging
import os
import sys
import time
import types
import typing
from contextlib import suppress
from seleniumbase import config as sb_config
from seleniumbase import extensions
from seleniumbase.config import settings
from seleniumbase.core import detect_b_ver
from seleniumbase.core import download_helper
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import shared_utils
from typing import Optional, List, Union, Callable
from .element import Element
from .browser import Browser
from .browser import PathLike
from .config import Config
from .tab import Tab
import mycdp as cdp

logger = logging.getLogger(__name__)
IS_LINUX = shared_utils.is_linux()
DOWNLOADS_FOLDER = download_helper.get_downloads_folder()
PROXY_DIR_LOCK = proxy_helper.PROXY_DIR_LOCK
EXTENSIONS_DIR = os.path.dirname(os.path.realpath(extensions.__file__))
AD_BLOCK_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "ad_block.zip")
T = typing.TypeVar("T")


def __activate_standard_virtual_display():
    from sbvirtualdisplay import Display
    width = settings.HEADLESS_START_WIDTH
    height = settings.HEADLESS_START_HEIGHT
    with suppress(Exception):
        _xvfb_display = Display(
            visible=0, size=(width, height)
        )
        _xvfb_display.start()
        sb_config._virtual_display = _xvfb_display
        sb_config.headless_active = True


def __activate_virtual_display_as_needed(
    headless, headed, xvfb, xvfb_metrics
):
    """This is only needed on Linux."""
    if (
        IS_LINUX
        and (not headed or xvfb)
        and (
            not hasattr(sb_config, "_virtual_display")
            or not sb_config._virtual_display
        )
    ):
        from sbvirtualdisplay import Display
        pip_find_lock = fasteners.InterProcessLock(
            constants.PipInstall.FINDLOCK
        )
        with pip_find_lock:  # Prevent issues with multiple processes
            if not headless:
                import Xlib.display
                try:
                    _xvfb_width = None
                    _xvfb_height = None
                    if xvfb_metrics:
                        with suppress(Exception):
                            metrics_string = xvfb_metrics
                            metrics_string = metrics_string.replace(" ", "")
                            metrics_list = metrics_string.split(",")[0:2]
                            _xvfb_width = int(metrics_list[0])
                            _xvfb_height = int(metrics_list[1])
                            # The minimum width,height is: 1024,768
                            if _xvfb_width < 1024:
                                _xvfb_width = 1024
                            sb_config._xvfb_width = _xvfb_width
                            if _xvfb_height < 768:
                                _xvfb_height = 768
                            sb_config._xvfb_height = _xvfb_height
                            xvfb = True
                    if not _xvfb_width:
                        _xvfb_width = 1366
                    if not _xvfb_height:
                        _xvfb_height = 768
                    _xvfb_display = Display(
                        visible=True,
                        size=(_xvfb_width, _xvfb_height),
                        backend="xvfb",
                        use_xauth=True,
                    )
                    if "--debug-display" in sys.argv:
                        print(
                            "Starting VDisplay from cdp_util: (%s, %s)"
                            % (_xvfb_width, _xvfb_height)
                        )
                    _xvfb_display.start()
                    if "DISPLAY" not in os.environ.keys():
                        print(
                            "\n  X11 display failed! Is Xvfb installed? "
                            "\n  Try this: `sudo apt install -y xvfb`"
                        )
                        __activate_standard_virtual_display()
                    else:
                        sb_config._virtual_display = _xvfb_display
                        sb_config.headless_active = True
                except Exception as e:
                    if hasattr(e, "msg"):
                        print("\n" + str(e.msg))
                    else:
                        print(e)
                    print("\nX11 display failed! Will use regular xvfb!")
                    __activate_standard_virtual_display()
                    return
                pyautogui_is_installed = False
                try:
                    import pyautogui
                    with suppress(Exception):
                        use_pyautogui_ver = constants.PyAutoGUI.VER
                        u_pv = shared_utils.make_version_tuple(
                            use_pyautogui_ver
                        )
                        pv = shared_utils.make_version_tuple(
                            pyautogui.__version__
                        )
                        if pv < u_pv:
                            del pyautogui  # To get newer ver
                            shared_utils.pip_install(
                                "pyautogui", version="Latest"
                            )
                            import pyautogui
                    pyautogui_is_installed = True
                except Exception:
                    message = (
                        "PyAutoGUI is required for CDP Mode on Linux! "
                        "Installing now..."
                    )
                    print("\n" + message)
                    shared_utils.pip_install("pyautogui", version="Latest")
                    import pyautogui
                    pyautogui_is_installed = True
                if (
                    pyautogui_is_installed
                    and hasattr(pyautogui, "_pyautogui_x11")
                ):
                    try:
                        pyautogui._pyautogui_x11._display = (
                            Xlib.display.Display(os.environ['DISPLAY'])
                        )
                        sb_config._pyautogui_x11_display = (
                            pyautogui._pyautogui_x11._display
                        )
                    except Exception as e:
                        if hasattr(e, "msg"):
                            print("\n" + str(e.msg))
                        else:
                            print(e)
            else:
                __activate_standard_virtual_display()


def __set_proxy_filenames():
    DOWNLOADS_DIR = constants.Files.DOWNLOADS_FOLDER
    for num in range(1000):
        PROXY_DIR_PATH = os.path.join(DOWNLOADS_DIR, "proxy_ext_dir_%s" % num)
        if os.path.exists(PROXY_DIR_PATH):
            continue
        proxy_helper.PROXY_DIR_PATH = PROXY_DIR_PATH
        return
    # Exceeded upper bound. Use Defaults:
    PROXY_DIR_PATH = os.path.join(DOWNLOADS_DIR, "proxy_ext_dir")
    proxy_helper.PROXY_DIR_PATH = PROXY_DIR_PATH


def __add_chrome_ext_dir(extension_dir, dir_path):
    # Add dir_path to the existing extension_dir
    option_exists = False
    if extension_dir:
        option_exists = True
        extension_dir = "%s,%s" % (
            extension_dir, os.path.realpath(dir_path)
        )
    if not option_exists:
        extension_dir = os.path.realpath(dir_path)
    return extension_dir


def __unzip_to_new_folder(zip_file, folder):
    proxy_dir_lock = fasteners.InterProcessLock(PROXY_DIR_LOCK)
    with proxy_dir_lock:
        with suppress(Exception):
            shared_utils.make_writable(PROXY_DIR_LOCK)
        if not os.path.exists(folder):
            import zipfile
            zip_ref = zipfile.ZipFile(zip_file, "r")
            os.makedirs(folder)
            zip_ref.extractall(folder)
            zip_ref.close()


def __add_chrome_proxy_extension(
    extension_dir,
    proxy_string,
    proxy_user,
    proxy_pass,
    proxy_scheme="http",
    proxy_bypass_list=None,
    multi_proxy=False,
):
    """Implementation of https://stackoverflow.com/a/35293284/7058266
    for https://stackoverflow.com/q/12848327/7058266
    (Run Selenium on a proxy server that requires authentication.)"""
    args = " ".join(sys.argv)
    bypass_list = proxy_bypass_list
    if (
        not ("-n" in sys.argv or " -n=" in args or args == "-c")
        and not multi_proxy
    ):
        # Single-threaded
        proxy_dir_lock = fasteners.InterProcessLock(PROXY_DIR_LOCK)
        with proxy_dir_lock:
            proxy_helper.create_proxy_ext(
                proxy_string,
                proxy_user,
                proxy_pass,
                proxy_scheme,
                bypass_list,
                zip_it=False,
            )
            proxy_dir_path = proxy_helper.PROXY_DIR_PATH
            extension_dir = __add_chrome_ext_dir(
                extension_dir, proxy_dir_path
            )
    else:
        # Multi-threaded
        proxy_dir_lock = fasteners.InterProcessLock(PROXY_DIR_LOCK)
        with proxy_dir_lock:
            with suppress(Exception):
                shared_utils.make_writable(PROXY_DIR_LOCK)
            if multi_proxy:
                __set_proxy_filenames()
            if not os.path.exists(proxy_helper.PROXY_DIR_PATH):
                proxy_helper.create_proxy_ext(
                    proxy_string,
                    proxy_user,
                    proxy_pass,
                    proxy_scheme,
                    bypass_list,
                    zip_it=False,
                )
            extension_dir = __add_chrome_ext_dir(
                extension_dir, proxy_helper.PROXY_DIR_PATH
            )
    return extension_dir


async def start(
    config: Optional[Config] = None,
    *,
    user_data_dir: Optional[PathLike] = None,
    headless: Optional[bool] = None,
    incognito: Optional[bool] = None,
    guest: Optional[bool] = None,
    browser_executable_path: Optional[PathLike] = None,
    browser_args: Optional[List[str]] = None,
    xvfb_metrics: Optional[List[str]] = None,  # "Width,Height" for Linux
    ad_block: Optional[bool] = None,
    sandbox: Optional[bool] = True,
    lang: Optional[str] = None,  # Set the Language Locale Code
    host: Optional[str] = None,  # Chrome remote-debugging-host
    port: Optional[int] = None,  # Chrome remote-debugging-port
    xvfb: Optional[int] = None,  # Use a special virtual display on Linux
    headed: Optional[bool] = None,  # Override default Xvfb mode on Linux
    expert: Optional[bool] = None,  # Open up closed Shadow-root elements
    agent: Optional[str] = None,  # Set the user-agent string
    proxy: Optional[str] = None,  # "host:port" or "user:pass@host:port"
    tzone: Optional[str] = None,  # Eg "America/New_York", "Asia/Kolkata"
    geoloc: Optional[list | tuple] = None,  # Eg (48.87645, 2.26340)
    extension_dir: Optional[str] = None,  # Chrome extension directory
    **kwargs: Optional[dict],
) -> Browser:
    """
    Helper function to launch a browser. It accepts several keyword parameters.
    Conveniently, you can just call it bare (no parameters) to quickly launch
    an instance with best practice defaults.
    Note: Due to a Chrome-130 bug, use start_async or start_sync instead.
     (Calling this method directly could lead to an unresponsive browser)
    Note: New args are expected: Use kwargs only!
    Note: This should be called ``await start()``
    :param user_data_dir:
    :type user_data_dir: PathLike
    :param headless:
    :type headless: bool
    :param browser_executable_path:
    :type browser_executable_path: PathLike
    :param browser_args:
     ["--some-chromeparam=somevalue", "some-other-param=someval"]
    :type browser_args: List[str]
    :param sandbox: Default True, but when set to False it adds --no-sandbox
     to the params, also when using linux under a root user,
     it adds False automatically (else Chrome won't start).
    :type sandbox: bool
    :param lang: language string
    :type lang: str
    :param port: If you connect to an existing debuggable session,
     you can specify the port here.
     If both host and port are provided,
     then a local Chrome browser will not be started!
    :type port: int
    :param host: If you connect to an existing debuggable session,
     you can specify the host here.
     If both host and port are provided,
     then a local Chrome browser will not be started!
    :type host: str
    :param expert: When set to True, "expert" mode is enabled.
     This means adding: --disable-web-security --disable-site-isolation-trials,
     as well as some scripts and patching useful for debugging.
     (For example, ensuring shadow-root is always in "open" mode.)
    :type expert: bool
    """
    sys_argv = sys.argv
    arg_join = " ".join(sys_argv)
    if headless is None:
        if "--headless" in sys_argv:
            headless = True
        else:
            headless = False
    if headed is None:
        if "--gui" in sys_argv or "--headed" in sys_argv:
            headed = True
        else:
            headed = False
    if xvfb is None:
        if "--xvfb" in sys_argv:
            xvfb = True
        else:
            xvfb = False
    if not hasattr(sb_config, "xvfb"):
        sb_config.xvfb = xvfb
    if incognito is None:
        if "--incognito" in sys_argv:
            incognito = True
        else:
            incognito = False
    if guest is None:
        if "--guest" in sys_argv:
            guest = True
        else:
            guest = False
    if ad_block is None:
        if "--ad-block" in sys_argv or "--ad_block" in sys_argv:
            ad_block = True
        else:
            ad_block = False
    if xvfb_metrics is None and "--xvfb-metrics" in arg_join:
        x_m = xvfb_metrics
        count = 0
        for arg in sys_argv:
            if arg.startswith("--xvfb-metrics="):
                x_m = arg.split("--xvfb-metrics=")[1]
                break
            elif arg == "--xvfb-metrics" and len(sys_argv) > count + 1:
                x_m = sys_argv[count + 1]
                if x_m.startswith("-"):
                    x_m = None
                break
            count += 1
        if x_m:
            if x_m.startswith('"') and x_m.endswith('"'):
                x_m = x_m[1:-1]
            elif x_m.startswith("'") and x_m.endswith("'"):
                x_m = x_m[1:-1]
        xvfb_metrics = x_m
    if agent is None and "user_agent" not in kwargs and "--agent" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--agent="):
                agent = arg.split("--agent=")[1]
                break
            elif arg == "--agent" and len(sys_argv) > count + 1:
                agent = sys_argv[count + 1]
                if agent.startswith("-"):
                    agent = None
                break
            count += 1
        if agent:
            if agent.startswith('"') and agent.endswith('"'):
                agent = agent[1:-1]
            elif agent.startswith("'") and agent.endswith("'"):
                agent = agent[1:-1]
    if (
        geoloc is None
        and "geolocation" not in kwargs
        and "--geolocation" in arg_join
    ):
        count = 0
        for arg in sys_argv:
            if arg.startswith("--geolocation="):
                geoloc = arg.split("--geolocation=")[1]
                break
            elif arg == "--geolocation" and len(sys_argv) > count + 1:
                geoloc = sys_argv[count + 1]
                if geoloc.startswith("-"):
                    geoloc = None
                break
            count += 1
        if geoloc:
            if geoloc.startswith('"') and geoloc.endswith('"'):
                geoloc = geoloc[1:-1]
            elif geoloc.startswith("'") and geoloc.endswith("'"):
                geoloc = geoloc[1:-1]
            if geoloc:
                import ast
                geoloc = ast.literal_eval(geoloc)
    if not lang and "locale" not in kwargs and "locale_code" not in kwargs:
        if "--locale" in arg_join:
            count = 0
            for arg in sys_argv:
                if arg.startswith("--locale="):
                    lang = arg.split("--locale=")[1]
                    break
                elif arg == "--locale" and len(sys_argv) > count + 1:
                    lang = sys_argv[count + 1]
                    if lang.startswith("-"):
                        lang = None
                    break
                count += 1
        elif "--lang" in arg_join:
            count = 0
            for arg in sys_argv:
                if arg.startswith("--lang="):
                    lang = arg.split("--lang=")[1]
                    break
                elif arg == "--lang" and len(sys_argv) > count + 1:
                    lang = sys_argv[count + 1]
                    if lang.startswith("-"):
                        lang = None
                    break
                count += 1
        if lang:
            if lang.startswith('"') and lang.endswith('"'):
                lang = lang[1:-1]
            elif lang.startswith("'") and lang.endswith("'"):
                lang = lang[1:-1]
    if not browser_executable_path and "binary_location" not in kwargs:
        bin_loc = None
        if "--binary-location" in arg_join or "--binary_location" in arg_join:
            bin_loc_cmd = "--binary-location"
            if "--binary_location" in arg_join:
                bin_loc_cmd = "--binary_location"
            count = 0
            bin_loc = None
            for arg in sys_argv:
                if arg.startswith("%s=" % bin_loc_cmd):
                    bin_loc = arg.split("%s=" % bin_loc_cmd)[1]
                    break
                elif arg == bin_loc_cmd and len(sys_argv) > count + 1:
                    bin_loc = sys_argv[count + 1]
                    if bin_loc.startswith("-"):
                        bin_loc = None
                    break
                count += 1
        elif "--bl=" in arg_join:
            count = 0
            bin_loc = None
            for arg in sys_argv:
                if arg.startswith("--bl="):
                    bin_loc = arg.split("--bl=")[1]
                    break
                count += 1
        if bin_loc:
            if bin_loc.startswith('"') and bin_loc.endswith('"'):
                bin_loc = bin_loc[1:-1]
            elif bin_loc.startswith("'") and bin_loc.endswith("'"):
                bin_loc = bin_loc[1:-1]
            if bin_loc and not os.path.exists(bin_loc):
                print("  No browser executable at PATH {%s}! " % bin_loc)
                print("  Using default Chrome browser instead!")
                bin_loc = None
            browser_executable_path = bin_loc
    if proxy is None and "--proxy" in arg_join:
        proxy_string = None
        if "--proxy=" in arg_join:
            proxy_string = arg_join.split("--proxy=")[1].split(" ")[0]
        elif "--proxy " in arg_join:
            proxy_string = arg_join.split("--proxy ")[1].split(" ")[0]
        if proxy_string:
            if proxy_string.startswith('"') and proxy_string.endswith('"'):
                proxy_string = proxy_string[1:-1]
            elif proxy_string.startswith("'") and proxy_string.endswith("'"):
                proxy_string = proxy_string[1:-1]
            proxy = proxy_string
    if tzone is None and "timezone" not in kwargs and "--timezone" in arg_join:
        tz_string = None
        if "--timezone=" in arg_join:
            tz_string = arg_join.split("--timezone=")[1].split(" ")[0]
        elif "--timezone " in arg_join:
            tz_string = arg_join.split("--timezone ")[1].split(" ")[0]
        if tz_string:
            if tz_string.startswith('"') and tz_string.endswith('"'):
                tz_string = proxy_string[1:-1]
            elif tz_string.startswith("'") and tz_string.endswith("'"):
                tz_string = proxy_string[1:-1]
            tzone = tz_string
    platform_var = None
    if (
        "platform" not in kwargs
        and "plat" not in kwargs
        and "--platform" in arg_join
    ):
        count = 0
        for arg in sys_argv:
            if arg.startswith("--platform="):
                platform_var = arg.split("--platform=")[1]
                break
            elif arg == "--platform" and len(sys_argv) > count + 1:
                platform_var = sys_argv[count + 1]
                if platform_var.startswith("-"):
                    platform_var = None
                break
            count += 1
        if platform_var:
            if platform_var.startswith('"') and platform_var.endswith('"'):
                platform_var = platform_var[1:-1]
            elif platform_var.startswith("'") and platform_var.endswith("'"):
                platform_var = platform_var[1:-1]
    if IS_LINUX and not headless and not headed and not xvfb:
        xvfb = True  # The default setting on Linux
    __activate_virtual_display_as_needed(headless, headed, xvfb, xvfb_metrics)
    if proxy and "@" in str(proxy):
        user_with_pass = proxy.split("@")[0]
        if ":" in user_with_pass:
            proxy_user = user_with_pass.split(":")[0]
            proxy_pass = user_with_pass.split(":")[1]
            proxy_string = proxy.split("@")[1]
            proxy_string, proxy_scheme = proxy_helper.validate_proxy_string(
                proxy_string, keep_scheme=True
            )
            extension_dir = __add_chrome_proxy_extension(
                extension_dir,
                proxy_string,
                proxy_user,
                proxy_pass,
                proxy_scheme,
            )
    if ad_block:
        sb_config.ad_block_on = True
        incognito = False
        guest = False
        ad_block_zip = AD_BLOCK_ZIP_PATH
        ad_block_dir = os.path.join(DOWNLOADS_FOLDER, "ad_block")
        __unzip_to_new_folder(ad_block_zip, ad_block_dir)
        extension_dir = __add_chrome_ext_dir(extension_dir, ad_block_dir)
    if "binary_location" in kwargs and not browser_executable_path:
        browser_executable_path = kwargs["binary_location"]
    if not browser_executable_path:
        browser = None
        if "browser" in kwargs:
            browser = kwargs["browser"]
        if not browser and "--browser" in arg_join:
            br_string = None
            if "--browser=" in arg_join:
                br_string = arg_join.split("--browser=")[1].split(" ")[0]
            elif "--browser " in arg_join:
                br_string = arg_join.split("--browser ")[1].split(" ")[0]
            if br_string:
                if br_string.startswith('"') and br_string.endswith('"'):
                    br_string = proxy_string[1:-1]
                elif br_string.startswith("'") and br_string.endswith("'"):
                    br_string = proxy_string[1:-1]
                browser = br_string
        if not browser:
            if "--edge" in sys_argv:
                browser = "edge"
            elif "--opera" in sys_argv:
                browser = "opera"
            elif "--brave" in sys_argv:
                browser = "brave"
            elif "--comet" in sys_argv:
                browser = "comet"
            elif "--atlas" in sys_argv:
                browser = "atlas"
            else:
                browser = "chrome"
        sb_config._cdp_browser = browser
        if browser == "comet" or browser == "atlas":
            incognito = False
            guest = False
        with suppress(Exception):
            browser_binary = detect_b_ver.get_binary_location(browser)
            if browser_binary and os.path.exists(browser_binary):
                browser_executable_path = browser_binary
    else:
        bin_loc = str(browser_executable_path).lower()
        if bin_loc.endswith("opera") or bin_loc.endswith("opera.exe"):
            sb_config._cdp_browser = "opera"
        elif bin_loc.endswith("edge") or bin_loc.endswith("edge.exe"):
            sb_config._cdp_browser = "edge"
        elif bin_loc.endswith("brave") or bin_loc.endswith("brave.exe"):
            sb_config._cdp_browser = "brave"
        elif bin_loc.endswith("comet") or bin_loc.endswith("comet.exe"):
            sb_config._cdp_browser = "comet"
        elif bin_loc.endswith("atlas") or bin_loc.endswith("atlas.exe"):
            sb_config._cdp_browser = "atlas"
        else:
            sb_config._cdp_browser = "chrome"
    if not config:
        config = Config(
            user_data_dir,
            headless,
            incognito,
            guest,
            browser_executable_path,
            browser_args,
            sandbox,
            lang,
            host=host,
            port=port,
            expert=expert,
            proxy=proxy,
            extension_dir=extension_dir,
            **kwargs,
        )
    driver = None
    try:
        driver = await Browser.create(config)
    except Exception:
        time.sleep(0.15)
        driver = await Browser.create(config)
    if proxy:
        sb_config._cdp_proxy = proxy
        if "@" in str(proxy):
            time.sleep(0.15)
    if lang:
        sb_config._cdp_locale = lang
    elif "locale" in kwargs:
        sb_config._cdp_locale = kwargs["locale"]
    elif "locale_code" in kwargs:
        sb_config._cdp_locale = kwargs["locale_code"]
    if tzone:
        sb_config._cdp_timezone = tzone
    elif "timezone" in kwargs:
        sb_config._cdp_timezone = kwargs["timezone"]
    else:
        sb_config._cdp_timezone = None
    if geoloc:
        sb_config._cdp_geolocation = geoloc
    elif "geolocation" in kwargs:
        sb_config._cdp_geolocation = kwargs["geolocation"]
    else:
        sb_config._cdp_geolocation = None
    if agent:
        sb_config._cdp_user_agent = agent
    elif "user_agent" in kwargs:
        sb_config._cdp_user_agent = kwargs["user_agent"]
    else:
        sb_config._cdp_user_agent = None
    if "platform" in kwargs:
        sb_config._cdp_platform = kwargs["platform"]
    elif "plat" in kwargs:
        sb_config._cdp_platform = kwargs["plat"]
    elif platform_var:
        sb_config._cdp_platform = platform_var
    else:
        sb_config._cdp_platform = None
    return driver


async def start_async(*args, **kwargs) -> Browser:
    if "user_data_dir" in kwargs and kwargs["user_data_dir"]:
        headless = False
        if "headless" in kwargs:
            headless = kwargs["headless"]
        decoy_args = kwargs
        decoy_args["headless"] = True
        driver = await start(**decoy_args)
        kwargs["headless"] = headless
        kwargs["user_data_dir"] = driver.config.user_data_dir
        time.sleep(0.2)
        driver.stop()  # Due to Chrome-130, must stop & start
        time.sleep(0.1)
    return await start(*args, **kwargs)


def start_sync(*args, **kwargs) -> Browser:
    loop = None
    if (
        "loop" in kwargs
        and kwargs["loop"]
        and hasattr(kwargs["loop"], "create_task")
    ):
        loop = kwargs["loop"]
    else:
        loop = asyncio.new_event_loop()
    if "user_data_dir" in kwargs and kwargs["user_data_dir"]:
        headless = False
        if "headless" in kwargs:
            headless = kwargs["headless"]
        decoy_args = kwargs
        decoy_args["headless"] = True
        driver = loop.run_until_complete(start(**decoy_args))
        kwargs["headless"] = headless
        kwargs["user_data_dir"] = driver.config.user_data_dir
        time.sleep(0.2)
        driver.stop()  # Due to Chrome-130, must stop & start
        time.sleep(0.1)
    return loop.run_until_complete(start(*args, **kwargs))


async def create_from_driver(driver) -> Browser:
    """Create a CDP Browser instance from a running UC driver.
    This method is DEPRECATED in favor of activate_cdp_mode(),
     which includes the option of switching between the modes,
     and also properly handles configuration based on options."""
    from .config import Config

    conf = Config()
    host, port = driver.options.debugger_address.split(":")
    conf.host, conf.port = host, int(port)
    # Create Browser instance
    browser = await start(conf)
    browser._process_pid = driver.browser_pid
    # Stop chromedriver binary
    try:
        driver.service.send_remote_shutdown_command()
    except TypeError:
        pass
    finally:
        with suppress(Exception):
            driver.service._terminate_process()
    driver.browser_pid = -1
    driver.user_data_dir = None
    return browser


def free_port() -> int:
    """Determines a free port using sockets."""
    import socket

    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(("127.0.0.1", 0))
    free_socket.listen(5)
    port: int = free_socket.getsockname()[1]
    free_socket.close()
    return port


def filter_recurse_all(
    doc: T, predicate: Callable[[cdp.dom.Node, Element], bool]
) -> List[T]:
    """
    Test each child using predicate(child),
    and return all children for which predicate(child) == True
    :param doc: The cdp.dom.Node object or :py:class:`cdp_driver.Element`
    :param predicate: A function which takes a node as first parameter
     and returns a boolean, where True means include.
    """
    if not hasattr(doc, "children"):
        raise TypeError("Object should have a .children attribute!")
    out = []
    if doc and doc.children:
        for child in doc.children:
            if predicate(child):
                out.append(child)
            if child.shadow_roots is not None:
                out.extend(
                    filter_recurse_all(child.shadow_roots[0], predicate)
                )
            out.extend(filter_recurse_all(child, predicate))
    return out


def filter_recurse(
    doc: T, predicate: Callable[[cdp.dom.Node, Element], bool]
) -> T:
    """
    Test each child using predicate(child),
    and return the first child of which predicate(child) == True
    :param doc: the cdp.dom.Node object or :py:class:`cdp_driver.Element`
    :param predicate: a function which takes a node as first parameter
     and returns a boolean, where True means include.
    """
    if not hasattr(doc, "children"):
        raise TypeError("Object should have a .children attribute!")
    if doc and doc.children:
        for child in doc.children:
            if predicate(child):
                return child
            if child.shadow_roots:
                shadow_root_result = filter_recurse(
                    child.shadow_roots[0], predicate
                )
                if shadow_root_result:
                    return shadow_root_result
            result = filter_recurse(child, predicate)
            if result:
                return result


def circle(
    x, y=None, radius=10, num=10, dir=0
) -> typing.Generator[typing.Tuple[float, float], None, None]:
    """
    A generator will calculate coordinates around a circle.
    :param x: start x position
    :type x: int
    :param y: start y position
    :type y: int
    :param radius: size of the circle
    :type radius: int
    :param num: the amount of points calculated
     (higher => slower, more cpu, but more detailed)
    :type num: int
    """
    import math

    r = radius
    w = num
    if not y:
        y = x
    a = int(x - r * 2)
    b = int(y - r * 2)
    m = (2 * math.pi) / w
    if dir == 0:
        # Regular direction
        ran = 0, w + 1, 1
    else:
        # Opposite direction
        ran = w + 1, 0, -1
    for i in range(*ran):
        x = a + r * math.sin(m * i)
        y = b + r * math.cos(m * i)
        yield x, y


def remove_from_tree(tree: cdp.dom.Node, node: cdp.dom.Node) -> cdp.dom.Node:
    if not hasattr(tree, "children"):
        raise TypeError("Object should have a .children attribute!")
    if tree and tree.children:
        for child in tree.children:
            if child.backend_node_id == node.backend_node_id:
                tree.children.remove(child)
            remove_from_tree(child, node)
    return tree


async def html_from_tree(
    tree: Union[cdp.dom.Node, Element], target: Tab
):
    if not hasattr(tree, "children"):
        raise TypeError("Object should have a .children attribute!")
    out = ""
    if tree and tree.children:
        for child in tree.children:
            if isinstance(child, Element):
                out += await child.get_html()
            else:
                out += await target.send(
                    cdp.dom.get_outer_html(
                        backend_node_id=child.backend_node_id
                    )
                )
            out += await html_from_tree(child, target)
    return out


def compare_target_info(
    info1: cdp.target.TargetInfo, info2: cdp.target.TargetInfo
) -> List[typing.Tuple[str, typing.Any, typing.Any]]:
    """
    When logging mode is set to debug, browser object will log when target info
    is changed. To provide more meaningful log messages,
    this function is called to check what has actually changed
    between the 2 (by simple dict comparison).
    It returns a list of tuples
        [ ... ( key_which_has_changed, old_value, new_value) ]
    :param info1:
    :param info2:
    """
    d1 = info1.__dict__
    d2 = info2.__dict__
    return [(k, v, d2[k]) for (k, v) in d1.items() if d2[k] != v]


def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def cdp_get_module(domain: Union[str, types.ModuleType]):
    """
    Get cdp module by given string.
    :param domain:
    """
    import importlib

    if isinstance(domain, types.ModuleType):
        domain_mod = domain
    else:
        try:
            if domain in ("input",):
                domain = "input_"
            domain_mod = getattr(cdp, domain)
            if not domain_mod:
                raise AttributeError
        except AttributeError:
            try:
                domain_mod = importlib.import_module(domain)
            except ModuleNotFoundError:
                raise ModuleNotFoundError(
                    "Could not find cdp module from input '%s'" % domain
                )
    return domain_mod
