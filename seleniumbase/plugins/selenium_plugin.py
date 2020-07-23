# -*- coding: utf-8 -*-
""" This is the nosetests Selenium plugin for test configuration. """

import sys
from nose.plugins import Plugin
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants


class SeleniumBrowser(Plugin):
    """
    This parser plugin includes the following command-line options for Nose:
    --browser=BROWSER  (The web browser to use.)
    --cap-file=FILE  (The web browser's desired capabilities to use.)
    --cap-string=STRING  (The web browser's desired capabilities to use.)
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
    --maximize-window  (The option to start with the web browser maximized.)
    --save-screenshot  (The option to save a screenshot after each test.)
    --visual-baseline  (Set the visual baseline for Visual/Layout tests.)
    --timeout-multiplier=MULTIPLIER  (Multiplies the default timeout values.)
    """
    name = 'selenium'  # Usage: --with-selenium

    def options(self, parser, env):
        super(SeleniumBrowser, self).options(parser, env=env)

        parser.add_option(
            '--browser',
            action='store',
            dest='browser',
            choices=constants.ValidBrowsers.valid_browsers,
            default=constants.Browser.GOOGLE_CHROME,
            help="""Specifies the web browser to use. Default: Chrome.
                    If you want to use Firefox, explicitly indicate that.
                    Example: (--browser=firefox)""")
        parser.add_option(
            '--browser_version', '--browser-version',
            action='store',
            dest='browser_version',
            default="latest",
            help="""The browser version to use. Explicitly select
                    a version number or use "latest".""")
        parser.add_option(
            '--cap_file', '--cap-file',
            action='store',
            dest='cap_file',
            default=None,
            help="""The file that stores browser desired capabilities
                    for BrowserStack or Sauce Labs web drivers.""")
        parser.add_option(
            '--cap_string', '--cap-string',
            dest='cap_string',
            default=None,
            help="""The string that stores browser desired
                    capabilities for BrowserStack, Sauce Labs,
                    and other remote web drivers to use.
                    Enclose cap-string in single quotes.
                    Enclose parameter keys in double quotes.
                    Example: --cap-string='{"name":"test1","v":"42"}'""")
        parser.add_option(
            '--user_data_dir', '--user-data-dir',
            action='store',
            dest='user_data_dir',
            default=None,
            help="""The Chrome User Data Directory to use. (Chrome Profile)
                    If the directory doesn't exist, it'll be created.""")
        parser.add_option(
            '--server',
            action='store',
            dest='servername',
            default='localhost',
            help="""Designates the Selenium Grid server to use.
                    Use "127.0.0.1" to connect to a localhost Grid.
                    If unset or set to "localhost", Grid isn't used.
                    Default: "localhost".""")
        parser.add_option(
            '--port',
            action='store',
            dest='port',
            default='4444',
            help="""Designates the Selenium Grid port to use.
                    Default: 4444.""")
        parser.add_option(
            '--proxy',
            action='store',
            dest='proxy_string',
            default=None,
            help="""Designates the proxy server:port to use.
                    Format: servername:port.  OR
                            username:password@servername:port  OR
                            A dict key from proxy_list.PROXY_LIST
                    Default: None.""")
        parser.add_option(
            '--agent', '--user-agent', '--user_agent',
            action='store',
            dest='user_agent',
            default=None,
            help="""Designates the User-Agent for the browser to use.
                    Format: A string.
                    Default: None.""")
        parser.add_option(
            '--mobile', '--mobile-emulator', '--mobile_emulator',
            action="store_true",
            dest='mobile_emulator',
            default=False,
            help="""If this option is enabled, the mobile emulator
                    will be used while running tests.""")
        parser.add_option(
            '--metrics', '--device-metrics', '--device_metrics',
            action='store',
            dest='device_metrics',
            default=None,
            help="""Designates the three device metrics of the mobile
                    emulator: CSS Width, CSS Height, and Pixel-Ratio.
                    Format: A comma-separated string with the 3 values.
                    Example: "375,734,3"
                    Default: None. (Will use default values if None)""")
        parser.add_option(
            '--extension_zip', '--extension-zip', '--crx',
            action='store',
            dest='extension_zip',
            default=None,
            help="""Designates the Chrome Extension ZIP file to load.
                    Format: A comma-separated list of .zip or .crx files
                    containing the Chrome extensions to load.
                    Default: None.""")
        parser.add_option(
            '--extension_dir', '--extension-dir',
            action='store',
            dest='extension_dir',
            default=None,
            help="""Designates the Chrome Extension folder to load.
                    Format: A directory containing the Chrome extension.
                    (Can also be a comma-separated list of directories.)
                    Default: None.""")
        parser.add_option(
            '--headless',
            action="store_true",
            dest='headless',
            default=False,
            help="""Using this makes Webdriver run web browsers headlessly,
                    which is required on headless machines.
                    Default: False on Mac/Windows. True on Linux.""")
        parser.add_option(
            '--headed', '--gui',
            action="store_true",
            dest='headed',
            default=False,
            help="""Using this makes Webdriver run web browsers with
                    a GUI when running tests on Linux machines.
                    (The default setting on Linux is headless.)
                    (The default setting on Mac or Windows is headed.)""")
        parser.add_option(
            '--start_page', '--start-page', '--url',
            action='store',
            dest='start_page',
            default=None,
            help="""Designates the starting URL for the web browser
                    when each test begins.
                    Default: None.""")
        parser.add_option(
            '--time_limit', '--time-limit', '--timelimit',
            action='store',
            dest='time_limit',
            default=None,
            help="""Use this to set a time limit per test, in seconds.
                    If a test runs beyond the limit, it fails.""")
        parser.add_option(
            '--slow_mode', '--slow-mode', '--slow',
            action="store_true",
            dest='slow_mode',
            default=False,
            help="""Using this slows down the automation.""")
        parser.add_option(
            '--demo_mode', '--demo-mode', '--demo',
            action="store_true",
            dest='demo_mode',
            default=False,
            help="""Using this slows down the automation and lets you
                    visually see what the tests are actually doing.""")
        parser.add_option(
            '--demo_sleep', '--demo-sleep',
            action='store',
            dest='demo_sleep',
            default=None,
            help="""Setting this overrides the Demo Mode sleep
                    time that happens after browser actions.""")
        parser.add_option(
            '--highlights',
            action='store',
            dest='highlights',
            default=None,
            help="""Setting this overrides the default number of
                    highlight animation loops to have per call.""")
        parser.add_option(
            '--message_duration', '--message-duration',
            action="store",
            dest='message_duration',
            default=None,
            help="""Setting this overrides the default time that
                    messenger notifications remain visible when reaching
                    assert statements during Demo Mode.""")
        parser.add_option(
            '--check_js', '--check-js',
            action="store_true",
            dest='js_checking_on',
            default=False,
            help="""The option to check for JavaScript errors after
                    every page load.""")
        parser.add_option(
            '--ad_block', '--ad-block', '--block_ads', '--block-ads',
            action="store_true",
            dest='ad_block_on',
            default=False,
            help="""Using this makes WebDriver block display ads
                    that are defined in ad_block_list.AD_BLOCK_LIST.""")
        parser.add_option(
            '--block_images', '--block-images',
            action="store_true",
            dest='block_images',
            default=False,
            help="""Using this makes WebDriver block images from
                    loading on web pages during tests.""")
        parser.add_option(
            '--verify_delay', '--verify-delay',
            action='store',
            dest='verify_delay',
            default=None,
            help="""Setting this overrides the default wait time
                    before each MasterQA verification pop-up.""")
        parser.add_option(
            '--disable_csp', '--disable-csp',
            action="store_true",
            dest='disable_csp',
            default=False,
            help="""Using this disables the Content Security Policy of
                    websites, which may interfere with some features of
                    SeleniumBase, such as loading custom JavaScript
                    libraries for various testing actions.
                    Setting this to True (--disable_csp) overrides the
                    value set in seleniumbase/config/settings.py""")
        parser.add_option(
            '--enable_sync', '--enable-sync',
            action="store_true",
            dest='enable_sync',
            default=False,
            help="""Using this enables the "Chrome Sync" feature.""")
        parser.add_option(
            '--use_auto_ext', '--use-auto-ext', '--auto-ext',
            action="store_true",
            dest='use_auto_ext',
            default=False,
            help="""Using this enables Chrome's Automation Extension.
                    It's not required, but some commands & advanced
                    features may need it.""")
        parser.add_option(
            '--no_sandbox', '--no-sandbox',
            action="store_true",
            dest='no_sandbox',
            default=False,
            help="""Using this enables the "No Sandbox" feature.
                    (This setting is now always enabled by default.)""")
        parser.add_option(
            '--disable_gpu', '--disable-gpu',
            action="store_true",
            dest='disable_gpu',
            default=False,
            help="""Using this enables the "Disable GPU" feature.
                    (This setting is now always enabled by default.)""")
        parser.add_option(
            '--swiftshader',
            action="store_true",
            dest='swiftshader',
            default=False,
            help="""Using this enables the "--use-gl=swiftshader"
                    feature when running tests on Chrome.""")
        parser.add_option(
            '--incognito', '--incognito_mode', '--incognito-mode',
            action="store_true",
            dest='incognito',
            default=False,
            help="""Using this enables Chrome's Incognito mode.""")
        parser.add_option(
            '--guest', '--guest_mode', '--guest-mode',
            action="store_true",
            dest='guest_mode',
            default=False,
            help="""Using this enables Chrome's Guest mode.""")
        parser.add_option(
            '--devtools', '--open_devtools', '--open-devtools',
            action="store_true",
            dest='devtools',
            default=False,
            help="""Using this opens Chrome's DevTools.""")
        parser.add_option(
            '--maximize_window', '--maximize-window', '--maximize',
            '--fullscreen',
            action="store_true",
            dest='maximize_option',
            default=False,
            help="""The option to start with the web browser maximized.""")
        parser.add_option(
            '--save_screenshot', '--save-screenshot',
            action="store_true",
            dest='save_screenshot',
            default=False,
            help="""Take a screenshot on last page after the last step
                    of the test. (Added to the "latest_logs" folder.)""")
        parser.add_option(
            '--visual_baseline', '--visual-baseline',
            action='store_true',
            dest='visual_baseline',
            default=False,
            help="""Setting this resets the visual baseline for
                    Automated Visual Testing with SeleniumBase.
                    When a test calls self.check_window(), it will
                    rebuild its files in the visual_baseline folder.""")
        parser.add_option(
            '--timeout_multiplier', '--timeout-multiplier',
            action='store',
            dest='timeout_multiplier',
            default=None,
            help="""Setting this overrides the default timeout
                    by the multiplier when waiting for page elements.
                    Unused when tests overide the default value.""")

    def configure(self, options, conf):
        super(SeleniumBrowser, self).configure(options, conf)
        self.enabled = True  # Used if test class inherits BaseCase
        self.options = options
        self.headless_active = False  # Default setting
        proxy_helper.remove_proxy_zip_if_present()

    def beforeTest(self, test):
        test.test.browser = self.options.browser
        test.test.cap_file = self.options.cap_file
        test.test.cap_string = self.options.cap_string
        test.test.headless = self.options.headless
        test.test.headed = self.options.headed
        test.test.start_page = self.options.start_page
        test.test.servername = self.options.servername
        test.test.port = self.options.port
        test.test.user_data_dir = self.options.user_data_dir
        test.test.extension_zip = self.options.extension_zip
        test.test.extension_dir = self.options.extension_dir
        test.test.proxy_string = self.options.proxy_string
        test.test.user_agent = self.options.user_agent
        test.test.mobile_emulator = self.options.mobile_emulator
        test.test.device_metrics = self.options.device_metrics
        test.test.time_limit = self.options.time_limit
        test.test.slow_mode = self.options.slow_mode
        test.test.demo_mode = self.options.demo_mode
        test.test.demo_sleep = self.options.demo_sleep
        test.test.highlights = self.options.highlights
        test.test.message_duration = self.options.message_duration
        test.test.js_checking_on = self.options.js_checking_on
        test.test.ad_block_on = self.options.ad_block_on
        test.test.block_images = self.options.block_images
        test.test.verify_delay = self.options.verify_delay  # MasterQA
        test.test.disable_csp = self.options.disable_csp
        test.test.enable_sync = self.options.enable_sync
        test.test.use_auto_ext = self.options.use_auto_ext
        test.test.no_sandbox = self.options.no_sandbox
        test.test.disable_gpu = self.options.disable_gpu
        test.test.swiftshader = self.options.swiftshader
        test.test.incognito = self.options.incognito
        test.test.guest_mode = self.options.guest_mode
        test.test.devtools = self.options.devtools
        test.test.maximize_option = self.options.maximize_option
        test.test.save_screenshot_after_test = self.options.save_screenshot
        test.test.visual_baseline = self.options.visual_baseline
        test.test.timeout_multiplier = self.options.timeout_multiplier
        test.test.use_grid = False
        test.test._reuse_session = False
        if test.test.servername != "localhost":
            # Use Selenium Grid (Use --server="127.0.0.1" for localhost Grid)
            test.test.use_grid = True
        if "linux" in sys.platform and (
                not self.options.headed and not self.options.headless):
            print(
                "(Running with --headless on Linux. "
                "Use --headed or --gui to override.)")
            self.options.headless = True
            test.test.headless = True
        if not self.options.headless:
            self.options.headed = True
            test.test.headed = True
        if self.options.headless:
            try:
                # from pyvirtualdisplay import Display  # Skip for own lib
                from seleniumbase.virtual_display.display import Display
                self.display = Display(visible=0, size=(1440, 1880))
                self.display.start()
                self.headless_active = True
            except Exception:
                # pyvirtualdisplay might not be necessary anymore because
                # Chrome and Firefox now have built-in headless displays
                pass
        # The driver will be received later
        self.driver = None
        test.test.driver = self.driver

    def finalize(self, result):
        """ This runs after all tests have completed with nosetests. """
        proxy_helper.remove_proxy_zip_if_present()

    def afterTest(self, test):
        try:
            # If the browser window is still open, close it now.
            self.driver.quit()
        except AttributeError:
            pass
        except Exception:
            pass
        if self.options.headless:
            if self.headless_active:
                try:
                    self.display.stop()
                except AttributeError:
                    pass
                except Exception:
                    pass
