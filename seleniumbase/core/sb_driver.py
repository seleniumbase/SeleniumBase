"""Add new methods to extend the driver"""
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

    def open_url(self, *args, **kwargs):
        page_actions.open_url(self.driver, *args, **kwargs)

    def click(self, *args, **kwargs):
        page_actions.click(self.driver, *args, **kwargs)

    def click_link(self, *args, **kwargs):
        page_actions.click_link(self.driver, *args, **kwargs)

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

    def get_active_element_css(self, *args, **kwargs):
        return js_utils.get_active_element_css(self.driver, *args, **kwargs)

    def get_locale_code(self, *args, **kwargs):
        return js_utils.get_locale_code(self.driver, *args, **kwargs)

    def get_origin(self, *args, **kwargs):
        return js_utils.get_origin(self.driver, *args, **kwargs)

    def get_user_agent(self, *args, **kwargs):
        return js_utils.get_user_agent(self.driver, *args, **kwargs)

    def highlight(self, *args, **kwargs):
        js_utils.highlight(self.driver, *args, **kwargs)
