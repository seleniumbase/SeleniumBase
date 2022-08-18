from seleniumbase import BaseCase


class SwagLabsLoginTests(BaseCase):
    def login_to_swag_labs(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce")
        self.click('input[type="submit"]')

    def test_swag_labs_login(self):
        self.login_to_swag_labs()
        self.assert_element("div.inventory_list")
        self.assert_element('.inventory_item:contains("Sauce Labs Backpack")')
        self.js_click("a#logout_sidebar_link")
        self.assert_element("div#login_button_container")
