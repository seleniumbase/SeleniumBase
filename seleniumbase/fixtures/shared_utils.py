"""Shared utility methods"""
import colorama
import os
import platform
import sys
import time
from contextlib import suppress
from seleniumbase import config as sb_config
from seleniumbase.fixtures import constants


def pip_install(package, version=None):
    import fasteners
    import subprocess

    pip_install_lock = fasteners.InterProcessLock(
        constants.PipInstall.LOCKFILE
    )
    with pip_install_lock:
        if not version:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package]
            )
        else:
            package_and_version = package + "==" + str(version)
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_and_version]
            )


def is_arm_mac():
    """(M1 / M2 Macs use the ARM processor)"""
    return (
        "darwin" in sys.platform
        and (
            "arm" in platform.processor().lower()
            or "arm64" in platform.version().lower()
        )
    )


def is_mac():
    return "darwin" in sys.platform


def is_linux():
    return "linux" in sys.platform


def is_windows():
    return "win32" in sys.platform


def is_safari(driver):
    return driver.capabilities["browserName"].lower() == "safari"


def get_terminal_width():
    width = 80  # default
    try:
        width = os.get_terminal_size().columns
    except Exception:
        try:
            import shutil

            width = shutil.get_terminal_size((80, 20)).columns
        except Exception:
            pass
    return width


def fix_colorama_if_windows():
    if is_windows():
        colorama.just_fix_windows_console()


def fix_url_as_needed(url):
    if not url:
        url = "data:,"
    elif url.startswith("//"):
        url = "https:" + url
    elif ":" not in url:
        url = "https://" + url
    return url


def reconnect_if_disconnected(driver):
    if (
        hasattr(driver, "_is_using_uc")
        and driver._is_using_uc
        and hasattr(driver, "is_connected")
        and not driver.is_connected()
    ):
        with suppress(Exception):
            driver.connect()


def is_cdp_swap_needed(driver):
    """
    When someone is using CDP Mode with a disconnected webdriver,
    but they forget to reconnect before calling a webdriver method,
    this method is used to substitute the webdriver method for a
    CDP Mode method instead, which keeps CDP Stealth Mode enabled.
    For other webdriver methods, SeleniumBase will reconnect first.
    """
    return (
        hasattr(driver, "is_cdp_mode_active")
        and driver.is_cdp_mode_active()
        and hasattr(driver, "is_connected")
        and not driver.is_connected()
    )


def is_chrome_130_or_newer(self, binary_location=None):
    from seleniumbase.core import detect_b_ver

    """Due to changes in Chrome-130, UC Mode freezes at start-up
    unless the user-data-dir already exists and is populated."""
    with suppress(Exception):
        if not binary_location:
            ver = detect_b_ver.get_browser_version_from_os("google-chrome")
        else:
            ver = detect_b_ver.get_browser_version_from_binary(
                binary_location
            )
        if ver and len(ver) > 3 and int(ver.split(".")[0]) >= 130:
            return True
    return False


def format_exc(exception, message):
    """Formats an exception message to make the output cleaner."""
    from selenium.common.exceptions import ElementNotVisibleException
    from selenium.common.exceptions import NoAlertPresentException
    from selenium.common.exceptions import NoSuchAttributeException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import NoSuchFrameException
    from selenium.common.exceptions import NoSuchWindowException
    from seleniumbase.common.exceptions import LinkTextNotFoundException
    from seleniumbase.common.exceptions import NoSuchFileException
    from seleniumbase.common.exceptions import NoSuchOptionException
    from seleniumbase.common.exceptions import TextNotVisibleException
    from seleniumbase.common import exceptions

    if exception is Exception:
        exc = Exception
        return exc, message
    elif exception is ElementNotVisibleException:
        exc = exceptions.ElementNotVisibleException
    elif exception == "ElementNotVisibleException":
        exc = exceptions.ElementNotVisibleException
    elif exception is LinkTextNotFoundException:
        exc = exceptions.LinkTextNotFoundException
    elif exception == "LinkTextNotFoundException":
        exc = exceptions.LinkTextNotFoundException
    elif exception is NoSuchElementException:
        exc = exceptions.NoSuchElementException
    elif exception == "NoSuchElementException":
        exc = exceptions.NoSuchElementException
    elif exception is TextNotVisibleException:
        exc = exceptions.TextNotVisibleException
    elif exception == "TextNotVisibleException":
        exc = exceptions.TextNotVisibleException
    elif exception is NoAlertPresentException:
        exc = exceptions.NoAlertPresentException
    elif exception == "NoAlertPresentException":
        exc = exceptions.NoAlertPresentException
    elif exception is NoSuchAttributeException:
        exc = exceptions.NoSuchAttributeException
    elif exception == "NoSuchAttributeException":
        exc = exceptions.NoSuchAttributeException
    elif exception is NoSuchFrameException:
        exc = exceptions.NoSuchFrameException
    elif exception == "NoSuchFrameException":
        exc = exceptions.NoSuchFrameException
    elif exception is NoSuchWindowException:
        exc = exceptions.NoSuchWindowException
    elif exception == "NoSuchWindowException":
        exc = exceptions.NoSuchWindowException
    elif exception is NoSuchFileException:
        exc = exceptions.NoSuchFileException
    elif exception == "NoSuchFileException":
        exc = exceptions.NoSuchFileException
    elif exception is NoSuchOptionException:
        exc = exceptions.NoSuchOptionException
    elif exception == "NoSuchOptionException":
        exc = exceptions.NoSuchOptionException
    elif isinstance(exception, str):
        exc = Exception
        message = "%s: %s" % (exception, message)
        return exc, message
    else:
        exc = Exception
        return exc, message
    message = _format_message(message)
    try:
        exc.message = message
    except Exception:
        pass
    return exc, message


def _format_message(message):
    message = "\n " + message
    return message


def __time_limit_exceeded(message):
    from seleniumbase.common.exceptions import TimeLimitExceededException

    raise TimeLimitExceededException(message)


def check_if_time_limit_exceeded():
    if (
        hasattr(sb_config, "time_limit")
        and sb_config.time_limit
        and not sb_config.recorder_mode
    ):
        time_limit = sb_config.time_limit
        now_ms = int(time.time() * 1000)
        if now_ms > sb_config.start_time_ms + sb_config.time_limit_ms:
            display_time_limit = time_limit
            plural = "s"
            if float(int(time_limit)) == float(time_limit):
                display_time_limit = int(time_limit)
                if display_time_limit == 1:
                    plural = ""
            message = (
                "This test has exceeded the time limit of %s second%s!"
                % (display_time_limit, plural)
            )
            message = _format_message(message)
            __time_limit_exceeded(message)
