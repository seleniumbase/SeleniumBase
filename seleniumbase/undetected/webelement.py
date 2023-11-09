import selenium.webdriver.remote.webelement


class WebElement(selenium.webdriver.remote.webelement.WebElement):
    def uc_click(
        self,
        driver=None,
        selector=None,
        by=None,
        reconnect_time=None,
    ):
        if driver and selector and by:
            driver.js_click(selector, by=by, timeout=1)
        else:
            super().click()
        if not reconnect_time:
            self._parent.reconnect(0.1)
        else:
            self._parent.reconnect(reconnect_time)

    def uc_reconnect(self, reconnect_time=None):
        if not reconnect_time:
            self._parent.reconnect(0.1)
        else:
            self._parent.reconnect(reconnect_time)
