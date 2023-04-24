""" Tests to demonstrate how to repeat the same test multiple times.
    The 1st example uses the "parameterized" library.
    The 2nd example uses "pytest.mark.parametrize()". (NO class)
    The 3rd example uses "pytest.mark.parametrize()". (in class) """
import pytest
from parameterized import parameterized
from seleniumbase import BaseCase


class RepeatTests(BaseCase):
    @parameterized.expand([[]] * 2)
    def test_repeat_this_test_with_parameterized(self):
        self.open("seleniumbase.github.io")
        self.click('a[href="help_docs/method_summary/"]')
        self.assert_text("API Reference", "h1")


@pytest.mark.parametrize("", [[]] * 2)
def test_repeat_this_test_with_pytest_parametrize(sb):
    sb.open("seleniumbase.github.io")
    sb.click('a[href="seleniumbase/console_scripts/ReadMe/"]')
    sb.assert_text("Console Scripts", "h1")


class RepeatTestsWithPytest:
    @pytest.mark.parametrize("", [[]] * 2)
    def test_repeat_test_with_pytest_parametrize(self, sb):
        sb.open("seleniumbase.github.io")
        sb.click('a[href="help_docs/customizing_test_runs/"]')
        sb.assert_text("Command Line Options", "h1")
