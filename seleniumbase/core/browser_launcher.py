import fasteners
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import types
import urllib3
import warnings
from contextlib import suppress
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.common.service import utils as service_utils
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from seleniumbase import config as sb_config
from seleniumbase import decorators
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
from seleniumbase import extensions  # browser extensions storage folder
from seleniumbase.config import settings
from seleniumbase.core import detect_b_ver
from seleniumbase.core import download_helper
from seleniumbase.core import proxy_helper
from seleniumbase.core import sb_driver
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import js_utils
from seleniumbase.fixtures import page_actions
from seleniumbase.fixtures import shared_utils

urllib3.disable_warnings()
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
# Make sure that the SeleniumBase DRIVER_DIR is at the top of the System PATH
# (Changes to the System PATH with os.environ only last during the test run)
if not os.environ["PATH"].startswith(DRIVER_DIR):
    # Remove existing SeleniumBase DRIVER_DIR from System PATH if present
    os.environ["PATH"] = os.environ["PATH"].replace(DRIVER_DIR, "")
    # If two path separators are next to each other, replace with just one
    os.environ["PATH"] = os.environ["PATH"].replace(
        os.pathsep + os.pathsep, os.pathsep
    )
    # Put the SeleniumBase DRIVER_DIR at the beginning of the System PATH
    os.environ["PATH"] = DRIVER_DIR + os.pathsep + os.environ["PATH"]
EXTENSIONS_DIR = os.path.dirname(os.path.realpath(extensions.__file__))
DISABLE_CSP_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "disable_csp.zip")
AD_BLOCK_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "ad_block.zip")
RECORDER_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "recorder.zip")
SBASE_EXT_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "sbase_ext.zip")
DOWNLOADS_FOLDER = download_helper.get_downloads_folder()
PROXY_ZIP_PATH = proxy_helper.PROXY_ZIP_PATH
PROXY_ZIP_LOCK = proxy_helper.PROXY_ZIP_LOCK
PROXY_DIR_PATH = proxy_helper.PROXY_DIR_PATH
PROXY_DIR_LOCK = proxy_helper.PROXY_DIR_LOCK
LOCAL_CHROMEDRIVER = None
LOCAL_GECKODRIVER = None
LOCAL_EDGEDRIVER = None
LOCAL_IEDRIVER = None
LOCAL_HEADLESS_IEDRIVER = None
LOCAL_UC_DRIVER = None
IS_ARM_MAC = shared_utils.is_arm_mac()
IS_MAC = shared_utils.is_mac()
IS_LINUX = shared_utils.is_linux()
IS_WINDOWS = shared_utils.is_windows()
if IS_MAC or IS_LINUX:
    LOCAL_CHROMEDRIVER = DRIVER_DIR + "/chromedriver"
    LOCAL_GECKODRIVER = DRIVER_DIR + "/geckodriver"
    LOCAL_EDGEDRIVER = DRIVER_DIR + "/msedgedriver"
    LOCAL_UC_DRIVER = DRIVER_DIR + "/uc_driver"
elif IS_WINDOWS:
    LOCAL_EDGEDRIVER = DRIVER_DIR + "/msedgedriver.exe"
    LOCAL_IEDRIVER = DRIVER_DIR + "/IEDriverServer.exe"
    LOCAL_HEADLESS_IEDRIVER = DRIVER_DIR + "/headless_ie_selenium.exe"
    LOCAL_CHROMEDRIVER = DRIVER_DIR + "/chromedriver.exe"
    LOCAL_GECKODRIVER = DRIVER_DIR + "/geckodriver.exe"
    LOCAL_UC_DRIVER = DRIVER_DIR + "/uc_driver.exe"
else:
    # Cannot determine system
    pass  # SeleniumBase will use web drivers from the System PATH by default


def log_d(message):
    """If setting sb_config.settings.HIDE_DRIVER_DOWNLOADS to True,
    output from driver downloads are logged instead of printed."""
    if (
        hasattr(settings, "HIDE_DRIVER_DOWNLOADS")
        and settings.HIDE_DRIVER_DOWNLOADS
    ):
        logging.debug(message)
    else:
        print(message)


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def make_driver_executable_if_not(driver_path):
    # Verify driver has executable permissions. If not, add them.
    permissions = oct(os.stat(driver_path)[0])[-3:]
    if "4" in permissions or "6" in permissions:
        # We want at least a '5' or '7' to make sure it's executable
        make_executable(driver_path)


def extend_driver(driver):
    # Extend the driver with new methods
    driver.default_find_element = driver.find_element
    driver.default_find_elements = driver.find_elements
    DM = sb_driver.DriverMethods(driver)
    driver.find_element = DM.find_element
    driver.find_elements = DM.find_elements
    driver.locator = DM.locator
    page = types.SimpleNamespace()
    page.open = DM.open_url
    page.click = DM.click
    page.click_link = DM.click_link
    page.click_if_visible = DM.click_if_visible
    page.click_active_element = DM.click_active_element
    page.send_keys = DM.send_keys
    page.press_keys = DM.press_keys
    page.type = DM.update_text
    page.submit = DM.submit
    page.assert_element = DM.assert_element_visible
    page.assert_element_present = DM.assert_element_present
    page.assert_element_not_visible = DM.assert_element_not_visible
    page.assert_text = DM.assert_text
    page.assert_exact_text = DM.assert_exact_text
    page.assert_non_empty_text = DM.assert_non_empty_text
    page.assert_text_not_visible = DM.assert_text_not_visible
    page.wait_for_element = DM.wait_for_element
    page.wait_for_text = DM.wait_for_text
    page.wait_for_exact_text = DM.wait_for_exact_text
    page.wait_for_non_empty_text = DM.wait_for_non_empty_text
    page.wait_for_text_not_visible = DM.wait_for_text_not_visible
    page.wait_for_and_accept_alert = DM.wait_for_and_accept_alert
    page.wait_for_and_dismiss_alert = DM.wait_for_and_dismiss_alert
    page.is_element_present = DM.is_element_present
    page.is_element_visible = DM.is_element_visible
    page.is_text_visible = DM.is_text_visible
    page.is_exact_text_visible = DM.is_exact_text_visible
    page.is_attribute_present = DM.is_attribute_present
    page.is_non_empty_text_visible = DM.is_non_empty_text_visible
    page.get_text = DM.get_text
    page.find_element = DM.find_element
    page.find_elements = DM.find_elements
    page.locator = DM.locator
    page.get_page_source = DM.get_page_source
    page.get_title = DM.get_title
    page.switch_to_default_window = DM.switch_to_default_window
    page.switch_to_newest_window = DM.switch_to_newest_window
    page.open_new_window = DM.open_new_window
    page.open_new_tab = DM.open_new_tab
    page.switch_to_window = DM.switch_to_window
    page.switch_to_tab = DM.switch_to_tab
    page.switch_to_frame = DM.switch_to_frame
    driver.page = page
    js = types.SimpleNamespace()
    js.js_click = DM.js_click
    js.get_active_element_css = DM.get_active_element_css
    js.get_locale_code = DM.get_locale_code
    js.get_origin = DM.get_origin
    js.get_user_agent = DM.get_user_agent
    js.highlight = DM.highlight
    driver.js = js
    driver.open = DM.open_url
    driver.click = DM.click
    driver.click_link = DM.click_link
    driver.click_if_visible = DM.click_if_visible
    driver.click_active_element = DM.click_active_element
    driver.send_keys = DM.send_keys
    driver.press_keys = DM.press_keys
    driver.type = DM.update_text
    driver.submit = DM.submit
    driver.assert_element = DM.assert_element_visible
    driver.assert_element_present = DM.assert_element_present
    driver.assert_element_not_visible = DM.assert_element_not_visible
    driver.assert_text = DM.assert_text
    driver.assert_exact_text = DM.assert_exact_text
    driver.assert_non_empty_text = DM.assert_non_empty_text
    driver.assert_text_not_visible = DM.assert_text_not_visible
    driver.wait_for_element = DM.wait_for_element
    driver.wait_for_element_visible = DM.wait_for_element_visible
    driver.wait_for_element_present = DM.wait_for_element_present
    driver.wait_for_selector = DM.wait_for_selector
    driver.wait_for_text = DM.wait_for_text
    driver.wait_for_exact_text = DM.wait_for_exact_text
    driver.wait_for_non_empty_text = DM.wait_for_non_empty_text
    driver.wait_for_text_not_visible = DM.wait_for_text_not_visible
    driver.wait_for_and_accept_alert = DM.wait_for_and_accept_alert
    driver.wait_for_and_dismiss_alert = DM.wait_for_and_dismiss_alert
    driver.is_element_present = DM.is_element_present
    driver.is_element_visible = DM.is_element_visible
    driver.is_text_visible = DM.is_text_visible
    driver.is_exact_text_visible = DM.is_exact_text_visible
    driver.is_attribute_present = DM.is_attribute_present
    driver.is_non_empty_text_visible = DM.is_non_empty_text_visible
    driver.is_valid_url = DM.is_valid_url
    driver.is_alert_present = DM.is_alert_present
    driver.is_online = DM.is_online
    driver.js_click = DM.js_click
    driver.get_text = DM.get_text
    driver.get_active_element_css = DM.get_active_element_css
    driver.get_locale_code = DM.get_locale_code
    driver.get_origin = DM.get_origin
    driver.get_user_agent = DM.get_user_agent
    driver.highlight = DM.highlight
    driver.highlight_click = DM.highlight_click
    driver.highlight_if_visible = DM.highlight_if_visible
    driver.sleep = time.sleep
    driver.get_attribute = DM.get_attribute
    driver.get_page_source = DM.get_page_source
    driver.get_title = DM.get_title
    driver.switch_to_default_window = DM.switch_to_default_window
    driver.switch_to_newest_window = DM.switch_to_newest_window
    driver.open_new_window = DM.open_new_window
    driver.open_new_tab = DM.open_new_tab
    driver.switch_to_window = DM.switch_to_window
    driver.switch_to_tab = DM.switch_to_tab
    driver.switch_to_frame = DM.switch_to_frame
    if hasattr(driver, "proxy"):
        driver.set_wire_proxy = DM.set_wire_proxy
    return driver


@decorators.rate_limited(4)
def requests_get(url, proxy_string=None):
    import requests

    protocol = "http"
    proxies = None
    if proxy_string:
        if proxy_string.endswith(":443"):
            protocol = "https"
        elif "socks4" in proxy_string:
            protocol = "socks4"
        elif "socks5" in proxy_string:
            protocol = "socks5"
        proxies = {protocol: proxy_string}
    response = None
    try:
        response = requests.get(url, proxies=proxies, timeout=1.25)
    except Exception:
        # Prevent SSLCertVerificationError / CERTIFICATE_VERIFY_FAILED
        url = url.replace("https://", "http://")
        time.sleep(0.04)
        response = requests.get(url, proxies=proxies, timeout=2.75)
    return response


def get_latest_chromedriver_version():
    from seleniumbase.console_scripts import sb_install
    return sb_install.get_latest_stable_chromedriver_version()


def chromedriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if (
            not IS_WINDOWS
            and os.path.exists(os.path.join(path, "chromedriver"))
        ):
            return os.path.join(path, "chromedriver")
        elif (
            IS_WINDOWS
            and os.path.exists(os.path.join(path, "chromedriver.exe"))
        ):
            return os.path.join(path, "chromedriver.exe")
    return None


def get_uc_driver_version(full=False):
    uc_driver_version = None
    if os.path.exists(LOCAL_UC_DRIVER):
        with suppress(Exception):
            output = subprocess.check_output(
                '"%s" --version' % LOCAL_UC_DRIVER, shell=True
            )
            if IS_WINDOWS:
                output = output.decode("latin1")
            else:
                output = output.decode("utf-8")
            full_version = output.split(" ")[1]
            output = output.split(" ")[1].split(".")[0]
            if int(output) >= 72:
                if full:
                    uc_driver_version = full_version
                else:
                    uc_driver_version = output
    return uc_driver_version


def find_chromedriver_version_to_use(use_version, driver_version):
    # Note: https://chromedriver.chromium.org/downloads stops at 114.
    # Future drivers are part of the Chrome-for-Testing collection.
    if (
        driver_version
        and str(driver_version).split(".")[0].isdigit()
        and int(str(driver_version).split(".")[0]) >= 72
    ):
        use_version = str(driver_version)
    elif driver_version and not str(driver_version).split(".")[0].isdigit():
        from seleniumbase.console_scripts import sb_install
        driver_version = driver_version.lower()
        if driver_version == "stable" or driver_version == "latest":
            use_version = sb_install.get_latest_stable_chromedriver_version()
        elif driver_version == "beta":
            use_version = sb_install.get_latest_beta_chromedriver_version()
        elif driver_version == "dev":
            use_version = sb_install.get_latest_dev_chromedriver_version()
        elif driver_version == "canary":
            use_version = sb_install.get_latest_canary_chromedriver_version()
        elif driver_version == "previous" or driver_version == "latest-1":
            use_version = sb_install.get_latest_stable_chromedriver_version()
            use_version = str(int(use_version.split(".")[0]) - 1)
        elif driver_version == "mlatest":
            if use_version.split(".")[0].isdigit():
                major = use_version.split(".")[0]
                if int(major) >= 115:
                    use_version = (
                        sb_install.get_cft_latest_version_from_milestone(major)
                    )
    return use_version


def find_edgedriver_version_to_use(use_version, driver_version):
    if (
        driver_version
        and str(driver_version).split(".")[0].isdigit()
        and int(str(driver_version).split(".")[0]) >= 80
    ):
        use_version = str(driver_version)
    return use_version


def has_captcha(text):
    if (
        "<title>403 Forbidden</title>" in text
        or "Permission Denied</title>" in text
        or 'id="challenge-error-text"' in text
        or "<title>Just a moment..." in text
        or 'action="/?__cf_chl_f_tk' in text
        or 'id="challenge-widget-' in text
        or 'src="chromedriver.js"' in text
        or 'class="g-recaptcha"' in text
        or 'content="Pixelscan"' in text
        or 'id="challenge-form"' in text
        or "/challenge-platform" in text
        or "window._cf_chl_opt" in text
        or "/recaptcha/api.js" in text
        or "/turnstile/" in text
    ):
        return True
    return False


def uc_special_open_if_cf(
    driver,
    url,
    proxy_string=None,
    mobile_emulator=None,
    device_width=None,
    device_height=None,
    device_pixel_ratio=None,
):
    if url.startswith("http:") or url.startswith("https:"):
        special = False
        with suppress(Exception):
            req_get = requests_get(url, proxy_string)
            status_str = str(req_get.status_code)
            if (
                status_str.startswith("3")
                or status_str.startswith("4")
                or status_str.startswith("5")
                or has_captcha(req_get.text)
            ):
                special = True
                if status_str == "403" or status_str == "429":
                    time.sleep(0.06)  # Forbidden / Blocked! (Wait first!)
        if special:
            time.sleep(0.05)
            with driver:
                driver.execute_script('window.open("%s","_blank");' % url)
                driver.close()
                if mobile_emulator:
                    page_actions.switch_to_window(
                        driver, driver.window_handles[-1], 2
                    )
                    uc_metrics = {}
                    if (
                        isinstance(device_width, int)
                        and isinstance(device_height, int)
                        and isinstance(device_pixel_ratio, (int, float))
                    ):
                        uc_metrics["width"] = device_width
                        uc_metrics["height"] = device_height
                        uc_metrics["pixelRatio"] = device_pixel_ratio
                    else:
                        uc_metrics["width"] = constants.Mobile.WIDTH
                        uc_metrics["height"] = constants.Mobile.HEIGHT
                        uc_metrics["pixelRatio"] = constants.Mobile.RATIO
                    set_device_metrics_override = dict(
                        {
                            "width": uc_metrics["width"],
                            "height": uc_metrics["height"],
                            "deviceScaleFactor": uc_metrics["pixelRatio"],
                            "mobile": True
                        }
                    )
                    with suppress(Exception):
                        driver.execute_cdp_cmd(
                            'Emulation.setDeviceMetricsOverride',
                            set_device_metrics_override
                        )
            if not mobile_emulator:
                page_actions.switch_to_window(
                    driver, driver.window_handles[-1], 2
                )
        else:
            driver.default_get(url)  # The original one
    else:
        driver.default_get(url)  # The original one
    return None


def uc_open(driver, url):
    if url.startswith("//"):
        url = "https:" + url
    elif ":" not in url:
        url = "https://" + url
    if (url.startswith("http:") or url.startswith("https:")):
        with driver:
            script = 'window.location.href = "%s";' % url
            js_utils.call_me_later(driver, script, 5)
    else:
        driver.default_get(url)  # The original one
    return None


def uc_open_with_tab(driver, url):
    if url.startswith("//"):
        url = "https:" + url
    elif ":" not in url:
        url = "https://" + url
    if (url.startswith("http:") or url.startswith("https:")):
        with driver:
            driver.execute_script('window.open("%s","_blank");' % url)
            driver.close()
        page_actions.switch_to_window(driver, driver.window_handles[-1], 2)
    else:
        driver.default_get(url)  # The original one
    return None


def uc_open_with_reconnect(driver, url, reconnect_time=None):
    """Open a url, disconnect chromedriver, wait, and reconnect."""
    if not reconnect_time:
        reconnect_time = constants.UC.RECONNECT_TIME
    if url.startswith("//"):
        url = "https:" + url
    elif ":" not in url:
        url = "https://" + url
    if (url.startswith("http:") or url.startswith("https:")):
        script = 'window.open("%s","_blank");' % url
        driver.execute_script(script)
        time.sleep(0.05)
        driver.close()
        if reconnect_time == "disconnect":
            driver.disconnect()
            time.sleep(0.008)
        else:
            driver.reconnect(reconnect_time)
            time.sleep(0.004)
            try:
                page_actions.switch_to_window(
                    driver, driver.window_handles[-1], 2
                )
            except InvalidSessionIdException:
                time.sleep(0.05)
                page_actions.switch_to_window(
                    driver, driver.window_handles[-1], 2
                )
    else:
        driver.default_get(url)  # The original one
    return None


def uc_open_with_disconnect(driver, url, timeout=None):
    """Open a url and disconnect chromedriver.
    Then waits for the duration of the timeout.
    Note: You can't perform Selenium actions again
    until after you've called driver.connect()."""
    if url.startswith("//"):
        url = "https:" + url
    elif ":" not in url:
        url = "https://" + url
    if (url.startswith("http:") or url.startswith("https:")):
        script = 'window.open("%s","_blank");' % url
        driver.execute_script(script)
        time.sleep(0.05)
        driver.close()
        driver.disconnect()
        min_timeout = 0.008
        if timeout and not str(timeout).replace(".", "", 1).isdigit():
            timeout = min_timeout
        if not timeout or timeout < min_timeout:
            timeout = min_timeout
        time.sleep(timeout)
    else:
        driver.default_get(url)  # The original one
    return None


def uc_click(
    driver,
    selector,
    by="css selector",
    timeout=settings.SMALL_TIMEOUT,
    reconnect_time=None,
):
    with suppress(Exception):
        rct = float(by)  # Add shortcut: driver.uc_click(selector, RCT)
        if not reconnect_time:
            reconnect_time = rct
        by = "css selector"
    element = driver.wait_for_selector(selector, by=by, timeout=timeout)
    tag_name = element.tag_name
    if not tag_name == "span" and not tag_name == "input":  # Must be "visible"
        element = driver.wait_for_element(selector, by=by, timeout=timeout)
    try:
        element.uc_click(
            driver,
            selector,
            by=by,
            reconnect_time=reconnect_time,
            tag_name=tag_name,
        )
    except ElementClickInterceptedException:
        time.sleep(0.16)
        driver.js_click(selector, by=by, timeout=timeout)
        if not reconnect_time:
            driver.reconnect(0.1)
        else:
            driver.reconnect(reconnect_time)


def verify_pyautogui_has_a_headed_browser(driver):
    """PyAutoGUI requires a headed browser so that it can
    focus on the correct element when performing actions."""
    if hasattr(driver, "_is_hidden") and driver._is_hidden:
        raise Exception(
            "PyAutoGUI can't be used in headless mode!"
        )


