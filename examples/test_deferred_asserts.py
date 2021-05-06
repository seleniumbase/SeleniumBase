"""
This test demonstrates the use of deferred asserts.
Deferred asserts won't raise exceptions from failures until either
process_deferred_asserts() is called, or the test reaches the tearDown() step.
"""
import pytest
from seleniumbase import BaseCase


class DeferredAssertTests(BaseCase):
    @pytest.mark.expected_failure
    def test_deferred_asserts(self):
        self.open("https://xkcd.com/993/")
        self.wait_for_element("#comic")
        print("\n(This test should fail)")
        self.deferred_assert_element('img[alt="Brand Identity"]')
        self.deferred_assert_element('img[alt="Rocket Ship"]')  # Will Fail
        self.deferred_assert_element("#comicmap")
        self.deferred_assert_text("Fake Item", "#middleContainer")  # Will Fail
        self.deferred_assert_text("Random", "#middleContainer")
        self.deferred_assert_element('a[name="Super Fake !!!"]')  # Will Fail
        self.process_deferred_asserts()
