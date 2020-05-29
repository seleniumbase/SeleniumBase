""" SeleniumBase Exceptions
    NoSuchFileException => Used by self.assert_downloaded_file(...)
    TimeLimitExceededException => Used by "--time-limit=SECONDS"
"""


class NoSuchFileException(Exception):
    pass


class TimeLimitExceededException(Exception):
    pass
