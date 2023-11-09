from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class LocaleCodeTests(BaseCase):
    def test_locale_code(self):
        self.open("about:blank")
        locale_code = self.get_locale_code()  # navigator.language
        print("\nYour Browser's Locale Code: %s" % locale_code)
        if self.browser == "chrome" and not self.headless:
            self.open("chrome://settings/languages")
            language_info = self.get_text(
                "settings-ui::shadow "
                "settings-main::shadow "
                "settings-basic-page::shadow "
                "settings-languages-page::shadow "
                "#languagesSection div.start div"
            )
            print("Language info (chrome://settings/languages):")
            print(language_info)
            self.sleep(1)
