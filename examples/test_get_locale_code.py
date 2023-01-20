from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class LocaleTests(BaseCase):
    def test_get_locale_code(self):
        self.open("about:blank")
        locale_code = self.get_locale_code()
        message = '\nLocale Code = "%s"' % locale_code
        print(message)
        self.set_messenger_theme(theme="flat", location="top_center")
        self.post_message(message, duration=4)
