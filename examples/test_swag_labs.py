from seleniumbase import BaseCase


class SwagLabsTests(BaseCase):

    def login_to_swag_labs(self, username="standard_user"):
        """ Login to Swag Labs and verify success. """
        self.open("https://www.saucedemo.com/v1")
        if username not in self.get_text("#login_credentials"):
            self.fail("Invalid user for login: %s" % username)
        self.type("#user-name", username)
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')
        self.assert_element("#inventory_container")
        self.assert_text("Products", "div.product_label")

    def test_swag_labs_basic_flow(self):
        """ This test checks functional flow of the Swag Labs store. """
        self.login_to_swag_labs(username="standard_user")

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
        self.click("#shopping_cart_container path")
        self.assert_exact_text("Your Cart", "div.subheader")
        self.assert_text(item_name, "div.inventory_item_name")
        self.assert_exact_text("1", "div.cart_quantity")
        self.assert_exact_text("REMOVE", "button.cart_button")
        continue_shopping_button = "link=CONTINUE SHOPPING"
        if self.browser == "safari":
            # Safari sees this element differently
            continue_shopping_button = "link=Continue Shopping"
        self.assert_element(continue_shopping_button)

        # Checkout - Add info
        self.click("link=CHECKOUT")
        self.assert_text("Checkout: Your Information", "div.subheader")
        self.assert_element("a.cart_cancel_link")
        self.type("#first-name", "SeleniumBase")
        self.type("#last-name", "Rocks")
        self.type("#postal-code", "01720")

        # Checkout - Overview
        self.click("input.btn_primary")
        self.assert_text("Checkout: Overview", "div.subheader")
        self.assert_element("link=CANCEL")
        self.assert_text(item_name, "div.inventory_item_name")
        self.assert_text(item_price, "div.inventory_item_price")
        self.assert_exact_text("1", "div.summary_quantity")

        # Finish Checkout and verify item is no longer in cart
        self.click("link=FINISH")
        self.assert_exact_text("THANK YOU FOR YOUR ORDER", "h2")
        self.assert_element("img.pony_express")
        self.click("#shopping_cart_container path")
        self.assert_element_absent("div.inventory_item_name")
        self.click(continue_shopping_button)
        self.assert_element_absent("span.shopping_cart_badge")
