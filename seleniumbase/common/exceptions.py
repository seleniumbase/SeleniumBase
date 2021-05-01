""" SeleniumBase Exceptions
    NoSuchFileException => Used by self.assert_downloaded_file(...)
    NotUsingChromeException => Used by Chrome-only methods if not using Chrome
    OutOfScopeException => Used by BaseCase methods when setUp() is skipped
    TimeLimitExceededException => Used by "--time-limit=SECONDS"
"""


class NoSuchFileException(Exception):
    pass


class NotUsingChromeException(Exception):
    pass


class OutOfScopeException(Exception):
    pass


class TimeLimitExceededException(Exception):
    pass
