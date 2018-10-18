import os
import re
import sys
import threading
import time
import warnings
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumbase.config import proxy_list
from seleniumbase.core import download_helper
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import page_utils
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
PROXY_ZIP_PATH = proxy_helper.PROXY_ZIP_PATH
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
    LOCAL_OPERADRIVER = DRIVER_DIR + '/operadriver'
elif "win32" in PLATFORM or "win64" in PLATFORM or "x64" in PLATFORM:
    IS_WINDOWS = True
    LOCAL_EDGEDRIVER = DRIVER_DIR + '/MicrosoftWebDriver.exe'
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


def _add_chrome_proxy_extension(
        chrome_options, proxy_string, proxy_user, proxy_pass):
    """ Implementation of https://stackoverflow.com/a/35293284 for
        https://stackoverflow.com/questions/12848327/
        (Run Selenium on a proxy server that requires authentication.)
        The retry_on_exception is only needed for multithreaded runs
        because proxy.zip is a common file shared between all tests
        in a single run. """
    if not "".join(sys.argv) == "-c":
        # Single-threaded
        proxy_helper.create_proxy_zip(proxy_string, proxy_user, proxy_pass)
    else:
        # Pytest multi-threaded test
        lock = threading.Lock()
        with lock:
            if not os.path.exists(PROXY_ZIP_PATH):
                proxy_helper.create_proxy_zip(
                    proxy_string, proxy_user, proxy_pass)
            time.sleep(0.3)
    chrome_options.add_extension(PROXY_ZIP_PATH)
    return chrome_options


def _set_chrome_options(
        downloads_path, proxy_string, proxy_auth, proxy_user, proxy_pass):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": downloads_path,
        "credentials_enable_service": False,
        "profile": {
            "password_manager_enabled": False
        }
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-single-click-autofill")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-web-security")
    if proxy_string:
        if proxy_auth:
            chrome_options = _add_chrome_proxy_extension(
                chrome_options, proxy_string, proxy_user, proxy_pass)
            chrome_options.add_extension(DRIVER_DIR + "/proxy.zip")
        chrome_options.add_argument('--proxy-server=%s' % proxy_string)
    return chrome_options


def _create_firefox_profile(downloads_path, proxy_string):
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    profile.set_preference("reader.parse-on-load.enabled", False)
    profile.set_preference("pdfjs.disabled", True)
    profile.set_preference("app.update.auto", False)
    profile.set_preference("app.update.enabled", False)
    if proxy_string:
        proxy_server = proxy_string.split(':')[0]
        proxy_port = proxy_string.split(':')[1]
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_server)
        profile.set_preference("network.proxy.http_port", int(proxy_port))
        profile.set_preference("network.proxy.ssl", proxy_server)
        profile.set_preference("network.proxy.ssl_port", int(proxy_port))
    profile.set_preference(
        "security.mixed_content.block_active_content", False)
    profile.set_preference("security.csp.enable", False)
    profile.set_preference(
        "browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference(
        "browser.download.animateNotifications", False)
    profile.set_preference("browser.download.dir", downloads_path)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        ("application/pdf, application/zip, application/octet-stream, "
         "text/csv, text/xml, application/xml, text/plain, "
         "text/octet-stream, "
         "application/"
         "vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
    return profile


def display_proxy_warning(proxy_string):
    message = ('\n\nWARNING: Proxy String ["%s"] is NOT in the expected '
               '"ip_address:port" or "server:port" format, '
               '(OR the key does not exist in proxy_list.PROXY_LIST). '
               '*** DEFAULTING to NOT USING a Proxy Server! ***'
               % proxy_string)
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


def get_driver(browser_name, headless=False, use_grid=False,
               servername='localhost', port=4444, proxy_string=None):
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
            if browser_name != constants.Browser.GOOGLE_CHROME:
                raise Exception(
                    "Chrome is required when using a proxy server that has "
                    "authentication! (If using a proxy server without auth, "
                    "either Chrome or Firefox may be used.)")
        proxy_string = validate_proxy_string(proxy_string)
        if proxy_string and proxy_user and proxy_pass:
            if not os.path.exists(PROXY_ZIP_PATH):
                proxy_helper.create_proxy_zip(
                    proxy_string, proxy_user, proxy_pass)
            proxy_auth = True
    if use_grid:
        return get_remote_driver(
            browser_name, headless, servername, port, proxy_string, proxy_auth,
            proxy_user, proxy_pass)
    else:
        return get_local_driver(
            browser_name, headless, proxy_string, proxy_auth,
            proxy_user, proxy_pass)


def get_remote_driver(
        browser_name, headless, servername, port, proxy_string, proxy_auth,
        proxy_user, proxy_pass):
    downloads_path = download_helper.get_downloads_folder()
    download_helper.reset_downloads_folder()
    address = "http://%s:%s/wd/hub" % (servername, port)

    if browser_name == constants.Browser.GOOGLE_CHROME:
        chrome_options = _set_chrome_options(
            downloads_path, proxy_string, proxy_auth,
            proxy_user, proxy_pass)
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
        capabilities = chrome_options.to_capabilities()
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities)
    elif browser_name == constants.Browser.FIREFOX:
        try:
            # Use Geckodriver for Firefox if it's on the PATH
            profile = _create_firefox_profile(downloads_path, proxy_string)
            firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
            firefox_capabilities['marionette'] = True
            if headless:
                firefox_capabilities['moz:firefoxOptions'] = (
                    {'args': ['-headless']})
            capabilities = firefox_capabilities
            address = "http://%s:%s/wd/hub" % (servername, port)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                browser_profile=profile)
        except WebDriverException:
            # Don't use Geckodriver: Only works for old versions of Firefox
            profile = _create_firefox_profile(downloads_path, proxy_string)
            firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
            firefox_capabilities['marionette'] = False
            if headless:
                firefox_capabilities['moz:firefoxOptions'] = (
                    {'args': ['-headless']})
            capabilities = firefox_capabilities
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                browser_profile=profile)
    elif browser_name == constants.Browser.INTERNET_EXPLORER:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.INTERNETEXPLORER))
    elif browser_name == constants.Browser.EDGE:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.EDGE))
    elif browser_name == constants.Browser.SAFARI:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.SAFARI))
    elif browser_name == constants.Browser.OPERA:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.OPERA))
    elif browser_name == constants.Browser.PHANTOM_JS:
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=(
                    webdriver.DesiredCapabilities.PHANTOMJS))


