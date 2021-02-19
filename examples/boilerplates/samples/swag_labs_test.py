from seleniumbase import BaseCase


class LoginPage():

    def login_to_swag_labs(self, sb, username):
        sb.type("#user-name", username)
        sb.type("#password", "secret_sauce")
        sb.click('input[type="submit"]')


class MyTests(BaseCase):

    def test_swag_labs_login(self):
        self.open("https://www.saucedemo.com/")
        LoginPage().login_to_swag_labs(self, "standard_user")
        self.assert_element("#inventory_container")
        self.assert_text("Products", "div.product_label")
