import re
import selenium.webdriver.remote.webelement
from seleniumbase.fixtures import js_utils


class WebElement(selenium.webdriver.remote.webelement.WebElement):
    def uc_click(
        self,
        driver=None,
        selector=None,
        by=None,
        reconnect_time=None,
        tag_name=None,
    ):
        if driver and selector and by:
            delayed_click = False
            if tag_name == "span" or tag_name == "button" or tag_name == "div":
                delayed_click = True
            if delayed_click and ":contains" not in selector:
                selector = js_utils.convert_to_css_selector(selector, by)
                selector = re.escape(selector)
                selector = js_utils.escape_quotes_if_needed(selector)
                script = 'document.querySelector("%s").click();' % selector
                js_utils.call_me_later(driver, script, 111)
            else:
                driver.js_click(selector, by=by, timeout=1)
        else:
            super().click()
        if not reconnect_time:
            self._parent.reconnect(0.5)
        else:
            self._parent.reconnect(reconnect_time)

    def uc_reconnect(self, reconnect_time=None):
        if not reconnect_time:
            self._parent.reconnect(0.2)
        else:
            self._parent.reconnect(reconnect_time)
