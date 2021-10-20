"""
This script installs the chromedriver version that matches your Chrome.
On newer versions of Python, you may replace "testdir" with "pytester".
(Run with "pytest") / (For Linux/macOS systems only!)
"""
import subprocess
import sys


class TestUpgradeChromedriver():
    def basic_run(self, testdir):
        testdir.makepyfile(
            """
            from seleniumbase import BaseCase
            class MyTestCase(BaseCase):
                def test_passing(self):
                    pass
            """
        )
        return testdir

    def upgrade_chromedriver(self, testdir):
        testdir.makepyfile(
            """
            import subprocess
            from seleniumbase import BaseCase
            class MyTestCase(BaseCase):
                def test_upgrade(self):
                    chrome_version = self.get_chrome_version()
                    major_chrome_ver = chrome_version.split(".")[0]
                    chromedriver_ver = self.get_chromedriver_version()
                    major_chromedriver_ver = chromedriver_ver.split(".")[0]
                    if major_chromedriver_ver != major_chrome_ver:
                        subprocess.check_call(
                            "sbase install chromedriver %s" % major_chrome_ver,
                            shell=True
                        )
            """
        )
        return testdir

    def print_versions_of_chromedriver_and_chrome(self, testdir):
        testdir.makepyfile(
            """
            from seleniumbase import BaseCase
            class MyTestCase(BaseCase):
                def test_print_versions(self):
                    chrome_version = self.get_chrome_version()
                    major_chrome_ver = chrome_version.split(".")[0]
                    chromedriver_ver = self.get_chromedriver_version()
                    major_chromedriver_ver = chromedriver_ver.split(".")[0]
                    print(
                        "\\n* Now using chromedriver %s with Chrome %s"
                        % (chromedriver_ver, chrome_version)
                    )
                    if major_chromedriver_ver == major_chrome_ver:
                        print(
                            "* SUCCESS: "
                            "The chromedriver version is compatible "
                            "with Chrome!"
                        )
                    elif major_chromedriver_ver < major_chrome_ver:
                        print("* !!! Version Mismatch !!!")
                        print(
                            "* The version of chromedriver is too low!\\n"
                            "* Try upgrading to chromedriver %s manually:\\n"
                            "* >>> sbase install chromedriver %s <<<"
                            % (major_chrome_ver, major_chrome_ver)
                        )
                    else:
                        print("* !!! Version Mismatch !!!")
                        print(
                            "* The version of chromedriver is too high!\\n"
                            "* Try downgrading to chromedriver %s manually:\\n"
                            "* >>> sbase install chromedriver %s <<<"
                            % (major_chrome_ver, major_chrome_ver)
                        )
            """
        )
        return testdir

    def test_upgrade_chromedriver(self, testdir):
        if "linux" not in sys.platform and "darwin" not in sys.platform:
            print("\n  This script is for Linux/macOS systems only!")
            self.skip("This script is for Linux/macOS systems only!")
        # Find out if the installed chromedriver version works with Chrome
        testdir = self.basic_run(testdir)
        result = testdir.inline_run("--headless")
        try:
            assert result.matchreport("test_passing").passed
        except Exception:
            # Install the compatibility version of chromedriver
            subprocess.check_call(
                "seleniumbase install chromedriver 2.44", shell=True
            )
        # Upgrade chromedriver to match the installed version of Chrome
        testdir = self.upgrade_chromedriver(testdir)
        result = testdir.inline_run("--headless", "-s")
        # Print the final installed versions of chromedriver and Chrome
        testdir = self.print_versions_of_chromedriver_and_chrome(testdir)
        result = testdir.inline_run("--headless", "-s")