def install_pyautogui_if_missing(driver):
    verify_pyautogui_has_a_headed_browser(driver)
    pip_find_lock = fasteners.InterProcessLock(
        constants.PipInstall.FINDLOCK
    )
    with pip_find_lock:  # Prevent issues with multiple processes
        try:
            import pyautogui
            with suppress(Exception):
                use_pyautogui_ver = constants.PyAutoGUI.VER
                if pyautogui.__version__ != use_pyautogui_ver:
                    del pyautogui
                    shared_utils.pip_install(
                        "pyautogui", version=use_pyautogui_ver
                    )
                    import pyautogui
        except Exception:
            print("\nPyAutoGUI required! Installing now...")
            shared_utils.pip_install(
                "pyautogui", version=constants.PyAutoGUI.VER
            )
            try:
                import pyautogui
            except Exception:
                if (
                    IS_LINUX
                    and hasattr(sb_config, "xvfb")
                    and hasattr(sb_config, "headed")
                    and hasattr(sb_config, "headless")
                    and hasattr(sb_config, "headless2")
                    and (not sb_config.headed or sb_config.xvfb)
                    and not (sb_config.headless or sb_config.headless2)
                ):
                    from sbvirtualdisplay import Display
                    xvfb_width = 1366
                    xvfb_height = 768
                    if (
                        hasattr(sb_config, "_xvfb_width")
                        and sb_config._xvfb_width
                        and isinstance(sb_config._xvfb_width, int)
                        and hasattr(sb_config, "_xvfb_height")
                        and sb_config._xvfb_height
                        and isinstance(sb_config._xvfb_height, int)
                    ):
                        xvfb_width = sb_config._xvfb_width
                        xvfb_height = sb_config._xvfb_height
                        if xvfb_width < 1024:
                            xvfb_width = 1024
                        sb_config._xvfb_width = xvfb_width
                        if xvfb_height < 768:
                            xvfb_height = 768
                        sb_config._xvfb_height = xvfb_height
                    with suppress(Exception):
                        xvfb_display = Display(
                            visible=True,
                            size=(xvfb_width, xvfb_height),
                            backend="xvfb",
                            use_xauth=True,
                        )
                        xvfb_display.start()


def get_configured_pyautogui(pyautogui_copy):
    if (
        IS_LINUX
        and hasattr(pyautogui_copy, "_pyautogui_x11")
        and "DISPLAY" in os.environ.keys()
    ):
        if (
            hasattr(sb_config, "_pyautogui_x11_display")
            and sb_config._pyautogui_x11_display
            and hasattr(pyautogui_copy._pyautogui_x11, "_display")
            and (
                sb_config._pyautogui_x11_display
                == pyautogui_copy._pyautogui_x11._display
            )
        ):
            pass
        else:
            import Xlib.display
            pyautogui_copy._pyautogui_x11._display = (
                Xlib.display.Display(os.environ['DISPLAY'])
            )
            sb_config._pyautogui_x11_display = (
                pyautogui_copy._pyautogui_x11._display
            )
    return pyautogui_copy


def uc_gui_press_key(driver, key):
    install_pyautogui_if_missing(driver)
    import pyautogui
    pyautogui = get_configured_pyautogui(pyautogui)
    gui_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.PYAUTOGUILOCK
    )
    with gui_lock:
        pyautogui.press(key)


def uc_gui_press_keys(driver, keys):
    install_pyautogui_if_missing(driver)
    import pyautogui
    pyautogui = get_configured_pyautogui(pyautogui)
    gui_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.PYAUTOGUILOCK
    )
    with gui_lock:
        for key in keys:
            pyautogui.press(key)


def uc_gui_write(driver, text):
    install_pyautogui_if_missing(driver)
    import pyautogui
    pyautogui = get_configured_pyautogui(pyautogui)
    gui_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.PYAUTOGUILOCK
    )
    with gui_lock:
        pyautogui.write(text)


def get_gui_element_position(driver, selector):
    element = driver.wait_for_element_present(selector, timeout=3)
    element_rect = element.rect
    window_rect = driver.get_window_rect()
    window_bottom_y = window_rect["y"] + window_rect["height"]
    viewport_height = driver.execute_script("return window.innerHeight;")
    viewport_x = window_rect["x"] + element_rect["x"]
    viewport_y = window_bottom_y - viewport_height + element_rect["y"]
    y_scroll_offset = driver.execute_script("return window.pageYOffset;")
    viewport_y = viewport_y - y_scroll_offset
    return (viewport_x, viewport_y)


def _uc_gui_click_x_y(driver, x, y, timeframe=0.25, uc_lock=False):
    install_pyautogui_if_missing(driver)
    import pyautogui
    pyautogui = get_configured_pyautogui(pyautogui)
    screen_width, screen_height = pyautogui.size()
    if x < 0 or y < 0 or x > screen_width or y > screen_height:
        raise Exception(
            "PyAutoGUI cannot click on point (%s, %s)"
            " outside screen. (Width: %s, Height: %s)"
            % (x, y, screen_width, screen_height)
        )
    if uc_lock:
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:  # Prevent issues with multiple processes
            pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
            if timeframe >= 0.25:
                time.sleep(0.056)  # Wait if moving at human-speed
            if "--debug" in sys.argv:
                print(" <DEBUG> pyautogui.click(%s, %s)" % (x, y))
            pyautogui.click(x=x, y=y)
    else:
        # Called from a method where the gui_lock is already active
        pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
        if timeframe >= 0.25:
            time.sleep(0.056)  # Wait if moving at human-speed
        if "--debug" in sys.argv:
            print(" <DEBUG> pyautogui.click(%s, %s)" % (x, y))
        pyautogui.click(x=x, y=y)


def uc_gui_click_x_y(driver, x, y, timeframe=0.25):
    gui_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.PYAUTOGUILOCK
    )
    with gui_lock:  # Prevent issues with multiple processes
        install_pyautogui_if_missing(driver)
        import pyautogui
        pyautogui = get_configured_pyautogui(pyautogui)
        connected = True
        width_ratio = 1.0
        if IS_WINDOWS:
            try:
                driver.window_handles
            except Exception:
                connected = False
            if (
                not connected
                and (
                    not hasattr(sb_config, "_saved_width_ratio")
                    or not sb_config._saved_width_ratio
                )
            ):
                driver.reconnect(0.1)
                connected = True
        if IS_WINDOWS and connected:
            window_rect = driver.get_window_rect()
            width = window_rect["width"]
            height = window_rect["height"]
            win_x = window_rect["x"]
            win_y = window_rect["y"]
            if (
                hasattr(sb_config, "_saved_width_ratio")
                and sb_config._saved_width_ratio
            ):
                width_ratio = sb_config._saved_width_ratio
            else:
                scr_width = pyautogui.size().width
                driver.maximize_window()
                win_width = driver.get_window_size()["width"]
                width_ratio = round(float(scr_width) / float(win_width), 2)
                width_ratio += 0.01
                if width_ratio < 0.45 or width_ratio > 2.55:
                    width_ratio = 1.01
                sb_config._saved_width_ratio = width_ratio
            driver.minimize_window()
            driver.set_window_rect(win_x, win_y, width, height)
        elif (
            IS_WINDOWS
            and not connected
            and hasattr(sb_config, "_saved_width_ratio")
            and sb_config._saved_width_ratio
        ):
            width_ratio = sb_config._saved_width_ratio
        if IS_WINDOWS:
            x = x * width_ratio
            y = y * width_ratio
            _uc_gui_click_x_y(driver, x, y, timeframe=timeframe, uc_lock=False)
            return
        with suppress(Exception):
            page_actions.switch_to_window(
                driver, driver.current_window_handle, 2, uc_lock=False
            )
        _uc_gui_click_x_y(driver, x, y, timeframe=timeframe, uc_lock=False)


def _on_a_cf_turnstile_page(driver):
    source = driver.get_page_source()
    if (
        'data-callback="onCaptchaSuccess"' in source
        or "/challenge-platform/scripts/" in source
        or 'id="challenge-widget-' in source
        or "cf-turnstile-" in source
    ):
        return True
    return False


def _on_a_g_recaptcha_page(driver):
    source = driver.get_page_source()
    if (
        'id="recaptcha-token"' in source
        or 'title="reCAPTCHA"' in source
    ):
        return True
    return False


def _uc_gui_click_captcha(
    driver,
    frame="iframe",
    retry=False,
    blind=False,
    ctype=None,
):
    _on_a_captcha_page = None
    if ctype == "cf_t":
        if not _on_a_cf_turnstile_page(driver):
            return
        else:
            _on_a_captcha_page = _on_a_cf_turnstile_page
    elif ctype == "g_rc":
        if not _on_a_g_recaptcha_page(driver):
            return
        else:
            _on_a_captcha_page = _on_a_g_recaptcha_page
    else:
        if _on_a_g_recaptcha_page(driver):
            ctype = "g_rc"
            _on_a_captcha_page = _on_a_g_recaptcha_page
        elif _on_a_cf_turnstile_page(driver):
            ctype = "cf_t"
            _on_a_captcha_page = _on_a_cf_turnstile_page
        else:
            return
    install_pyautogui_if_missing(driver)
    import pyautogui
    pyautogui = get_configured_pyautogui(pyautogui)
    i_x = None
    i_y = None
    x = None
    y = None
    visible_iframe = True
    gui_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.PYAUTOGUILOCK
    )
    with gui_lock:  # Prevent issues with multiple processes
        needs_switch = False
        width_ratio = 1.0
        is_in_frame = js_utils.is_in_frame(driver)
        if is_in_frame and driver.is_element_present("#challenge-stage"):
            driver.switch_to.parent_frame()
            needs_switch = True
            is_in_frame = js_utils.is_in_frame(driver)
        if not is_in_frame:
            # Make sure the window is on top
            page_actions.switch_to_window(
                driver, driver.current_window_handle, 2, uc_lock=False
            )
        if IS_WINDOWS:
            window_rect = driver.get_window_rect()
            width = window_rect["width"]
            height = window_rect["height"]
            win_x = window_rect["x"]
            win_y = window_rect["y"]
            scr_width = pyautogui.size().width
            driver.maximize_window()
            win_width = driver.get_window_size()["width"]
            width_ratio = round(float(scr_width) / float(win_width), 2) + 0.01
            if width_ratio < 0.45 or width_ratio > 2.55:
                width_ratio = 1.01
            sb_config._saved_width_ratio = width_ratio
            driver.minimize_window()
            driver.set_window_rect(win_x, win_y, width, height)
        if ctype == "cf_t":
            if (
                driver.is_element_present(".cf-turnstile-wrapper iframe")
                or driver.is_element_present(
                    '[data-callback="onCaptchaSuccess"] iframe'
                )
            ):
                pass
            else:
                visible_iframe = False
                if (
                    frame != "iframe"
                    and driver.is_element_present(
                        "%s .cf-turnstile-wrapper" % frame
                    )
                ):
                    frame = "%s .cf-turnstile-wrapper" % frame
                elif (
                    frame != "iframe"
                    and driver.is_element_present(
                        '%s [name*="cf-turnstile"]' % frame
                    )
                    and driver.is_element_present("%s div" % frame)
                ):
                    frame = "%s div" % frame
                elif (
                    driver.is_element_present('[name*="cf-turnstile-"]')
                    and driver.is_element_present('[class*=spacer] + div div')
                ):
                    frame = '[class*=spacer] + div div'
                elif (
                    driver.is_element_present('[name*="cf-turnstile-"]')
                    and driver.is_element_present("div.spacer div")
                ):
                    frame = "div.spacer div"
                elif (
                    driver.is_element_present('script[src*="challenges.c"]')
                    and driver.is_element_present(
                        '[data-testid*="challenge-"] div'
                    )
                ):
                    frame = '[data-testid*="challenge-"] div'
                elif driver.is_element_present(
                    'form div:not([class]):has(input[name*="cf-turn"])'
                ):
                    frame = 'form div:not([class]):has(input[name*="cf-turn"])'
                elif (
                    driver.is_element_present('[src*="/turnstile/"]')
                    and driver.is_element_present("form div:not(:has(*))")
                ):
                    frame = "form div:not(:has(*))"
                elif driver.is_element_present(".cf-turnstile-wrapper"):
                    frame = ".cf-turnstile-wrapper"
                elif driver.is_element_present(
                    '[data-callback="onCaptchaSuccess"]'
                ):
                    frame = '[data-callback="onCaptchaSuccess"]'
                else:
                    return
            if driver.is_element_present('form[class*=center]'):
                script = (
                    """var $elements = document.querySelectorAll('form');
                    var index = 0, length = $elements.length;
                    for(; index < length; index++){
                    the_class = $elements[index].getAttribute('class');
                    new_class = the_class.replaceAll('center', 'left');
                    $elements[index].setAttribute('class', new_class);}"""
                )
                driver.execute_script(script)
        if not is_in_frame or needs_switch:
            # Currently not in frame (or nested frame outside CF one)
            try:
                i_x, i_y = get_gui_element_position(driver, frame)
                if visible_iframe:
                    driver.switch_to_frame(frame)
            except Exception:
                if visible_iframe:
                    if driver.is_element_present("iframe"):
                        i_x, i_y = get_gui_element_position(driver, "iframe")
                        driver.switch_to_frame("iframe")
                    else:
                        return
            if not i_x or not i_y:
                return
        try:
            if visible_iframe:
                selector = "span"
                if ctype == "g_rc":
                    selector = "span.recaptcha-checkbox"
                element = driver.wait_for_element_present(
                    selector, timeout=2.5
                )
                x = i_x + element.rect["x"] + int(element.rect["width"] / 2)
                x += 1
                y = i_y + element.rect["y"] + int(element.rect["height"] / 2)
                y += 1
            else:
                x = (i_x + 34) * width_ratio
                y = (i_y + 34) * width_ratio
            driver.switch_to.default_content()
        except Exception:
            try:
                driver.switch_to.default_content()
            except Exception:
                return
        if x and y:
            sb_config._saved_cf_x_y = (x, y)
            if driver.is_element_present(".footer .clearfix .ray-id"):
                driver.uc_open_with_disconnect(driver.current_url, 3.8)
            else:
                driver.disconnect()
            with suppress(Exception):
                _uc_gui_click_x_y(driver, x, y, timeframe=0.32)
    reconnect_time = (float(constants.UC.RECONNECT_TIME) / 2.0) + 0.6
    if IS_LINUX:
        reconnect_time = constants.UC.RECONNECT_TIME + 0.2
    if not x or not y:
        reconnect_time = 1  # Make it quick (it already failed)
    driver.reconnect(reconnect_time)
    caught = False
    if (
        driver.is_element_present(".footer .clearfix .ray-id")
        and not driver.is_element_visible("#challenge-success-text")
    ):
        blind = True
        caught = True
    if blind:
        retry = True
    if retry and x and y and (caught or _on_a_captcha_page(driver)):
        with gui_lock:  # Prevent issues with multiple processes
            # Make sure the window is on top
            page_actions.switch_to_window(
                driver, driver.current_window_handle, 2, uc_lock=False
            )
            if driver.is_element_present("iframe"):
                try:
                    driver.switch_to_frame(frame)
                except Exception:
                    try:
                        driver.switch_to_frame("iframe")
                    except Exception:
                        return
                checkbox_success = None
                if ctype == "cf_t":
                    checkbox_success = "#success-icon"
                elif ctype == "g_rc":
                    checkbox_success = "span.recaptcha-checkbox-checked"
                else:
                    return  # If this line is reached, ctype wasn't set
                if driver.is_element_visible("#success-icon"):
                    driver.switch_to.parent_frame(checkbox_success)
                    return
            if blind:
                driver.uc_open_with_disconnect(driver.current_url, 3.8)
                _uc_gui_click_x_y(driver, x, y, timeframe=0.32)
            else:
                driver.uc_open_with_reconnect(driver.current_url, 3.8)
                if _on_a_captcha_page(driver):
                    driver.disconnect()
                    _uc_gui_click_x_y(driver, x, y, timeframe=0.32)
        driver.reconnect(reconnect_time)


def uc_gui_click_captcha(driver, frame="iframe", retry=False, blind=False):
    _uc_gui_click_captcha(
        driver,
        frame=frame,
        retry=retry,
        blind=blind,
        ctype=None,
    )


def uc_gui_click_rc(driver, frame="iframe", retry=False, blind=False):
    _uc_gui_click_captcha(
        driver,
        frame=frame,
        retry=retry,
        blind=blind,
        ctype="g_rc",
    )


def uc_gui_click_cf(driver, frame="iframe", retry=False, blind=False):
    _uc_gui_click_captcha(
        driver,
        frame=frame,
        retry=retry,
        blind=blind,
        ctype="cf_t",
    )


def _uc_gui_handle_captcha_(driver, frame="iframe", ctype=None):
    if ctype == "cf_t":
        if not _on_a_cf_turnstile_page(driver):
            return
    elif ctype == "g_rc":
        if not _on_a_g_recaptcha_page(driver):
            return
    else:
        if _on_a_g_recaptcha_page(driver):
            ctype = "g_rc"
        elif _on_a_cf_turnstile_page(driver):
            ctype = "cf_t"
        else:
            return
    install_pyautogui_if_missing(driver)
    import pyautogui
    pyautogui = get_configured_pyautogui(pyautogui)
    visible_iframe = True
    gui_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.PYAUTOGUILOCK
    )
    with gui_lock:  # Prevent issues with multiple processes
        needs_switch = False
        is_in_frame = js_utils.is_in_frame(driver)
        selector = "#challenge-stage"
        if ctype == "g_rc":
            selector = "#recaptcha-token"
        if is_in_frame and driver.is_element_present(selector):
            driver.switch_to.parent_frame()
            needs_switch = True
            is_in_frame = js_utils.is_in_frame(driver)
        if not is_in_frame:
            # Make sure the window is on top
            page_actions.switch_to_window(
                driver, driver.current_window_handle, 2, uc_lock=False
            )
        if IS_WINDOWS and hasattr(pyautogui, "getActiveWindowTitle"):
            py_a_g_title = pyautogui.getActiveWindowTitle()
            window_title = driver.title
            if not py_a_g_title.startswith(window_title):
                window_rect = driver.get_window_rect()
                width = window_rect["width"]
                height = window_rect["height"]
                win_x = window_rect["x"]
                win_y = window_rect["y"]
                driver.minimize_window()
                driver.set_window_rect(win_x, win_y, width, height)
                time.sleep(0.33)
        tab_up_first = False
        special_form = False
        if ctype == "cf_t":
            if (
                driver.is_element_present(".cf-turnstile-wrapper iframe")
                or driver.is_element_present(
                    '[data-callback="onCaptchaSuccess"] iframe'
                )
            ):
                pass
            else:
                visible_iframe = False
                if driver.is_element_present(".cf-turnstile-wrapper"):
                    frame = ".cf-turnstile-wrapper"
                elif driver.is_element_present(
                    '[data-callback="onCaptchaSuccess"]'
                ):
                    frame = '[data-callback="onCaptchaSuccess"]'
                elif (
                    driver.is_element_present('[name*="cf-turnstile-"]')
                    and driver.is_element_present("div.spacer div")
                ):
                    frame = "div.spacer div"
                elif (
                    driver.is_element_present('script[src*="challenges.c"]')
                    and driver.is_element_present(
                        '[data-testid*="challenge-"] div'
                    )
                ):
                    frame = '[data-testid*="challenge-"] div'
                elif driver.is_element_present(
                    'form div:not([class]):has(input[name*="cf-turn"])'
                ):
                    frame = 'form div:not([class]):has(input[name*="cf-turn"])'
                    tab_up_first = True
                    special_form = True
                elif (
                    driver.is_element_present('[src*="/turnstile/"]')
                    and driver.is_element_present("form div:not(:has(*))")
                ):
                    frame = "form div:not(:has(*))"
                    tab_up_first = True
                else:
                    return
        else:
            if (
                driver.is_element_present('iframe[title="reCAPTCHA"]')
                and frame == "iframe"
            ):
                frame = 'iframe[title="reCAPTCHA"]'
        if not is_in_frame or needs_switch:
            # Currently not in frame (or nested frame outside CF one)
            try:
                if visible_iframe or ctype == "g_rc":
                    driver.switch_to_frame(frame)
            except Exception:
                if visible_iframe or ctype == "g_rc":
                    if driver.is_element_present("iframe"):
                        driver.switch_to_frame("iframe")
                    else:
                        return
        try:
            selector = "div.cf-turnstile"
            if ctype == "g_rc":
                selector = "span#recaptcha-anchor"
            found_checkbox = False
            if tab_up_first:
                for i in range(10):
                    pyautogui.hotkey("shift", "tab")
                    time.sleep(0.027)
            tab_count = 0
            for i in range(34):
                pyautogui.press("\t")
                tab_count += 1
                time.sleep(0.027)
                active_element_css = js_utils.get_active_element_css(driver)
                if (
                    active_element_css.startswith(selector)
                    or active_element_css.endswith(" > div" * 2)
                    or (special_form and active_element_css.endswith(" div"))
                ):
                    found_checkbox = True
                    sb_config._saved_cf_tab_count = tab_count
                    break
                time.sleep(0.02)
            if not found_checkbox:
                return
        except Exception:
            try:
                driver.switch_to.default_content()
            except Exception:
                return
        if (
            driver.is_element_present(".footer .clearfix .ray-id")
            and hasattr(sb_config, "_saved_cf_tab_count")
            and sb_config._saved_cf_tab_count
        ):
            driver.uc_open_with_disconnect(driver.current_url, 3.8)
            with suppress(Exception):
                for i in range(sb_config._saved_cf_tab_count):
                    pyautogui.press("\t")
                    time.sleep(0.027)
                pyautogui.press(" ")
        else:
            driver.disconnect()
            pyautogui.press(" ")
    reconnect_time = (float(constants.UC.RECONNECT_TIME) / 2.0) + 0.6
    if IS_LINUX:
        reconnect_time = constants.UC.RECONNECT_TIME + 0.2
    driver.reconnect(reconnect_time)


