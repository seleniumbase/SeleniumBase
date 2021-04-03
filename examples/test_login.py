from seleniumbase import BaseCase


class SwagLabsLoginTests(BaseCase):

    def login_to_swag_labs(self):
        """ Login to Swag Labs and verify that login was successful. """
        self.open("https://www.saucedemo.com/v1")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')

    def test_swag_labs_login(self):
        """ This test checks standard login for the Swag Labs store. """
        self.login_to_swag_labs()
        self.assert_element("div.header_label div.app_logo")
        self.assert_text("Products", "div.product_label")
