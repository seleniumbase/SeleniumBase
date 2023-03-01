"""Clean SeleniumBase Example - (Uses simple, reliable methods)"""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CleanSeleniumBase(BaseCase):
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
