from seleniumbase import BaseCase
from seleniumbase.common import decorators


class MyTestClass(BaseCase):

    @decorators.rate_limited(3.5)  # The arg is max calls per second
    def print_item(self, item):
        print item

    def test_rate_limited_printing(self):
        print "\nRunning rate-limited print test:"
        for item in xrange(1, 11):
            self.print_item(item)
