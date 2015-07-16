"""
This is the Selenium plugin. It takes in some default parameters that tests need.
It also provides a WebDriver object for the tests to use.
"""

import time
import os
from nose.plugins import Plugin
from selenium import webdriver
from test_framework.core import selenium_launcher
from test_framework.fixtures import constants


class SeleniumBase(Plugin):
    """
    The plugin for Selenium tests. Takes in key arguments and then
    creates a WebDriver object. All arguments are passed to the tests.

    The following variables are made to the tests:
    self.options.browser -- the browser to use (--browser)
    self.options.server -- the server used by the test (--server)
    self.options.port -- the port used by thest (--port)
    """
    name = 'selenium'  # Usage: --with-selenium

    def options(self, parser, env):
        super(SeleniumBase, self).options(parser, env=env)

        parser.add_option('--browser', action='store',
                          dest='browser',
                          choices=constants.Browser.VERSION.keys(),
                          default=constants.Browser.FIREFOX,
                          help="""Specifies the browser to use. Default = FireFox.
                          If you want to use Chrome, explicitly indicate that.""")
        parser.add_option('--browser_version', action='store',
                          dest='browser_version',
                          default="latest",
                          help="""The browser version to use. Explicitly select
                          a version number or use "latest".""")
        parser.add_option('--server', action='store', dest='servername',
                          default='localhost',
                          help="Designates the server used by the test. Default: localhost.")
        parser.add_option('--port', action='store', dest='port',
                          default='4444',
                          help="Designates the port used by the test. Default: 4444.")


    def configure(self, options, conf):
        super(SeleniumBase, self).configure(options, conf)
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
        ### print 'OPTIONS = ' + str(self.options)  # Try this for debugging if needed

        if (self.options.servername == "localhost" and
            self.options.browser == constants.Browser.HTML_UNIT):
            selenium_launcher.execute_selenium(self.options.servername,
                                               self.options.port,
                                               self.options.log_path)


    def beforeTest(self, test):
        """ Running Selenium locally will be handled differently
            from how Selenium is run remotely, such as from Jenkins. """

        if self.options.servername == "localhost":
            try:
                self.driver = self.__select_browser(self.options.browser)
                test.test.driver = self.driver
                if "version" in self.browser_settings.keys():
                    version = self.browser_settings["version"]
                else:
                    version = ""
                test.test.browser = "%s%s" % (self.options.browser, version)
            except Exception as err:
                print "Error starting/connecting to Selenium:"
                print err
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
                    test.test.browser = "%s%s" % (self.options.browser, version)
                    connected = True
                    break
                except Exception as err:
                    # nose eats beforeTest exceptions, so this gets the word out if something breaks here
                    print "Attempt #%s to connect to Selenium failed" % i
                    if i < 3:
                        print "Retrying in 15 seconds..."
                        time.sleep(15)
            if not connected:
                print "Error starting/connecting to Selenium:"
                print err
                print "\n\n\n"
                os.kill(os.getpid(), 9)


    def afterTest(self, test):
        try:
            self.driver.quit()
        except:
            print "No driver to quit."


    def __select_browser(self, browser_name):
        if (self.options.servername != "localhost" or
            self.options.browser == constants.Browser.HTML_UNIT):
            return webdriver.Remote("http://%s:%s/wd/hub" %
                                    (self.options.servername,
                                    self.options.port),
                                    self.browser_settings)
        else:
            if browser_name == constants.Browser.FIREFOX:
                try:
                    profile = webdriver.FirefoxProfile()
                    profile.set_preference("reader.parse-on-load.enabled", False)
                    return webdriver.Firefox(profile)
                except:
                    return webdriver.Firefox()
            if browser_name == constants.Browser.INTERNET_EXPLORER:
                return webdriver.Ie()
            if browser_name == constants.Browser.PHANTOM_JS:
                return webdriver.PhantomJS()
            if browser_name == constants.Browser.GOOGLE_CHROME:
                try:
                    # Make it possible for Chrome to save screenshot files to disk.
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument("--allow-file-access-from-files")
                    return webdriver.Chrome(chrome_options=chrome_options)
                except Exception:
                    return webdriver.Chrome()