def _uc_gui_handle_captcha(driver, frame="iframe", ctype=None):
    _uc_gui_handle_captcha_(driver, frame=frame, ctype=ctype)
    if (
        driver.is_element_present(".footer .clearfix .ray-id")
        and not driver.is_element_visible("#challenge-success-text")
    ):
        driver.uc_open_with_reconnect(driver.current_url, 3.8)
        _uc_gui_handle_captcha_(driver, frame=frame, ctype=ctype)


def uc_gui_handle_captcha(driver, frame="iframe"):
    _uc_gui_handle_captcha(driver, frame=frame, ctype=None)


def uc_gui_handle_cf(driver, frame="iframe"):
    _uc_gui_handle_captcha(driver, frame=frame, ctype="cf_t")


def uc_gui_handle_rc(driver, frame="iframe"):
    _uc_gui_handle_captcha(driver, frame=frame, ctype="g_rc")


def uc_switch_to_frame(driver, frame="iframe", reconnect_time=None):
    from selenium.webdriver.remote.webelement import WebElement
    if isinstance(frame, WebElement):
        if not reconnect_time:
            driver.reconnect(0.1)
        else:
            driver.reconnect(reconnect_time)
        driver.switch_to.frame(frame)
    else:
        iframe = driver.locator(frame)
        if not reconnect_time:
            driver.reconnect(0.1)
        else:
            driver.reconnect(reconnect_time)
        driver.switch_to.frame(iframe)


def edgedriver_on_path():
    return os.path.exists(LOCAL_EDGEDRIVER)


def geckodriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if (not IS_WINDOWS) and os.path.exists(path + "/geckodriver"):
            return True
        elif IS_WINDOWS and os.path.exists(path + "/geckodriver.exe"):
            return True
    return False


def iedriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if os.path.exists(path + "/IEDriverServer.exe"):
            return True
    return False


def headless_iedriver_on_path():
    return os.path.exists(LOCAL_HEADLESS_IEDRIVER)


def get_valid_binary_names_for_browser(browser):
    if browser == constants.Browser.GOOGLE_CHROME:
        if IS_LINUX:
            return constants.ValidBinaries.valid_chrome_binaries_on_linux
        elif IS_MAC:
            return constants.ValidBinaries.valid_chrome_binaries_on_macos
        elif IS_WINDOWS:
            return constants.ValidBinaries.valid_chrome_binaries_on_windows
        else:
            raise Exception("Could not determine OS, or unsupported!")
    elif browser == constants.Browser.EDGE:
        if IS_LINUX:
            return constants.ValidBinaries.valid_edge_binaries_on_linux
        elif IS_MAC:
            return constants.ValidBinaries.valid_edge_binaries_on_macos
        elif IS_WINDOWS:
            return constants.ValidBinaries.valid_edge_binaries_on_windows
        else:
            raise Exception("Could not determine OS, or unsupported!")
    else:
        raise Exception("Invalid combination for OS browser binaries!")


def _repair_chromedriver(chrome_options, headless_options, mcv=None):
    if mcv:
        subprocess.check_call(
            "sbase get chromedriver %s" % mcv, shell=True
        )
        return
    driver = None
    subprocess.check_call(
        "sbase get chromedriver 72.0.3626.69", shell=True
    )
    try:
        service = ChromeService(executable_path=LOCAL_CHROMEDRIVER)
        driver = webdriver.Chrome(
            service=service,
            options=headless_options,
        )
    except Exception:
        subprocess.check_call(
            "sbase get chromedriver latest-1", shell=True
        )
        return
    chrome_version = None
    if "version" in driver.capabilities:
        chrome_version = driver.capabilities["version"]
    else:
        chrome_version = driver.capabilities["browserVersion"]
    major_chrome_ver = chrome_version.split(".")[0]
    chrome_dict = driver.capabilities["chrome"]
    driver.quit()
    chromedriver_ver = chrome_dict["chromedriverVersion"]
    chromedriver_ver = chromedriver_ver.split(" ")[0]
    major_chromedriver_ver = chromedriver_ver.split(".")[0]
    if (
        major_chromedriver_ver != major_chrome_ver
        and int(major_chrome_ver) >= 73
    ):
        subprocess.check_call(
            "sbase get chromedriver %s" % major_chrome_ver, shell=True
        )
    return


def _repair_edgedriver(edge_version):
    log_d(
        "\nWarning: msedgedriver version doesn't match Edge version!"
        "\nAttempting to install a matching version of msedgedriver:"
    )
    subprocess.check_call(
        "sbase get edgedriver %s" % edge_version, shell=True
    )
    return


def _mark_driver_repaired():
    import codecs

    abs_path = os.path.abspath(".")
    driver_repaired_lock = constants.MultiBrowser.DRIVER_REPAIRED
    file_path = os.path.join(abs_path, driver_repaired_lock)
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)
    out_file = codecs.open(file_path, "w+", encoding="utf-8")
    out_file.writelines("")
    out_file.close()


def _was_driver_repaired():
    abs_path = os.path.abspath(".")
    driver_repaired_lock = constants.MultiBrowser.DRIVER_REPAIRED
    file_path = os.path.join(abs_path, driver_repaired_lock)
    return os.path.exists(file_path)


def _set_proxy_filenames():
    DOWNLOADS_DIR = constants.Files.DOWNLOADS_FOLDER
    for num in range(1000):
        PROXY_ZIP_PATH = os.path.join(DOWNLOADS_DIR, "proxy_%s.zip" % num)
        PROXY_DIR_PATH = os.path.join(DOWNLOADS_DIR, "proxy_ext_dir_%s" % num)
        if os.path.exists(PROXY_ZIP_PATH) or os.path.exists(PROXY_DIR_PATH):
            continue
        proxy_helper.PROXY_ZIP_PATH = PROXY_ZIP_PATH
        proxy_helper.PROXY_DIR_PATH = PROXY_DIR_PATH
        return
    # Exceeded upper bound. Use Defaults:
    PROXY_ZIP_PATH = os.path.join(DOWNLOADS_DIR, "proxy.zip")
    PROXY_DIR_PATH = os.path.join(DOWNLOADS_DIR, "proxy_ext_dir")
    proxy_helper.PROXY_ZIP_PATH = PROXY_ZIP_PATH
    proxy_helper.PROXY_DIR_PATH = PROXY_DIR_PATH


def _add_chrome_proxy_extension(
    chrome_options,
    proxy_string,
    proxy_user,
    proxy_pass,
    proxy_bypass_list=None,
    zip_it=True,
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
        if zip_it:
            proxy_helper.create_proxy_ext(
                proxy_string, proxy_user, proxy_pass, bypass_list
            )
            proxy_zip = proxy_helper.PROXY_ZIP_PATH
            chrome_options.add_extension(proxy_zip)
        else:
            proxy_helper.create_proxy_ext(
                proxy_string, proxy_user, proxy_pass, bypass_list, zip_it=False
            )
            proxy_dir_path = proxy_helper.PROXY_DIR_PATH
            chrome_options = add_chrome_ext_dir(chrome_options, proxy_dir_path)
    else:
        # Multi-threaded
        if zip_it:
            proxy_zip_lock = fasteners.InterProcessLock(PROXY_ZIP_LOCK)
            with proxy_zip_lock:
                if multi_proxy:
                    _set_proxy_filenames()
                if not os.path.exists(proxy_helper.PROXY_ZIP_PATH):
                    proxy_helper.create_proxy_ext(
                        proxy_string, proxy_user, proxy_pass, bypass_list
                    )
                proxy_zip = proxy_helper.PROXY_ZIP_PATH
                chrome_options.add_extension(proxy_zip)
        else:
            proxy_dir_lock = fasteners.InterProcessLock(PROXY_DIR_LOCK)
            with proxy_dir_lock:
                if multi_proxy:
                    _set_proxy_filenames()
                if not os.path.exists(proxy_helper.PROXY_DIR_PATH):
                    proxy_helper.create_proxy_ext(
                        proxy_string,
                        proxy_user,
                        proxy_pass,
                        bypass_list,
                        False,
                    )
                chrome_options = add_chrome_ext_dir(
                    chrome_options, proxy_helper.PROXY_DIR_PATH
                )
    return chrome_options


def is_using_uc(undetectable, browser_name):
    if undetectable and browser_name == constants.Browser.GOOGLE_CHROME:
        return True
    return False


def _unzip_to_new_folder(zip_file, folder):
    proxy_dir_lock = fasteners.InterProcessLock(PROXY_DIR_LOCK)
    with proxy_dir_lock:
        if not os.path.exists(folder):
            import zipfile
            zip_ref = zipfile.ZipFile(zip_file, "r")
            os.makedirs(folder)
            zip_ref.extractall(folder)
            zip_ref.close()


def add_chrome_ext_dir(chrome_options, dir_path):
    option_exists = False
    for arg in chrome_options.arguments:
        if arg.startswith("--load-extension="):
            option_exists = True
            chrome_options.arguments.remove(arg)
            chrome_options.add_argument(
                "%s,%s" % (arg, os.path.realpath(dir_path))
            )
    if not option_exists:
        chrome_options.add_argument(
            "--load-extension=%s" % os.path.realpath(dir_path)
        )
    return chrome_options


def _add_chrome_disable_csp_extension(chrome_options):
    """Disable Chrome's Content-Security-Policy with a browser extension.
    See https://github.com/PhilGrayson/chrome-csp-disable for details."""
    chrome_options.add_extension(DISABLE_CSP_ZIP_PATH)
    return chrome_options


def _add_chrome_ad_block_extension(chrome_options):
    """Block Ads on Chromium Browsers with a browser extension.
    See https://github.com/slingamn/simpleblock for details."""
    chrome_options.add_extension(AD_BLOCK_ZIP_PATH)
    return chrome_options


def _add_chrome_recorder_extension(chrome_options):
    """The SeleniumBase Recorder Chrome/Edge extension.
    https://seleniumbase.io/help_docs/recorder_mode/"""
    chrome_options.add_extension(RECORDER_ZIP_PATH)
    return chrome_options


def _set_chrome_options(
    browser_name,
    downloads_path,
    headless,
    locale_code,
    proxy_string,
    proxy_auth,
    proxy_user,
    proxy_pass,
    proxy_bypass_list,
    proxy_pac_url,
    multi_proxy,
    user_agent,
    recorder_ext,
    disable_cookies,
    disable_js,
    disable_csp,
    enable_ws,
    enable_sync,
    use_auto_ext,
    undetectable,
    uc_cdp_events,
    uc_subprocess,
    log_cdp_events,
    no_sandbox,
    disable_gpu,
    headless1,
    headless2,
    incognito,
    guest_mode,
    dark_mode,
    devtools,
    remote_debug,
    enable_3d_apis,
    swiftshader,
    ad_block_on,
    host_resolver_rules,
    block_images,
    do_not_track,
    chromium_arg,
    user_data_dir,
    extension_zip,
    extension_dir,
    disable_features,
    binary_location,
    driver_version,
    page_load_strategy,
    use_wire,
    external_pdf,
    servername,
    mobile_emulator,
    device_width,
    device_height,
    device_pixel_ratio,
):
    chrome_options = webdriver.ChromeOptions()
    if is_using_uc(undetectable, browser_name):
        from seleniumbase import undetected
        chrome_options = undetected.ChromeOptions()
    elif browser_name == constants.Browser.EDGE:
        chrome_options = webdriver.edge.options.Options()
    prefs = {}
    prefs["download.default_directory"] = downloads_path
    prefs["download.directory_upgrade"] = True
    prefs["download.prompt_for_download"] = False
    prefs["credentials_enable_service"] = False
    prefs["local_discovery.notifications_enabled"] = False
    prefs["safebrowsing.enabled"] = False  # Prevent PW "data breach" pop-ups
    prefs["safebrowsing.disable_download_protection"] = True
    prefs["omnibox-max-zero-suggest-matches"] = 0
    prefs["omnibox-use-existing-autocomplete-client"] = 0
    prefs["omnibox-trending-zero-prefix-suggestions-on-ntp"] = 0
    prefs["omnibox-local-history-zero-suggest-beyond-ntp"] = 0
    prefs["omnibox-on-focus-suggestions-contextual-web"] = 0
    prefs["omnibox-on-focus-suggestions-srp"] = 0
    prefs["omnibox-zero-suggest-prefetching"] = 0
    prefs["omnibox-zero-suggest-prefetching-on-srp"] = 0
    prefs["omnibox-zero-suggest-prefetching-on-web"] = 0
    prefs["omnibox-zero-suggest-in-memory-caching"] = 0
    prefs["content_settings.exceptions.automatic_downloads.*.setting"] = 1
    prefs["default_content_setting_values.notifications"] = 0
    prefs["default_content_settings.popups"] = 0
    prefs["managed_default_content_settings.popups"] = 0
    prefs["profile.password_manager_enabled"] = False
    prefs["profile.default_content_setting_values.notifications"] = 2
    prefs["profile.default_content_settings.popups"] = 0
    prefs["profile.managed_default_content_settings.popups"] = 0
    prefs["profile.default_content_setting_values.automatic_downloads"] = 1
    if locale_code:
        prefs["intl.accept_languages"] = locale_code
    if block_images:
        prefs["profile.managed_default_content_settings.images"] = 2
    if disable_cookies:
        prefs["profile.default_content_setting_values.cookies"] = 2
    if disable_js:
        prefs["profile.managed_default_content_settings.javascript"] = 2
    if do_not_track:
        prefs["enable_do_not_track"] = True
    if external_pdf:
        prefs["plugins.always_open_pdf_externally"] = True
    if proxy_string or proxy_pac_url:
        # Implementation of https://stackoverflow.com/q/65705775/7058266
        prefs["webrtc.ip_handling_policy"] = "disable_non_proxied_udp"
        prefs["webrtc.multiple_routes_enabled"] = False
        prefs["webrtc.nonproxied_udp_enabled"] = False
    chrome_options.add_experimental_option("prefs", prefs)
    if enable_sync:
        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation", "enable-logging", "disable-sync"],
        )
        chrome_options.add_argument("--enable-sync")
    else:
        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation", "enable-logging", "enable-blink-features"],
        )
    if log_cdp_events:
        chrome_options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
        )
    if host_resolver_rules:
        chrome_options.add_argument(
            "--host-resolver-rules=%s" % host_resolver_rules
        )
    if mobile_emulator and not is_using_uc(undetectable, browser_name):
        emulator_settings = {}
        device_metrics = {}
        if (
            isinstance(device_width, int)
            and isinstance(device_height, int)
            and isinstance(device_pixel_ratio, (int, float))
        ):
            device_metrics["width"] = device_width
            device_metrics["height"] = device_height
            device_metrics["pixelRatio"] = device_pixel_ratio
        else:
            device_metrics["width"] = constants.Mobile.WIDTH
            device_metrics["height"] = constants.Mobile.HEIGHT
            device_metrics["pixelRatio"] = constants.Mobile.RATIO
        emulator_settings["deviceMetrics"] = device_metrics
        if user_agent:
            emulator_settings["userAgent"] = user_agent
        chrome_options.add_experimental_option(
            "mobileEmulation", emulator_settings
        )
    # Handle Window Position
    if (headless or headless2) and IS_WINDOWS:
        # https://stackoverflow.com/a/78999088/7058266
        chrome_options.add_argument("--window-position=-2400,-2400")
    else:
        if (
            hasattr(settings, "WINDOW_START_X")
            and isinstance(settings.WINDOW_START_X, int)
            and hasattr(settings, "WINDOW_START_Y")
            and isinstance(settings.WINDOW_START_Y, int)
        ):
            chrome_options.add_argument(
                "--window-position=%s,%s" % (
                    settings.WINDOW_START_X, settings.WINDOW_START_Y
                )
            )
    # Handle Window Size
    if headless or headless2:
        if (
            hasattr(settings, "HEADLESS_START_WIDTH")
            and isinstance(settings.HEADLESS_START_WIDTH, int)
            and hasattr(settings, "HEADLESS_START_HEIGHT")
            and isinstance(settings.HEADLESS_START_HEIGHT, int)
        ):
            chrome_options.add_argument(
                "--window-size=%s,%s" % (
                    settings.HEADLESS_START_WIDTH,
                    settings.HEADLESS_START_HEIGHT,
                )
            )
    else:
        if (
            hasattr(settings, "CHROME_START_WIDTH")
            and isinstance(settings.CHROME_START_WIDTH, int)
            and hasattr(settings, "CHROME_START_HEIGHT")
            and isinstance(settings.CHROME_START_HEIGHT, int)
        ):
            chrome_options.add_argument(
                "--window-size=%s,%s" % (
                    settings.CHROME_START_WIDTH,
                    settings.CHROME_START_HEIGHT,
                )
            )
    if (
        not proxy_auth
        and not disable_csp
        and not ad_block_on
        and not recorder_ext
        and (not extension_zip and not extension_dir)
    ):
        if incognito:
            # Use Chrome's Incognito Mode
            # Incognito Mode prevents Chrome extensions from loading,
            # so if using extensions or a feature that uses extensions,
            # then Chrome's Incognito mode will be disabled instead.
            chrome_options.add_argument("--incognito")
        elif guest_mode:
            # Use Chrome's Guest Mode
            # Guest mode prevents Chrome extensions from loading,
            # so if using extensions or a feature that uses extensions,
            # then Chrome's Guest Mode will be disabled instead.
            chrome_options.add_argument("--guest")
        else:
            pass
    if dark_mode:
        chrome_options.add_argument("--enable-features=WebContentsForceDark")
    if user_data_dir and not is_using_uc(undetectable, browser_name):
        abs_path = os.path.abspath(user_data_dir)
        chrome_options.add_argument("--user-data-dir=%s" % abs_path)
    if extension_zip:
        # Can be a comma-separated list of .ZIP or .CRX files
        extension_zip_list = extension_zip.split(",")
        for extension_zip_item in extension_zip_list:
            abs_path = os.path.abspath(extension_zip_item)
            chrome_options.add_extension(abs_path)
    if extension_dir:
        # load-extension input can be a comma-separated list
        abs_path = os.path.abspath(extension_dir)
        chrome_options = add_chrome_ext_dir(chrome_options, abs_path)
    if (
        page_load_strategy
        and page_load_strategy.lower() in ["eager", "none"]
    ):
        # Only change it if not "normal", which is the default.
        chrome_options.page_load_strategy = page_load_strategy.lower()
    elif (
        not page_load_strategy
        and hasattr(settings, "PAGE_LOAD_STRATEGY")
        and settings.PAGE_LOAD_STRATEGY
        and settings.PAGE_LOAD_STRATEGY.lower() in ["eager", "none"]
    ):
        # Only change it if not "normal", which is the default.
        chrome_options.page_load_strategy = settings.PAGE_LOAD_STRATEGY.lower()
    if headless2:
        if servername and servername != "localhost":
            # The Grid Node will need Chrome 109 or newer
            chrome_options.add_argument("--headless=new")
        else:
            pass  # Processed After Version Check
    elif headless:
        if not undetectable:
            if headless1:
                chrome_options.add_argument("--headless=old")
            else:
                chrome_options.add_argument("--headless")
        if undetectable and servername and servername != "localhost":
            # The Grid Node will need Chrome 109 or newer
            chrome_options.add_argument("--headless=new")
        else:
            pass  # Processed After Version Check
    if (settings.DISABLE_CSP_ON_CHROME or disable_csp) and not headless:
        # Headless Chrome does not support extensions, which are required
        # for disabling the Content Security Policy on Chrome.
        if is_using_uc(undetectable, browser_name):
            disable_csp_zip = DISABLE_CSP_ZIP_PATH
            disable_csp_dir = os.path.join(DOWNLOADS_FOLDER, "disable_csp")
            _unzip_to_new_folder(disable_csp_zip, disable_csp_dir)
            chrome_options = add_chrome_ext_dir(
                chrome_options, disable_csp_dir
            )
        else:
            chrome_options = _add_chrome_disable_csp_extension(chrome_options)
    if ad_block_on and not headless:
        # Headless Chrome does not support extensions.
        if is_using_uc(undetectable, browser_name):
            ad_block_zip = AD_BLOCK_ZIP_PATH
            ad_block_dir = os.path.join(DOWNLOADS_FOLDER, "ad_block")
            _unzip_to_new_folder(ad_block_zip, ad_block_dir)
            chrome_options = add_chrome_ext_dir(chrome_options, ad_block_dir)
        else:
            chrome_options = _add_chrome_ad_block_extension(chrome_options)
    if recorder_ext and not headless:
        if is_using_uc(undetectable, browser_name):
            recorder_zip = RECORDER_ZIP_PATH
            recorder_dir = os.path.join(DOWNLOADS_FOLDER, "recorder")
            _unzip_to_new_folder(recorder_zip, recorder_dir)
            chrome_options = add_chrome_ext_dir(chrome_options, recorder_dir)
        else:
            chrome_options = _add_chrome_recorder_extension(chrome_options)
    if chromium_arg and "sbase" in chromium_arg:
        sbase_ext_zip = SBASE_EXT_ZIP_PATH
        sbase_ext_dir = os.path.join(DOWNLOADS_FOLDER, "sbase_ext")
        _unzip_to_new_folder(sbase_ext_zip, sbase_ext_dir)
        chrome_options = add_chrome_ext_dir(chrome_options, sbase_ext_dir)
    if proxy_string:
        if proxy_auth:
            zip_it = True
            if is_using_uc(undetectable, browser_name):
                zip_it = False  # undetected-chromedriver needs a folder ext
            chrome_options = _add_chrome_proxy_extension(
                chrome_options,
                proxy_string,
                proxy_user,
                proxy_pass,
                proxy_bypass_list,
                zip_it,
                multi_proxy,
            )
        chrome_options.add_argument("--proxy-server=%s" % proxy_string)
        if proxy_bypass_list:
            chrome_options.add_argument(
                "--proxy-bypass-list=%s" % proxy_bypass_list
            )
    elif proxy_pac_url:
        if proxy_auth:
            zip_it = True  # undetected-chromedriver needs a folder ext
            if is_using_uc(undetectable, browser_name):
                zip_it = False
            chrome_options = _add_chrome_proxy_extension(
                chrome_options,
                None,
                proxy_user,
                proxy_pass,
                proxy_bypass_list,
                zip_it,
                multi_proxy,
            )
        chrome_options.add_argument("--proxy-pac-url=%s" % proxy_pac_url)
    if (
        not is_using_uc(undetectable, browser_name)
        or not enable_ws
        or proxy_string
    ):
        chrome_options.add_argument("--ignore-certificate-errors")
    if not enable_ws:
        chrome_options.add_argument("--disable-web-security")
    if (
        IS_LINUX
        or (IS_MAC and not is_using_uc(undetectable, browser_name))
    ):
        chrome_options.add_argument("--no-sandbox")
    if remote_debug:
        # To access the Debugger, go to: chrome://inspect/#devices
        # while a Chromium driver is running.
        # Info: https://chromedevtools.github.io/devtools-protocol/
        args = " ".join(sys.argv)
        debug_port = 9222
        if ("-n" in sys.argv or " -n=" in args or args == "-c"):
            debug_port = service_utils.free_port()
        chrome_options.add_argument("--remote-debugging-port=%s" % debug_port)
    if swiftshader:
        chrome_options.add_argument("--use-gl=angle")
        chrome_options.add_argument("--use-angle=swiftshader-webgl")
    elif (
        not is_using_uc(undetectable, browser_name)
        and not enable_3d_apis
    ):
        chrome_options.add_argument("--disable-gpu")
    if not IS_LINUX and is_using_uc(undetectable, browser_name):
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-application-cache")
    if IS_LINUX:
        chrome_options.add_argument("--disable-dev-shm-usage")
        if is_using_uc(undetectable, browser_name):
            chrome_options.add_argument("--disable-application-cache")
            chrome_options.add_argument("--disable-setuid-sandbox")
            if not binary_location:
                br_app = "google-chrome"
                binary_loc = detect_b_ver.get_binary_location(br_app, True)
                if os.path.exists(binary_loc):
                    binary_location = binary_loc
    extra_disabled_features = []
    if chromium_arg:
        # Can be a comma-separated list of Chromium args or a list
        chromium_arg_list = None
        if isinstance(chromium_arg, (list, tuple)):
            chromium_arg_list = chromium_arg
        else:
            chromium_arg_list = chromium_arg.split(",")
        for chromium_arg_item in chromium_arg_list:
            chromium_arg_item = chromium_arg_item.strip()
            if not chromium_arg_item.startswith("--"):
                if chromium_arg_item.startswith("-"):
                    chromium_arg_item = "-" + chromium_arg_item
                else:
                    chromium_arg_item = "--" + chromium_arg_item
            if "remote-debugging-port=" in chromium_arg_item:
                with suppress(Exception):
                    # Extra processing for UC Mode
                    chrome_options._remote_debugging_port = int(
                        chromium_arg_item.split("remote-debugging-port=")[1]
                    )
            if "set-binary" in chromium_arg_item and not binary_location:
                br_app = "google-chrome"
                binary_loc = detect_b_ver.get_binary_location(
                    br_app, is_using_uc(undetectable, browser_name)
                )
                if os.path.exists(binary_loc):
                    binary_location = binary_loc
            elif "disable-features=" in chromium_arg_item:
                d_f = chromium_arg_item.split("disable-features=")[-1]
                extra_disabled_features.append(d_f)
            elif len(chromium_arg_item) >= 3:
                chrome_options.add_argument(chromium_arg_item)
    if disable_features:
        extra_disabled_features.extend(disable_features.split(","))
    if devtools and not headless:
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
    if user_agent:
        chrome_options.add_argument("--user-agent=%s" % user_agent)
    chrome_options.add_argument("--safebrowsing-disable-download-protection")
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-single-click-autofill")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--disable-prompt-on-repost")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-translate")
    if binary_location:
        chrome_options.binary_location = binary_location
    if not enable_3d_apis and not is_using_uc(undetectable, browser_name):
        chrome_options.add_argument("--disable-3d-apis")
    if headless or headless2 or is_using_uc(undetectable, browser_name):
        chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-oopr-debug-crash-dump")
    chrome_options.add_argument("--disable-top-sites")
    chrome_options.add_argument("--ash-no-nudges")
    chrome_options.add_argument("--no-crash-upload")
    chrome_options.add_argument("--deny-permission-prompts")
    chrome_options.add_argument(
        '--simulate-outdated-no-au="Tue, 31 Dec 2099 23:59:59 GMT"'
    )
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--disable-password-generation")
    chrome_options.add_argument("--disable-domain-reliability")
    chrome_options.add_argument("--disable-component-update")
    chrome_options.add_argument("--disable-breakpad")
    included_disabled_features = []
    included_disabled_features.append("OptimizationHints")
    included_disabled_features.append("OptimizationHintsFetching")
    included_disabled_features.append("Translate")
    included_disabled_features.append("OptimizationTargetPrediction")
    included_disabled_features.append("OptimizationGuideModelDownloading")
    included_disabled_features.append("DownloadBubble")
    included_disabled_features.append("DownloadBubbleV2")
    included_disabled_features.append("InsecureDownloadWarnings")
    included_disabled_features.append("InterestFeedContentSuggestions")
    included_disabled_features.append("PrivacySandboxSettings4")
    included_disabled_features.append("SidePanelPinning")
    included_disabled_features.append("UserAgentClientHint")
    for item in extra_disabled_features:
        if item not in included_disabled_features:
            included_disabled_features.append(item)
    d_f_string = ",".join(included_disabled_features)
    chrome_options.add_argument("--disable-features=%s" % d_f_string)
    if (
        is_using_uc(undetectable, browser_name)
        and (
            not headless
            or IS_LINUX  # switches to Xvfb (non-headless)
        )
    ):
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--homepage=chrome://new-tab-page/")
        # Skip remaining options that trigger anti-bot services
        return chrome_options
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument(
        "--disable-autofill-keyboard-accessory-view[8]"
    )
    chrome_options.add_argument("--homepage=about:blank")
    chrome_options.add_argument("--dom-automation")
    chrome_options.add_argument("--disable-hang-monitor")
    return chrome_options


