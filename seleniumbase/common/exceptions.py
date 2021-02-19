""" SeleniumBase Exceptions
    NoSuchFileException => Used by self.assert_downloaded_file(...)
    OutOfScopeException => Used by BaseCase methods when setUp() is skipped
    TimeLimitExceededException => Used by "--time-limit=SECONDS"
"""


class NoSuchFileException(Exception):
    pass


class OutOfScopeException(Exception):
    pass


class TimeLimitExceededException(Exception):
    pass
