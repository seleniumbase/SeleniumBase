"""Use SeleniumBase to test the Coffee Cart App."""
from parameterized import parameterized
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CoffeeCartTests(BaseCase):
    def test_1_verify_nav_link_to_coffee_cart(self):
        self.open("https://seleniumbase.io/help_docs/customizing_test_runs/")
        self.js_click('nav a:contains("Coffee Cart")')
        self.assert_title("Coffee Cart")
        self.assert_element('h4:contains("Espresso")')

    def test_buy_one_cappuccino(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.click('div[data-test="Cappuccino"]')
        self.assert_exact_text("cart (1)", 'a[aria-label="Cart page"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $19.00", 'button[data-test="checkout"]')
        self.click('button[data-test="checkout"]')
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "div#app div.success")
        self.assert_exact_text("cart (0)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $0.00", 'button[data-test="checkout"]')

    @parameterized.expand([[False], [True]])
    def test_coffee_promo_with_preview(self, accept_promo):
        self.open("https://seleniumbase.io/coffee/")
        self.click('div[data-test="Espresso"]')
        self.click('div[data-test="Americano"]')
        self.click('div[data-test="Cafe_Latte"]')
        self.assert_exact_text("cart (3)", 'a[aria-label="Cart page"]')
        promo = False
        total_string = "Total: $33.00"
        if self.is_element_visible("div.promo"):
            self.assert_text("Get an extra cup of Mocha for $4.", "div.promo")
            if accept_promo:
                self.click("div.promo button.yes")
                self.assert_exact_text("cart (4)", 'a[aria-label="Cart page"]')
                promo = True
                total_string = "Total: $37.00"
            else:
                self.click("div.promo button.no")
        checkout_button = 'button[data-test="checkout"]'
        if promo:
            self.hover(checkout_button)
            if not self.is_element_visible("ul.cart-preview"):
                self.highlight(checkout_button)
                self.post_message("STOP moving the mouse!<br />Hover blocked!")
                self.hover(checkout_button)
            self.assert_text("(Discounted) Mocha", "ul.cart-preview")
        self.assert_exact_text(total_string, checkout_button)
        self.click(checkout_button)
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "div#app div.success")

    def test_context_click_add_coffee(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.context_click('div[data-test="Espresso_Macchiato"]')
        self.click('form button:contains("Yes")')
        self.assert_exact_text("cart (1)", 'a[aria-label="Cart page"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $12.00", 'button[data-test="checkout"]')
        self.click('button[data-test="checkout"]')
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "div#app div.success")

    def test_remove_added_coffee(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.assert_exact_text("cart (0)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $0.00", "button.pay")
        self.wait_for_element('div[class="cup-body"]')
        self.click_visible_elements('div[class="cup-body"]', limit=6)
        self.assert_exact_text("cart (6)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $74.00", 'button[data-test="checkout"]')
        self.click('a[aria-label="Cart page"]')
        self.click_visible_elements("button.delete")
        self.assert_text("No coffee, go add some.", "div#app")
        self.click('a[aria-label="Menu page"]')
        self.assert_exact_text("cart (0)", 'a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $0.00", 'button[data-test="checkout"]')
