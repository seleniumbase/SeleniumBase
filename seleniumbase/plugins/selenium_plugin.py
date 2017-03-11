"""
This plugin gives the power of Selenium to nosetests
by providing a WebDriver object for the tests to use.
"""

import time
import os
from nose.plugins import Plugin
from selenium import webdriver
from pyvirtualdisplay import Display
from seleniumbase.core import selenium_launcher
from seleniumbase.core import browser_launcher
from seleniumbase.fixtures import constants


class SeleniumBrowser(Plugin):
    """
    The plugin for Selenium tests. Takes in key arguments and then
    creates a WebDriver object. All arguments are passed to the tests.

    The following command line options are available to the tests:
    self.options.browser -- the browser to use (--browser)
    self.options.server -- the server used by the test (--server)
    self.options.port -- the port used by the test (--port)
    self.options.headless -- the option to run headlessly (--headless)
    self.options.demo_mode -- the option to slow down Selenium (--demo_mode)
    self.options.demo_sleep -- Selenium action delay in DemoMode (--demo_sleep)
    self.options.highlights -- # of highlight animations shown (--highlights)
    self.options.verify_delay -- delay before MasterQA checks (--verify_delay)
    """
    name = 'selenium'  # Usage: --with-selenium

    def options(self, parser, env):
        super(SeleniumBrowser, self).options(parser, env=env)

        parser.add_option(
            '--browser', action='store',
            dest='browser',
            choices=constants.Browser.VERSION.keys(),
            default=constants.Browser.GOOGLE_CHROME,
            help="""Specifies the web browser to use. Default: Chrome.
                    If you want to use Firefox, explicitly indicate that.
                    Example: (--browser=firefox)""")
        parser.add_option(
            '--browser_version', action='store',
            dest='browser_version',
            default="latest",
            help="""The browser version to use. Explicitly select
                    a version number or use "latest".""")
        parser.add_option(
            '--server', action='store', dest='servername',
            default='localhost',
            help="""Designates the server used by the test.
                    Default: localhost.""")
        parser.add_option(
            '--port', action='store', dest='port',
            default='4444',
            help="""Designates the port used by the test.
                    Default: 4444.""")
        parser.add_option(
            '--headless', action="store_true",
            dest='headless',
            default=False,
            help="""Using this makes Webdriver run headlessly,
                    which is useful inside a Linux Docker.""")
        parser.add_option(
            '--demo_mode', action="store_true",
            dest='demo_mode',
            default=False,
            help="""Using this slows down the automation so that
                    you can see what it's actually doing.""")
        parser.add_option(
            '--demo_sleep', action='store', dest='demo_sleep',
            default=None,
            help="""Setting this overrides the Demo Mode sleep
                    time that happens after browser actions.""")
        parser.add_option(
            '--highlights', action='store',
            dest='highlights', default=None,
            help="""Setting this overrides the default number of
                    highlight animation loops to have per call.""")
        parser.add_option(
            '--verify_delay', action='store',
            dest='verify_delay', default=None,
            help="""Setting this overrides the default wait time
                    before each MasterQA verification pop-up.""")

    def configure(self, options, conf):
        super(SeleniumBrowser, self).configure(options, conf)
        if not self.enabled:
            return

        # Determine the browser version to use, and configure settings
        self.browser_settings = {
            "browserName": options.browser,
            'name': self.conf.testNames[0],
            'build': os.getenv('BUILD_TAG'),
            'project': os.getenv('JOB_NAME')
        }

        if options.browser == constants.Browser.INTERNET_EXPLORER:
            self.browser_settings["platform"] = "WINDOWS"
            self.browser_settings["browserName"] = "internet explorer"

        if options.browser_version == 'latest':
            version = constants.Browser.LATEST[options.browser]
            if version is not None:
                self.browser_settings["version"] = version
        else:
            version_options = constants.Browser.VERSION[options.browser]
            if (version_options is not None and
                    options.browser_version in version_options):
                self.browser_settings["version"] = options.browser_version

        self.options = options
        self.headless_active = False

        if (self.options.servername == "localhost" and
                self.options.browser == constants.Browser.HTML_UNIT):
            selenium_launcher.execute_selenium(self.options.servername,
                                               self.options.port,
                                               self.options.log_path)

    def beforeTest(self, test):
        """ Running Selenium locally will be handled differently
            from how Selenium is run remotely, such as from Jenkins. """

        if self.options.headless:
            self.display = Display(visible=0, size=(1200, 800))
            self.display.start()
            self.headless_active = True
        if self.options.servername == "localhost":
            try:
                self.driver = self.__select_browser(self.options.browser)
                test.test.driver = self.driver
                if "version" in self.browser_settings.keys():
                    version = self.browser_settings["version"]
                else:
                    version = ""
                test.test.browser = "%s%s" % (self.options.browser, version)
                test.test.demo_mode = self.options.demo_mode
                test.test.demo_sleep = self.options.demo_sleep
                test.test.highlights = self.options.highlights
                test.test.verify_delay = self.options.verify_delay  # MasterQA
            except Exception as err:
                print("Error starting/connecting to Selenium:")
                print(err)
                os.kill(os.getpid(), 9)
        else:
            connected = False
            for i in range(1, 4):
                try:
                    self.driver = self.__select_browser(self.options.browser)
                    test.test.driver = self.driver
                    if "version" in self.browser_settings.keys():
                        version = self.browser_settings["version"]
                    else:
                        version = ""
                    test.test.browser = "%s%s" % (
                        self.options.browser, version)
                    connected = True
                    break
                except Exception as err:
                    print("Attempt #%s to connect to Selenium failed" % i)
                    if i < 3:
                        print("Retrying in 3 seconds...")
                        time.sleep(3)
            if not connected:
                print("Error starting/connecting to Selenium:")
                print(err)
                print("\n\n")
                os.kill(os.getpid(), 9)

    def afterTest(self, test):
        try:
            self.driver.quit()
        except AttributeError:
            pass
        except:
            print("No driver to quit.")
        if self.options.headless:
            if self.headless_active:
                self.display.stop()

    def __select_browser(self, browser_name):
        if (self.options.servername != "localhost" or
                self.options.browser == constants.Browser.HTML_UNIT):
            return webdriver.Remote("http://%s:%s/wd/hub" % (
                self.options.servername,
                self.options.port),
                self.browser_settings)
        else:
            return browser_launcher.get_driver(browser_name)
