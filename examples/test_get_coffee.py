"""Use SeleniumBase to get coffee"""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class GetCoffeeTest(BaseCase):
    def test_get_coffee(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.assert_exact_text("cart (0)", 'a[aria-label="Cart page"]')
        self.assert_element('div[data-sb="Mocha"]')
        self.click('div[data-sb="Mocha"]')
        self.assert_link_text("cart (1)")
        self.click_link_text("cart (1)")
        self.assert_exact_text("Total: $8.00", "button.pay")
        self.click("button.pay")
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks", "#app div.success")
