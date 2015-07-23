import json
import time
import logging
import unittest
from test_framework.config import settings
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import page_loads, page_interactions


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


    def is_text_visible(self, text, selector, by=By.CSS_SELECTOR):
        return page_interactions.is_text_visible(self.driver, text, selector, by)


    def jquery_click(self, selector):
        return self.driver.execute_script("jQuery('%s').click()" % selector)


    def click(self, selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT):
        element = page_loads.wait_for_element_visible(self.driver, selector, by, timeout=timeout)
        return element.click()


    def open(self, url):
        self.driver.get(url)


    def open_url(self, url):
        """ In case people are mixing up self.open() with open() """
        self.driver.get(url)


    def activate_jquery(self):
        """ (It's not on by default on all website pages.) """
        self.driver.execute_script('var script = document.createElement("script"); script.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"; document.getElementsByTagName("head")[0].appendChild(script);')


    def scroll_to(self, selector):
        self.driver.execute_script("jQuery('%s')[0].scrollIntoView()" % selector)


    def scroll_click(self, selector):
        self.scroll_to(selector)
        self.click(selector)


    def jq_format(self, code):
        """ Use before throwing raw code such as 'div[tab="advanced"]' into jQuery. Similar to "json.dumps(value)".
        The first replace should take care of everything. Now see what else there is. """
        code = code.replace('\\','\\\\').replace('\t','    ').replace('\n', '\\n').replace('\"','\\\"').replace('\'','\\\'').replace('\r', '\\r').replace('\v', '\\v').replace('\a', '\\a').replace('\f', '\\f').replace('\b', '\\b').replace('\u', '\\u')
        return code


    def set_value(self, selector, value):
        val = json.dumps(value)
        return self.driver.execute_script("jQuery('%s').val(%s)" % (selector, val))


    def update_text_value(self, selector, new_value, timeout=settings.SMALL_TIMEOUT, retry=False):
        """ This method updates a selector's text value with a new value
            @Params
            selector - the selector with the value to change
            new_value - the new value for the text field where the selector points to
            timeout - how long to want for the selector to be visible before timing out
            retry - if text update fails, try the jQuery version (Warning: don't use this if update_text_value() takes you to
                    a new page, or if it resets the value (such as using [backslash n] for the enter key) """
        element = self.wait_for_element_visible(selector, timeout=timeout)
        element.clear()
        element.send_keys(new_value)

        if retry:
            if element.get_attribute('value') != new_value:
                logging.debug('update_text_value is falling back to jQuery!')
                # Since selectors with quotes inside of quotes such as 'div[data-tab-name="advanced"]' break jQuery, format them first
                selector = self.jq_format(selector)
                self.set_value(selector, new_value)


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


    def wait_for_and_switch_to_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_loads.wait_for_and_switch_to_alert(self.driver, timeout)
