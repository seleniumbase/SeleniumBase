"""This test shows the use of SeleniumBase deferred asserts.
Deferred asserts won't raise exceptions from failures until
process_deferred_asserts() is called, or the test completes."""
import pytest
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class DeferredAssertTests(BaseCase):
    @pytest.mark.expected_failure
    def test_deferred_asserts(self):
        self.open("https://xkcd.com/993/")
        self.wait_for_element("#comic")
        print("\n(This test should fail)")
        self.deferred_assert_element('img[alt="Brand Identity"]')
        self.deferred_assert_element('img[alt="Rocket Ship"]')  # Will Fail
        self.deferred_assert_element("#comicmap")
        self.deferred_assert_text("Fake Item", "ul.comicNav")  # Will Fail
        self.deferred_assert_text("Random", "ul.comicNav")
        self.deferred_assert_element('a[name="Super Fake !!!"]')  # Will Fail
        self.deferred_assert_exact_text("Brand Identity", "#ctitle")
        self.deferred_assert_exact_text("Fake Food", "#comic")  # Will Fail
        self.process_deferred_asserts()
