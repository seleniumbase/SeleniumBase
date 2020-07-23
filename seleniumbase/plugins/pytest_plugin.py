# -*- coding: utf-8 -*-
""" This is the pytest configuration file """

import pytest
import sys
from seleniumbase import config as sb_config
from seleniumbase.core import log_helper
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants


def pytest_addoption(parser):
    """
    This parser plugin includes the following command-line options for pytest:
    --browser=BROWSER  (The web browser to use.)
    --cap-file=FILE  (The web browser's desired capabilities to use.)
    --cap-string=STRING  (The web browser's desired capabilities to use.)
    --settings-file=FILE  (Overrides SeleniumBase settings.py values.)
    --env=ENV  (Set a test environment. Use "self.env" to use this in tests.)
    --data=DATA  (Extra data to pass to tests. Use "self.data" in tests.)
    --var1=DATA  (Extra data to pass to tests. Use "self.var1" in tests.)
    --var2=DATA  (Extra data to pass to tests. Use "self.var2" in tests.)
    --var3=DATA  (Extra data to pass to tests. Use "self.var3" in tests.)
    --user-data-dir=DIR  (Set the Chrome user data directory to use.)
    --server=SERVER  (The server / IP address used by the tests.)
    --port=PORT  (The port that's used by the test server.)
    --proxy=SERVER:PORT  (This is the proxy server:port combo used by tests.)
    --agent=STRING  (This designates the web browser's User Agent to use.)
    --mobile  (The option to use the mobile emulator while running tests.)
    --metrics=STRING  ("CSSWidth,Height,PixelRatio" for mobile emulator tests.)
    --extension-zip=ZIP  (Load a Chrome Extension .zip file, comma-separated.)
    --extension-dir=DIR  (Load a Chrome Extension directory, comma-separated.)
    --headless  (The option to run tests headlessly. The default on Linux OS.)
    --headed  (The option to run tests with a GUI on Linux OS.)
    --start-page=URL  (The starting URL for the web browser when tests begin.)
    --archive-logs  (Archive old log files instead of deleting them.)
    --time-limit=SECONDS  (Safely fail any test that exceeds the limit limit.)
    --slow  (The option to slow down the automation.)
    --demo  (The option to visually see test actions as they occur.)
    --demo-sleep=SECONDS  (The option to wait longer after Demo Mode actions.)
    --highlights=NUM  (Number of highlight animations for Demo Mode actions.)
    --message-duration=SECONDS  (The time length for Messenger alerts.)
    --check-js  (The option to check for JavaScript errors after page loads.)
    --ad-block  (The option to block some display ads after page loads.)
    --block-images (The option to block images from loading during tests.)
    --verify-delay=SECONDS  (The delay before MasterQA verification checks.)
    --disable-csp  (This disables the Content Security Policy of websites.)
    --enable-sync  (The option to enable "Chrome Sync".)
    --use-auto-ext  (The option to use Chrome's automation extension.)
    --swiftshader  (The option to use Chrome's "--use-gl=swiftshader" feature.)
    --incognito  (The option to enable Chrome's Incognito mode.)
    --guest  (The option to enable Chrome's Guest mode.)
    --devtools  (The option to open Chrome's DevTools when the browser opens.)
    --reuse-session  (The option to reuse the browser session between tests.)
    --crumbs  (Option to delete all cookies between tests reusing a session.)
    --maximize  (The option to start with the web browser maximized.)
    --save-screenshot  (The option to save a screenshot after each test.)
    --visual-baseline  (Set the visual baseline for Visual/Layout tests.)
    --timeout-multiplier=MULTIPLIER  (Multiplies the default timeout values.)
    """
    parser = parser.getgroup('SeleniumBase',
                             'SeleniumBase specific configuration options')
    parser.addoption('--browser',
                     action="store",
                     dest='browser',
                     type=str.lower,
                     choices=constants.ValidBrowsers.valid_browsers,
                     default=constants.Browser.GOOGLE_CHROME,
                     help="""Specifies the web browser to use. Default: Chrome.
                          If you want to use Firefox, explicitly indicate that.
                          Example: (--browser=firefox)""")
    parser.addoption('--with-selenium',
                     action="store_true",
                     dest='with_selenium',
                     default=True,
                     help="Use if tests need to be run with a web browser.")
    parser.addoption('--env',
                     action='store',
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
    parser.addoption('--data',
                     dest='data',
                     default=None,
                     help='Extra data to pass to tests from the command line.')
    parser.addoption('--var1',
                     dest='var1',
                     default=None,
                     help='Extra data to pass to tests from the command line.')
    parser.addoption('--var2',
                     dest='var2',
                     default=None,
                     help='Extra data to pass to tests from the command line.')
    parser.addoption('--var3',
                     dest='var3',
                     default=None,
                     help='Extra data to pass to tests from the command line.')
    parser.addoption('--cap_file', '--cap-file',
                     dest='cap_file',
                     default=None,
                     help="""The file that stores browser desired capabilities
                          for BrowserStack, Sauce Labs, and other
                          remote web drivers to use.""")
    parser.addoption('--cap_string', '--cap-string',
                     dest='cap_string',
                     default=None,
                     help="""The string that stores browser desired
                          capabilities for BrowserStack, Sauce Labs,
                          and other remote web drivers to use.
                          Enclose cap-string in single quotes.
                          Enclose parameter keys in double quotes.
                          Example: --cap-string='{"name":"test1","v":"42"}'""")
    parser.addoption('--settings_file', '--settings-file', '--settings',
                     action='store',
                     dest='settings_file',
                     default=None,
                     help="""The file that stores key/value pairs for
                          overriding values in the
                          seleniumbase/config/settings.py file.""")
    parser.addoption('--user_data_dir', '--user-data-dir',
                     dest='user_data_dir',
                     default=None,
                     help="""The Chrome User Data Directory to use. (Profile)
                          If the directory doesn't exist, it'll be created.""")
    parser.addoption('--with-testing_base', '--with-testing-base',
                     action="store_true",
                     dest='with_testing_base',
                     default=True,
                     help="""Use to save logs and screenshots when tests fail.
                          The following options are now active by default
                          with --with-testing_base (which is on by default):
                          --with-screen_shots ,
                          --with-basic_test_info ,
                          --with-page_source
                          """)
    parser.addoption('--log_path', '--log-path',
                     dest='log_path',
                     default='latest_logs/',
                     help='Where log files are saved. (No longer editable!)')
    parser.addoption('--archive_logs', '--archive-logs',
                     action="store_true",
                     dest='archive_logs',
                     default=False,
                     help="Archive old log files instead of deleting them.")
    parser.addoption('--with-db_reporting', '--with-db-reporting',
                     action="store_true",
                     dest='with_db_reporting',
                     default=False,
                     help="Use to record test data in the MySQL database.")
    parser.addoption('--database_env', '--database-env',
                     action='store',
                     dest='database_env',
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
                     help="The database environment to run the tests in.")
    parser.addoption('--with-s3_logging', '--with-s3-logging',
                     action="store_true",
                     dest='with_s3_logging',
                     default=False,
                     help="Use to save test log files in Amazon S3.")
    parser.addoption('--with-screen_shots', '--with-screen-shots',
                     action="store_true",
                     dest='with_screen_shots',
                     default=False,
                     help="""Use to save screenshots on test failure.
                          (Automatically on when using --with-testing_base)""")
    parser.addoption('--with-basic_test_info', '--with-basic-test-info',
                     action="store_true",
                     dest='with_basic_test_info',
                     default=False,
                     help="""Use to save basic test info on test failure.
                          (Automatically on when using --with-testing_base)""")
    parser.addoption('--with-page_source', '--with-page-source',
                     action="store_true",
                     dest='with_page_source',
                     default=False,
                     help="""Use to save page source on test failure.
                          (Automatically on when using --with-testing_base)""")
    parser.addoption('--server',
                     action='store',
                     dest='servername',
                     default='localhost',
                     help="""Designates the Selenium Grid server to use.
                          Use "127.0.0.1" to connect to a localhost Grid.
                          If unset or set to "localhost", Grid isn't used.
                          Default: "localhost".""")
    parser.addoption('--port',
                     action='store',
                     dest='port',
                     default='4444',
                     help="""Designates the Selenium Grid port to use.
                          Default: 4444.""")
    parser.addoption('--proxy',
                     action='store',
                     dest='proxy_string',
                     default=None,
                     help="""Designates the proxy server:port to use.
                          Format: servername:port.  OR
                                  username:password@servername:port  OR
                                  A dict key from proxy_list.PROXY_LIST
                          Default: None.""")
    parser.addoption('--agent', '--user-agent', '--user_agent',
                     action='store',
                     dest='user_agent',
                     default=None,
                     help="""Designates the User-Agent for the browser to use.
                          Format: A string.
                          Default: None.""")
    parser.addoption('--mobile', '--mobile-emulator', '--mobile_emulator',
                     action="store_true",
                     dest='mobile_emulator',
                     default=False,
                     help="""If this option is enabled, the mobile emulator
                          will be used while running tests.""")
    parser.addoption('--metrics', '--device-metrics', '--device_metrics',
                     action='store',
                     dest='device_metrics',
                     default=None,
                     help="""Designates the three device metrics of the mobile
                          emulator: CSS Width, CSS Height, and Pixel-Ratio.
                          Format: A comma-separated string with the 3 values.
                          Example: "375,734,3"
                          Default: None. (Will use default values if None)""")
    parser.addoption('--extension_zip', '--extension-zip', '--crx',
                     action='store',
                     dest='extension_zip',
                     default=None,
                     help="""Designates the Chrome Extension ZIP file to load.
                          Format: A comma-separated list of .zip or .crx files
                          containing the Chrome extensions to load.
                          Default: None.""")
    parser.addoption('--extension_dir', '--extension-dir',
                     action='store',
                     dest='extension_dir',
                     default=None,
                     help="""Designates the Chrome Extension folder to load.
                          Format: A directory containing the Chrome extension.
                          (Can also be a comma-separated list of directories.)
                          Default: None.""")
    parser.addoption('--headless',
                     action="store_true",
                     dest='headless',
                     default=False,
                     help="""Using this makes Webdriver run web browsers
                          headlessly, which is required on headless machines.
                          Default: False on Mac/Windows. True on Linux.""")
    parser.addoption('--headed', '--gui',
                     action="store_true",
                     dest='headed',
                     default=False,
                     help="""Using this makes Webdriver run web browsers with
                          a GUI when running tests on Linux machines.
                          (The default setting on Linux is headless.)
                          (The default setting on Mac or Windows is headed.)
                          """)
    parser.addoption('--start_page', '--start-page', '--url',
                     action='store',
                     dest='start_page',
                     default=None,
                     help="""Designates the starting URL for the web browser
                          when each test begins.
                          Default: None.""")
    parser.addoption('--is_pytest', '--is-pytest',
                     action="store_true",
                     dest='is_pytest',
                     default=True,
                     help="""This is used by the BaseCase class to tell apart
                          pytest runs from nosetest runs. (Automatic)""")
    parser.addoption('--time_limit', '--time-limit', '--timelimit',
                     action='store',
                     dest='time_limit',
                     default=None,
                     help="""Use this to set a time limit per test, in seconds.
                          If a test runs beyond the limit, it fails.""")
    parser.addoption('--slow_mode', '--slow-mode', '--slow',
                     action="store_true",
                     dest='slow_mode',
                     default=False,
                     help="""Using this slows down the automation.""")
    parser.addoption('--demo_mode', '--demo-mode', '--demo',
                     action="store_true",
                     dest='demo_mode',
                     default=False,
                     help="""Using this slows down the automation and lets you
                          visually see what the tests are actually doing.""")
    parser.addoption('--demo_sleep', '--demo-sleep',
                     action='store',
                     dest='demo_sleep',
                     default=None,
                     help="""Setting this overrides the Demo Mode sleep
                          time that happens after browser actions.""")
    parser.addoption('--highlights',
                     action='store',
                     dest='highlights',
                     default=None,
                     help="""Setting this overrides the default number of
                          highlight animation loops to have per call.""")
    parser.addoption('--message_duration', '--message-duration',
                     action="store",
                     dest='message_duration',
                     default=None,
                     help="""Setting this overrides the default time that
                          messenger notifications remain visible when reaching
                          assert statements during Demo Mode.""")
    parser.addoption('--check_js', '--check-js',
                     action="store_true",
                     dest='js_checking_on',
                     default=False,
                     help="""The option to check for JavaScript errors after
                          every page load.""")
    parser.addoption('--ad_block', '--ad-block', '--block_ads', '--block-ads',
                     action="store_true",
                     dest='ad_block_on',
                     default=False,
                     help="""Using this makes WebDriver block display ads
                          that are defined in ad_block_list.AD_BLOCK_LIST.""")
    parser.addoption('--block_images', '--block-images',
                     action="store_true",
                     dest='block_images',
                     default=False,
                     help="""Using this makes WebDriver block images from
                          loading on web pages during tests.""")
    parser.addoption('--verify_delay', '--verify-delay',
                     action='store',
                     dest='verify_delay',
                     default=None,
                     help="""Setting this overrides the default wait time
                          before each MasterQA verification pop-up.""")
    parser.addoption('--disable_csp', '--disable-csp', '--no_csp', '--no-csp',
                     action="store_true",
                     dest='disable_csp',
                     default=False,
                     help="""Using this disables the Content Security Policy of
                          websites, which may interfere with some features of
                          SeleniumBase, such as loading custom JavaScript
                          libraries for various testing actions.
                          Setting this to True (--disable_csp) overrides the
                          value set in seleniumbase/config/settings.py""")
    parser.addoption('--enable_sync', '--enable-sync',
                     action="store_true",
                     dest='enable_sync',
                     default=False,
                     help="""Using this enables the "Chrome Sync" feature.""")
    parser.addoption('--use_auto_ext', '--use-auto-ext', '--auto-ext',
                     action="store_true",
                     dest='use_auto_ext',
                     default=False,
                     help="""Using this enables Chrome's Automation Extension.
                          It's not required, but some commands & advanced
                          features may need it.""")
    parser.addoption('--no_sandbox', '--no-sandbox',
                     action="store_true",
                     dest='no_sandbox',
                     default=False,
                     help="""Using this enables the "No Sandbox" feature.
                          (This setting is now always enabled by default.)""")
    parser.addoption('--disable_gpu', '--disable-gpu',
                     action="store_true",
                     dest='disable_gpu',
                     default=False,
                     help="""Using this enables the "Disable GPU" feature.
                          (This setting is now always enabled by default.)""")
    parser.addoption('--swiftshader',
                     action="store_true",
                     dest='swiftshader',
                     default=False,
                     help="""Using this enables the "--use-gl=swiftshader"
                          feature when running tests on Chrome.""")
    parser.addoption('--incognito', '--incognito_mode', '--incognito-mode',
                     action="store_true",
                     dest='incognito',
                     default=False,
                     help="""Using this enables Chrome's Incognito mode.""")
    parser.addoption('--guest', '--guest_mode', '--guest-mode',
                     action="store_true",
                     dest='guest_mode',
                     default=False,
                     help="""Using this enables Chrome's Guest mode.""")
    parser.addoption('--devtools', '--open_devtools', '--open-devtools',
                     action="store_true",
                     dest='devtools',
                     default=False,
                     help="""Using this opens Chrome's DevTools.""")
    parser.addoption('--rs', '--reuse_session', '--reuse-session',
                     action="store_true",
                     dest='reuse_session',
                     default=False,
                     help="""The option to reuse the selenium browser window
                          session between tests.""")
    parser.addoption('--crumbs',
                     action="store_true",
                     dest='crumbs',
                     default=False,
                     help="""The option to delete all cookies between tests
                          that reuse the same browser session. This option
                          is only needed when using "--reuse-session".""")
    parser.addoption('--maximize_window', '--maximize-window', '--maximize',
                     '--fullscreen',
                     action="store_true",
                     dest='maximize_option',
                     default=False,
                     help="""The option to start with the browser window
                          maximized.""")
    parser.addoption('--save_screenshot', '--save-screenshot',
                     action='store_true',
                     dest='save_screenshot',
                     default=False,
                     help="""Take a screenshot on last page after the last step
                          of the test. (Added to the "latest_logs" folder.)""")
    parser.addoption('--visual_baseline', '--visual-baseline',
                     action='store_true',
                     dest='visual_baseline',
                     default=False,
                     help="""Setting this resets the visual baseline for
                          Automated Visual Testing with SeleniumBase.
                          When a test calls self.check_window(), it will
                          rebuild its files in the visual_baseline folder.""")
    parser.addoption('--timeout_multiplier', '--timeout-multiplier',
                     action='store',
                     dest='timeout_multiplier',
                     default=None,
                     help="""Setting this overrides the default timeout
                          by the multiplier when waiting for page elements.
                          Unused when tests overide the default value.""")
    for arg in sys.argv:
        if "--timeout=" in arg:
            raise Exception(
                "\n\n  Don't use --timeout=s from pytest-timeout! "
                "\n  It's not thread-safe for WebDriver processes! "
                "\n  Use --time-limit=s from SeleniumBase instead!\n")


def pytest_configure(config):
    """ This runs after command line options have been parsed """
    sb_config.is_pytest = True
    sb_config.browser = config.getoption('browser')
    sb_config.data = config.getoption('data')
    sb_config.var1 = config.getoption('var1')
    sb_config.var2 = config.getoption('var2')
    sb_config.var3 = config.getoption('var3')
    sb_config.environment = config.getoption('environment')
    sb_config.with_selenium = config.getoption('with_selenium')
    sb_config.user_agent = config.getoption('user_agent')
    sb_config.mobile_emulator = config.getoption('mobile_emulator')
    sb_config.device_metrics = config.getoption('device_metrics')
    sb_config.headless = config.getoption('headless')
    sb_config.headed = config.getoption('headed')
    sb_config.start_page = config.getoption('start_page')
    sb_config.extension_zip = config.getoption('extension_zip')
    sb_config.extension_dir = config.getoption('extension_dir')
    sb_config.with_testing_base = config.getoption('with_testing_base')
    sb_config.with_db_reporting = config.getoption('with_db_reporting')
    sb_config.with_s3_logging = config.getoption('with_s3_logging')
    sb_config.with_screen_shots = config.getoption('with_screen_shots')
    sb_config.with_basic_test_info = config.getoption('with_basic_test_info')
    sb_config.with_page_source = config.getoption('with_page_source')
    sb_config.servername = config.getoption('servername')
    sb_config.port = config.getoption('port')
    sb_config.proxy_string = config.getoption('proxy_string')
    sb_config.cap_file = config.getoption('cap_file')
    sb_config.cap_string = config.getoption('cap_string')
    sb_config.settings_file = config.getoption('settings_file')
    sb_config.user_data_dir = config.getoption('user_data_dir')
    sb_config.database_env = config.getoption('database_env')
    sb_config.log_path = 'latest_logs/'  # (No longer editable!)
    sb_config.archive_logs = config.getoption('archive_logs')
    sb_config._time_limit = config.getoption('time_limit')
    sb_config.time_limit = config.getoption('time_limit')
    sb_config.slow_mode = config.getoption('slow_mode')
    sb_config.demo_mode = config.getoption('demo_mode')
    sb_config.demo_sleep = config.getoption('demo_sleep')
    sb_config.highlights = config.getoption('highlights')
    sb_config.message_duration = config.getoption('message_duration')
    sb_config.js_checking_on = config.getoption('js_checking_on')
    sb_config.ad_block_on = config.getoption('ad_block_on')
    sb_config.block_images = config.getoption('block_images')
    sb_config.verify_delay = config.getoption('verify_delay')
    sb_config.disable_csp = config.getoption('disable_csp')
    sb_config.enable_sync = config.getoption('enable_sync')
    sb_config.use_auto_ext = config.getoption('use_auto_ext')
    sb_config.no_sandbox = config.getoption('no_sandbox')
    sb_config.disable_gpu = config.getoption('disable_gpu')
    sb_config.swiftshader = config.getoption('swiftshader')
    sb_config.incognito = config.getoption('incognito')
    sb_config.guest_mode = config.getoption('guest_mode')
    sb_config.devtools = config.getoption('devtools')
    sb_config.reuse_session = config.getoption('reuse_session')
    sb_config.crumbs = config.getoption('crumbs')
    sb_config.shared_driver = None  # The default driver for session reuse
    sb_config.maximize_option = config.getoption('maximize_option')
    sb_config.save_screenshot = config.getoption('save_screenshot')
    sb_config.visual_baseline = config.getoption('visual_baseline')
    sb_config.timeout_multiplier = config.getoption('timeout_multiplier')
    sb_config.pytest_html_report = config.getoption('htmlpath')  # --html=FILE

    if sb_config.reuse_session:
        arg_join = " ".join(sys.argv)
        if ("-n" in sys.argv) or ("-n=" in arg_join) or (arg_join == "-c"):
            # sb_config.reuse_session = False
            pass  # Allow multithreaded browser sessions to be reused now

    if "linux" in sys.platform and (
            not sb_config.headed and not sb_config.headless):
        print(
            "(Running with --headless on Linux. "
            "Use --headed or --gui to override.)")
        sb_config.headless = True
    if not sb_config.headless:
        sb_config.headed = True

    if sb_config.with_testing_base:
        log_helper.log_folder_setup(sb_config.log_path, sb_config.archive_logs)
    proxy_helper.remove_proxy_zip_if_present()


def pytest_unconfigure():
    """ This runs after all tests have completed with pytest. """
    proxy_helper.remove_proxy_zip_if_present()
    if sb_config.reuse_session:
        # Close the shared browser session
        if sb_config.shared_driver:
            try:
                sb_config.shared_driver.quit()
            except AttributeError:
                pass
            except Exception:
                pass
        sb_config.shared_driver = None
    log_helper.archive_logs_if_set(sb_config.log_path, sb_config.archive_logs)


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


@pytest.fixture()
def sb(request):
    """ SeleniumBase as a pytest fixture.
        Usage example: "def test_one(sb):"
        You'll need to use this for tests that use other pytest fixtures. """
    from seleniumbase import BaseCase

    class BaseClass(BaseCase):
        def base_method():
            pass

    if request.cls:
        request.cls.sb = BaseClass("base_method")
        request.cls.sb.setUp()
        yield request.cls.sb
        request.cls.sb.tearDown()
    else:
        sb = BaseClass("base_method")
        sb.setUp()
        yield sb
        sb.tearDown()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    if pytest_html and report.when == 'call':
        try:
            extra_report = item._testcase._html_report_extra
            extra = getattr(report, 'extra', [])
            if extra_report[1]["content"]:
                report.extra = extra + extra_report
        except Exception:
            pass
