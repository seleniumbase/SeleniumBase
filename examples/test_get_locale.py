from seleniumbase import BaseCase


class LocaleTestClass(BaseCase):

    def test_get_locale_code(self):
        self.open("data:,")
        locale_code = self.get_locale_code()
        message = '\nLocale Code = "%s"' % locale_code
        print(message)
        self.set_messenger_theme(
            theme="flat", location="top_center")
        self.post_message(message, duration=4)
