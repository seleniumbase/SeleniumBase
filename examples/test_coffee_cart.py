"""Use SeleniumBase to test the Coffee Cart App."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CoffeeCartTest(BaseCase):
    def test_coffee_cart(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.click('div[data-sb="Cappuccino"]')
        self.click('div[data-sb="Flat-White"]')
        self.click('div[data-sb="Cafe-Latte"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $53.00", "button.pay")
        self.click("button.pay")
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "#app .success")
