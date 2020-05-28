"""
This module contains shared utility methods.
"""
import time
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from selenium.webdriver.remote.errorhandler import NoAlertPresentException
from selenium.webdriver.remote.errorhandler import NoSuchFrameException
from selenium.webdriver.remote.errorhandler import NoSuchWindowException
from seleniumbase import config as sb_config


def format_exc(exception, message):
    """
    Formats an exception message to make the output cleaner.
    """
    if exception == Exception:
        pass
    elif exception == ElementNotVisibleException:
        message = "ElementNotVisibleException: %s" % message
    elif exception == NoSuchElementException:
        message = "NoSuchElementException: %s" % message
    elif exception == NoAlertPresentException:
        message = "NoAlertPresentException: %s" % message
    elif exception == NoSuchFrameException:
        message = "NoSuchFrameException: %s" % message
    elif exception == NoSuchWindowException:
        message = "NoSuchWindowException: %s" % message
    elif type(exception) is str:
        message = "%s: %s" % (exception, message)
    else:
        pass
    return message


def __time_limit_exceeded(message):
    raise Exception(
        "TimeLimitExceeded: %s" % message)


def check_if_time_limit_exceeded():
    if sb_config.time_limit:
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
                "" % (display_time_limit, plural))
            __time_limit_exceeded(message)
