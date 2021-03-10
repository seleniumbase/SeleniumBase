"""
This test demonstrates the use of the "rate_limited" decorator.
You can use this decorator on any method to rate-limit it.
"""

from seleniumbase import BaseCase
from seleniumbase import decorators


class RateLimitingTests(BaseCase):

    @decorators.rate_limited(4.2)  # The arg is max calls per second
    def print_item(self, item):
        print(item)

    def test_rate_limited_printing(self):
        message = "Running rate-limited print() on the command line"
        self.open("data:text/html,<p>%s</p>" % message)
        print("\n%s:" % message)
        for item in range(1, 11):
            self.print_item(item)
