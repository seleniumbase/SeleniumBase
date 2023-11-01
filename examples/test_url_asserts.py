from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class URLTestClass(BaseCase):
    def test_url_asserts(self):
        self.open("https://seleniumbase.io/help_docs/how_it_works/")
        self.assert_url("https://seleniumbase.io/help_docs/how_it_works/")
        self.assert_title_contains("How it Works")
        self.js_click('nav a:contains("Coffee Cart")')
        self.assert_url_contains("/coffee")
        self.assert_title("Coffee Cart")
