import json
import logging
import os
import random
import re
import sys
import time
import urllib3
import warnings
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumbase.config import proxy_list
from seleniumbase.config import settings
from seleniumbase.core import download_helper
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import page_utils
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
from seleniumbase import extensions  # browser extensions storage folder
urllib3.disable_warnings()
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
# Make sure that the SeleniumBase DRIVER_DIR is at the top of the System PATH
# (Changes to the System PATH with os.environ only last during the test run)
if not os.environ["PATH"].startswith(DRIVER_DIR):
    # Remove existing SeleniumBase DRIVER_DIR from System PATH if present
    os.environ["PATH"] = os.environ["PATH"].replace(DRIVER_DIR, "")
    # If two path separators are next to each other, replace with just one
    os.environ["PATH"] = os.environ["PATH"].replace(
        os.pathsep + os.pathsep, os.pathsep)
    # Put the SeleniumBase DRIVER_DIR at the beginning of the System PATH
    os.environ["PATH"] = DRIVER_DIR + os.pathsep + os.environ["PATH"]
EXTENSIONS_DIR = os.path.dirname(os.path.realpath(extensions.__file__))
DISABLE_CSP_ZIP_PATH = "%s/%s" % (EXTENSIONS_DIR, "disable_csp.zip")
PROXY_ZIP_PATH = proxy_helper.PROXY_ZIP_PATH
PROXY_ZIP_PATH_2 = proxy_helper.PROXY_ZIP_PATH_2
PLATFORM = sys.platform
IS_WINDOWS = False
LOCAL_CHROMEDRIVER = None
LOCAL_GECKODRIVER = None
LOCAL_EDGEDRIVER = None
LOCAL_IEDRIVER = None
LOCAL_OPERADRIVER = None
if "darwin" in PLATFORM or "linux" in PLATFORM:
    LOCAL_CHROMEDRIVER = DRIVER_DIR + '/chromedriver'
    LOCAL_GECKODRIVER = DRIVER_DIR + '/geckodriver'
    LOCAL_EDGEDRIVER = DRIVER_DIR + '/msedgedriver'
    LOCAL_OPERADRIVER = DRIVER_DIR + '/operadriver'
elif "win32" in PLATFORM or "win64" in PLATFORM or "x64" in PLATFORM:
    IS_WINDOWS = True
    LOCAL_EDGEDRIVER = DRIVER_DIR + '/msedgedriver.exe'
    LOCAL_IEDRIVER = DRIVER_DIR + '/IEDriverServer.exe'
    LOCAL_CHROMEDRIVER = DRIVER_DIR + '/chromedriver.exe'
    LOCAL_GECKODRIVER = DRIVER_DIR + '/geckodriver.exe'
    LOCAL_OPERADRIVER = DRIVER_DIR + '/operadriver.exe'
else:
    # Cannot determine system
    pass  # SeleniumBase will use web drivers from the System PATH by default


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def make_driver_executable_if_not(driver_path):
    # Verify driver has executable permissions. If not, add them.
    permissions = oct(os.stat(driver_path)[0])[-3:]
    if '4' in permissions or '6' in permissions:
        # We want at least a '5' or '7' to make sure it's executable
        make_executable(driver_path)


def is_chromedriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if os.path.exists(path + '/' + "chromedriver"):
            return True
    return False


def is_edgedriver_on_path():
    return os.path.exists(LOCAL_EDGEDRIVER)


def is_geckodriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if os.path.exists(path + '/' + "geckodriver"):
            return True
    return False


def _add_chrome_proxy_extension(
        chrome_options, proxy_string, proxy_user, proxy_pass):
    """ Implementation of https://stackoverflow.com/a/35293284 for
        https://stackoverflow.com/questions/12848327/
        (Run Selenium on a proxy server that requires authentication.) """
    arg_join = " ".join(sys.argv)
    if not ("-n" in sys.argv or "-n=" in arg_join or arg_join == "-c"):
        # Single-threaded
        proxy_helper.create_proxy_zip(proxy_string, proxy_user, proxy_pass)
    else:
        # Pytest multi-threaded test
        import threading
        lock = threading.Lock()
        with lock:
            time.sleep(random.uniform(0.02, 0.15))
            if not os.path.exists(PROXY_ZIP_PATH):
                proxy_helper.create_proxy_zip(
                    proxy_string, proxy_user, proxy_pass)
            time.sleep(random.uniform(0.1, 0.2))
    proxy_zip = PROXY_ZIP_PATH
    if not os.path.exists(PROXY_ZIP_PATH):
        # Handle "Permission denied" on the default proxy.zip path
        proxy_zip = PROXY_ZIP_PATH_2
    chrome_options.add_extension(proxy_zip)
    return chrome_options


