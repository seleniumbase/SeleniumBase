from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumbase.config import settings
from seleniumbase.core import download_helper
from seleniumbase.fixtures import constants


def _create_firefox_profile(downloads_path):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("reader.parse-on-load.enabled", False)
    profile.set_preference("pdfjs.disabled", True)
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


def get_driver(browser_name, headless=False, use_grid=False,
               servername='localhost', port=4444):
    if use_grid:
        return get_remote_driver(browser_name, headless, servername, port)
    else:
        return get_local_driver(browser_name, headless)


def get_remote_driver(browser_name, headless, servername, port):
    downloads_path = download_helper.get_downloads_folder()
    download_helper.reset_downloads_folder()
    address = "http://%s:%s/wd/hub" % (servername, port)

    if browser_name == constants.Browser.GOOGLE_CHROME:
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": downloads_path,
            "credentials_enable_service": False,
            "profile": {
                "password_manager_enabled": False
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--allow-file-access-from-files")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-infobars")
        if headless:
            chrome_options.add_argument("--headless")
        if settings.START_CHROME_IN_FULL_SCREEN_MODE:
            # Run Chrome in full screen mode on WINDOWS
            chrome_options.add_argument("--start-maximized")
            # Run Chrome in full screen mode on MAC/Linux
            chrome_options.add_argument("--kiosk")
        capabilities = chrome_options.to_capabilities()
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=capabilities)

    if browser_name == constants.Browser.FIREFOX:
        try:
            # Use Geckodriver for Firefox if it's on the PATH
            profile = _create_firefox_profile(downloads_path)
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
            profile = _create_firefox_profile(downloads_path)
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

    if browser_name == constants.Browser.INTERNET_EXPLORER:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.INTERNETEXPLORER))
    if browser_name == constants.Browser.EDGE:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.EDGE))
    if browser_name == constants.Browser.SAFARI:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.SAFARI))
    if browser_name == constants.Browser.PHANTOM_JS:
        return webdriver.Remote(
            command_executor=address,
            desired_capabilities=(
                webdriver.DesiredCapabilities.PHANTOMJS))


def get_local_driver(browser_name, headless):
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
                profile = _create_firefox_profile(downloads_path)
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
                profile = _create_firefox_profile(downloads_path)
                firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
                firefox_capabilities['marionette'] = False
                firefox_driver = webdriver.Firefox(
                    firefox_profile=profile, capabilities=firefox_capabilities)
            return firefox_driver
        except Exception:
            return webdriver.Firefox()
    if browser_name == constants.Browser.INTERNET_EXPLORER:
        return webdriver.Ie()
    if browser_name == constants.Browser.EDGE:
        return webdriver.Edge()
    if browser_name == constants.Browser.SAFARI:
        return webdriver.Safari()
    if browser_name == constants.Browser.PHANTOM_JS:
        return webdriver.PhantomJS()
    if browser_name == constants.Browser.GOOGLE_CHROME:
        try:
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                "download.default_directory": downloads_path,
                "credentials_enable_service": False,
                "profile": {
                    "password_manager_enabled": False
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--allow-file-access-from-files")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-infobars")
            if headless:
                chrome_options.add_argument("--headless")
            if settings.START_CHROME_IN_FULL_SCREEN_MODE:
                # Run Chrome in full screen mode on WINDOWS
                chrome_options.add_argument("--start-maximized")
                # Run Chrome in full screen mode on MAC/Linux
                chrome_options.add_argument("--kiosk")
            return webdriver.Chrome(chrome_options=chrome_options)
        except Exception:
            return webdriver.Chrome()
