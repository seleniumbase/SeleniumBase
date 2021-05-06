from parameterized import parameterized
from seleniumbase import BaseCase


class SwagLabsTests(BaseCase):
    def login_to_swag_labs(self, username="standard_user"):
        """ Login to Swag Labs and verify success. """
        url = "https://www.saucedemo.com"
        self.open(url)
        if username not in self.get_text("#login_credentials"):
            self.fail("Invalid user for login: %s" % username)
        self.type("#user-name", username)
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')
        self.assert_element("#inventory_container")
        self.assert_element('div:contains("Sauce Labs Backpack")')

    @parameterized.expand(
        [
            ["standard_user"],
            ["problem_user"],
        ]
    )
    def test_swag_labs_basic_flow(self, username):
        """This test checks functional flow of the Swag Labs store.
        This test is parameterized on the login user."""
        self.login_to_swag_labs(username=username)
        if username == "problem_user":
            print("\n(This test should fail)")

        # Verify that the "Test.allTheThings() T-Shirt" appears on the page
        item_name = "Test.allTheThings() T-Shirt"
        self.assert_text(item_name)

        # Verify that a reverse-alphabetical sort works as expected
        self.select_option_by_value("select.product_sort_container", "za")
        if item_name not in self.get_text("div.inventory_item"):
            self.fail('Sort Failed! Expecting "%s" on top!' % item_name)

        # Add the "Test.allTheThings() T-Shirt" to the cart
        self.assert_exact_text("ADD TO CART", "button.btn_inventory")
        item_price = self.get_text("div.inventory_item_price")
        self.click("button.btn_inventory")
        self.assert_exact_text("REMOVE", "button.btn_inventory")
        self.assert_exact_text("1", "span.shopping_cart_badge")

        # Verify your cart
        self.click("#shopping_cart_container")
        self.assert_element('span:contains("Your Cart")')
        self.assert_text(item_name, "div.inventory_item_name")
        self.assert_exact_text("1", "div.cart_quantity")
        self.assert_exact_text("REMOVE", "button.cart_button")
        self.assert_element("button#continue-shopping")

        # Checkout - Add info
        self.click("button#checkout")
        self.assert_element('span:contains("Checkout: Your Information")')
        self.assert_element("button#cancel")
        self.type("#first-name", "SeleniumBase")
        self.type("#last-name", "Rocks")
        self.type("#postal-code", "01720")

        # Checkout - Overview
        self.click("input#continue")
        self.assert_element('span:contains("Checkout: Overview")')
        self.assert_element("button#cancel")
        self.assert_text(item_name, "div.inventory_item_name")
        self.assert_text(item_price, "div.inventory_item_price")
        self.assert_exact_text("1", "div.cart_quantity")

        # Finish Checkout and verify that the cart is now empty
        self.click("button#finish")
        self.assert_exact_text("THANK YOU FOR YOUR ORDER", "h2")
        self.assert_element("img.pony_express")
        self.click("#shopping_cart_container")
        self.assert_element_absent("div.inventory_item_name")
        self.click("button#continue-shopping")
        self.assert_element_absent("span.shopping_cart_badge")

    def tearDown(self):
        self.save_teardown_screenshot()
        # Reset App State and Logout if the controls are present
        try:
            if self.is_element_present("a#reset_sidebar_link"):
                self.js_click("a#reset_sidebar_link")
            if self.is_element_present("a#logout_sidebar_link"):
                self.js_click("a#logout_sidebar_link")
        except Exception:
            pass
        super(SwagLabsTests, self).tearDown()
