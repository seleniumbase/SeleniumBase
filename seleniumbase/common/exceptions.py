""" SeleniumBase Exceptions
    LinkTextNotFoundException => Called when expected link text is not visible.
    NoSuchFileException => Called when self.assert_downloaded_file(...) fails.
    NoSuchOptionException => Called when select_option_by_*() lacks the option.
    NotConnectedException => Called when Internet is not reachable when needed.
    NotUsingChromeException => Used by Chrome-only methods if not using Chrome.
    NotUsingChromiumException => Used by Chromium-only methods if not Chromium.
    OutOfScopeException => Used by BaseCase methods when setUp() is skipped.
    ProxyConnectionException => Called when the proxy connection failed.
    TextNotVisibleException => Called when the expected text is not visible.
    TimeLimitExceededException => Called when exceeding "--time-limit=SECONDS".
    TimeoutException => Called when some timeout limit has been exceeded.
    VisualException => Called when there's a Visual Diff Assertion Failure.
"""


class LinkTextNotFoundException(Exception):
    pass


class NoSuchFileException(Exception):
    pass


class NoSuchOptionException(Exception):
    pass


class NotConnectedException(Exception):
    pass


class NotUsingChromeException(Exception):
    pass


class NotUsingChromiumException(Exception):
    pass


class OutOfScopeException(Exception):
    pass


class ProxyConnectionException(Exception):
    pass


class TextNotVisibleException(Exception):
    pass


class TimeLimitExceededException(Exception):
    pass


class TimeoutException(Exception):
    pass


class VisualException(Exception):
    pass


""" Selenium Exceptions (Simplified for SeleniumBase) """


class WebDriverException(Exception):
    """Base webdriver exception."""

    def __init__(self, msg=None, screen=None, stacktrace=None):
        super().__init__()
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.screen:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class InvalidSwitchToTargetException(WebDriverException):
    """Thrown when frame or window target to be switched doesn't exist."""


class NoSuchFrameException(InvalidSwitchToTargetException):
    """Thrown when frame target to be switched doesn't exist."""


class NoSuchWindowException(InvalidSwitchToTargetException):
    """Thrown when window target to be switched doesn't exist."""


class NoSuchElementException(WebDriverException):
    """Thrown when element could not be found."""


class NoSuchAttributeException(WebDriverException):
    """Thrown when the attribute of element could not be found."""


class InvalidElementStateException(WebDriverException):
    """Thrown when a command could not be completed because the element is in
    an invalid state."""


class NoAlertPresentException(WebDriverException):
    """Thrown when switching to no presented alert."""


class ElementNotVisibleException(InvalidElementStateException):
    """Thrown when an element is present in the DOM, but not visible."""
