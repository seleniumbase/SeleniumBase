"""
This module contains shared utility methods.
"""
import fasteners
import subprocess
import sys
import time
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from seleniumbase.common.exceptions import TextNotVisibleException
from seleniumbase.fixtures import constants
from seleniumbase import config as sb_config


def pip_install(package, version=None):
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


def format_exc(exception, message):
    """
    Formats an exception message to make the output cleaner.
    """
    from seleniumbase.common.exceptions import NoSuchFileException

    if exception == Exception:
        exc = Exception
        return exc, message
    elif exception == ElementNotVisibleException:
        exc = ElementNotVisibleException
    elif exception == "ElementNotVisibleException":
        exc = ElementNotVisibleException
    elif exception == NoSuchElementException:
        exc = NoSuchElementException
    elif exception == "NoSuchElementException":
        exc = NoSuchElementException
    elif exception == TextNotVisibleException:
        exc = TextNotVisibleException
    elif exception == "TextNotVisibleException":
        exc = TextNotVisibleException
    elif exception == NoAlertPresentException:
        exc = NoAlertPresentException
    elif exception == "NoAlertPresentException":
        exc = NoAlertPresentException
    elif exception == NoSuchAttributeException:
        exc = NoSuchAttributeException
    elif exception == "NoSuchAttributeException":
        exc = NoSuchAttributeException
    elif exception == NoSuchFrameException:
        exc = NoSuchFrameException
    elif exception == "NoSuchFrameException":
        exc = NoSuchFrameException
    elif exception == NoSuchWindowException:
        exc = NoSuchWindowException
    elif exception == "NoSuchWindowException":
        exc = NoSuchWindowException
    elif exception == NoSuchFileException:
        exc = NoSuchFileException
    elif exception == "NoSuchFileException":
        exc = NoSuchFileException
    elif type(exception) is str:
        exc = Exception
        message = "%s: %s" % (exception, message)
        return exc, message
    else:
        exc = Exception
        return exc, message
    message = _format_message(message)
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
