from selenium import webdriver
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class OverrideDriverTest(BaseCase):
    def get_new_driver(self, *args, **kwargs):
        """This method overrides get_new_driver() from BaseCase."""
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"],
        )
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=options)

    def test_driver_override(self):
        self.open("https://seleniumbase.io/demo_page")
        self.type("#myTextInput", "This is Automated")
        self.set_value("input#mySlider", "100")
        self.select_option_by_text("#mySelect", "Set to 100%")
        self.click("#checkBox1")
        self.drag_and_drop("img#logo", "div#drop2")
        self.click('button:contains("Click Me")')
