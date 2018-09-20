"""
The BaseCase class is the main gateway for using The SeleniumBase Framework.
It inherits Python's unittest.TestCase class, and runs with Pytest or Nose.
All tests using BaseCase automatically launch WebDriver browsers for tests.

Usage:

    from seleniumbase import BaseCase
    class MyTestClass(BaseCase):
        def test_anything(self):
            # Write your code here. Example:
            self.open("https://github.com/")
            self.update_text("input.header-search-input", "SeleniumBase\n")
            self.click('a[href="/seleniumbase/SeleniumBase"]')
            self.assert_element("div.repository-content")
            ....

SeleniumBase methods expand and improve on existing WebDriver commands.
Improvements include making WebDriver more robust, reliable, and flexible.
Page elements are given enough time to load before WebDriver acts on them.
Code becomes greatly simplified and easier to maintain.
"""

import getpass
import logging
import math
import os
import pytest
import re
import requests
import sys
import time
import traceback
import unittest
import uuid
from bs4 import BeautifulSoup
from seleniumbase.common import decorators
from seleniumbase.config import settings
from seleniumbase.core.application_manager import ApplicationManager
from seleniumbase.core.testcase_manager import ExecutionQueryPayload
from seleniumbase.core.testcase_manager import TestcaseDataPayload
from seleniumbase.core.testcase_manager import TestcaseManager
from seleniumbase.core import download_helper
from seleniumbase.core import log_helper
from seleniumbase.core import style_sheet
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import page_actions
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import xpath_to_css
from selenium.common.exceptions import (StaleElementReferenceException,
                                        MoveTargetOutOfBoundsException,
                                        WebDriverException)
from selenium.common import exceptions as selenium_exceptions
try:
    # Selenium 3 (ElementNotInteractableException does not exist in selenium 2)
    ENI_Exception = selenium_exceptions.ElementNotInteractableException
