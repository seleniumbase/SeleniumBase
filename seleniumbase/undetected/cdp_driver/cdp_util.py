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
    if IS_LINUX and (not headed or xvfb):
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
                    _xvfb_display.start()
                    if "DISPLAY" not in os.environ.keys():
                        print(
                            "\nX11 display failed! Will use regular xvfb!"
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
                        if pyautogui.__version__ != use_pyautogui_ver:
                            del pyautogui  # To get newer ver
                            shared_utils.pip_install(
                                "pyautogui", version=use_pyautogui_ver
                            )
                            import pyautogui
                    pyautogui_is_installed = True
                except Exception:
                    message = (
                        "PyAutoGUI is required for UC Mode on Linux! "
                        "Installing now..."
                    )
                    print("\n" + message)
                    shared_utils.pip_install(
                        "pyautogui", version=constants.PyAutoGUI.VER
                    )
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
    headless: Optional[bool] = False,
    incognito: Optional[bool] = False,
    guest: Optional[bool] = False,
    browser_executable_path: Optional[PathLike] = None,
    browser_args: Optional[List[str]] = None,
    xvfb_metrics: Optional[List[str]] = None,  # "Width,Height" for Linux
    ad_block: Optional[bool] = False,
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
    if IS_LINUX and not headless and not headed and not xvfb:
        xvfb = True  # The default setting on Linux
    __activate_virtual_display_as_needed(headless, headed, xvfb, xvfb_metrics)
    if proxy and "@" in str(proxy):
        user_with_pass = proxy.split("@")[0]
        if ":" in user_with_pass:
            proxy_user = user_with_pass.split(":")[0]
            proxy_pass = user_with_pass.split(":")[1]
            proxy_string = proxy.split("@")[1]
            extension_dir = __add_chrome_proxy_extension(
                extension_dir,
                proxy_string,
                proxy_user,
                proxy_pass,
            )
    if ad_block:
        incognito = False
        guest = False
        ad_block_zip = AD_BLOCK_ZIP_PATH
        ad_block_dir = os.path.join(DOWNLOADS_FOLDER, "ad_block")
        __unzip_to_new_folder(ad_block_zip, ad_block_dir)
        extension_dir = __add_chrome_ext_dir(extension_dir, ad_block_dir)
    if (
        "binary_location" in kwargs
        and not browser_executable_path
    ):
        browser_executable_path = kwargs["binary_location"]
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
    if proxy and "@" in str(proxy):
        time.sleep(0.15)
    if lang:
        sb_config._cdp_locale = lang
    elif "locale" in kwargs:
        sb_config._cdp_locale = kwargs["locale"]
    elif "locale_code" in kwargs:
        sb_config._cdp_locale = kwargs["locale_code"]
    else:
        sb_config._cdp_locale = None
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
    else:
        sb_config._cdp_platform = None
    return driver


async def start_async(*args, **kwargs) -> Browser:
    headless = False
    binary_location = None
    if "browser_executable_path" in kwargs:
        binary_location = kwargs["browser_executable_path"]
    else:
        binary_location = detect_b_ver.get_binary_location("google-chrome")
        if binary_location and not os.path.exists(binary_location):
            binary_location = None
    if (
        shared_utils.is_chrome_130_or_newer(binary_location)
        and "user_data_dir" in kwargs
        and kwargs["user_data_dir"]
    ):
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
    headless = False
    binary_location = None
    if "browser_executable_path" in kwargs:
        binary_location = kwargs["browser_executable_path"]
    else:
        binary_location = detect_b_ver.get_binary_location("google-chrome")
        if binary_location and not os.path.exists(binary_location):
            binary_location = None
    if (
        shared_utils.is_chrome_130_or_newer(binary_location)
        and "user_data_dir" in kwargs
        and kwargs["user_data_dir"]
    ):
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
    """Create a Browser instance from a running driver instance."""
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

def get_cf_template() -> bytearray:
    """
    this returns a 36x36 px image of a cf checkbox
    """
    return bytearray(
        [
            255,
            216,
            255,
            224,
            0,
            16,
            74,
            70,
            73,
            70,
            0,
            1,
            1,
            1,
            0,
            96,
            0,
            96,
            0,
            0,
            255,
            219,
            0,
            67,
            0,
            2,
            1,
            1,
            2,
            1,
            1,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            3,
            5,
            3,
            3,
            3,
            3,
            3,
            6,
            4,
            4,
            3,
            5,
            7,
            6,
            7,
            7,
            7,
            6,
            7,
            7,
            8,
            9,
            11,
            9,
            8,
            8,
            10,
            8,
            7,
            7,
            10,
            13,
            10,
            10,
            11,
            12,
            12,
            12,
            12,
            7,
            9,
            14,
            15,
            13,
            12,
            14,
            11,
            12,
            12,
            12,
            255,
            219,
            0,
            67,
            1,
            2,
            2,
            2,
            3,
            3,
            3,
            6,
            3,
            3,
            6,
            12,
            8,
            7,
            8,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            12,
            255,
            192,
            0,
            17,
            8,
            0,
            61,
            0,
            43,
            3,
            1,
            34,
            0,
            2,
            17,
            1,
            3,
            17,
            1,
            255,
            196,
            0,
            31,
            0,
            0,
            1,
            5,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            255,
            196,
            0,
            181,
            16,
            0,
            2,
            1,
            3,
            3,
            2,
            4,
            3,
            5,
            5,
            4,
            4,
            0,
            0,
            1,
            125,
            1,
            2,
            3,
            0,
            4,
            17,
            5,
            18,
            33,
            49,
            65,
            6,
            19,
            81,
            97,
            7,
            34,
            113,
            20,
            50,
            129,
            145,
            161,
            8,
            35,
            66,
            177,
            193,
            21,
            82,
            209,
            240,
            36,
            51,
            98,
            114,
            130,
            9,
            10,
            22,
            23,
            24,
            25,
            26,
            37,
            38,
            39,
            40,
            41,
            42,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            115,
            116,
            117,
            118,
            119,
            120,
            121,
            122,
            131,
            132,
            133,
            134,
            135,
            136,
            137,
            138,
            146,
            147,
            148,
            149,
            150,
            151,
            152,
            153,
            154,
            162,
            163,
            164,
            165,
            166,
            167,
            168,
            169,
            170,
            178,
            179,
            180,
            181,
            182,
            183,
            184,
            185,
            186,
            194,
            195,
            196,
            197,
            198,
            199,
            200,
            201,
            202,
            210,
            211,
            212,
            213,
            214,
            215,
            216,
            217,
            218,
            225,
            226,
            227,
            228,
            229,
            230,
            231,
            232,
            233,
            234,
            241,
            242,
            243,
            244,
            245,
            246,
            247,
            248,
            249,
            250,
            255,
            196,
            0,
            31,
            1,
            0,
            3,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            255,
            196,
            0,
            181,
            17,
            0,
            2,
            1,
            2,
            4,
            4,
            3,
            4,
            7,
            5,
            4,
            4,
            0,
            1,
            2,
            119,
            0,
            1,
            2,
            3,
            17,
            4,
            5,
            33,
            49,
            6,
            18,
            65,
            81,
            7,
            97,
            113,
            19,
            34,
            50,
            129,
            8,
            20,
            66,
            145,
            161,
            177,
            193,
            9,
            35,
            51,
            82,
            240,
            21,
            98,
            114,
            209,
            10,
            22,
            36,
            52,
            225,
            37,
            241,
            23,
            24,
            25,
            26,
            38,
            39,
            40,
            41,
            42,
            53,
            54,
            55,
            56,
            57,
            58,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            115,
            116,
            117,
            118,
            119,
            120,
            121,
            122,
            130,
            131,
            132,
            133,
            134,
            135,
            136,
            137,
            138,
            146,
            147,
            148,
            149,
            150,
            151,
            152,
            153,
            154,
            162,
            163,
            164,
            165,
            166,
            167,
            168,
            169,
            170,
            178,
            179,
            180,
            181,
            182,
            183,
            184,
            185,
            186,
            194,
            195,
            196,
            197,
            198,
            199,
            200,
            201,
            202,
            210,
            211,
            212,
            213,
            214,
            215,
            216,
            217,
            218,
            226,
            227,
            228,
            229,
            230,
            231,
            232,
            233,
            234,
            242,
            243,
            244,
            245,
            246,
            247,
            248,
            249,
            250,
            255,
            218,
            0,
            12,
            3,
            1,
            0,
            2,
            17,
            3,
            17,
            0,
            63,
            0,
            253,
            233,
            223,
            245,
            252,
            205,
            27,
            254,
            191,
            153,
            164,
            162,
            128,
            23,
            127,
            215,
            243,
            52,
            111,
            250,
            254,
            102,
            146,
            138,
            0,
            93,
            255,
            0,
            95,
            204,
            209,
            191,
            235,
            249,
            154,
            74,
            40,
            0,
            81,
            184,
            226,
            188,
            151,
            246,
            190,
            248,
            249,
            172,
            252,
            8,
            240,
            47,
            135,
            191,
            225,
            27,
            211,
            244,
            221,
            67,
            196,
            222,
            50,
            241,
            21,
            143,
            134,
            116,
            149,
            212,
            93,
            214,
            206,
            11,
            155,
            166,
            125,
            173,
            48,
            79,
            156,
            162,
            132,
            109,
            219,
            78,
            125,
            187,
            87,
            173,
            117,
            175,
            157,
            127,
            224,
            161,
            169,
            153,
            126,
            4,
            252,
            199,
            254,
            74,
            255,
            0,
            135,
            207,
            65,
            235,
            56,
            253,
            122,
            253,
            104,
            1,
            194,
            211,
            246,
            186,
            56,
            255,
            0,
            147,
            114,
            92,
            246,
            39,
            89,
            227,
            219,
            173,
            13,
            101,
            251,
            94,
            227,
            129,
            251,
            55,
            231,
            182,
            91,
            90,
            255,
            0,
            10,
            250,
            112,
            46,
            40,
            52,
            1,
            243,
            135,
            192,
            159,
            143,
            63,
            17,
            227,
            253,
            163,
            245,
            47,
            133,
            255,
            0,
            20,
            52,
            239,
            5,
            255,
            0,
            109,
            47,
            135,
            19,
            197,
            54,
            55,
            222,
            23,
            146,
            228,
            90,
            27,
            111,
            180,
            155,
            102,
            138,
            65,
            113,
            243,
            25,
            4,
            152,
            228,
            96,
            99,
            181,
            123,
            207,
            217,
            238,
            38,
            1,
            163,
            41,
            180,
            129,
            214,
            50,
            121,
            239,
            220,
            119,
            205,
            124,
            243,
            122,
            79,
            252,
            61,
            209,
            121,
            111,
            249,
            36,
            28,
            115,
            235,
            173,
            100,
            254,
            120,
            175,
            122,
            190,
            138,
            75,
            139,
            157,
            227,
            31,
            50,
            169,
            253,
            5,
            76,
            164,
            146,
            187,
            42,
            49,
            230,
            118,
            69,
            225,
            244,
            207,
            183,
            173,
            124,
            231,
            255,
            0,
            5,
            13,
            98,
            37,
            248,
            19,
            207,
            252,
            213,
            255,
            0,
            15,
            243,
            183,
            140,
            127,
            164,
            115,
            159,
            114,
            56,
            246,
            175,
            163,
            1,
            193,
            174,
            31,
            227,
            223,
            192,
            13,
            11,
            246,
            138,
            240,
            36,
            122,
            14,
            185,
            38,
            165,
            106,
            182,
            183,
            112,
            223,
            216,
            223,
            105,
            215,
            31,
            103,
            189,
            211,
            110,
            97,
            109,
            209,
            77,
            12,
            152,
            33,
            93,
            50,
            64,
            56,
            56,
            201,
            239,
            205,
            81,
            39,
            165,
            111,
            250,
            143,
            194,
            130,
            192,
            142,
            162,
            190,
            97,
            31,
            240,
            78,
            221,
            189,
            62,
            59,
            126,
            209,
            139,
            129,
            129,
            143,
            25,
            244,
            31,
            247,
            230,
            134,
            255,
            0,
            130,
            118,
            179,
            46,
            63,
            225,
            124,
            126,
            210,
            60,
            250,
            120,
            220,
            255,
            0,
            241,
            154,
            0,
            146,
            236,
            19,
            255,
            0,
            5,
            115,
            94,
            159,
            242,
            72,
            14,
            125,
            71,
            252,
            78,
            128,
            233,
            239,
            95,
            68,
            21,
            205,
            121,
            55,
            192,
            111,
            216,
            251,
            67,
            248,
            19,
            227,
            77,
            75,
            196,
            191,
            240,
            144,
            120,
            211,
            198,
            94,
            36,
            212,
            173,
            19,
            79,
            58,
            175,
            138,
            53,
            95,
            237,
            27,
            171,
            123,
            85,
            98,
            226,
            8,
            219,
            106,
            225,
            55,
            157,
            220,
            130,
            114,
            58,
            215,
            172,
            209,
            107,
            134,
            250,
            133,
            20,
            81,
            64,
            5,
            20,
            81,
            64,
            5,
            20,
            81,
            64,
            31,
            255,
            217,
        ]
    )
