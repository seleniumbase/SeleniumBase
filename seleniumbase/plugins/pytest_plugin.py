""" This is the pytest configuration file """

import optparse
import pytest
from seleniumbase.core import log_helper
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants


def pytest_addoption(parser):
    parser = parser.getgroup('SeleniumBase',
                             'SeleniumBase specific configuration options')
    parser.addoption('--browser', action="store",
                     dest='browser',
                     type=str.lower,
                     choices=constants.ValidBrowsers.valid_browsers,
                     default=constants.Browser.GOOGLE_CHROME,
                     help="""Specifies the web browser to use. Default: Chrome.
                          If you want to use Firefox, explicitly indicate that.
                          Example: (--browser=firefox)""")
    parser.addoption('--with-selenium', action="store_true",
                     dest='with_selenium',
                     default=True,
                     help="Use if tests need to be run with a web browser.")
    parser.addoption('--env', action='store',
                     dest='environment',
                     type=str.lower,
                     choices=(
                         constants.Environment.QA,
                         constants.Environment.STAGING,
                         constants.Environment.DEVELOP,
                         constants.Environment.PRODUCTION,
                         constants.Environment.MASTER,
                         constants.Environment.LOCAL,
                         constants.Environment.TEST
                     ),
                     default=constants.Environment.TEST,
                     help="The environment to run the tests in.")
    parser.addoption('--data', dest='data',
                     default=None,
                     help='Extra data to pass from the command line.')
    parser.addoption('--with-testing_base', action="store_true",
                     dest='with_testing_base',
                     default=True,
                     help="Use to save logs (screenshots) when tests fail.")
    parser.addoption('--log_path', dest='log_path',
                     default='latest_logs/',
                     help='Where the log files are saved.')
    parser.addoption('--with-db_reporting', action="store_true",
                     dest='with_db_reporting',
                     default=False,
                     help="Use to record test data in the MySQL database.")
    parser.addoption('--database_env', action='store',
                     dest='database_env',
                     choices=(
                         'production', 'qa', 'staging', 'develop',
                         'test', 'local', 'master'
                     ),
                     default='test',
                     help=optparse.SUPPRESS_HELP)
    parser.addoption('--with-s3_logging', action="store_true",
                     dest='with_s3_logging',
                     default=False,
                     help="Use to save test log files in Amazon S3.")
    parser.addoption('--with-screen_shots', action="store_true",
                     dest='with_screen_shots',
                     default=False,
                     help="Use to save screenshots on test failure.")
    parser.addoption('--with-basic_test_info', action="store_true",
                     dest='with_basic_test_info',
                     default=False,
                     help="Use to save basic test info on test failure.")
    parser.addoption('--with-page_source', action="store_true",
                     dest='with_page_source',
                     default=False,
                     help="Use to save page source on test failure.")
    parser.addoption('--server', action='store',
                     dest='servername',
                     default='localhost',
                     help="""Designates the Selenium Grid server to use.
                          Default: localhost.""")
    parser.addoption('--port', action='store',
                     dest='port',
                     default='4444',
                     help="""Designates the Selenium Grid port to use.
                          Default: 4444.""")
    parser.addoption('--proxy', action='store',
                     dest='proxy_string',
                     default=None,
                     help="""Designates the proxy server:port to use.
                          Format: servername:port.  OR
                                  username:password@servername:port  OR
                                  A dict key from proxy_list.PROXY_LIST
                          Default: None.""")
    parser.addoption('--headless', action="store_true",
                     dest='headless',
                     default=False,
                     help="""Using this makes Webdriver run headlessly,
                          which is required on headless machines.""")
    parser.addoption('--is_pytest', action="store_true",
                     dest='is_pytest',
                     default=True,
                     help="""This is used by the BaseCase class to tell apart
                          pytest runs from nosetest runs. (Automatic)""")
    parser.addoption('--demo_mode', action="store_true",
                     dest='demo_mode',
                     default=False,
                     help="""Using this slows down the automation so that
                          you can see what it's actually doing.""")
    parser.addoption('--demo_sleep', action='store', dest='demo_sleep',
                     default=None,
                     help="""Setting this overrides the Demo Mode sleep
                          time that happens after browser actions.""")
    parser.addoption('--highlights', action='store', dest='highlights',
                     default=None,
                     help="""Setting this overrides the default number of
                          highlight animation loops to have per call.""")
    parser.addoption('--message_duration', action="store",
                     dest='message_duration',
                     default=None,
                     help="""Setting this overrides the default time that
                          messenger notifications remain visible when reaching
                          assert statements during Demo Mode.""")
    parser.addoption('--ad_block', action="store_true",
                     dest='ad_block_on',
                     default=False,
                     help="""Using this makes WebDriver block display ads
                          that are defined in ad_block_list.AD_BLOCK_LIST.""")
    parser.addoption('--verify_delay', action='store', dest='verify_delay',
                     default=None,
                     help="""Setting this overrides the default wait time
                          before each MasterQA verification pop-up.""")
    parser.addoption('--timeout_multiplier', action='store',
                     dest='timeout_multiplier',
                     default=None,
                     help="""Setting this overrides the default timeout
                          by the multiplier when waiting for page elements.
                          Unused when tests overide the default value.""")


def pytest_configure(config):
    """ This runs after command line options have been parsed """
    with_testing_base = config.getoption('with_testing_base')
    if with_testing_base:
        log_path = config.getoption('log_path')
        log_helper.log_folder_setup(log_path)
    proxy_helper.remove_proxy_zip_if_present()


def pytest_unconfigure():
    """ This runs after all tests have completed with pytest. """
    proxy_helper.remove_proxy_zip_if_present()


def pytest_runtest_setup():
    """ This runs before every test with pytest """
    pass


def pytest_runtest_teardown(item):
    """ This runs after every test with pytest """

    # Make sure webdriver has exited properly and any headless display
    try:
        self = item._testcase
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except Exception:
            pass
        try:
            if hasattr(self, 'headless') and self.headless:
                if self.headless_active:
                    if hasattr(self, 'display') and self.display:
                        self.display.stop()
        except Exception:
            pass
    except Exception:
        pass


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    if pytest_html and report.when == 'call':
        try:
            extra_report = item._testcase._html_report_extra
            extra = getattr(report, 'extra', [])
            report.extra = extra + extra_report
        except Exception:
            pass