except Exception:
    # Selenium 2 (Keep compatibility with seleneium 2.53.6 if still being used)
    ENI_Exception = selenium_exceptions.ElementNotSelectableException
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
        self.driver = None
        self.environment = None
        self.env = None  # Add a shortened version of self.environment
        self.__last_url_of_delayed_assert = "data:,"
        self.__last_page_load_url = "data:,"
        self.__page_check_count = 0
        self.__page_check_failures = []
        # Requires self._* instead of self.__* for external class use
        self._html_report_extra = []  # (Used by pytest_plugin.py)
        self._default_driver = None
        self._drivers_list = []
        self._tour_steps = {}

    def open(self, url):
        self.__last_page_load_url = None
        self.driver.get(url)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def open_url(self, url):
        """ In case people are mixing up self.open() with open(),
            use this alternative. """
        self.open(url)

    def click(self, selector, by=By.CSS_SELECTOR,
              timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self.__scroll_to_element(element)
        pre_action_url = self.driver.current_url
        try:
            if self.browser == 'ie' and by == By.LINK_TEXT:
                # An issue with clicking Link Text on IE means using jquery
                self.__jquery_click(selector, by=by)
            else:
                # Normal click
                element.click()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout=timeout)
            element.click()
        except (WebDriverException, MoveTargetOutOfBoundsException):
            self.wait_for_ready_state_complete()
            try:
                self.__js_click(selector, by=by)
            except Exception:
                try:
                    self.__jquery_click(selector, by=by)
                except Exception:
                    # One more attempt to click on the element
                    element = page_actions.wait_for_element_visible(
                        self.driver, selector, by, timeout=timeout)
                    element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)

    def double_click(self, selector, by=By.CSS_SELECTOR,
                     timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self.__scroll_to_element(element)
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
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)

    def click_chain(self, selectors_list, by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT, spacing=0):
        """ This method clicks on a list of elements in succession.
            'spacing' is the amount of time to wait between clicks. (sec) """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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

    def get_link_attribute(self, link_text, attribute, hard_fail=True):
        """ Finds a link by link text and then returns the attribute's value.
            If the link text or attribute cannot be found, an exception will
            get raised if hard_fail is True (otherwise None is returned). """
        self.wait_for_ready_state_complete()
        source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        html_links = soup.find_all('a')
        for html_link in html_links:
            if html_link.text.strip() == link_text.strip():
                if html_link.has_attr(attribute):
                    attribute_value = html_link.get(attribute)
                    return attribute_value
                if hard_fail:
                    raise Exception(
                        'Unable to find attribute {%s} from link text {%s}!'
                        % (attribute, link_text))
                else:
                    return None
        if hard_fail:
            raise Exception("Link text {%s} was not found!" % link_text)
        else:
            return None

    def wait_for_link_text_present(self, link_text,
                                   timeout=settings.SMALL_TIMEOUT):
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 5)):
            try:
                if not self.is_link_text_present(link_text):
                    raise Exception(
                        "Link text {%s} was not found!" % link_text)
                return
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.2)
        raise Exception(
            "Link text {%s} was not present after %s seconds!" % (
                link_text, timeout))

    def click_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ This method clicks link text on a page """
        # If using phantomjs, might need to extract and open the link directly
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if self.browser == 'phantomjs':
            if self.is_link_text_visible(link_text):
                element = self.wait_for_link_text_visible(link_text)
                element.click()
                return
            self.open(self.__get_href_from_link_text(link_text))
            return
        if not self.is_link_text_present(link_text):
            self.wait_for_link_text_present(link_text)
        pre_action_url = self.get_current_url()
        try:
            element = self.wait_for_link_text_visible(
                link_text, timeout=0.2)
            self.__demo_mode_highlight_if_active(link_text, by=By.LINK_TEXT)
            try:
                element.click()
            except (StaleElementReferenceException, ENI_Exception):
                self.wait_for_ready_state_complete()
                time.sleep(0.05)
                element = self.wait_for_link_text_visible(
                    link_text, timeout=timeout)
                element.click()
        except Exception:
            found_css = False
            text_id = self.get_link_attribute(link_text, "id", False)
            if text_id:
                link_css = '[id="%s"]' % link_text
                found_css = True

            if not found_css:
                href = self.__get_href_from_link_text(link_text, False)
                if href:
                    if href.startswith('/') or page_utils.is_valid_url(href):
                        link_css = '[href="%s"]' % href
                        found_css = True

            if not found_css:
                ngclick = self.get_link_attribute(link_text, "ng-click", False)
                if ngclick:
                    link_css = '[ng-click="%s"]' % ngclick
                    found_css = True

            if not found_css:
                onclick = self.get_link_attribute(link_text, "onclick", False)
                if onclick:
                    link_css = '[onclick="%s"]' % onclick
                    found_css = True

            success = False
            if found_css:
                if self.is_element_visible(link_css):
                    self.click(link_css)
                    success = True
                else:
                    # The link text might be hidden under a dropdown menu
                    success = self.__click_dropdown_link_text(
                        link_text, link_css)

            if not success:
                element = self.wait_for_link_text_visible(
                    link_text, timeout=settings.MINI_TIMEOUT)
                element.click()

        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)

    def click_link(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ Same as self.click_link_text() """
        self.click_link_text(link_text, timeout=timeout)

    def click_partial_link_text(self, partial_link_text,
                                timeout=settings.SMALL_TIMEOUT):
        """ This method clicks the partial link text on a page. """
        # If using phantomjs, might need to extract and open the link directly
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
                        '{%s}' % partial_link_text)
            raise Exception(
                "Partial link text {%s} was not found!" % partial_link_text)
        # Not using phantomjs
        element = self.wait_for_partial_link_text(
            partial_link_text, timeout=timeout)
        self.__demo_mode_highlight_if_active(
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
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)

    def get_text(self, selector, by=By.CSS_SELECTOR,
                 timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
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
            raise Exception("Element {%s} has no attribute {%s}!" % (
                selector, attribute))

    def refresh_page(self):
        self.__last_page_load_url = None
        self.driver.refresh()
        self.wait_for_ready_state_complete()

    def refresh(self):
        """ The shorter version of self.refresh_page() """
        self.refresh_page()

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
        self.__last_page_load_url = None
        self.driver.back()
        self.wait_for_ready_state_complete()

    def go_forward(self):
        self.__last_page_load_url = None
        self.driver.forward()
        self.wait_for_ready_state_complete()

    def get_image_url(self, selector, by=By.CSS_SELECTOR,
                      timeout=settings.SMALL_TIMEOUT):
        """ Extracts the URL from an image element on the page. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.get_attribute(selector,
                                  attribute='src', by=by, timeout=timeout)

    def add_text(self, selector, new_value, by=By.CSS_SELECTOR,
                 timeout=settings.LARGE_TIMEOUT):
        """ The more-reliable version of driver.send_keys()
            Similar to update_text(), but won't clear the text field first. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self.__scroll_to_element(element)
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
        except Exception:
            exc_message = self.__get_improved_exception_message()
            raise Exception(exc_message)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)

    def send_keys(self, selector, new_value, by=By.CSS_SELECTOR,
                  timeout=settings.LARGE_TIMEOUT):
        """ Same as add_text() -> more reliable, but less name confusion. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
            retry - if True, use JS if the selenium text update fails
        """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode:
            self.__scroll_to_element(element)
        try:
            element.clear()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            element.clear()
        except Exception:
            pass  # Clearing the text field first isn't critical
        self.__demo_mode_pause_if_active(tiny=True)
        pre_action_url = self.driver.current_url
        try:
            if not new_value.endswith('\n'):
                element.send_keys(new_value)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
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
        except Exception:
            exc_message = self.__get_improved_exception_message()
            raise Exception(exc_message)
        if (retry and element.get_attribute('value') != new_value and (
                not new_value.endswith('\n'))):
            logging.debug('update_text() is falling back to JavaScript!')
            self.set_value(selector, new_value, by=by)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)

    def update_text(self, selector, new_value, by=By.CSS_SELECTOR,
                    timeout=settings.LARGE_TIMEOUT, retry=False):
        """ The shorter version of update_text_value(), which
            clears existing text and adds new text into the text field.
            We want to keep the old version for backward compatibility. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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

    def is_element_in_an_iframe(self, selector, by=By.CSS_SELECTOR):
        """ Returns True if the selector's element is located in an iframe.
            Otherwise returns False. """
        selector, by = self.__recalculate_selector(selector, by)
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

    def switch_to_frame_of_element(self, selector, by=By.CSS_SELECTOR):
        """ Set driver control to the iframe of the element (assuming the
            element is in a single-nested iframe) and returns the iframe name.
            If element is not in an iframe, returns None, and nothing happens.
            May not work if multiple iframes are nested within each other. """
        selector, by = self.__recalculate_selector(selector, by)
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
            timeout = self.__get_new_timeout(timeout)
        self.driver.set_script_timeout(timeout)
        return self.driver.execute_async_script(script)

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)
        self.__demo_mode_pause_if_active()

    def maximize_window(self):
        self.driver.maximize_window()
        self.__demo_mode_pause_if_active()

    def add_css_link(self, css_link):
        script_to_add_css = (
            """function injectCSS() {
                  var head = document.getElementsByTagName("head")[0];
                  var link = document.createElement("link");
                  link.rel = "stylesheet";
                  link.type = "text/css";
                  link.href = "%s";
                  link.crossorigin = "anonymous";
                  head.appendChild(link);
               }
               injectCSS();""")
        self.execute_script(script_to_add_css % css_link)

    def add_js_link(self, js_link):
        script_to_add_js = (
            """function injectJS() {
                  var head = document.getElementsByTagName("head")[0];
                  var script = document.createElement("script");
                  script.src = "%s";
                  script.defer;
                  script.crossorigin = "anonymous";
                  script.onload = function() { null };
                  head.appendChild(script);
               }
               injectJS();""")
        self.execute_script(script_to_add_js % js_link)

    def add_css_style(self, css_style):
        add_css_style_script = (
            '''var h = document.getElementsByTagName('head').item(0);'''
            '''var s = document.createElement("style");'''
            '''s.type = "text/css";'''
            '''s.appendChild(document.createTextNode("%s"));'''
            '''h.appendChild(s);''')
        css_style = re.escape(css_style)
        css_style = self.__escape_quotes_if_needed(css_style)
        self.execute_script(add_css_style_script % css_style)

    def add_js_code_from_link(self, js_link):
        if js_link.startswith("//"):
            js_link = "http:" + js_link
        js_code = requests.get(js_link).text
        add_js_code_script = (
            '''var h = document.getElementsByTagName('head').item(0);'''
            '''var s = document.createElement("script");'''
            '''s.type = "text/javascript";'''
            '''s.onload = function() { null };'''
            '''s.appendChild(document.createTextNode("%s"));'''
            '''h.appendChild(s);''')
        js_code = re.escape(js_code)
        js_code = self.__escape_quotes_if_needed(js_code)
        self.execute_script(add_js_code_script % js_code)

    def add_meta_tag(self, http_equiv=None, content=None):
        if http_equiv is None:
            http_equiv = "Content-Security-Policy"
        if content is None:
            content = ("default-src *; style-src 'self' 'unsafe-inline'; "
                       "script-src: 'self' 'unsafe-inline' 'unsafe-eval'")
        script_to_add_meta = (
            """function injectMeta() {
               var meta = document.createElement('meta');
               meta.httpEquiv = "%s";
               meta.content = "%s";
               document.getElementsByTagName('head')[0].appendChild(meta);
            }
            injectMeta();""" % (http_equiv, content))
        self.execute_script(script_to_add_meta)

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
        jquery_js = constants.JQuery.MIN_JS
        self.add_js_link(jquery_js)
        for x in range(int(settings.MINI_TIMEOUT * 10.0)):
            # jQuery needs a small amount of time to activate.
            try:
                self.execute_script("jQuery('html')")
                return
            except Exception:
                time.sleep(0.1)
        # Since jQuery still isn't activating, give up and raise an exception
        raise Exception(
            '''Unable to load jQuery on "%s" due to a possible violation '''
            '''of the website's Content Security Policy '''
            '''directive. ''' % self.driver.current_url)

    def __are_quotes_escaped(self, string):
        return page_utils.are_quotes_escaped(string)

    def __escape_quotes_if_needed(self, string):
        return page_utils.escape_quotes_if_needed(string)

    def __activate_bootstrap(self):
        """ Allows you to use Bootstrap Tours with SeleniumBase
            http://bootstraptour.com/
        """
        bootstrap_tour_css = constants.BootstrapTour.MIN_CSS
        bootstrap_tour_js = constants.BootstrapTour.MIN_JS

        verify_script = ("""// Instance the tour
                         var tour2 = new Tour({
                         });""")

        for x in range(4):
            self.activate_jquery()
            self.add_css_link(bootstrap_tour_css)
            self.add_js_link(bootstrap_tour_js)
            time.sleep(0.1)

            for x in range(int(settings.MINI_TIMEOUT * 2.0)):
                # Bootstrap needs a small amount of time to load & activate.
                try:
                    self.execute_script(verify_script)
                    time.sleep(0.05)
                    return
                except Exception:
                    time.sleep(0.15)

        raise Exception(
            '''Unable to load jQuery on "%s" due to a possible violation '''
            '''of the website's Content Security Policy '''
            '''directive. ''' % self.driver.current_url)

    def __is_bootstrap_activated(self):
        verify_script = ("""// Instance the tour
                         var tour2 = new Tour({
                         });""")
        try:
            self.execute_script(verify_script)
            return True
        except Exception:
            return False

    def __activate_shepherd(self):
        """ Allows you to use Shepherd Tours with SeleniumBase
            http://github.hubspot.com/shepherd/docs/welcome/
        """
        shepherd_js = constants.Shepherd.MIN_JS
        sh_theme_arrows_css = constants.Shepherd.THEME_ARROWS_CSS
        sh_theme_arrows_fix_css = constants.Shepherd.THEME_ARR_FIX_CSS
        sh_theme_default_css = constants.Shepherd.THEME_DEFAULT_CSS
        sh_theme_dark_css = constants.Shepherd.THEME_DARK_CSS
        sh_theme_sq_css = constants.Shepherd.THEME_SQ_CSS
        sh_theme_sq_dark_css = constants.Shepherd.THEME_SQ_DK_CSS
        tether_js = constants.Tether.MIN_JS
        underscore_js = constants.Underscore.MIN_JS
        backbone_js = constants.Backbone.MIN_JS
        spinner_css = constants.Messenger.SPINNER_CSS

        sh_style = style_sheet.sh_style_test
        backdrop_style = style_sheet.sh_backdrop_style

        self.__activate_bootstrap()
        self.wait_for_ready_state_complete()
        self.add_css_style(backdrop_style)
        self.wait_for_ready_state_complete()
        for x in range(4):
            # self.activate_jquery()  # Included with __activate_bootstrap()
            self.add_css_link(spinner_css)
            self.add_css_link(sh_theme_arrows_css)
            self.add_css_link(sh_theme_arrows_fix_css)
            self.add_css_link(sh_theme_default_css)
            self.add_css_link(sh_theme_dark_css)
            self.add_css_link(sh_theme_sq_css)
            self.add_css_link(sh_theme_sq_dark_css)
            self.add_js_link(tether_js)
            self.add_js_link(underscore_js)
            self.add_js_link(backbone_js)
            self.add_js_link(shepherd_js)
            time.sleep(0.1)

            for x in range(int(settings.MINI_TIMEOUT * 2.0)):
                # Shepherd needs a small amount of time to load & activate.
                try:
                    self.execute_script(sh_style)  # Verify Shepherd has loaded
                    self.wait_for_ready_state_complete()
                    self.execute_script(sh_style)  # Need it twice for ordering
                    self.wait_for_ready_state_complete()
                    time.sleep(0.05)
                    return
                except Exception:
                    time.sleep(0.15)

        raise Exception(
            '''Unable to load jQuery on "%s" due to a possible violation '''
            '''of the website's Content Security Policy '''
            '''directive. ''' % self.driver.current_url)

    def __is_shepherd_activated(self):
        sh_style = style_sheet.sh_style_test
        try:
            self.execute_script(sh_style)  # Verify Shepherd has loaded
            return True
        except Exception:
            return False

    def create_tour(self, name=None, theme=None):
        """ Creates a tour for a website.
            @Params
            name - If creating multiple tours, use this to select the
                   tour you wish to add steps to.
            theme - Sets the default theme for the tour.
                    Choose from "light"/"arrows", "dark", "default", "square",
                    and "square-dark". ("arrows" is used if None is selected.)
        """
        if not name:
            name = "default"

        shepherd_theme = "shepherd-theme-arrows"
        if theme:
            if theme.lower() == "bootstrap":
                self.create_bootstrap_tour(name)
                return
            elif theme == "default":
                shepherd_theme = "shepherd-theme-default"
            elif theme == "dark":
                shepherd_theme = "shepherd-theme-dark"
            elif theme == "light":
                shepherd_theme = "shepherd-theme-arrows"
            elif theme == "arrows":
                shepherd_theme = "shepherd-theme-arrows"
            elif theme == "square":
                shepherd_theme = "shepherd-theme-square"
            elif theme == "square-dark":
                shepherd_theme = "shepherd-theme-square-dark"

        new_tour = ("""
                    // Shepherd Tour
                    let tour = new Shepherd.Tour({
                        defaults: {
                            classes: '%s',
                            scrollTo: true
                        }
                    });
                    """ % shepherd_theme)

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_bootstrap_tour(self, name=None):
        """ Creates a Bootstrap tour for a website.
            @Params
            name - If creating multiple tours, use this to select the
                   tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = ("""
                    // Bootstrap Tour
                    var tour = new Tour({
                    steps: [
                    """)

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def add_tour_step(self, message, selector=None, name=None,
                      title=None, theme=None, alignment=None, duration=None):
        """ Allows the user to add tour steps for a website.
            @Params
            message - The message to display.
            selector - The CSS Selector of the Element to attach to.
            name - If creating multiple tours, use this to select the
                   tour you wish to add steps to.
            title - Additional header text that appears above the message.
            theme - (NON-Bootstrap Tours ONLY) The styling of the tour step.
                    Choose from "light"/"arrows", "dark", "default", "square",
                    and "square-dark". ("arrows" is used if None is selected.)
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("top" is the default alignment).
            duration - (Bootstrap Tours ONLY) The amount of time, in seconds,
                       before automatically advancing to the next tour step.
        """
        if not selector:
            selector = "html"
        selector = re.escape(selector)
        selector = self.__escape_quotes_if_needed(selector)

        if not name:
            name = "default"
        if name not in self._tour_steps:
            # By default, will create a Bootstrap tour if no tours exist
            self.create_tour(name=name, theme="bootstrap")

        if not title:
            title = ""
        title = re.escape(title)
        title = self.__escape_quotes_if_needed(title)

        if message:
            message = re.escape(message)
            message = self.__escape_quotes_if_needed(message)
        else:
            message = ""

        if not alignment or (
                alignment not in ["top", "bottom", "left", "right"]):
            alignment = "top"

        if "Bootstrap" in self._tour_steps[name][0]:
            self.__add_bootstrap_tour_step(
                message, selector=selector, name=name, title=title,
                alignment=alignment, duration=duration)
        else:
            self.__add_shepherd_tour_step(
                message, selector=selector, name=name, title=title,
                theme=theme, alignment=alignment)

    def __add_shepherd_tour_step(self, message, selector=None, name=None,
                                 title=None, theme=None, alignment=None):
        """ Allows the user to add tour steps for a website.
            @Params
            message - The message to display.
            selector - The CSS Selector of the Element to attach to.
            name - If creating multiple tours, use this to select the
                   tour you wish to add steps to.
            title - Additional header text that appears above the message.
            theme - (NON-Bootstrap Tours ONLY) The styling of the tour step.
                    Choose from "light"/"arrows", "dark", "default", "square",
                    and "square-dark". ("arrows" is used if None is selected.)
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("top" is the default alignment).
        """
        if theme == "default":
            shepherd_theme = "shepherd-theme-default"
        elif theme == "dark":
            shepherd_theme = "shepherd-theme-dark"
        elif theme == "light":
            shepherd_theme = "shepherd-theme-arrows"
        elif theme == "arrows":
            shepherd_theme = "shepherd-theme-arrows"
        elif theme == "square":
            shepherd_theme = "shepherd-theme-square"
        elif theme == "square-dark":
            shepherd_theme = "shepherd-theme-square-dark"
        else:
            shepherd_base_theme = re.search(
                r"[\S\s]+classes: '([\S\s]+)',[\S\s]+",
                self._tour_steps[name][0]).group(1)
            shepherd_theme = shepherd_base_theme

        shepherd_classes = shepherd_theme
        if selector == "html":
            shepherd_classes += " shepherd-orphan"
        step = ("""
                tour.addStep('%s', {
                    title: '%s',
                    classes: '%s',
                    text: '%s',
                    attachTo: {element: '%s', on: '%s'},
                    advanceOn: '.docs-link click'
                });""" % (
                name, title, shepherd_classes, message, selector, alignment))

        self._tour_steps[name].append(step)

    def __add_bootstrap_tour_step(self, message, selector=None, name=None,
                                  title=None, alignment=None, duration=None):
        """ Allows the user to add tour steps for a website.
            @Params
            message - The message to display.
            selector - The CSS Selector of the Element to attach to.
            name - If creating multiple tours, use this to select the
                   tour you wish to add steps to.
            title - Additional header text that appears above the message.
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("top" is the default alignment).
            duration - (Bootstrap Tours ONLY) The amount of time, in seconds,
                       before automatically advancing to the next tour step.
        """
        if selector != "html":
            element_row = "element: '%s'," % selector
        else:
            element_row = ""
        if not duration:
            duration = "0"
        else:
            duration = str(float(duration) * 1000.0)

        step = ("""{
                %s
                title: '%s',
                content: '%s',
                orphan: true,
                placement: 'auto %s',
                smartPlacement: true,
                duration: %s,
                },""" % (element_row, title, message, alignment, duration))

        self._tour_steps[name].append(step)

    def play_tour(self, name=None, interval=0):
        """ Plays a tour on the current website.
            @Params
            name - If creating multiple tours, use this to select the
                   tour you wish to play.
            interval - The delay time between autoplaying tour steps.
                       If set to 0 (default), the tour is fully manual control.
        """
        if self.headless:
            return  # Tours should not run in headless mode.

        if not name:
            name = "default"
        if name not in self._tour_steps:
            raise Exception("Tour {%s} does not exist!" % name)

        if "Bootstrap" in self._tour_steps[name][0]:
            self.__play_bootstrap_tour(name=name, interval=interval)
        else:
            self.__play_shepherd_tour(name=name, interval=interval)

    def __play_shepherd_tour(self, name=None, interval=0):
        """ Plays a tour on the current website.
            @Params
            name - If creating multiple tours, use this to select the
                   tour you wish to play.
            interval - The delay time between autoplaying tour steps.
                       If set to 0 (default), the tour is fully manual control.
        """
        instructions = ""
        for tour_step in self._tour_steps[name]:
            instructions += tour_step
        instructions += "tour.start();"

        autoplay = False
        if interval and interval > 0:
            autoplay = True
            interval = float(interval)
            if interval < 0.5:
                interval = 0.5

        if not self.__is_shepherd_activated():
            self.__activate_shepherd()

        if len(self._tour_steps[name]) > 1:
            try:
                selector = re.search(
                    r"[\S\s]+{element: '([\S\s]+)', on: [\S\s]+",
                    self._tour_steps[name][1]).group(1)
                selector = selector.replace('\\', '')
                self.wait_for_element_present(
                    selector, timeout=(settings.SMALL_TIMEOUT))
            except Exception:
                self.__post_messenger_error_message(
                    "Tour Error: {'%s'} was not found!"
                    "" % selector,
                    duration=settings.SMALL_TIMEOUT)
                raise Exception(
                    "Tour Error: {'%s'} was not found! "
                    "Exiting due to failure on first tour step!"
                    "" % selector)

        self.execute_script(instructions)
        tour_on = True
        if autoplay:
            start_ms = time.time() * 1000.0
            stop_ms = start_ms + (interval * 1000.0)
            latest_element = None
            latest_text = None
        while tour_on:
            try:
                time.sleep(0.01)
                result = self.execute_script(
                    "return Shepherd.activeTour.currentStep.isOpen()")
            except Exception:
                tour_on = False
                result = None
            if result:
                tour_on = True
                if autoplay:
                    try:
                        element = self.execute_script(
                            "Shepherd.activeTour.currentStep"
                            ".options.attachTo.element")
                        shep_text = self.execute_script(
                            "Shepherd.activeTour.currentStep.options.text")
                    except Exception:
                        continue
                    now_ms = time.time() * 1000.0
                    if now_ms >= stop_ms:
                        if ((element == latest_element) and
                                (shep_text == latest_text)):
                            self.execute_script("Shepherd.activeTour.next()")
                            try:
                                latest_element = self.execute_script(
                                    "Shepherd.activeTour.currentStep"
                                    ".options.attachTo.element")
                                latest_text = self.execute_script(
                                    "Shepherd.activeTour.currentStep"
                                    ".options.text")
                                start_ms = time.time() * 1000.0
                                stop_ms = start_ms + (interval * 1000.0)
                            except Exception:
                                pass
                            continue

            else:
                try:
                    time.sleep(0.01)
                    selector = self.execute_script(
                        "return Shepherd.activeTour"
                        ".currentStep.options.attachTo.element")
                    try:
                        self.__wait_for_css_query_selector(
                            selector, timeout=(settings.MINI_TIMEOUT))
                    except Exception:
                        self.remove_elements("div.shepherd-content")
                        self.__post_messenger_error_message(
                            "Tour Error: {'%s'} was not found!"
                            "" % selector,
                            duration=settings.SMALL_TIMEOUT)
                        time.sleep(0.1)
                    self.execute_script("Shepherd.activeTour.next()")
                    if autoplay:
                        start_ms = time.time() * 1000.0
                        stop_ms = start_ms + (interval * 1000.0)
                    tour_on = True
                except Exception:
                    tour_on = False
                    time.sleep(0.1)

    def __play_bootstrap_tour(self, name=None, interval=0):
        """ Plays a tour on the current website.
            @Params
            name - If creating multiple tours, use this to select the
                   tour you wish to play.
            interval - The delay time between autoplaying tour steps.
                       If set to 0 (default), the tour is fully manual control.
        """
        instructions = ""
        for tour_step in self._tour_steps[name]:
            instructions += tour_step
        instructions += (
            """]});

            // Initialize the tour
            tour.init();

            // Start the tour
            tour.start();

            $tour = tour;
            $tour.restart();""")

        if interval and interval > 0:
            if interval < 1:
                interval = 1
            interval = str(float(interval) * 1000.0)
            instructions = instructions.replace(
                'duration: 0,', 'duration: %s,' % interval)

        if not self.__is_bootstrap_activated():
            self.__activate_bootstrap()

        if len(self._tour_steps[name]) > 1:
            try:
                if "element: " in self._tour_steps[name][1]:
                    selector = re.search(
                        r"[\S\s]+element: '([\S\s]+)',[\S\s]+title: '",
                        self._tour_steps[name][1]).group(1)
                    selector = selector.replace('\\', '')
                    self.wait_for_element_present(
                        selector, timeout=(settings.SMALL_TIMEOUT))
                else:
                    selector = "html"
            except Exception:
                self.__post_messenger_error_message(
                    "Tour Error: {'%s'} was not found!"
                    "" % selector,
                    duration=settings.SMALL_TIMEOUT)
                raise Exception(
                    "Tour Error: {'%s'} was not found! "
                    "Exiting due to failure on first tour step!"
                    "" % selector)

        self.execute_script(instructions)
        tour_on = True
        while tour_on:
            try:
                time.sleep(0.01)
                result = self.execute_script(
                    "return $tour.ended()")
            except Exception:
                tour_on = False
                result = None
            if result is False:
                tour_on = True
            else:
                try:
                    time.sleep(0.01)
                    result = self.execute_script(
                        "return $tour.ended()")
                    if result is False:
                        time.sleep(0.1)
                        continue
                    else:
                        return
                except Exception:
                    tour_on = False
                    time.sleep(0.1)

    def __wait_for_css_query_selector(
            self, selector, timeout=settings.SMALL_TIMEOUT):
        element = None
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 10)):
            try:
                selector = re.escape(selector)
                selector = self.__escape_quotes_if_needed(selector)
                element = self.execute_script(
                    """return document.querySelector('%s')""" % selector)
                if element:
                    return element
            except Exception:
                element = None
            if not element:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)

        raise Exception(
            "Element {%s} was not present after %s seconds!" % (
                selector, timeout))

    def activate_messenger(self):
        jquery_js = constants.JQuery.MIN_JS
        messenger_css = constants.Messenger.MIN_CSS
        messenger_js = constants.Messenger.MIN_JS
        msgr_theme_flat_js = constants.Messenger.THEME_FLAT_JS
        msgr_theme_future_js = constants.Messenger.THEME_FUTURE_JS
        msgr_theme_flat_css = constants.Messenger.THEME_FLAT_CSS
        msgr_theme_future_css = constants.Messenger.THEME_FUTURE_CSS
        msgr_theme_block_css = constants.Messenger.THEME_BLOCK_CSS
        msgr_theme_air_css = constants.Messenger.THEME_AIR_CSS
        msgr_theme_ice_css = constants.Messenger.THEME_ICE_CSS
        spinner_css = constants.Messenger.SPINNER_CSS
        underscore_js = constants.Underscore.MIN_JS
        backbone_js = constants.Backbone.MIN_JS

        msg_style = ("Messenger.options = {'maxMessages': 8, "
                     "extraClasses: 'messenger-fixed "
                     "messenger-on-bottom messenger-on-right', "
                     "theme: 'future'}")

        self.add_js_link(jquery_js)
        self.add_css_link(messenger_css)
        self.add_css_link(msgr_theme_flat_css)
        self.add_css_link(msgr_theme_future_css)
        self.add_css_link(msgr_theme_block_css)
        self.add_css_link(msgr_theme_air_css)
        self.add_css_link(msgr_theme_ice_css)
        self.add_js_link(underscore_js)
        self.add_js_link(backbone_js)
        self.add_css_link(spinner_css)
        self.add_js_link(messenger_js)
        self.add_js_link(msgr_theme_flat_js)
        self.add_js_link(msgr_theme_future_js)

        for x in range(int(settings.MINI_TIMEOUT * 10.0)):
            # Messenger needs a small amount of time to load & activate.
            try:
                self.execute_script(msg_style)
                self.wait_for_ready_state_complete()
                return
            except Exception:
                time.sleep(0.1)

    def set_messenger_theme(self, theme="default", location="default",
                            max_messages="default"):
        if theme == "default":
            theme = "future"
        if location == "default":
            location = "bottom_right"
        if max_messages == "default":
            max_messages = "8"

        valid_themes = ['flat', 'future', 'block', 'air', 'ice']
        if theme not in valid_themes:
            raise Exception("Theme: %s is not in %s!" % (theme, valid_themes))
        valid_locations = (['top_left', 'top_center', 'top_right'
                            'bottom_left', 'bottom_center', 'bottom_right'])
        if location not in valid_locations:
            raise Exception(
                "Location: %s is not in %s!" % (location, valid_locations))

        if location == 'top_left':
            messenger_location = "messenger-on-top messenger-on-left"
        elif location == 'top_center':
            messenger_location = "messenger-on-top"
        elif location == 'top_right':
            messenger_location = "messenger-on-top messenger-on-right"
        elif location == 'bottom_left':
            messenger_location = "messenger-on-bottom messenger-on-left"
        elif location == 'bottom_center':
            messenger_location = "messenger-on-bottom"
        elif location == 'bottom_right':
            messenger_location = "messenger-on-bottom messenger-on-right"

        msg_style = ("Messenger.options = {'maxMessages': %s, "
                     "extraClasses: 'messenger-fixed %s', theme: '%s'}"
                     % (max_messages, messenger_location, theme))
        try:
            self.execute_script(msg_style)
        except Exception:
            self.activate_messenger()
            self.execute_script(msg_style)
        time.sleep(0.1)

    def post_message(self, message, style="info", duration=None):
        """ Post a message on the screen with Messenger.
            Arguments:
                message: The message to display.
                style: "info", "success", or "error".
                duration: The time until the message vanishes.

            You can also post messages by using =>
                self.execute_script('Messenger().post("My Message")')
             """
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        message = re.escape(message)
        message = self.__escape_quotes_if_needed(message)
        messenger_script = ('''Messenger().post({message: "%s", type: "%s", '''
                            '''hideAfter: %s, hideOnNavigate: true});'''
                            % (message, style, duration))
        try:
            self.execute_script(messenger_script)
        except Exception:
            self.activate_messenger()
            self.set_messenger_theme()
            try:
                self.execute_script(messenger_script)
            except Exception:
                time.sleep(0.2)
                self.activate_messenger()
                time.sleep(0.2)
                self.set_messenger_theme()
                time.sleep(0.5)
                self.execute_script(messenger_script)

    def get_property_value(self, selector, property, by=By.CSS_SELECTOR,
                           timeout=settings.SMALL_TIMEOUT):
        """ Returns the property value of a page element's computed style.
            Example:
                opacity = self.get_property_value("html body a", "opacity")
                self.assertTrue(float(opacity) > 0, "Element not visible!") """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        self.wait_for_ready_state_complete()
        page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't run action if can't convert to CSS_Selector for JavaScript
            raise Exception(
                "Exception: Could not convert {%s}(by=%s) to CSS_SELECTOR!" % (
                    selector, by))
        selector = re.escape(selector)
        selector = self.__escape_quotes_if_needed(selector)
        script = ("""var $elm = document.querySelector('%s');
                  $val = window.getComputedStyle($elm).getPropertyValue('%s');
                  return $val;"""
                  % (selector, property))
        value = self.execute_script(script)
        if value is not None:
            return value
        else:
            return ""  # Return an empty string if the property doesn't exist

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
            # Don't run action if can't convert to CSS_Selector for JavaScript
            return
        selector = re.escape(selector)
        selector = self.__escape_quotes_if_needed(selector)
        script = ("""document.querySelector('%s').style.zIndex = '9999';"""
                  % selector)
        self.execute_script(script)

    def highlight_click(self, selector, by=By.CSS_SELECTOR,
                        loops=3, scroll=True):
        if not self.demo_mode:
            self.highlight(selector, by=by, loops=loops, scroll=scroll)
        self.click(selector, by=by)

    def highlight_update_text(self, selector, new_value, by=By.CSS_SELECTOR,
                              loops=3, scroll=True):
        if not self.demo_mode:
            self.highlight(selector, by=by, loops=loops, scroll=scroll)
        self.update_text(selector, new_value, by=by)

    def highlight(self, selector, by=By.CSS_SELECTOR,
                  loops=settings.HIGHLIGHTS, scroll=True):
        """ This method uses fancy JavaScript to highlight an element.
            Used during demo_mode.
            @Params
            selector - the selector of the element to find
            by - the type of selector to search by (Default: CSS)
            loops - # of times to repeat the highlight animation
                    (Default: 4. Each loop lasts for about 0.18s)
            scroll - the option to scroll to the element first (Default: True)
        """
        selector, by = self.__recalculate_selector(selector, by)
        element = self.find_element(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if scroll:
            self.__slow_scroll_to_element(element)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't highlight if can't convert to CSS_SELECTOR
            return

        if self.highlights:
            loops = self.highlights
        if self.browser == 'ie':
            loops = 1  # Override previous setting because IE is slow
        loops = int(loops)

        o_bs = ''  # original_box_shadow
        style = element.get_attribute('style')
        if style:
            if 'box-shadow: ' in style:
                box_start = style.find('box-shadow: ')
                box_end = style.find(';', box_start) + 1
                original_box_shadow = style[box_start:box_end]
                o_bs = original_box_shadow

        if ":contains" not in selector and ":first" not in selector:
            selector = re.escape(selector)
            selector = self.__escape_quotes_if_needed(selector)
            self.__highlight_with_js(selector, loops, o_bs)
        else:
            selector = self.__make_css_match_first_element_only(selector)
            selector = re.escape(selector)
            selector = self.__escape_quotes_if_needed(selector)
            try:
                self.__highlight_with_jquery(selector, loops, o_bs)
            except Exception:
                pass  # JQuery probably couldn't load. Skip highlighting.
        time.sleep(0.065)

    def __highlight_with_js(self, selector, loops, o_bs):
        script = ("""document.querySelector('%s').style =
                  'box-shadow: 0px 0px 6px 6px rgba(128, 128, 128, 0.5)';"""
                  % selector)
        self.execute_script(script)

        for n in range(loops):
            script = ("""document.querySelector('%s').style =
                      'box-shadow: 0px 0px 6px 6px rgba(255, 0, 0, 1)';"""
                      % selector)
            self.execute_script(script)
            time.sleep(0.0181)
            script = ("""document.querySelector('%s').style =
                      'box-shadow: 0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
                      % selector)
            self.execute_script(script)
            time.sleep(0.0181)
            script = ("""document.querySelector('%s').style =
                      'box-shadow: 0px 0px 6px 6px rgba(0, 0, 255, 1)';"""
                      % selector)
            self.execute_script(script)
            time.sleep(0.0181)
            script = ("""document.querySelector('%s').style =
                      'box-shadow: 0px 0px 6px 6px rgba(0, 255, 0, 1)';"""
                      % selector)
            self.execute_script(script)
            time.sleep(0.0181)
            script = ("""document.querySelector('%s').style =
                      'box-shadow: 0px 0px 6px 6px rgba(128, 128, 0, 1)';"""
                      % selector)
            self.execute_script(script)
            time.sleep(0.0181)
            script = ("""document.querySelector('%s').style =
                      'box-shadow: 0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
                      % selector)
            self.execute_script(script)
            time.sleep(0.0181)

        script = ("""document.querySelector('%s').style =
                  'box-shadow: %s';"""
                  % (selector, o_bs))
        self.execute_script(script)

    def __highlight_with_jquery(self, selector, loops, o_bs):
        script = """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(128, 128, 128, 0.5)');""" % selector
        self.safe_execute_script(script)

        for n in range(loops):
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(255, 0, 0, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.0181)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(128, 0, 128, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.0181)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(0, 0, 255, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.0181)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(0, 255, 0, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.0181)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(128, 128, 0, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.0181)
            script = """jQuery('%s').css('box-shadow',
                '0px 0px 6px 6px rgba(128, 0, 128, 1)');""" % selector
            self.execute_script(script)
            time.sleep(0.0181)

        script = """jQuery('%s').css('box-shadow', '%s');""" % (selector, o_bs)
        self.execute_script(script)

    def scroll_to(self, selector, by=By.CSS_SELECTOR,
                  timeout=settings.SMALL_TIMEOUT):
        ''' Fast scroll to destination '''
        if self.demo_mode:
            self.slow_scroll_to(selector, by=by, timeout=timeout)
            return
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        try:
            self.__scroll_to_element(element)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            self.__scroll_to_element(element)

    def slow_scroll_to(self, selector, by=By.CSS_SELECTOR,
                       timeout=settings.SMALL_TIMEOUT):
        ''' Slow motion scroll to destination '''
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self.__slow_scroll_to_element(element)

    def scroll_click(self, selector, by=By.CSS_SELECTOR):
        # DEPRECATED - self.click() now scrolls to the element before clicking
        # self.scroll_to(selector, by=by)
        self.click(selector, by=by)

    def click_xpath(self, xpath):
        self.click(xpath, by=By.XPATH)

    def js_click(self, selector, by=By.CSS_SELECTOR):
        """ Clicks an element using pure JS. Does not use jQuery. """
        selector, by = self.__recalculate_selector(selector, by)
        if by == By.LINK_TEXT:
            message = (
                "Pure JavaScript doesn't support clicking by Link Text. "
                "You may want to use self.jquery_click() instead, which "
                "allows this with :contains(), assuming jQuery isn't blocked. "
                "For now, self.js_click() will use a regular WebDriver click.")
            logging.debug(message)
            self.click(selector, by=by)
            return
        element = self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
            if not self.demo_mode:
                self.__scroll_to_element(element)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)
        css_selector = self.__escape_quotes_if_needed(css_selector)
        self.__js_click(selector, by=by)  # The real "magic" happens here
        self.__demo_mode_pause_if_active()

    def jquery_click(self, selector, by=By.CSS_SELECTOR):
        """ Clicks an element using jQuery. Different from using pure JS. """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        click_script = """jQuery('%s')[0].click()""" % selector
        self.safe_execute_script(click_script)
        self.__demo_mode_pause_if_active()

    def hide_element(self, selector, by=By.CSS_SELECTOR):
        """ Hide the first element on the page that matches the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        hide_script = """jQuery('%s').hide()""" % selector
        self.safe_execute_script(hide_script)

    def hide_elements(self, selector, by=By.CSS_SELECTOR):
        """ Hide all elements on the page that match the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        hide_script = """jQuery('%s').hide()""" % selector
        self.safe_execute_script(hide_script)

    def show_element(self, selector, by=By.CSS_SELECTOR):
        """ Show the first element on the page that matches the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        show_script = """jQuery('%s').show(0)""" % selector
        self.safe_execute_script(show_script)

    def show_elements(self, selector, by=By.CSS_SELECTOR):
        """ Show all elements on the page that match the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        show_script = """jQuery('%s').show(0)""" % selector
        self.safe_execute_script(show_script)

    def remove_element(self, selector, by=By.CSS_SELECTOR):
        """ Remove the first element on the page that matches the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        remove_script = """jQuery('%s').remove()""" % selector
        self.safe_execute_script(remove_script)

    def remove_elements(self, selector, by=By.CSS_SELECTOR):
        """ Remove all elements on the page that match the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        remove_script = """jQuery('%s').remove()""" % selector
        self.safe_execute_script(remove_script)

    def ad_block(self):
        from seleniumbase.config import ad_block_list
        for css_selector in ad_block_list.AD_BLOCK_LIST:
            css_selector = re.escape(css_selector)
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = ("""var $elements = document.querySelectorAll('%s');
                      var index = 0, length = $elements.length;
                      for(; index < length; index++){
                      $elements[index].remove();}"""
                      % css_selector)
            try:
                self.execute_script(script)
            except Exception:
                pass  # Don't fail test if ad_blocking fails

    def jq_format(self, code):
        # DEPRECATED - Use re.escape() instead, which does the action you want.
        return page_utils._jq_format(code)

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
            If no destination folder is specified, the default one is used.
            (The default downloads folder = "./downloaded_files") """
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

    def save_data_as(self, data, file_name, destination_folder=None):
        """ Saves the data specified to a file of the name specified.
            If no destination folder is specified, the default one is used.
            (The default downloads folder = "./downloaded_files") """
        if not destination_folder:
            destination_folder = constants.Files.DOWNLOADS_FOLDER
        page_utils._save_data_as(data, destination_folder, file_name)

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
            This method should only be used for jQuery/JavaScript actions.
            Pure JavaScript doesn't support using a:contains("LINK_TEXT"). """
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
                "Exception: Could not convert {%s}(by=%s) to CSS_SELECTOR!" % (
                    selector, by))

    def set_value(self, selector, new_value, by=By.CSS_SELECTOR,
                  timeout=settings.LARGE_TIMEOUT):
        """ This method uses JavaScript to update a text field. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        orginal_selector = selector
        css_selector = self.convert_to_css_selector(selector, by=by)
        self.__demo_mode_highlight_if_active(orginal_selector, by)
        if not self.demo_mode:
            self.scroll_to(orginal_selector, by=by, timeout=timeout)
        value = re.escape(new_value)
        value = self.__escape_quotes_if_needed(value)
        css_selector = re.escape(css_selector)
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = ("""document.querySelector('%s').value='%s';"""
                  % (css_selector, value))
        self.execute_script(script)
        if new_value.endswith('\n'):
            element = self.wait_for_element_present(
                orginal_selector, by=by, timeout=timeout)
            element.send_keys(Keys.RETURN)
            if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def js_update_text(self, selector, new_value, by=By.CSS_SELECTOR,
                       timeout=settings.LARGE_TIMEOUT):
        """ Same as self.set_value() """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.set_value(
            selector, new_value, by=by, timeout=timeout)

    def jquery_update_text_value(self, selector, new_value, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        """ This method uses jQuery to update a text field.
            If the new_value string ends with the newline character,
            WebDriver will finish the call, which simulates pressing
            {Enter/Return} after the text is entered. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        selector = self.__escape_quotes_if_needed(selector)
        new_value = re.escape(new_value)
        new_value = self.__escape_quotes_if_needed(new_value)
        update_text_script = """jQuery('%s').val('%s')""" % (
            selector, new_value)
        self.safe_execute_script(update_text_script)
        if new_value.endswith('\n'):
            element.send_keys('\n')
        self.__demo_mode_pause_if_active()

    def jquery_update_text(self, selector, new_value, by=By.CSS_SELECTOR,
                           timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of self.jquery_update_text_value()
            (The longer version remains for backwards compatibility.) """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.jquery_update_text_value(
            selector, new_value, by=by, timeout=timeout)

    def hover_on_element(self, selector, by=By.CSS_SELECTOR):
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        self.__demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        time.sleep(0.05)  # Settle down from scrolling before hovering
        return page_actions.hover_on_element(self.driver, selector)

    def hover_and_click(self, hover_selector, click_selector,
                        hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                        timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(hover_selector):
            hover_by = By.XPATH
        if page_utils.is_xpath_selector(click_selector):
            click_by = By.XPATH
        if page_utils.is_link_text_selector(hover_selector):
            hover_selector = page_utils.get_link_text_from_selector(
                hover_selector)
            hover_by = By.LINK_TEXT
        if page_utils.is_link_text_selector(click_selector):
            click_selector = page_utils.get_link_text_from_selector(
                click_selector)
            click_by = By.LINK_TEXT
        self.wait_for_element_visible(
            hover_selector, by=hover_by, timeout=timeout)
        self.__demo_mode_highlight_if_active(hover_selector, hover_by)
        self.scroll_to(hover_selector, by=hover_by)
        pre_action_url = self.driver.current_url
        element = page_actions.hover_and_click(
            self.driver, hover_selector, click_selector,
            hover_by, click_by, timeout)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        return element

    def pick_select_option_by_text(self, dropdown_selector, option,
                                   dropdown_by=By.CSS_SELECTOR,
                                   timeout=settings.LARGE_TIMEOUT):
        """ Picks an HTML <select> option by option text. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__pick_select_option(dropdown_selector, option,
                                  dropdown_by=dropdown_by, option_by="text",
                                  timeout=timeout)

    def pick_select_option_by_index(self, dropdown_selector, option,
                                    dropdown_by=By.CSS_SELECTOR,
                                    timeout=settings.LARGE_TIMEOUT):
        """ Picks an HTML <select> option by option index. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__pick_select_option(dropdown_selector, option,
                                  dropdown_by=dropdown_by, option_by="index",
                                  timeout=timeout)

    def pick_select_option_by_value(self, dropdown_selector, option,
                                    dropdown_by=By.CSS_SELECTOR,
                                    timeout=settings.LARGE_TIMEOUT):
        """ Picks an HTML <select> option by option value. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__pick_select_option(dropdown_selector, option,
                                  dropdown_by=dropdown_by, option_by="value",
                                  timeout=timeout)

    ############

    def generate_referral(self, start_page, destination_page):
        """ This method opens the start_page, creates a referral link there,
            and clicks on that link, which goes to the destination_page.
            (This generates real traffic for testing analytics software.) """
        if not page_utils.is_valid_url(destination_page):
            raise Exception(
                "Exception: destination_page {%s} is not a valid URL!"
                % destination_page)
        if start_page:
            if not page_utils.is_valid_url(start_page):
                raise Exception(
                    "Exception: start_page {%s} is not a valid URL! "
                    "(Use an empty string or None to start from current page.)"
                    % start_page)
            self.open(start_page)
            time.sleep(0.08)
        referral_link = ('''<a class='analytics referral test' href='%s' '''
                         '''style='font-family: Arial,sans-serif; '''
                         '''font-size: 30px; color: #18a2cd'>'''
                         '''Magic Link Button</a>''' % destination_page)
        self.execute_script(
            '''document.body.innerHTML = \"%s\"''' % referral_link)
        time.sleep(0.1)
        self.click("a.analytics.referral.test")  # Clicks the generated button
        time.sleep(0.15)
        try:
            self.click("html")
            time.sleep(0.08)
        except Exception:
            pass

    def generate_traffic(self, start_page, destination_page, loops=1):
        """ Similar to generate_referral(), but can do multiple loops. """
        for loop in range(loops):
            self.generate_referral(start_page, destination_page)
            time.sleep(0.05)

    def generate_referral_chain(self, pages):
        """ Use this method to chain the action of creating button links on
            one website page that will take you to the next page.
            (When you want to create a referral to a website for traffic
            generation without increasing the bounce rate, you'll want to visit
            at least one additional page on that site with a button click.) """
        if not type(pages) is tuple and not type(pages) is list:
            raise Exception(
                "Exception: Expecting a list of website pages for chaining!")
        if len(pages) < 2:
            raise Exception(
                "Exception: At least two website pages required for chaining!")
        for page in pages:
            # Find out if any of the web pages are invalid before continuing
            if not page_utils.is_valid_url(page):
                raise Exception(
                    "Exception: Website page {%s} is not a valid URL!" % page)
        for page in pages:
            self.generate_referral(None, page)

    def generate_traffic_chain(self, pages, loops=1):
        """ Similar to generate_referral_chain(), but for multiple loops. """
        for loop in range(loops):
            self.generate_referral_chain(pages)
            time.sleep(0.05)

    ############

    def wait_for_element_present(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to appear in the HTML of a page.
            The element does not need be visible (it may be hidden). """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def find_element(self, selector, by=By.CSS_SELECTOR,
                     timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_element_visible() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def assert_element(self, selector, by=By.CSS_SELECTOR,
                       timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_visible(selector, by=by, timeout=timeout)

        if self.demo_mode:
            if page_utils.is_xpath_selector(selector):
                by = By.XPATH
            if page_utils.is_link_text_selector(selector):
                selector = page_utils.get_link_text_from_selector(selector)
                by = By.LINK_TEXT
            messenger_post = "ASSERT %s: %s" % (by, selector)
            self.__highlight_with_assert_success(messenger_post, selector, by)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_text_visible(self, text, selector, by=By.CSS_SELECTOR,
                              timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def find_text(self, text, selector, by=By.CSS_SELECTOR,
                  timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_text_visible() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def assert_text_visible(self, text, selector, by=By.CSS_SELECTOR,
                            timeout=settings.SMALL_TIMEOUT):
        """ Same as assert_text() """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.assert_text(text, selector, by=by, timeout=timeout)

    def assert_text(self, text, selector, by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_text_visible()
            Raises an exception if the element or the text is not found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_text_visible(text, selector, by=by, timeout=timeout)

        if self.demo_mode:
            if page_utils.is_xpath_selector(selector):
                by = By.XPATH
            if page_utils.is_link_text_selector(selector):
                selector = page_utils.get_link_text_from_selector(selector)
                by = By.LINK_TEXT
            messenger_post = ("ASSERT TEXT {%s} in %s: %s"
                              % (text, by, selector))
            self.__highlight_with_assert_success(messenger_post, selector, by)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_link_text_visible(self, link_text,
                                   timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(
            link_text, by=By.LINK_TEXT, timeout=timeout)

    def wait_for_link_text(self, link_text, timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_link_text_visible() """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def find_link_text(self, link_text, timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_link_text_visible() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def assert_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_link_text_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_link_text_visible(link_text, timeout=timeout)
        if self.demo_mode:
            messenger_post = ("ASSERT LINK TEXT {%s}." % link_text)
            self.__highlight_with_assert_success(
                messenger_post, link_text, by=By.LINK_TEXT)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_partial_link_text(self, partial_link_text,
                                   timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(
            partial_link_text, by=By.PARTIAL_LINK_TEXT, timeout=timeout)

    def find_partial_link_text(self, partial_link_text,
                               timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_partial_link_text() - returns the element """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_partial_link_text(
            partial_link_text, timeout=timeout)

    def assert_partial_link_text(self, partial_link_text,
                                 timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_partial_link_text(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_absent(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                     timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to no longer be visible on a page.
            The element can be non-existant in the HTML or hidden on the page
            to qualify as not visible. """
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_not_visible(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_ready_state_complete(self, timeout=settings.EXTREME_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        is_ready = page_actions.wait_for_ready_state_complete(self.driver,
                                                              timeout)
        self.wait_for_angularjs(timeout=settings.MINI_TIMEOUT)
        if self.ad_block_on:
            # If the ad_block feature is enabled, then block ads for new URLs
            current_url = self.get_current_url()
            if not current_url == self.__last_page_load_url:
                time.sleep(0.02)
                self.ad_block()
                time.sleep(0.01)
                if self.is_element_present("iframe"):
                    time.sleep(0.07)  # iframe ads take slightly longer to load
                    self.ad_block()  # Do ad_block on slower-loading iframes
                self.__last_page_load_url = current_url
        return is_ready

    def wait_for_angularjs(self, timeout=settings.LARGE_TIMEOUT, **kwargs):
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
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
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def wait_for_and_dismiss_alert(self, timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def wait_for_and_switch_to_alert(self, timeout=settings.LARGE_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)

    def switch_to_frame(self, frame, timeout=settings.SMALL_TIMEOUT):
        """ Sets driver control to the specified browser frame. """
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        page_actions.switch_to_frame(self.driver, frame, timeout)

    def switch_to_default_content(self):
        """ Brings driver control outside the current iframe.
            (If driver control is inside an iframe, the driver control
            will be set to one level above the current frame. If the driver
            control is not currenly in an iframe, nothing will happen.) """
        self.driver.switch_to.default_content()

    def open_new_window(self, switch_to=True):
        """ Opens a new browser tab/window and switches to it by default. """
        self.driver.execute_script("window.open('');")
        time.sleep(0.01)
        if switch_to:
            self.switch_to_window(len(self.driver.window_handles) - 1)

    def switch_to_window(self, window, timeout=settings.SMALL_TIMEOUT):
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        page_actions.switch_to_window(self.driver, window, timeout)

    def switch_to_default_window(self):
        self.switch_to_window(0)

    def save_screenshot(self, name, folder=None):
        """ The screenshot will be in PNG format. """
        return page_actions.save_screenshot(self.driver, name, folder)

    def get_new_driver(self, browser=None, headless=None,
                       servername=None, port=None, proxy=None, switch_to=True):
        """ This method spins up an extra browser for tests that require
            more than one. The first browser is already provided by tests
            that import base_case.BaseCase from seleniumbase. If parameters
            aren't specified, the method uses the same as the default driver.
            @Params
            browser - the browser to use. (Ex: "chrome", "firefox")
            headless - the option to run webdriver in headless mode
            servername - if using a Selenium Grid, set the host address here
            port - if using a Selenium Grid, set the host port here
            proxy - if using a proxy server, specify the "host:port" combo here
            switch_to - the option to switch to the new driver (default = True)
        """
        if browser is None:
            browser = self.browser
        browser_name = browser
        if headless is None:
            headless = self.headless
        if servername is None:
            servername = self.servername
        if port is None:
            port = self.port
        use_grid = False
        if servername != "localhost":
            # Use Selenium Grid (Use "127.0.0.1" for localhost Grid)
            use_grid = True
        proxy_string = proxy
        if proxy_string is None:
            proxy_string = self.proxy_string
        valid_browsers = constants.ValidBrowsers.valid_browsers
        if browser_name not in valid_browsers:
            raise Exception("Browser: {%s} is not a valid browser option. "
                            "Valid options = {%s}" % (browser, valid_browsers))
        # Launch a web browser
        from seleniumbase.core import browser_launcher
        new_driver = browser_launcher.get_driver(browser_name=browser_name,
                                                 headless=headless,
                                                 use_grid=use_grid,
                                                 servername=servername,
                                                 port=port,
                                                 proxy_string=proxy_string)
        self._drivers_list.append(new_driver)
        if switch_to:
            self.driver = new_driver
            if self.headless:
                # Make sure the invisible browser window is big enough
                try:
                    self.set_window_size(1920, 1200)
                    self.wait_for_ready_state_complete()
                except Exception:
                    # This shouldn't fail, but in case it does,
                    # get safely through setUp() so that
                    # WebDrivers can get closed during tearDown().
                    pass
            else:
                if self.browser == 'chrome':
                    try:
                        if settings.START_CHROME_IN_FULL_SCREEN_MODE:
                            self.driver.maximize_window()
                        else:
                            self.driver.set_window_size(1250, 800)
                        self.wait_for_ready_state_complete()
                    except Exception:
                        pass  # Keep existing browser resolution
        return new_driver

    def switch_to_driver(self, driver):
        """ Sets self.driver to the specified driver.
            You may need this if using self.get_new_driver() in your code. """
        self.driver = driver

    def switch_to_default_driver(self):
        """ Sets self.driver to the default/original driver. """
        self.driver = self._default_driver

    ############

    def __get_new_timeout(self, timeout):
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

    def __get_exception_message(self):
        """ This method extracts the message from an exception if there
            was an exception that occurred during the test, assuming
            that the exception was in a try/except block and not thrown. """
        exception_info = sys.exc_info()[1]
        if hasattr(exception_info, 'msg'):
            exc_message = exception_info.msg
        elif hasattr(exception_info, 'message'):
            exc_message = exception_info.message
        else:
            exc_message = '(Unknown Exception)'
        return exc_message

    def __get_improved_exception_message(self):
        """
        If Chromedriver is out-of-date, make it clear!
        Given the high popularity of the following StackOverflow article:
        https://stackoverflow.com/questions/49162667/unknown-error-
                call-function-result-missing-value-for-selenium-send-keys-even
        ... the original error message was not helpful. Tell people directly.
        (Only expected when using driver.send_keys() with an old Chromedriver.)
        """
        exc_message = self.__get_exception_message()
        maybe_using_old_chromedriver = False
        if "unknown error: call function result missing" in exc_message:
            maybe_using_old_chromedriver = True
        if self.browser == 'chrome' and maybe_using_old_chromedriver:
            update = ("Your version of ChromeDriver may be out-of-date! "
                      "Please go to "
                      "https://sites.google.com/a/chromium.org/chromedriver/ "
                      "and download the latest version to your system PATH! "
                      "Or use: ``seleniumbase install chromedriver`` . "
                      "Original Exception Message: %s" % exc_message)
            exc_message = update
        return exc_message

    def __add_delayed_assert_failure(self):
        """ Add a delayed_assert failure into a list for future processing. """
        current_url = self.driver.current_url
        message = self.__get_exception_message()
        self.__page_check_failures.append(
            "CHECK #%s: (%s)\n %s" % (
                self.__page_check_count, current_url, message))

    def delayed_assert_element(self, selector, by=By.CSS_SELECTOR,
                               timeout=settings.MINI_TIMEOUT):
        """ A non-terminating assertion for an element on a page.
            Failures will be saved until the process_delayed_asserts()
            method is called from inside a test, likely at the end of it. """
        self.__page_check_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_delayed_assert:
                timeout = 1
            else:
                self.__last_url_of_delayed_assert = url
        except Exception:
            pass
        try:
            self.wait_for_element_visible(selector, by=by, timeout=timeout)
            return True
        except Exception:
            self.__add_delayed_assert_failure()
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
        self.__page_check_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_delayed_assert:
                timeout = 1
            else:
                self.__last_url_of_delayed_assert = url
        except Exception:
            pass
        try:
            self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
            return True
        except Exception:
            self.__add_delayed_assert_failure()
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
        if self.__page_check_failures:
            exception_output = ''
            exception_output += "\n*** DELAYED ASSERTION FAILURES FOR: "
            exception_output += "%s\n" % self.id()
            all_failing_checks = self.__page_check_failures
            self.__page_check_failures = []
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

    def __js_click(self, selector, by=By.CSS_SELECTOR):
        """ Clicks an element using pure JS. Does not use jQuery. """
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = ("""var simulateClick = function (elem) {
                         var evt = new MouseEvent('click', {
                             bubbles: true,
                             cancelable: true,
                             view: window
                         });
                         var canceled = !elem.dispatchEvent(evt);
                     };
                     var someLink = document.querySelector('%s');
                     simulateClick(someLink);"""
                  % css_selector)
        self.execute_script(script)

    def __jquery_click(self, selector, by=By.CSS_SELECTOR):
        """ Clicks an element using jQuery. Different from using pure JS. """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        click_script = """jQuery('%s')[0].click()""" % selector
        self.safe_execute_script(click_script)

    def __get_href_from_link_text(self, link_text, hard_fail=True):
        href = self.get_link_attribute(link_text, "href", hard_fail)
        if not href:
            return None
        if href.startswith('//'):
            link = "http:" + href
        elif href.startswith('/'):
            url = self.driver.current_url
            domain_url = self.get_domain_url(url)
            link = domain_url + href
        else:
            link = href
        return link

    def __click_dropdown_link_text(self, link_text, link_css):
        """ When a link may be hidden under a dropdown menu, use this. """
        source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        drop_down_list = soup.select('[class*=dropdown]')
        csstype = link_css.split('[')[1].split('=')[0]
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
                            self.driver, dropdown, link_text,
                            click_by=By.LINK_TEXT, timeout=0.1)
                        return True
                    except Exception:
                        pass
        return False

    def __pick_select_option(self, dropdown_selector, option,
                             dropdown_by=By.CSS_SELECTOR, option_by="text",
                             timeout=settings.SMALL_TIMEOUT):
        """ Picks an HTML <select> option by specification.
            Option specifications are by "text", "index", or "value".
            Defaults to "text" if option_by is unspecified or unknown. """
        element = self.find_element(
            dropdown_selector, by=dropdown_by, timeout=timeout)
        self.__demo_mode_highlight_if_active(dropdown_selector, dropdown_by)
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
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)

    def __recalculate_selector(self, selector, by):
        # Try to determine the type of selector automatically
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        return (selector, by)

    def __make_css_match_first_element_only(self, selector):
        # Only get the first match
        last_syllable = selector.split(' ')[-1]
        if ':' not in last_syllable and ':contains' not in selector:
            selector += ':first'
        return selector

    def __demo_mode_pause_if_active(self, tiny=False):
        if self.demo_mode:
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            else:
                wait_time = settings.DEFAULT_DEMO_MODE_TIMEOUT
            if not tiny:
                time.sleep(wait_time)
            else:
                time.sleep(wait_time / 3.4)

    def __demo_mode_scroll_if_active(self, selector, by):
        if self.demo_mode:
            self.slow_scroll_to(selector, by=by)

    def __demo_mode_highlight_if_active(self, selector, by):
        if self.demo_mode:
            # Includes self.slow_scroll_to(selector, by=by) by default
            self.highlight(selector, by=by)

    def __scroll_to_element(self, element):
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
        self.__demo_mode_pause_if_active(tiny=True)

    def __slow_scroll_to_element(self, element):
        if self.browser == 'ie':
            # IE breaks on slow-scrolling. Do a fast scroll instead.
            self.__scroll_to_element(element)
            return
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

    def __post_messenger_success_message(self, message, duration=None):
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        try:
            self.set_messenger_theme(theme="future", location="bottom_right")
            self.post_message(message, style="success", duration=duration)
            time.sleep(duration)
        except Exception:
            pass

    def __post_messenger_error_message(self, message, duration=None):
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        try:
            self.set_messenger_theme(theme="block", location="top_center")
            self.post_message(message, style="error", duration=duration)
            time.sleep(duration)
        except Exception:
            pass

    def __highlight_with_assert_success(
            self, message, selector, by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        element = self.find_element(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't highlight if can't convert to CSS_SELECTOR
            return

        o_bs = ''  # original_box_shadow
        style = element.get_attribute('style')
        if style:
            if 'box-shadow: ' in style:
                box_start = style.find('box-shadow: ')
                box_end = style.find(';', box_start) + 1
                original_box_shadow = style[box_start:box_end]
                o_bs = original_box_shadow

        if ":contains" not in selector and ":first" not in selector:
            selector = re.escape(selector)
            selector = self.__escape_quotes_if_needed(selector)
            self.__highlight_with_js_2(message, selector, o_bs)
        else:
            selector = self.__make_css_match_first_element_only(selector)
            selector = re.escape(selector)
            selector = self.__escape_quotes_if_needed(selector)
            try:
                self.__highlight_with_jquery_2(message, selector, o_bs)
            except Exception:
                pass  # JQuery probably couldn't load. Skip highlighting.
        time.sleep(0.065)

    def __highlight_with_js_2(self, message, selector, o_bs):
        script = ("""document.querySelector('%s').style =
                  'box-shadow: 0px 0px 6px 6px rgba(128, 128, 128, 0.5)';"""
                  % selector)
        self.execute_script(script)
        time.sleep(0.0181)
        script = ("""document.querySelector('%s').style =
                  'box-shadow: 0px 0px 6px 6px rgba(205, 30, 0, 1)';"""
                  % selector)
        self.execute_script(script)
        time.sleep(0.0181)
        script = ("""document.querySelector('%s').style =
                  'box-shadow: 0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
                  % selector)
        self.execute_script(script)
        time.sleep(0.0181)
        script = ("""document.querySelector('%s').style =
                  'box-shadow: 0px 0px 6px 6px rgba(50, 50, 128, 1)';"""
                  % selector)
        self.execute_script(script)
        time.sleep(0.0181)
        script = ("""document.querySelector('%s').style =
                  'box-shadow: 0px 0px 6px 6px rgba(50, 205, 50, 1)';"""
                  % selector)
        self.execute_script(script)
        time.sleep(0.0181)

        self.__post_messenger_success_message(message)

        script = ("""document.querySelector('%s').style =
                  'box-shadow: %s';"""
                  % (selector, o_bs))
        self.execute_script(script)

    def __highlight_with_jquery_2(self, message, selector, o_bs):
        script = """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(128, 128, 128, 0.5)');""" % selector
        self.safe_execute_script(script)
        time.sleep(0.0181)
        script = """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(205, 30, 0, 1)');""" % selector
        self.execute_script(script)
        time.sleep(0.0181)
        script = """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(128, 0, 128, 1)');""" % selector
        self.execute_script(script)
        time.sleep(0.0181)
        script = """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(50, 50, 200, 1)');""" % selector
        self.execute_script(script)
        time.sleep(0.0181)
        script = """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(50, 205, 50, 1)');""" % selector
        self.execute_script(script)
        time.sleep(0.0181)

        self.__post_messenger_success_message(message)

        script = """jQuery('%s').css('box-shadow', '%s');""" % (selector, o_bs)
        self.execute_script(script)

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
            self.environment = pytest.config.option.environment
            self.env = self.environment  # Add a shortened version
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
            self.message_duration = pytest.config.option.message_duration
            self.ad_block_on = pytest.config.option.ad_block_on
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
                data_payload.test_address = test_id
                application = ApplicationManager.generate_application_string(
                    self._testMethodName)
                data_payload.env = application.split('.')[0]
                data_payload.start_time = application.split('.')[1]
                data_payload.state = constants.State.NOTRUN
                self.testcase_manager.insert_testcase_data(data_payload)
                self.case_start_time = int(time.time() * 1000)
            if self.headless:
                try:
                    from pyvirtualdisplay import Display
                    self.display = Display(visible=0, size=(1920, 1200))
                    self.display.start()
                    self.headless_active = True
                except Exception:
                    # pyvirtualdisplay might not be necessary anymore because
                    # Chrome and Firefox now have built-in headless displays
                    pass

        # Launch WebDriver for both Pytest and Nosetests
        if not hasattr(self, "browser"):
            raise Exception("""SeleniumBase plugins did not load! """
                            """Please reinstall using:\n"""
                            """ >>> "python setup.py develop" <<< """)
        self.driver = self.get_new_driver(browser=self.browser,
                                          headless=self.headless,
                                          servername=self.servername,
                                          port=self.port,
                                          proxy=self.proxy_string,
                                          switch_to=True)
        self._default_driver = self.driver

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

    def __add_pytest_html_extra(self):
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

    def __quit_all_drivers(self):
        # Close all open browser windows
        self._drivers_list.reverse()  # Last In, First Out
        for driver in self._drivers_list:
            try:
                driver.quit()
            except AttributeError:
                pass
            except Exception:
                pass
        self.driver = None
        self._drivers_list = []

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
        if self.__page_check_failures:
            print(
                "\nWhen using self.delayed_assert_*() methods in your tests, "
                "remember to call self.process_delayed_asserts() afterwards. "
                "Now calling in tearDown()...\nFailures Detected:")
            if not has_exception:
                self.process_delayed_asserts()
            else:
                self.process_delayed_asserts(print_only=True)
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
            try:
                with_selenium = self.with_selenium
            except Exception:
                sub_class_name = str(
                    self.__class__.__bases__[0]).split('.')[-1].split("'")[0]
                sub_file_name = str(self.__class__.__bases__[0]).split('.')[-2]
                sub_file_name = sub_file_name + ".py"
                class_name = str(self.__class__).split('.')[-1].split("'")[0]
                file_name = str(self.__class__).split('.')[-2] + ".py"
                class_name_used = sub_class_name
                file_name_used = sub_file_name
                if sub_class_name == "BaseCase":
                    class_name_used = class_name
                    file_name_used = file_name
                fix_setup = "super(%s, self).setUp()" % class_name_used
                fix_teardown = "super(%s, self).tearDown()" % class_name_used
                message = ("You're overriding SeleniumBase's BaseCase setUp() "
                           "method with your own setUp() method, which breaks "
                           "SeleniumBase. You can fix this by going to your "
                           "%s class located in your %s file and adding the "
                           "following line of code AT THE BEGINNING of your "
                           "setUp() method:\n%s\n\nAlso make sure "
                           "you have added the following line of code AT THE "
                           "END of your tearDown() method:\n%s\n"
                           % (class_name_used, file_name_used,
                              fix_setup, fix_teardown))
                raise Exception(message)
            if with_selenium:
                # Save a screenshot if logging is on when an exception occurs
                if has_exception:
                    self.__add_pytest_html_extra()
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
                # (Pytest) Finally close all open browser windows
                self.__quit_all_drivers()
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
                """ If enabled, upload logs to S3 during test exceptions. """
                from seleniumbase.core.s3_manager import S3LoggingBucket
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
            # (Nosetests)
            if has_exception:
                test_id = "%s.%s.%s" % (self.__class__.__module__,
                                        self.__class__.__name__,
                                        self._testMethodName)
                test_logpath = "latest_logs/" + test_id
                if not os.path.exists(test_logpath):
                    os.makedirs(test_logpath)
                log_helper.log_test_failure_data(
                    self, test_logpath, self.driver, self.browser)
                if len(self._drivers_list) > 0:
                    log_helper.log_screenshot(test_logpath, self.driver)
                    log_helper.log_page_source(test_logpath, self.driver)
            # Finally close all open browser windows
            self.__quit_all_drivers()
