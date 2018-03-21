import re
import warnings
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumbase.config import settings
from seleniumbase.config import proxy_list
from seleniumbase.core import download_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import page_utils


def _set_chrome_options(downloads_path, proxy_string):
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
        chrome_options.add_argument('--proxy-server=%s' % proxy_string)
    if settings.START_CHROME_IN_FULL_SCREEN_MODE:
        # Run Chrome in full screen mode on WINDOWS
        chrome_options.add_argument("--start-maximized")
        # Run Chrome in full screen mode on MAC/Linux
        chrome_options.add_argument("--kiosk")
    return chrome_options


def _create_firefox_profile(downloads_path, proxy_string):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("reader.parse-on-load.enabled", False)
    profile.set_preference("pdfjs.disabled", True)
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
    profile.set_preference(
        "browser.download.manager.showAlertOnComplete", False)
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
    val_ip = re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', proxy_string)
    if not val_ip:
        if proxy_string.startswith('http://'):
            proxy_string = proxy_string.split('http://')[1]
        elif proxy_string.startswith('https://'):
            proxy_string = proxy_string.split('https://')[1]
        elif '://' in proxy_string:
            proxy_string = proxy_string.split('://')[1]
        chunks = proxy_string.split(':')
        if len(chunks) == 2:
            if re.match('^\d+$', chunks[1]):
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
    if proxy_string:
        proxy_string = validate_proxy_string(proxy_string)
    if use_grid:
        return get_remote_driver(
            browser_name, headless, servername, port, proxy_string)
    else:
        return get_local_driver(browser_name, headless, proxy_string)


def get_remote_driver(browser_name, headless, servername, port, proxy_string):
    downloads_path = download_helper.get_downloads_folder()
    download_helper.reset_downloads_folder()
    address = "http://%s:%s/wd/hub" % (servername, port)

    if browser_name == constants.Browser.GOOGLE_CHROME:
        chrome_options = _set_chrome_options(downloads_path, proxy_string)
        if headless:
            chrome_options.add_argument("--headless")
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
    elif browser_name == constants.Browser.PHANTOM_JS:
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=(
                    webdriver.DesiredCapabilities.PHANTOMJS))


def get_local_driver(browser_name, headless, proxy_string):
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
                firefox_driver = webdriver.Firefox(
                    firefox_profile=profile, capabilities=firefox_capabilities,
                    firefox_options=options)
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
        return webdriver.Ie()
    elif browser_name == constants.Browser.EDGE:
        return webdriver.Edge()
    elif browser_name == constants.Browser.SAFARI:
        return webdriver.Safari()
    elif browser_name == constants.Browser.PHANTOM_JS:
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.PhantomJS()
    elif browser_name == constants.Browser.GOOGLE_CHROME:
        try:
            chrome_options = _set_chrome_options(downloads_path, proxy_string)
            if headless:
                chrome_options.add_argument("--headless")
            return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            if headless:
                raise Exception(e)
            return webdriver.Chrome()
