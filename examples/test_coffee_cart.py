"""Use SeleniumBase to test the Coffee Cart App."""
from seleniumbase import BaseCase

if __name__ == "__main__":  # If "python" called
    from pytest import main
    from sys import argv
    main([*argv, "-s"])  # Run pytest, same args


class CoffeeCartTest(BaseCase):
    def test_coffee_cart(self):
        self.open("https://seleniumbase.io/coffee/")
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
