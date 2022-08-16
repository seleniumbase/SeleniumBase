"""
Add an item to a shopping cart; verify; remove item; verify.
"""
from seleniumbase import BaseCase


class MyTestClass(BaseCase):
    def test_basics(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_exact_text("PRODUCTS", "span.title")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("YOUR CART", "span.title")
        self.assert_text("Backpack", "div.cart_item")
        self.click('button:contains("Remove")')  # HTML innerText
        self.assert_text_not_visible("Backpack", "div.cart_item")
        self.js_click("a#logout_sidebar_link")
        self.assert_element("div#login_button_container")
