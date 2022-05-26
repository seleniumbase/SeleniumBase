""" SeleniumBase Exceptions
    NoSuchFileException => Called when self.assert_downloaded_file(...) fails.
    NotUsingChromeException => Used by Chrome-only methods if not using Chrome.
    OutOfScopeException => Used by BaseCase methods when setUp() is skipped.
    TextNotVisibleException => Called when expected text fails to appear.
    TimeLimitExceededException => Called when exceeding "--time-limit=SECONDS".
"""
from selenium.common.exceptions import WebDriverException


class NoSuchFileException(Exception):
    pass


class NotUsingChromeException(WebDriverException):
    pass


class OutOfScopeException(Exception):
    pass


class TextNotVisibleException(WebDriverException):
    pass


class TimeLimitExceededException(Exception):
    pass
