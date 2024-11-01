"""CDP-Driver is based on NoDriver"""
from __future__ import annotations
import asyncio
import fasteners
import logging
import os
import time
import types
import typing
from contextlib import suppress
from seleniumbase import config as sb_config
from seleniumbase.config import settings
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
    sandbox: Optional[bool] = True,
    lang: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    xvfb: Optional[int] = None,  # Use a special virtual display on Linux
    headed: Optional[bool] = None,  # Override default Xvfb mode on Linux
    expert: Optional[bool] = None,  # Open up closed Shadow-root elements
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
            **kwargs,
        )
    return await Browser.create(config)


async def start_async(*args, **kwargs) -> Browser:
    headless = False
    binary_location = None
    if "browser_executable_path" in kwargs:
        binary_location = kwargs["browser_executable_path"]
    if shared_utils.is_chrome_130_or_newer(binary_location):
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
    loop = asyncio.get_event_loop()
    headless = False
    binary_location = None
    if "browser_executable_path" in kwargs:
        binary_location = kwargs["browser_executable_path"]
    if shared_utils.is_chrome_130_or_newer(binary_location):
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
    driver.service.stop()
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
