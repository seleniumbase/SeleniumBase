"""
This is the Docker version of the Selenium plugin.
"""

import os
from nose.plugins import Plugin
from pyvirtualdisplay import Display
from selenium import webdriver
from seleniumbase.fixtures import constants


class SeleniumBrowser(Plugin):
    """
    The plugin for Selenium tests. Takes in key arguments and then
    creates a WebDriver object. All arguments are passed to the tests.

    The following variables are made to the tests:
    self.options.browser -- the browser to use (--browser)
    self.options.server -- the server used by the test (--server)
    self.options.port -- the port used by thest (--port)
    """
    name = 'selenium_docker'  # Usage: --with-selenium_docker

    def options(self, parser, env):
        super(SeleniumBrowser, self).options(parser, env=env)

        parser.add_option('--browser', action='store',
                          dest='browser',
                          choices=constants.Browser.VERSION.keys(),
                          default=constants.Browser.FIREFOX,
                          help="""Specifies the browser. Default: FireFox.
                               If you want to use Chrome, indicate that.""")
        parser.add_option('--browser_version', action='store',
                          dest='browser_version',
                          default="latest",
                          help="""The browser version to use. Explicitly select
                          a version number or use "latest".""")
        parser.add_option('--server', action='store', dest='servername',
                          default='localhost',
                          help="""Designates the server used by the test.
                               Default: localhost.""")
        parser.add_option('--port', action='store', dest='port',
                          default='4444',
                          help="""Designates the port used by the test.
                               Default: 4444.""")

    def configure(self, options, conf):
        super(SeleniumBrowser, self).configure(options, conf)
        self.display = Display(visible=0, size=(1200, 800))
        self.display.start()
        self.driver = self.__select_browser()
        self.options = options

    def beforeTest(self, test):
        """ Running Selenium locally will be handled differently
            from how Selenium is run remotely, such as from Jenkins. """

        try:
            self.driver = self.__select_browser()
            test.test.driver = self.driver
            test.test.browser = "firefox"
        except Exception as err:
            print "Error starting/connecting to Selenium:"
            print err
            os.kill(os.getpid(), 9)
        return self.driver

    def afterTest(self, test):
        try:
            self.driver.quit()
            self.display.stop()
        except:
            print "No driver to quit."

    def __select_browser(self):
        try:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("reader.parse-on-load.enabled", False)
            return webdriver.Firefox(profile)
        except:
            return webdriver.Firefox()