def _set_firefox_options(
    downloads_path,
    headless,
    locale_code,
    proxy_string,
    proxy_bypass_list,
    proxy_pac_url,
    user_agent,
    disable_cookies,
    disable_js,
    disable_csp,
    firefox_arg,
    firefox_pref,
    external_pdf,
):
    blank_p = "about:blank"
    options = webdriver.FirefoxOptions()
    options.accept_untrusted_certs = True
    options.set_preference("reader.parse-on-load.enabled", False)
    options.set_preference("browser.startup.homepage", blank_p)
    options.set_preference("startup.homepage_welcome_url", blank_p)
    options.set_preference("startup.homepage_welcome_url.additional", blank_p)
    options.set_preference("browser.newtab.url", blank_p)
    options.set_preference("trailhead.firstrun.branches", "nofirstrun-empty")
    options.set_preference("browser.aboutwelcome.enabled", False)
    options.set_preference("app.update.auto", False)
    options.set_preference("app.update.enabled", False)
    options.set_preference("browser.formfill.enable", False)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("dom.disable_beforeunload", True)
    options.set_preference("browser.contentblocking.database.enabled", True)
    options.set_preference("extensions.allowPrivateBrowsingByDefault", True)
    options.set_preference("extensions.PrivateBrowsing.notification", False)
    options.set_preference("extensions.systemAddon.update.enabled", False)
    options.set_preference("extensions.update.autoUpdateDefault", False)
    options.set_preference("extensions.update.enabled", False)
    options.set_preference("datareporting.healthreport.service.enabled", False)
    options.set_preference("datareporting.healthreport.uploadEnabled", False)
    options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
    options.set_preference("browser.search.update", False)
    options.set_preference("privacy.trackingprotection.enabled", False)
    options.set_preference("toolkit.telemetry.enabled", False)
    options.set_preference("toolkit.telemetry.unified", False)
    options.set_preference("toolkit.telemetry.archive.enabled", False)
    if proxy_string:
        socks_proxy = False
        socks_ver = 0
        chunks = proxy_string.split(":")
        if len(chunks) == 3 and (
            chunks[0] == "socks4" or chunks[0] == "socks5"
        ):
            socks_proxy = True
            socks_ver = int(chunks[0][5])
            if chunks[1].startswith("//") and len(chunks[1]) > 2:
                chunks[1] = chunks[1][2:]
            proxy_server = chunks[1]
            proxy_port = chunks[2]
        else:
            proxy_server = proxy_string.split(":")[0]
            proxy_port = proxy_string.split(":")[1]
        options.set_preference("network.proxy.type", 1)
        if socks_proxy:
            options.set_preference("network.proxy.socks", proxy_server)
            options.set_preference("network.proxy.socks_port", int(proxy_port))
            options.set_preference("network.proxy.socks_version", socks_ver)
        else:
            options.set_preference("network.proxy.http", proxy_server)
            options.set_preference("network.proxy.http_port", int(proxy_port))
            options.set_preference("network.proxy.ssl", proxy_server)
            options.set_preference("network.proxy.ssl_port", int(proxy_port))
        if proxy_bypass_list:
            options.set_preference("no_proxies_on", proxy_bypass_list)
    elif proxy_pac_url:
        options.set_preference("network.proxy.type", 2)
        options.set_preference("network.proxy.autoconfig_url", proxy_pac_url)
    if user_agent:
        options.set_preference("general.useragent.override", user_agent)
    options.set_preference(
        "security.mixed_content.block_active_content", False
    )
    options.set_preference("security.warn_submit_insecure", False)
    if disable_cookies:
        options.set_preference("network.cookie.cookieBehavior", 2)
    if disable_js:
        options.set_preference("javascript.enabled", False)
    if settings.DISABLE_CSP_ON_FIREFOX or disable_csp:
        options.set_preference("security.csp.enable", False)
    options.set_preference(
        "browser.download.manager.showAlertOnComplete", False
    )
    if headless and not IS_LINUX:
        options.add_argument("--headless")
    elif headless and IS_LINUX:
        # This assumes Xvfb is running, which prevents many Linux issues.
        # If not, we'll fix this later during the error-handling process.
        # To override this feature: ``pytest --firefox-arg="-headless"``.
        pass
    if locale_code:
        options.set_preference("intl.accept_languages", locale_code)
    options.set_preference("browser.shell.checkDefaultBrowser", False)
    options.set_preference("browser.startup.page", 0)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.animateNotifications", False)
    options.set_preference("browser.download.dir", downloads_path)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        (
            "application/pdf,application/zip,application/octet-stream,"
            "text/csv,text/xml,application/xml,text/plain,application/json,"
            "text/octet-stream,application/x-gzip,application/x-tar,"
            "application/java-archive,text/x-java-source,java,"
            "application/javascript,video/jpeg,audio/x-aac,image/svg+xml,"
            "application/x-font-woff,application/x-7z-compressed,"
            "application/mp4,video/mp4,audio/mp4,video/x-msvideo,"
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
    if external_pdf:
        options.set_preference("pdfjs.disabled", True)
    else:
        options.set_preference("pdfjs.disabled", False)
    if firefox_arg:
        # Can be a comma-separated list of Firefox args
        firefox_arg_list = firefox_arg.split(",")
        for firefox_arg_item in firefox_arg_list:
            firefox_arg_item = firefox_arg_item.strip()
            if not firefox_arg_item.startswith("--"):
                if firefox_arg_item.startswith("-"):
                    firefox_arg_item = "-" + firefox_arg_item
                else:
                    firefox_arg_item = "--" + firefox_arg_item
            if len(firefox_arg_item) >= 3:
                options.add_argument(firefox_arg_item)
    if firefox_pref:
        # Can be a comma-separated list of Firefox preference:value pairs
        firefox_pref_list = firefox_pref.split(",")
        for firefox_pref_item in firefox_pref_list:
            f_pref = None
            f_pref_value = None
            needs_conversion = False
            if firefox_pref_item.count(":") == 0:
                f_pref = firefox_pref_item
                f_pref_value = True
            elif firefox_pref_item.count(":") == 1:
                f_pref = firefox_pref_item.split(":")[0]
                f_pref_value = firefox_pref_item.split(":")[1]
                needs_conversion = True
            elif firefox_pref_item.count("://") == 1:
                f_pref = firefox_pref_item.split(":")[0]
                f_pref_value = ":".join(firefox_pref_item.split(":")[1:])
            else:  # More than one ":" in the set without a URL.
                raise Exception(
                    'Incorrect formatting for Firefox "pref:value" set!'
                )
            if needs_conversion:
                if f_pref_value.lower() == "true" or len(f_pref_value) == 0:
                    f_pref_value = True
                elif f_pref_value.lower() == "false":
                    f_pref_value = False
                elif f_pref_value.isdigit():
                    f_pref_value = int(f_pref_value)
                elif f_pref_value.replace(".", "", 1).isdigit():
                    f_pref_value = float(f_pref_value)
                else:
                    pass  # keep as string
            if len(f_pref) >= 1:
                options.set_preference(f_pref, f_pref_value)
    return options


def get_driver(
    browser_name=None,
    headless=False,
    locale_code=None,
    use_grid=False,
    protocol="http",
    servername="localhost",
    port=4444,
    proxy_string=None,
    proxy_bypass_list=None,
    proxy_pac_url=None,
    multi_proxy=None,
    user_agent=None,
    cap_file=None,
    cap_string=None,
    recorder_ext=False,
    disable_cookies=False,
    disable_js=False,
    disable_csp=False,
    enable_ws=False,
    enable_sync=False,
    use_auto_ext=False,
    undetectable=False,
    uc_cdp_events=False,
    uc_subprocess=False,
    log_cdp_events=False,
    no_sandbox=False,
    disable_gpu=False,
    headless1=False,
    headless2=False,
    incognito=False,
    guest_mode=False,
    dark_mode=False,
    devtools=False,
    remote_debug=False,
    enable_3d_apis=False,
    swiftshader=False,
    ad_block_on=False,
    host_resolver_rules=None,
    block_images=False,
    do_not_track=False,
    chromium_arg=None,
    firefox_arg=None,
    firefox_pref=None,
    user_data_dir=None,
    extension_zip=None,
    extension_dir=None,
    disable_features=None,
    binary_location=None,
    driver_version=None,
    page_load_strategy=None,
    use_wire=False,
    external_pdf=False,
    test_id=None,
    mobile_emulator=False,
    device_width=None,
    device_height=None,
    device_pixel_ratio=None,
    browser=None,  # A duplicate of browser_name to avoid confusion
):
    if not browser_name:
        if browser:
            browser_name = browser
        else:
            browser_name = "chrome"  # The default if not specified
    browser_name = browser_name.lower()
    if headless2 and browser_name == constants.Browser.FIREFOX:
        headless2 = False  # Only for Chromium
        headless = True
    if (
        binary_location
        and isinstance(binary_location, str)
        and (
            browser_name == constants.Browser.GOOGLE_CHROME
            or browser_name == constants.Browser.EDGE
        )
    ):
        if not os.path.exists(binary_location):
            log_d(
                "\nWarning: The Chromium binary specified (%s) was NOT found!"
                "\n(Will use default settings...)\n" % binary_location
            )
            binary_location = None
        elif binary_location.endswith("/") or binary_location.endswith("\\"):
            log_d(
                "\nWarning: The Chromium binary path must be a full path "
                "that includes the driver filename at the end of it!"
                "\n(Will use default settings...)\n" % binary_location
            )
            # Example of a valid binary location path - MacOS:
            # "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            binary_location = None
        else:
            binary_name = binary_location.split("/")[-1].split("\\")[-1]
            valid_names = get_valid_binary_names_for_browser(browser_name)
            if binary_name not in valid_names:
                log_d(
                    "\nWarning: The Chromium binary specified is NOT valid!"
                    '\nExpecting "%s" to be found in %s for the browser / OS!'
                    "\n(Will use default settings...)\n"
                    "" % (binary_name, valid_names)
                )
                binary_location = None
    if (uc_cdp_events or uc_subprocess) and not undetectable:
        undetectable = True
    if mobile_emulator and not user_agent:
        # Use a Pixel user agent by default if not specified
        user_agent = constants.Mobile.AGENT
    if page_load_strategy and page_load_strategy.lower() == "none":
        settings.PAGE_LOAD_STRATEGY = "none"
    proxy_auth = False
    proxy_user = None
    proxy_pass = None
    if proxy_string:
        username_and_password = None
        if "@" in proxy_string:
            # Format => username:password@hostname:port
            try:
                username_and_password = proxy_string.split("@")[0]
                proxy_string = proxy_string.split("@")[1]
                proxy_user = username_and_password.split(":")[0]
                proxy_pass = username_and_password.split(":")[1]
            except Exception:
                raise Exception(
                    "The format for using a proxy server with authentication "
                    'is: "username:password@hostname:port". If using a proxy '
                    'server without auth, the format is: "hostname:port".'
                )
            if browser_name != constants.Browser.GOOGLE_CHROME and (
                browser_name != constants.Browser.EDGE
            ):
                raise Exception(
                    "Chrome or Edge is required when using a proxy server "
                    "that has authentication! (If using a proxy server "
                    "without auth, Chrome, Edge, or Firefox may be used.)"
                )
        proxy_string = proxy_helper.validate_proxy_string(proxy_string)
        if proxy_string and proxy_user and proxy_pass:
            proxy_auth = True
    elif proxy_pac_url:
        username_and_password = None
        if "@" in proxy_pac_url:
            # Format => username:password@PAC_URL.pac
            try:
                username_and_password = proxy_pac_url.split("@")[0]
                proxy_pac_url = proxy_pac_url.split("@")[1]
                proxy_user = username_and_password.split(":")[0]
                proxy_pass = username_and_password.split(":")[1]
            except Exception:
                raise Exception(
                    "The format for using a PAC URL with authentication "
                    'is: "username:password@PAC_URL.pac". If using a PAC '
                    'URL without auth, the format is: "PAC_URL.pac".'
                )
            if browser_name != constants.Browser.GOOGLE_CHROME and (
                browser_name != constants.Browser.EDGE
            ):
                raise Exception(
                    "Chrome or Edge is required when using a PAC URL "
                    "that has authentication! (If using a PAC URL "
                    "without auth, Chrome, Edge, or Firefox may be used.)"
                )
        if not proxy_pac_url.lower().endswith(".pac"):
            raise Exception('The proxy PAC URL must end with ".pac"!')
        if proxy_pac_url and proxy_user and proxy_pass:
            proxy_auth = True
    if (
        is_using_uc(undetectable, browser_name)
        and not IS_LINUX
        and headless
    ):
        headless = False
        headless2 = True
    if (
        headless
        and (
            proxy_auth
            or disable_cookies
            or disable_js
            or ad_block_on
            or disable_csp
            or recorder_ext
            or extension_zip
            or extension_dir
        )
        and (
            browser_name == constants.Browser.GOOGLE_CHROME
            or browser_name == constants.Browser.EDGE
        )
    ):
        # Headless Chrome/Edge doesn't support extensions, which are
        # required when using a proxy server that has authentication,
        # or when using other SeleniumBase extensions (eg: Recorder).
        # Instead, base_case.py will use the SBVirtualDisplay when not
        # using Chrome's built-in headless mode. See link for details:
        # https://bugs.chromium.org/p/chromium/issues/detail?id=706008
        headless = False
        if not IS_LINUX:
            # Use the new headless mode on Chrome if not using Linux:
            # bugs.chromium.org/p/chromium/issues/detail?id=706008#c36
            # Although Linux is technically supported, there are a lot
            # of old versions of Chrome on Linux server machines, and
            # this mode requires a recent version of Chrome to work.
            # Specify "--headless2" as a pytest arg to use on Linux.
            headless2 = True
    if (
        browser_name == constants.Browser.GOOGLE_CHROME
        and user_data_dir
        and len(user_data_dir) < 3
    ):
        raise Exception(
            "Name length of Chrome's User Data Directory must be >= 3."
        )
    if use_grid:
        return get_remote_driver(
            browser_name,
            headless,
            locale_code,
            protocol,
            servername,
            port,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            multi_proxy,
            user_agent,
            cap_file,
            cap_string,
            recorder_ext,
            disable_cookies,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_cdp_events,
            uc_subprocess,
            log_cdp_events,
            no_sandbox,
            disable_gpu,
            headless1,
            headless2,
            incognito,
            guest_mode,
            dark_mode,
            devtools,
            remote_debug,
            enable_3d_apis,
            swiftshader,
            ad_block_on,
            host_resolver_rules,
            block_images,
            do_not_track,
            chromium_arg,
            firefox_arg,
            firefox_pref,
            user_data_dir,
            extension_zip,
            extension_dir,
            disable_features,
            binary_location,
            driver_version,
            page_load_strategy,
            use_wire,
            external_pdf,
            test_id,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )
    else:
        return get_local_driver(
            browser_name,
            headless,
            locale_code,
            servername,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            multi_proxy,
            user_agent,
            recorder_ext,
            disable_cookies,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_cdp_events,
            uc_subprocess,
            log_cdp_events,
            no_sandbox,
            disable_gpu,
            headless1,
            headless2,
            incognito,
            guest_mode,
            dark_mode,
            devtools,
            remote_debug,
            enable_3d_apis,
            swiftshader,
            ad_block_on,
            host_resolver_rules,
            block_images,
            do_not_track,
            chromium_arg,
            firefox_arg,
            firefox_pref,
            user_data_dir,
            extension_zip,
            extension_dir,
            disable_features,
            binary_location,
            driver_version,
            page_load_strategy,
            use_wire,
            external_pdf,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )


def get_remote_driver(
    browser_name,
    headless,
    locale_code,
    protocol,
    servername,
    port,
    proxy_string,
    proxy_auth,
    proxy_user,
    proxy_pass,
    proxy_bypass_list,
    proxy_pac_url,
    multi_proxy,
    user_agent,
    cap_file,
    cap_string,
    recorder_ext,
    disable_cookies,
    disable_js,
    disable_csp,
    enable_ws,
    enable_sync,
    use_auto_ext,
    undetectable,
    uc_cdp_events,
    uc_subprocess,
    log_cdp_events,
    no_sandbox,
    disable_gpu,
    headless1,
    headless2,
    incognito,
    guest_mode,
    dark_mode,
    devtools,
    remote_debug,
    enable_3d_apis,
    swiftshader,
    ad_block_on,
    host_resolver_rules,
    block_images,
    do_not_track,
    chromium_arg,
    firefox_arg,
    firefox_pref,
    user_data_dir,
    extension_zip,
    extension_dir,
    disable_features,
    binary_location,
    driver_version,
    page_load_strategy,
    use_wire,
    external_pdf,
    test_id,
    mobile_emulator,
    device_width,
    device_height,
    device_pixel_ratio,
):
    if use_wire:
        pip_find_lock = fasteners.InterProcessLock(
            constants.PipInstall.FINDLOCK
        )
        with pip_find_lock:  # Prevent issues with multiple processes
            try:
                from seleniumwire import webdriver
                import blinker
                with suppress(Exception):
                    use_blinker_ver = constants.SeleniumWire.BLINKER_VER
                    if blinker.__version__ != use_blinker_ver:
                        shared_utils.pip_install(
                            "blinker", version=use_blinker_ver
                        )
                del blinker
            except Exception:
                shared_utils.pip_install(
                    "blinker", version=constants.SeleniumWire.BLINKER_VER
                )
                shared_utils.pip_install(
                    "selenium-wire", version=constants.SeleniumWire.VER
                )
                from seleniumwire import webdriver
            warnings.simplefilter("ignore", category=DeprecationWarning)
    else:
        from selenium import webdriver

    # Construct the address for connecting to a Selenium Grid
    if servername.startswith("https://"):
        protocol = "https"
        servername = servername.split("https://")[1]
    elif "://" in servername:
        servername = servername.split("://")[1]
    server_with_port = ""
    if ":" not in servername:
        col_port = ":" + str(port)
        first_slash = servername.find("/")
        if first_slash != -1:
            server_with_port = (
                servername[:first_slash] + col_port + servername[first_slash:]
            )
        else:
            server_with_port = servername + col_port
    else:
        server_with_port = servername
    address = "%s://%s" % (protocol, server_with_port)
    if not address.endswith("/wd/hub"):
        if address.endswith("/"):
            address += "wd/hub"
        else:
            address += "/wd/hub"
    downloads_path = DOWNLOADS_FOLDER
    desired_caps = {}
    extra_caps = {}
    if cap_file:
        from seleniumbase.core import capabilities_parser
        desired_caps = capabilities_parser.get_desired_capabilities(cap_file)
    if cap_string:
        import json
        try:
            extra_caps = json.loads(str(cap_string))
        except Exception as e:
            p1 = "Invalid input format for --cap-string:\n  %s" % e
            p2 = "The --cap-string input was: %s" % cap_string
            p3 = (
                "Enclose cap-string in SINGLE quotes; "
                "keys and values in DOUBLE quotes."
            )
            p4 = (
                """Here's an example of correct cap-string usage:\n  """
                """--cap-string='{"browserName":"chrome","name":"test1"}'"""
            )
            raise Exception("%s\n%s\n%s\n%s" % (p1, p2, p3, p4))
        for cap_key in extra_caps.keys():
            desired_caps[cap_key] = extra_caps[cap_key]
    if cap_file or cap_string:
        if "name" in desired_caps.keys():
            if desired_caps["name"] == "*":
                desired_caps["name"] = test_id
    if browser_name == constants.Browser.GOOGLE_CHROME:
        chrome_options = _set_chrome_options(
            browser_name,
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            multi_proxy,
            user_agent,
            recorder_ext,
            disable_cookies,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_cdp_events,
            uc_subprocess,
            log_cdp_events,
            no_sandbox,
            disable_gpu,
            headless1,
            headless2,
            incognito,
            guest_mode,
            dark_mode,
            devtools,
            remote_debug,
            enable_3d_apis,
            swiftshader,
            ad_block_on,
            host_resolver_rules,
            block_images,
            do_not_track,
            chromium_arg,
            user_data_dir,
            extension_zip,
            extension_dir,
            disable_features,
            binary_location,
            driver_version,
            page_load_strategy,
            use_wire,
            external_pdf,
            servername,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )
        capabilities = webdriver.ChromeOptions().to_capabilities()
        # Set custom desired capabilities
        selenoid = False
        selenoid_options = None
        screen_resolution = None
        browser_version = None
        platform_name = None
        extension_capabilities = {}
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
            if key == "selenoid:options":
                selenoid = True
                selenoid_options = desired_caps[key]
            elif key == "screenResolution":
                screen_resolution = desired_caps[key]
            elif key == "version" or key == "browserVersion":
                browser_version = desired_caps[key]
            elif key == "platform" or key == "platformName":
                platform_name = desired_caps[key]
            elif re.match("[a-zA-Z0-9]*:[a-zA-Z0-9]*", key):
                extension_capabilities[key] = desired_caps[key]
        cap_str = str(desired_caps).lower()
        if "browserstack" in cap_str or "bstack" in cap_str:
            chrome_options.set_capability("bstack:options", desired_caps)
        chrome_options.set_capability("cloud:options", capabilities)
        if selenoid:
            snops = selenoid_options
            chrome_options.set_capability("selenoid:options", snops)
        if screen_resolution:
            scres = screen_resolution
            chrome_options.set_capability("screenResolution", scres)
        if browser_version:
            br_vers = browser_version
            chrome_options.set_capability("browserVersion", br_vers)
        if platform_name:
            plat_name = platform_name
            chrome_options.set_capability("platformName", plat_name)
        if extension_capabilities:
            for key in extension_capabilities:
                ext_caps = extension_capabilities
                chrome_options.set_capability(key, ext_caps[key])
        driver = webdriver.Remote(
            command_executor=address,
            options=chrome_options,
        )
        return extend_driver(driver)
    elif browser_name == constants.Browser.FIREFOX:
        firefox_options = _set_firefox_options(
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            disable_cookies,
            disable_js,
            disable_csp,
            firefox_arg,
            firefox_pref,
            external_pdf,
        )
        capabilities = webdriver.FirefoxOptions().to_capabilities()
        capabilities["marionette"] = True
        if IS_LINUX and headless:
            capabilities["moz:firefoxOptions"] = {"args": ["-headless"]}
        # Set custom desired capabilities
        selenoid = False
        selenoid_options = None
        screen_resolution = None
        browser_version = None
        platform_name = None
        extension_capabilities = {}
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
            if key == "selenoid:options":
                selenoid = True
                selenoid_options = desired_caps[key]
            elif key == "screenResolution":
                screen_resolution = desired_caps[key]
            elif key == "version" or key == "browserVersion":
                browser_version = desired_caps[key]
            elif key == "platform" or key == "platformName":
                platform_name = desired_caps[key]
            elif re.match("[a-zA-Z0-9]*:[a-zA-Z0-9]*", key):
                extension_capabilities[key] = desired_caps[key]
        cap_str = str(desired_caps).lower()
        if "browserstack" in cap_str or "bstack" in cap_str:
            firefox_options.set_capability("bstack:options", desired_caps)
        firefox_options.set_capability("cloud:options", capabilities)
        if selenoid:
            snops = selenoid_options
            firefox_options.set_capability("selenoid:options", snops)
        if screen_resolution:
            scres = screen_resolution
            firefox_options.set_capability("screenResolution", scres)
        if browser_version:
            br_vers = browser_version
            firefox_options.set_capability("browserVersion", br_vers)
        if platform_name:
            plat_name = platform_name
            firefox_options.set_capability("platformName", plat_name)
        if extension_capabilities:
            for key in extension_capabilities:
                ext_caps = extension_capabilities
                firefox_options.set_capability(key, ext_caps[key])
        driver = webdriver.Remote(
            command_executor=address,
            options=firefox_options,
        )
        return extend_driver(driver)
    elif browser_name == constants.Browser.INTERNET_EXPLORER:
        capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
        remote_options = ArgOptions()
        remote_options.set_capability("cloud:options", desired_caps)
        driver = webdriver.Remote(
            command_executor=address,
            options=remote_options,
        )
        return extend_driver(driver)
    elif browser_name == constants.Browser.EDGE:
        edge_options = _set_chrome_options(
            browser_name,
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            multi_proxy,
            user_agent,
            recorder_ext,
            disable_cookies,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_cdp_events,
            uc_subprocess,
            log_cdp_events,
            no_sandbox,
            disable_gpu,
            headless1,
            headless2,
            incognito,
            guest_mode,
            dark_mode,
            devtools,
            remote_debug,
            enable_3d_apis,
            swiftshader,
            ad_block_on,
            host_resolver_rules,
            block_images,
            do_not_track,
            chromium_arg,
            user_data_dir,
            extension_zip,
            extension_dir,
            disable_features,
            binary_location,
            driver_version,
            page_load_strategy,
            use_wire,
            external_pdf,
            servername,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )
        capabilities = webdriver.EdgeOptions().to_capabilities()
        # Set custom desired capabilities
        selenoid = False
        selenoid_options = None
        screen_resolution = None
        browser_version = None
        platform_name = None
        extension_capabilities = {}
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
            if key == "selenoid:options":
                selenoid = True
                selenoid_options = desired_caps[key]
            elif key == "screenResolution":
                screen_resolution = desired_caps[key]
            elif key == "version" or key == "browserVersion":
                browser_version = desired_caps[key]
            elif key == "platform" or key == "platformName":
                platform_name = desired_caps[key]
            elif re.match("[a-zA-Z0-9]*:[a-zA-Z0-9]*", key):
                extension_capabilities[key] = desired_caps[key]
        edge_options.set_capability("cloud:options", capabilities)
        if selenoid:
            snops = selenoid_options
            edge_options.set_capability("selenoid:options", snops)
        if screen_resolution:
            scres = screen_resolution
            edge_options.set_capability("screenResolution", scres)
        if browser_version:
            br_vers = browser_version
            edge_options.set_capability("browserVersion", br_vers)
        if platform_name:
            plat_name = platform_name
            edge_options.set_capability("platformName", plat_name)
        if extension_capabilities:
            for key in extension_capabilities:
                ext_caps = extension_capabilities
                edge_options.set_capability(key, ext_caps[key])
        driver = webdriver.Remote(
            command_executor=address,
            options=edge_options,
        )
        return extend_driver(driver)
    elif browser_name == constants.Browser.SAFARI:
        capabilities = webdriver.DesiredCapabilities.SAFARI
        remote_options = ArgOptions()
        remote_options.set_capability("cloud:options", desired_caps)
        driver = webdriver.Remote(
            command_executor=address,
            options=remote_options,
        )
        return extend_driver(driver)
    elif browser_name == constants.Browser.REMOTE:
        remote_options = ArgOptions()
        for cap_name, cap_value in desired_caps.items():
            remote_options.set_capability(cap_name, cap_value)
        cap_str = str(desired_caps).lower()
        if "browserstack" in cap_str or "bstack" in cap_str:
            remote_options.set_capability("bstack:options", desired_caps)
        driver = webdriver.Remote(
            command_executor=address,
            options=remote_options,
        )
        return extend_driver(driver)


def get_local_driver(
    browser_name,
    headless,
    locale_code,
    servername,
    proxy_string,
    proxy_auth,
    proxy_user,
    proxy_pass,
    proxy_bypass_list,
    proxy_pac_url,
    multi_proxy,
    user_agent,
    recorder_ext,
    disable_cookies,
    disable_js,
    disable_csp,
    enable_ws,
    enable_sync,
    use_auto_ext,
    undetectable,
    uc_cdp_events,
    uc_subprocess,
    log_cdp_events,
    no_sandbox,
    disable_gpu,
    headless1,
    headless2,
    incognito,
    guest_mode,
    dark_mode,
    devtools,
    remote_debug,
    enable_3d_apis,
    swiftshader,
    ad_block_on,
    host_resolver_rules,
    block_images,
    do_not_track,
    chromium_arg,
    firefox_arg,
    firefox_pref,
    user_data_dir,
    extension_zip,
    extension_dir,
    disable_features,
    binary_location,
    driver_version,
    page_load_strategy,
    use_wire,
    external_pdf,
    mobile_emulator,
    device_width,
    device_height,
    device_pixel_ratio,
):
    """Spins up a new web browser and returns the driver.
    Can also be used to spin up additional browsers for the same test."""
    downloads_path = DOWNLOADS_FOLDER
    b_path = binary_location
    if use_wire:
        pip_find_lock = fasteners.InterProcessLock(
            constants.PipInstall.FINDLOCK
        )
        with pip_find_lock:  # Prevent issues with multiple processes
            try:
                from seleniumwire import webdriver
                import blinker
                with suppress(Exception):
                    use_blinker_ver = constants.SeleniumWire.BLINKER_VER
                    if blinker.__version__ != use_blinker_ver:
                        shared_utils.pip_install(
                            "blinker", version=use_blinker_ver
                        )
                del blinker
            except Exception:
                shared_utils.pip_install(
                    "blinker", version=constants.SeleniumWire.BLINKER_VER
                )
                shared_utils.pip_install(
                    "selenium-wire", version=constants.SeleniumWire.VER
                )
                from seleniumwire import webdriver
            warnings.simplefilter("ignore", category=DeprecationWarning)
    else:
        from selenium import webdriver

    if browser_name == constants.Browser.FIREFOX:
        firefox_options = _set_firefox_options(
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            disable_cookies,
            disable_js,
            disable_csp,
            firefox_arg,
            firefox_pref,
            external_pdf,
        )
        if LOCAL_GECKODRIVER and os.path.exists(LOCAL_GECKODRIVER):
            try:
                make_driver_executable_if_not(LOCAL_GECKODRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make geckodriver"
                    " executable: %s" % e
                )
        elif not geckodriver_on_path():
            from seleniumbase.console_scripts import sb_install
            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                sys_args = sys.argv  # Save a copy of current sys args
                log_d("\nWarning: geckodriver not found. Getting it now:")
                try:
                    sb_install.main(override="geckodriver")
                except Exception as e:
                    log_d("\nWarning: Could not install geckodriver: %s" % e)
                sys.argv = sys_args  # Put back the original sys args
            else:
                geckodriver_fixing_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                )
                with geckodriver_fixing_lock:
                    if not geckodriver_on_path():
                        sys_args = sys.argv  # Save a copy of sys args
                        log_d(
                            "\nWarning: geckodriver not found. "
                            "Getting it now:"
                        )
                        sb_install.main(override="geckodriver")
                        sys.argv = sys_args  # Put back original sys args
        # Launch Firefox
        if os.path.exists(LOCAL_GECKODRIVER):
            service = FirefoxService(
                executable_path=LOCAL_GECKODRIVER,
                log_output=os.devnull,
            )
            try:
                driver = webdriver.Firefox(
                    service=service,
                    options=firefox_options,
                )
                return extend_driver(driver)
            except BaseException as e:
                if (
                    "geckodriver unexpectedly exited" in str(e)
                    or "Process unexpectedly closed" in str(e)
                    or "Failed to read marionette port" in str(e)
                    or "A connection attempt failed" in str(e)
                    or "Expected browser binary" in str(e)
                    or hasattr(e, "msg") and (
                        "geckodriver unexpectedly exited" in e.msg
                        or "Process unexpectedly closed" in e.msg
                        or "Failed to read marionette port" in e.msg
                        or "A connection attempt failed" in e.msg
                        or "Expected browser binary" in e.msg
                    )
                ):
                    time.sleep(0.1)
                    if (
                        IS_LINUX
                        and headless
                        and (
                            "unexpected" in str(e)
                            or (
                                hasattr(e, "msg") and "unexpected" in e.msg
                            )
                        )
                    ):
                        firefox_options.add_argument("-headless")
                    driver = webdriver.Firefox(
                        service=service,
                        options=firefox_options,
                    )
                    return extend_driver(driver)
                else:
                    raise  # Not an obvious fix.
        else:
            service = FirefoxService(log_output=os.devnull)
            try:
                driver = webdriver.Firefox(
                    service=service,
                    options=firefox_options,
                )
                return extend_driver(driver)
            except BaseException as e:
                if (
                    "geckodriver unexpectedly exited" in str(e)
                    or "Process unexpectedly closed" in str(e)
                    or "Failed to read marionette port" in str(e)
                    or "A connection attempt failed" in str(e)
                    or "Expected browser binary" in str(e)
                    or hasattr(e, "msg") and (
                        "geckodriver unexpectedly exited" in e.msg
                        or "Process unexpectedly closed" in e.msg
                        or "Failed to read marionette port" in e.msg
                        or "A connection attempt failed" in e.msg
                        or "Expected browser binary" in e.msg
                    )
                ):
                    time.sleep(0.1)
                    if (
                        IS_LINUX
                        and headless
                        and (
                            "unexpected" in str(e)
                            or (
                                hasattr(e, "msg") and "unexpected" in e.msg
                            )
                        )
                    ):
                        firefox_options.add_argument("-headless")
                    driver = webdriver.Firefox(
                        service=service,
                        options=firefox_options,
                    )
                    return extend_driver(driver)
                else:
                    raise  # Not an obvious fix.
    elif browser_name == constants.Browser.INTERNET_EXPLORER:
        if not IS_WINDOWS:
            raise Exception(
                "IE Browser is for Windows-based systems only!"
            )
        from selenium.webdriver.ie.options import Options
        from selenium.webdriver.ie.service import Service
        ie_options = Options()
        ie_options.add_argument("--guest")
        ie_options.attach_to_edge_chrome = True
        ie_options.ignore_protected_mode_settings = True
        ie_options.ignore_zoom_level = True
        ie_options.require_window_focus = False
        ie_options.native_events = True
        ie_options.full_page_screenshot = True
        ie_options.persistent_hover = True
        if LOCAL_IEDRIVER and os.path.exists(LOCAL_IEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_IEDRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make IEDriver executable: %s" % e
                )
        elif not iedriver_on_path():
            from seleniumbase.console_scripts import sb_install
            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                sys_args = sys.argv  # Save a copy of current sys args
                log_d("\nWarning: IEDriver not found. Getting it now:")
                sb_install.main(override="iedriver")
                sys.argv = sys_args  # Put back the original sys args
        if LOCAL_HEADLESS_IEDRIVER and os.path.exists(LOCAL_HEADLESS_IEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_HEADLESS_IEDRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make HeadlessIEDriver executable: %s"
                    % e
                )
        elif not headless_iedriver_on_path():
            from seleniumbase.console_scripts import sb_install
            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                sys_args = sys.argv  # Save a copy of current sys args
                log_d("\nWarning: HeadlessIEDriver not found. Getting it now:")
                sb_install.main(override="iedriver")
                sys.argv = sys_args  # Put back the original sys args
        d_b_c = "--disable-build-check"
        logger = logging.getLogger("selenium")
        logger.setLevel("INFO")
        if not headless:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            service = Service(service_args=[d_b_c], log_output=os.devnull)
            driver = webdriver.Ie(service=service, options=ie_options)
            return extend_driver(driver)
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            service = Service(
                executable_path=LOCAL_IEDRIVER,
                service_args=[d_b_c],
                log_output=os.devnull,
            )
            driver = webdriver.Ie(service=service, options=ie_options)
            return extend_driver(driver)
    elif browser_name == constants.Browser.EDGE:
        prefs = {
            "download.default_directory": downloads_path,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "credentials_enable_service": False,
            "local_discovery.notifications_enabled": False,
            "safebrowsing.disable_download_protection": True,
            "safebrowsing.enabled": False,  # Prevent PW "data breach" pop-ups
            "omnibox-max-zero-suggest-matches": 0,
            "omnibox-use-existing-autocomplete-client": 0,
            "omnibox-trending-zero-prefix-suggestions-on-ntp": 0,
            "omnibox-local-history-zero-suggest-beyond-ntp": 0,
            "omnibox-on-focus-suggestions-contextual-web": 0,
            "omnibox-on-focus-suggestions-srp": 0,
            "omnibox-zero-suggest-prefetching": 0,
            "omnibox-zero-suggest-prefetching-on-srp": 0,
            "omnibox-zero-suggest-prefetching-on-web": 0,
            "omnibox-zero-suggest-in-memory-caching": 0,
            "content_settings.exceptions.automatic_downloads.*.setting": 1,
            "default_content_setting_values.notifications": 0,
            "default_content_settings.popups": 0,
            "managed_default_content_settings.popups": 0,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads": 1,
        }
        use_version = "latest"
        major_edge_version = None
        saved_mev = None
        use_br_version_for_edge = False
        use_exact_version_for_edge = False
        try:
            if binary_location:
                try:
                    major_edge_version = (
                        detect_b_ver.get_browser_version_from_binary(
                            binary_location
                        )
                    )
                    saved_mev = major_edge_version
                    major_edge_version = saved_mev.split(".")[0]
                    if len(major_edge_version) < 2:
                        major_edge_version = None
                except Exception:
                    major_edge_version = None
            if not major_edge_version:
                br_app = "edge"
                major_edge_version = (
                    detect_b_ver.get_browser_version_from_os(br_app)
                )
                saved_mev = major_edge_version
                major_edge_version = major_edge_version.split(".")[0]
            if int(major_edge_version) < 80:
                major_edge_version = None
            elif int(major_edge_version) >= 115:
                if (
                    driver_version == "browser"
                    and saved_mev
                    and len(saved_mev.split(".")) == 4
                ):
                    driver_version = saved_mev
                    use_br_version_for_edge = True
        except Exception:
            major_edge_version = None
        if driver_version and "." in driver_version:
            use_exact_version_for_edge = True
        if use_br_version_for_edge:
            major_edge_version = saved_mev
        if major_edge_version:
            use_version = major_edge_version
        edge_driver_version = None
        edgedriver_upgrade_needed = False
        if os.path.exists(LOCAL_EDGEDRIVER):
            with suppress(Exception):
                output = subprocess.check_output(
                    '"%s" --version' % LOCAL_EDGEDRIVER, shell=True
                )
                if IS_WINDOWS:
                    output = output.decode("latin1")
                else:
                    output = output.decode("utf-8")
                if output.split(" ")[0] == "MSEdgeDriver":
                    # MSEdgeDriver VERSION
                    output = output.split(" ")[1]
                    if use_exact_version_for_edge:
                        edge_driver_version = output.split(" ")[0]
                    output = output.split(".")[0]
                elif output.split(" ")[0] == "Microsoft":
                    output = output.split(" ")[3]
                    if use_exact_version_for_edge:
                        edge_driver_version = output.split(" ")[0]
                    output = output.split(".")[0]
                else:
                    output = 0
                if int(output) >= 2:
                    if not use_exact_version_for_edge:
                        edge_driver_version = output
                    if driver_version == "keep":
                        driver_version = edge_driver_version
        use_version = find_edgedriver_version_to_use(
            use_version, driver_version
        )
        local_edgedriver_exists = False
        if LOCAL_EDGEDRIVER and os.path.exists(LOCAL_EDGEDRIVER):
            local_edgedriver_exists = True
            if (
                use_version != "latest"
                and edge_driver_version
                and use_version != edge_driver_version
            ):
                edgedriver_upgrade_needed = True
            else:
                try:
                    make_driver_executable_if_not(LOCAL_EDGEDRIVER)
                except Exception as e:
                    logging.debug(
                        "\nWarning: Could not make edgedriver"
                        " executable: %s" % e
                    )
        if not local_edgedriver_exists or edgedriver_upgrade_needed:
            from seleniumbase.console_scripts import sb_install
            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                msg = "Microsoft Edge Driver not found."
                if edgedriver_upgrade_needed:
                    msg = "Microsoft Edge Driver update needed."
                sys_args = sys.argv  # Save a copy of current sys args
                log_d("\n%s Getting it now:" % msg)
                sb_install.main(override="edgedriver %s" % use_version)
                sys.argv = sys_args  # Put back the original sys args
            else:
                edgedriver_fixing_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                )
                with edgedriver_fixing_lock:
                    msg = "Microsoft Edge Driver not found."
                    if edgedriver_upgrade_needed:
                        msg = "Microsoft Edge Driver update needed."
                    sys_args = sys.argv  # Save a copy of current sys args
                    log_d("\n%s Getting it now:" % msg)
                    sb_install.main(override="edgedriver %s" % use_version)
                    sys.argv = sys_args  # Put back the original sys args

        # For Microsoft Edge (Chromium) version 80 or higher
        Edge = webdriver.edge.webdriver.WebDriver
        EdgeOptions = webdriver.edge.webdriver.Options
        if LOCAL_EDGEDRIVER and os.path.exists(LOCAL_EDGEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_EDGEDRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make edgedriver"
                    " executable: %s" % e
                )
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        if locale_code:
            prefs["intl.accept_languages"] = locale_code
        if block_images:
            prefs["profile.managed_default_content_settings.images"] = 2
        if disable_cookies:
            prefs["profile.default_content_setting_values.cookies"] = 2
        if disable_js:
            prefs["profile.managed_default_content_settings.javascript"] = 2
        if do_not_track:
            prefs["enable_do_not_track"] = True
        if external_pdf:
            prefs["plugins.always_open_pdf_externally"] = True
        pdce = "user_experience_metrics.personalization_data_consent_enabled"
        prefs[pdce] = True  # Remove "Personalize your web experience" prompt
        edge_options.add_experimental_option("prefs", prefs)
        edge_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        edge_options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        if log_cdp_events:
            edge_options.set_capability(
                "ms:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
            )
        if host_resolver_rules:
            edge_options.add_argument(
                "--host-resolver-rules=%s" % host_resolver_rules
            )
        if not enable_sync:
            edge_options.add_argument("--disable-sync")
        if (
            not recorder_ext and not disable_csp and not proxy_auth
        ):
            edge_options.add_argument("--guest")
        if dark_mode:
            edge_options.add_argument("--enable-features=WebContentsForceDark")
        if headless2:
            try:
                if use_version == "latest" or int(use_version) >= 109:
                    edge_options.add_argument("--headless=new")
                else:
                    edge_options.add_argument("--headless=chrome")
            except Exception:
                edge_options.add_argument("--headless=new")
        elif headless and undetectable:
            # (For later: UC Mode doesn't support Edge now)
            with suppress(Exception):
                if int(use_version) >= 109:
                    edge_options.add_argument("--headless=new")
                elif (
                    int(use_version) >= 96
                    and int(use_version) <= 108
                ):
                    edge_options.add_argument("--headless=chrome")
                else:
                    pass  # Will need Xvfb on Linux
        elif headless:
            if (
                "--headless" not in edge_options.arguments
                and "--headless=old" not in edge_options.arguments
            ):
                if headless1:
                    edge_options.add_argument("--headless=old")
                else:
                    edge_options.add_argument("--headless")
        if mobile_emulator and not is_using_uc(undetectable, browser_name):
            emulator_settings = {}
            device_metrics = {}
            if (
                isinstance(device_width, int)
                and isinstance(device_height, int)
                and isinstance(device_pixel_ratio, (int, float))
            ):
                device_metrics["width"] = device_width
                device_metrics["height"] = device_height
                device_metrics["pixelRatio"] = device_pixel_ratio
            else:
                device_metrics["width"] = constants.Mobile.WIDTH
                device_metrics["height"] = constants.Mobile.HEIGHT
                device_metrics["pixelRatio"] = constants.Mobile.RATIO
            emulator_settings["deviceMetrics"] = device_metrics
            if user_agent:
                emulator_settings["userAgent"] = user_agent
            edge_options.add_experimental_option(
                "mobileEmulation", emulator_settings
            )
        # Handle Window Position
        if (headless or headless2) and IS_WINDOWS:
            # https://stackoverflow.com/a/78999088/7058266
            edge_options.add_argument("--window-position=-2400,-2400")
        else:
            if (
                hasattr(settings, "WINDOW_START_X")
                and isinstance(settings.WINDOW_START_X, int)
                and hasattr(settings, "WINDOW_START_Y")
                and isinstance(settings.WINDOW_START_Y, int)
            ):
                edge_options.add_argument(
                    "--window-position=%s,%s" % (
                        settings.WINDOW_START_X, settings.WINDOW_START_Y
                    )
                )
        # Handle Window Size
        if headless or headless2:
            if (
                hasattr(settings, "HEADLESS_START_WIDTH")
                and isinstance(settings.HEADLESS_START_WIDTH, int)
                and hasattr(settings, "HEADLESS_START_HEIGHT")
                and isinstance(settings.HEADLESS_START_HEIGHT, int)
            ):
                edge_options.add_argument(
                    "--window-size=%s,%s" % (
                        settings.HEADLESS_START_WIDTH,
                        settings.HEADLESS_START_HEIGHT,
                    )
                )
        else:
            if (
                hasattr(settings, "CHROME_START_WIDTH")
                and isinstance(settings.CHROME_START_WIDTH, int)
                and hasattr(settings, "CHROME_START_HEIGHT")
                and isinstance(settings.CHROME_START_HEIGHT, int)
            ):
                edge_options.add_argument(
                    "--window-size=%s,%s" % (
                        settings.CHROME_START_WIDTH,
                        settings.CHROME_START_HEIGHT,
                    )
                )
        if user_data_dir and not is_using_uc(undetectable, browser_name):
            abs_path = os.path.abspath(user_data_dir)
            edge_options.add_argument("--user-data-dir=%s" % abs_path)
        if extension_zip:
            # Can be a comma-separated list of .ZIP or .CRX files
            extension_zip_list = extension_zip.split(",")
            for extension_zip_item in extension_zip_list:
                abs_path = os.path.abspath(extension_zip_item)
                edge_options.add_extension(abs_path)
        if extension_dir:
            # load-extension input can be a comma-separated list
            abs_path = os.path.abspath(extension_dir)
            edge_options = add_chrome_ext_dir(edge_options, abs_path)
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-save-password-bubble")
        edge_options.add_argument("--disable-single-click-autofill")
        edge_options.add_argument(
            "--disable-autofill-keyboard-accessory-view[8]"
        )
        edge_options.add_argument("--safebrowsing-disable-download-protection")
        edge_options.add_argument("--disable-search-engine-choice-screen")
        edge_options.add_argument("--disable-browser-side-navigation")
        edge_options.add_argument("--disable-translate")
        if not enable_ws:
            edge_options.add_argument("--disable-web-security")
        edge_options.add_argument("--homepage=about:blank")
        edge_options.add_argument("--dns-prefetch-disable")
        edge_options.add_argument("--dom-automation")
        edge_options.add_argument("--disable-hang-monitor")
        edge_options.add_argument("--disable-prompt-on-repost")
        if not enable_3d_apis:
            edge_options.add_argument("--disable-3d-apis")
        if headless or headless2 or is_using_uc(undetectable, browser_name):
            edge_options.add_argument("--disable-renderer-backgrounding")
        edge_options.add_argument("--disable-backgrounding-occluded-windows")
        edge_options.add_argument("--disable-client-side-phishing-detection")
        edge_options.add_argument("--disable-oopr-debug-crash-dump")
        edge_options.add_argument("--disable-top-sites")
        edge_options.add_argument("--ash-no-nudges")
        edge_options.add_argument("--no-crash-upload")
        edge_options.add_argument("--deny-permission-prompts")
        if (
            page_load_strategy
            and page_load_strategy.lower() in ["eager", "none"]
        ):
            # Only change it if not "normal", which is the default.
            edge_options.page_load_strategy = page_load_strategy.lower()
        elif (
            not page_load_strategy
            and hasattr(settings, "PAGE_LOAD_STRATEGY")
            and settings.PAGE_LOAD_STRATEGY
            and settings.PAGE_LOAD_STRATEGY.lower() in ["eager", "none"]
        ):
            # Only change it if not "normal", which is the default.
            edge_options.page_load_strategy = (
                settings.PAGE_LOAD_STRATEGY.lower()
            )
        if (settings.DISABLE_CSP_ON_CHROME or disable_csp) and not headless:
            # Headless Edge doesn't support extensions, which are required
            # for disabling the Content Security Policy on Edge
            edge_options = _add_chrome_disable_csp_extension(edge_options)
        if ad_block_on and not headless:
            edge_options = _add_chrome_ad_block_extension(edge_options)
        if recorder_ext and not headless:
            edge_options = _add_chrome_recorder_extension(edge_options)
        if proxy_string:
            if proxy_auth:
                edge_options = _add_chrome_proxy_extension(
                    edge_options,
                    proxy_string,
                    proxy_user,
                    proxy_pass,
                    proxy_bypass_list,
                    zip_it=True,
                    multi_proxy=multi_proxy,
                )
            edge_options.add_argument("--proxy-server=%s" % proxy_string)
            if proxy_bypass_list:
                edge_options.add_argument(
                    "--proxy-bypass-list=%s" % proxy_bypass_list
                )
        elif proxy_pac_url:
            if proxy_auth:
                edge_options = _add_chrome_proxy_extension(
                    edge_options,
                    None,
                    proxy_user,
                    proxy_pass,
                    proxy_bypass_list,
                    zip_it=True,
                    multi_proxy=multi_proxy,
                )
            edge_options.add_argument("--proxy-pac-url=%s" % proxy_pac_url)
        edge_options.add_argument("--test-type")
        edge_options.add_argument("--log-level=3")
        edge_options.add_argument("--no-first-run")
        edge_options.add_argument("--ignore-certificate-errors")
        if devtools and not headless:
            edge_options.add_argument("--auto-open-devtools-for-tabs")
        edge_options.add_argument("--allow-file-access-from-files")
        edge_options.add_argument("--allow-insecure-localhost")
        edge_options.add_argument("--allow-running-insecure-content")
        if user_agent:
            edge_options.add_argument("--user-agent=%s" % user_agent)
        if (
            IS_LINUX
            or (IS_MAC and not is_using_uc(undetectable, browser_name))
        ):
            edge_options.add_argument("--no-sandbox")
        if remote_debug:
            # To access the Debugger, go to: edge://inspect/#devices
            # while a Chromium driver is running.
            # Info: https://chromedevtools.github.io/devtools-protocol/
            args = " ".join(sys.argv)
            free_port = 9222
            if ("-n" in sys.argv or " -n=" in args or args == "-c"):
                free_port = service_utils.free_port()
            edge_options.add_argument("--remote-debugging-port=%s" % free_port)
        if swiftshader:
            edge_options.add_argument("--use-gl=angle")
            edge_options.add_argument("--use-angle=swiftshader-webgl")
        elif (
            not is_using_uc(undetectable, browser_name)
            and not enable_3d_apis
        ):
            edge_options.add_argument("--disable-gpu")
        if IS_LINUX:
            edge_options.add_argument("--disable-dev-shm-usage")
        extra_disabled_features = []
        set_binary = False
        if chromium_arg:
            # Can be a comma-separated list of Chromium args
            chromium_arg_list = None
            if isinstance(chromium_arg, (list, tuple)):
                chromium_arg_list = chromium_arg
            else:
                chromium_arg_list = chromium_arg.split(",")
            for chromium_arg_item in chromium_arg_list:
                chromium_arg_item = chromium_arg_item.strip()
                if not chromium_arg_item.startswith("--"):
                    if chromium_arg_item.startswith("-"):
                        chromium_arg_item = "-" + chromium_arg_item
                    else:
                        chromium_arg_item = "--" + chromium_arg_item
                if "set-binary" in chromium_arg_item:
                    set_binary = True
                elif "disable-features=" in chromium_arg_item:
                    d_f = chromium_arg_item.split("disable-features=")[-1]
                    extra_disabled_features.append(d_f)
                elif len(chromium_arg_item) >= 3:
                    edge_options.add_argument(chromium_arg_item)
        if disable_features:
            extra_disabled_features.extend(disable_features.split(","))
        edge_options.add_argument(
            '--simulate-outdated-no-au="Tue, 31 Dec 2099 23:59:59 GMT"'
        )
        edge_options.add_argument("--disable-ipc-flooding-protection")
        edge_options.add_argument("--disable-password-generation")
        edge_options.add_argument("--disable-domain-reliability")
        edge_options.add_argument("--disable-component-update")
        edge_options.add_argument("--disable-breakpad")
        included_disabled_features = []
        included_disabled_features.append("OptimizationHints")
        included_disabled_features.append("OptimizationHintsFetching")
        included_disabled_features.append("Translate")
        included_disabled_features.append("OptimizationTargetPrediction")
        included_disabled_features.append("OptimizationGuideModelDownloading")
        included_disabled_features.append("InsecureDownloadWarnings")
        included_disabled_features.append("InterestFeedContentSuggestions")
        included_disabled_features.append("PrivacySandboxSettings4")
        included_disabled_features.append("SidePanelPinning")
        included_disabled_features.append("UserAgentClientHint")
        for item in extra_disabled_features:
            if item not in included_disabled_features:
                included_disabled_features.append(item)
        d_f_string = ",".join(included_disabled_features)
        edge_options.add_argument("--disable-features=%s" % d_f_string)
        if (set_binary or IS_LINUX) and not binary_location:
            br_app = "edge"
            binary_loc = detect_b_ver.get_binary_location(br_app)
            if os.path.exists(binary_loc):
                binary_location = binary_loc
        if binary_location:
            edge_options.binary_location = binary_location
        service = EdgeService(
            executable_path=LOCAL_EDGEDRIVER,
            log_output=os.devnull,
            service_args=["--disable-build-check"],
        )
        try:
            driver = Edge(service=service, options=edge_options)
        except Exception as e:
            if not hasattr(e, "msg"):
                raise
            auto_upgrade_edgedriver = False
            edge_version = None
            if (
                "This version of MSEdgeDriver only supports" in e.msg
                or "This version of Microsoft Edge WebDriver" in e.msg
            ):
                if "Current browser version is " in e.msg:
                    auto_upgrade_edgedriver = True
                    edge_version = e.msg.split(
                        "Current browser version is "
                    )[1].split(" ")[0]
                elif "only supports MSEdge version " in e.msg:
                    auto_upgrade_edgedriver = True
                    edge_version = e.msg.split(
                        "only supports MSEdge version "
                    )[1].split(" ")[0]
            elif "DevToolsActivePort file doesn't exist" in e.msg:
                # https://stackoverflow.com/a/56638103/7058266
                args = " ".join(sys.argv)
                free_port = 9222
                if ("-n" in sys.argv or " -n=" in args or args == "-c"):
                    free_port = service_utils.free_port()
                edge_options.add_argument(
                    "--remote-debugging-port=%s" % free_port
                )
                driver = Edge(service=service, options=edge_options)
                return extend_driver(driver)
            if not auto_upgrade_edgedriver:
                raise  # Not an obvious fix.
            else:
                pass  # Try upgrading EdgeDriver to match Edge.
            args = " ".join(sys.argv)
            if "-n" in sys.argv or " -n=" in args or args == "-c":
                edgedriver_fixing_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                )
                with edgedriver_fixing_lock:
                    with suppress(Exception):
                        if not _was_driver_repaired():
                            _repair_edgedriver(edge_version)
                            _mark_driver_repaired()
            else:
                with suppress(Exception):
                    if not _was_driver_repaired():
                        _repair_edgedriver(edge_version)
                    _mark_driver_repaired()
            driver = Edge(service=service, options=edge_options)
        return extend_driver(driver)
    elif browser_name == constants.Browser.SAFARI:
        args = " ".join(sys.argv)
        if ("-n" in sys.argv or " -n=" in args or args == "-c"):
            # Skip if multithreaded
            raise Exception("Can't run Safari tests in multithreaded mode!")
        warnings.simplefilter("ignore", category=DeprecationWarning)
        from selenium.webdriver.safari.options import Options as SafariOptions
        service = SafariService(quiet=False)
        options = SafariOptions()
        if (
            page_load_strategy
            and page_load_strategy.lower() in ["eager", "none"]
        ):
            # Only change it if not "normal", which is the default.
            options.page_load_strategy = page_load_strategy.lower()
        elif (
            not page_load_strategy
            and hasattr(settings, "PAGE_LOAD_STRATEGY")
            and settings.PAGE_LOAD_STRATEGY
            and settings.PAGE_LOAD_STRATEGY.lower() in ["eager", "none"]
        ):
            # Only change it if not "normal", which is the default.
            options.page_load_strategy = settings.PAGE_LOAD_STRATEGY.lower()
        driver = webdriver.safari.webdriver.WebDriver(
            service=service, options=options
        )
        return extend_driver(driver)
    elif browser_name == constants.Browser.GOOGLE_CHROME:
        try:
            chrome_options = _set_chrome_options(
                browser_name,
                downloads_path,
                headless,
                locale_code,
                proxy_string,
                proxy_auth,
                proxy_user,
                proxy_pass,
                proxy_bypass_list,
                proxy_pac_url,
                multi_proxy,
                user_agent,
                recorder_ext,
                disable_cookies,
                disable_js,
                disable_csp,
                enable_ws,
                enable_sync,
                use_auto_ext,
                undetectable,
                uc_cdp_events,
                uc_subprocess,
                log_cdp_events,
                no_sandbox,
                disable_gpu,
                headless1,
                headless2,
                incognito,
                guest_mode,
                dark_mode,
                devtools,
                remote_debug,
                enable_3d_apis,
                swiftshader,
                ad_block_on,
                host_resolver_rules,
                block_images,
                do_not_track,
                chromium_arg,
                user_data_dir,
                extension_zip,
                extension_dir,
                disable_features,
                binary_location,
                driver_version,
                page_load_strategy,
                use_wire,
                external_pdf,
                servername,
                mobile_emulator,
                device_width,
                device_height,
                device_pixel_ratio,
            )
            use_version = "latest"
            major_chrome_version = None
            saved_mcv = None
            full_ch_version = None
            full_ch_driver_version = None
            use_br_version_for_uc = False
            try:
                if chrome_options.binary_location:
                    try:
                        major_chrome_version = (
                            detect_b_ver.get_browser_version_from_binary(
                                chrome_options.binary_location,
                            )
                        )
                        saved_mcv = major_chrome_version
                        major_chrome_version = saved_mcv.split(".")[0]
                        if len(major_chrome_version) < 2:
                            major_chrome_version = None
                    except Exception:
                        major_chrome_version = None
                if not major_chrome_version:
                    br_app = "google-chrome"
                    full_ch_version = (
                        detect_b_ver.get_browser_version_from_os(br_app)
                    )
                    saved_mcv = full_ch_version
                    major_chrome_version = full_ch_version.split(".")[0]
                if int(major_chrome_version) < 67:
                    major_chrome_version = None
                elif (
                    int(major_chrome_version) >= 67
                    and int(major_chrome_version) <= 72
                ):
                    # chromedrivers 2.41 - 2.46 could be swapped with 72
                    major_chrome_version = "72"
                elif int(major_chrome_version) >= 115:
                    if (
                        driver_version == "browser"
                        and saved_mcv
                        and len(saved_mcv.split(".")) == 4
                    ):
                        driver_version = saved_mcv
                        if is_using_uc(undetectable, browser_name):
                            use_br_version_for_uc = True
                    if (
                        (headless or headless2)
                        and IS_WINDOWS
                        and major_chrome_version
                        and int(major_chrome_version) >= 117
                        and not is_using_uc(undetectable, browser_name)
                        and not (remote_debug or devtools or use_wire)
                        and not (proxy_string or multi_proxy or proxy_pac_url)
                        and (not chromium_arg or "debug" not in chromium_arg)
                        and (not servername or servername == "localhost")
                    ):
                        # Hide the "DevTools listening on ..." message.
                        # https://bugs.chromium.org
                        # /p/chromedriver/issues/detail?id=4403#c35
                        # (Only when the remote debugging port is not needed.)
                        chrome_options.add_argument("--remote-debugging-pipe")
            except Exception:
                major_chrome_version = None
            if major_chrome_version:
                use_version = major_chrome_version
            ch_driver_version = None
            path_chromedriver = chromedriver_on_path()
            if os.path.exists(LOCAL_CHROMEDRIVER):
                with suppress(Exception):
                    output = subprocess.check_output(
                        '"%s" --version' % LOCAL_CHROMEDRIVER, shell=True
                    )
                    if IS_WINDOWS:
                        output = output.decode("latin1")
                    else:
                        output = output.decode("utf-8")
                    full_ch_driver_version = output.split(" ")[1]
                    output = full_ch_driver_version.split(".")[0]
                    if int(output) >= 2:
                        ch_driver_version = output
                        if driver_version == "keep":
                            driver_version = ch_driver_version
            elif path_chromedriver:
                try:
                    make_driver_executable_if_not(path_chromedriver)
                except Exception as e:
                    logging.debug(
                        "\nWarning: Could not make chromedriver"
                        " executable: %s" % e
                    )
                with suppress(Exception):
                    output = subprocess.check_output(
                        '"%s" --version' % path_chromedriver, shell=True
                    )
                    if IS_WINDOWS:
                        output = output.decode("latin1")
                    else:
                        output = output.decode("utf-8")
                    full_ch_driver_version = output.split(" ")[1]
                    output = full_ch_driver_version.split(".")[0]
                    if int(output) >= 2:
                        ch_driver_version = output
                        if driver_version == "keep":
                            use_version = ch_driver_version
            disable_build_check = True
            uc_driver_version = None
            if is_using_uc(undetectable, browser_name):
                if use_br_version_for_uc or driver_version == "mlatest":
                    uc_driver_version = get_uc_driver_version(full=True)
                    full_ch_driver_version = uc_driver_version
                else:
                    uc_driver_version = get_uc_driver_version()
                if multi_proxy:
                    sb_config.multi_proxy = True
                if uc_driver_version and driver_version == "keep":
                    driver_version = uc_driver_version
            use_version = find_chromedriver_version_to_use(
                use_version, driver_version
            )
            if headless2:
                try:
                    if (
                        use_version == "latest"
                        or int(str(use_version).split(".")[0]) >= 109
                    ):
                        chrome_options.add_argument("--headless=new")
                    else:
                        chrome_options.add_argument("--headless=chrome")
                except Exception:
                    chrome_options.add_argument("--headless=new")
            elif headless and undetectable:
                try:
                    int_use_version = int(str(use_version).split(".")[0])
                    if int_use_version >= 109:
                        chrome_options.add_argument("--headless=new")
                    elif (
                        int_use_version >= 96
                        and int_use_version <= 108
                    ):
                        chrome_options.add_argument("--headless=chrome")
                    else:
                        pass  # Will need Xvfb on Linux
                except Exception:
                    pass  # Will need Xvfb on Linux
            elif headless:
                if (
                    "--headless" not in chrome_options.arguments
                    and "--headless=old" not in chrome_options.arguments
                ):
                    if headless1:
                        chrome_options.add_argument("--headless=old")
                    else:
                        chrome_options.add_argument("--headless")
            if LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                except Exception as e:
                    logging.debug(
                        "\nWarning: Could not make chromedriver"
                        " executable: %s" % e
                    )
            use_uc = is_using_uc(undetectable, browser_name)
            make_uc_driver_from_chromedriver = False
            local_ch_exists = (
                LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER)
            )
            """If no LOCAL_CHROMEDRIVER, but path_chromedriver, and the
            browser version nearly matches the driver version, then use
            the path_chromedriver instead of downloading a new driver.
            Eg. 116.0.* for both is close, but not 116.0.* and 116.1.*"""
            browser_driver_close_match = False
            if (
                path_chromedriver
                and full_ch_version
                and full_ch_driver_version
            ):
                full_ch_v_p = full_ch_version.split(".")[0:2]
                full_ch_driver_v_p = full_ch_driver_version.split(".")[0:2]
                if (
                    full_ch_v_p == full_ch_driver_v_p
                    or driver_version == "keep"
                ):
                    browser_driver_close_match = True
            # If not ARM MAC and need to use uc_driver (and it's missing),
            # and already have chromedriver with the correct version,
            # then copy chromedriver to uc_driver (and it'll get patched).
            if (
                not IS_ARM_MAC
                and use_uc
                and (
                    (
                        (local_ch_exists or path_chromedriver)
                        and use_version == ch_driver_version
                        and (
                            not os.path.exists(LOCAL_UC_DRIVER)
                            or uc_driver_version != use_version
                        )
                    )
                    or (
                        local_ch_exists
                        and use_version == "latest"
                        and not os.path.exists(LOCAL_UC_DRIVER)
                    )
                )
            ):
                make_uc_driver_from_chromedriver = True
            elif (
                (use_uc and not os.path.exists(LOCAL_UC_DRIVER))
                or (not use_uc and not path_chromedriver)
                or (
                    not use_uc
                    and use_version != "latest"  # Browser version detected
                    and (ch_driver_version or not local_ch_exists)
                    and (
                        use_version.split(".")[0] != ch_driver_version
                        or (
                            not local_ch_exists
                            and use_version.isnumeric()
                            and int(use_version) >= 115
                            and not browser_driver_close_match
                        )
                    )
                )
                or (
                    use_uc
                    and use_version != "latest"  # Browser version detected
                    and uc_driver_version != use_version
                )
                or (
                    full_ch_driver_version  # Also used for the uc_driver
                    and driver_version
                    and len(str(driver_version).split(".")) == 4
                    and full_ch_driver_version != driver_version
                )
            ):
                # chromedriver download needed in the seleniumbase/drivers dir
                from seleniumbase.console_scripts import sb_install
                args = " ".join(sys.argv)
                if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                    # (Not multithreaded)
                    sys_args = sys.argv  # Save a copy of current sys args
                    msg = "chromedriver update needed. Getting it now:"
                    if not path_chromedriver:
                        msg = "chromedriver not found. Getting it now:"
                    if use_uc and not os.path.exists(LOCAL_UC_DRIVER):
                        msg = "uc_driver not found. Getting it now:"
                    if use_uc and os.path.exists(LOCAL_UC_DRIVER):
                        msg = "uc_driver update needed. Getting it now:"
                    log_d("\nWarning: %s" % msg)
                    force_uc = False
                    intel_for_uc = False
                    if use_uc:
                        force_uc = True
                    if IS_ARM_MAC and use_uc:
                        intel_for_uc = True  # Use Intel's driver for UC Mode
                    try:
                        sb_install.main(
                            override="chromedriver %s" % use_version,
                            intel_for_uc=intel_for_uc,
                            force_uc=force_uc,
                        )
                    except Exception:
                        d_latest = get_latest_chromedriver_version()
                        if (
                            d_latest
                            and use_version != "latest"
                            and int(use_version) > int(d_latest.split(".")[0])
                        ):
                            disable_build_check = True
                            d_latest_major = d_latest.split(".")[0]
                            if (
                                not path_chromedriver
                                or (
                                    ch_driver_version
                                    and (
                                        int(ch_driver_version)
                                        < int(d_latest_major)
                                    )
                                )
                            ):
                                sb_install.main(override="chromedriver latest")
                    sys.argv = sys_args  # Put back the original sys args
                else:
                    # (Multithreaded)
                    chromedriver_fixing_lock = fasteners.InterProcessLock(
                        constants.MultiBrowser.DRIVER_FIXING_LOCK
                    )
                    with chromedriver_fixing_lock:
                        msg = "chromedriver update needed. Getting it now:"
                        if not path_chromedriver:
                            msg = "chromedriver not found. Getting it now:"
                        if use_uc and not os.path.exists(LOCAL_UC_DRIVER):
                            msg = "uc_driver not found. Getting it now:"
                        if use_uc and os.path.exists(LOCAL_UC_DRIVER):
                            msg = "uc_driver update needed. Getting it now:"
                        force_uc = False
                        intel_for_uc = False
                        if use_uc:
                            force_uc = True
                        if IS_ARM_MAC and use_uc:
                            intel_for_uc = True  # Use Intel driver for UC Mode
                        if os.path.exists(LOCAL_CHROMEDRIVER):
                            with suppress(Exception):
                                output = subprocess.check_output(
                                    '"%s" --version' % LOCAL_CHROMEDRIVER,
                                    shell=True,
                                )
                                if IS_WINDOWS:
                                    output = output.decode("latin1")
                                else:
                                    output = output.decode("utf-8")
                                full_ch_driver_version = output.split(" ")[1]
                                output = full_ch_driver_version.split(".")[0]
                                if int(output) >= 2:
                                    ch_driver_version = output
                        if (
                            (
                                not use_uc
                                and not os.path.exists(LOCAL_CHROMEDRIVER)
                            )
                            or (use_uc and not os.path.exists(LOCAL_UC_DRIVER))
                            or (
                                not use_uc
                                and (
                                    use_version.split(".")[0]
                                    != ch_driver_version
                                )
                            )
                            or (
                                use_uc
                                and (
                                    use_version.split(".")[0]
                                    != get_uc_driver_version()
                                )
                            )
                        ):
                            log_d("\nWarning: %s" % msg)
                            sys_args = sys.argv  # Save a copy of sys args
                            try:
                                sb_install.main(
                                    override="chromedriver %s" % use_version,
                                    intel_for_uc=intel_for_uc,
                                    force_uc=force_uc,
                                )
                            except Exception:
                                d_latest = get_latest_chromedriver_version()
                                if (
                                    d_latest
                                    and use_version != "latest"
                                    and (
                                        int(use_version)
                                        > int(d_latest.split(".")[0])
                                    )
                                ):
                                    disable_build_check = True
                                    d_latest_major = d_latest.split(".")[0]
                                    if (
                                        not path_chromedriver
                                        or (
                                            ch_driver_version
                                            and (
                                                int(ch_driver_version)
                                                < int(d_latest_major)
                                            )
                                        )
                                    ):
                                        sb_install.main(
                                            override="chromedriver latest"
                                        )
                            finally:
                                sys.argv = sys_args  # Put back original args
            service_args = []
            if disable_build_check:
                service_args = ["--disable-build-check"]
            if is_using_uc(undetectable, browser_name):
                uc_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                )
                with uc_lock:  # Avoid multithreaded issues
                    if make_uc_driver_from_chromedriver:
                        if os.path.exists(LOCAL_CHROMEDRIVER):
                            shutil.copyfile(
                                LOCAL_CHROMEDRIVER, LOCAL_UC_DRIVER
                            )
                        elif os.path.exists(path_chromedriver):
                            shutil.copyfile(
                                path_chromedriver, LOCAL_UC_DRIVER
                            )
                        try:
                            make_driver_executable_if_not(LOCAL_UC_DRIVER)
                        except Exception as e:
                            logging.debug(
                                "\nWarning: Could not make uc_driver"
                                " executable: %s" % e
                            )
            if (
                not headless
                or not IS_LINUX
                or is_using_uc(undetectable, browser_name)
            ):
                uc_activated = False
                try:
                    if (
                        os.path.exists(LOCAL_CHROMEDRIVER)
                        or is_using_uc(undetectable, browser_name)
                    ):
                        if headless and not IS_LINUX:
                            undetectable = False  # No support for headless
                        if is_using_uc(undetectable, browser_name):
                            from seleniumbase import undetected
                            from urllib.error import URLError
                            if IS_LINUX:
                                if "--headless" in (
                                    chrome_options.arguments
                                ):
                                    chrome_options.arguments.remove(
                                        "--headless"
                                    )
                                if "--headless=old" in (
                                    chrome_options.arguments
                                ):
                                    chrome_options.arguments.remove(
                                        "--headless=old"
                                    )
                            uc_chrome_version = None
                            if (
                                use_version.isnumeric()
                                and int(use_version) >= 72
                            ):
                                uc_chrome_version = int(use_version)
                            elif (
                                str(use_version).split(".")[0].isnumeric()
                                and int(str(use_version).split(".")[0]) >= 72
                            ):
                                uc_chrome_version = (
                                    int(str(use_version).split(".")[0])
                                )
                            cdp_events = uc_cdp_events
                            cert = "unable to get local issuer certificate"
                            mac_certificate_error = False
                            if (
                                use_version.isnumeric()
                                and int(use_version) <= 74
                            ):
                                chrome_options.add_experimental_option(
                                    "w3c", True
                                )
                            if (
                                (not user_agent or "Headless" in user_agent)
                                and uc_chrome_version
                                and uc_chrome_version >= 117
                                and (headless or headless2)
                                and hasattr(sb_config, "uc_agent_cache")
                            ):
                                user_agent = sb_config.uc_agent_cache
                                chrome_options.add_argument(
                                    "--user-agent=%s" % user_agent
                                )
                            with suppress(Exception):
                                if (
                                    (
                                        not user_agent
                                        or "Headless" in user_agent
                                    )
                                    and uc_chrome_version
                                    and uc_chrome_version >= 117
                                    and (headless or headless2)
                                ):
                                    from seleniumbase.console_scripts import (
                                        sb_install
                                    )
                                    sb_config.uc_user_agent_cache = True
                                    headless_options = _set_chrome_options(
                                        browser_name,
                                        downloads_path,
                                        True,  # headless
                                        locale_code,
                                        None,  # proxy_string
                                        None,  # proxy_auth
                                        None,  # proxy_user
                                        None,  # proxy_pass
                                        None,  # proxy_bypass_list
                                        None,  # proxy_pac_url
                                        None,  # multi_proxy
                                        None,  # user_agent
                                        None,  # recorder_ext
                                        disable_cookies,
                                        disable_js,
                                        disable_csp,
                                        enable_ws,
                                        enable_sync,
                                        use_auto_ext,
                                        False,  # undetectable
                                        False,  # uc_cdp_events
                                        False,  # uc_subprocess
                                        False,  # log_cdp_events
                                        no_sandbox,
                                        disable_gpu,
                                        False,  # headless1
                                        False,  # headless2
                                        incognito,
                                        guest_mode,
                                        dark_mode,
                                        None,  # devtools
                                        remote_debug,
                                        enable_3d_apis,
                                        swiftshader,
                                        None,  # ad_block_on
                                        None,  # host_resolver_rules
                                        block_images,
                                        do_not_track,
                                        None,  # chromium_arg
                                        None,  # user_data_dir
                                        None,  # extension_zip
                                        None,  # extension_dir
                                        None,  # disable_features
                                        binary_location,
                                        driver_version,
                                        page_load_strategy,
                                        use_wire,
                                        external_pdf,
                                        servername,
                                        mobile_emulator,
                                        device_width,
                                        device_height,
                                        device_pixel_ratio,
                                    )
                                    if (
                                        not path_chromedriver
                                        or (
                                            ch_driver_version
                                            and use_version
                                            and (
                                                int(ch_driver_version)
                                                < int(str(
                                                    use_version).split(".")[0]
                                                )
                                            )
                                        )
                                    ):
                                        sb_install.main(
                                            override="chromedriver %s"
                                            % use_version,
                                            intel_for_uc=False,
                                            force_uc=False,
                                        )
                                    d_b_c = "--disable-build-check"
                                    if os.path.exists(LOCAL_CHROMEDRIVER):
                                        service = ChromeService(
                                            executable_path=LOCAL_CHROMEDRIVER,
                                            log_output=os.devnull,
                                            service_args=[d_b_c],
                                        )
                                        driver = webdriver.Chrome(
                                            service=service,
                                            options=headless_options,
                                        )
                                    else:
                                        service = ChromeService(
                                            log_output=os.devnull,
                                            service_args=[d_b_c],
                                        )
                                        driver = webdriver.Chrome(
                                            service=service,
                                            options=headless_options,
                                        )
                                    with suppress(Exception):
                                        user_agent = driver.execute_script(
                                            "return navigator.userAgent;"
                                        )
                                        if (
                                            major_chrome_version
                                            and full_ch_version
                                            and full_ch_version.count(".") == 3
                                            and full_ch_version in user_agent
                                        ):
                                            mcv = major_chrome_version
                                            user_agent = user_agent.replace(
                                                "Chrome/%s" % full_ch_version,
                                                "Chrome/%s.0.0.0" % mcv
                                            )
                                        user_agent = user_agent.replace(
                                            "Headless", ""
                                        )
                                        chrome_options.add_argument(
                                            "--user-agent=%s" % user_agent
                                        )
                                        sb_config.uc_agent_cache = user_agent
                                    driver.quit()
                            uc_path = None
                            if os.path.exists(LOCAL_UC_DRIVER):
                                uc_path = LOCAL_UC_DRIVER
                                uc_path = os.path.realpath(uc_path)
                            try:
                                driver = undetected.Chrome(
                                    options=chrome_options,
                                    user_data_dir=user_data_dir,
                                    driver_executable_path=uc_path,
                                    browser_executable_path=b_path,
                                    enable_cdp_events=cdp_events,
                                    headless=False,  # Xvfb needed!
                                    version_main=uc_chrome_version,
                                    use_subprocess=True,  # Always!
                                )
                                uc_activated = True
                            except URLError as e:
                                if cert in e.args[0] and IS_MAC:
                                    mac_certificate_error = True
                                else:
                                    raise
                            except SessionNotCreatedException:
                                time.sleep(0.2)
                                driver = undetected.Chrome(
                                    options=chrome_options,
                                    user_data_dir=user_data_dir,
                                    driver_executable_path=uc_path,
                                    browser_executable_path=b_path,
                                    enable_cdp_events=cdp_events,
                                    headless=False,  # Xvfb needed!
                                    version_main=uc_chrome_version,
                                    use_subprocess=True,  # Always!
                                )
                                uc_activated = True
                            if mac_certificate_error:
                                cf_lock_path = (
                                    constants.MultiBrowser.CERT_FIXING_LOCK
                                )
                                cf_lock = fasteners.InterProcessLock(
                                    constants.MultiBrowser.CERT_FIXING_LOCK
                                )
                                if not os.path.exists(cf_lock_path):
                                    # Avoid multithreaded issues
                                    with cf_lock:
                                        # Install Python Certificates (MAC)
                                        os.system(
                                            r"bash /Applications/Python*/"
                                            r"Install\ "
                                            r"Certificates.command"
                                        )
                                driver = undetected.Chrome(
                                    options=chrome_options,
                                    user_data_dir=user_data_dir,
                                    driver_executable_path=uc_path,
                                    browser_executable_path=b_path,
                                    enable_cdp_events=cdp_events,
                                    headless=False,  # Xvfb needed!
                                    version_main=uc_chrome_version,
                                    use_subprocess=True,  # Always!
                                )
                                uc_activated = True
                        else:
                            if (
                                use_version.isnumeric()
                                and int(use_version) <= 74
                            ):
                                chrome_options.add_experimental_option(
                                    "w3c", True
                                )
                            service = ChromeService(
                                executable_path=LOCAL_CHROMEDRIVER,
                                log_output=os.devnull,
                                service_args=service_args,
                            )
                            driver = webdriver.Chrome(
                                service=service,
                                options=chrome_options,
                            )
                    else:
                        service = ChromeService(
                            log_output=os.devnull,
                            service_args=service_args,
                        )
                        driver = webdriver.Chrome(
                            service=service,
                            options=chrome_options,
                        )
                except Exception as e:
                    if not hasattr(e, "msg"):
                        raise
                    auto_upgrade_chromedriver = False
                    if "This version of ChromeDriver only supports" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Chrome version must be between" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Missing or invalid capabilities" in e.msg:
                        chrome_options.add_experimental_option("w3c", True)
                        service = ChromeService(
                            log_output=os.devnull,
                            service_args=service_args,
                        )
                        with warnings.catch_warnings():
                            warnings.simplefilter(
                                "ignore", category=DeprecationWarning
                            )
                            driver = webdriver.Chrome(
                                service=service, options=chrome_options
                            )
                            return extend_driver(driver)
                    if not auto_upgrade_chromedriver:
                        raise  # Not an obvious fix.
                    else:
                        pass  # Try upgrading ChromeDriver to match Chrome.
                    mcv = None  # Major Chrome Version
                    if "Current browser version is " in e.msg:
                        line = e.msg.split("Current browser version is ")[1]
                        browser_version = line.split(" ")[0]
                        major_chrome_version = browser_version.split(".")[0]
                        if (
                            major_chrome_version.isnumeric()
                            and int(major_chrome_version) >= 86
                        ):
                            mcv = major_chrome_version
                            mcv = find_chromedriver_version_to_use(
                                mcv, driver_version
                            )
                    headless_options = _set_chrome_options(
                        browser_name,
                        downloads_path,
                        True,  # headless
                        locale_code,
                        None,  # proxy_string
                        None,  # proxy_auth
                        None,  # proxy_user
                        None,  # proxy_pass
                        None,  # proxy_bypass_list
                        None,  # proxy_pac_url
                        None,  # multi_proxy
                        None,  # user_agent
                        None,  # recorder_ext
                        disable_cookies,
                        disable_js,
                        disable_csp,
                        enable_ws,
                        enable_sync,
                        use_auto_ext,
                        False,  # undetectable
                        False,  # uc_cdp_events
                        False,  # uc_subprocess
                        False,  # log_cdp_events
                        no_sandbox,
                        disable_gpu,
                        False,  # headless1
                        False,  # headless2
                        incognito,
                        guest_mode,
                        dark_mode,
                        None,  # devtools
                        remote_debug,
                        enable_3d_apis,
                        swiftshader,
                        None,  # ad_block_on
                        None,  # host_resolver_rules
                        block_images,
                        do_not_track,
                        None,  # chromium_arg
                        None,  # user_data_dir
                        None,  # extension_zip
                        None,  # extension_dir
                        None,  # disable_features
                        binary_location,
                        driver_version,
                        page_load_strategy,
                        use_wire,
                        external_pdf,
                        servername,
                        mobile_emulator,
                        device_width,
                        device_height,
                        device_pixel_ratio,
                    )
                    args = " ".join(sys.argv)
                    if "-n" in sys.argv or " -n=" in args or args == "-c":
                        chromedriver_fixing_lock = fasteners.InterProcessLock(
                            constants.MultiBrowser.DRIVER_FIXING_LOCK
                        )
                        with chromedriver_fixing_lock:
                            if not _was_driver_repaired():
                                _repair_chromedriver(
                                    chrome_options, headless_options, mcv
                                )
                                _mark_driver_repaired()
                    else:
                        if not _was_driver_repaired():
                            _repair_chromedriver(
                                chrome_options, headless_options, mcv
                            )
                        _mark_driver_repaired()
                    if os.path.exists(LOCAL_CHROMEDRIVER):
                        service = ChromeService(
                            executable_path=LOCAL_CHROMEDRIVER,
                            log_output=os.devnull,
                            service_args=["--disable-build-check"],
                        )
                        driver = webdriver.Chrome(
                            service=service,
                            options=chrome_options,
                        )
                    else:
                        service = ChromeService(
                            log_output=os.devnull,
                            service_args=["--disable-build-check"],
                        )
                        driver = webdriver.Chrome(
                            service=service,
                            options=chrome_options,
                        )
                driver.default_get = driver.get  # Save copy of original
                if uc_activated:
                    driver.get = lambda url: uc_special_open_if_cf(
                        driver,
                        url,
                        proxy_string,
                        mobile_emulator,
                        device_width,
                        device_height,
                        device_pixel_ratio,
                    )
                    driver.uc_open = lambda url: uc_open(driver, url)
                    driver.uc_open_with_tab = (
                        lambda url: uc_open_with_tab(driver, url)
                    )
                    driver.uc_open_with_reconnect = (
                        lambda *args, **kwargs: uc_open_with_reconnect(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_open_with_disconnect = (
                        lambda *args, **kwargs: uc_open_with_disconnect(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_click = lambda *args, **kwargs: uc_click(
                        driver, *args, **kwargs
                    )
                    driver.uc_gui_press_key = (
                        lambda *args, **kwargs: uc_gui_press_key(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_press_keys = (
                        lambda *args, **kwargs: uc_gui_press_keys(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_write = (
                        lambda *args, **kwargs: uc_gui_write(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_click_x_y = (
                        lambda *args, **kwargs: uc_gui_click_x_y(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_click_captcha = (
                        lambda *args, **kwargs: uc_gui_click_captcha(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_click_cf = (
                        lambda *args, **kwargs: uc_gui_click_cf(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_click_rc = (
                        lambda *args, **kwargs: uc_gui_click_rc(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_handle_captcha = (
                        lambda *args, **kwargs: uc_gui_handle_captcha(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_handle_cf = (
                        lambda *args, **kwargs: uc_gui_handle_cf(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_gui_handle_rc = (
                        lambda *args, **kwargs: uc_gui_handle_rc(
                            driver, *args, **kwargs
                        )
                    )
                    driver.uc_switch_to_frame = (
                        lambda *args, **kwargs: uc_switch_to_frame(
                            driver, *args, **kwargs
                        )
                    )
                    driver._is_hidden = (headless or headless2)
                    driver._is_using_uc = True
                    if mobile_emulator:
                        uc_metrics = {}
                        if (
                            isinstance(device_width, int)
                            and isinstance(device_height, int)
                            and isinstance(device_pixel_ratio, (int, float))
                        ):
                            uc_metrics["width"] = device_width
                            uc_metrics["height"] = device_height
                            uc_metrics["pixelRatio"] = device_pixel_ratio
                        else:
                            uc_metrics["width"] = constants.Mobile.WIDTH
                            uc_metrics["height"] = constants.Mobile.HEIGHT
                            uc_metrics["pixelRatio"] = constants.Mobile.RATIO
                        set_device_metrics_override = dict(
                            {
                                "width": uc_metrics["width"],
                                "height": uc_metrics["height"],
                                "deviceScaleFactor": uc_metrics["pixelRatio"],
                                "mobile": True
                            }
                        )
                        with suppress(Exception):
                            driver.execute_cdp_cmd(
                                'Emulation.setDeviceMetricsOverride',
                                set_device_metrics_override
                            )
                return extend_driver(driver)
            else:  # Running headless on Linux (and not using --uc)
                try:
                    driver = webdriver.Chrome(options=chrome_options)
                    return extend_driver(driver)
                except Exception as e:
                    if not hasattr(e, "msg"):
                        raise
                    auto_upgrade_chromedriver = False
                    if "This version of ChromeDriver only supports" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Chrome version must be between" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Missing or invalid capabilities" in e.msg:
                        chrome_options.add_experimental_option("w3c", True)
                        service = ChromeService(
                            log_output=os.devnull,
                            service_args=["--disable-build-check"],
                        )
                        with warnings.catch_warnings():
                            warnings.simplefilter(
                                "ignore", category=DeprecationWarning
                            )
                            driver = webdriver.Chrome(
                                service=service, options=chrome_options
                            )
                            return extend_driver(driver)
                    mcv = None  # Major Chrome Version
                    if "Current browser version is " in e.msg:
                        line = e.msg.split("Current browser version is ")[1]
                        browser_version = line.split(" ")[0]
                        major_chrome_version = browser_version.split(".")[0]
                        if (
                            major_chrome_version.isnumeric()
                            and int(major_chrome_version) >= 86
                        ):
                            mcv = major_chrome_version
                    if auto_upgrade_chromedriver:
                        args = " ".join(sys.argv)
                        if "-n" in sys.argv or " -n=" in args or args == "-c":
                            chromedr_fixing_lock = fasteners.InterProcessLock(
                                constants.MultiBrowser.DRIVER_FIXING_LOCK
                            )
                            with chromedr_fixing_lock:
                                if not _was_driver_repaired():
                                    with suppress(Exception):
                                        _repair_chromedriver(
                                            chrome_options, chrome_options, mcv
                                        )
                                        _mark_driver_repaired()
                        else:
                            if not _was_driver_repaired():
                                with suppress(Exception):
                                    _repair_chromedriver(
                                        chrome_options, chrome_options, mcv
                                    )
                            _mark_driver_repaired()
                        with suppress(Exception):
                            service = ChromeService(
                                log_output=os.devnull,
                                service_args=["--disable-build-check"],
                            )
                            driver = webdriver.Chrome(
                                service=service,
                                options=chrome_options,
                            )
                            return extend_driver(driver)
                    # Use the virtual display on Linux during headless errors
                    logging.debug(
                        "\nWarning: Chrome failed to launch in"
                        " headless mode. Attempting to use the"
                        " SeleniumBase virtual display on Linux..."
                    )
                    if "--headless" in chrome_options.arguments:
                        chrome_options.arguments.remove("--headless")
                    if "--headless=old" in chrome_options.arguments:
                        chrome_options.arguments.remove("--headless=old")
                    service = ChromeService(
                        log_output=os.devnull,
                        service_args=["--disable-build-check"]
                    )
                    driver = webdriver.Chrome(
                        service=service, options=chrome_options
                    )
                    return extend_driver(driver)
        except Exception as original_exception:
            if is_using_uc(undetectable, browser_name):
                raise
            # Try again if Chrome didn't launch
            with suppress(Exception):
                service = ChromeService(service_args=["--disable-build-check"])
                driver = webdriver.Chrome(
                    service=service, options=chrome_options
                )
                return extend_driver(driver)
            if user_data_dir:
                print("\nUnable to set user_data_dir while starting Chrome!\n")
                raise
            elif mobile_emulator:
                print("\nFailed to start Chrome's mobile device emulator!\n")
                raise
            elif extension_zip or extension_dir:
                print("\nUnable to load extension while starting Chrome!\n")
                raise
            elif headless or headless2 or IS_LINUX or proxy_string or use_wire:
                raise
            # Try running without any options (bare bones Chrome launch)
            if LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                except Exception as e:
                    logging.debug(
                        "\nWarning: Could not make chromedriver"
                        " executable: %s" % e
                    )
            service = ChromeService(
                log_output=os.devnull,
                service_args=["--disable-build-check"]
            )
            try:
                driver = webdriver.Chrome(service=service)
                return extend_driver(driver)
            except Exception:
                raise original_exception
    else:
        raise Exception(
            "%s is not a valid browser option for this system!" % browser_name
        )
