"""
Playwright TestCase Example with Tracing.
Trace logs are saved to: `latest_logs/[TESTPATH]/trace.zip`
To open Trace Viewer: `playwright show-trace TRACEPATH.zip`
"""
import os
import sys
from playwright.sync_api import sync_playwright, expect
from unittest import TestCase


class PlaywrightTestCaseWithTracing(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        headless = "linux" in sys.platform or "--headless" in sys.argv
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

    def test_add_item_to_cart(self):
        page = self.page

        page.goto("https://www.saucedemo.com")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.press("#password", "Enter")
        expect(page.locator("div.inventory_list")).to_be_visible()
        expect(page.locator("span.title")).to_contain_text("Products")

        page.click('button[name*="backpack"]')
        page.click("#shopping_cart_container a")
        expect(page.locator("span.title")).to_have_text("Your Cart")
        expect(page.locator("div.cart_item")).to_contain_text("Backpack")

        page.click("#remove-sauce-labs-backpack")
        expect(page.locator("div.cart_item")).to_be_hidden()

        page.click("#react-burger-menu-btn")
        page.click("a#logout_sidebar_link")
        expect(page.locator("input#login-button")).to_be_visible()


if __name__ == "__main__":
    from pytest import main
    main([__file__, "-s"])
