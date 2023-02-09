""" SeleniumBase Exceptions
    NoSuchFileException => Called when self.assert_downloaded_file(...) fails.
    NotUsingChromeException => Used by Chrome-only methods if not using Chrome.
    NotUsingChromiumException => Used by Chromium-only methods if not Chromium.
    OutOfScopeException => Used by BaseCase methods when setUp() is skipped.
    TextNotVisibleException => Called when expected text fails to appear.
    TimeLimitExceededException => Called when exceeding "--time-limit=SECONDS".
    VisualException => Called when there's a Visual Diff Assertion Failure.
"""


class NoSuchFileException(Exception):
    pass


class NotUsingChromeException(Exception):
    pass


class NotUsingChromiumException(Exception):
    pass


class OutOfScopeException(Exception):
    pass


class TextNotVisibleException(Exception):
    pass


class TimeLimitExceededException(Exception):
    pass


class VisualException(Exception):
    pass
