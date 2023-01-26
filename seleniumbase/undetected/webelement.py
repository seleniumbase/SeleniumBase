import selenium.webdriver.remote.webelement
from seleniumbase.config import settings


class WebElement(selenium.webdriver.remote.webelement.WebElement):
    def uc_click(self):
        super().click()
        if (
            hasattr(settings, "PAGE_LOAD_STRATEGY")
            and settings.PAGE_LOAD_STRATEGY == "none"
        ):
            pass
        else:
            self._parent.reconnect(0.1)
