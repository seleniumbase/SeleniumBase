''' NOTE: This test suite contains 2 passing tests and 2 failing tests. '''

from seleniumbase import BaseCase


class MyTestSuite(BaseCase):

    def test_1(self):
        self.open("http://xkcd.com/1663/")
        self.find_text("Garden", "div#ctitle", timeout=3)
        for p in range(4):
            self.click('a[rel="next"]')
        self.find_text("Algorithms", "div#ctitle", timeout=3)

    def test_2(self):
        # This test should FAIL
        print("\n(This test fails on purpose)")
        self.open("http://xkcd.com/1675/")
        raise Exception("FAKE EXCEPTION: This test fails on purpose.")

    def test_3(self):
        self.open("http://xkcd.com/1406/")
        self.find_text("Universal Converter Box", "div#ctitle", timeout=3)
        self.open("http://xkcd.com/608/")
        self.find_text("Form", "div#ctitle", timeout=3)

    def test_4(self):
        # This test should FAIL
        print("\n(This test fails on purpose)")
        self.open("http://xkcd.com/1670/")
        self.find_element("FakeElement.DoesNotExist", timeout=0.5)
