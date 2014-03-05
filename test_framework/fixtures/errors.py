"""
This module contains test state related exceptions. 
Raising one of these in a test will cause the state of the test to
be logged appropriately.
"""

#this makes DeprecatedTest and SkipTest available, but nose currently
#(for 3 years) has a bug that won't let us handle them properly so 
#we define our own

class BlockedTest(Exception):
    """Raise this to mark a test as Blocked"""
    pass


class SkipTest(Exception):
    """Raise this to mark a test as Skipped."""
    pass


class DeprecatedTest(Exception):
    """Raise this to mark a test as Deprecated."""
    pass
