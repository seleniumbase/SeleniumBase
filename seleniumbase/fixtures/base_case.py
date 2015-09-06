import json
import time
import logging
import unittest
from seleniumbase.config import settings
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import page_loads, page_interactions, page_utils


class BaseCase(unittest.TestCase):
    '''
    A base test case that wraps a bunch of methods from tools
    for easier access. You can also add your own methods here.
    '''

    def __init__(self, *args, **kwargs):
        super(BaseCase, self).__init__(*args, **kwargs)
        try:
            self.driver = WebDriver()
        except Exception:
            pass
        self.environment = None


    def find_visible_elements(self, selector, by=By.CSS_SELECTOR):
        return page_interactions.find_visible_elements(self.driver, selector, by)


    def hover_on_element(self, selector):
        return page_interactions.hover_on_element(self.driver, selector)


    def hover_and_click(self, hover_selector, click_selector, click_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT):
        return page_interactions.hover_and_click(self.driver, hover_selector, click_selector, click_by, timeout)


    def is_element_present(self, selector, by=By.CSS_SELECTOR):
        return page_interactions.is_element_present(self.driver, selector, by)


    def is_element_visible(self, selector, by=By.CSS_SELECTOR):
        return page_interactions.is_element_visible(self.driver, selector, by)


    def is_link_text_visible(self, link_text):
        return page_interactions.is_element_visible(self.driver, link_text, by=By.LINK_TEXT)


    def is_text_visible(self, text, selector, by=By.CSS_SELECTOR):
        return page_interactions.is_text_visible(self.driver, text, selector, by)


    def jquery_click(self, selector):
        self.driver.execute_script("jQuery('%s').click()" % selector)


    def click(self, selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT):
        element = page_loads.wait_for_element_visible(self.driver, selector, by, timeout=timeout)
        element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()


    def open(self, url):
        self.driver.get(url)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            self.wait_for_ready_state_complete()


    def open_url(self, url):
        """ In case people are mixing up self.open() with open(), use this alternative. """
        self.open(url)


    def execute_script(self, script):
        return self.driver.execute_script(script)


    def set_window_size(self, width, height):
        return self.driver.set_window_size(width, height)


    def maximize_window(self):
        return self.driver.maximize_window()


    def wait_for_link_text_visible(self, link_text, timeout=settings.LARGE_TIMEOUT):
        return self.wait_for_element_visible(link_text, by=By.LINK_TEXT, timeout=timeout)


    def click_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        element = self.wait_for_link_text_visible(link_text, timeout=timeout)
        element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()


    def activate_jquery(self):
        """ (It's not on by default on all website pages.) """
        self.driver.execute_script('var script = document.createElement("script"); script.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"; document.getElementsByTagName("head")[0].appendChild(script);')


    def scroll_to(self, selector):
        self.wait_for_element_visible(selector, timeout=settings.SMALL_TIMEOUT)
        self.driver.execute_script("jQuery('%s')[0].scrollIntoView()" % selector)


    def scroll_click(self, selector):
        self.scroll_to(selector)
        self.click(selector)


    def jq_format(self, code):
        return page_utils.jq_format(code)


    def set_value(self, selector, value):
        val = json.dumps(value)
        self.driver.execute_script("jQuery('%s').val(%s)" % (selector, val))


    def update_text_value(self, selector, new_value, timeout=settings.SMALL_TIMEOUT, retry=False):
        """ This method updates a selector's text value with a new value
            @Params
            selector - the selector with the value to update
            new_value - the new value for setting the text field
            timeout - how long to wait for the selector to be visible
            retry - if True, use jquery if the selenium text update fails
        """
        element = self.wait_for_element_visible(selector, timeout=timeout)
        element.clear()
        element.send_keys(new_value)
        if retry and element.get_attribute('value') != new_value and not new_value.endswith('\n'):
            logging.debug('update_text_value is falling back to jQuery!')
            selector = self.jq_format(selector)
            self.set_value(selector, new_value)


    def jquery_update_text_value(self, selector, new_value, timeout=settings.SMALL_TIMEOUT):
        element = self.wait_for_element_visible(selector, timeout=timeout)
        self.driver.execute_script("""jQuery('%s').val('%s')"""
                                   % (selector, self.jq_format(new_value)))
        if new_value.endswith('\n'):
            element.send_keys('\n')


    def wait_for_element_present(self, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_element_present(self.driver, selector, by, timeout)


    def wait_for_element_visible(self, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_element_visible(self.driver, selector, by, timeout)


    def wait_for_text_visible(self, text, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_text_visible(self.driver, text, selector, by, timeout)


    def wait_for_element_absent(self, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_element_absent(self.driver, selector, by, timeout)


    def wait_for_element_not_visible(self, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_element_not_visible(self.driver, selector, by, timeout)


    def wait_for_ready_state_complete(self, timeout=settings.EXTREME_TIMEOUT):
        return page_loads.wait_for_ready_state_complete(self.driver, timeout)


    def wait_for_and_accept_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_and_accept_alert(self.driver, timeout)


    def wait_for_and_dismiss_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_and_dismiss_alert(self.driver, timeout)


    def wait_for_and_switch_to_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_and_switch_to_alert(self.driver, timeout)
