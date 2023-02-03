"""A complete end-to-end test for an e-commerce website."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    def test_swag_labs(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_exact_text("PRODUCTS", "span.title")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("YOUR CART", "span.title")
        self.assert_text("Backpack", "div.cart_item")
        self.click("button#checkout")
        self.type("#first-name", "SeleniumBase")
        self.type("#last-name", "Automation")
        self.type("#postal-code", "77123")
        self.click("input#continue")
        self.assert_text("CHECKOUT: OVERVIEW")
        self.assert_text("Backpack", "div.cart_item")
        self.assert_text("29.99", "div.inventory_item_price")
        self.click("button#finish")
        self.assert_exact_text("THANK YOU FOR YOUR ORDER", "h2")
        self.assert_element('img[alt="Pony Express"]')
        self.js_click("a#logout_sidebar_link")
        self.assert_element("div#login_button_container")


#######################################################################
#
#    ****  NOTES / USEFUL INFO  ****
#
# 1. By default, page elements are identified by "css selector".
#    CSS Guide: "https://www.w3schools.com/cssref/css_selectors.asp".
#    Other selectors include: "link text", "partial link text", "name",
#    "class name", and "id", but most of those can be expressed as CSS.
#
#    Here's an example of changing the "by":
#    [
#        self.click('Next', by="partial link text")
#    ]
#
#    XPath is used by default if the arg starts with "/", "./", or "(":
#    [
#        self.click('/html/body/div[3]/div[4]/p[2]/a')
#    ]
#
#    If you're completely new to CSS selectors, right-click on a
#    web page and select "Inspect" to see the CSS in the html.
#
# 2. Most methods have the optional "timeout" argument.
#    Here's an example of changing the "timeout":
#    [
#        self.assert_element('img[alt="Python"]', timeout=15)
#    ]
#    The "timeout" argument tells the method how many seconds to wait
#    for an element to appear before failing the test. This is
#    useful if a web page needs additional time to load an element.
#    If you don't specify a "timeout", a default timeout is used.
#    Default timeouts are configured in seleniumbase/config/settings.py
#
# 3. SeleniumBase methods often perform multiple actions. For example,
#    self.type(SELECTOR, TEXT) will do the following:
#    * Wait for the element to be visible
#    * Wait for the element to be interactive
#    * Clear the text field
#    * Type in the new text
#    * Press Enter/Return if the text ends in "\n": {element.submit()}
#
# 4. There are duplicate method names that exist for the same method:
#    (This makes it easier to switch over from other test frameworks.)
#    Example:
#    self.open() = self.visit() = self.open_url() = self.goto()
#    self.type() = self.update_text() = self.input() = self.fill()
#    self.send_keys() = self.add_text()
#    self.get_element() = self.wait_for_element_present()
#    self.find_element() = self.wait_for_element_visible()
#                        = self.wait_for_element()
#    self.assert_element() = self.assert_element_visible()
#    self.assert_text() = self.assert_text_visible()
#    self.find_text() = self.wait_for_text_visible()
#                     = self.wait_for_text()
#    self.click_link("LinkText") = self.click("link=LinkText")
#                            = self.click_link_text("LinkText")
#                            = self.click('a:contains("LinkText")')
#    * self.get(url) is SPECIAL: *
#    If {url} is a valid URL, self.get() works just like self.open()
#    Otherwise {url} becomes a selector for calling self.get_element()
#
# 5. There's usually more than one way to do the same thing.
#    Example 1:
#    [
#        self.assert_text("xkcd: volume 0", "h3")
#    ]
#    Is the same as:
#    [
#        text = self.get_text("h3")
#        self.assert_true("xkcd: volume 0" in text)
#    ]
#    Is also the same as:
#    [
#        element = self.find_element("h3")
#        text = element.text
#        self.assert_true("xkcd: volume 0" in text)
#    ]
#
#    Example 2:
#    [
#        self.assert_exact_text("xkcd.com", "h2")
#    ]
#    Is the same as:
#    [
#        text = self.get_text("h2").strip()
#        self.assert_true("xkcd.com".strip() == text)
#    ]
#
#    Example 3:
#    [
#        title = self.get_attribute("#comic img", "title")
#    ]
#    Is the same as:
#    [
#        element = self.find_element("#comic img")
#        title = element.get_attribute("title")
#    ]
#
# 6. self.assert_exact_text(TEXT) ignores leading and trailing
#    whitespace in the TEXT assertion.
#    So, self.assert_exact_text("Some Text") will find [" Some Text "].
#
# 7. self.js_click(SELECTOR) can be used to click on hidden elements.
#
# 8. self.open(URL) will automatically complete URLs missing a prefix.
#    Example: google.com will become https://google.com before opened.
#
# 9. For the full method list, see one of the following:
#    * SeleniumBase/seleniumbase/fixtures/base_case.py
#    * SeleniumBase/help_docs/method_summary.md
#
# 10. BaseCase.main(__name__, __file__) enables "python" to run pytest,
#     which is useful if someone forgets that tests run with "pytest".
