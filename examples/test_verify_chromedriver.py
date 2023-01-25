from seleniumbase import BaseCase


class ChromedriverTests(BaseCase):
    def test_fail_if_using_an_old_chromedriver(self):
        self.open("data:,")
        if self.browser != "chrome":
            self.open_if_not_url("data:,")
            print("\n  This test is only for Chrome!")
            print("  (Run with: '--browser=chrome')")
            self.skip("This test is only for Chrome!")
        chrome_version = self.get_chrome_version()
        major_chrome_version = chrome_version.split(".")[0]
        chromedriver_version = self.get_chromedriver_version()
        major_chromedriver_version = chromedriver_version.split(".")[0]
        install_sb = "sbase install chromedriver %s" % major_chrome_version
        if (
            int(major_chromedriver_version) < 73
            and int(major_chrome_version) >= 73
        ):
            message = (
                'Your version of chromedriver: "%s"\n  '
                'is too old for your version of Chrome: "%s"\n'
                "You should upgrade chromedriver "
                "to receive important bug fixes!\n"
                'Run this command to upgrade: "%s"'
                % (chromedriver_version, chrome_version, install_sb)
            )
            raise Exception(message)  # chromedriver is out-of-date
