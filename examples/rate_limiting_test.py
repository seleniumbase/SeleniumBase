"""
This test demonstrates the use of the "rate_limited" decorator.
You can use this decorator on any method to rate-limit it.
"""

import unittest
from seleniumbase import decorators


class MyTestClass(unittest.TestCase):

    @decorators.rate_limited(3.5)  # The arg is max calls per second
    def print_item(self, item):
        print(item)

    def test_rate_limited_printing(self):
        print("\nRunning rate-limited print test:")
        for item in range(1, 11):
            self.print_item(item)