def _add_chrome_disable_csp_extension(chrome_options):
    """ Disable Chrome's Content-Security-Policy with a browser extension.
        See https://github.com/PhilGrayson/chrome-csp-disable for details. """
    disable_csp_zip = DISABLE_CSP_ZIP_PATH
    chrome_options.add_extension(disable_csp_zip)
    return chrome_options


def _set_chrome_options(
        browser_name, downloads_path, headless, locale_code,
        proxy_string, proxy_auth, proxy_user, proxy_pass,
        user_agent, disable_csp, enable_ws, enable_sync, use_auto_ext,
        no_sandbox, disable_gpu, incognito, guest_mode,
        devtools, remote_debug, swiftshader, block_images,
        user_data_dir, extension_zip, extension_dir, servername,
        mobile_emulator, device_width, device_height, device_pixel_ratio):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": downloads_path,
        "local_discovery.notifications_enabled": False,
        "credentials_enable_service": False,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True,
        "default_content_setting_values.notifications": 0,
        "default_content_settings.popups": 0,
        "managed_default_content_settings.popups": 0,
        "content_settings.exceptions.automatic_downloads.*.setting": 1,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 0,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    if locale_code:
        prefs["intl.accept_languages"] = locale_code
    if block_images:
        prefs["profile.managed_default_content_settings.images"] = 2
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("w3c", True)
    if enable_sync:
        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation", "enable-logging", "disable-sync"])
        chrome_options.add_argument("--enable-sync")
    else:
        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation", "enable-logging", "enable-blink-features"])
    if browser_name == constants.Browser.OPERA:
        # Disable the Blink features
        if enable_sync:
            chrome_options.add_experimental_option(
                "excludeSwitches",
                (["enable-automation", "enable-logging", "disable-sync",
                    "enable-blink-features"]))
            chrome_options.add_argument("--enable-sync")
        else:
            chrome_options.add_experimental_option(
                "excludeSwitches",
                (["enable-automation", "enable-logging",
                    "enable-blink-features"]))
    if mobile_emulator:
        emulator_settings = {}
        device_metrics = {}
        if type(device_width) is int and type(device_height) is int and (
                type(device_pixel_ratio) is int):
            device_metrics["width"] = device_width
            device_metrics["height"] = device_height
            device_metrics["pixelRatio"] = device_pixel_ratio
        else:
            device_metrics["width"] = 411
            device_metrics["height"] = 731
            device_metrics["pixelRatio"] = 3
        emulator_settings["deviceMetrics"] = device_metrics
        if user_agent:
            emulator_settings["userAgent"] = user_agent
        chrome_options.add_experimental_option(
            "mobileEmulation", emulator_settings)
        chrome_options.add_argument("--enable-sync")
    if not proxy_auth and not disable_csp and (
            not extension_zip and not extension_dir):
        if incognito:
            # Use Chrome's Incognito Mode
            # Incognito Mode prevents Chrome extensions from loading,
            # so if using extensions or a feature that uses extensions,
            # then Chrome's Incognito mode will be disabled instead.
            chrome_options.add_argument("--incognito")
        elif guest_mode:
            # Use Chrome's Guest Mode
            # Guest mode prevents Chrome extensions from loading,
            # so if using extensions or a feature that uses extensions,
            # then Chrome's Guest Mode will be disabled instead.
            chrome_options.add_argument("--guest")
        else:
            pass
    if user_data_dir:
        abs_path = os.path.abspath(user_data_dir)
        chrome_options.add_argument("user-data-dir=%s" % abs_path)
    if extension_zip:
        # Can be a comma-separated list of .ZIP or .CRX files
        extension_zip_list = extension_zip.split(',')
        for extension_zip_item in extension_zip_list:
            abs_path = os.path.abspath(extension_zip_item)
            chrome_options.add_extension(abs_path)
    if extension_dir:
        # load-extension input can be a comma-separated list
        abs_path = os.path.abspath(extension_dir)
        chrome_options.add_argument("--load-extension=%s" % abs_path)
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-first-run")
    if devtools and not headless:
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--allow-running-insecure-content")
    if user_agent:
        chrome_options.add_argument("--user-agent=%s" % user_agent)
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-single-click-autofill")
    chrome_options.add_argument(
        "--disable-autofill-keyboard-accessory-view[8]")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--homepage=about:blank")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--dom-automation")
    chrome_options.add_argument("--disable-hang-monitor")
    chrome_options.add_argument("--disable-prompt-on-repost")
    if servername != "localhost":
        use_auto_ext = True  # Use Automation Extension with the Selenium Grid
    if not use_auto_ext:  # (It's ON by default. Disable it when not wanted.)
        chrome_options.add_experimental_option("useAutomationExtension", False)
    if (settings.DISABLE_CSP_ON_CHROME or disable_csp) and not headless:
        # Headless Chrome doesn't support extensions, which are required
        # for disabling the Content Security Policy on Chrome
        chrome_options = _add_chrome_disable_csp_extension(chrome_options)
        chrome_options.add_argument("--enable-sync")
    if proxy_string:
        if proxy_auth:
            chrome_options = _add_chrome_proxy_extension(
                chrome_options, proxy_string, proxy_user, proxy_pass)
        chrome_options.add_argument('--proxy-server=%s' % proxy_string)
    if headless:
        if not proxy_auth and not browser_name == constants.Browser.OPERA:
            # Headless Chrome doesn't support extensions, which are
            # required when using a proxy server that has authentication.
            # Instead, base_case.py will use PyVirtualDisplay when not
            # using Chrome's built-in headless mode. See link for details:
            # https://bugs.chromium.org/p/chromium/issues/detail?id=706008
            # Also, Opera Chromium doesn't support headless mode:
            # https://github.com/operasoftware/operachromiumdriver/issues/62
            chrome_options.add_argument("--headless")
    if browser_name != constants.Browser.OPERA:
        # Opera Chromium doesn't support these switches
        chrome_options.add_argument("--ignore-certificate-errors")
        if not enable_ws:
            chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--no-sandbox")
    else:
        # Opera Chromium only!
        chrome_options.add_argument("--allow-elevated-browser")
    if remote_debug:
        # To access the Remote Debugger, go to: http://localhost:9222
        # while a Chromium driver is running.
        # Info: https://chromedevtools.github.io/devtools-protocol/
        chrome_options.add_argument('--remote-debugging-port=9222')
    if swiftshader:
        chrome_options.add_argument("--use-gl=swiftshader")
    else:
        chrome_options.add_argument("--disable-gpu")
    if "linux" in PLATFORM:
        chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


