"""
SeleniumBase MySQL-related exceptions.

This feature is DEPRECATED!
Use self.skip() for skipping tests!

Raising one of these in a test will cause the
test-state to be logged appropriately in the DB
for tests that use the SeleniumBase MySQL option.
"""


class BlockedTest(Exception):
    """Raise this to mark a test as Blocked in the DB."""

    pass


class SkipTest(Exception):
    """Raise this to mark a test as Skipped in the DB."""

    pass


class DeprecatedTest(Exception):
    """Raise this to mark a test as Deprecated in the DB."""

    pass