def get_local_driver(
        browser_name, headless, proxy_string, proxy_auth,
        proxy_user, proxy_pass):
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
                profile = _create_firefox_profile(downloads_path, proxy_string)
                firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
                firefox_capabilities['marionette'] = True
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument('-headless')
                if LOCAL_GECKODRIVER and os.path.exists(LOCAL_GECKODRIVER):
                    make_driver_executable_if_not(LOCAL_GECKODRIVER)
                    firefox_driver = webdriver.Firefox(
                        firefox_profile=profile,
                        capabilities=firefox_capabilities,
                        options=options,
                        executable_path=LOCAL_GECKODRIVER)
                else:
                    firefox_driver = webdriver.Firefox(
                        firefox_profile=profile,
                        capabilities=firefox_capabilities,
                        options=options)
            except WebDriverException:
                # Don't use Geckodriver: Only works for old versions of Firefox
                profile = _create_firefox_profile(downloads_path, proxy_string)
                firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
                firefox_capabilities['marionette'] = False
                firefox_driver = webdriver.Firefox(
                    firefox_profile=profile, capabilities=firefox_capabilities)
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
        ie_options.ignore_protected_mode_settings = False
        ie_options.ignore_zoom_level = True
        ie_options.require_window_focus = False
        ie_options.native_events = True
        ie_options.full_page_screenshot = True
        ie_options.persistent_hover = True
        ie_capabilities = ie_options.to_capabilities()
        if LOCAL_IEDRIVER and os.path.exists(LOCAL_IEDRIVER):
            make_driver_executable_if_not(LOCAL_IEDRIVER)
            return webdriver.Ie(
                capabilities=ie_capabilities,
                executable_path=LOCAL_IEDRIVER)
        else:
            return webdriver.Ie(capabilities=ie_capabilities)
    elif browser_name == constants.Browser.EDGE:
        if not IS_WINDOWS:
            raise Exception(
                "Edge Browser is for Windows-based operating systems only!")
        edge_capabilities = DesiredCapabilities.EDGE.copy()
        if LOCAL_EDGEDRIVER and os.path.exists(LOCAL_EDGEDRIVER):
            make_driver_executable_if_not(LOCAL_EDGEDRIVER)
            return webdriver.Edge(
                capabilities=edge_capabilities,
                executable_path=LOCAL_EDGEDRIVER)
        else:
            return webdriver.Edge(capabilities=edge_capabilities)
    elif browser_name == constants.Browser.SAFARI:
        return webdriver.Safari()
    elif browser_name == constants.Browser.OPERA:
        if LOCAL_OPERADRIVER and os.path.exists(LOCAL_OPERADRIVER):
            make_driver_executable_if_not(LOCAL_OPERADRIVER)
            return webdriver.Opera(executable_path=LOCAL_OPERADRIVER)
        else:
            return webdriver.Opera()
    elif browser_name == constants.Browser.PHANTOM_JS:
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.PhantomJS()
    elif browser_name == constants.Browser.GOOGLE_CHROME:
        try:
            chrome_options = _set_chrome_options(
                downloads_path, proxy_string, proxy_auth,
                proxy_user, proxy_pass)
            if headless:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
            if LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER):
                make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                return webdriver.Chrome(
                    executable_path=LOCAL_CHROMEDRIVER, options=chrome_options)
            else:
                return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            if headless:
                raise Exception(e)
            if LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER):
                make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                return webdriver.Chrome(executable_path=LOCAL_CHROMEDRIVER)
            else:
                return webdriver.Chrome()