def _set_safari_capabilities():
    from selenium.webdriver.safari.webdriver import DesiredCapabilities as SDC
    safari_capabilities = SDC.SAFARI.copy()
    safari_capabilities["cleanSession"] = True
    return safari_capabilities


def _create_firefox_profile(
        downloads_path, locale_code, proxy_string, user_agent, disable_csp):
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    profile.set_preference("reader.parse-on-load.enabled", False)
    profile.set_preference("pdfjs.disabled", True)
    profile.set_preference("app.update.auto", False)
    profile.set_preference("app.update.enabled", False)
    profile.set_preference("app.update.silent", True)
    profile.set_preference("browser.formfill.enable", False)
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("devtools.errorconsole.enabled", True)
    profile.set_preference("dom.webnotifications.enabled", False)
    profile.set_preference("dom.disable_beforeunload", True)
    profile.set_preference("browser.contentblocking.database.enabled", False)
    profile.set_preference("extensions.allowPrivateBrowsingByDefault", True)
    profile.set_preference("extensions.PrivateBrowsing.notification", False)
    profile.set_preference("extensions.systemAddon.update.enabled", False)
    profile.set_preference("extensions.update.autoUpdateDefault", False)
    profile.set_preference("extensions.update.enabled", False)
    profile.set_preference("extensions.update.silent", True)
    profile.set_preference(
        "datareporting.healthreport.logging.consoleEnabled", False)
    profile.set_preference("datareporting.healthreport.service.enabled", False)
    profile.set_preference(
        "datareporting.healthreport.service.firstRun", False)
    profile.set_preference("datareporting.healthreport.uploadEnabled", False)
    profile.set_preference("datareporting.policy.dataSubmissionEnabled", False)
    profile.set_preference(
        "datareporting.policy.dataSubmissionPolicyAccepted", False)
    profile.set_preference("toolkit.telemetry.unified", False)
    if proxy_string:
        proxy_server = proxy_string.split(':')[0]
        proxy_port = proxy_string.split(':')[1]
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_server)
        profile.set_preference("network.proxy.http_port", int(proxy_port))
        profile.set_preference("network.proxy.ssl", proxy_server)
        profile.set_preference("network.proxy.ssl_port", int(proxy_port))
    if user_agent:
        profile.set_preference("general.useragent.override", user_agent)
    profile.set_preference(
        "security.mixed_content.block_active_content", False)
    if settings.DISABLE_CSP_ON_FIREFOX or disable_csp:
        profile.set_preference("security.csp.enable", False)
    profile.set_preference(
        "browser.download.manager.showAlertOnComplete", False)
    if locale_code:
        profile.set_preference("intl.accept_languages", locale_code)
    profile.set_preference("browser.shell.checkDefaultBrowser", False)
    profile.set_preference("browser.startup.page", 0)
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference(
        "browser.download.animateNotifications", False)
    profile.set_preference("browser.download.dir", downloads_path)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference(
        "browser.download.manager.showWhenStarting", False)
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        ("application/pdf, application/zip, application/octet-stream, "
         "text/csv, text/xml, application/xml, text/plain, "
         "text/octet-stream, application/x-gzip, application/x-tar "
         "application/"
         "vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
    return profile


def display_proxy_warning(proxy_string):
    message = ('\n\nWARNING: Proxy String ["%s"] is NOT in the expected '
               '"ip_address:port" or "server:port" format, '
               '(OR the key does not exist in '
               'seleniumbase.config.proxy_list.PROXY_LIST).'
               % proxy_string)
    if settings.RAISE_INVALID_PROXY_STRING_EXCEPTION:
        raise Exception(message)
    else:
        message += ' *** DEFAULTING to NOT USING a Proxy Server! ***'
        warnings.simplefilter('always', Warning)  # See Warnings
        warnings.warn(message, category=Warning, stacklevel=2)
        warnings.simplefilter('default', Warning)  # Set Default


def validate_proxy_string(proxy_string):
    if proxy_string in proxy_list.PROXY_LIST.keys():
        proxy_string = proxy_list.PROXY_LIST[proxy_string]
        if not proxy_string:
            return None
    valid = False
    val_ip = re.match(
        r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', proxy_string)
    if not val_ip:
        if proxy_string.startswith('http://'):
            proxy_string = proxy_string.split('http://')[1]
        elif proxy_string.startswith('https://'):
            proxy_string = proxy_string.split('https://')[1]
        elif '://' in proxy_string:
            proxy_string = proxy_string.split('://')[1]
        chunks = proxy_string.split(':')
        if len(chunks) == 2:
            if re.match(r'^\d+$', chunks[1]):
                if page_utils.is_valid_url('http://' + proxy_string):
                    valid = True
    else:
        proxy_string = val_ip.group()
        valid = True
    if not valid:
        display_proxy_warning(proxy_string)
        proxy_string = None
    return proxy_string


def get_driver(browser_name, headless=False, locale_code=None,
               use_grid=False, servername='localhost', port=4444,
               proxy_string=None, user_agent=None,
               cap_file=None, cap_string=None,
               disable_csp=None, enable_ws=None, enable_sync=None,
               use_auto_ext=None, no_sandbox=None, disable_gpu=None,
               incognito=None, guest_mode=None,
               devtools=None, remote_debug=None,
               swiftshader=None, block_images=None,
               user_data_dir=None, extension_zip=None, extension_dir=None,
               test_id=None, mobile_emulator=False, device_width=None,
               device_height=None, device_pixel_ratio=None):
    proxy_auth = False
    proxy_user = None
    proxy_pass = None
    if proxy_string:
        username_and_password = None
        if "@" in proxy_string:
            # Format => username:password@hostname:port
            try:
                username_and_password = proxy_string.split('@')[0]
                proxy_string = proxy_string.split('@')[1]
                proxy_user = username_and_password.split(':')[0]
                proxy_pass = username_and_password.split(':')[1]
            except Exception:
                raise Exception(
                    'The format for using a proxy server with authentication '
                    'is: "username:password@hostname:port". If using a proxy '
                    'server without auth, the format is: "hostname:port".')
            if browser_name != constants.Browser.GOOGLE_CHROME and (
                    browser_name != constants.Browser.EDGE):
                raise Exception(
                    "Chrome or Edge is required when using a proxy server "
                    "that has authentication! (If using a proxy server "
                    "without auth, Chrome, Edge, or Firefox may be used.)")
        proxy_string = validate_proxy_string(proxy_string)
        if proxy_string and proxy_user and proxy_pass:
            proxy_auth = True
    if browser_name == "chrome" and user_data_dir and len(user_data_dir) < 3:
        raise Exception(
            "Name length of Chrome's User Data Directory must be >= 3.")
    if use_grid:
        return get_remote_driver(
            browser_name, headless, locale_code, servername, port,
            proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
            cap_file, cap_string, disable_csp, enable_ws, enable_sync,
            use_auto_ext, no_sandbox, disable_gpu, incognito, guest_mode,
            devtools, remote_debug, swiftshader, block_images,
            user_data_dir, extension_zip, extension_dir, test_id,
            mobile_emulator, device_width, device_height, device_pixel_ratio)
    else:
        return get_local_driver(
            browser_name, headless, locale_code, servername,
            proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
            disable_csp, enable_ws, enable_sync,
            use_auto_ext, no_sandbox, disable_gpu, incognito, guest_mode,
            devtools, remote_debug, swiftshader, block_images,
            user_data_dir, extension_zip, extension_dir,
            mobile_emulator, device_width, device_height, device_pixel_ratio)


def get_remote_driver(
        browser_name, headless, locale_code, servername, port,
        proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
        cap_file, cap_string, disable_csp, enable_ws, enable_sync,
        use_auto_ext, no_sandbox, disable_gpu, incognito, guest_mode,
        devtools, remote_debug, swiftshader, block_images,
        user_data_dir, extension_zip, extension_dir, test_id,
        mobile_emulator, device_width, device_height, device_pixel_ratio):
    downloads_path = download_helper.get_downloads_folder()
    download_helper.reset_downloads_folder()
    address = "http://%s:%s/wd/hub" % (servername, port)
    desired_caps = {}
    extra_caps = {}
    if cap_file:
        from seleniumbase.core import capabilities_parser
        desired_caps = capabilities_parser.get_desired_capabilities(cap_file)
    if cap_string:
        try:
            extra_caps = json.loads(cap_string)
        except Exception as e:
            p1 = "Invalid input format for --cap-string:\n  %s" % e
            p2 = "The --cap-string input was: %s" % cap_string
            p3 = "Enclose cap-string in SINGLE quotes; keys in DOUBLE quotes."
            p4 = ("""Here's an example of correct cap-string usage:\n  """
                  """--cap-string='{"browserName":"chrome","name":"test1"}'""")
            raise Exception("%s\n%s\n%s\n%s" % (p1, p2, p3, p4))
        for cap_key in extra_caps.keys():
            desired_caps[cap_key] = extra_caps[cap_key]
    if cap_file or cap_string:
        if "name" in desired_caps.keys():
            if desired_caps["name"] == "*":
                desired_caps["name"] = test_id
    if browser_name == constants.Browser.GOOGLE_CHROME:
        chrome_options = _set_chrome_options(
            browser_name, downloads_path, headless, locale_code,
            proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
            disable_csp, enable_ws, enable_sync, use_auto_ext, no_sandbox,
            disable_gpu, incognito, guest_mode,
            devtools, remote_debug, swiftshader, block_images,
            user_data_dir, extension_zip, extension_dir,
            servername, mobile_emulator,
            device_width, device_height, device_pixel_ratio)
        capabilities = chrome_options.to_capabilities()
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.FIREFOX:
        try:
            # Use Geckodriver for Firefox if it's on the PATH
            profile = _create_firefox_profile(
                downloads_path, locale_code,
                proxy_string, user_agent, disable_csp)
            firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
            firefox_capabilities['marionette'] = True
            if headless:
                firefox_capabilities['moz:firefoxOptions'] = (
                    {'args': ['-headless']})
            for key in desired_caps.keys():
                firefox_capabilities[key] = desired_caps[key]
            capabilities = firefox_capabilities
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                browser_profile=profile,
                keep_alive=True)
        except WebDriverException:
            # Don't use Geckodriver: Only works for old versions of Firefox
            profile = _create_firefox_profile(
                downloads_path, locale_code,
                proxy_string, user_agent, disable_csp)
            firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
            firefox_capabilities['marionette'] = False
            if headless:
                firefox_capabilities['moz:firefoxOptions'] = (
                    {'args': ['-headless']})
            for key in desired_caps.keys():
                firefox_capabilities[key] = desired_caps[key]
            capabilities = firefox_capabilities
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                browser_profile=profile,
                keep_alive=True)
    elif browser_name == constants.Browser.INTERNET_EXPLORER:
        capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.EDGE:
        capabilities = webdriver.DesiredCapabilities.EDGE
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.SAFARI:
        capabilities = webdriver.DesiredCapabilities.SAFARI
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.OPERA:
        capabilities = webdriver.DesiredCapabilities.OPERA
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.PHANTOM_JS:
        capabilities = webdriver.DesiredCapabilities.PHANTOMJS
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True)
    elif browser_name == constants.Browser.ANDROID:
        capabilities = webdriver.DesiredCapabilities.ANDROID
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.IPHONE:
        capabilities = webdriver.DesiredCapabilities.IPHONE
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.IPAD:
        capabilities = webdriver.DesiredCapabilities.IPAD
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities,
            keep_alive=True)
    elif browser_name == constants.Browser.REMOTE:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=desired_caps,
            keep_alive=True)


