from selenium import webdriver
from seleniumbase.fixtures import constants


def get_driver(browser_name):
    '''
    Spins up a new web browser and returns the driver.
    Tests that run with pytest spin up the browser from here.
    Can also be used to spin up additional browsers for the same test.
    '''
    if browser_name == constants.Browser.FIREFOX:
        try:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("reader.parse-on-load.enabled", False)
            return webdriver.Firefox(profile)
        except:
            return webdriver.Firefox()
    if browser_name == constants.Browser.INTERNET_EXPLORER:
        return webdriver.Ie()
    if browser_name == constants.Browser.PHANTOM_JS:
        return webdriver.PhantomJS()
    if browser_name == constants.Browser.GOOGLE_CHROME:
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--allow-file-access-from-files")
            return webdriver.Chrome(chrome_options=chrome_options)
        except Exception:
            return webdriver.Chrome()
