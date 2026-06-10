"""A SeleniumBase test for verifying the Login Page on Swag Labs"""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class SwagLabsLoginTests(BaseCase):
    def test_swag_labs_login(self):
        self.goto("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')
        self.assert_element("div.inventory_list")
        self.assert_element('div.inventory_item:contains("Bike")')
        self.js_click("a#logout_sidebar_link")
        self.assert_element("div#login_button_container")
