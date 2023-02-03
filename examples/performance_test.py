"""Performance test example.

Uses decorators.print_runtime(), which prints the runtime duration
of a method or "with"-block after the method (or block) completes.
Also raises an exception when exceeding the time "limit" if set.

Arguments ->
    description  # Optional - Shows description in print output.
    limit  # Optional - Fail if the duration is above the limit.

Method / Function example usage ->
    from seleniumbase import decorators

    @decorators.print_runtime("My Method")
    def my_method():
        # code ...
        # code ...

"with"-block example usage ->
    from seleniumbase import decorators

    with decorators.print_runtime("My Code Block"):
        # code ...
        # code ... """
from seleniumbase import BaseCase
from seleniumbase import decorators
BaseCase.main(__name__, __file__)


class PerformanceClass(BaseCase):
    @decorators.print_runtime("Open Swag Labs and Log In")
    def login_to_swag_labs(self):
        with decorators.print_runtime("Open Swag Labs"):
            self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")

    def test_performance_of_swag_labs(self):
        self.login_to_swag_labs()
        self.assert_element("div.inventory_list")
        self.assert_exact_text("PRODUCTS", "span.title")
        with decorators.print_runtime("Add backpack and see cart"):
            self.click('button[name*="backpack"]')
            self.click("#shopping_cart_container a")
            self.assert_text("Backpack", "div.cart_item")
        with decorators.print_runtime("Remove backpack from cart"):
            self.click('button:contains("Remove")')  # HTML innerText
            self.assert_text_not_visible("Backpack", "div.cart_item")
        with decorators.print_runtime("Log out from Swag Labs", 3):
            self.js_click("a#logout_sidebar_link")
            self.assert_element("div#login_button_container")
