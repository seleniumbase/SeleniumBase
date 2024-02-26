import sys
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ChromedriverTests(BaseCase):
    def test_fail_if_versions_dont_match(self):
        self.open("about:blank")
        if self.browser != "chrome":
            print("\n  This test is only for Chrome!")
            self.skip("This test is only for Chrome!")
        chrome_version = self.get_chrome_version()
        major_chrome_version = chrome_version.split(".")[0]
        chromedriver_version = self.get_chromedriver_version()
        major_chromedriver_version = chromedriver_version.split(".")[0]
        install_sb = "sbase get chromedriver %s" % major_chrome_version
        arg_join = " ".join(sys.argv)
        message = (
            'Your version of chromedriver: "%s"\n  '
            'does not match your version of Chrome: "%s"\n'
            'Run this command to fix that: "%s"'
            % (chromedriver_version, chrome_version, install_sb)
        )
        if "--driver-version=" in arg_join or "--driver-version=" in arg_join:
            if int(major_chromedriver_version) != int(major_chrome_version):
                print("\nWarning -> " + message)
        elif int(major_chromedriver_version) != int(major_chrome_version):
            raise Exception(message)
        else:
            print(
                "\n* Chrome version: {%s}\n* Driver version: {%s}"
                % (chromedriver_version, chrome_version)
            )
