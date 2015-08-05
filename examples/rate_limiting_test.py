from seleniumbase import BaseCase
from seleniumbase.common import decorators


class MyTestClass(BaseCase):

    @decorators.rate_limited(4)
    def print_item(self, item):
        print item

    def test_rate_limited_printing(self):
        for item in xrange(10):
            self.print_item(item)
