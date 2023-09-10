"""Add new methods to extend the driver"""
from seleniumbase.fixtures import js_utils
from seleniumbase.fixtures import page_actions


class DriverMethods():
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, *args, **kwargs):
        page_actions.open_url(self.driver, *args, **kwargs)

    def click(self, *args, **kwargs):
        page_actions.click(self.driver, *args, **kwargs)

    def send_keys(self, *args, **kwargs):
        page_actions.send_keys(self.driver, *args, **kwargs)

    def update_text(self, *args, **kwargs):
        page_actions.update_text(self.driver, *args, **kwargs)

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
