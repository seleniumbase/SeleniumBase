"""
BaseCase gathers SeleniumBase libraries into a single file for easy calling.
Usage:

    from seleniumbase import BaseCase
    class MyTestClass(BaseCase):
        test_anything(self):
            # Write your code here. Example:
            self.open("https://github.com/")
            self.update_text("input.header-search-input", "SeleniumBase\n")
            self.click('a[href="/seleniumbase/SeleniumBase"]')
            self.assert_element("div.repository-content")
            ....

The methods here expand and improve existing WebDriver commands.
Improvements include making WebDriver more robust and more reliable.
Page elements are given enough time to load before taking action on them.
Code becomes greatly simplified and easier to maintain.
"""

import getpass
import json
import logging
import math
import os
import pytest
import sys
import time
import traceback
import unittest
import uuid
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from seleniumbase.common import decorators
from seleniumbase.config import settings
from seleniumbase.core.application_manager import ApplicationManager
from seleniumbase.core.s3_manager import S3LoggingBucket
from seleniumbase.core.testcase_manager import ExecutionQueryPayload
from seleniumbase.core.testcase_manager import TestcaseDataPayload
from seleniumbase.core.testcase_manager import TestcaseManager
from seleniumbase.core import browser_launcher
from seleniumbase.core import download_helper
from seleniumbase.core import log_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import page_actions
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import xpath_to_css
from selenium.common.exceptions import (StaleElementReferenceException,
                                        WebDriverException)
from selenium.common import exceptions as selenium_exceptions
try:
    # Selenium 3 (ElementNotInteractableException does not exist in selenium 2)
    ENI_Exception = selenium_exceptions.ElementNotInteractableException
except Exception:
    # Selenium 2 (Keep compatibility with seleneium 2.53.6 if still being used)
    ENI_Exception = selenium_exceptions.ElementNotSelectableException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains


