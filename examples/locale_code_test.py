from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class LocaleCodeTests(BaseCase):
    def test_locale_code(self):
        self.open("https://localeplanet.com/support/browser.html")
        locale_code = self.get_locale_code()
        print("\nYour Browser's Locale Code: %s" % locale_code)
        expected_text = "navigator.language: %s" % locale_code
        self.demo_mode = True  # Display test actions
        self.assert_text(expected_text, "pre")
