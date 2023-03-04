"""This test suite contains 2 passing tests and 2 failing tests."""
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTestSuite(BaseCase):
    def test_1(self):
        self.open("https://xkcd.com/1722/")
        self.assert_text("Debugging", "div#ctitle", timeout=4)
        for p in range(3):
            self.click('a[rel="next"]')
        self.assert_text("Linear Regression", "div#ctitle", timeout=4)

    @pytest.mark.expected_failure
    def test_2(self):
        print("\n(This test should fail)")
        self.open("https://xkcd.com/1373/")
        self.assert_text("FakeText", "div#ctitle", timeout=0.4)

    def test_3(self):
        self.open("https://xkcd.com/2224/")
        self.assert_text("Software Updates", "div#ctitle", timeout=4)
        self.open("https://xkcd.com/608/")
        self.assert_exact_text("Form", "div#ctitle", timeout=4)

    @pytest.mark.expected_failure
    def test_4(self):
        print("\n(This test should fail)")
        self.open("https://xkcd.com/2224/")
        self.assert_element("FakeElement.DoesNotExist", timeout=0.4)
