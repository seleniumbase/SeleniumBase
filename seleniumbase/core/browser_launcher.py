from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumbase.core import download_helper
from seleniumbase.fixtures import constants


def get_driver(browser_name):
    '''
    Spins up a new web browser and returns the driver.
    Tests that run with pytest spin up the browser from here.
    Can also be used to spin up additional browsers for the same test.
    '''
    downloads_path = download_helper.get_downloads_folder()
    download_helper.reset_downloads_folder()

    if browser_name == constants.Browser.FIREFOX:
        try:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("reader.parse-on-load.enabled", False)
            profile.set_preference("pdfjs.disabled", True)
            profile.set_preference(
                "security.mixed_content.block_active_content", False)
            profile.set_preference(
                "browser.download.manager.showAlertOnComplete", True)
            profile.set_preference("browser.download.panel.shown", True)
            profile.set_preference(
                "browser.download.animateNotifications", True)
            profile.set_preference("browser.download.dir", downloads_path)
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference(
                "browser.helperApps.neverAsk.saveToDisk",
                ("application/pdf, application/zip, application/octet-stream, "
                 "text/csv, text/xml, application/xml, text/plain, "
                 "text/octet-stream"))
            firefox_capabilities = DesiredCapabilities.FIREFOX
            try:
                # Use Geckodriver for Firefox if it's on the PATH
                firefox_capabilities['marionette'] = True
                firefox_driver = webdriver.Firefox(
                    firefox_profile=profile, capabilities=firefox_capabilities)
            except WebDriverException:
                # Don't use Geckodriver: Only works for old versions of Firefox
                firefox_capabilities['marionette'] = False
                firefox_driver = webdriver.Firefox(
                    firefox_profile=profile, capabilities=firefox_capabilities)
            return firefox_driver
        except:
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
            prefs = {"download.default_directory": downloads_path}
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--allow-file-access-from-files")
            chrome_options.add_argument("--allow-running-insecure-content")
            return webdriver.Chrome(chrome_options=chrome_options)
        except Exception:
            return webdriver.Chrome()
