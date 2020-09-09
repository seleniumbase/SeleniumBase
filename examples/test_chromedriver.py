"""
This test is only for Chrome!
(Verify that your chromedriver is compatible with your version of Chrome.)
"""
import colorama
from seleniumbase import BaseCase


class ChromeTestClass(BaseCase):

    def test_chromedriver_matches_chrome(self):
        if self.browser != "chrome":
            print("\n  This test is only for Chrome!")
            print("  (Run with: '--browser=chrome')")
            self.skip("This test is only for Chrome!")
        driver_capabilities = self.driver.__dict__["capabilities"]
        if "version" in driver_capabilities:
            chrome_version = driver_capabilities["version"]
        else:
            chrome_version = driver_capabilities["browserVersion"]
        major_chrome_version = chrome_version.split('.')[0]
        chrome_dict = self.driver.__dict__["capabilities"]["chrome"]
        chromedriver_version = chrome_dict["chromedriverVersion"]
        chromedriver_version = chromedriver_version.split(' ')[0]
        major_chromedriver_version = chromedriver_version.split('.')[0]
        colorama.init(autoreset=True)
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
        c4 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTGREEN_EX
        cr = colorama.Style.RESET_ALL
        pr_chromedriver_version = c3 + chromedriver_version + cr
        pr_chrome_version = c2 + chrome_version + cr
        message = (
            "\n"
            "* Your version of chromedriver is: %s\n"
            "*\n* And your version of Chrome is: %s"
            "" % (pr_chromedriver_version, pr_chrome_version))
        print(message)
        if major_chromedriver_version < major_chrome_version:
            install_sb = (
                "seleniumbase install chromedriver %s" % major_chrome_version)
            pr_install_sb = c1 + install_sb + cr
            up_msg = "You may want to upgrade your version of chromedriver:"
            up_msg = c4 + up_msg + cr
            message = ("*\n* %s\n*\n* >>> %s" % (up_msg, pr_install_sb))
            print(message)
        elif major_chromedriver_version > major_chrome_version:
            up_msg = "You may want to upgrade your version of Chrome:"
            up_msg = c5 + up_msg + cr
            up_url = c1 + "chrome://settings/help" + cr
            message = ("*\n* %s\n*\n* See: %s" % (up_msg, up_url))
            print(message)
        else:
            up_msg = (
                "Success! Your chromedriver is compatible with your Chrome!")
            up_msg = c1 + up_msg + cr
            message = ("*\n* %s\n" % up_msg)
            print(message)