class BaseCase(unittest.TestCase):
    '''
    A base test case that wraps methods for enhanced usage.
    You can also add your own methods here.
    '''

    def __init__(self, *args, **kwargs):
        super(BaseCase, self).__init__(*args, **kwargs)
        try:
            self.driver = WebDriver()
        except Exception:
            pass
        self.environment = None
        self._last_url_of_delayed_assert = "data:,"
        self._page_check_count = 0
        self._page_check_failures = []
        self._html_report_extra = []

    def open(self, url):
        self.driver.get(url)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            self.wait_for_ready_state_complete()
        self._demo_mode_pause_if_active()

    def open_url(self, url):
        """ In case people are mixing up self.open() with open(),
            use this alternative. """
        self.open(url)

    def click(self, selector, by=By.CSS_SELECTOR,
              timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
            if not self.is_link_text_visible(selector):
                # Handle a special case of links hidden in dropdowns
                self.click_link_text(selector, timeout=timeout)
                return
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self._scroll_to_element(element)
        pre_action_url = self.driver.current_url
        try:
            element.click()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout=timeout)
            element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)

    def double_click(self, selector, by=By.CSS_SELECTOR,
                     timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self._scroll_to_element(element)
        pre_action_url = self.driver.current_url
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.double_click(element)
            actions.perform()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout=timeout)
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.double_click(element)
            actions.perform()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)

    def click_chain(self, selectors_list, by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT, spacing=0):
        """ This method clicks on a list of elements in succession.
            'spacing' is the amount of time to wait between clicks. (sec) """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        for selector in selectors_list:
            self.click(selector, by=by, timeout=timeout)
            if spacing > 0:
                time.sleep(spacing)

    def is_link_text_present(self, link_text):
        """ Returns True if the link text appears in the HTML of the page.
            The element doesn't need to be visible,
            such as elements hidden inside a dropdown selection. """
        self.wait_for_ready_state_complete()
        source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        html_links = soup.find_all('a')
        for html_link in html_links:
            if html_link.text.strip() == link_text.strip():
                return True
        return False

    def get_link_text_attribute(self, link_text, attribute):
        self.wait_for_ready_state_complete()
        source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        html_links = soup.find_all('a')
        for html_link in html_links:
            if html_link.text.strip() == link_text.strip():
                if html_link.has_attr(attribute):
                    attribute_value = html_link.get(attribute)
                    return attribute_value
                raise Exception(
                    'Could not parse link from link_text [%s]' % link_text)
        raise Exception("Link Text [%s] was not found!" % link_text)

    def wait_for_link_text_present(self, link_text,
                                   timeout=settings.SMALL_TIMEOUT):
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 5)):
            try:
                if not self.is_link_text_present(link_text):
                    raise Exception("Link text [%s] not found!" % link_text)
                return
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.2)
        raise Exception(
            "Link text [%s] was not present after %s seconds!" % (
                link_text, timeout))

    def click_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ This method clicks link text on a page """
        # If using phantomjs, might need to extract and open the link directly
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if self.browser == 'phantomjs':
            if self.is_link_text_visible(link_text):
                element = self.wait_for_link_text_visible(link_text)
                element.click()
                return
            self.open(self._get_href_from_link_text(link_text))
            return
        if not self.is_link_text_present(link_text):
            self.wait_for_link_text_present(link_text)
        pre_action_url = self.get_current_url()
        try:
            element = self.wait_for_link_text_visible(
                link_text, timeout=0.2)
            self._demo_mode_highlight_if_active(link_text, by=By.LINK_TEXT)
            try:
                element.click()
            except (StaleElementReferenceException, ENI_Exception):
                self.wait_for_ready_state_complete()
                time.sleep(0.05)
                element = self.wait_for_link_text_visible(
                    link_text, timeout=timeout)
                element.click()
        except Exception:
            hidden_css = None
            try:
                href = self._get_href_from_link_text(link_text)
                link_css = '[href="%s"]' % href
                if self.is_element_visible(link_css):
                    self.click(link_css)
                else:
                    hidden_css = link_css
                    raise Exception("Element %s is not clickable!" % link_css)
            except Exception:
                try:
                    ng_click = self._get_ng_click_from_link_text(link_text)
                    link_css = '[ng-click="%s"]' % (ng_click)
                    if self.is_element_visible(link_css):
                        self.click(link_css)
                    else:
                        if not hidden_css:
                            hidden_css = link_css
                        raise Exception(
                            "Element %s is not clickable!" % link_css)
                except Exception:
                    # The link text is probably hidden under a dropdown menu
                    if not self._click_dropdown_link_text(link_text,
                                                          hidden_css):
                        element = self.wait_for_link_text_visible(
                            link_text, timeout=settings.MINI_TIMEOUT)
                        element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)

    def click_link(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ Same as self.click_link_text() """
        self.click_link_text(link_text, timeout=timeout)

    def click_partial_link_text(self, partial_link_text,
                                timeout=settings.SMALL_TIMEOUT):
        """ This method clicks the partial link text on a page. """
        # If using phantomjs, might need to extract and open the link directly
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if self.browser == 'phantomjs':
            if self.is_partial_link_text_visible(partial_link_text):
                element = self.wait_for_partial_link_text(partial_link_text)
                element.click()
                return
            source = self.get_page_source()
            soup = BeautifulSoup(source, "html.parser")
            html_links = soup.fetch('a')
            for html_link in html_links:
                if partial_link_text in html_link.text:
                    for html_attribute in html_link.attrs:
                        if html_attribute[0] == 'href':
                            href = html_attribute[1]
                            if href.startswith('//'):
                                link = "http:" + href
                            elif href.startswith('/'):
                                url = self.driver.current_url
                                domain_url = self.get_domain_url(url)
                                link = domain_url + href
                            else:
                                link = href
                            self.open(link)
                            return
                    raise Exception(
                        'Could not parse link from partial link_text '
                        '[%s]' % partial_link_text)
            raise Exception(
                "Partial link text [%s] was not found!" % partial_link_text)
        # Not using phantomjs
        element = self.wait_for_partial_link_text(
            partial_link_text, timeout=timeout)
        self._demo_mode_highlight_if_active(
            partial_link_text, by=By.PARTIAL_LINK_TEXT)
        pre_action_url = self.driver.current_url
        try:
            element.click()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = self.wait_for_partial_link_text(
                partial_link_text, timeout=timeout)
            element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)

    def get_text(self, selector, by=By.CSS_SELECTOR,
                 timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)
        try:
            element_text = element.text
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout)
            element_text = element.text
        return element_text

    def get_attribute(self, selector, attribute, by=By.CSS_SELECTOR,
                      timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)
        try:
            attribute_value = element.get_attribute(attribute)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = page_actions.wait_for_element_present(
                self.driver, selector, by, timeout)
            attribute_value = element.get_attribute(attribute)
        if attribute_value is not None:
            return attribute_value
        else:
            raise Exception("Element [%s] has no attribute [%s]!" % (
                selector, attribute))

    def refresh_page(self):
        self.driver.refresh()

    def refresh(self):
        """ The shorter version of self.refresh_page() """
        self.driver.refresh()

    def get_current_url(self):
        return self.driver.current_url

    def get_page_source(self):
        return self.driver.page_source

    def get_page_title(self):
        return self.driver.title

    def get_title(self):
        """ The shorter version of self.get_page_title() """
        return self.driver.title

    def go_back(self):
        self.driver.back()

    def go_forward(self):
        self.driver.forward()

    def get_image_url(self, selector, by=By.CSS_SELECTOR,
                      timeout=settings.SMALL_TIMEOUT):
        """ Extracts the URL from an image element on the page. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.get_attribute(selector,
                                  attribute='src', by=by, timeout=timeout)

    def add_text(self, selector, new_value, by=By.CSS_SELECTOR,
                 timeout=settings.LARGE_TIMEOUT):
        """ The more-reliable version of driver.send_keys()
            Similar to update_text(), but won't clear the text field first. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self._scroll_to_element(element)
        pre_action_url = self.driver.current_url
        try:
            if not new_value.endswith('\n'):
                element.send_keys(new_value)
            else:
                new_value = new_value[:-1]
                element.send_keys(new_value)
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            if not new_value.endswith('\n'):
                element.send_keys(new_value)
            else:
                new_value = new_value[:-1]
                element.send_keys(new_value)
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)

    def send_keys(self, selector, new_value, by=By.CSS_SELECTOR,
                  timeout=settings.LARGE_TIMEOUT):
        """ Same as add_text() -> more reliable, but less name confusion. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        self.add_text(selector, new_value, by=by, timeout=timeout)

    def update_text_value(self, selector, new_value, by=By.CSS_SELECTOR,
                          timeout=settings.LARGE_TIMEOUT, retry=False):
        """ This method updates an element's text value with a new value.
            @Params
            selector - the selector with the value to update
            new_value - the new value for setting the text field
            by - the type of selector to search by (Default: CSS)
            timeout - how long to wait for the selector to be visible
            retry - if True, use jquery if the selenium text update fails
        """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self._scroll_to_element(element)
        try:
            element.clear()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            element.clear()
        self._demo_mode_pause_if_active(tiny=True)
        pre_action_url = self.driver.current_url
        try:
            if not new_value.endswith('\n'):
                element.send_keys(new_value)
            else:
                new_value = new_value[:-1]
                element.send_keys(new_value)
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            element.clear()
            if not new_value.endswith('\n'):
                element.send_keys(new_value)
            else:
                new_value = new_value[:-1]
                element.send_keys(new_value)
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        if (retry and element.get_attribute('value') != new_value and (
                not new_value.endswith('\n'))):
            logging.debug('update_text_value is falling back to jQuery!')
            selector = self.jq_format(selector)
            self.set_value(selector, new_value, by=by)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)

    def update_text(self, selector, new_value, by=By.CSS_SELECTOR,
                    timeout=settings.LARGE_TIMEOUT, retry=False):
        """ The shorter version of update_text_value(), which
            clears existing text and adds new text into the text field.
            We want to keep the old version for backward compatibility. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        self.update_text_value(selector, new_value, by=by,
                               timeout=timeout, retry=retry)

    def is_element_present(self, selector, by=By.CSS_SELECTOR):
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.is_element_present(self.driver, selector, by)

    def is_element_visible(self, selector, by=By.CSS_SELECTOR):
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.is_element_visible(self.driver, selector, by)

    def is_link_text_visible(self, link_text):
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        return page_actions.is_element_visible(self.driver, link_text,
                                               by=By.LINK_TEXT)

    def is_partial_link_text_visible(self, partial_link_text):
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        return page_actions.is_element_visible(self.driver, partial_link_text,
                                               by=By.PARTIAL_LINK_TEXT)

    def is_text_visible(self, text, selector, by=By.CSS_SELECTOR):
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.is_text_visible(self.driver, text, selector, by)

    def find_visible_elements(self, selector, by=By.CSS_SELECTOR):
        """ Returns a list of matching WebElements that are visible. """
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.find_visible_elements(self.driver, selector, by)

    def is_element_in_frame(self, selector, by=By.CSS_SELECTOR):
        """ Returns True if the selector's element is located in an iFrame.
            Otherwise returns False. """
        selector, by = self._recalculate_selector(selector, by)
        if self.is_element_present(selector, by=by):
            return False
        source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        iframe_list = soup.select('iframe')
        for iframe in iframe_list:
            iframe_identifier = None
            if iframe.has_attr('name') and len(iframe['name']) > 0:
                iframe_identifier = iframe['name']
            elif iframe.has_attr('id') and len(iframe['id']) > 0:
                iframe_identifier = iframe['id']
            else:
                continue
            self.switch_to_frame(iframe_identifier)
            if self.is_element_present(selector, by=by):
                self.switch_to_default_content()
                return True
            self.switch_to_default_content()
        return False

    def enter_frame_of_element(self, selector, by=By.CSS_SELECTOR):
        """ Returns the frame name of the selector's element if in an iFrame.
            Also enters the iFrame if the element was inside an iFrame.
            If the element is not in an iFrame, returns None. """
        selector, by = self._recalculate_selector(selector, by)
        if self.is_element_present(selector, by=by):
            return None
        source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        iframe_list = soup.select('iframe')
        for iframe in iframe_list:
            iframe_identifier = None
            if iframe.has_attr('name') and len(iframe['name']) > 0:
                iframe_identifier = iframe['name']
            elif iframe.has_attr('id') and len(iframe['id']) > 0:
                iframe_identifier = iframe['id']
            else:
                continue
            self.switch_to_frame(iframe_identifier)
            if self.is_element_present(selector, by=by):
                return iframe_identifier
            self.switch_to_default_content()
        return None

    def execute_script(self, script):
        return self.driver.execute_script(script)

    def execute_async_script(self, script, timeout=settings.EXTREME_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.driver.set_script_timeout(timeout)
        return self.driver.execute_async_script(script)

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)
        self._demo_mode_pause_if_active()

    def maximize_window(self):
        self.driver.maximize_window()
        self._demo_mode_pause_if_active()

    def activate_jquery(self):
        """ If "jQuery is not defined", use this method to activate it for use.
            This happens because jQuery is not always defined on web sites. """
        try:
            # Let's first find out if jQuery is already defined.
            self.execute_script("jQuery('html')")
            # Since that command worked, jQuery is defined. Let's return.
            return
        except Exception:
            # jQuery is not currently defined. Let's proceed by defining it.
            pass
        self.execute_script(
            '''var script = document.createElement("script"); '''
            '''script.src = "http://code.jquery.com/jquery-3.2.1.min.js"; '''
            '''document.getElementsByTagName("head")[0]'''
            '''.appendChild(script);''')
        for x in range(30):
            # jQuery needs a small amount of time to activate. (At most 3s)
            try:
                self.execute_script("jQuery('html')")
                return
            except Exception:
                time.sleep(0.1)
        # Since jQuery still isn't activating, give up and raise an exception
        raise Exception("Exception: WebDriver could not activate jQuery!")

    def bring_to_front(self, selector, by=By.CSS_SELECTOR):
        """ Updates the Z-index of a page element to bring it into view.
            Useful when getting a WebDriverException, such as the one below:
                { Element is not clickable at point (#, #).
                  Other element would receive the click: ... } """
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        self.find_element(selector, by=by, timeout=settings.SMALL_TIMEOUT)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't perform action if can't convert to CSS_SELECTOR for jQuery
            return

        script = ("""document.querySelector('%s').style.zIndex = "1";"""
                  % selector)
        self.execute_script(script)

    def highlight(self, selector, by=By.CSS_SELECTOR,
                  loops=settings.HIGHLIGHTS, scroll=True):
        """ This method uses fancy javascript to highlight an element.
            Used during demo_mode.
            @Params
            selector - the selector of the element to find
            by - the type of selector to search by (Default: CSS)
            loops - # of times to repeat the highlight animation
                    (Default: 4. Each loop lasts for about 0.18s)
            scroll - the option to scroll to the element first (Default: True)
        """
        selector, by = self._recalculate_selector(selector, by)
        element = self.find_element(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if scroll:
            self._slow_scroll_to_element(element)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't highlight if can't convert to CSS_SELECTOR for jQuery
            return
        selector = self._make_css_match_first_element_only(selector)

        o_bs = ''  # original_box_shadow
        style = element.get_attribute('style')
        if style:
            if 'box-shadow: ' in style:
                box_start = style.find('box-shadow: ')
                box_end = style.find(';', box_start) + 1
                original_box_shadow = style[box_start:box_end]
                o_bs = original_box_shadow

        script = """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(128, 128, 128, 0.5)');""" % selector
        self.safe_execute_script(script)

        if self.highlights:
            loops = self.highlights
        loops = int(loops)
        for n in range(loops):
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(255, 0, 0, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.02)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(128, 0, 128, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.02)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(0, 0, 255, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.02)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(0, 255, 0, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.02)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(128, 128, 0, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.02)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(128, 0, 128, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.02)

        script = """jQuery('%s').css('box-shadow', '%s');""" % (selector, o_bs)
        self.execute_script(script)
        time.sleep(0.065)

    def scroll_to(self, selector, by=By.CSS_SELECTOR,
                  timeout=settings.SMALL_TIMEOUT):
        ''' Fast scroll to destination '''
        if self.demo_mode:
            self.slow_scroll_to(selector, by=by, timeout=timeout)
            return
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        try:
            self._scroll_to_element(element)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            self._scroll_to_element(element)

    def slow_scroll_to(self, selector, by=By.CSS_SELECTOR,
                       timeout=settings.SMALL_TIMEOUT):
        ''' Slow motion scroll to destination '''
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._slow_scroll_to_element(element)

    def scroll_click(self, selector, by=By.CSS_SELECTOR):
        # DEPRECATED - self.click() now scrolls to the element before clicking
        # self.scroll_to(selector, by=by)
        self.click(selector, by=by)

    def click_xpath(self, xpath):
        self.click(xpath, by=By.XPATH)

    def jquery_click(self, selector, by=By.CSS_SELECTOR):
        selector, by = self._recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if self.is_element_visible(selector, by=by):
            self._demo_mode_highlight_if_active(selector, by)
        selector = self._make_css_match_first_element_only(selector)
        click_script = """jQuery('%s')[0].click()""" % selector
        self.safe_execute_script(click_script)
        self._demo_mode_pause_if_active()

    def hide_element(self, selector, by=By.CSS_SELECTOR):
        """ Hide the first element on the page that matches the selector. """
        selector, by = self._recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self._make_css_match_first_element_only(selector)
        hide_script = """jQuery('%s').hide()""" % selector
        self.safe_execute_script(hide_script)

    def hide_elements(self, selector, by=By.CSS_SELECTOR):
        """ Hide all elements on the page that match the selector. """
        selector, by = self._recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        hide_script = """jQuery('%s').hide()""" % selector
        self.safe_execute_script(hide_script)

    def show_element(self, selector, by=By.CSS_SELECTOR):
        """ Show the first element on the page that matches the selector. """
        selector, by = self._recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self._make_css_match_first_element_only(selector)
        show_script = """jQuery('%s').show(0)""" % selector
        self.safe_execute_script(show_script)

    def show_elements(self, selector, by=By.CSS_SELECTOR):
        """ Show all elements on the page that match the selector. """
        selector, by = self._recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        show_script = """jQuery('%s').show(0)""" % selector
        self.safe_execute_script(show_script)

    def remove_element(self, selector, by=By.CSS_SELECTOR):
        """ Remove the first element on the page that matches the selector. """
        selector, by = self._recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self._make_css_match_first_element_only(selector)
        remove_script = """jQuery('%s').remove()""" % selector
        self.safe_execute_script(remove_script)

    def remove_elements(self, selector, by=By.CSS_SELECTOR):
        """ Remove all elements on the page that match the selector. """
        selector, by = self._recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        remove_script = """jQuery('%s').remove()""" % selector
        self.safe_execute_script(remove_script)

    def jq_format(self, code):
        return page_utils.jq_format(code)

    def get_domain_url(self, url):
        return page_utils.get_domain_url(url)

    def safe_execute_script(self, script):
        """ When executing a script that contains a jQuery command,
            it's important that the jQuery library has been loaded first.
            This method will load jQuery if it wasn't already loaded. """
        try:
            self.execute_script(script)
        except Exception:
            # The likely reason this fails is because: "jQuery is not defined"
            self.activate_jquery()  # It's a good thing we can define it here
            self.execute_script(script)

    def download_file(self, file_url, destination_folder=None):
        """ Downloads the file from the url to the destination folder.
            If no destination folder is specified, the default one is used. """
        if not destination_folder:
            destination_folder = constants.Files.DOWNLOADS_FOLDER
        page_utils._download_file_to(file_url, destination_folder)

    def save_file_as(self, file_url, new_file_name, destination_folder=None):
        """ Similar to self.download_file(), except that you get to rename the
            file being downloaded to whatever you want. """
        if not destination_folder:
            destination_folder = constants.Files.DOWNLOADS_FOLDER
        page_utils._download_file_to(
            file_url, destination_folder, new_file_name)

    def get_downloads_folder(self):
        """ Returns the OS path of the Downloads Folder.
            (Works with Chrome and Firefox only, for now.) """
        return download_helper.get_downloads_folder()

    def get_path_of_downloaded_file(self, file):
        """ Returns the OS path of the downloaded file. """
        return os.path.join(self.get_downloads_folder(), file)

    def is_downloaded_file_present(self, file):
        """ Checks if the file exists in the Downloads Folder. """
        return os.path.exists(self.get_path_of_downloaded_file(file))

    def assert_downloaded_file(self, file):
        """ Asserts that the file exists in the Downloads Folder. """
        assert os.path.exists(self.get_path_of_downloaded_file(file))

    def convert_xpath_to_css(self, xpath):
        return xpath_to_css.convert_xpath_to_css(xpath)

    def convert_to_css_selector(self, selector, by):
        """ This method converts a selector to a CSS_SELECTOR.
            jQuery commands require a CSS_SELECTOR for finding elements.
            This method should only be used for jQuery actions. """
        if by == By.CSS_SELECTOR:
            return selector
        elif by == By.ID:
            return '#%s' % selector
        elif by == By.CLASS_NAME:
            return '.%s' % selector
        elif by == By.NAME:
            return '[name="%s"]' % selector
        elif by == By.TAG_NAME:
            return selector
        elif by == By.XPATH:
            return self.convert_xpath_to_css(selector)
        elif by == By.LINK_TEXT:
            return 'a:contains("%s")' % selector
        elif by == By.PARTIAL_LINK_TEXT:
            return 'a:contains("%s")' % selector
        else:
            raise Exception(
                "Exception: Could not convert [%s](by=%s) to CSS_SELECTOR!" % (
                    selector, by))

    def set_value(self, selector, new_value, by=By.CSS_SELECTOR,
                  timeout=settings.LARGE_TIMEOUT):
        """ This method uses jQuery to update a text field. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        selector = self.convert_to_css_selector(selector, by=by)
        self._demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by, timeout=timeout)
        value = json.dumps(new_value)
        selector = self._make_css_match_first_element_only(selector)
        set_value_script = """jQuery('%s').val(%s)""" % (selector, value)
        self.safe_execute_script(set_value_script)
        self._demo_mode_pause_if_active()

    def jquery_update_text_value(self, selector, new_value, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        """ This method uses jQuery to update a text field.
            If the new_value string ends with the newline character,
            WebDriver will finish the call, which simulates pressing
            {Enter/Return} after the text is entered.  """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self._make_css_match_first_element_only(selector)
        update_text_script = """jQuery('%s').val('%s')""" % (
            selector, self.jq_format(new_value))
        self.safe_execute_script(update_text_script)
        if new_value.endswith('\n'):
            element.send_keys('\n')
        self._demo_mode_pause_if_active()

    def jquery_update_text(self, selector, new_value, by=By.CSS_SELECTOR,
                           timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of jquery_update_text_value()
            (The longer version remains for backwards compatibility.) """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.jquery_update_text_value(
            selector, new_value, by=by, timeout=timeout)

    def hover_on_element(self, selector, by=By.CSS_SELECTOR):
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        self._demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        time.sleep(0.05)  # Settle down from scrolling before hovering
        return page_actions.hover_on_element(self.driver, selector)

    def hover_and_click(self, hover_selector, click_selector,
                        hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                        timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(hover_selector):
            hover_by = By.XPATH
        if page_utils.is_xpath_selector(click_selector):
            click_by = By.XPATH
        self.wait_for_element_visible(
            hover_selector, by=hover_by, timeout=timeout)
        self._demo_mode_highlight_if_active(hover_selector, hover_by)
        self.scroll_to(hover_selector, by=hover_by)
        pre_action_url = self.driver.current_url
        element = page_actions.hover_and_click(
                self.driver, hover_selector, click_selector,
                hover_by, click_by, timeout)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)
        return element

    def pick_select_option_by_text(self, dropdown_selector, option,
                                   dropdown_by=By.CSS_SELECTOR,
                                   timeout=settings.LARGE_TIMEOUT):
        """ Picks an HTML <select> option by option text. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self._pick_select_option(dropdown_selector, option,
                                 dropdown_by=dropdown_by, option_by="text",
                                 timeout=timeout)

    def pick_select_option_by_index(self, dropdown_selector, option,
                                    dropdown_by=By.CSS_SELECTOR,
                                    timeout=settings.LARGE_TIMEOUT):
        """ Picks an HTML <select> option by option index. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self._pick_select_option(dropdown_selector, option,
                                 dropdown_by=dropdown_by, option_by="index",
                                 timeout=timeout)

    def pick_select_option_by_value(self, dropdown_selector, option,
                                    dropdown_by=By.CSS_SELECTOR,
                                    timeout=settings.LARGE_TIMEOUT):
        """ Picks an HTML <select> option by option value. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self._pick_select_option(dropdown_selector, option,
                                 dropdown_by=dropdown_by, option_by="value",
                                 timeout=timeout)

    def generate_referral(self, start_page, destination_page):
        """ This method opens the start_page, creates a referral link there,
            and clicks on that link, which goes to the destination_page.
            (This generates real traffic for testing analytics software.) """
        if not page_utils.is_valid_url(destination_page):
            raise Exception(
                "Exception: destination_page [%s] is not a valid URL!"
                % destination_page)
        if start_page:
            if not page_utils.is_valid_url(start_page):
                raise Exception(
                    "Exception: start_page [%s] is not a valid URL! "
                    "(Use an empty string or None to start from current page.)"
                    % start_page)
            self.open(start_page)
            time.sleep(0.08)
        referral_link = ('''<a class='analytics referral test' href='%s' '''
                         '''style='font-family: Arial,sans-serif; '''
                         '''font-size: 30px; color: #18a2cd'>'''
                         '''* Magic Link Button! *</a>''' % destination_page)
        self.execute_script(
            '''document.body.innerHTML = \"%s\"''' % referral_link)
        time.sleep(0.1)
        self.click("a.analytics.referral.test")  # Clicks the generated button
        time.sleep(0.12)

    def generate_traffic(self, start_page, destination_page, loops=1):
        """ Similar to generate_referral(), but can do multiple loops. """
        for loop in range(loops):
            self.generate_referral(start_page, destination_page)
            time.sleep(0.05)

    ############

    def wait_for_element_present(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to appear in the HTML of a page.
            The element does not need be visible (it may be hidden). """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)

    def assert_element_present(self, selector, by=By.CSS_SELECTOR,
                               timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_present(), but returns nothing.
            Waits for an element to appear in the HTML of a page.
            The element does not need be visible (it may be hidden).
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_element_visible(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to appear in the HTML of a page.
            The element must be visible (it cannot be hidden). """
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)

    def wait_for_element(self, selector, by=By.CSS_SELECTOR,
                         timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_element_visible() """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def find_element(self, selector, by=By.CSS_SELECTOR,
                     timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_element_visible() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def assert_element(self, selector, by=By.CSS_SELECTOR,
                       timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.wait_for_element_visible(selector, by=by, timeout=timeout)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_text_visible(self, text, selector, by=By.CSS_SELECTOR,
                              timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.wait_for_text_visible(
            self.driver, text, selector, by, timeout)

    def wait_for_text(self, text, selector, by=By.CSS_SELECTOR,
                      timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_text_visible() """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def find_text(self, text, selector, by=By.CSS_SELECTOR,
                  timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_text_visible() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def assert_text(self, text, selector, by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_text_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_link_text_visible(self, link_text,
                                   timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_element_visible(
            link_text, by=By.LINK_TEXT, timeout=timeout)

    def wait_for_link_text(self, link_text, timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_link_text_visible() """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def find_link_text(self, link_text, timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_link_text_visible() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def assert_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_link_text_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.wait_for_link_text_visible(link_text, timeout=timeout)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_partial_link_text(self, partial_link_text,
                                   timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_element_visible(
            partial_link_text, by=By.PARTIAL_LINK_TEXT, timeout=timeout)

    def find_partial_link_text(self, partial_link_text,
                               timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_partial_link_text() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return self.wait_for_partial_link_text(
            partial_link_text, timeout=timeout)

    def assert_partial_link_text(self, partial_link_text,
                                 timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_partial_link_text(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.wait_for_partial_link_text(partial_link_text, timeout=timeout)
        return True

    ############

    def wait_for_element_absent(self, selector, by=By.CSS_SELECTOR,
                                timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to no longer appear in the HTML of a page.
            A hidden element still counts as appearing in the page HTML.
            If an element with "hidden" status is acceptable,
            use wait_for_element_not_visible() instead. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        return page_actions.wait_for_element_absent(
            self.driver, selector, by, timeout)

    def assert_element_absent(self, selector, by=By.CSS_SELECTOR,
                              timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_absent() - returns nothing.
            As above, will raise an exception if the element stays present.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.wait_for_element_absent(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                     timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to no longer be visible on a page.
            The element can be non-existant in the HTML or hidden on the page
            to qualify as not visible. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return page_actions.wait_for_element_not_visible(
            self.driver, selector, by, timeout)

    def assert_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                   timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_not_visible() - returns nothing.
            As above, will raise an exception if the element stays visible.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        self.wait_for_element_not_visible(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_ready_state_complete(self, timeout=settings.EXTREME_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        is_ready = page_actions.wait_for_ready_state_complete(self.driver,
                                                              timeout)
        self.wait_for_angularjs()
        return is_ready

    def wait_for_angularjs(self, timeout=settings.LARGE_TIMEOUT, **kwargs):
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        if not settings.WAIT_FOR_ANGULARJS:
            return

        NG_WRAPPER = '%(prefix)s' \
                     'var $elm=document.querySelector(' \
                     '\'[data-ng-app],[ng-app],.ng-scope\')||document;' \
                     'if(window.angular && angular.getTestability){' \
                     'angular.getTestability($elm).whenStable(%(handler)s)' \
                     '}else{' \
                     'var $inj;try{$inj=angular.element($elm).injector()||' \
                     'angular.injector([\'ng\'])}catch(ex){' \
                     '$inj=angular.injector([\'ng\'])};$inj.get=$inj.get||' \
                     '$inj;$inj.get(\'$browser\').' \
                     'notifyWhenNoOutstandingRequests(%(handler)s)}' \
                     '%(suffix)s'
        def_pre = 'var cb=arguments[arguments.length-1];if(window.angular){'
        prefix = kwargs.pop('prefix', def_pre)
        handler = kwargs.pop('handler', 'function(){cb(true)}')
        suffix = kwargs.pop('suffix', '}else{cb(false)}')
        script = NG_WRAPPER % {'prefix': prefix,
                               'handler': handler,
                               'suffix': suffix}
        try:
            self.execute_async_script(script, timeout=timeout)
        except Exception:
            time.sleep(0.05)

    def wait_for_and_accept_alert(self, timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def wait_for_and_dismiss_alert(self, timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def wait_for_and_switch_to_alert(self, timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)

    def switch_to_frame(self, frame, timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        page_actions.switch_to_frame(self.driver, frame, timeout)

    def switch_to_window(self, window, timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self._get_new_timeout(timeout)
        page_actions.switch_to_window(self.driver, window, timeout)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def save_screenshot(self, name, folder=None):
        return page_actions.save_screenshot(self.driver, name, folder)

    ############

    def _get_new_timeout(self, timeout):
        """ When using --timeout_multiplier=#.# """
        try:
            timeout_multiplier = float(self.timeout_multiplier)
            if timeout_multiplier <= 0.5:
                timeout_multiplier = 0.5
            timeout = int(math.ceil(timeout_multiplier * timeout))
            return timeout
        except Exception:
            # Wrong data type for timeout_multiplier (expecting int or float)
            return timeout

    ############

    def _get_exception_message(self):
        """ This method extracts the message from an exception if there
            was an exception that occurred during the test, assuming
            that the exception was in a try/except block and not thrown. """
        if sys.version.startswith('3') and hasattr(self, '_outcome'):
            exception_info = self._outcome.errors
            if exception_info:
                try:
                    exc_message = exception_info[0][1][1]
                except Exception:
                    exc_message = "(Unknown Exception)"
            else:
                exc_message = "(Unknown Exception)"
        else:
            exception_info = sys.exc_info()[1]
            if hasattr(exception_info, 'msg'):
                exc_message = exception_info.msg
            elif hasattr(exception_info, 'message'):
                exc_message = exception_info.message
            else:
                exc_message = '(Unknown Exception)'
        return exc_message

    def _add_delayed_assert_failure(self):
        """ Add a delayed_assert failure into a list for future processing. """
        current_url = self.driver.current_url
        message = self._get_exception_message()
        self._page_check_failures.append(
                "CHECK #%s: (%s)\n %s" % (
                    self._page_check_count, current_url, message))

    def delayed_assert_element(self, selector, by=By.CSS_SELECTOR,
                               timeout=settings.MINI_TIMEOUT):
        """ A non-terminating assertion for an element on a page.
            Failures will be saved until the process_delayed_asserts()
            method is called from inside a test, likely at the end of it. """
        self._page_check_count += 1
        try:
            url = self.get_current_url()
            if url == self._last_url_of_delayed_assert:
                timeout = 1
            else:
                self._last_url_of_delayed_assert = url
        except Exception:
            pass
        try:
            self.wait_for_element_visible(selector, by=by, timeout=timeout)
            return True
        except Exception:
            self._add_delayed_assert_failure()
            return False

    @decorators.deprecated("Use self.delayed_assert_element() instead!")
    def check_assert_element(self, selector, by=By.CSS_SELECTOR,
                             timeout=settings.MINI_TIMEOUT):
        """ DEPRECATED - Use self.delayed_assert_element() instead. """
        return self.delayed_assert_element(selector, by=by, timeout=timeout)

    def delayed_assert_text(self, text, selector, by=By.CSS_SELECTOR,
                            timeout=settings.MINI_TIMEOUT):
        """ A non-terminating assertion for text from an element on a page.
            Failures will be saved until the process_delayed_asserts()
            method is called from inside a test, likely at the end of it. """
        self._page_check_count += 1
        try:
            url = self.get_current_url()
            if url == self._last_url_of_delayed_assert:
                timeout = 1
            else:
                self._last_url_of_delayed_assert = url
        except Exception:
            pass
        try:
            self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
            return True
        except Exception:
            self._add_delayed_assert_failure()
            return False

    @decorators.deprecated("Use self.delayed_assert_text() instead!")
    def check_assert_text(self, text, selector, by=By.CSS_SELECTOR,
                          timeout=settings.MINI_TIMEOUT):
        """ DEPRECATED - Use self.delayed_assert_text() instead. """
        return self.delayed_assert_text(text, selector, by=by, timeout=timeout)

    def process_delayed_asserts(self, print_only=False):
        """ To be used with any test that uses delayed_asserts, which are
            non-terminating verifications that only raise exceptions
            after this method is called.
            This is useful for pages with multiple elements to be checked when
            you want to find as many bugs as possible in a single test run
            before having all the exceptions get raised simultaneously.
            Might be more useful if this method is called after processing all
            the delayed asserts on a single html page so that the failure
            screenshot matches the location of the delayed asserts.
            If "print_only" is set to True, the exception won't get raised. """
        if self._page_check_failures:
            exception_output = ''
            exception_output += "\n*** DELAYED ASSERTION FAILURES FOR: "
            exception_output += "%s\n" % self.id()
            all_failing_checks = self._page_check_failures
            self._page_check_failures = []
            for tb in all_failing_checks:
                exception_output += "%s\n" % tb
            if print_only:
                print(exception_output)
            else:
                raise Exception(exception_output)

    @decorators.deprecated("Use self.process_delayed_asserts() instead!")
    def process_checks(self, print_only=False):
        """ DEPRECATED - Use self.process_delayed_asserts() instead. """
        self.process_delayed_asserts(print_only=print_only)

    ############

    def _get_href_from_link_text(self, link_text):
        href = self.get_link_text_attribute(link_text, "href")
        if href.startswith('//'):
            link = "http:" + href
        elif href.startswith('/'):
            url = self.driver.current_url
            domain_url = self.get_domain_url(url)
            link = domain_url + href
        else:
            link = href
        return link

    def _get_ng_click_from_link_text(self, link_text):
        ng_click = self.get_link_text_attribute(link_text, "ng-click")
        return ng_click

    def _click_dropdown_link_text(self, link_text, hidden_css):
        """ When a link is hidden under a dropdown menu, use this. """
        source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        drop_down_list = soup.select('[class*=dropdown]')
        csstype = hidden_css.split('[')[1].split('=')[0]
        for item in drop_down_list:
            if link_text in item.text.split('\n') and csstype in item.decode():
                dropdown_css = ""
                for css_class in item['class']:
                    dropdown_css += '.'
                    dropdown_css += css_class
                dropdown_css = item.name + dropdown_css
                matching_dropdowns = self.find_visible_elements(dropdown_css)
                for dropdown in matching_dropdowns:
                    # The same class names might be used for multiple dropdowns
                    try:
                        page_actions.hover_element_and_click(
                            self.driver, dropdown, hidden_css,
                            click_by=By.CSS_SELECTOR, timeout=0.2)
                        return True
                    except Exception:
                        pass
        return False

    def _pick_select_option(self, dropdown_selector, option,
                            dropdown_by=By.CSS_SELECTOR, option_by="text",
                            timeout=settings.SMALL_TIMEOUT):
        """ Picks an HTML <select> option by specification.
            Option specifications are by "text", "index", or "value".
            Defaults to "text" if option_by is unspecified or unknown. """
        element = self.find_element(
            dropdown_selector, by=dropdown_by, timeout=timeout)
        self._demo_mode_highlight_if_active(dropdown_selector, dropdown_by)
        pre_action_url = self.driver.current_url
        try:
            if option_by == "index":
                Select(element).select_by_index(option)
            elif option_by == "value":
                Select(element).select_by_value(option)
            else:
                Select(element).select_by_visible_text(option)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = self.find_element(
                dropdown_selector, by=dropdown_by, timeout=timeout)
            if option_by == "index":
                Select(element).select_by_index(option)
            elif option_by == "value":
                Select(element).select_by_value(option)
            else:
                Select(element).select_by_visible_text(option)
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self._demo_mode_pause_if_active()
            else:
                self._demo_mode_pause_if_active(tiny=True)

    ############

    def _recalculate_selector(self, selector, by):
        # Try to determine the type of selector automatically
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return (selector, by)

    def _make_css_match_first_element_only(self, selector):
        # Only get the first match
        last_syllable = selector.split(' ')[-1]
        if ':' not in last_syllable and ':contains' not in selector:
            selector += ':first'
        return selector

    def _demo_mode_pause_if_active(self, tiny=False):
        if self.demo_mode:
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            else:
                wait_time = settings.DEFAULT_DEMO_MODE_TIMEOUT
            if not tiny:
                time.sleep(wait_time)
            else:
                time.sleep(wait_time/3.4)

    def _demo_mode_scroll_if_active(self, selector, by):
        if self.demo_mode:
            self.slow_scroll_to(selector, by=by)

    def _demo_mode_highlight_if_active(self, selector, by):
        if self.demo_mode:
            # Includes self.slow_scroll_to(selector, by=by) by default
            self.highlight(selector, by=by)

    def _scroll_to_element(self, element):
        element_location = element.location['y']
        element_location = element_location - 130
        if element_location < 0:
            element_location = 0
        scroll_script = "window.scrollTo(0, %s);" % element_location
        # The old jQuery scroll_script required by=By.CSS_SELECTOR
        # scroll_script = "jQuery('%s')[0].scrollIntoView()" % selector
        try:
            self.execute_script(scroll_script)
        except WebDriverException:
            pass  # Older versions of Firefox experienced issues here
        self._demo_mode_pause_if_active(tiny=True)

    def _slow_scroll_to_element(self, element):
        scroll_position = self.execute_script("return window.scrollY;")
        element_location = element.location['y']
        element_location = element_location - 130
        if element_location < 0:
            element_location = 0
        distance = element_location - scroll_position
        if distance != 0:
            total_steps = int(abs(distance) / 50.0) + 2.0
            step_value = float(distance) / total_steps
            new_position = scroll_position
            for y in range(int(total_steps)):
                time.sleep(0.0114)
                new_position += step_value
                scroll_script = "window.scrollTo(0, %s);" % new_position
                self.execute_script(scroll_script)
        time.sleep(0.01)
        scroll_script = "window.scrollTo(0, %s);" % element_location
        self.execute_script(scroll_script)
        time.sleep(0.01)
        if distance > 430 or distance < -300:
            # Add small recovery time for long-distance slow-scrolling
            time.sleep(0.162)

    ############

    def setUp(self):
        """
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
            # pytest-specific code
            test_id = "%s.%s.%s" % (self.__class__.__module__,
                                    self.__class__.__name__,
                                    self._testMethodName)
            self.with_selenium = pytest.config.option.with_selenium
            self.headless = pytest.config.option.headless
            self.headless_active = False
            self.with_testing_base = pytest.config.option.with_testing_base
            self.with_db_reporting = pytest.config.option.with_db_reporting
            self.with_s3_logging = pytest.config.option.with_s3_logging
            self.with_screen_shots = pytest.config.option.with_screen_shots
            self.with_basic_test_info = (
                pytest.config.option.with_basic_test_info)
            self.with_page_source = pytest.config.option.with_page_source
            self.servername = pytest.config.option.servername
            self.port = pytest.config.option.port
            self.proxy_string = pytest.config.option.proxy_string
            self.database_env = pytest.config.option.database_env
            self.log_path = pytest.config.option.log_path
            self.browser = pytest.config.option.browser
            self.data = pytest.config.option.data
            self.demo_mode = pytest.config.option.demo_mode
            self.demo_sleep = pytest.config.option.demo_sleep
            self.highlights = pytest.config.option.highlights
            self.verify_delay = pytest.config.option.verify_delay
            self.timeout_multiplier = pytest.config.option.timeout_multiplier
            self.use_grid = False
            if self.servername != "localhost":
                # Use Selenium Grid (Use --server=127.0.0.1 for localhost Grid)
                self.use_grid = True
            if self.with_db_reporting:
                self.execution_guid = str(uuid.uuid4())
                self.testcase_guid = None
                self.execution_start_time = 0
                self.case_start_time = 0
                self.application = None
                self.testcase_manager = None
                self.error_handled = False
                self.testcase_manager = TestcaseManager(self.database_env)
                #
                exec_payload = ExecutionQueryPayload()
                exec_payload.execution_start_time = int(time.time() * 1000)
                self.execution_start_time = exec_payload.execution_start_time
                exec_payload.guid = self.execution_guid
                exec_payload.username = getpass.getuser()
                self.testcase_manager.insert_execution_data(exec_payload)
                #
                data_payload = TestcaseDataPayload()
                self.testcase_guid = str(uuid.uuid4())
                data_payload.guid = self.testcase_guid
                data_payload.execution_guid = self.execution_guid
                if self.with_selenium:
                    data_payload.browser = self.browser
                else:
                    data_payload.browser = "N/A"
                data_payload.testcaseAddress = test_id
                application = ApplicationManager.generate_application_string(
                    self._testMethodName)
                data_payload.env = application.split('.')[0]
                data_payload.start_time = application.split('.')[1]
                data_payload.state = constants.State.NOTRUN
                self.testcase_manager.insert_testcase_data(data_payload)
                self.case_start_time = int(time.time() * 1000)
            if self.headless:
                self.display = Display(visible=0, size=(1920, 1200))
                self.display.start()
                self.headless_active = True

        # Launch WebDriver for both Pytest and Nosetests
        if not hasattr(self, "browser"):
            raise Exception("""SeleniumBase plugins did not load! """
                            """Please reinstall using:\n"""
                            """ >>> "python setup.py develop" <<< """)
        self.driver = browser_launcher.get_driver(self.browser,
                                                  self.headless,
                                                  self.use_grid,
                                                  self.servername,
                                                  self.port,
                                                  self.proxy_string)

    def __insert_test_result(self, state, err):
        data_payload = TestcaseDataPayload()
        data_payload.runtime = int(time.time() * 1000) - self.case_start_time
        data_payload.guid = self.testcase_guid
        data_payload.execution_guid = self.execution_guid
        data_payload.state = state
        if err:
            tb_string = traceback.format_exc()
            if "Message: " in tb_string:
                data_payload.message = "Message: " + tb_string.split(
                    "Message: ")[-1]
            elif "Exception: " in tb_string:
                data_payload.message = tb_string.split("Exception: ")[-1]
            elif "Error: " in tb_string:
                data_payload.message = tb_string.split("Error: ")[-1]
            else:
                data_payload.message = "Unknown Error: See Stacktrace"
        self.testcase_manager.update_testcase_data(data_payload)

    def _add_pytest_html_extra(self):
        try:
            pytest_html = pytest.config.pluginmanager.getplugin('html')
            if self.with_selenium and pytest_html:
                driver = self.driver
                extra_url = pytest_html.extras.url(driver.current_url)
                screenshot = driver.get_screenshot_as_base64()
                extra_image = pytest_html.extras.image(screenshot,
                                                       name='Screenshot')
                self._html_report_extra.append(extra_url)
                self._html_report_extra.append(extra_image)
        except Exception:
            pass

    def tearDown(self):
        """
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass's tearDown():
        super(SubClassOfBaseCase, self).tearDown()
        """
        has_exception = False
        if sys.version.startswith('3') and hasattr(self, '_outcome'):
            if self._outcome.errors:
                has_exception = True
        else:
            has_exception = sys.exc_info()[1] is not None
        if self._page_check_failures:
            print(
                "\nWhen using self.delayed_assert_*() methods in your tests, "
                "remember to call self.process_delayed_asserts() afterwards. "
                "Now calling in tearDown()...\nFailures Detected:")
            if not has_exception:
                self.process_checks()
            else:
                self.process_checks(print_only=True)
        self.is_pytest = None
        try:
            # This raises an exception if the test is not coming from pytest
            self.is_pytest = pytest.config.option.is_pytest
        except Exception:
            # Not using pytest (probably nosetests)
            self.is_pytest = False
        if self.is_pytest:
            # pytest-specific code
            test_id = "%s.%s.%s" % (self.__class__.__module__,
                                    self.__class__.__name__,
                                    self._testMethodName)
            if self.with_selenium:
                # Save a screenshot if logging is on when an exception occurs
                if has_exception:
                    self._add_pytest_html_extra()
                if self.with_testing_base and has_exception:
                    test_logpath = self.log_path + "/" + test_id
                    if not os.path.exists(test_logpath):
                        os.makedirs(test_logpath)
                    if ((not self.with_screen_shots) and
                            (not self.with_basic_test_info) and
                            (not self.with_page_source)):
                        # Log everything if nothing specified (if testing_base)
                        log_helper.log_screenshot(test_logpath, self.driver)
                        log_helper.log_test_failure_data(
                            self, test_logpath, self.driver, self.browser)
                        log_helper.log_page_source(test_logpath, self.driver)
                    else:
                        if self.with_screen_shots:
                            log_helper.log_screenshot(
                                test_logpath, self.driver)
                        if self.with_basic_test_info:
                            log_helper.log_test_failure_data(
                                self, test_logpath, self.driver, self.browser)
                        if self.with_page_source:
                            log_helper.log_page_source(
                                test_logpath, self.driver)
                # Finally close the browser
                try:
                    self.driver.quit()
                except AttributeError:
                    pass
                except Exception:
                    pass
                self.driver = None
            if self.headless:
                if self.headless_active:
                    self.display.stop()
                    self.display = None
            if self.with_db_reporting:
                if has_exception:
                    self.__insert_test_result(constants.State.ERROR, True)
                else:
                    self.__insert_test_result(constants.State.PASS, False)
                runtime = int(time.time() * 1000) - self.execution_start_time
                self.testcase_manager.update_execution_data(
                    self.execution_guid, runtime)
            if self.with_s3_logging and has_exception:
                """ After each testcase, upload logs to the S3 bucket. """
                s3_bucket = S3LoggingBucket()
                guid = str(uuid.uuid4().hex)
                path = "%s/%s" % (self.log_path, test_id)
                uploaded_files = []
                for logfile in os.listdir(path):
                    logfile_name = "%s/%s/%s" % (guid,
                                                 test_id,
                                                 logfile.split(path)[-1])
                    s3_bucket.upload_file(logfile_name,
                                          "%s/%s" % (path, logfile))
                    uploaded_files.append(logfile_name)
                s3_bucket.save_uploaded_file_names(uploaded_files)
                index_file = s3_bucket.upload_index_file(test_id, guid)
                print("\n\n*** Log files uploaded: ***\n%s\n" % index_file)
                logging.error(
                    "\n\n*** Log files uploaded: ***\n%s\n" % index_file)
                if self.with_db_reporting:
                    self.testcase_manager = TestcaseManager(self.database_env)
                    data_payload = TestcaseDataPayload()
                    data_payload.guid = self.testcase_guid
                    data_payload.logURL = index_file
                    self.testcase_manager.update_testcase_log_url(data_payload)
        else:
            # Using Nosetests
            try:
                # Finally close the browser
                self.driver.quit()
            except AttributeError:
                pass
            except Exception:
                pass
            self.driver = None
