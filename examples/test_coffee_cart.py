from seleniumbase import BaseCase


class CoffeeCartTest(BaseCase):
    def test_coffee_cart(self):
        self.open("https://coffee-cart.netlify.app/")
        self.click('div[data-test="Cappucino"]')
        self.click('div[data-test="Cafe_Latte"]')
        self.click('div[data-test="Cafe_Breve"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $50.00", 'button[data-test="checkout"]')
        self.click('button[data-test="checkout"]')
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "div#app div")
