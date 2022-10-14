"""
This module contains shared utility methods.
"""
import subprocess
import sys
from seleniumbase.fixtures import constants
from seleniumbase import config as sb_config


def pip_install(package, version=None):
    import fasteners

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


def is_windows():
    platform = sys.platform
    if "win32" in platform or "win64" in platform or "x64" in platform:
        return True
    else:
        return False


def get_terminal_width():
    import os

    width = 80  # default
    try:
        width = os.get_terminal_size().columns
    except Exception:
        try:
            if is_windows():
                raise Exception("Don't even try 'tput cols' on Windows!")
            width = int(subprocess.check_output(["tput", "cols"]))
        except Exception:
            try:
                import shutil

                width = shutil.get_terminal_size((80, 20)).columns
            except Exception:
                pass
    return width


def format_exc(exception, message):
    """
    Formats an exception message to make the output cleaner.
    """
    from selenium.common.exceptions import ElementNotVisibleException
    from selenium.common.exceptions import NoAlertPresentException
    from selenium.common.exceptions import NoSuchAttributeException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import NoSuchFrameException
    from selenium.common.exceptions import NoSuchWindowException
    from seleniumbase.common.exceptions import NoSuchFileException
    from seleniumbase.common.exceptions import TextNotVisibleException

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
        import time

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
