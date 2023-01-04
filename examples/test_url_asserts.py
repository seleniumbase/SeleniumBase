from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class URLTestClass(BaseCase):
    def test_url_asserts(self):
        self.open("https://seleniumbase.io/")
        self.assert_url("https://seleniumbase.io/")
        self.assert_title_contains("SeleniumBase")
        self.js_click('nav a:contains("Coffee Cart")')
        self.assert_url_contains("/coffee")
        self.assert_title("Coffee Cart")
