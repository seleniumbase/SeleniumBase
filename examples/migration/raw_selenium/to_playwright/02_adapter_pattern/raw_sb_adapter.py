"""SeleniumBase Adapter Example."""
from seleniumbase import SB
from unittest import TestCase


class SeleniumBaseAdapter(TestCase):
    def setUp(self):
        self.sb_context = SB()
        self.sb = self.sb_context.__enter__()

    def tearDown(self):
        self.sb_context.__exit__(None, None, None)

    def open(self, url):
        self.sb.open(url)

    def click(self, selector, by="css selector", timeout=7):
        self.sb.click(selector=selector, by=by, timeout=timeout)

    def type(self, selector, text, by="css selector", timeout=10):
        self.sb.type(selector, text=text, by=by, timeout=timeout)

    def assert_element(self, selector, by="css selector", timeout=7):
        self.sb.assert_element(selector, by=by, timeout=timeout)

    def assert_text(self, text, selector="html", by="css selector", timeout=7):
        self.sb.assert_text(text, selector=selector, by=by, timeout=timeout)

    def assert_exact_text(self, text, selector, by="css selector", timeout=7):
        self.sb.assert_exact_text(
            text, selector=selector, by=by, timeout=timeout
        )

    def assert_element_not_visible(
        self, selector, by="css selector", timeout=7
    ):
        self.sb.assert_element_not_visible(selector, by=by, timeout=timeout)

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
