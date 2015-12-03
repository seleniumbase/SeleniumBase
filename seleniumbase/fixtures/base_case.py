"""
These methods improve on and expand existing WebDriver commands.
Improvements include making WebDriver commands more robust and more reliable
by giving page elements enough time to load before taking action on them.
"""

import json
import logging
import os
import pytest
import sys
import unittest
from seleniumbase.config import settings
from seleniumbase.core import browser_launcher
from seleniumbase.core import log_helper
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import page_actions
import page_utils


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

    def setUp(self):
        """
        pytest-specific code
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass setUp() method:
        super(SubClassOfBaseCase, self).setUp()
        """
        self.is_pytest = None
        try:
            # This raises an exception if the test is not coming from pytest
            self.is_pytest = pytest.config.option.is_pytest
        except Exception:
            # Not using pytest (probably nosetests)
            self.is_pytest = False
        if self.is_pytest:
            self.with_selenium = pytest.config.option.with_selenium
            self.with_testing_base = pytest.config.option.with_testing_base
            self.log_path = pytest.config.option.log_path
            self.browser = pytest.config.option.browser
            self.data = pytest.config.option.data
            if self.with_selenium:
                self.driver = browser_launcher.get_driver(self.browser)

    def tearDown(self):
        """
        pytest-specific code
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass's tearDown():
        super(SubClassOfBaseCase, self).tearDown()
        """
        if self.is_pytest:
            if self.with_selenium:
                # Save a screenshot if logging is on when an exception occurs
                if self.with_testing_base and (sys.exc_info()[1] is not None):
                    test_id = "%s.%s.%s" % (self.__class__.__module__,
                                            self.__class__.__name__,
                                            self._testMethodName)
                    test_logpath = self.log_path + "/" + test_id
                    if not os.path.exists(test_logpath):
                        os.makedirs(test_logpath)
                    # Handle screenshot logging
                    log_helper.log_screenshot(test_logpath, self.driver)
                    # Handle basic test info logging
                    log_helper.log_test_failure_data(
                        test_logpath, self.driver, self.browser)
                    # Handle page source logging
                    log_helper.log_page_source(test_logpath, self.driver)

                # Finally close the browser
                self.driver.quit()

    def open(self, url):
        self.driver.get(url)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            self.wait_for_ready_state_complete()

    def open_url(self, url):
        """ In case people are mixing up self.open() with open(),
            use this alternative. """
        self.open(url)

    def click(self, selector, by=By.CSS_SELECTOR,
              timeout=settings.SMALL_TIMEOUT):
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()

    def click_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        element = self.wait_for_link_text_visible(link_text, timeout=timeout)
        element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()

    def update_text_value(self, selector, new_value,
                          timeout=settings.SMALL_TIMEOUT, retry=False):
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
        if (retry and element.get_attribute('value') != new_value
                and not new_value.endswith('\n')):
            logging.debug('update_text_value is falling back to jQuery!')
            selector = self.jq_format(selector)
            self.set_value(selector, new_value)

    def is_element_present(self, selector, by=By.CSS_SELECTOR):
        return page_actions.is_element_present(self.driver, selector, by)

    def is_element_visible(self, selector, by=By.CSS_SELECTOR):
        return page_actions.is_element_visible(self.driver, selector, by)

    def is_link_text_visible(self, link_text):
        return page_actions.is_element_visible(self.driver, link_text,
                                               by=By.LINK_TEXT)

    def is_text_visible(self, text, selector, by=By.CSS_SELECTOR):
        return page_actions.is_text_visible(self.driver, text, selector, by)

    def find_visible_elements(self, selector, by=By.CSS_SELECTOR):
        return page_actions.find_visible_elements(self.driver, selector, by)

    def execute_script(self, script):
        return self.driver.execute_script(script)

    def set_window_size(self, width, height):
        return self.driver.set_window_size(width, height)

    def maximize_window(self):
        return self.driver.maximize_window()

    def activate_jquery(self):
        """ (It's not on by default on all website pages.) """
        self.driver.execute_script(
            '''var script = document.createElement("script"); '''
            '''script.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/'''
            '''jquery.min.js"; document.getElementsByTagName("head")[0]'''
            '''.appendChild(script);''')

    def scroll_to(self, selector):
        self.wait_for_element_visible(selector, timeout=settings.SMALL_TIMEOUT)
        self.driver.execute_script(
            "jQuery('%s')[0].scrollIntoView()" % selector)

    def scroll_click(self, selector):
        self.scroll_to(selector)
        self.click(selector)

    def jquery_click(self, selector):
        self.driver.execute_script("jQuery('%s').click()" % selector)

    def jq_format(self, code):
        return page_utils.jq_format(code)

    def set_value(self, selector, value):
        val = json.dumps(value)
        self.driver.execute_script("jQuery('%s').val(%s)" % (selector, val))

    def jquery_update_text_value(self, selector, new_value,
                                 timeout=settings.SMALL_TIMEOUT):
        element = self.wait_for_element_visible(selector, timeout=timeout)
        self.driver.execute_script("""jQuery('%s').val('%s')"""
                                   % (selector, self.jq_format(new_value)))
        if new_value.endswith('\n'):
            element.send_keys('\n')

    def hover_on_element(self, selector):
        return page_actions.hover_on_element(self.driver, selector)

    def hover_and_click(self, hover_selector, click_selector,
                        click_by=By.CSS_SELECTOR,
                        timeout=settings.SMALL_TIMEOUT):
        return page_actions.hover_and_click(self.driver, hover_selector,
                                            click_selector, click_by, timeout)

    def wait_for_element_present(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)

    def wait_for_element_visible(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)

    def wait_for_text_visible(self, text, selector, by=By.CSS_SELECTOR,
                              timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_text_visible(
            self.driver, text, selector, by, timeout)

    def wait_for_link_text_visible(self, link_text,
                                   timeout=settings.LARGE_TIMEOUT):
        return self.wait_for_element_visible(
            link_text, by=By.LINK_TEXT, timeout=timeout)

    def wait_for_element_absent(self, selector, by=By.CSS_SELECTOR,
                                timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_element_absent(
            self.driver, selector, by, timeout)

    def wait_for_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                     timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_element_not_visible(
            self.driver, selector, by, timeout)

    def wait_for_ready_state_complete(self, timeout=settings.EXTREME_TIMEOUT):
        return page_actions.wait_for_ready_state_complete(self.driver, timeout)

    def wait_for_and_accept_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def wait_for_and_dismiss_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def wait_for_and_switch_to_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)
