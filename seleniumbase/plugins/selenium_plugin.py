# -*- coding: utf-8 -*-
"""
This is the Nosetest plugin for setting Selenium test configuration.
"""

import sys
from nose.plugins import Plugin
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants

is_windows = False
if sys.platform in ["win32", "win64", "x64"]:
    is_windows = True


class SeleniumBrowser(Plugin):
    """
    This plugin adds the following command-line options to nosetests:
    --browser=BROWSER  (The web browser to use. Default: "chrome".)
    --user-data-dir=DIR  (Set the Chrome user data directory to use.)
    --protocol=PROTOCOL  (The Selenium Grid protocol: http|https.)
    --server=SERVER  (The Selenium Grid server/IP used for tests.)
    --port=PORT  (The Selenium Grid port used by the test server.)
    --cap-file=FILE  (The web browser's desired capabilities to use.)
    --cap-string=STRING  (The web browser's desired capabilities to use.)
    --proxy=SERVER:PORT  (Connect to a proxy server:port for tests.)
    --proxy=USERNAME:PASSWORD@SERVER:PORT  (Use authenticated proxy server.)
    --proxy-bypass-list=STRING (";"-separated hosts to bypass, Eg "*.foo.com")
    --proxy-pac-url=URL  (Connect to a proxy server using a PAC_URL.pac file.)
    --proxy-pac-url=USERNAME:PASSWORD@URL  (Authenticated proxy with PAC URL.)
    --agent=STRING  (Modify the web browser's User-Agent string.)
    --mobile  (Use the mobile device emulator while running tests.)
    --metrics=STRING  (Set mobile metrics: "CSSWidth,CSSHeight,PixelRatio".)
    --chromium-arg="ARG=N,ARG2" (Set Chromium args, ","-separated, no spaces.)
    --firefox-arg="ARG=N,ARG2" (Set Firefox args, comma-separated, no spaces.)
    --firefox-pref=SET  (Set a Firefox preference:value set, comma-separated.)
    --extension-zip=ZIP  (Load a Chrome Extension .zip|.crx, comma-separated.)
    --extension-dir=DIR  (Load a Chrome Extension directory, comma-separated.)
    --sjw  (Skip JS Waits for readyState to be "complete" or Angular to load.)
    --pls=PLS  (Set pageLoadStrategy on Chrome: "normal", "eager", or "none".)
    --headless  (Run tests in headless mode. The default arg on Linux OS.)
    --headless2  (Use the new headless mode, which supports extensions.)
    --headed  (Run tests in headed/GUI mode on Linux OS, where not default.)
    --xvfb  (Run tests using the Xvfb virtual display server on Linux OS.)
    --locale=LOCALE_CODE  (Set the Language Locale Code for the web browser.)
    --interval=SECONDS  (The autoplay interval for presentations & tour steps)
    --start-page=URL  (The starting URL for the web browser when tests begin.)
    --time-limit=SECONDS  (Safely fail any test that exceeds the time limit.)
    --slow  (Slow down the automation. Faster than using Demo Mode.)
    --demo  (Slow down and visually see test actions as they occur.)
    --demo-sleep=SECONDS  (Set the wait time after Slow & Demo Mode actions.)
    --highlights=NUM  (Number of highlight animations for Demo Mode actions.)
    --message-duration=SECONDS  (The time length for Messenger alerts.)
    --check-js  (Check for JavaScript errors after page loads.)
    --ad-block  (Block some types of display ads from loading.)
    --block-images  (Block images from loading during tests.)
    --do-not-track  (Indicate to websites that you don't want to be tracked.)
    --verify-delay=SECONDS  (The delay before MasterQA verification checks.)
    --recorder  (Enables the Recorder for turning browser actions into code.)
    --rec-behave  (Same as Recorder Mode, but also generates behave-gherkin.)
    --rec-sleep  (If the Recorder is enabled, also records self.sleep calls.)
    --rec-print  (If the Recorder is enabled, prints output after tests end.)
    --disable-js  (Disable JavaScript on websites. Pages might break!)
    --disable-csp  (Disable the Content Security Policy of websites.)
    --disable-ws  (Disable Web Security on Chromium-based browsers.)
    --enable-ws  (Enable Web Security on Chromium-based browsers.)
    --enable-sync  (Enable "Chrome Sync" on websites.)
    --use-auto-ext  (Use Chrome's automation extension.)
    --uc | --undetected  (Use undetected-chromedriver to evade bot-detection.)
    --uc-sub | --uc-subprocess  (Use undetected-chromedriver as a subprocess.)
    --remote-debug  (Enable Chrome's Remote Debugger on http://localhost:9222)
    --final-debug  (Enter Debug Mode after each test ends. Don't use with CI!)
    --swiftshader  (Use Chrome's "--use-gl=swiftshader" feature.)
    --incognito  (Enable Chrome's Incognito mode.)
    --guest  (Enable Chrome's Guest mode.)
    --devtools  (Open Chrome's DevTools when the browser opens.)
    --disable-beforeunload  (Disable the "beforeunload" event on Chrome.)
    --window-size=WIDTH,HEIGHT  (Set the browser's starting window size.)
    --maximize  (Start tests with the browser window maximized.)
    --screenshot  (Save a screenshot at the end of each test.)
    --visual-baseline  (Set the visual baseline for Visual/Layout tests.)
    --external-pdf (Set Chromium "plugins.always_open_pdf_externally": True.)
    --timeout-multiplier=MULTIPLIER  (Multiplies the default timeout values.)
    """

    name = "selenium"  # Usage: --with-selenium

    def options(self, parser, env):
        super(SeleniumBrowser, self).options(parser, env=env)

        parser.add_option(
            "--browser",
            action="store",
            dest="browser",
            choices=constants.ValidBrowsers.valid_browsers,
            default=constants.Browser.GOOGLE_CHROME,
            help="""Specifies the web browser to use. Default: Chrome.
                    If you want to use Firefox, explicitly indicate that.
                    Example: (--browser=firefox)""",
        )
        parser.add_option(
            "--browser_version",
            "--browser-version",
            action="store",
            dest="browser_version",
            default="latest",
            help="""The browser version to use. Explicitly select
                    a version number or use "latest".""",
        )
        parser.add_option(
            "--cap_file",
            "--cap-file",
            action="store",
            dest="cap_file",
            default=None,
            help="""The file that stores browser desired capabilities
                    for BrowserStack, LambdaTest, Sauce Labs,
                    and other remote web drivers to use.""",
        )
        parser.add_option(
            "--cap_string",
            "--cap-string",
            dest="cap_string",
            default=None,
            help="""The string that stores browser desired capabilities
                    for BrowserStack, LambdaTest, Sauce Labs,
                    and other remote web drivers to use.
                    Enclose cap-string in single quotes.
                    Enclose parameter keys in double quotes.
                    Example: --cap-string='{"name":"test1","v":"42"}'""",
        )
        parser.add_option(
            "--user_data_dir",
            "--user-data-dir",
            action="store",
            dest="user_data_dir",
            default=None,
            help="""The Chrome User Data Directory to use. (Chrome Profile)
                    If the directory doesn't exist, it'll be created.""",
        )
        parser.add_option(
            "--sjw",
            "--skip_js_waits",
            "--skip-js-waits",
            action="store_true",
            dest="skip_js_waits",
            default=False,
            help="""Skip all calls to wait_for_ready_state_complete()
                    and wait_for_angularjs(), which are part of many
                    SeleniumBase methods for improving reliability.""",
        )
        parser.add_option(
            "--protocol",
            action="store",
            dest="protocol",
            choices=(
                constants.Protocol.HTTP,
                constants.Protocol.HTTPS,
            ),
            default=constants.Protocol.HTTP,
            help="""Designates the Selenium Grid protocol to use.
                    Default: http.""",
        )
        parser.add_option(
            "--server",
            action="store",
            dest="servername",
            default="localhost",
            help="""Designates the Selenium Grid server to use.
                    Use "127.0.0.1" to connect to a localhost Grid.
                    If unset or set to "localhost", Grid isn't used.
                    Default: "localhost".""",
        )
        parser.add_option(
            "--port",
            action="store",
            dest="port",
            default="4444",
            help="""Designates the Selenium Grid port to use.
                    Default: 4444. (If 443, protocol becomes "https")""",
        )
        parser.add_option(
            "--proxy",
            "--proxy-server",
            "--proxy-string",
            action="store",
            dest="proxy_string",
            default=None,
            help="""Designates the proxy server:port to use.
                    Format: servername:port.  OR
                            username:password@servername:port  OR
                            A dict key from proxy_list.PROXY_LIST
                    Default: None.""",
        )
        parser.add_option(
            "--proxy-bypass-list",
            "--proxy_bypass_list",
            action="store",
            dest="proxy_bypass_list",
            default=None,
            help="""Designates the hosts, domains, and/or IP addresses
                    to bypass when using a proxy server with "--proxy".
                    Format: A ";"-separated string.
                    Example usage:
                        pytest
                            --proxy="username:password@servername:port"
                            --proxy-bypass-list="*.foo.com;github.com"
                        pytest
                            --proxy="servername:port"
                            --proxy-bypass-list="127.0.0.1:8080"
                    Default: None.""",
        )
        parser.add_option(
            "--proxy-pac-url",
            "--pac-url",
            action="store",
            dest="proxy_pac_url",
            default=None,
            help="""Designates the proxy PAC URL to use.
                    Format: A URL string  OR
                            A username:password@URL string
                    Default: None.""",
        )
        parser.add_option(
            "--agent",
            "--user-agent",
            "--user_agent",
            action="store",
            dest="user_agent",
            default=None,
            help="""Designates the User-Agent for the browser to use.
                    Format: A string.
                    Default: None.""",
        )
        parser.add_option(
            "--mobile",
            "--mobile-emulator",
            "--mobile_emulator",
            action="store_true",
            dest="mobile_emulator",
            default=False,
            help="""If this option is enabled, the mobile emulator
                    will be used while running tests.""",
        )
        parser.add_option(
            "--metrics",
            "--device-metrics",
            "--device_metrics",
            action="store",
            dest="device_metrics",
            default=None,
            help="""Designates the three device metrics of the mobile
                    emulator: CSS Width, CSS Height, and Pixel-Ratio.
                    Format: A comma-separated string with the 3 values.
                    Example: "375,734,3"
                    Default: None. (Will use default values if None)""",
        )
        parser.add_option(
            "--chromium_arg",
            "--chromium-arg",
            action="store",
            dest="chromium_arg",
            default=None,
            help="""Add a Chromium argument for Chrome/Edge browsers.
                    Format: A comma-separated list of Chromium args.
                    If an arg doesn't start with "--", that will be
                    added to the beginning of the arg automatically.
                    Default: None.""",
        )
        parser.add_option(
            "--firefox_arg",
            "--firefox-arg",
            action="store",
            dest="firefox_arg",
            default=None,
            help="""Add a Firefox argument for Firefox browser runs.
                    Format: A comma-separated list of Firefox args.
                    If an arg doesn't start with "--", that will be
                    added to the beginning of the arg automatically.
                    Default: None.""",
        )
        parser.add_option(
            "--firefox_pref",
            "--firefox-pref",
            action="store",
            dest="firefox_pref",
            default=None,
            help="""Set a Firefox preference:value combination.
                    Format: A comma-separated list of pref:value items.
                    Example usage:
                        --firefox-pref="browser.formfill.enable:True"
                        --firefox-pref="pdfjs.disabled:False"
                        --firefox-pref="abc.def.xyz:42,hello.world:text"
                    Boolean and integer values to the right of the ":"
                    will be automatically converted into proper format.
                    If there's no ":" in the string, then True is used.
                    Default: None.""",
        )
        parser.add_option(
            "--extension_zip",
            "--extension-zip",
            "--crx",
            action="store",
            dest="extension_zip",
            default=None,
            help="""Designates the Chrome Extension ZIP file to load.
                    Format: A comma-separated list of .zip or .crx files
                    containing the Chrome extensions to load.
                    Default: None.""",
        )
        parser.add_option(
            "--extension_dir",
            "--extension-dir",
            action="store",
            dest="extension_dir",
            default=None,
            help="""Designates the Chrome Extension folder to load.
                    Format: A directory containing the Chrome extension.
                    (Can also be a comma-separated list of directories.)
                    Default: None.""",
        )
        parser.add_option(
            "--pls",
            "--page_load_strategy",
            "--page-load-strategy",
            action="store",
            dest="page_load_strategy",
            choices=(
                constants.PageLoadStrategy.NORMAL,
                constants.PageLoadStrategy.EAGER,
                constants.PageLoadStrategy.NONE,
            ),
            default=None,
            help="""This option sets Chrome's pageLoadStrategy.
                    List of choices: "normal", "eager", "none".""",
        )
        parser.add_option(
            "--headless",
            action="store_true",
            dest="headless",
            default=False,
            help="""Using this option activates headless mode,
                which is required on headless machines
                UNLESS using a virtual display with Xvfb.
                Default: False on Mac/Windows. True on Linux.""",
        )
        parser.add_option(
            "--headless2",
            action="store_true",
            dest="headless2",
            default=False,
            help="""This option activates the new headless mode,
                    which supports Chromium extensions, and more,
                    but is slower than the standard headless mode.""",
        )
        parser.add_option(
            "--headed",
            "--gui",
            action="store_true",
            dest="headed",
            default=False,
            help="""Using this makes Webdriver run web browsers with
                    a GUI when running tests on Linux machines.
                    (The default setting on Linux is headless.)
                    (The default setting on Mac or Windows is headed.)""",
        )
        parser.add_option(
            "--xvfb",
            action="store_true",
            dest="xvfb",
            default=False,
            help="""Using this makes tests run headlessly using Xvfb
                    instead of the browser's built-in headless mode.
                    When using "--xvfb", the "--headless" option
                    will no longer be enabled by default on Linux.
                    Default: False. (Linux-ONLY!)""",
        )
        parser.add_option(
            "--locale_code",
            "--locale-code",
            "--locale",
            action="store",
            dest="locale_code",
            default=None,
            help="""Designates the Locale Code for the web browser.
                    A Locale is a specific version of a spoken Language.
                    The Locale alters visible text on supported websites.
                    See: https://seleniumbase.io/help_docs/locale_codes/
                    Default: None. (The web browser's default mode.)""",
        )
        parser.add_option(
            "--interval",
            action="store",
            dest="interval",
            default=None,
            help="""This globally overrides the default interval,
                    (in seconds), of features that include autoplay
                    functionality, such as tours and presentations.
                    Overrides from methods take priority over this.
                    (Headless Mode skips tours and presentations.)""",
        )
        parser.add_option(
            "--start_page",
            "--start-page",
            "--url",
            action="store",
            dest="start_page",
            default=None,
            help="""Designates the starting URL for the web browser
                    when each test begins.
                    Default: None.""",
        )
        parser.add_option(
            "--time_limit",
            "--time-limit",
            "--timelimit",
            action="store",
            dest="time_limit",
            default=None,
            help="""Use this to set a time limit per test, in seconds.
                    If a test runs beyond the limit, it fails.""",
        )
        parser.add_option(
            "--slow_mode",
            "--slow-mode",
            "--slowmo",
            "--slow",
            action="store_true",
            dest="slow_mode",
            default=False,
            help="""Using this slows down the automation.""",
        )
        parser.add_option(
            "--demo_mode",
            "--demo-mode",
            "--demo",
            action="store_true",
            dest="demo_mode",
            default=False,
            help="""Using this slows down the automation and lets you
                    visually see what the tests are actually doing.""",
        )
        parser.add_option(
            "--demo_sleep",
            "--demo-sleep",
            action="store",
            dest="demo_sleep",
            default=None,
            help="""Setting this overrides the Demo Mode sleep
                    time that happens after browser actions.""",
        )
        parser.add_option(
            "--highlights",
            action="store",
            dest="highlights",
            default=None,
            help="""Setting this overrides the default number of
                    highlight animation loops to have per call.""",
        )
        parser.add_option(
            "--message_duration",
            "--message-duration",
            action="store",
            dest="message_duration",
            default=None,
            help="""Setting this overrides the default time that
                    messenger notifications remain visible when reaching
                    assert statements during Demo Mode.""",
        )
        parser.add_option(
            "--check_js",
            "--check-js",
            action="store_true",
            dest="js_checking_on",
            default=False,
            help="""The option to check for JavaScript errors after
                    every page load.""",
        )
        parser.add_option(
            "--adblock",
            "--ad_block",
            "--ad-block",
            "--block_ads",
            "--block-ads",
            action="store_true",
            dest="ad_block_on",
            default=False,
            help="""Using this makes WebDriver block display ads
                    that are defined in ad_block_list.AD_BLOCK_LIST.""",
        )
        parser.add_option(
            "--block_images",
            "--block-images",
            action="store_true",
            dest="block_images",
            default=False,
            help="""Using this makes WebDriver block images from
                    loading on web pages during tests.""",
        )
        parser.add_option(
            "--do_not_track",
            "--do-not-track",
            action="store_true",
            dest="do_not_track",
            default=False,
            help="""Indicate to websites that you don't want to be
                    tracked. The browser will send an extra HTTP
                    header each time it requests a web page.
                    https://support.google.com/chrome/answer/2790761""",
        )
        parser.add_option(
            "--verify_delay",
            "--verify-delay",
            action="store",
            dest="verify_delay",
            default=None,
            help="""Setting this overrides the default wait time
                    before each MasterQA verification pop-up.""",
        )
        parser.add_option(
            "--recorder",
            "--record",
            "--rec",
            "--codegen",
            action="store_true",
            dest="recorder_mode",
            default=False,
            help="""Using this enables the SeleniumBase Recorder,
                    which records browser actions for converting
                    into SeleniumBase scripts.""",
        )
        parser.add_option(
            "--rec-behave",
            "--rec-gherkin",
            action="store_true",
            dest="rec_behave",
            default=False,
            help="""Not only enables the SeleniumBase Recorder,
                    but also saves recorded actions into the
                    behave-gerkin format, which includes a
                    feature file, an imported steps file,
                    and the environment.py file.""",
        )
        parser.add_option(
            "--rec-sleep",
            "--record-sleep",
            action="store_true",
            dest="record_sleep",
            default=False,
            help="""If Recorder Mode is enabled,
                    records sleep(seconds) calls.""",
        )
        parser.add_option(
            "--rec-print",
            action="store_true",
            dest="rec_print",
            default=False,
            help="""If Recorder Mode is enabled,
                    prints output after tests end.""",
        )
        parser.add_option(
            "--disable_js",
            "--disable-js",
            action="store_true",
            dest="disable_js",
            default=False,
            help="""The option to disable JavaScript on web pages.
                    Warning: Most web pages will stop working!""",
        )
        parser.add_option(
            "--disable_csp",
            "--disable-csp",
            "--no_csp",
            "--no-csp",
            "--dcsp",
            action="store_true",
            dest="disable_csp",
            default=False,
            help="""Using this disables the Content Security Policy of
                    websites, which may interfere with some features of
                    SeleniumBase, such as loading custom JavaScript
                    libraries for various testing actions.
                    Setting this to True (--disable-csp) overrides the
                    value set in seleniumbase/config/settings.py""",
        )
        parser.add_option(
            "--disable_ws",
            "--disable-ws",
            "--disable-web-security",
            action="store_true",
            dest="disable_ws",
            default=False,
            help="""Using this disables the "Web Security" feature of
                    Chrome and Chromium-based browsers such as Edge.""",
        )
        parser.add_option(
            "--enable_ws",
            "--enable-ws",
            "--enable-web-security",
            action="store_true",
            dest="enable_ws",
            default=False,
            help="""Using this enables the "Web Security" feature of
                    Chrome and Chromium-based browsers such as Edge.""",
        )
        parser.add_option(
            "--enable_sync",
            "--enable-sync",
            action="store_true",
            dest="enable_sync",
            default=False,
            help="""Using this enables the "Chrome Sync" feature.""",
        )
        parser.add_option(
            "--use_auto_ext",
            "--use-auto-ext",
            "--auto-ext",
            action="store_true",
            dest="use_auto_ext",
            default=False,
            help="""Using this enables Chrome's Automation Extension.
                    It's not required, but some commands & advanced
                    features may need it.""",
        )
        parser.add_option(
            "--undetected",
            "--undetectable",
            "--uc",  # undetected-chromedriver
            action="store_true",
            dest="undetectable",
            default=False,
            help="""Using this option makes chromedriver undetectable
                    to websites that use anti-bot services to block
                    automation tools from navigating them freely.""",
        )
        parser.add_option(
            "--uc_subprocess",
            "--uc-subprocess",
            "--uc-sub",  # undetected-chromedriver subprocess mode
            action="store_true",
            dest="uc_subprocess",
            default=False,
            help="""Use undetectable-chromedriver as a subprocess,
                    which can help avoid issues that might result.
                    It may reduce UC's ability to avoid detection.""",
        )
        parser.add_option(
            "--no_sandbox",
            "--no-sandbox",
            action="store_true",
            dest="no_sandbox",
            default=False,
            help="""Using this enables the "No Sandbox" feature.
                    (This setting is now always enabled by default.)""",
        )
        parser.add_option(
            "--disable_gpu",
            "--disable-gpu",
            action="store_true",
            dest="disable_gpu",
            default=False,
            help="""Using this enables the "Disable GPU" feature.
                    (This setting is now always enabled by default.)""",
        )
        parser.add_option(
            "--remote_debug",
            "--remote-debug",
            action="store_true",
            dest="remote_debug",
            default=False,
            help="""This enables Chromium's remote debugger.
                    To access the remote debugging interface, go to:
                    http://localhost:9222 while Chromedriver is running.
                    Info: chromedevtools.github.io/devtools-protocol/""",
        )
        parser.add_option(
            "--final-debug",
            action="store_true",
            dest="final_debug",
            default=False,
            help="""Enter Debug Mode at the end of each test.
                    To enter Debug Mode only on failures, use "--pdb".
                    If using both "--final-debug" and "--pdb" together,
                    then Debug Mode will activate twice on failures.""",
        )
        parser.add_option(
            "--swiftshader",
            action="store_true",
            dest="swiftshader",
            default=False,
            help="""Using this enables the "--use-gl=swiftshader"
                    feature when running tests on Chrome.""",
        )
        parser.add_option(
            "--incognito",
            "--incognito_mode",
            "--incognito-mode",
            action="store_true",
            dest="incognito",
            default=False,
            help="""Using this enables Chrome's Incognito mode.""",
        )
        parser.add_option(
            "--guest",
            "--guest_mode",
            "--guest-mode",
            action="store_true",
            dest="guest_mode",
            default=False,
            help="""Using this enables Chrome's Guest mode.""",
        )
        parser.add_option(
            "--devtools",
            "--open_devtools",
            "--open-devtools",
            action="store_true",
            dest="devtools",
            default=False,
            help="""Using this opens Chrome's DevTools.""",
        )
        parser.add_option(
            "--disable-beforeunload",
            "--disable_beforeunload",
            action="store_true",
            dest="_disable_beforeunload",
            default=False,
            help="""The option to disable the "beforeunload" event
                    on Chromium browsers (Chrome or Edge).
                    This is already the default Firefox option.""",
        )
        parser.add_option(
            "--window-size",
            "--window_size",
            action="store",
            dest="window_size",
            default=None,
            help="""The option to set the default window "width,height".
                    Format: A comma-separated string with the 2 values.
                    Example: "1200,800"
                    Default: None. (Will use default values if None)""",
        )
        parser.add_option(
            "--maximize_window",
            "--maximize-window",
            "--maximize",
            "--fullscreen",
            action="store_true",
            dest="maximize_option",
            default=False,
            help="""The option to start with a maximized browser window.
                    (Overrides the "window-size" option if used.)""",
        )
        parser.add_option(
            "--screenshot",
            "--save_screenshot",
            "--save-screenshot",
            "--ss",
            action="store_true",
            dest="save_screenshot",
            default=False,
            help="""Save a screenshot at the end of the test.
                    (Added to the "latest_logs/" folder.)""",
        )
        parser.add_option(
            "--visual_baseline",
            "--visual-baseline",
            action="store_true",
            dest="visual_baseline",
            default=False,
            help="""Setting this resets the visual baseline for
                    Automated Visual Testing with SeleniumBase.
                    When a test calls self.check_window(), it will
                    rebuild its files in the visual_baseline folder.""",
        )
        parser.add_option(
            "--external_pdf",
            "--external-pdf",
            action="store_true",
            dest="external_pdf",
            default=False,
            help="""This option sets the following on Chromium:
                    "plugins.always_open_pdf_externally": True,
                    which causes opened PDF URLs to download immediately,
                    instead of being displayed in the browser window.""",
        )
        parser.add_option(
            "--timeout_multiplier",
            "--timeout-multiplier",
            action="store",
            dest="timeout_multiplier",
            default=None,
            help="""Setting this overrides the default timeout
                    by the multiplier when waiting for page elements.
                    Unused when tests override the default value.""",
        )

    def configure(self, options, conf):
        super(SeleniumBrowser, self).configure(options, conf)
        self.enabled = True  # Used if test class inherits BaseCase
        self.options = options
        self.headless_active = False  # Default setting
        sb_config.headless_active = False
        sb_config.is_nosetest = True
        proxy_helper.remove_proxy_zip_if_present()

    def beforeTest(self, test):
        sb_config._context_of_runner = False  # Context Manager Compatibility
        browser = self.options.browser
        if self.options.recorder_mode and browser not in ["chrome", "edge"]:
            message = (
                "\n\n  Recorder Mode ONLY supports Chrome and Edge!"
                '\n  (Your browser choice was: "%s")\n' % browser
            )
            raise Exception(message)
        window_size = self.options.window_size
        if window_size:
            if window_size.count(",") != 1:
                message = (
                    '\n\n  window_size expects a "width,height" string!'
                    '\n  (Your input was: "%s")\n' % window_size
                )
                raise Exception(message)
            window_size = window_size.replace(" ", "")
            width = None
            height = None
            try:
                width = int(window_size.split(",")[0])
                height = int(window_size.split(",")[1])
            except Exception:
                message = (
                    '\n\n  Expecting integer values for "width,height"!'
                    '\n  (window_size input was: "%s")\n' % window_size
                )
                raise Exception(message)
            settings.CHROME_START_WIDTH = width
            settings.CHROME_START_HEIGHT = height
            settings.HEADLESS_START_WIDTH = width
            settings.HEADLESS_START_HEIGHT = height
        test.test.is_nosetest = True
        test.test.is_behave = False
        test.test.is_pytest = False
        test.test.is_context_manager = False
        sb_config.is_nosetest = True
        sb_config.is_behave = False
        sb_config.is_pytest = False
        sb_config.is_context_manager = False
        test.test.browser = self.options.browser
        test.test.cap_file = self.options.cap_file
        test.test.cap_string = self.options.cap_string
        test.test.headless = self.options.headless
        test.test.headless2 = self.options.headless2
        if test.test.headless2 and test.test.browser == "firefox":
            test.test.headless2 = False  # Only for Chromium browsers
            test.test.headless = True  # Firefox has regular headless
            self.options.headless2 = False
            self.options.headless = True
        elif test.test.browser not in ["chrome", "edge"]:
            test.test.headless2 = False  # Only for Chromium browsers
            self.options.headless2 = False
        test.test.headed = self.options.headed
        test.test.xvfb = self.options.xvfb
        test.test.locale_code = self.options.locale_code
        test.test.interval = self.options.interval
        test.test.start_page = self.options.start_page
        if self.options.skip_js_waits:
            settings.SKIP_JS_WAITS = True
        test.test.protocol = self.options.protocol
        test.test.servername = self.options.servername
        test.test.port = self.options.port
        test.test.user_data_dir = self.options.user_data_dir
        test.test.extension_zip = self.options.extension_zip
        test.test.extension_dir = self.options.extension_dir
        test.test.page_load_strategy = self.options.page_load_strategy
        test.test.chromium_arg = self.options.chromium_arg
        test.test.firefox_arg = self.options.firefox_arg
        test.test.firefox_pref = self.options.firefox_pref
        test.test.proxy_string = self.options.proxy_string
        test.test.proxy_bypass_list = self.options.proxy_bypass_list
        test.test.proxy_pac_url = self.options.proxy_pac_url
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
        test.test.do_not_track = self.options.do_not_track
        test.test.verify_delay = self.options.verify_delay  # MasterQA
        test.test.recorder_mode = self.options.recorder_mode
        test.test.recorder_ext = self.options.recorder_mode  # Again
        test.test.rec_behave = self.options.rec_behave
        test.test.rec_print = self.options.rec_print
        test.test.record_sleep = self.options.record_sleep
        if self.options.rec_print:
            test.test.recorder_mode = True
            test.test.recorder_ext = True
        elif self.options.rec_behave:
            test.test.recorder_mode = True
            test.test.recorder_ext = True
        elif self.options.record_sleep:
            test.test.recorder_mode = True
            test.test.recorder_ext = True
        test.test.disable_js = self.options.disable_js
        test.test.disable_csp = self.options.disable_csp
        test.test.disable_ws = self.options.disable_ws
        test.test.enable_ws = self.options.enable_ws
        if not self.options.disable_ws:
            test.test.enable_ws = True
        test.test.enable_sync = self.options.enable_sync
        test.test.use_auto_ext = self.options.use_auto_ext
        test.test.undetectable = self.options.undetectable
        test.test.uc_subprocess = self.options.uc_subprocess
        if test.test.uc_subprocess and not test.test.undetectable:
            test.test.undetectable = True
        test.test.no_sandbox = self.options.no_sandbox
        test.test.disable_gpu = self.options.disable_gpu
        test.test.remote_debug = self.options.remote_debug
        test.test._final_debug = self.options.final_debug
        test.test.swiftshader = self.options.swiftshader
        test.test.incognito = self.options.incognito
        test.test.guest_mode = self.options.guest_mode
        test.test.devtools = self.options.devtools
        test.test._disable_beforeunload = self.options._disable_beforeunload
        test.test.window_size = self.options.window_size
        test.test.maximize_option = self.options.maximize_option
        test.test.save_screenshot_after_test = self.options.save_screenshot
        test.test.visual_baseline = self.options.visual_baseline
        test.test.external_pdf = self.options.external_pdf
        test.test.timeout_multiplier = self.options.timeout_multiplier
        test.test.dashboard = False
        test.test._multithreaded = False
        test.test._reuse_session = False
        if test.test.servername != "localhost":
            # Using Selenium Grid
            # (Set --server="127.0.0.1" for localhost Grid)
            if str(self.options.port) == "443":
                test.test.protocol = "https"
        if self.options.xvfb and "linux" not in sys.platform:
            # The Xvfb virtual display server is for Linux OS Only!
            self.options.xvfb = False
        if (
            "linux" in sys.platform
            and not self.options.headed
            and not self.options.headless
            and not self.options.headless2
            and not self.options.xvfb
        ):
            print(
                "(Linux uses --headless by default. "
                "To override, use --headed / --gui. "
                "For Xvfb mode instead, use --xvfb. "
                "Or hide this info with --headless, "
                "or by calling the new --headless2.)"
            )
            self.options.headless = True
            test.test.headless = True
        # Recorder Mode can still optimize scripts in --headless2 mode.
        if self.options.recorder_mode and self.options.headless:
            self.options.headless = False
            self.options.headless2 = True
            test.test.headless = False
            test.test.headless2 = True
        if not self.options.headless and not self.options.headless2:
            self.options.headed = True
            test.test.headed = True
        if (
            self.options.headless
            or self.options.headless2
            or self.options.xvfb
        ):
            try:
                # from pyvirtualdisplay import Display  # Skip for own lib
                from sbvirtualdisplay import Display

                self.display = Display(visible=0, size=(1440, 1880))
                self.display.start()
                self.headless_active = True
                sb_config.headless_active = True
            except Exception:
                # pyvirtualdisplay might not be necessary anymore because
                # Chrome and Firefox now have built-in headless displays
                pass
        sb_config._is_timeout_changed = False
        sb_config._SMALL_TIMEOUT = settings.SMALL_TIMEOUT
        sb_config._LARGE_TIMEOUT = settings.LARGE_TIMEOUT
        # The driver will be received later
        self.driver = None
        test.test.driver = self.driver

    def finalize(self, result):
        """This runs after all tests have completed with nosetests."""
        proxy_helper.remove_proxy_zip_if_present()

    def afterTest(self, test):
        try:
            # If the browser window is still open, close it now.
            if (
                not is_windows
                or test.test.browser == "ie"
                or self.driver.service.process
            ):
                self.driver.quit()
        except AttributeError:
            pass
        except Exception:
            pass
        if self.options.headless or self.options.xvfb:
            if self.headless_active:
                try:
                    self.headless_active = False
                    sb_config.headless_active = False
                    self.display.stop()
                except AttributeError:
                    pass
                except Exception:
                    pass
