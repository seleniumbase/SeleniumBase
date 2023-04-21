"""The Nosetest plugin for setting Selenium test configuration."""
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
    """This plugin adds the following command-line options to nosetests:
    --browser=BROWSER  (The web browser to use. Default: "chrome".)
    --chrome  (Shortcut for "--browser=chrome". Default.)
    --edge  (Shortcut for "--browser=edge".)
    --firefox  (Shortcut for "--browser=firefox".)
    --safari  (Shortcut for "--browser=safari".)
    --user-data-dir=DIR  (Set the Chrome user data directory to use.)
    --protocol=PROTOCOL  (The Selenium Grid protocol: http|https.)
    --server=SERVER  (The Selenium Grid server/IP used for tests.)
    --port=PORT  (The Selenium Grid port used by the test server.)
    --cap-file=FILE  (The web browser's desired capabilities to use.)
    --cap-string=STRING  (The web browser's desired capabilities to use.)
    --proxy=SERVER:PORT  (Connect to a proxy server:port as tests are running)
    --proxy=USERNAME:PASSWORD@SERVER:PORT  (Use an authenticated proxy server)
    --proxy-bypass-list=STRING (";"-separated hosts to bypass, Eg "*.foo.com")
    --proxy-pac-url=URL  (Connect to a proxy server using a PAC_URL.pac file.)
    --proxy-pac-url=USERNAME:PASSWORD@URL  (Authenticated proxy with PAC URL.)
    --proxy-driver  (If a driver download is needed, will use: --proxy=PROXY.)
    --multi-proxy  (Allow multiple authenticated proxies when multi-threaded.)
    --agent=STRING  (Modify the web browser's User-Agent string.)
    --mobile  (Use the mobile device emulator while running tests.)
    --metrics=STRING  (Set mobile metrics: "CSSWidth,CSSHeight,PixelRatio".)
    --chromium-arg="ARG=N,ARG2" (Set Chromium args, ","-separated, no spaces.)
    --firefox-arg="ARG=N,ARG2" (Set Firefox args, comma-separated, no spaces.)
    --firefox-pref=SET  (Set a Firefox preference:value set, comma-separated.)
    --extension-zip=ZIP  (Load a Chrome Extension .zip|.crx, comma-separated.)
    --extension-dir=DIR  (Load a Chrome Extension directory, comma-separated.)
    --binary-location=PATH  (Set path of the Chromium browser binary to use.)
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
    --uc | --undetected  (Use undetected-chromedriver to evade bot-detection.)
    --uc-cdp-events  (Capture CDP events when running in "--undetected" mode.)
    --remote-debug  (Sync to Chrome Remote Debugger chrome://inspect/#devices)
    --final-debug  (Enter Debug Mode after each test ends. Don't use with CI!)
    --enable-3d-apis  (Enables WebGL and 3D APIs.)
    --swiftshader  (Use Chrome's "--use-gl=swiftshader" feature.)
    --incognito  (Enable Chrome's Incognito mode.)
    --guest  (Enable Chrome's Guest mode.)
    --devtools  (Open Chrome's DevTools when the browser opens.)
    --disable-beforeunload  (Disable the "beforeunload" event on Chrome.)
    --window-size=WIDTH,HEIGHT  (Set the browser's starting window size.)
    --maximize  (Start tests with the browser window maximized.)
    --screenshot  (Save a screenshot at the end of each test.)
    --visual-baseline  (Set the visual baseline for Visual/Layout tests.)
    --wire  (Use selenium-wire's webdriver for replacing selenium webdriver.)
    --external-pdf (Set Chromium "plugins.always_open_pdf_externally": True.)
    --timeout-multiplier=MULTIPLIER  (Multiplies the default timeout values.)
    """
    name = "selenium"  # Usage: --with-selenium

    def options(self, parser, env):
        super().options(parser, env=env)
        parser.addoption = parser.add_option  # Reuse name from pytest parser
        parser.addoption(
            "--browser",
            action="store",
            dest="browser",
            choices=constants.ValidBrowsers.valid_browsers,
            default=constants.Browser.GOOGLE_CHROME,
            help="""Specifies the web browser to use. Default: Chrome.
                    Examples: (--browser=edge OR --browser=firefox)""",
        )
        parser.addoption(
            "--chrome",
            action="store_true",
            dest="use_chrome",
            default=False,
            help="""Shortcut for --browser=chrome (Default)""",
        )
        parser.addoption(
            "--edge",
            action="store_true",
            dest="use_edge",
            default=False,
            help="""Shortcut for --browser=edge""",
        )
        parser.addoption(
            "--firefox",
            action="store_true",
            dest="use_firefox",
            default=False,
            help="""Shortcut for --browser=firefox""",
        )
        parser.addoption(
            "--ie",
            action="store_true",
            dest="use_ie",
            default=False,
            help="""Shortcut for --browser=ie""",
        )
        parser.addoption(
            "--opera",
            action="store_true",
            dest="use_opera",
            default=False,
            help="""Shortcut for --browser=opera""",
        )
        parser.addoption(
            "--safari",
            action="store_true",
            dest="use_safari",
            default=False,
            help="""Shortcut for --browser=safari""",
        )
        parser.addoption(
            "--cap_file",
            "--cap-file",
            action="store",
            dest="cap_file",
            default=None,
            help="""The file that stores browser desired capabilities
                    for BrowserStack, LambdaTest, Sauce Labs,
                    and other remote web drivers to use.""",
        )
        parser.addoption(
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
        parser.addoption(
            "--user_data_dir",
            "--user-data-dir",
            action="store",
            dest="user_data_dir",
            default=None,
            help="""The Chrome User Data Directory to use. (Chrome Profile)
                    If the directory doesn't exist, it'll be created.""",
        )
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
            "--server",
            action="store",
            dest="servername",
            default="localhost",
            help="""Designates the Selenium Grid server to use.
                    Use "127.0.0.1" to connect to a localhost Grid.
                    If unset or set to "localhost", Grid isn't used.
                    Default: "localhost".""",
        )
        parser.addoption(
            "--port",
            action="store",
            dest="port",
            default="4444",
            help="""Designates the Selenium Grid port to use.
                    Default: 4444. (If 443, protocol becomes "https")""",
        )
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
            "--proxy-driver",
            "--proxy_driver",
            action="store_true",
            dest="proxy_driver",
            default=False,
            help="""If a driver download is needed for tests,
                    uses proxy settings set via --proxy=PROXY.""",
        )
        parser.addoption(
            "--multi-proxy",
            "--multi_proxy",
            action="store_true",
            dest="multi_proxy",
            default=False,
            help="""If you need to run multi-threaded tests with
                    multiple proxies that require authentication,
                    set this to allow multiple configurations.""",
        )
        parser.addoption(
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
        parser.addoption(
            "--mobile",
            "--mobile-emulator",
            "--mobile_emulator",
            action="store_true",
            dest="mobile_emulator",
            default=False,
            help="""If this option is enabled, the mobile emulator
                    will be used while running tests.""",
        )
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
            "--binary_location",
            "--binary-location",
            action="store",
            dest="binary_location",
            default=None,
            help="""Sets the path of the Chromium browser binary to use.
                    Uses the default location if not os.path.exists(PATH)""",
        )
        parser.addoption(
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
        parser.addoption(
            "--headless",
            action="store_true",
            dest="headless",
            default=False,
            help="""Using this option activates headless mode,
                which is required on headless machines
                UNLESS using a virtual display with Xvfb.
                Default: False on Mac/Windows. True on Linux.""",
        )
        parser.addoption(
            "--headless2",
            action="store_true",
            dest="headless2",
            default=False,
            help="""This option activates the new headless mode,
                    which supports Chromium extensions, and more,
                    but is slower than the standard headless mode.""",
        )
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
            "--time_limit",
            "--time-limit",
            "--timelimit",
            action="store",
            dest="time_limit",
            default=None,
            help="""Use this to set a time limit per test, in seconds.
                    If a test runs beyond the limit, it fails.""",
        )
        parser.addoption(
            "--slow_mode",
            "--slow-mode",
            "--slowmo",
            "--slow",
            action="store_true",
            dest="slow_mode",
            default=False,
            help="""Using this slows down the automation.""",
        )
        parser.addoption(
            "--demo_mode",
            "--demo-mode",
            "--demo",
            action="store_true",
            dest="demo_mode",
            default=False,
            help="""Using this slows down the automation and lets you
                    visually see what the tests are actually doing.""",
        )
        parser.addoption(
            "--demo_sleep",
            "--demo-sleep",
            action="store",
            dest="demo_sleep",
            default=None,
            help="""Setting this overrides the Demo Mode sleep
                    time that happens after browser actions.""",
        )
        parser.addoption(
            "--highlights",
            action="store",
            dest="highlights",
            default=None,
            help="""Setting this overrides the default number of
                    highlight animation loops to have per call.""",
        )
        parser.addoption(
            "--message_duration",
            "--message-duration",
            action="store",
            dest="message_duration",
            default=None,
            help="""Setting this overrides the default time that
                    messenger notifications remain visible when reaching
                    assert statements during Demo Mode.""",
        )
        parser.addoption(
            "--check_js",
            "--check-js",
            action="store_true",
            dest="js_checking_on",
            default=False,
            help="""The option to check for JavaScript errors after
                    every page load.""",
        )
        parser.addoption(
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
        parser.addoption(
            "--block_images",
            "--block-images",
            action="store_true",
            dest="block_images",
            default=False,
            help="""Using this makes WebDriver block images from
                    loading on web pages during tests.""",
        )
        parser.addoption(
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
        parser.addoption(
            "--verify_delay",
            "--verify-delay",
            action="store",
            dest="verify_delay",
            default=None,
            help="""Setting this overrides the default wait time
                    before each MasterQA verification pop-up.""",
        )
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
            "--rec-sleep",
            "--record-sleep",
            action="store_true",
            dest="record_sleep",
            default=False,
            help="""If Recorder Mode is enabled,
                    records sleep(seconds) calls.""",
        )
        parser.addoption(
            "--rec-print",
            action="store_true",
            dest="rec_print",
            default=False,
            help="""If Recorder Mode is enabled,
                    prints output after tests end.""",
        )
        parser.addoption(
            "--disable_js",
            "--disable-js",
            action="store_true",
            dest="disable_js",
            default=False,
            help="""The option to disable JavaScript on web pages.
                    Warning: Most web pages will stop working!""",
        )
        parser.addoption(
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
        parser.addoption(
            "--disable_ws",
            "--disable-ws",
            "--disable-web-security",
            action="store_true",
            dest="disable_ws",
            default=False,
            help="""Using this disables the "Web Security" feature of
                    Chrome and Chromium-based browsers such as Edge.""",
        )
        parser.addoption(
            "--enable_ws",
            "--enable-ws",
            "--enable-web-security",
            action="store_true",
            dest="enable_ws",
            default=False,
            help="""Using this enables the "Web Security" feature of
                    Chrome and Chromium-based browsers such as Edge.""",
        )
        parser.addoption(
            "--enable_sync",
            "--enable-sync",
            action="store_true",
            dest="enable_sync",
            default=False,
            help="""Using this enables the "Chrome Sync" feature.""",
        )
        parser.addoption(
            "--use_auto_ext",
            "--use-auto-ext",
            "--auto-ext",
            action="store_true",
            dest="use_auto_ext",
            default=False,
            help="""(DEPRECATED) - Enable the automation extension.
                    It's not required, but some commands & advanced
                    features may need it.""",
        )
        parser.addoption(
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
        parser.addoption(
            "--uc_cdp_events",
            "--uc-cdp-events",
            "--uc-cdp",  # For capturing CDP events during UC Mode
            action="store_true",
            dest="uc_cdp_events",
            default=None,
            help="""Captures CDP events during Undetectable Mode runs.
                    Then you can add a listener to perform actions on
                    received data, such as printing it to the console:
                        from pprint import pformat
                        self.driver.add_cdp_listener(
                            "*", lambda data: print(pformat(data))
                        )
                        self.open(URL)""",
        )
        parser.addoption(
            "--uc_subprocess",
            "--uc-subprocess",
            "--uc-sub",  # undetected-chromedriver subprocess mode
            action="store_true",
            dest="uc_subprocess",
            default=None,
            help="""(DEPRECATED) - (UC Mode always uses this now.)
                    Use undetectable-chromedriver as a subprocess,
                    which can help avoid issues that might result.""",
        )
        parser.addoption(
            "--no_sandbox",
            "--no-sandbox",
            action="store_true",
            dest="no_sandbox",
            default=False,
            help="""Using this enables the "No Sandbox" feature.
                    (This setting is now always enabled by default.)""",
        )
        parser.addoption(
            "--disable_gpu",
            "--disable-gpu",
            action="store_true",
            dest="disable_gpu",
            default=False,
            help="""Using this enables the "Disable GPU" feature.
                    (This setting is now always enabled by default.)""",
        )
        parser.addoption(
            "--remote_debug",
            "--remote-debug",
            "--remote-debugger",
            "--remote_debugger",
            action="store_true",
            dest="remote_debug",
            default=False,
            help="""This syncs the browser to Chromium's remote debugger.
                    To access the remote debugging interface, go to:
                    chrome://inspect/#devices while tests are running.
                    The previous URL was at: http://localhost:9222/
                    Info: chromedevtools.github.io/devtools-protocol/""",
        )
        parser.addoption(
            "--final-debug",
            "--final-trace",
            "--fdebug",
            "--ftrace",
            action="store_true",
            dest="final_debug",
            default=False,
            help="""Enter Debug Mode at the end of each test.
                    To enter Debug Mode only on failures, use "--pdb".
                    If using both "--final-debug" and "--pdb" together,
                    then Debug Mode will activate twice on failures.""",
        )
        parser.addoption(
            "--enable_3d_apis",
            "--enable-3d-apis",
            action="store_true",
            dest="enable_3d_apis",
            default=False,
            help="""Using this enables WebGL and 3D APIs.""",
        )
        parser.addoption(
            "--swiftshader",
            action="store_true",
            dest="swiftshader",
            default=False,
            help="""Using this enables the "--use-gl=swiftshader"
                    feature when running tests on Chrome.""",
        )
        parser.addoption(
            "--incognito",
            "--incognito_mode",
            "--incognito-mode",
            action="store_true",
            dest="incognito",
            default=False,
            help="""Using this enables Chrome's Incognito mode.""",
        )
        parser.addoption(
            "--guest",
            "--guest_mode",
            "--guest-mode",
            action="store_true",
            dest="guest_mode",
            default=False,
            help="""Using this enables Chrome's Guest mode.""",
        )
        parser.addoption(
            "--devtools",
            "--open_devtools",
            "--open-devtools",
            action="store_true",
            dest="devtools",
            default=False,
            help="""Using this opens Chrome's DevTools.""",
        )
        parser.addoption(
            "--disable-beforeunload",
            "--disable_beforeunload",
            action="store_true",
            dest="_disable_beforeunload",
            default=False,
            help="""The option to disable the "beforeunload" event
                    on Chromium browsers (Chrome or Edge).
                    This is already the default Firefox option.""",
        )
        parser.addoption(
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
        parser.addoption(
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
        parser.addoption(
            "--screenshot",
            "--save_screenshot",
            "--save-screenshot",
            "--ss",
            action="store_true",
            dest="save_screenshot",
            default=False,
            help="""Save a screenshot at the end of every test.
                    By default, this is only done for failures.
                    Will be saved in the "latest_logs/" folder.""",
        )
        parser.addoption(
            "--no-screenshot",
            "--no_screenshot",
            "--ns",
            action="store_true",
            dest="no_screenshot",
            default=False,
            help="""No screenshots saved unless tests directly ask it.
                    This changes default behavior where screenshots are
                    saved for test failures and pytest-html reports.""",
        )
        parser.addoption(
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
        parser.addoption(
            "--wire",
            action="store_true",
            dest="use_wire",
            default=False,
            help="""Use selenium-wire's webdriver for selenium webdriver.""",
        )
        parser.addoption(
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
        parser.addoption(
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
        super().configure(options, conf)
        self.enabled = True  # Used if test class inherits BaseCase
        self.options = options
        self.headless_active = False  # Default setting
        sb_config.headless_active = False
        sb_config.is_nosetest = True
        proxy_helper.remove_proxy_zip_if_present()

    def beforeTest(self, test):
        browser = self.options.browser
        test.test.browser = browser
        test.test.headless = None
        test.test.headless2 = None
        # As a shortcut, you can use "--edge" instead of "--browser=edge", etc,
        # but you can only specify one default browser. (Default: chrome)
        sb_config._browser_shortcut = None
        sys_argv = sys.argv
        browser_changes = 0
        browser_set = None
        browser_text = None
        browser_list = []
        if "--browser=chrome" in sys_argv or "--browser chrome" in sys_argv:
            browser_changes += 1
            browser_set = "chrome"
            browser_list.append("--browser=chrome")
        if "--browser=edge" in sys_argv or "--browser edge" in sys_argv:
            browser_changes += 1
            browser_set = "edge"
            browser_list.append("--browser=edge")
        if "--browser=firefox" in sys_argv or "--browser firefox" in sys_argv:
            browser_changes += 1
            browser_set = "firefox"
            browser_list.append("--browser=firefox")
        if "--browser=opera" in sys_argv or "--browser opera" in sys_argv:
            browser_changes += 1
            browser_set = "opera"
            browser_list.append("--browser=opera")
        if "--browser=safari" in sys_argv or "--browser safari" in sys_argv:
            browser_changes += 1
            browser_set = "safari"
            browser_list.append("--browser=safari")
        if "--browser=ie" in sys_argv or "--browser ie" in sys_argv:
            browser_changes += 1
            browser_set = "ie"
            browser_list.append("--browser=ie")
        if "--browser=remote" in sys_argv or "--browser remote" in sys_argv:
            browser_changes += 1
            browser_set = "remote"
            browser_list.append("--browser=remote")
        browser_text = browser_set
        if "--chrome" in sys_argv and not browser_set == "chrome":
            browser_changes += 1
            browser_text = "chrome"
            sb_config._browser_shortcut = "chrome"
            browser_list.append("--chrome")
        if "--edge" in sys_argv and not browser_set == "edge":
            browser_changes += 1
            browser_text = "edge"
            sb_config._browser_shortcut = "edge"
            browser_list.append("--edge")
        if "--firefox" in sys_argv and not browser_set == "firefox":
            browser_changes += 1
            browser_text = "firefox"
            sb_config._browser_shortcut = "firefox"
            browser_list.append("--firefox")
        if "--ie" in sys_argv and not browser_set == "ie":
            browser_changes += 1
            browser_text = "ie"
            sb_config._browser_shortcut = "ie"
            browser_list.append("--ie")
        if "--opera" in sys_argv and not browser_set == "opera":
            browser_changes += 1
            browser_text = "opera"
            sb_config._browser_shortcut = "opera"
            browser_list.append("--opera")
        if "--safari" in sys_argv and not browser_set == "safari":
            browser_changes += 1
            browser_text = "safari"
            sb_config._browser_shortcut = "safari"
            browser_list.append("--safari")
        if browser_changes > 1:
            message = "\n\n  TOO MANY browser types were entered!"
            message += "\n  There were %s found:\n  >  %s" % (
                browser_changes,
                ", ".join(browser_list),
            )
            message += "\n  ONLY ONE default browser is allowed!"
            message += "\n  Select a single browser & try again!\n"
            raise Exception(message)
        if browser_text:
            browser = browser_text
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
        if sb_config._browser_shortcut:
            self.options.browser = sb_config._browser_shortcut
            test.test.browser = sb_config._browser_shortcut
        test.test.cap_file = self.options.cap_file
        test.test.cap_string = self.options.cap_string
        test.test.headless = self.options.headless
        test.test.headless2 = self.options.headless2
        if test.test.headless and test.test.browser == "safari":
            test.test.headless = False  # Safari doesn't use headless
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
        test.test.binary_location = self.options.binary_location
        test.test.page_load_strategy = self.options.page_load_strategy
        test.test.chromium_arg = self.options.chromium_arg
        test.test.firefox_arg = self.options.firefox_arg
        test.test.firefox_pref = self.options.firefox_pref
        test.test.proxy_string = self.options.proxy_string
        test.test.proxy_bypass_list = self.options.proxy_bypass_list
        test.test.proxy_pac_url = self.options.proxy_pac_url
        test.test.multi_proxy = self.options.multi_proxy
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
        test.test.uc_cdp_events = self.options.uc_cdp_events
        if test.test.uc_cdp_events and not test.test.undetectable:
            test.test.undetectable = True
        test.test.uc_subprocess = self.options.uc_subprocess
        if test.test.uc_subprocess and not test.test.undetectable:
            test.test.undetectable = True
        test.test.no_sandbox = self.options.no_sandbox
        test.test.disable_gpu = self.options.disable_gpu
        test.test.remote_debug = self.options.remote_debug
        test.test._final_debug = self.options.final_debug
        test.test.enable_3d_apis = self.options.enable_3d_apis
        test.test.swiftshader = self.options.swiftshader
        test.test.incognito = self.options.incognito
        test.test.guest_mode = self.options.guest_mode
        test.test.devtools = self.options.devtools
        test.test._disable_beforeunload = self.options._disable_beforeunload
        test.test.window_size = self.options.window_size
        test.test.maximize_option = self.options.maximize_option
        if self.options.save_screenshot and self.options.no_screenshot:
            self.options.save_screenshot = False  # no_screenshot has priority
        test.test.save_screenshot_after_test = self.options.save_screenshot
        test.test.no_screenshot_after_test = self.options.no_screenshot
        test.test.visual_baseline = self.options.visual_baseline
        test.test.use_wire = self.options.use_wire
        test.test.external_pdf = self.options.external_pdf
        test.test.timeout_multiplier = self.options.timeout_multiplier
        test.test.dashboard = False
        test.test._multithreaded = False
        test.test._reuse_session = False
        sb_config.no_screenshot = test.test.no_screenshot_after_test
        if test.test.servername != "localhost":
            # Using Selenium Grid
            # (Set --server="127.0.0.1" for localhost Grid)
            if str(self.options.port) == "443":
                test.test.protocol = "https"
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
                "Or you can hide this info by using "
                "--headless / --headless2.)"
            )
            self.options.headless = True
            test.test.headless = True
        if self.options.use_wire and self.options.undetectable:
            print(
                "\n"
                "SeleniumBase doesn't support mixing --uc with --wire mode.\n"
                "If you need both, override get_new_driver() from BaseCase:\n"
                "https://seleniumbase.io/help_docs/syntax_formats/#sb_sf_09\n"
                "(Only UC Mode without Wire Mode will be used for this run)\n"
            )
            self.options.use_wire = False
            test.test.use_wire = False
        if self.options.mobile_emulator and self.options.undetectable:
            print(
                "\n"
                "SeleniumBase doesn't support mixing --uc with --mobile.\n"
                "(Only UC Mode without Mobile will be used for this run)\n"
            )
            self.options.mobile_emulator = False
            test.test.mobile_emulator = False
            self.options.user_agent = None
            test.test.user_agent = None
        # Recorder Mode can still optimize scripts in --headless2 mode.
        if self.options.recorder_mode and self.options.headless:
            self.options.headless = False
            self.options.headless2 = True
            test.test.headless = False
            test.test.headless2 = True
        if not self.options.headless and not self.options.headless2:
            self.options.headed = True
            test.test.headed = True
        sb_config._virtual_display = None
        sb_config.headless_active = False
        self.headless_active = False
        if (
            "linux" in sys.platform
            and (not self.options.headed or self.options.xvfb)
        ):
            width = settings.HEADLESS_START_WIDTH
            height = settings.HEADLESS_START_HEIGHT
            try:
                from sbvirtualdisplay import Display

                self._xvfb_display = Display(visible=0, size=(width, height))
                self._xvfb_display.start()
                sb_config._virtual_display = self._xvfb_display
                self.headless_active = True
                sb_config.headless_active = True
            except Exception:
                pass
        sb_config._is_timeout_changed = False
        sb_config._SMALL_TIMEOUT = settings.SMALL_TIMEOUT
        sb_config._LARGE_TIMEOUT = settings.LARGE_TIMEOUT
        sb_config._context_of_runner = False  # Context Manager Compatibility
        sb_config.proxy_driver = self.options.proxy_driver
        sb_config.multi_proxy = self.options.multi_proxy
        # The driver will be received later
        self.driver = None
        test.test.driver = self.driver

    def finalize(self, result):
        """This runs after all tests have completed with nosetests."""
        if not sb_config.multi_proxy:
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
        try:
            if (
                hasattr(self, "_xvfb_display")
                and self._xvfb_display
                and hasattr(self._xvfb_display, "stop")
            ):
                self.headless_active = False
                sb_config.headless_active = False
                self._xvfb_display.stop()
                self._xvfb_display = None
            if (
                hasattr(sb_config, "_virtual_display")
                and sb_config._virtual_display
                and hasattr(sb_config._virtual_display, "stop")
            ):
                sb_config._virtual_display.stop()
                sb_config._virtual_display = None
        except Exception:
            pass
