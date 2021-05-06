""" Classic Page Object Model with BaseCase inheritance """

from seleniumbase import BaseCase


class LoginPage:
    def login_to_swag_labs(self, sb, username):
        sb.open("https://www.saucedemo.com")
        sb.type("#user-name", username)
        sb.type("#password", "secret_sauce")
        sb.click('input[type="submit"]')


class MyTests(BaseCase):
    def test_swag_labs_login(self):
        LoginPage().login_to_swag_labs(self, "standard_user")
        self.assert_element("#inventory_container")
        self.assert_element('div:contains("Sauce Labs Backpack")')
