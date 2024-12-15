from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    def test_swag_labs(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_text("Backpack", "div.cart_item")
        self.click("button#checkout")
        self.type("input#first-name", "SeleniumBase")
        self.type("input#last-name", "Automation")
        self.type("input#postal-code", "77123")
        self.click("input#continue")
        self.click("button#finish")
        self.assert_text("Thank you for your order!")
