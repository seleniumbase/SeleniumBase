""" This is the pytest configuration file """

import optparse
import os
import pytest
import shutil
import time
from seleniumbase.config import settings
from seleniumbase.fixtures import constants


def pytest_addoption(parser):
    parser = parser.getgroup('SeleniumBase',
                             'SeleniumBase specific configuration options')
    parser.addoption('--browser', action="store",
                     dest='browser',
                     choices=constants.Browser.VERSION.keys(),
                     default=constants.Browser.GOOGLE_CHROME,
                     help="""Specifies the web browser to use. Default: Chrome.
                          If you want to use Firefox, explicitly indicate that.
                          Example: (--browser=firefox)""")
    parser.addoption('--with-selenium', action="store_true",
                     dest='with_selenium',
                     default=False,
                     help="Use if tests need to be run with a web browser.")
    parser.addoption('--data', dest='data',
                     default=None,
                     help='Extra data to pass from the command line.')
    parser.addoption('--with-testing_base', action="store_true",
                     dest='with_testing_base',
                     default=False,
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
                     choices=('prod', 'qa', 'test'),
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
    parser.addoption('--headless', action="store_true",
                     dest='headless',
                     default=False,
                     help="""Using this makes Webdriver run headlessly,
                          which is useful inside a Linux Docker.""")
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
    log_folder_setup(config)


def log_folder_setup(config):
    """ Handle Logging """
    with_testing_base = config.getoption('with_testing_base')
    if with_testing_base:
        log_path = config.getoption('log_path')
        if log_path.endswith("/"):
            log_path = log_path[:-1]
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        else:
            archived_folder = "%s/../archived_logs/" % log_path
            if not os.path.exists(archived_folder):
                os.makedirs(archived_folder)
            archived_logs = "%slogs_%s" % (archived_folder, int(time.time()))
            shutil.move(log_path, archived_logs)
            os.makedirs(log_path)
            if not settings.ARCHIVE_EXISTING_LOGS:
                shutil.rmtree(archived_logs)


def pytest_unconfigure():
    """ This runs after all tests have completed with pytest """
    pass


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
        except:
            pass
        try:
            if hasattr(self, 'headless') and self.headless:
                if self.headless_active:
                    if hasattr(self, 'display') and self.display:
                        self.display.stop()
        except:
            pass
    except:
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
        except:
            pass
