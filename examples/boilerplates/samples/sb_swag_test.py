""" Classic Page Object Model with the "sb" fixture """


class LoginPage:
    def login_to_swag_labs(self, sb, username):
        sb.open("https://www.saucedemo.com")
        sb.type("#user-name", username)
        sb.type("#password", "secret_sauce")
        sb.click('input[type="submit"]')


class MyTests:
    def test_swag_labs_login(self, sb):
        LoginPage().login_to_swag_labs(sb, "standard_user")
        sb.assert_element("#inventory_container")
        sb.assert_element('div:contains("Sauce Labs Backpack")')