def get_local_driver(
        browser_name, headless, locale_code, servername,
        proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
        disable_csp, enable_ws, enable_sync, use_auto_ext, no_sandbox,
        disable_gpu, incognito, guest_mode,
        devtools, remote_debug, swiftshader, block_images,
        user_data_dir, extension_zip, extension_dir,
        mobile_emulator, device_width, device_height, device_pixel_ratio):
    '''
    Spins up a new web browser and returns the driver.
    Can also be used to spin up additional browsers for the same test.
    '''
    downloads_path = download_helper.get_downloads_folder()
    download_helper.reset_downloads_folder()

    if browser_name == constants.Browser.FIREFOX:
        try:
            try:
                # Use Geckodriver for Firefox if it's on the PATH
                profile = _create_firefox_profile(
                    downloads_path, locale_code,
                    proxy_string, user_agent, disable_csp)
                firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
                firefox_capabilities['marionette'] = True
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument('-headless')
                    firefox_capabilities['moz:firefoxOptions'] = (
                        {'args': ['-headless']})
                if LOCAL_GECKODRIVER and os.path.exists(LOCAL_GECKODRIVER):
                    try:
                        make_driver_executable_if_not(LOCAL_GECKODRIVER)
                    except Exception as e:
                        logging.debug("\nWarning: Could not make geckodriver"
                                      " executable: %s" % e)
                elif not is_geckodriver_on_path():
                    args = " ".join(sys.argv)
                    if not ("-n" in sys.argv or "-n=" in args or args == "-c"):
                        # (Not multithreaded)
                        from seleniumbase.console_scripts import sb_install
                        sys_args = sys.argv  # Save a copy of current sys args
                        print("\nWarning: geckodriver not found!"
                              " Installing now:")
                        try:
                            sb_install.main(override="geckodriver")
                        except Exception as e:
                            print("\nWarning: Could not install geckodriver: "
                                  "%s" % e)
                        sys.argv = sys_args  # Put back the original sys args
                firefox_driver = webdriver.Firefox(
                    firefox_profile=profile,
                    capabilities=firefox_capabilities,
                    options=options)
            except Exception:
                profile = _create_firefox_profile(
                    downloads_path, locale_code,
                    proxy_string, user_agent, disable_csp)
                firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
                firefox_driver = webdriver.Firefox(
                    firefox_profile=profile,
                    capabilities=firefox_capabilities)
            return firefox_driver
        except Exception as e:
            if headless:
                raise Exception(e)
            return webdriver.Firefox()
    elif browser_name == constants.Browser.INTERNET_EXPLORER:
        if not IS_WINDOWS:
            raise Exception(
                "IE Browser is for Windows-based operating systems only!")
        from selenium.webdriver.ie.options import Options
        ie_options = Options()
        ie_options.ignore_protected_mode_settings = True
        ie_options.ignore_zoom_level = True
        ie_options.require_window_focus = False
        ie_options.native_events = True
        ie_options.full_page_screenshot = True
        ie_options.persistent_hover = True
        ie_capabilities = ie_options.to_capabilities()
        if LOCAL_IEDRIVER and os.path.exists(LOCAL_IEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_IEDRIVER)
            except Exception as e:
                logging.debug("\nWarning: Could not make iedriver"
                              " executable: %s" % e)
        return webdriver.Ie(capabilities=ie_capabilities)
    elif browser_name == constants.Browser.EDGE:
        try:
            chrome_options = _set_chrome_options(
                browser_name, downloads_path, headless, locale_code,
                proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
                disable_csp, enable_ws, enable_sync, use_auto_ext,
                no_sandbox, disable_gpu, incognito, guest_mode,
                devtools, remote_debug, swiftshader, block_images,
                user_data_dir, extension_zip, extension_dir, servername,
                mobile_emulator, device_width, device_height,
                device_pixel_ratio)
            if LOCAL_EDGEDRIVER and os.path.exists(LOCAL_EDGEDRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_EDGEDRIVER)
                except Exception as e:
                    logging.debug("\nWarning: Could not make edgedriver"
                                  " executable: %s" % e)
            elif not is_edgedriver_on_path():
                args = " ".join(sys.argv)
                if not ("-n" in sys.argv or "-n=" in args or args == "-c"):
                    # (Not multithreaded)
                    from seleniumbase.console_scripts import sb_install
                    sys_args = sys.argv  # Save a copy of current sys args
                    print("\nWarning: msedgedriver not found. Installing now:")
                    sb_install.main(override="edgedriver")
                    sys.argv = sys_args  # Put back the original sys args
            # For Microsoft Edge (Chromium) version 79 or lower
            return webdriver.Chrome(executable_path=LOCAL_EDGEDRIVER,
                                    options=chrome_options)
        except Exception:
            # For Microsoft Edge (Chromium) version 80 or higher
            from msedge.selenium_tools import Edge, EdgeOptions
            if LOCAL_EDGEDRIVER and os.path.exists(LOCAL_EDGEDRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_EDGEDRIVER)
                except Exception as e:
                    logging.debug("\nWarning: Could not make edgedriver"
                                  " executable: %s" % e)
            edge_options = EdgeOptions()
            edge_options.use_chromium = True
            prefs = {
                "download.default_directory": downloads_path,
                "local_discovery.notifications_enabled": False,
                "credentials_enable_service": False,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True,
                "default_content_setting_values.notifications": 0,
                "default_content_settings.popups": 0,
                "managed_default_content_settings.popups": 0,
                "content_settings.exceptions.automatic_downloads.*.setting": 1,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 0,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.popups": 0,
                "profile.default_content_setting_values.automatic_downloads": 1
            }
            if locale_code:
                prefs["intl.accept_languages"] = locale_code
            if block_images:
                prefs["profile.managed_default_content_settings.images"] = 2
            edge_options.add_experimental_option("prefs", prefs)
            edge_options.add_experimental_option("w3c", True)
            edge_options.add_experimental_option(
                "useAutomationExtension", False)
            edge_options.add_experimental_option(
                "excludeSwitches", ["enable-automation", "enable-logging"])
            if guest_mode:
                edge_options.add_argument("--guest")
            if headless:
                edge_options.add_argument("--headless")
            if mobile_emulator:
                emulator_settings = {}
                device_metrics = {}
                if type(device_width) is int and (
                        type(device_height) is int and (
                        type(device_pixel_ratio) is int)):
                    device_metrics["width"] = device_width
                    device_metrics["height"] = device_height
                    device_metrics["pixelRatio"] = device_pixel_ratio
                else:
                    device_metrics["width"] = 411
                    device_metrics["height"] = 731
                    device_metrics["pixelRatio"] = 3
                emulator_settings["deviceMetrics"] = device_metrics
                if user_agent:
                    emulator_settings["userAgent"] = user_agent
                edge_options.add_experimental_option(
                    "mobileEmulation", emulator_settings)
                edge_options.add_argument("--enable-sync")
            edge_options.add_argument("--disable-infobars")
            edge_options.add_argument("--disable-save-password-bubble")
            edge_options.add_argument("--disable-single-click-autofill")
            edge_options.add_argument(
                "--disable-autofill-keyboard-accessory-view[8]")
            edge_options.add_argument("--disable-translate")
            if not enable_ws:
                edge_options.add_argument("--disable-web-security")
            edge_options.add_argument("--homepage=about:blank")
            edge_options.add_argument("--dns-prefetch-disable")
            edge_options.add_argument("--dom-automation")
            edge_options.add_argument("--disable-hang-monitor")
            edge_options.add_argument("--disable-prompt-on-repost")
            if proxy_string:
                edge_options.add_argument('--proxy-server=%s' % proxy_string)
            edge_options.add_argument("--test-type")
            edge_options.add_argument("--log-level=3")
            edge_options.add_argument("--no-first-run")
            edge_options.add_argument("--ignore-certificate-errors")
            if devtools and not headless:
                edge_options.add_argument("--auto-open-devtools-for-tabs")
            edge_options.add_argument("--allow-file-access-from-files")
            edge_options.add_argument("--allow-insecure-localhost")
            edge_options.add_argument("--allow-running-insecure-content")
            if user_agent:
                edge_options.add_argument("--user-agent=%s" % user_agent)
            edge_options.add_argument("--no-sandbox")
            if remote_debug:
                # To access the Remote Debugger, go to: http://localhost:9222
                # while a Chromium driver is running.
                # Info: https://chromedevtools.github.io/devtools-protocol/
                edge_options.add_argument('--remote-debugging-port=9222')
            if swiftshader:
                edge_options.add_argument("--use-gl=swiftshader")
            else:
                edge_options.add_argument("--disable-gpu")
            if "linux" in PLATFORM:
                edge_options.add_argument("--disable-dev-shm-usage")
            capabilities = edge_options.to_capabilities()
            capabilities["platform"] = ''
            return Edge(
                executable_path=LOCAL_EDGEDRIVER, capabilities=capabilities)
    elif browser_name == constants.Browser.SAFARI:
        arg_join = " ".join(sys.argv)
        if ("-n" in sys.argv) or ("-n=" in arg_join) or (arg_join == "-c"):
            # Skip if multithreaded
            raise Exception("Can't run Safari tests in multi-threaded mode!")
        safari_capabilities = _set_safari_capabilities()
        return webdriver.Safari(desired_capabilities=safari_capabilities)
    elif browser_name == constants.Browser.OPERA:
        try:
            if LOCAL_OPERADRIVER and os.path.exists(LOCAL_OPERADRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_OPERADRIVER)
                except Exception as e:
                    logging.debug("\nWarning: Could not make operadriver"
                                  " executable: %s" % e)
            opera_options = _set_chrome_options(
                browser_name, downloads_path, headless, locale_code,
                proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
                disable_csp, enable_ws, enable_sync, use_auto_ext,
                no_sandbox, disable_gpu, incognito, guest_mode,
                devtools, remote_debug, swiftshader, block_images,
                user_data_dir, extension_zip, extension_dir,
                servername, mobile_emulator,
                device_width, device_height, device_pixel_ratio)
            opera_options.headless = False  # No support for headless Opera
            return webdriver.Opera(options=opera_options)
        except Exception:
            return webdriver.Opera()
    elif browser_name == constants.Browser.PHANTOM_JS:
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.PhantomJS()
    elif browser_name == constants.Browser.GOOGLE_CHROME:
        try:
            chrome_options = _set_chrome_options(
                browser_name, downloads_path, headless, locale_code,
                proxy_string, proxy_auth, proxy_user, proxy_pass, user_agent,
                disable_csp, enable_ws, enable_sync, use_auto_ext,
                no_sandbox, disable_gpu, incognito, guest_mode,
                devtools, remote_debug, swiftshader, block_images,
                user_data_dir, extension_zip, extension_dir,
                servername, mobile_emulator,
                device_width, device_height, device_pixel_ratio)
            if LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                except Exception as e:
                    logging.debug("\nWarning: Could not make chromedriver"
                                  " executable: %s" % e)
            elif not is_chromedriver_on_path():
                args = " ".join(sys.argv)
                if not ("-n" in sys.argv or "-n=" in args or args == "-c"):
                    # (Not multithreaded)
                    from seleniumbase.console_scripts import sb_install
                    sys_args = sys.argv  # Save a copy of current sys args
                    print("\nWarning: chromedriver not found. Installing now:")
                    sb_install.main(override="chromedriver")
                    sys.argv = sys_args  # Put back the original sys args
            if not headless or "linux" not in PLATFORM:
                return webdriver.Chrome(options=chrome_options)
            else:  # Running headless on Linux
                try:
                    return webdriver.Chrome(options=chrome_options)
                except Exception:
                    # Use the virtual display on Linux during headless errors
                    logging.debug("\nWarning: Chrome failed to launch in"
                                  " headless mode. Attempting to use the"
                                  " SeleniumBase virtual display on Linux...")
                    chrome_options.headless = False
                    return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            if headless:
                raise Exception(e)
            if LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                except Exception as e:
                    logging.debug("\nWarning: Could not make chromedriver"
                                  " executable: %s" % e)
            return webdriver.Chrome()
    else:
        raise Exception(
            "%s is not a valid browser option for this system!" % browser_name)
