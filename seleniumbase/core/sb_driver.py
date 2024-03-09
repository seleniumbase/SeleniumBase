"""Add new methods to extend the driver"""
from selenium.webdriver.remote.webelement import WebElement
from seleniumbase.fixtures import js_utils
from seleniumbase.fixtures import page_actions
from seleniumbase.fixtures import page_utils


class DriverMethods():
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by=None, value=None):
        if not value:
            value = by
            by = "css selector"
        elif not by:
            by = "css selector"
        else:
            value, by = page_utils.swap_selector_and_by_if_reversed(value, by)
        return self.driver.default_find_element(by=by, value=value)

    def find_elements(self, by=None, value=None):
        if not value:
            value = by
            by = "css selector"
        elif not by:
            by = "css selector"
        else:
            value, by = page_utils.swap_selector_and_by_if_reversed(value, by)
        return self.driver.default_find_elements(by=by, value=value)

    def locator(self, selector, by=None):
        if not by:
            by = "css selector"
        else:
            selector, by = page_utils.swap_selector_and_by_if_reversed(
                selector, by
            )
        try:
            return self.driver.default_find_element(by=by, value=selector)
        except Exception:
            pass
        raise Exception('No such Element: {%s} (by="%s")!' % (selector, by))

    def get_attribute(self, selector, attribute, by="css selector"):
        element = self.locator(selector, by=by)
        return element.get_attribute(attribute)

    def get_page_source(self):
        return self.driver.page_source

    def get_title(self):
        return self.driver.title

    def open_url(self, *args, **kwargs):
        page_actions.open_url(self.driver, *args, **kwargs)

    def click(self, *args, **kwargs):
        page_actions.click(self.driver, *args, **kwargs)

    def click_link(self, *args, **kwargs):
        page_actions.click_link(self.driver, *args, **kwargs)

    def click_if_visible(self, *args, **kwargs):
        page_actions.click_if_visible(self.driver, *args, **kwargs)

    def click_active_element(self, *args, **kwargs):
        page_actions.click_active_element(self.driver, *args, **kwargs)

    def send_keys(self, *args, **kwargs):
        page_actions.send_keys(self.driver, *args, **kwargs)

    def press_keys(self, *args, **kwargs):
        page_actions.press_keys(self.driver, *args, **kwargs)

    def update_text(self, *args, **kwargs):
        page_actions.update_text(self.driver, *args, **kwargs)

    def submit(self, *args, **kwargs):
        page_actions.submit(self.driver, *args, **kwargs)

    def assert_element_visible(self, *args, **kwargs):
        page_actions.assert_element_visible(self.driver, *args, **kwargs)

    def assert_element_present(self, *args, **kwargs):
        page_actions.assert_element_present(self.driver, *args, **kwargs)

    def assert_element_not_visible(self, *args, **kwargs):
        page_actions.assert_element_not_visible(self.driver, *args, **kwargs)

    def assert_text(self, *args, **kwargs):
        page_actions.assert_text(self.driver, *args, **kwargs)

    def assert_exact_text(self, *args, **kwargs):
        page_actions.assert_exact_text(self.driver, *args, **kwargs)

    def wait_for_element(self, *args, **kwargs):
        return page_actions.wait_for_element(self.driver, *args, **kwargs)

    def wait_for_element_visible(self, *args, **kwargs):
        return page_actions.wait_for_element(self.driver, *args, **kwargs)

    def wait_for_element_present(self, *args, **kwargs):
        return page_actions.wait_for_selector(self.driver, *args, **kwargs)

    def wait_for_selector(self, *args, **kwargs):
        return page_actions.wait_for_selector(self.driver, *args, **kwargs)

    def wait_for_text(self, *args, **kwargs):
        return page_actions.wait_for_text(self.driver, *args, **kwargs)

    def wait_for_exact_text(self, *args, **kwargs):
        return page_actions.wait_for_exact_text(self.driver, *args, **kwargs)

    def wait_for_and_accept_alert(self, *args, **kwargs):
        return page_actions.wait_for_and_accept_alert(
            self.driver, *args, **kwargs
        )

    def wait_for_and_dismiss_alert(self, *args, **kwargs):
        return page_actions.wait_for_and_dismiss_alert(
            self.driver, *args, **kwargs
        )

    def is_element_present(self, *args, **kwargs):
        return page_actions.is_element_present(self.driver, *args, **kwargs)

    def is_element_visible(self, *args, **kwargs):
        return page_actions.is_element_visible(self.driver, *args, **kwargs)

    def is_text_visible(self, *args, **kwargs):
        return page_actions.is_text_visible(self.driver, *args, **kwargs)

    def is_exact_text_visible(self, *args, **kwargs):
        return page_actions.is_exact_text_visible(self.driver, *args, **kwargs)

    def get_text(self, *args, **kwargs):
        return page_actions.get_text(self.driver, *args, **kwargs)

    def js_click(self, *args, **kwargs):
        return page_actions.js_click(self.driver, *args, **kwargs)

    def is_attribute_present(self, *args, **kwargs):
        return page_actions.has_attribute(self.driver, *args, **kwargs)

    def get_active_element_css(self, *args, **kwargs):
        return js_utils.get_active_element_css(self.driver, *args, **kwargs)

    def get_locale_code(self, *args, **kwargs):
        return js_utils.get_locale_code(self.driver, *args, **kwargs)

    def get_origin(self, *args, **kwargs):
        return js_utils.get_origin(self.driver, *args, **kwargs)

    def get_user_agent(self, *args, **kwargs):
        return js_utils.get_user_agent(self.driver, *args, **kwargs)

    def highlight(self, *args, **kwargs):
        if "scroll" in kwargs:
            kwargs.pop("scroll")
        w_args = kwargs.copy()
        if "loops" in w_args:
            w_args.pop("loops")
        element = page_actions.wait_for_element(self.driver, *args, **w_args)
        browser = self.driver.capabilities["browserName"].lower()
        js_utils.slow_scroll_to_element(self.driver, element, browser)
        if "timeout" in kwargs:
            kwargs.pop("timeout")
        js_utils.highlight(self.driver, *args, **kwargs)

    def highlight_click(self, *args, **kwargs):
        self.highlight(*args, **kwargs)
        if "loops" in kwargs:
            kwargs.pop("loops")
        if "scroll" in kwargs:
            kwargs.pop("scroll")
        page_actions.click(self.driver, *args, **kwargs)

    def highlight_if_visible(
        self, selector, by="css selector", loops=4, scroll=True
    ):
        if self.is_element_visible(selector, by=by):
            self.highlight(selector, by=by, loops=loops, scroll=scroll)

    def switch_to_frame(self, frame):
        if isinstance(frame, WebElement):
            self.driver.switch_to.frame(frame)
        else:
            iframe = self.locator(frame)
            self.driver.switch_to.frame(iframe)

    def set_wire_proxy(self, string):
        """Set a proxy server for selenium-wire mode ("--wire")
        Examples:  (ONLY avilable if using selenium-wire mode!)
        driver.set_wire_proxy("SERVER:PORT")
        driver.set_wire_proxy("socks5://SERVER:PORT")
        driver.set_wire_proxy("USERNAME:PASSWORD@SERVER:PORT")
        """
        the_http = "http"
        the_https = "https"
        if string.startswith("socks4://"):
            the_http = "socks4"
            the_https = "socks4"
        elif string.startswith("socks5://"):
            the_http = "socks5"
            the_https = "socks5"
        string = string.split("//")[-1]
        if hasattr(self.driver, "proxy"):
            self.driver.proxy = {
                "http": "%s://%s" % (the_http, string),
                "https": "%s://%s" % (the_https, string),
                "no_proxy": "localhost,127.0.0.1",
            }
