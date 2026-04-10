"""
Playwright Adapter Example with Tracing.
Trace logs are saved to: `latest_logs/[MODULE.CLASS.METHOD]/trace.zip`
To open Trace Viewer: `playwright show-trace [PATH_TO_LOGS]/trace.zip`
"""
import os
import sys
from playwright.sync_api import sync_playwright, expect
from unittest import TestCase


class PlaywrightAdapterWithTracing(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        headless = "linux" in sys.platform
        # Launch browser once for the whole class
        cls.browser = cls.playwright.chromium.launch(
            channel="chrome", headless=headless
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        # Create new session for every test
        self.context = self.browser.new_context()
        self.context.tracing.start(
            snapshots=True, screenshots=True, sources=True
        )
        self.page = self.context.new_page()

    def tearDown(self):
        # Close the session (browser runs until tearDownClass)
        log_folder = "latest_logs"
        test_id = "%s.%s.%s" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._testMethodName,
        )
        trace_path = os.path.join(log_folder, test_id, "trace.zip")
        self.context.tracing.stop(path=trace_path)
        self.page.close()
        self.context.close()

    def open(self, url):
        self.page.goto(url)

    def click(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        self.page.click(selector, timeout=timeout)

    def type(self, selector, text, timeout=10):
        timeout = float(timeout) * 1000.0
        if text.endswith("\n"):
            self.page.fill(selector, text[:-1], timeout=timeout)
            self.page.press(selector, "Enter")
        else:
            self.page.fill(selector, text, timeout=timeout)

    def assert_element(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        # expect() has built-in retry logic
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def assert_text(self, text, selector="html", timeout=7):
        timeout = float(timeout) * 1000.0
        # to_contain_text is the equivalent of "assertIn"
        expect(self.page.locator(selector)).to_contain_text(
            text, timeout=timeout
        )

    def assert_exact_text(self, text, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_have_text(text, timeout=timeout)

    def assert_element_not_visible(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

    def test_add_item_to_cart(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_text("Products", "span.title")

        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("Your Cart", "span.title")
        self.assert_text("Backpack", "div.cart_item")

        self.click("#remove-sauce-labs-backpack")
        self.assert_element_not_visible("div.cart_item")

        self.click("#react-burger-menu-btn")
        self.click("a#logout_sidebar_link")
        self.assert_element("input#login-button")


if __name__ == "__main__":
    from pytest import main
    main([__file__, "-s"])
