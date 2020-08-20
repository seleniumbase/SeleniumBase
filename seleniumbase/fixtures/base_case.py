# -*- coding: utf-8 -*-
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
            self.type("input.header-search-input", "SeleniumBase\n")
            self.click('a[href="/seleniumbase/SeleniumBase"]')
            self.assert_element("div.repository-content")
            ....

SeleniumBase methods expand and improve on existing WebDriver commands.
Improvements include making WebDriver more robust, reliable, and flexible.
Page elements are given enough time to load before WebDriver acts on them.
Code becomes greatly simplified and easier to maintain.
"""

import codecs
import json
import logging
import math
import os
import re
import sys
import time
import urllib3
import unittest
from selenium.common.exceptions import (StaleElementReferenceException,
                                        MoveTargetOutOfBoundsException,
                                        WebDriverException)
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
from seleniumbase import config as sb_config
from seleniumbase.common import decorators
from seleniumbase.config import settings
from seleniumbase.core import log_helper
from seleniumbase.core import tour_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import js_utils
from seleniumbase.fixtures import page_actions
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import shared_utils
from seleniumbase.fixtures import xpath_to_css
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
urllib3.disable_warnings()
LOGGER.setLevel(logging.WARNING)
SSMD = constants.Values.SSMD  # Smooth Scrolling
JS_Exc = selenium_exceptions.JavascriptException
ECI_Exception = selenium_exceptions.ElementClickInterceptedException
ENI_Exception = selenium_exceptions.ElementNotInteractableException


class BaseCase(unittest.TestCase):
    """ <Class seleniumbase.BaseCase> """

    def __init__(self, *args, **kwargs):
        super(BaseCase, self).__init__(*args, **kwargs)
        self.driver = None
        self.environment = None
        self.env = None  # Add a shortened version of self.environment
        self.__last_url_of_deferred_assert = "data:,"
        self.__last_page_load_url = "data:,"
        self.__last_page_screenshot = None
        self.__last_page_screenshot_png = None
        self.__last_page_url = None
        self.__last_page_source = None
        self.__added_pytest_html_extra = None
        self.__deferred_assert_count = 0
        self.__deferred_assert_failures = []
        self.__device_width = None
        self.__device_height = None
        self.__device_pixel_ratio = None
        # Requires self._* instead of self.__* for external class use
        self._language = "English"
        self._presentation_slides = {}
        self._presentation_transition = {}
        self._sb_test_identifier = None
        self._html_report_extra = []  # (Used by pytest_plugin.py)
        self._default_driver = None
        self._drivers_list = []
        self._chart_data = {}
        self._chart_count = 0
        self._chart_label = {}
        self._chart_first_series = {}
        self._chart_series_count = {}
        self._tour_steps = {}

    def open(self, url):
        """ Navigates the current browser window to the specified page. """
        if type(url) is str:
            url = url.strip()  # Remove leading and trailing whitespace
        if (type(url) is not str) or not self.__looks_like_a_page_url(url):
            # url should start with one of the following:
            # "http:", "https:", "://", "data:", "file:",
            # "about:", "chrome:", "opera:", or "edge:".
            msg = 'Did you forget to prefix your URL with "http:" or "https:"?'
            raise Exception('Invalid URL: "%s"\n%s' % (url, msg))
        self.__last_page_load_url = None
        js_utils.clear_out_console_logs(self.driver)
        if url.startswith("://"):
            # Convert URLs such as "://google.com" into "https://google.com"
            url = "https" + url
        self.driver.get(url)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def get(self, url):
        """ If url looks like a page URL, opens the URL in the web browser.
            Otherwise, returns self.get_element(URL_AS_A_SELECTOR)
            Examples:
                self.get("https://seleniumbase.io")  # Navigates to the URL
                self.get("input.class")  # Finds and returns the WebElement
        """
        if self.__looks_like_a_page_url(url):
            self.open(url)
        else:
            return self.get_element(url)  # url is treated like a selector

    def click(self, selector, by=By.CSS_SELECTOR, timeout=None, delay=0):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if page_utils.is_link_text_selector(selector) or by == By.LINK_TEXT:
            if not self.is_link_text_visible(selector):
                # Handle a special case of links hidden in dropdowns
                self.click_link_text(selector, timeout=timeout)
                return
        if page_utils.is_partial_link_text_selector(selector) or (
                by == By.PARTIAL_LINK_TEXT):
            if not self.is_partial_link_text_visible(selector):
                # Handle a special case of partial links hidden in dropdowns
                self.click_partial_link_text(selector, timeout=timeout)
                return
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        pre_action_url = self.driver.current_url
        if delay and delay > 0:
            time.sleep(delay)
        try:
            if self.browser == 'ie' and by == By.LINK_TEXT:
                # An issue with clicking Link Text on IE means using jquery
                self.__jquery_click(selector, by=by)
            elif self.browser == "safari":
                if by == By.LINK_TEXT:
                    self.__jquery_click(selector, by=by)
                else:
                    self.__js_click(selector, by=by)
            else:
                # Normal click
                element.click()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout=timeout)
            if self.browser == "safari":
                if by == By.LINK_TEXT:
                    self.__jquery_click(selector, by=by)
                else:
                    self.__js_click(selector, by=by)
            else:
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
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def slow_click(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Similar to click(), but pauses for a brief moment before clicking.
            When used in combination with setting the user-agent, you can often
            bypass bot-detection by tricking websites into thinking that you're
            not a bot. (Useful on websites that block web automation tools.)
            To set the user-agent, use: ``--agent=AGENT``.
            Here's an example message from GitHub's bot-blocker:
            ``You have triggered an abuse detection mechanism...`` """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if not self.demo_mode and not self.slow_mode:
            self.click(selector, by=by, timeout=timeout, delay=1.05)
        elif self.slow_mode:
            self.click(selector, by=by, timeout=timeout, delay=0.65)
        else:
            # Demo Mode already includes a small delay
            self.click(selector, by=by, timeout=timeout, delay=0.25)

    def double_click(self, selector, by=By.CSS_SELECTOR, timeout=None):
        from selenium.webdriver.common.action_chains import ActionChains
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        pre_action_url = self.driver.current_url
        try:
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout=timeout)
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
        except Exception:
            css_selector = self.convert_to_css_selector(selector, by=by)
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            double_click_script = (
                """var targetElement1 = document.querySelector('%s');
                var clickEvent1 = document.createEvent('MouseEvents');
                clickEvent1.initEvent('dblclick', true, true);
                targetElement1.dispatchEvent(clickEvent1);""" % css_selector)
            if ":contains\\(" not in css_selector:
                self.execute_script(double_click_script)
            else:
                double_click_script = (
                    """jQuery('%s').dblclick();""" % css_selector)
                self.safe_execute_script(double_click_script)
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def click_chain(self, selectors_list, by=By.CSS_SELECTOR,
                    timeout=None, spacing=0):
        """ This method clicks on a list of elements in succession.
            'spacing' is the amount of time to wait between clicks. (sec) """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        for selector in selectors_list:
            self.click(selector, by=by, timeout=timeout)
            if spacing > 0:
                time.sleep(spacing)

    def update_text(self, selector, text, by=By.CSS_SELECTOR,
                    timeout=None, retry=False):
        """ This method updates an element's text field with new text.
            Has multiple parts:
            * Waits for the element to be visible.
            * Waits for the element to be interactive.
            * Clears the text field.
            * Types in the new text.
            * Hits Enter/Submit (if the text ends in "\n").
            @Params
            selector - the selector of the text field
            text - the new text to type into the text field
            by - the type of selector to search by (Default: CSS Selector)
            timeout - how long to wait for the selector to be visible
            retry - if True, use JS if the Selenium text update fails
        """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        try:
            element.clear()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            try:
                element.clear()
            except Exception:
                pass  # Clearing the text field first isn't critical
        except Exception:
            pass  # Clearing the text field first isn't critical
        self.__demo_mode_pause_if_active(tiny=True)
        pre_action_url = self.driver.current_url
        if type(text) is int or type(text) is float:
            text = str(text)
        try:
            if not text.endswith('\n'):
                element.send_keys(text)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
            else:
                element.send_keys(text[:-1])
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            element.clear()
            if not text.endswith('\n'):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        except Exception:
            exc_message = self.__get_improved_exception_message()
            raise Exception(exc_message)
        if (retry and element.get_attribute('value') != text and (
                not text.endswith('\n'))):
            logging.debug('update_text() is falling back to JavaScript!')
            self.set_value(selector, text, by=by)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def add_text(self, selector, text, by=By.CSS_SELECTOR, timeout=None):
        """ The more-reliable version of driver.send_keys()
            Similar to update_text(), but won't clear the text field first. """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        pre_action_url = self.driver.current_url
        try:
            if not text.endswith('\n'):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            if not text.endswith('\n'):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
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
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def type(self, selector, text, by=By.CSS_SELECTOR,
             timeout=None, retry=False):
        """ Same as self.update_text()
            This method updates an element's text field with new text.
            Has multiple parts:
            * Waits for the element to be visible.
            * Waits for the element to be interactive.
            * Clears the text field.
            * Types in the new text.
            * Hits Enter/Submit (if the text ends in "\n").
            @Params
            selector - the selector of the text field
            text - the new text to type into the text field
            by - the type of selector to search by (Default: CSS Selector)
            timeout - how long to wait for the selector to be visible
            retry - if True, use JS if the Selenium text update fails
            DO NOT confuse self.type() with Python type()! They are different!
        """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.update_text(selector, text, by=by, timeout=timeout, retry=retry)

    def submit(self, selector, by=By.CSS_SELECTOR):
        """ Alternative to self.driver.find_element_by_*(SELECTOR).submit() """
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        element.submit()
        self.__demo_mode_pause_if_active()

    def refresh_page(self):
        self.__last_page_load_url = None
        js_utils.clear_out_console_logs(self.driver)
        self.driver.refresh()
        self.wait_for_ready_state_complete()

    def refresh(self):
        """ The shorter version of self.refresh_page() """
        self.refresh_page()

    def get_current_url(self):
        current_url = self.driver.current_url
        if "%" in current_url and sys.version_info[0] >= 3:
            try:
                from urllib.parse import unquote
                current_url = unquote(current_url, errors='strict')
            except Exception:
                pass
        return current_url

    def get_page_source(self):
        self.wait_for_ready_state_complete()
        return self.driver.page_source

    def get_page_title(self):
        self.wait_for_ready_state_complete()
        self.wait_for_element_present("title", timeout=settings.SMALL_TIMEOUT)
        time.sleep(0.03)
        return self.driver.title

    def get_title(self):
        """ The shorter version of self.get_page_title() """
        return self.get_page_title()

    def get_user_agent(self):
        user_agent = self.driver.execute_script("return navigator.userAgent;")
        return user_agent

    def go_back(self):
        self.__last_page_load_url = None
        if self.browser != "safari":
            self.driver.back()
        else:
            self.sleep(0.05)
            self.execute_script("window.location=document.referrer;")
            self.sleep(0.05)
        self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def go_forward(self):
        self.__last_page_load_url = None
        if self.browser != "safari":
            self.driver.forward()
        else:
            self.sleep(0.05)
            self.execute_script("window.history.forward();")
            self.sleep(0.05)
        self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def is_element_present(self, selector, by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.is_element_present(self.driver, selector, by)

    def is_element_visible(self, selector, by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.is_element_visible(self.driver, selector, by)

    def is_text_visible(self, text, selector="html", by=By.CSS_SELECTOR):
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.is_text_visible(self.driver, text, selector, by)

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

    def is_link_text_present(self, link_text):
        """ Returns True if the link text appears in the HTML of the page.
            The element doesn't need to be visible,
            such as elements hidden inside a dropdown selection. """
        soup = self.get_beautiful_soup()
        html_links = soup.find_all('a')
        for html_link in html_links:
            if html_link.text.strip() == link_text.strip():
                return True
        return False

    def is_partial_link_text_present(self, link_text):
        """ Returns True if the partial link appears in the HTML of the page.
            The element doesn't need to be visible,
            such as elements hidden inside a dropdown selection. """
        soup = self.get_beautiful_soup()
        html_links = soup.find_all('a')
        for html_link in html_links:
            if link_text.strip() in html_link.text.strip():
                return True
        return False

    def get_link_attribute(self, link_text, attribute, hard_fail=True):
        """ Finds a link by link text and then returns the attribute's value.
            If the link text or attribute cannot be found, an exception will
            get raised if hard_fail is True (otherwise None is returned). """
        soup = self.get_beautiful_soup()
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

    def get_link_text_attribute(self, link_text, attribute, hard_fail=True):
        """ Same as self.get_link_attribute()
            Finds a link by link text and then returns the attribute's value.
            If the link text or attribute cannot be found, an exception will
            get raised if hard_fail is True (otherwise None is returned). """
        return self.get_link_attribute(link_text, attribute, hard_fail)

    def get_partial_link_text_attribute(self, link_text, attribute,
                                        hard_fail=True):
        """ Finds a link by partial link text and then returns the attribute's
            value. If the partial link text or attribute cannot be found, an
            exception will get raised if hard_fail is True (otherwise None
            is returned). """
        soup = self.get_beautiful_soup()
        html_links = soup.find_all('a')
        for html_link in html_links:
            if link_text.strip() in html_link.text.strip():
                if html_link.has_attr(attribute):
                    attribute_value = html_link.get(attribute)
                    return attribute_value
                if hard_fail:
                    raise Exception(
                        'Unable to find attribute {%s} from '
                        'partial link text {%s}!'
                        % (attribute, link_text))
                else:
                    return None
        if hard_fail:
            raise Exception(
                "Partial Link text {%s} was not found!" % link_text)
        else:
            return None

    def click_link_text(self, link_text, timeout=None):
        """ This method clicks link text on a page """
        # If using phantomjs, might need to extract and open the link directly
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if self.browser == 'phantomjs':
            if self.is_link_text_visible(link_text):
                element = self.wait_for_link_text_visible(
                    link_text, timeout=timeout)
                element.click()
                return
            self.open(self.__get_href_from_link_text(link_text))
            return
        if self.browser == "safari":
            if self.demo_mode:
                self.wait_for_link_text_present(link_text, timeout=timeout)
                try:
                    self.__jquery_slow_scroll_to(link_text, by=By.LINK_TEXT)
                except Exception:
                    pass
                o_bs = ''  # original_box_shadow
                loops = settings.HIGHLIGHTS
                selector = self.convert_to_css_selector(
                    link_text, by=By.LINK_TEXT)
                selector = self.__make_css_match_first_element_only(selector)
                try:
                    selector = re.escape(selector)
                    selector = self.__escape_quotes_if_needed(selector)
                    self.__highlight_with_jquery(selector, loops, o_bs)
                except Exception:
                    pass  # JQuery probably couldn't load. Skip highlighting.
            self.__jquery_click(link_text, by=By.LINK_TEXT)
            return
        if not self.is_link_text_present(link_text):
            self.wait_for_link_text_present(link_text, timeout=timeout)
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
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def click_partial_link_text(self, partial_link_text, timeout=None):
        """ This method clicks the partial link text on a page. """
        # If using phantomjs, might need to extract and open the link directly
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if self.browser == 'phantomjs':
            if self.is_partial_link_text_visible(partial_link_text):
                element = self.wait_for_partial_link_text(partial_link_text)
                element.click()
                return
            soup = self.get_beautiful_soup()
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
        if not self.is_partial_link_text_present(partial_link_text):
            self.wait_for_partial_link_text_present(
                partial_link_text, timeout=timeout)
        pre_action_url = self.get_current_url()
        try:
            element = self.wait_for_partial_link_text(
                partial_link_text, timeout=0.2)
            self.__demo_mode_highlight_if_active(
                partial_link_text, by=By.LINK_TEXT)
            try:
                element.click()
            except (StaleElementReferenceException, ENI_Exception):
                self.wait_for_ready_state_complete()
                time.sleep(0.05)
                element = self.wait_for_partial_link_text(
                    partial_link_text, timeout=timeout)
                element.click()
        except Exception:
            found_css = False
            text_id = self.get_partial_link_text_attribute(
                partial_link_text, "id", False)
            if text_id:
                link_css = '[id="%s"]' % partial_link_text
                found_css = True

            if not found_css:
                href = self.__get_href_from_partial_link_text(
                    partial_link_text, False)
                if href:
                    if href.startswith('/') or page_utils.is_valid_url(href):
                        link_css = '[href="%s"]' % href
                        found_css = True

            if not found_css:
                ngclick = self.get_partial_link_text_attribute(
                    partial_link_text, "ng-click", False)
                if ngclick:
                    link_css = '[ng-click="%s"]' % ngclick
                    found_css = True

            if not found_css:
                onclick = self.get_partial_link_text_attribute(
                    partial_link_text, "onclick", False)
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
                    success = self.__click_dropdown_partial_link_text(
                        partial_link_text, link_css)

            if not success:
                element = self.wait_for_link_text_visible(
                    partial_link_text, timeout=settings.MINI_TIMEOUT)
                element.click()

        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def get_text(self, selector, by=By.CSS_SELECTOR, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
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
                      timeout=None, hard_fail=True):
        """ This method uses JavaScript to get the value of an attribute. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
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
            if hard_fail:
                raise Exception("Element {%s} has no attribute {%s}!" % (
                    selector, attribute))
            else:
                return None

    def set_attribute(self, selector, attribute, value, by=By.CSS_SELECTOR,
                      timeout=None):
        """ This method uses JavaScript to set/update an attribute.
            Only the first matching selector from querySelector() is used. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_element_visible(selector, by=by):
            try:
                self.scroll_to(selector, by=by, timeout=timeout)
            except Exception:
                pass
        attribute = re.escape(attribute)
        attribute = self.__escape_quotes_if_needed(attribute)
        value = re.escape(value)
        value = self.__escape_quotes_if_needed(value)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = ("""document.querySelector('%s').setAttribute('%s','%s');"""
                  % (css_selector, attribute, value))
        self.execute_script(script)

    def set_attributes(self, selector, attribute, value, by=By.CSS_SELECTOR):
        """ This method uses JavaScript to set/update a common attribute.
            All matching selectors from querySelectorAll() are used.
            Example => (Make all links on a website redirect to Google):
            self.set_attributes("a", "href", "https://google.com") """
        selector, by = self.__recalculate_selector(selector, by)
        attribute = re.escape(attribute)
        attribute = self.__escape_quotes_if_needed(attribute)
        value = re.escape(value)
        value = self.__escape_quotes_if_needed(value)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = ("""var $elements = document.querySelectorAll('%s');
                  var index = 0, length = $elements.length;
                  for(; index < length; index++){
                  $elements[index].setAttribute('%s','%s');}"""
                  % (css_selector, attribute, value))
        try:
            self.execute_script(script)
        except Exception:
            pass

    def set_attribute_all(self, selector, attribute, value,
                          by=By.CSS_SELECTOR):
        """ Same as set_attributes(), but using querySelectorAll naming scheme.
            This method uses JavaScript to set/update a common attribute.
            All matching selectors from querySelectorAll() are used.
            Example => (Make all links on a website redirect to Google):
            self.set_attribute_all("a", "href", "https://google.com") """
        self.set_attributes(selector, attribute, value, by=by)

    def remove_attribute(self, selector, attribute, by=By.CSS_SELECTOR,
                         timeout=None):
        """ This method uses JavaScript to remove an attribute.
            Only the first matching selector from querySelector() is used. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_element_visible(selector, by=by):
            try:
                self.scroll_to(selector, by=by, timeout=timeout)
            except Exception:
                pass
        attribute = re.escape(attribute)
        attribute = self.__escape_quotes_if_needed(attribute)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = ("""document.querySelector('%s').removeAttribute('%s');"""
                  % (css_selector, attribute))
        self.execute_script(script)

    def remove_attributes(self, selector, attribute, by=By.CSS_SELECTOR):
        """ This method uses JavaScript to remove a common attribute.
            All matching selectors from querySelectorAll() are used. """
        selector, by = self.__recalculate_selector(selector, by)
        attribute = re.escape(attribute)
        attribute = self.__escape_quotes_if_needed(attribute)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = ("""var $elements = document.querySelectorAll('%s');
                  var index = 0, length = $elements.length;
                  for(; index < length; index++){
                  $elements[index].removeAttribute('%s');}"""
                  % (css_selector, attribute))
        try:
            self.execute_script(script)
        except Exception:
            pass

    def get_property_value(self, selector, property, by=By.CSS_SELECTOR,
                           timeout=None):
        """ Returns the property value of a page element's computed style.
            Example:
                opacity = self.get_property_value("html body a", "opacity")
                self.assertTrue(float(opacity) > 0, "Element not visible!") """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
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

    def get_image_url(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Extracts the URL from an image element on the page. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.get_attribute(selector,
                                  attribute='src', by=by, timeout=timeout)

    def find_elements(self, selector, by=By.CSS_SELECTOR, limit=0):
        """ Returns a list of matching WebElements.
            Elements could be either hidden or visible on the page.
            If "limit" is set and > 0, will only return that many elements. """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        time.sleep(0.05)
        elements = self.driver.find_elements(by=by, value=selector)
        if limit and limit > 0 and len(elements) > limit:
            elements = elements[:limit]
        return elements

    def find_visible_elements(self, selector, by=By.CSS_SELECTOR, limit=0):
        """ Returns a list of matching WebElements that are visible.
            If "limit" is set and > 0, will only return that many elements. """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        time.sleep(0.05)
        v_elems = page_actions.find_visible_elements(self.driver, selector, by)
        if limit and limit > 0 and len(v_elems) > limit:
            v_elems = v_elems[:limit]
        return v_elems

    def click_visible_elements(self, selector, by=By.CSS_SELECTOR, limit=0):
        """ Finds all matching page elements and clicks visible ones in order.
            If a click reloads or opens a new page, the clicking will stop.
            If no matching elements appear, an Exception will be raised.
            If "limit" is set and > 0, will only click that many elements.
            Also clicks elements that become visible from previous clicks.
            Works best for actions such as clicking all checkboxes on a page.
            Example:  self.click_visible_elements('input[type="checkbox"]') """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        elements = self.find_elements(selector, by=by)
        if self.browser == "safari":
            if not limit:
                limit = 0
            num_elements = len(elements)
            if num_elements == 0:
                raise Exception(
                    "No matching elements found for selector {%s}!" % selector)
            elif num_elements < limit or limit == 0:
                limit = num_elements
            selector, by = self.__recalculate_selector(selector, by)
            css_selector = self.convert_to_css_selector(selector, by=by)
            last_css_chunk = css_selector.split(' ')[-1]
            if ":" in last_css_chunk:
                self.__js_click_all(css_selector)
                self.wait_for_ready_state_complete()
                return
            else:
                for i in range(1, limit+1):
                    new_selector = css_selector + ":nth-of-type(%s)" % str(i)
                    if self.is_element_visible(new_selector):
                        self.__js_click(new_selector)
                        self.wait_for_ready_state_complete()
                return
        click_count = 0
        for element in elements:
            if limit and limit > 0 and click_count >= limit:
                return
            try:
                if element.is_displayed():
                    self.__scroll_to_element(element)
                    element.click()
                    click_count += 1
                    self.wait_for_ready_state_complete()
            except ECI_Exception:
                continue  # ElementClickInterceptedException (Overlay likely)
            except (StaleElementReferenceException, ENI_Exception):
                self.wait_for_ready_state_complete()
                time.sleep(0.04)
                try:
                    if element.is_displayed():
                        self.__scroll_to_element(element)
                        element.click()
                        click_count += 1
                        self.wait_for_ready_state_complete()
                except (StaleElementReferenceException, ENI_Exception):
                    return  # Probably on new page / Elements are all stale

    def click_nth_visible_element(self, selector, number, by=By.CSS_SELECTOR):
        """ Finds all matching page elements and clicks the nth visible one.
            Example:  self.click_nth_visible_element('[type="checkbox"]', 5)
                        (Clicks the 5th visible checkbox on the page.) """
        elements = self.find_visible_elements(selector, by=by)
        if len(elements) < number:
            raise Exception("Not enough matching {%s} elements of type {%s} to"
                            " click number %s!" % (selector, by, number))
        number = number - 1
        if number < 0:
            number = 0
        element = elements[number]
        self.wait_for_ready_state_complete()
        try:
            self.__scroll_to_element(element)
            element.click()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.03)
            self.__scroll_to_element(element)
            element.click()

    def click_if_visible(self, selector, by=By.CSS_SELECTOR):
        """ If the page selector exists and is visible, clicks on the element.
            This method only clicks on the first matching element found.
            (Use click_visible_elements() to click all matching elements.) """
        self.wait_for_ready_state_complete()
        if self.is_element_visible(selector, by=by):
            self.click(selector, by=by)

    def is_checked(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Determines if a checkbox or a radio button element is checked.
            Returns True if the element is checked.
            Returns False if the element is not checked.
            If the element is not present on the page, raises an exception.
            If the element is not a checkbox or radio, raises an exception. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        kind = self.get_attribute(selector, "type", by=by, timeout=timeout)
        if kind != "checkbox" and kind != "radio":
            raise Exception("Expecting a checkbox or a radio button element!")
        is_checked = self.get_attribute(
            selector, "checked", by=by, timeout=timeout, hard_fail=False)
        if is_checked:
            return True
        else:  # (NoneType)
            return False

    def is_selected(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Same as is_checked() """
        return self.is_checked(selector, by=by, timeout=timeout)

    def check_if_unchecked(self, selector, by=By.CSS_SELECTOR):
        """ If a checkbox or radio button is not checked, will check it. """
        selector, by = self.__recalculate_selector(selector, by)
        if not self.is_checked(selector, by=by):
            if self.is_element_visible(selector, by=by):
                self.click(selector, by=by)
            else:
                selector = self.convert_to_css_selector(selector, by=by)
                self.js_click(selector, by=By.CSS_SELECTOR)

    def select_if_unselected(self, selector, by=By.CSS_SELECTOR):
        """ Same as check_if_unchecked() """
        self.check_if_unchecked(selector, by=by)

    def uncheck_if_checked(self, selector, by=By.CSS_SELECTOR):
        """ If a checkbox is checked, will uncheck it. """
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_checked(selector, by=by):
            if self.is_element_visible(selector, by=by):
                self.click(selector, by=by)
            else:
                selector = self.convert_to_css_selector(selector, by=by)
                self.js_click(selector, by=By.CSS_SELECTOR)

    def unselect_if_selected(self, selector, by=By.CSS_SELECTOR):
        """ Same as uncheck_if_checked() """
        self.uncheck_if_checked(selector, by=by)

    def is_element_in_an_iframe(self, selector, by=By.CSS_SELECTOR):
        """ Returns True if the selector's element is located in an iframe.
            Otherwise returns False. """
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_element_present(selector, by=by):
            return False
        soup = self.get_beautiful_soup()
        iframe_list = soup.select('iframe')
        for iframe in iframe_list:
            iframe_identifier = None
            if iframe.has_attr('name') and len(iframe['name']) > 0:
                iframe_identifier = iframe['name']
            elif iframe.has_attr('id') and len(iframe['id']) > 0:
                iframe_identifier = iframe['id']
            elif iframe.has_attr('class') and len(iframe['class']) > 0:
                iframe_class = " ".join(iframe["class"])
                iframe_identifier = '[class="%s"]' % iframe_class
            else:
                continue
            self.switch_to_frame(iframe_identifier)
            if self.is_element_present(selector, by=by):
                self.switch_to_default_content()
                return True
            self.switch_to_default_content()
        return False

    def switch_to_frame_of_element(self, selector, by=By.CSS_SELECTOR):
        """ Set driver control to the iframe containing element (assuming the
            element is in a single-nested iframe) and returns the iframe name.
            If element is not in an iframe, returns None, and nothing happens.
            May not work if multiple iframes are nested within each other. """
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_element_present(selector, by=by):
            return None
        soup = self.get_beautiful_soup()
        iframe_list = soup.select('iframe')
        for iframe in iframe_list:
            iframe_identifier = None
            if iframe.has_attr('name') and len(iframe['name']) > 0:
                iframe_identifier = iframe['name']
            elif iframe.has_attr('id') and len(iframe['id']) > 0:
                iframe_identifier = iframe['id']
            elif iframe.has_attr('class') and len(iframe['class']) > 0:
                iframe_class = " ".join(iframe["class"])
                iframe_identifier = '[class="%s"]' % iframe_class
            else:
                continue
            try:
                self.switch_to_frame(iframe_identifier, timeout=1)
                if self.is_element_present(selector, by=by):
                    return iframe_identifier
            except Exception:
                pass
            self.switch_to_default_content()
        try:
            self.switch_to_frame(selector, timeout=1)
            return selector
        except Exception:
            if self.is_element_present(selector, by=by):
                return ""
            raise Exception("Could not switch to iframe containing "
                            "element {%s}!" % selector)

    def hover_on_element(self, selector, by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        if page_utils.is_xpath_selector(selector):
            selector = self.convert_to_css_selector(selector, By.XPATH)
            by = By.CSS_SELECTOR
        self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        self.__demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        time.sleep(0.05)  # Settle down from scrolling before hovering
        return page_actions.hover_on_element(self.driver, selector)

    def hover_and_click(self, hover_selector, click_selector,
                        hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                        timeout=None):
        """ When you want to hover over an element or dropdown menu,
            and then click an element that appears after that. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        hover_selector, hover_by = self.__recalculate_selector(
            hover_selector, hover_by)
        hover_selector = self.convert_to_css_selector(
            hover_selector, hover_by)
        hover_by = By.CSS_SELECTOR
        click_selector, click_by = self.__recalculate_selector(
            click_selector, click_by)
        dropdown_element = self.wait_for_element_visible(
            hover_selector, by=hover_by, timeout=timeout)
        self.__demo_mode_highlight_if_active(hover_selector, hover_by)
        self.scroll_to(hover_selector, by=hover_by)
        pre_action_url = self.driver.current_url
        outdated_driver = False
        element = None
        try:
            if self.mobile_emulator:
                # On mobile, click to hover the element
                dropdown_element.click()
            elif self.browser == "safari":
                # Use the workaround for hover-clicking on Safari
                raise Exception("This Exception will be caught.")
            else:
                page_actions.hover_element(self.driver, dropdown_element)
        except Exception:
            outdated_driver = True
            element = self.wait_for_element_present(
                click_selector, click_by, timeout)
            if click_by == By.LINK_TEXT:
                self.open(self.__get_href_from_link_text(click_selector))
            elif click_by == By.PARTIAL_LINK_TEXT:
                self.open(self.__get_href_from_partial_link_text(
                    click_selector))
            else:
                self.js_click(click_selector, by=click_by)
        if outdated_driver:
            pass  # Already did the click workaround
        elif self.mobile_emulator:
            self.click(click_selector, by=click_by)
        elif not outdated_driver:
            element = page_actions.hover_and_click(
                self.driver, hover_selector, click_selector,
                hover_by, click_by, timeout)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        return element

    def hover_and_double_click(self, hover_selector, click_selector,
                               hover_by=By.CSS_SELECTOR,
                               click_by=By.CSS_SELECTOR,
                               timeout=None):
        """ When you want to hover over an element or dropdown menu,
            and then double-click an element that appears after that. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        hover_selector, hover_by = self.__recalculate_selector(
            hover_selector, hover_by)
        hover_selector = self.convert_to_css_selector(
            hover_selector, hover_by)
        hover_by = By.CSS_SELECTOR
        click_selector, click_by = self.__recalculate_selector(
            click_selector, click_by)
        dropdown_element = self.wait_for_element_visible(
            hover_selector, by=hover_by, timeout=timeout)
        self.__demo_mode_highlight_if_active(hover_selector, hover_by)
        self.scroll_to(hover_selector, by=hover_by)
        pre_action_url = self.driver.current_url
        outdated_driver = False
        element = None
        try:
            page_actions.hover_element(self.driver, dropdown_element)
        except Exception:
            outdated_driver = True
            element = self.wait_for_element_present(
                click_selector, click_by, timeout)
            if click_by == By.LINK_TEXT:
                self.open(self.__get_href_from_link_text(click_selector))
            elif click_by == By.PARTIAL_LINK_TEXT:
                self.open(self.__get_href_from_partial_link_text(
                    click_selector))
            else:
                self.js_click(click_selector, click_by)
        if not outdated_driver:
            element = page_actions.hover_element_and_double_click(
                self.driver, dropdown_element, click_selector,
                click_by=By.CSS_SELECTOR, timeout=timeout)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        return element

    def drag_and_drop(self, drag_selector, drop_selector,
                      drag_by=By.CSS_SELECTOR, drop_by=By.CSS_SELECTOR,
                      timeout=None):
        """ Drag and drop an element from one selector to another. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        drag_selector, drag_by = self.__recalculate_selector(
            drag_selector, drag_by)
        drop_selector, drop_by = self.__recalculate_selector(
            drop_selector, drop_by)
        drag_element = self.wait_for_element_visible(
            drag_selector, by=drag_by, timeout=timeout)
        self.__demo_mode_highlight_if_active(drag_selector, drag_by)
        self.wait_for_element_visible(
            drop_selector, by=drop_by, timeout=timeout)
        self.__demo_mode_highlight_if_active(drop_selector, drop_by)
        self.scroll_to(drag_selector, by=drag_by)
        drag_selector = self.convert_to_css_selector(
            drag_selector, drag_by)
        drop_selector = self.convert_to_css_selector(
            drop_selector, drop_by)
        drag_and_drop_script = js_utils.get_drag_and_drop_script()
        self.safe_execute_script(
            drag_and_drop_script + (
                "$('%s').simulateDragDrop("
                "{dropTarget: "
                "'%s'});" % (drag_selector, drop_selector)))
        if self.demo_mode:
            self.__demo_mode_pause_if_active()
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        return drag_element

    def __select_option(self, dropdown_selector, option,
                        dropdown_by=By.CSS_SELECTOR, option_by="text",
                        timeout=None):
        """ Selects an HTML <select> option by specification.
            Option specifications are by "text", "index", or "value".
            Defaults to "text" if option_by is unspecified or unknown. """
        from selenium.webdriver.support.ui import Select
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if page_utils.is_xpath_selector(dropdown_selector):
            dropdown_by = By.XPATH
        self.wait_for_ready_state_complete()
        element = self.wait_for_element_present(
            dropdown_selector, by=dropdown_by, timeout=timeout)
        if self.is_element_visible(dropdown_selector, by=dropdown_by):
            self.__demo_mode_highlight_if_active(
                dropdown_selector, dropdown_by)
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
            time.sleep(0.03)
            element = self.wait_for_element_present(
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
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def select_option_by_text(self, dropdown_selector, option,
                              dropdown_by=By.CSS_SELECTOR,
                              timeout=None):
        """ Selects an HTML <select> option by option text.
            @Params
            dropdown_selector - the <select> selector
            option - the text of the option """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__select_option(dropdown_selector, option,
                             dropdown_by=dropdown_by, option_by="text",
                             timeout=timeout)

    def select_option_by_index(self, dropdown_selector, option,
                               dropdown_by=By.CSS_SELECTOR,
                               timeout=None):
        """ Selects an HTML <select> option by option index.
            @Params
            dropdown_selector - the <select> selector
            option - the index number of the option """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__select_option(dropdown_selector, option,
                             dropdown_by=dropdown_by, option_by="index",
                             timeout=timeout)

    def select_option_by_value(self, dropdown_selector, option,
                               dropdown_by=By.CSS_SELECTOR,
                               timeout=None):
        """ Selects an HTML <select> option by option value.
            @Params
            dropdown_selector - the <select> selector
            option - the value property of the option """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__select_option(dropdown_selector, option,
                             dropdown_by=dropdown_by, option_by="value",
                             timeout=timeout)

    def load_html_string(self, html_string, new_page=True):
        """ Loads an HTML string into the web browser.
            If new_page==True, the page will switch to: "data:text/html,"
            If new_page==False, will load HTML into the current page. """

        soup = self.get_beautiful_soup(html_string)
        found_base = False
        links = soup.findAll("link")
        href = None

        for link in links:
            if link.get("rel") == ["canonical"] and link.get("href"):
                found_base = True
                href = link.get("href")
                href = self.get_domain_url(href)
        if found_base and html_string.count("<head>") == 1 and (
                html_string.count("<base") == 0):
            html_string = html_string.replace(
                "<head>", '<head><base href="%s">' % href)
        elif not found_base:
            bases = soup.findAll("base")
            for base in bases:
                if base.get("href"):
                    href = base.get("href")
        if href:
            html_string = html_string.replace(
                'base: "."', 'base: "%s"' % href)

        soup = self.get_beautiful_soup(html_string)
        scripts = soup.findAll("script")
        for script in scripts:
            if script.get("type") != "application/json":
                html_string = html_string.replace(str(script), "")
        soup = self.get_beautiful_soup(html_string)

        found_head = False
        found_body = False
        html_head = None
        html_body = None
        if soup.head and len(str(soup.head)) > 12:
            found_head = True
            html_head = str(soup.head)
            html_head = re.escape(html_head)
            html_head = self.__escape_quotes_if_needed(html_head)
            html_head = html_head.replace('\\ ', ' ')
        if soup.body and len(str(soup.body)) > 12:
            found_body = True
            html_body = str(soup.body)
            html_body = html_body.replace("\xc2\xa0", "&#xA0;")
            html_body = html_body.replace("\xc2\xa1", "&#xA1;")
            html_body = html_body.replace("\xc2\xa9", "&#xA9;")
            html_body = html_body.replace("\xc2\xb7", "&#xB7;")
            html_body = html_body.replace("\xc2\xbf", "&#xBF;")
            html_body = html_body.replace("\xc3\x97", "&#xD7;")
            html_body = html_body.replace("\xc3\xb7", "&#xF7;")
            html_body = re.escape(html_body)
            html_body = self.__escape_quotes_if_needed(html_body)
            html_body = html_body.replace('\\ ', ' ')
        html_string = re.escape(html_string)
        html_string = self.__escape_quotes_if_needed(html_string)
        html_string = html_string.replace('\\ ', ' ')

        if new_page:
            self.open("data:text/html,")
        inner_head = '''document.getElementsByTagName("head")[0].innerHTML'''
        inner_body = '''document.getElementsByTagName("body")[0].innerHTML'''
        if not found_body:
            self.execute_script(
                '''%s = \"%s\"''' % (inner_body, html_string))
        elif found_body and not found_head:
            self.execute_script(
                '''%s = \"%s\"''' % (inner_body, html_body))
        elif found_body and found_head:
            self.execute_script(
                '''%s = \"%s\"''' % (inner_head, html_head))
            self.execute_script(
                '''%s = \"%s\"''' % (inner_body, html_body))
        else:
            raise Exception("Logic Error!")

        for script in scripts:
            js_code = script.string
            js_src = script.get("src")
            if js_code and script.get("type") != "application/json":
                js_code_lines = js_code.split('\n')
                new_lines = []
                for line in js_code_lines:
                    line = line.strip()
                    new_lines.append(line)
                js_code = '\n'.join(new_lines)
                js_utils.add_js_code(self.driver, js_code)
            elif js_src:
                js_utils.add_js_link(self.driver, js_src)
            else:
                pass

    def load_html_file(self, html_file, new_page=True):
        """ Loads a local html file into the browser from a relative file path.
            If new_page==True, the page will switch to: "data:text/html,"
            If new_page==False, will load HTML into the current page.
            Local images and other local src content WILL BE IGNORED. """
        if self.__looks_like_a_page_url(html_file):
            self.open(html_file)
            return
        if len(html_file) < 6 or not html_file.endswith(".html"):
            raise Exception('Expecting a ".html" file!')
        abs_path = os.path.abspath('.')
        file_path = None
        if abs_path in html_file:
            file_path = html_file
        else:
            file_path = abs_path + "/%s" % html_file
        html_string = None
        with open(file_path, 'r') as f:
            html_string = f.read().strip()
        self.load_html_string(html_string, new_page)

    def open_html_file(self, html_file):
        """ Opens a local html file into the browser from a relative file path.
            The URL displayed in the web browser will start with "file://". """
        if self.__looks_like_a_page_url(html_file):
            self.open(html_file)
            return
        if len(html_file) < 6 or not html_file.endswith(".html"):
            raise Exception('Expecting a ".html" file!')
        abs_path = os.path.abspath('.')
        file_path = None
        if abs_path in html_file:
            file_path = html_file
        else:
            file_path = abs_path + "/%s" % html_file
        self.open("file://" + file_path)

    def execute_script(self, script):
        return self.driver.execute_script(script)

    def execute_async_script(self, script, timeout=None):
        if not timeout:
            timeout = settings.EXTREME_TIMEOUT
        return js_utils.execute_async_script(self.driver, script, timeout)

    def safe_execute_script(self, script):
        """ When executing a script that contains a jQuery command,
            it's important that the jQuery library has been loaded first.
            This method will load jQuery if it wasn't already loaded. """
        try:
            return self.execute_script(script)
        except Exception:
            # The likely reason this fails is because: "jQuery is not defined"
            self.activate_jquery()  # It's a good thing we can define it here
            return self.execute_script(script)

    def set_window_rect(self, x, y, width, height):
        self.driver.set_window_rect(x, y, width, height)
        self.__demo_mode_pause_if_active()

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)
        self.__demo_mode_pause_if_active()

    def maximize_window(self):
        self.driver.maximize_window()
        self.__demo_mode_pause_if_active()

    def switch_to_frame(self, frame, timeout=None):
        """
        Wait for an iframe to appear, and switch to it. This should be
        usable as a drop-in replacement for driver.switch_to.frame().
        @Params
        frame - the frame element, name, id, index, or selector
        timeout - the time to wait for the alert in seconds
        """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
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

    def switch_to_window(self, window, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        page_actions.switch_to_window(self.driver, window, timeout)

    def switch_to_default_window(self):
        self.switch_to_window(0)

    def get_new_driver(self, browser=None, headless=None, locale_code=None,
                       servername=None, port=None, proxy=None, agent=None,
                       switch_to=True, cap_file=None, cap_string=None,
                       disable_csp=None, enable_sync=None, use_auto_ext=None,
                       no_sandbox=None, disable_gpu=None,
                       incognito=None, guest_mode=None, devtools=None,
                       swiftshader=None, block_images=None, user_data_dir=None,
                       extension_zip=None, extension_dir=None, is_mobile=False,
                       d_width=None, d_height=None, d_p_r=None):
        """ This method spins up an extra browser for tests that require
            more than one. The first browser is already provided by tests
            that import base_case.BaseCase from seleniumbase. If parameters
            aren't specified, the method uses the same as the default driver.
            @Params
            browser - the browser to use. (Ex: "chrome", "firefox")
            headless - the option to run webdriver in headless mode
            locale_code - the Language Locale Code for the web browser
            servername - if using a Selenium Grid, set the host address here
            port - if using a Selenium Grid, set the host port here
            proxy - if using a proxy server, specify the "host:port" combo here
            switch_to - the option to switch to the new driver (default = True)
            cap_file - the file containing desired capabilities for the browser
            cap_string - the string with desired capabilities for the browser
            disable_csp - an option to disable Chrome's Content Security Policy
            enable_sync - the option to enable the Chrome Sync feature (Chrome)
            use_auto_ext - the option to enable Chrome's Automation Extension
            no_sandbox - the option to enable the "No-Sandbox" feature (Chrome)
            disable_gpu - the option to enable Chrome's "Disable GPU" feature
            incognito - the option to enable Chrome's Incognito mode (Chrome)
            guest - the option to enable Chrome's Guest mode (Chrome)
            devtools - the option to open Chrome's DevTools on start (Chrome)
            swiftshader  the option to use "--use-gl=swiftshader" (Chrome-only)
            block_images - the option to block images from loading (Chrome)
            user_data_dir - Chrome's User Data Directory to use (Chrome-only)
            extension_zip - A Chrome Extension ZIP file to use (Chrome-only)
            extension_dir - A Chrome Extension folder to use (Chrome-only)
            is_mobile - the option to use the mobile emulator (Chrome-only)
            d_width - the device width of the mobile emulator (Chrome-only)
            d_height - the device height of the mobile emulator (Chrome-only)
            d_p_r - the device pixel ratio of the mobile emulator (Chrome-only)
        """
        if self.browser == "remote" and self.servername == "localhost":
            raise Exception('Cannot use "remote" browser driver on localhost!'
                            ' Did you mean to connect to a remote Grid server'
                            ' such as BrowserStack or Sauce Labs? In that'
                            ' case, you must specify the "server" and "port"'
                            ' parameters on the command line! '
                            'Example: '
                            '--server=user:key@hub.browserstack.com --port=80')
        browserstack_ref = (
            'https://browserstack.com/automate/capabilities')
        sauce_labs_ref = (
            'https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/')
        if self.browser == "remote" and not (self.cap_file or self.cap_string):
            raise Exception('Need to specify a desired capabilities file when '
                            'using "--browser=remote". Add "--cap_file=FILE". '
                            'File should be in the Python format used by: '
                            '%s OR '
                            '%s '
                            'See SeleniumBase/examples/sample_cap_file_BS.py '
                            'and SeleniumBase/examples/sample_cap_file_SL.py'
                            % (browserstack_ref, sauce_labs_ref))
        if browser is None:
            browser = self.browser
        browser_name = browser
        if headless is None:
            headless = self.headless
        if locale_code is None:
            locale_code = self.locale_code
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
        user_agent = agent
        if user_agent is None:
            user_agent = self.user_agent
        if disable_csp is None:
            disable_csp = self.disable_csp
        if enable_sync is None:
            enable_sync = self.enable_sync
        if use_auto_ext is None:
            use_auto_ext = self.use_auto_ext
        if no_sandbox is None:
            no_sandbox = self.no_sandbox
        if disable_gpu is None:
            disable_gpu = self.disable_gpu
        if incognito is None:
            incognito = self.incognito
        if guest_mode is None:
            guest_mode = self.guest_mode
        if devtools is None:
            devtools = self.devtools
        if swiftshader is None:
            swiftshader = self.swiftshader
        if block_images is None:
            block_images = self.block_images
        if user_data_dir is None:
            user_data_dir = self.user_data_dir
        if extension_zip is None:
            extension_zip = self.extension_zip
        if extension_dir is None:
            extension_dir = self.extension_dir
        test_id = self.__get_test_id()
        if cap_file is None:
            cap_file = self.cap_file
        if cap_string is None:
            cap_string = self.cap_string
        if is_mobile is None:
            is_mobile = False
        if d_width is None:
            d_width = self.__device_width
        if d_height is None:
            d_height = self.__device_height
        if d_p_r is None:
            d_p_r = self.__device_pixel_ratio
        valid_browsers = constants.ValidBrowsers.valid_browsers
        if browser_name not in valid_browsers:
            raise Exception("Browser: {%s} is not a valid browser option. "
                            "Valid options = {%s}" % (browser, valid_browsers))
        # Launch a web browser
        from seleniumbase.core import browser_launcher
        new_driver = browser_launcher.get_driver(browser_name=browser_name,
                                                 headless=headless,
                                                 locale_code=locale_code,
                                                 use_grid=use_grid,
                                                 servername=servername,
                                                 port=port,
                                                 proxy_string=proxy_string,
                                                 user_agent=user_agent,
                                                 cap_file=cap_file,
                                                 cap_string=cap_string,
                                                 disable_csp=disable_csp,
                                                 enable_sync=enable_sync,
                                                 use_auto_ext=use_auto_ext,
                                                 no_sandbox=no_sandbox,
                                                 disable_gpu=disable_gpu,
                                                 incognito=incognito,
                                                 guest_mode=guest_mode,
                                                 devtools=devtools,
                                                 swiftshader=swiftshader,
                                                 block_images=block_images,
                                                 user_data_dir=user_data_dir,
                                                 extension_zip=extension_zip,
                                                 extension_dir=extension_dir,
                                                 test_id=test_id,
                                                 mobile_emulator=is_mobile,
                                                 device_width=d_width,
                                                 device_height=d_height,
                                                 device_pixel_ratio=d_p_r)
        self._drivers_list.append(new_driver)
        if switch_to:
            self.driver = new_driver
            if self.headless:
                # Make sure the invisible browser window is big enough
                width = settings.HEADLESS_START_WIDTH
                height = settings.HEADLESS_START_HEIGHT
                try:
                    self.driver.set_window_size(width, height)
                    self.wait_for_ready_state_complete()
                except Exception:
                    # This shouldn't fail, but in case it does,
                    # get safely through setUp() so that
                    # WebDrivers can get closed during tearDown().
                    pass
            else:
                if self.browser == 'chrome' or self.browser == 'edge':
                    width = settings.CHROME_START_WIDTH
                    height = settings.CHROME_START_HEIGHT
                    try:
                        if self.maximize_option:
                            self.driver.maximize_window()
                        else:
                            self.driver.set_window_size(width, height)
                        self.wait_for_ready_state_complete()
                    except Exception:
                        pass  # Keep existing browser resolution
                elif self.browser == 'firefox':
                    width = settings.CHROME_START_WIDTH
                    try:
                        if self.maximize_option:
                            self.driver.maximize_window()
                        else:
                            self.driver.set_window_size(width, 720)
                        self.wait_for_ready_state_complete()
                    except Exception:
                        pass  # Keep existing browser resolution
                elif self.browser == 'safari':
                    width = settings.CHROME_START_WIDTH
                    if self.maximize_option:
                        try:
                            self.driver.maximize_window()
                            self.wait_for_ready_state_complete()
                        except Exception:
                            pass  # Keep existing browser resolution
                    else:
                        try:
                            self.driver.set_window_rect(10, 30, width, 630)
                        except Exception:
                            pass
                elif self.browser == 'opera':
                    width = settings.CHROME_START_WIDTH
                    if self.maximize_option:
                        try:
                            self.driver.maximize_window()
                            self.wait_for_ready_state_complete()
                        except Exception:
                            pass  # Keep existing browser resolution
                    else:
                        try:
                            self.driver.set_window_rect(10, 30, width, 700)
                        except Exception:
                            pass
            if self.start_page and len(self.start_page) >= 4:
                if page_utils.is_valid_url(self.start_page):
                    self.open(self.start_page)
                else:
                    new_start_page = "http://" + self.start_page
                    if page_utils.is_valid_url(new_start_page):
                        self.open(new_start_page)
        return new_driver

    def switch_to_driver(self, driver):
        """ Sets self.driver to the specified driver.
            You may need this if using self.get_new_driver() in your code. """
        self.driver = driver

    def switch_to_default_driver(self):
        """ Sets self.driver to the default/original driver. """
        self.driver = self._default_driver

    def save_screenshot(self, name, folder=None):
        """ The screenshot will be in PNG format. """
        return page_actions.save_screenshot(self.driver, name, folder)

    def save_page_source(self, name, folder=None):
        """ Saves the page HTML to the current directory (or given subfolder).
            If the folder specified doesn't exist, it will get created.
            @Params
            name - The file name to save the current page's HTML to.
            folder - The folder to save the file to. (Default = current folder)
        """
        return page_actions.save_page_source(self.driver, name, folder)

    def save_cookies(self, name="cookies.txt"):
        """ Saves the page cookies to the "saved_cookies" folder. """
        cookies = self.driver.get_cookies()
        json_cookies = json.dumps(cookies)
        if name.endswith('/'):
            raise Exception("Invalid filename for Cookies!")
        if '/' in name:
            name = name.split('/')[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = constants.SavedCookies.STORAGE_FOLDER
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        cookies_file_path = "%s/%s" % (file_path, name)
        cookies_file = codecs.open(cookies_file_path, "w+", encoding="utf-8")
        cookies_file.writelines(json_cookies)
        cookies_file.close()

    def load_cookies(self, name="cookies.txt"):
        """ Loads the page cookies from the "saved_cookies" folder. """
        if name.endswith('/'):
            raise Exception("Invalid filename for Cookies!")
        if '/' in name:
            name = name.split('/')[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = constants.SavedCookies.STORAGE_FOLDER
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        cookies_file_path = "%s/%s" % (file_path, name)
        json_cookies = None
        with open(cookies_file_path, 'r') as f:
            json_cookies = f.read().strip()
        cookies = json.loads(json_cookies)
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)

    def delete_all_cookies(self):
        """ Deletes all cookies in the web browser.
            Does NOT delete the saved cookies file. """
        self.driver.delete_all_cookies()

    def delete_saved_cookies(self, name="cookies.txt"):
        """ Deletes the cookies file from the "saved_cookies" folder.
            Does NOT delete the cookies from the web browser. """
        if name.endswith('/'):
            raise Exception("Invalid filename for Cookies!")
        if '/' in name:
            name = name.split('/')[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = constants.SavedCookies.STORAGE_FOLDER
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        cookies_file_path = "%s/%s" % (file_path, name)
        if os.path.exists(cookies_file_path):
            if cookies_file_path.endswith('.txt'):
                os.remove(cookies_file_path)

    def wait_for_ready_state_complete(self, timeout=None):
        try:
            # If there's an alert, skip
            self.driver.switch_to.alert
            return
        except Exception:
            # If there's no alert, continue
            pass
        if not timeout:
            timeout = settings.EXTREME_TIMEOUT
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        is_ready = js_utils.wait_for_ready_state_complete(self.driver, timeout)
        self.wait_for_angularjs(timeout=settings.MINI_TIMEOUT)
        if self.js_checking_on:
            self.assert_no_js_errors()
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

    def wait_for_angularjs(self, timeout=None, **kwargs):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        js_utils.wait_for_angularjs(self.driver, timeout, **kwargs)

    def sleep(self, seconds):
        if not sb_config.time_limit:
            time.sleep(seconds)
        elif seconds <= 0.3:
            shared_utils.check_if_time_limit_exceeded()
            time.sleep(seconds)
            shared_utils.check_if_time_limit_exceeded()
        else:
            start_ms = time.time() * 1000.0
            stop_ms = start_ms + (seconds * 1000.0)
            for x in range(int(seconds * 5)):
                shared_utils.check_if_time_limit_exceeded()
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.2)

    def activate_design_mode(self):
        # Activate Chrome's Design Mode, which lets you edit a site directly.
        # See: https://twitter.com/sulco/status/1177559150563344384
        script = ("""document.designMode = 'on';""")
        self.execute_script(script)

    def deactivate_design_mode(self):
        # Deactivate Chrome's Design Mode.
        script = ("""document.designMode = 'off';""")
        self.execute_script(script)

    def activate_jquery(self):
        """ If "jQuery is not defined", use this method to activate it for use.
            This happens because jQuery is not always defined on web sites. """
        js_utils.activate_jquery(self.driver)
        self.wait_for_ready_state_complete()

    def __are_quotes_escaped(self, string):
        return js_utils.are_quotes_escaped(string)

    def __escape_quotes_if_needed(self, string):
        return js_utils.escape_quotes_if_needed(string)

    def bring_to_front(self, selector, by=By.CSS_SELECTOR):
        """ Updates the Z-index of a page element to bring it into view.
            Useful when getting a WebDriverException, such as the one below:
                { Element is not clickable at point (#, #).
                  Other element would receive the click: ... } """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't run action if can't convert to CSS_Selector for JavaScript
            return
        selector = re.escape(selector)
        selector = self.__escape_quotes_if_needed(selector)
        script = ("""document.querySelector('%s').style.zIndex = '999999';"""
                  % selector)
        self.execute_script(script)

    def highlight_click(self, selector, by=By.CSS_SELECTOR,
                        loops=3, scroll=True):
        if not self.demo_mode:
            self.highlight(selector, by=by, loops=loops, scroll=scroll)
        self.click(selector, by=by)

    def highlight_update_text(self, selector, text, by=By.CSS_SELECTOR,
                              loops=3, scroll=True):
        if not self.demo_mode:
            self.highlight(selector, by=by, loops=loops, scroll=scroll)
        self.update_text(selector, text, by=by)

    def highlight(self, selector, by=By.CSS_SELECTOR,
                  loops=None, scroll=True):
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
        element = self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if not loops:
            loops = settings.HIGHLIGHTS
        if scroll:
            try:
                if self.browser != "safari":
                    scroll_distance = js_utils.get_scroll_distance_to_element(
                        self.driver, element)
                    if abs(scroll_distance) > SSMD:
                        self.__jquery_slow_scroll_to(selector, by)
                    else:
                        self.__slow_scroll_to_element(element)
                else:
                    self.__jquery_slow_scroll_to(selector, by)
            except (StaleElementReferenceException, ENI_Exception, JS_Exc):
                self.wait_for_ready_state_complete()
                time.sleep(0.03)
                element = self.wait_for_element_visible(
                    selector, by=by, timeout=settings.SMALL_TIMEOUT)
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
        try:
            style = element.get_attribute('style')
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.03)
            element = self.wait_for_element_visible(
                selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)
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
        js_utils.highlight_with_js(self.driver, selector, loops, o_bs)

    def __highlight_with_jquery(self, selector, loops, o_bs):
        js_utils.highlight_with_jquery(self.driver, selector, loops, o_bs)

    def press_up_arrow(self, selector="html", times=1, by=By.CSS_SELECTOR):
        """ Simulates pressing the UP Arrow on the keyboard.
            By default, "html" will be used as the CSS Selector target.
            You can specify how many times in-a-row the action happens. """
        if times < 1:
            return
        element = self.wait_for_element_present(selector)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        for i in range(int(times)):
            try:
                element.send_keys(Keys.ARROW_UP)
            except Exception:
                self.wait_for_ready_state_complete()
                element = self.wait_for_element_visible(selector)
                element.send_keys(Keys.ARROW_UP)
            time.sleep(0.01)
            if self.slow_mode:
                time.sleep(0.1)

    def press_down_arrow(self, selector="html", times=1, by=By.CSS_SELECTOR):
        """ Simulates pressing the DOWN Arrow on the keyboard.
            By default, "html" will be used as the CSS Selector target.
            You can specify how many times in-a-row the action happens. """
        if times < 1:
            return
        element = self.wait_for_element_present(selector)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        for i in range(int(times)):
            try:
                element.send_keys(Keys.ARROW_DOWN)
            except Exception:
                self.wait_for_ready_state_complete()
                element = self.wait_for_element_visible(selector)
                element.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.01)
            if self.slow_mode:
                time.sleep(0.1)

    def press_left_arrow(self, selector="html", times=1, by=By.CSS_SELECTOR):
        """ Simulates pressing the LEFT Arrow on the keyboard.
            By default, "html" will be used as the CSS Selector target.
            You can specify how many times in-a-row the action happens. """
        if times < 1:
            return
        element = self.wait_for_element_present(selector)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        for i in range(int(times)):
            try:
                element.send_keys(Keys.ARROW_LEFT)
            except Exception:
                self.wait_for_ready_state_complete()
                element = self.wait_for_element_visible(selector)
                element.send_keys(Keys.ARROW_LEFT)
            time.sleep(0.01)
            if self.slow_mode:
                time.sleep(0.1)

    def press_right_arrow(self, selector="html", times=1, by=By.CSS_SELECTOR):
        """ Simulates pressing the RIGHT Arrow on the keyboard.
            By default, "html" will be used as the CSS Selector target.
            You can specify how many times in-a-row the action happens. """
        if times < 1:
            return
        element = self.wait_for_element_present(selector)
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        for i in range(int(times)):
            try:
                element.send_keys(Keys.ARROW_RIGHT)
            except Exception:
                self.wait_for_ready_state_complete()
                element = self.wait_for_element_visible(selector)
                element.send_keys(Keys.ARROW_RIGHT)
            time.sleep(0.01)
            if self.slow_mode:
                time.sleep(0.1)

    def scroll_to(self, selector, by=By.CSS_SELECTOR, timeout=None):
        ''' Fast scroll to destination '''
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if self.demo_mode or self.slow_mode:
            self.slow_scroll_to(selector, by=by, timeout=timeout)
            return
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        try:
            self.__scroll_to_element(element, selector, by)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.03)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            self.__scroll_to_element(element, selector, by)

    def slow_scroll_to(self, selector, by=By.CSS_SELECTOR, timeout=None):
        ''' Slow motion scroll to destination '''
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        try:
            scroll_distance = js_utils.get_scroll_distance_to_element(
                self.driver, element)
            if abs(scroll_distance) > SSMD:
                self.__jquery_slow_scroll_to(selector, by)
            else:
                self.__slow_scroll_to_element(element)
        except (StaleElementReferenceException, ENI_Exception, JS_Exc):
            self.wait_for_ready_state_complete()
            time.sleep(0.03)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            self.__slow_scroll_to_element(element)

    def scroll_to_top(self):
        """ Scroll to the top of the page. """
        scroll_script = "window.scrollTo(0, 0);"
        try:
            self.execute_script(scroll_script)
            time.sleep(0.012)
            return True
        except Exception:
            return False

    def scroll_to_bottom(self):
        """ Scroll to the bottom of the page. """
        scroll_script = "window.scrollTo(0, 10000);"
        try:
            self.execute_script(scroll_script)
            time.sleep(0.012)
            return True
        except Exception:
            return False

    def click_xpath(self, xpath):
        # Technically self.click() will automatically detect an xpath selector,
        # so self.click_xpath() is just a longer name for the same action.
        self.click(xpath, by=By.XPATH)

    def js_click(self, selector, by=By.CSS_SELECTOR, all_matches=False):
        """ Clicks an element using JavaScript.
            If "all_matches" is False, only the first match is clicked. """
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
            if not self.demo_mode and not self.slow_mode:
                self.__scroll_to_element(element, selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        if not all_matches:
            if ":contains\\(" not in css_selector:
                self.__js_click(selector, by=by)
            else:
                click_script = """jQuery('%s')[0].click();""" % css_selector
                self.safe_execute_script(click_script)
        else:
            if ":contains\\(" not in css_selector:
                self.__js_click_all(selector, by=by)
            else:
                click_script = """jQuery('%s').click();""" % css_selector
                self.safe_execute_script(click_script)
        self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def js_click_all(self, selector, by=By.CSS_SELECTOR):
        """ Clicks all matching elements using pure JS. (No jQuery) """
        self.js_click(selector, by=By.CSS_SELECTOR, all_matches=True)

    def jquery_click(self, selector, by=By.CSS_SELECTOR):
        """ Clicks an element using jQuery. Different from using pure JS. """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        click_script = """jQuery('%s')[0].click();""" % selector
        self.safe_execute_script(click_script)
        self.__demo_mode_pause_if_active()

    def jquery_click_all(self, selector, by=By.CSS_SELECTOR):
        """ Clicks all matching elements using jQuery. """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        click_script = """jQuery('%s').click();""" % css_selector
        self.safe_execute_script(click_script)
        self.__demo_mode_pause_if_active()

    def hide_element(self, selector, by=By.CSS_SELECTOR):
        """ Hide the first element on the page that matches the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        hide_script = """jQuery('%s').hide();""" % selector
        self.safe_execute_script(hide_script)

    def hide_elements(self, selector, by=By.CSS_SELECTOR):
        """ Hide all elements on the page that match the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        hide_script = """jQuery('%s').hide();""" % selector
        self.safe_execute_script(hide_script)

    def show_element(self, selector, by=By.CSS_SELECTOR):
        """ Show the first element on the page that matches the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        show_script = """jQuery('%s').show(0);""" % selector
        self.safe_execute_script(show_script)

    def show_elements(self, selector, by=By.CSS_SELECTOR):
        """ Show all elements on the page that match the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        show_script = """jQuery('%s').show(0);""" % selector
        self.safe_execute_script(show_script)

    def remove_element(self, selector, by=By.CSS_SELECTOR):
        """ Remove the first element on the page that matches the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        remove_script = """jQuery('%s').remove();""" % selector
        self.safe_execute_script(remove_script)

    def remove_elements(self, selector, by=By.CSS_SELECTOR):
        """ Remove all elements on the page that match the selector. """
        selector, by = self.__recalculate_selector(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        remove_script = """jQuery('%s').remove();""" % selector
        self.safe_execute_script(remove_script)

    def ad_block(self):
        """ Block ads that appear on the current web page. """
        from seleniumbase.config import ad_block_list
        for css_selector in ad_block_list.AD_BLOCK_LIST:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
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

    def get_domain_url(self, url):
        return page_utils.get_domain_url(url)

    def get_beautiful_soup(self, source=None):
        """ BeautifulSoup is a toolkit for dissecting an HTML document
            and extracting what you need. It's great for screen-scraping! """
        from bs4 import BeautifulSoup
        if not source:
            self.wait_for_ready_state_complete()
            source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        return soup

    def get_unique_links(self):
        """ Get all unique links in the html of the page source.
            Page links include those obtained from:
            "a"->"href", "img"->"src", "link"->"href", and "script"->"src". """
        page_url = self.get_current_url()
        soup = self.get_beautiful_soup(self.get_page_source())
        links = page_utils._get_unique_links(page_url, soup)
        return links

    def get_link_status_code(self, link, allow_redirects=False, timeout=5):
        """ Get the status code of a link.
            If the timeout is exceeded, will return a 404.
            For a list of available status codes, see:
            https://en.wikipedia.org/wiki/List_of_HTTP_status_codes """
        status_code = page_utils._get_link_status_code(
            link, allow_redirects=allow_redirects, timeout=timeout)
        return status_code

    def assert_link_status_code_is_not_404(self, link):
        status_code = str(self.get_link_status_code(link))
        bad_link_str = 'Error: "%s" returned a 404!' % link
        self.assertNotEqual(status_code, "404", bad_link_str)

    def assert_no_404_errors(self, multithreaded=True):
        """ Assert no 404 errors from page links obtained from:
            "a"->"href", "img"->"src", "link"->"href", and "script"->"src". """
        all_links = self.get_unique_links()
        links = []
        for link in all_links:
            if "javascript:" not in link and "mailto:" not in link:
                links.append(link)
        if multithreaded:
            from multiprocessing.dummy import Pool as ThreadPool
            pool = ThreadPool(10)
            pool.map(self.assert_link_status_code_is_not_404, links)
            pool.close()
            pool.join()
        else:
            for link in links:
                self.assert_link_status_code_is_not_404(link)
        if self.demo_mode:
            a_t = "ASSERT NO 404 ERRORS"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD
                a_t = SD.translate_assert_no_404_errors(self._language)
            messenger_post = ("%s" % a_t)
            self.__highlight_with_assert_success(messenger_post, "html")

    def print_unique_links_with_status_codes(self):
        """ Finds all unique links in the html of the page source
            and then prints out those links with their status codes.
            Format:  ["link"  ->  "status_code"]  (per line)
            Page links include those obtained from:
            "a"->"href", "img"->"src", "link"->"href", and "script"->"src". """
        page_url = self.get_current_url()
        soup = self.get_beautiful_soup(self.get_page_source())
        page_utils._print_unique_links_with_status_codes(page_url, soup)

    def __fix_unicode_conversion(self, text):
        """ Fixing Chinese characters when converting from PDF to HTML. """
        if sys.version_info[0] < 3:
            # Update encoding for Python 2 users
            reload(sys)  # noqa
            sys.setdefaultencoding('utf8')
        text = text.replace(u'\u2f8f', u'\u884c')
        text = text.replace(u'\u2f45', u'\u65b9')
        text = text.replace(u'\u2f08', u'\u4eba')
        text = text.replace(u'\u2f70', u'\u793a')
        return text

    def get_pdf_text(self, pdf, page=None, maxpages=None,
                     password=None, codec='utf-8', wrap=False, nav=False,
                     override=False):
        """ Gets text from a PDF file.
            PDF can be either a URL or a file path on the local file system.
            @Params
            pdf - The URL or file path of the PDF file.
            page - The page number (or a list of page numbers) of the PDF.
                    If a page number is provided, looks only at that page.
                        (1 is the first page, 2 is the second page, etc.)
                    If no page number is provided, returns all PDF text.
            maxpages - Instead of providing a page number, you can provide
                       the number of pages to use from the beginning.
            password - If the PDF is password-protected, enter it here.
            codec - The compression format for character encoding.
                    (The default codec used by this method is 'utf-8'.)
            wrap - Replaces ' \n' with ' ' so that individual sentences
                   from a PDF don't get broken up into seperate lines when
                   getting converted into text format.
            nav - If PDF is a URL, navigates to the URL in the browser first.
                  (Not needed because the PDF will be downloaded anyway.)
            override - If the PDF file to be downloaded already exists in the
                       downloaded_files/ folder, that PDF will be used
                       instead of downloading it again. """
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            from pdfminer.high_level import extract_text
        if not password:
            password = ''
        if not maxpages:
            maxpages = 0
        if not pdf.lower().endswith('.pdf'):
            raise Exception("%s is not a PDF file! (Expecting a .pdf)" % pdf)
        file_path = None
        if page_utils.is_valid_url(pdf):
            if nav:
                if self.get_current_url() != pdf:
                    self.open(pdf)
            file_name = pdf.split('/')[-1]
            file_path = self.get_downloads_folder() + '/' + file_name
            if not os.path.exists(file_path):
                self.download_file(pdf)
            elif override:
                self.download_file(pdf)
        else:
            if not os.path.exists(pdf):
                raise Exception("%s is not a valid URL or file path!" % pdf)
            file_path = os.path.abspath(pdf)
        page_search = None  # (Pages are delimited by '\x0c')
        if type(page) is list:
            pages = page
            page_search = []
            for page in pages:
                page_search.append(page - 1)
        elif type(page) is int:
            page = page - 1
            if page < 0:
                page = 0
            page_search = [page]
        else:
            page_search = None
        pdf_text = extract_text(
            file_path, password='', page_numbers=page_search,
            maxpages=maxpages, caching=False, codec=codec)
        pdf_text = self.__fix_unicode_conversion(pdf_text)
        if wrap:
            pdf_text = pdf_text.replace(' \n', ' ')
        pdf_text = pdf_text.strip()  # Remove leading and trailing whitespace
        return pdf_text

    def assert_pdf_text(self, pdf, text, page=None, maxpages=None,
                        password=None, codec='utf-8', wrap=True, nav=False,
                        override=False):
        """ Asserts text in a PDF file.
            PDF can be either a URL or a file path on the local file system.
            @Params
            pdf - The URL or file path of the PDF file.
            text - The expected text to verify in the PDF.
            page - The page number of the PDF to use (optional).
                    If a page number is provided, looks only at that page.
                        (1 is the first page, 2 is the second page, etc.)
                    If no page number is provided, looks at all the pages.
            maxpages - Instead of providing a page number, you can provide
                       the number of pages to use from the beginning.
            password - If the PDF is password-protected, enter it here.
            codec - The compression format for character encoding.
                    (The default codec used by this method is 'utf-8'.)
            wrap - Replaces ' \n' with ' ' so that individual sentences
                   from a PDF don't get broken up into seperate lines when
                   getting converted into text format.
            nav - If PDF is a URL, navigates to the URL in the browser first.
                  (Not needed because the PDF will be downloaded anyway.)
            override - If the PDF file to be downloaded already exists in the
                       downloaded_files/ folder, that PDF will be used
                       instead of downloading it again. """
        text = self.__fix_unicode_conversion(text)
        if not codec:
            codec = 'utf-8'
        pdf_text = self.get_pdf_text(
            pdf, page=page, maxpages=maxpages, password=password, codec=codec,
            wrap=wrap, nav=nav, override=override)
        if type(page) is int:
            if text not in pdf_text:
                raise Exception("PDF [%s] is missing expected text [%s] on "
                                "page [%s]!" % (pdf, text, page))
        else:
            if text not in pdf_text:
                raise Exception("PDF [%s] is missing expected text [%s]!"
                                "" % (pdf, text))
        return True

    def create_folder(self, folder):
        """ Creates a folder of the given name if it doesn't already exist. """
        if folder.endswith("/"):
            folder = folder[:-1]
        if len(folder) < 1:
            raise Exception("Minimum folder name length = 1.")
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception:
                pass

    def choose_file(self, selector, file_path, by=By.CSS_SELECTOR,
                    timeout=None):
        """ This method is used to choose a file to upload to a website.
            It works by populating a file-chooser "input" field of type="file".
            A relative file_path will get converted into an absolute file_path.

            Example usage:
                self.choose_file('input[type="file"]', "my_dir/my_file.txt")
        """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        abs_path = os.path.abspath(file_path)
        self.add_text(selector, abs_path, by=by, timeout=timeout)

    def save_element_as_image_file(self, selector, file_name, folder=None):
        """ Take a screenshot of an element and save it as an image file.
            If no folder is specified, will save it to the current folder. """
        element = self.wait_for_element_visible(selector)
        element_png = element.screenshot_as_png
        if len(file_name.split('.')[0]) < 1:
            raise Exception("Error: file_name length must be > 0.")
        if not file_name.endswith(".png"):
            file_name = file_name + ".png"
        image_file_path = None
        if folder:
            if folder.endswith("/"):
                folder = folder[:-1]
            if len(folder) > 0:
                self.create_folder(folder)
                image_file_path = "%s/%s" % (folder, file_name)
        if not image_file_path:
            image_file_path = file_name
        with open(image_file_path, "wb") as file:
            file.write(element_png)

    def download_file(self, file_url, destination_folder=None):
        """ Downloads the file from the url to the destination folder.
            If no destination folder is specified, the default one is used.
            (The default downloads folder = "./downloaded_files") """
        if not destination_folder:
            destination_folder = constants.Files.DOWNLOADS_FOLDER
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
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
        from seleniumbase.core import download_helper
        return download_helper.get_downloads_folder()

    def get_path_of_downloaded_file(self, file):
        """ Returns the OS path of the downloaded file. """
        return os.path.join(self.get_downloads_folder(), file)

    def is_downloaded_file_present(self, file):
        """ Checks if the file exists in the Downloads Folder. """
        return os.path.exists(self.get_path_of_downloaded_file(file))

    def assert_downloaded_file(self, file, timeout=None):
        """ Asserts that the file exists in the Downloads Folder. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout)):
            shared_utils.check_if_time_limit_exceeded()
            try:
                self.assertTrue(
                    os.path.exists(self.get_path_of_downloaded_file(file)),
                    "File [%s] was not found in the downloads folder [%s]!"
                    "" % (file, self.get_downloads_folder()))
                if self.demo_mode:
                    messenger_post = ("ASSERT DOWNLOADED FILE: [%s]" % file)
                    js_utils.post_messenger_success_message(
                        self.driver, messenger_post, self.message_duration)
                return
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(1)
        if not os.path.exists(self.get_path_of_downloaded_file(file)):
            message = (
                "File {%s} was not found in the downloads folder {%s} "
                "after %s seconds! (Or the download didn't complete!)"
                "" % (file, self.get_downloads_folder(), timeout))
            page_actions.timeout_exception("NoSuchFileException", message)
        if self.demo_mode:
            messenger_post = ("ASSERT DOWNLOADED FILE: [%s]" % file)
            js_utils.post_messenger_success_message(
                self.driver, messenger_post, self.message_duration)

    def assert_true(self, expr, msg=None):
        """ Asserts that the expression is True.
            Will raise an exception if the statement if False. """
        self.assertTrue(expr, msg=msg)

    def assert_false(self, expr, msg=None):
        """ Asserts that the expression is False.
            Will raise an exception if the statement if True. """
        self.assertFalse(expr, msg=msg)

    def assert_equal(self, first, second, msg=None):
        """ Asserts that the two values are equal.
            Will raise an exception if the values are not equal. """
        self.assertEqual(first, second, msg=msg)

    def assert_not_equal(self, first, second, msg=None):
        """ Asserts that the two values are not equal.
            Will raise an exception if the values are equal. """
        self.assertNotEqual(first, second, msg=msg)

    def assert_raises(self, *args, **kwargs):
        """ Asserts that the following block of code raises an exception.
            Will raise an exception if the block of code has no exception.
            Usage Example =>
                    # Verify that the expected exception is raised.
                    with self.assert_raises(Exception):
                        raise Exception("Expected Exception!")
        """
        self.assertRaises(*args, **kwargs)

    def assert_title(self, title):
        """ Asserts that the web page title matches the expected title. """
        expected = title
        actual = self.get_page_title()
        self.assertEqual(expected, actual, "Expected page title [%s] "
                         "does not match the actual page title [%s]!"
                         "" % (expected, actual))
        if self.demo_mode:
            a_t = "ASSERT TITLE"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD
                a_t = SD.translate_assert_title(self._language)
            messenger_post = ("%s: {%s}" % (a_t, title))
            self.__highlight_with_assert_success(messenger_post, "html")

    def assert_no_js_errors(self):
        """ Asserts that there are no JavaScript "SEVERE"-level page errors.
            Works ONLY for Chrome (non-headless) and Chrome-based browsers.
            Does NOT work on Firefox, Edge, IE, and some other browsers:
                * See https://github.com/SeleniumHQ/selenium/issues/1161
            Based on the following Stack Overflow solution:
                * https://stackoverflow.com/a/41150512/7058266 """
        time.sleep(0.1)  # May take a moment for errors to appear after loads.
        try:
            browser_logs = self.driver.get_log('browser')
        except (ValueError, WebDriverException):
            # If unable to get browser logs, skip the assert and return.
            return

        messenger_library = "//cdnjs.cloudflare.com/ajax/libs/messenger"
        errors = []
        for entry in browser_logs:
            if entry['level'] == 'SEVERE':
                if messenger_library not in entry['message']:
                    # Add errors if not caused by SeleniumBase dependencies
                    errors.append(entry)
        if len(errors) > 0:
            current_url = self.get_current_url()
            raise Exception(
                "JavaScript errors found on %s => %s" % (current_url, errors))
        if self.demo_mode:
            if (self.browser == 'chrome' or self.browser == 'edge'):
                a_t = "ASSERT NO JS ERRORS"
                if self._language != "English":
                    from seleniumbase.fixtures.words import SD
                    a_t = SD.translate_assert_no_js_errors(self._language)
                messenger_post = ("%s" % a_t)
                self.__highlight_with_assert_success(messenger_post, "html")

    def __activate_html_inspector(self):
        self.wait_for_ready_state_complete()
        time.sleep(0.05)
        js_utils.activate_html_inspector(self.driver)

    def inspect_html(self):
        """ Inspects the Page HTML with HTML-Inspector.
            (https://github.com/philipwalton/html-inspector)
            (https://cdnjs.com/libraries/html-inspector)
            Prints the results and also returns them. """
        self.__activate_html_inspector()
        script = ("""HTMLInspector.inspect();""")
        self.execute_script(script)
        time.sleep(0.1)
        browser_logs = []
        try:
            browser_logs = self.driver.get_log('browser')
        except (ValueError, WebDriverException):
            # If unable to get browser logs, skip the assert and return.
            return("(Unable to Inspect HTML! -> Only works on Chrome!)")
        messenger_library = "//cdnjs.cloudflare.com/ajax/libs/messenger"
        url = self.get_current_url()
        header = '\n* HTML Inspection Results: %s' % url
        results = [header]
        row_count = 0
        for entry in browser_logs:
            message = entry['message']
            if "0:6053 " in message:
                message = message.split("0:6053")[1]
            message = message.replace("\\u003C", "<")
            if message.startswith(' "') and message.count('"') == 2:
                message = message.split('"')[1]
            message = "X - " + message
            if messenger_library not in message:
                if message not in results:
                    results.append(message)
                    row_count += 1
        if row_count > 0:
            results.append('* (See the Console output for details!)')
        else:
            results.append('* (No issues detected!)')
        results = '\n'.join(results)
        print(results)
        return(results)

    def get_google_auth_password(self, totp_key=None):
        """ Returns a time-based one-time password based on the
            Google Authenticator password algorithm. Works with Authy.
            If "totp_key" is not specified, defaults to using the one
            provided in seleniumbase/config/settings.py
            Google Auth passwords expire and change at 30-second intervals.
            If the fetched password expires in the next 1.5 seconds, waits
            for a new one before returning it (may take up to 1.5 seconds).
            See https://pyotp.readthedocs.io/en/latest/ for details. """
        import pyotp
        if not totp_key:
            totp_key = settings.TOTP_KEY

        epoch_interval = time.time() / 30.0
        cycle_lifespan = float(epoch_interval) - int(epoch_interval)
        if float(cycle_lifespan) > 0.95:
            # Password expires in the next 1.5 seconds. Wait for a new one.
            for i in range(30):
                time.sleep(0.05)
                epoch_interval = time.time() / 30.0
                cycle_lifespan = float(epoch_interval) - int(epoch_interval)
                if not float(cycle_lifespan) > 0.95:
                    # The new password cycle has begun
                    break

        totp = pyotp.TOTP(totp_key)
        return str(totp.now())

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

    def set_value(self, selector, text, by=By.CSS_SELECTOR, timeout=None):
        """ This method uses JavaScript to update a text field. """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        orginal_selector = selector
        css_selector = self.convert_to_css_selector(selector, by=by)
        self.__demo_mode_highlight_if_active(orginal_selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.scroll_to(orginal_selector, by=by, timeout=timeout)
        if type(text) is int or type(text) is float:
            text = str(text)
        value = re.escape(text)
        value = self.__escape_quotes_if_needed(value)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        if ":contains\\(" not in css_selector:
            script = (
                """document.querySelector('%s').value='%s';"""
                "" % (css_selector, value))
            self.execute_script(script)
        else:
            script = (
                """jQuery('%s')[0].value='%s';"""
                "" % (css_selector, value))
            self.safe_execute_script(script)
        if text.endswith('\n'):
            element = self.wait_for_element_present(
                orginal_selector, by=by, timeout=timeout)
            element.send_keys(Keys.RETURN)
            if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def js_update_text(self, selector, text, by=By.CSS_SELECTOR,
                       timeout=None):
        """ JavaScript + send_keys are used to update a text field.
            Performs self.set_value() and triggers event listeners.
            If text ends in "\n", set_value() presses RETURN after.
            Works faster than send_keys() alone due to the JS call.
        """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if type(text) is int or type(text) is float:
            text = str(text)
        self.set_value(
            selector, text, by=by, timeout=timeout)
        if not text.endswith('\n'):
            try:
                element = page_actions.wait_for_element_present(
                    self.driver, selector, by, timeout=0.2)
                element.send_keys(" \b")
            except Exception:
                pass

    def js_type(self, selector, text, by=By.CSS_SELECTOR,
                timeout=None):
        """ Same as self.js_update_text()
            JavaScript + send_keys are used to update a text field.
            Performs self.set_value() and triggers event listeners.
            If text ends in "\n", set_value() presses RETURN after.
            Works faster than send_keys() alone due to the JS call.
        """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if type(text) is int or type(text) is float:
            text = str(text)
        self.set_value(
            selector, text, by=by, timeout=timeout)
        if not text.endswith('\n'):
            try:
                element = page_actions.wait_for_element_present(
                    self.driver, selector, by, timeout=0.2)
                element.send_keys(" \b")
            except Exception:
                pass

    def jquery_update_text(self, selector, text, by=By.CSS_SELECTOR,
                           timeout=None):
        """ This method uses jQuery to update a text field.
            If the text string ends with the newline character,
            Selenium finishes the call, which simulates pressing
            {Enter/Return} after the text is entered. """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self.__demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        selector = self.__escape_quotes_if_needed(selector)
        text = re.escape(text)
        text = self.__escape_quotes_if_needed(text)
        update_text_script = """jQuery('%s').val('%s');""" % (
            selector, text)
        self.safe_execute_script(update_text_script)
        if text.endswith('\n'):
            element.send_keys('\n')
        self.__demo_mode_pause_if_active()

    def set_time_limit(self, time_limit):
        if time_limit:
            try:
                sb_config.time_limit = float(time_limit)
            except Exception:
                sb_config.time_limit = None
        else:
            sb_config.time_limit = None
        if sb_config.time_limit and sb_config.time_limit > 0:
            sb_config.time_limit_ms = int(sb_config.time_limit * 1000.0)
            self.time_limit = sb_config.time_limit
        else:
            self.time_limit = None
            sb_config.time_limit = None
            sb_config.time_limit_ms = None

    def skip(self, reason=""):
        """ Mark the test as Skipped. """
        self.skipTest(reason)

    ############

    # Application "Local Storage" controls

    def set_local_storage_item(self, key, value):
        self.execute_script(
            "window.localStorage.setItem('{}', '{}');".format(key, value))

    def get_local_storage_item(self, key):
        return self.execute_script(
            "return window.localStorage.getItem('{}');".format(key))

    def remove_local_storage_item(self, key):
        self.execute_script(
            "window.localStorage.removeItem('{}');".format(key))

    def clear_local_storage(self):
        self.execute_script("window.localStorage.clear();")

    def get_local_storage_keys(self):
        return self.execute_script(
            "var ls = window.localStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys;")

    def get_local_storage_items(self):
        return self.execute_script(
            r"var ls = window.localStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items;")

    # Application "Session Storage" controls

    def set_session_storage_item(self, key, value):
        self.execute_script(
            "window.sessionStorage.setItem('{}', '{}');".format(key, value))

    def get_session_storage_item(self, key):
        return self.execute_script(
            "return window.sessionStorage.getItem('{}');".format(key))

    def remove_session_storage_item(self, key):
        self.execute_script(
            "window.sessionStorage.removeItem('{}');".format(key))

    def clear_session_storage(self):
        self.execute_script("window.sessionStorage.clear();")

    def get_session_storage_keys(self):
        return self.execute_script(
            "var ls = window.sessionStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys;")

    def get_session_storage_items(self):
        return self.execute_script(
            r"var ls = window.sessionStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items;")

    ############

    # Duplicates (Avoids name confusion when migrating from other frameworks.)

    def open_url(self, url):
        """ Same as self.open() """
        self.open(url)

    def visit(self, url):
        """ Same as self.open() """
        self.open(url)

    def visit_url(self, url):
        """ Same as self.open() """
        self.open(url)

    def goto(self, url):
        """ Same as self.open() """
        self.open(url)

    def go_to(self, url):
        """ Same as self.open() """
        self.open(url)

    def reload(self):
        """ Same as self.refresh_page() """
        self.refresh_page()

    def reload_page(self):
        """ Same as self.refresh_page() """
        self.refresh_page()

    def input(self, selector, text, by=By.CSS_SELECTOR,
              timeout=None, retry=False):
        """ Same as self.update_text() """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.update_text(selector, text, by=by, timeout=timeout, retry=retry)

    def write(self, selector, text, by=By.CSS_SELECTOR,
              timeout=None, retry=False):
        """ Same as self.update_text() """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.update_text(selector, text, by=by, timeout=timeout, retry=retry)

    def send_keys(self, selector, text, by=By.CSS_SELECTOR, timeout=None):
        """ Same as self.add_text() """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.add_text(selector, text, by=by, timeout=timeout)

    def click_link(self, link_text, timeout=None):
        """ Same as self.click_link_text() """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.click_link_text(link_text, timeout=timeout)

    def wait_for_element_visible(self, selector, by=By.CSS_SELECTOR,
                                 timeout=None):
        """ Same as self.wait_for_element() """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)

    def wait_for_element_not_present(self, selector, by=By.CSS_SELECTOR,
                                     timeout=None):
        """ Same as self.wait_for_element_absent()
            Waits for an element to no longer appear in the HTML of a page.
            A hidden element still counts as appearing in the page HTML.
            If an element with "hidden" status is acceptable,
            use wait_for_element_not_visible() instead. """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_absent(
            self.driver, selector, by, timeout)

    def assert_element_not_present(self, selector, by=By.CSS_SELECTOR,
                                   timeout=None):
        """ Same as self.assert_element_absent()
            Will raise an exception if the element stays present.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_absent(selector, by=by, timeout=timeout)
        return True

    def assert_no_broken_links(self, multithreaded=True):
        """ Same as self.assert_no_404_errors() """
        self.assert_no_404_errors(multithreaded=multithreaded)

    def wait(self, seconds):
        """ Same as self.sleep() - Some JS frameworks use this method name. """
        self.sleep(seconds)

    def block_ads(self):
        """ Same as self.ad_block() """
        self.ad_block()

    def _print(self, msg):
        """ Same as Python's print() """
        print(msg)

    def start_tour(self, name=None, interval=0):
        self.play_tour(name=name, interval=interval)

    ############

    def add_css_link(self, css_link):
        js_utils.add_css_link(self.driver, css_link)

    def add_js_link(self, js_link):
        js_utils.add_js_link(self.driver, js_link)

    def add_css_style(self, css_style):
        js_utils.add_css_style(self.driver, css_style)

    def add_js_code_from_link(self, js_link):
        js_utils.add_js_code_from_link(self.driver, js_link)

    def add_js_code(self, js_code):
        js_utils.add_js_code(self.driver, js_code)

    def add_meta_tag(self, http_equiv=None, content=None):
        js_utils.add_meta_tag(
            self.driver, http_equiv=http_equiv, content=content)

    ############

    def create_presentation(
            self, name=None, theme="default", transition="default"):
        """ Creates a Reveal-JS presentation that you can add slides to.
            @Params
            name - If creating multiple presentations at the same time,
                   use this to specify the name of the current presentation.
            theme - Set a theme with a unique style for the presentation.
                    Valid themes: "serif" (default), "sky", "white", "black",
                                  "simple", "league", "moon", "night",
                                  "beige", "blood", and "solarized".
            transition - Set a transition between slides.
                         Valid transitions: "none" (default), "slide", "fade",
                                            "zoom", "convex", and "concave".
        """
        if not name:
            name = "default"
        if not theme or theme == "default":
            theme = "serif"
        valid_themes = (["serif", "white", "black", "beige", "simple", "sky",
                         "league", "moon", "night", "blood", "solarized"])
        theme = theme.lower()
        if theme not in valid_themes:
            raise Exception(
                "Theme {%s} not found! Valid themes: %s"
                "" % (theme, valid_themes))
        if not transition or transition == "default":
            transition = "none"
        valid_transitions = (
            ["none", "slide", "fade", "zoom", "convex", "concave"])
        transition = transition.lower()
        if transition not in valid_transitions:
            raise Exception(
                "Transition {%s} not found! Valid transitions: %s"
                "" % (transition, valid_transitions))

        reveal_theme_css = None
        if theme == "serif":
            reveal_theme_css = constants.Reveal.SERIF_MIN_CSS
        elif theme == "sky":
            reveal_theme_css = constants.Reveal.SKY_MIN_CSS
        elif theme == "white":
            reveal_theme_css = constants.Reveal.WHITE_MIN_CSS
        elif theme == "black":
            reveal_theme_css = constants.Reveal.BLACK_MIN_CSS
        elif theme == "simple":
            reveal_theme_css = constants.Reveal.SIMPLE_MIN_CSS
        elif theme == "league":
            reveal_theme_css = constants.Reveal.LEAGUE_MIN_CSS
        elif theme == "moon":
            reveal_theme_css = constants.Reveal.MOON_MIN_CSS
        elif theme == "night":
            reveal_theme_css = constants.Reveal.NIGHT_MIN_CSS
        elif theme == "beige":
            reveal_theme_css = constants.Reveal.BEIGE_MIN_CSS
        elif theme == "blood":
            reveal_theme_css = constants.Reveal.BLOOD_MIN_CSS
        elif theme == "solarized":
            reveal_theme_css = constants.Reveal.SOLARIZED_MIN_CSS
        else:
            # Use the default if unable to determine the theme
            reveal_theme_css = constants.Reveal.SERIF_MIN_CSS

        new_presentation = (
            '<html>\n'
            '<head>\n'
            '<meta charset="utf-8">\n'
            '<link rel="stylesheet" href="%s">\n'
            '<link rel="stylesheet" href="%s">\n'
            '<style>\n'
            'pre{background-color:#fbe8d4;border-radius:8px;}\n'
            'div[flex_div]{height:75vh;margin:0;align-items:center;'
            'justify-content:center;}\n'
            'img[rounded]{border-radius:16px;max-width:82%%;}\n'
            '</style>\n'
            '</head>\n\n'
            '<body>\n'
            '<!-- Generated by SeleniumBase - https://seleniumbase.io -->'
            '<div class="reveal">\n'
            '<div class="slides">\n'
            '' % (constants.Reveal.MIN_CSS, reveal_theme_css))

        self._presentation_slides[name] = []
        self._presentation_slides[name].append(new_presentation)
        self._presentation_transition[name] = transition

    def add_slide(self, content=None, image=None, code=None, iframe=None,
                  content2=None, notes=None, transition=None, name=None):
        """ Allows the user to add slides to a presentation.
            @Params
            content - The HTML content to display on the presentation slide.
            image - Attach an image (from a URL link) to the slide.
            code - Attach code of any programming language to the slide.
                   Language-detection will be used to add syntax formatting.
            iframe - Attach an iFrame (from a URL link) to the slide.
            content2 - HTML content to display after adding an image or code.
            notes - Additional notes to include with the slide.
                    ONLY SEEN if show_notes is set for the presentation.
            transition - Set a transition between slides. (overrides previous)
                         Valid transitions: "none" (default), "slide", "fade",
                                            "zoom", "convex", and "concave".
            name - If creating multiple presentations at the same time,
                   use this to select the presentation to add slides to.
        """

        if not name:
            name = "default"
        if name not in self._presentation_slides:
            # Create a presentation if it doesn't already exist
            self.create_presentation(name=name)
        if not content:
            content = ""
        if not content2:
            content2 = ""
        if not notes:
            notes = ""
        if not transition:
            transition = self._presentation_transition[name]
        elif transition == "default":
            transition = "none"
        valid_transitions = (
            ["none", "slide", "fade", "zoom", "convex", "concave"])
        transition = transition.lower()
        if transition not in valid_transitions:
            raise Exception(
                "Transition {%s} not found! Valid transitions: %s"
                "" % (transition, valid_transitions))
        add_line = ""
        if content.startswith("<"):
            add_line = "\n"
        html = (
            '\n<section data-transition="%s">%s%s' % (
                transition, add_line, content))
        if image:
            html += '\n<div flex_div><img rounded src="%s"></div>' % image
        if code:
            html += '\n<div></div>'
            html += '\n<pre class="prettyprint">\n%s</pre>' % code
        if iframe:
            html += ('\n<div></div>'
                     '\n<iframe src="%s" style="width:92%%;height:550;'
                     'title="iframe content"></iframe>' % iframe)
        add_line = ""
        if content2.startswith("<"):
            add_line = "\n"
        if content2:
            html += '%s%s' % (add_line, content2)
        html += '\n<aside class="notes">%s</aside>' % notes
        html += '\n</section>\n'

        self._presentation_slides[name].append(html)

    def save_presentation(
            self, name=None, filename=None, show_notes=False, interval=0):
        """ Saves a Reveal-JS Presentation to a file for later use.
            @Params
            name - If creating multiple presentations at the same time,
                   use this to select the one you wish to use.
            filename - The name of the HTML file that you wish to
                       save the presentation to. (filename must end in ".html")
            show_notes - When set to True, the Notes feature becomes enabled,
                         which allows presenters to see notes next to slides.
            interval - The delay time between autoplaying slides. (in seconds)
                       If set to 0 (default), autoplay is disabled.
        """

        if not name:
            name = "default"
        if not filename:
            filename = "my_presentation.html"
        if name not in self._presentation_slides:
            raise Exception("Presentation {%s} does not exist!" % name)
        if not filename.endswith('.html'):
            raise Exception('Presentation file must end in ".html"!')
        if not interval:
            interval = 0
        if not type(interval) is int and not type(interval) is float:
            raise Exception('Expecting a numeric value for "interval"!')
        if interval < 0:
            raise Exception('The "interval" cannot be a negative number!')
        interval_ms = float(interval) * 1000.0

        show_notes_str = "false"
        if show_notes:
            show_notes_str = "true"

        the_html = ""
        for slide in self._presentation_slides[name]:
            the_html += slide

        the_html += (
            '\n</div>\n'
            '</div>\n'
            '<script src="%s"></script>\n'
            '<script src="%s"></script>\n'
            '<script>Reveal.initialize('
            '{showNotes: %s, slideNumber: true, '
            'autoSlide: %s,});'
            '</script>\n'
            '</body>\n'
            '</html>\n'
            '' % (constants.Reveal.MIN_JS,
                  constants.PrettifyJS.RUN_PRETTIFY_JS,
                  show_notes_str,
                  interval_ms))

        saved_presentations_folder = constants.Presentations.SAVED_FOLDER
        if saved_presentations_folder.endswith("/"):
            saved_presentations_folder = saved_presentations_folder[:-1]
        if not os.path.exists(saved_presentations_folder):
            try:
                os.makedirs(saved_presentations_folder)
            except Exception:
                pass
        file_path = saved_presentations_folder + "/" + filename
        out_file = codecs.open(file_path, "w+", encoding="utf-8")
        out_file.writelines(the_html)
        out_file.close()
        print('\n>>> [%s] was saved!\n' % file_path)
        return file_path

    def begin_presentation(
            self, name=None, filename=None, show_notes=False, interval=0):
        """ Begin a Reveal-JS Presentation in the web browser.
            @Params
            name - If creating multiple presentations at the same time,
                   use this to select the one you wish to use.
            filename - The name of the HTML file that you wish to
                       save the presentation to. (filename must end in ".html")
            show_notes - When set to True, the Notes feature becomes enabled,
                         which allows presenters to see notes next to slides.
            interval - The delay time between autoplaying slides. (in seconds)
                       If set to 0 (default), autoplay is disabled.
        """
        if self.headless:
            return  # Presentations should not run in headless mode.
        if not name:
            name = "default"
        if not filename:
            filename = "my_presentation.html"
        if name not in self._presentation_slides:
            raise Exception("Presentation {%s} does not exist!" % name)
        if not filename.endswith('.html'):
            raise Exception('Presentation file must end in ".html"!')
        if not interval:
            interval = 0
        if not type(interval) is int and not type(interval) is float:
            raise Exception('Expecting a numeric value for "interval"!')
        if interval < 0:
            raise Exception('The "interval" cannot be a negative number!')

        end_slide = (
            '\n<section data-transition="none">\n'
            '<p class="End_Presentation_Now"> </p>\n</section>\n')
        self._presentation_slides[name].append(end_slide)
        file_path = self.save_presentation(
            name=name, filename=filename,
            show_notes=show_notes, interval=interval)
        self._presentation_slides[name].pop()

        self.open_html_file(file_path)
        presentation_folder = constants.Presentations.SAVED_FOLDER
        try:
            while (len(self.driver.window_handles) > 0 and (
                    presentation_folder in self.get_current_url())):
                time.sleep(0.05)
                if self.is_element_visible(
                        "section.present p.End_Presentation_Now"):
                    break
                time.sleep(0.05)
        except Exception:
            pass

    ############

    def create_pie_chart(
            self, chart_name=None, title=None, subtitle=None,
            data_name=None, unit=None, libs=True):
        """ Creates a JavaScript pie chart using "HighCharts".
            @Params
            chart_name - If creating multiple charts,
                         use this to select which one.
            title - The title displayed for the chart.
            subtitle - The subtitle displayed for the chart.
            data_name - Set the series name. Useful for multi-series charts.
            unit - The description label given to the chart's y-axis values.
            libs - The option to include Chart libraries (JS and CSS files).
                   Should be set to True (default) for the first time creating
                   a chart on a web page. If creating multiple charts on the
                   same web page, you won't need to re-import the libraries
                   when creating additional charts.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "pie"
        self.__create_highchart(
            chart_name=chart_name, title=title, subtitle=subtitle,
            style=style, data_name=data_name, unit=unit, libs=libs)

    def create_bar_chart(
            self, chart_name=None, title=None, subtitle=None,
            data_name=None, unit=None, libs=True):
        """ Creates a JavaScript bar chart using "HighCharts".
            @Params
            chart_name - If creating multiple charts,
                         use this to select which one.
            title - The title displayed for the chart.
            subtitle - The subtitle displayed for the chart.
            data_name - Set the series name. Useful for multi-series charts.
            unit - The description label given to the chart's y-axis values.
            libs - The option to include Chart libraries (JS and CSS files).
                   Should be set to True (default) for the first time creating
                   a chart on a web page. If creating multiple charts on the
                   same web page, you won't need to re-import the libraries
                   when creating additional charts.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "bar"
        self.__create_highchart(
            chart_name=chart_name, title=title, subtitle=subtitle,
            style=style, data_name=data_name, unit=unit, libs=libs)

    def create_column_chart(
            self, chart_name=None, title=None, subtitle=None,
            data_name=None, unit=None, libs=True):
        """ Creates a JavaScript column chart using "HighCharts".
            @Params
            chart_name - If creating multiple charts,
                         use this to select which one.
            title - The title displayed for the chart.
            subtitle - The subtitle displayed for the chart.
            data_name - Set the series name. Useful for multi-series charts.
            unit - The description label given to the chart's y-axis values.
            libs - The option to include Chart libraries (JS and CSS files).
                   Should be set to True (default) for the first time creating
                   a chart on a web page. If creating multiple charts on the
                   same web page, you won't need to re-import the libraries
                   when creating additional charts.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "column"
        self.__create_highchart(
            chart_name=chart_name, title=title, subtitle=subtitle,
            style=style, data_name=data_name, unit=unit, libs=libs)

    def create_line_chart(
            self, chart_name=None, title=None, subtitle=None,
            data_name=None, unit=None, zero=False, libs=True):
        """ Creates a JavaScript line chart using "HighCharts".
            @Params
            chart_name - If creating multiple charts,
                         use this to select which one.
            title - The title displayed for the chart.
            subtitle - The subtitle displayed for the chart.
            data_name - Set the series name. Useful for multi-series charts.
            unit - The description label given to the chart's y-axis values.
            zero - If True, the y-axis always starts at 0. (Default: False).
            libs - The option to include Chart libraries (JS and CSS files).
                   Should be set to True (default) for the first time creating
                   a chart on a web page. If creating multiple charts on the
                   same web page, you won't need to re-import the libraries
                   when creating additional charts.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "line"
        self.__create_highchart(
            chart_name=chart_name, title=title, subtitle=subtitle,
            style=style, data_name=data_name, unit=unit, zero=zero, libs=libs)

    def create_area_chart(
            self, chart_name=None, title=None, subtitle=None,
            data_name=None, unit=None, zero=False, libs=True):
        """ Creates a JavaScript area chart using "HighCharts".
            @Params
            chart_name - If creating multiple charts,
                         use this to select which one.
            title - The title displayed for the chart.
            subtitle - The subtitle displayed for the chart.
            data_name - Set the series name. Useful for multi-series charts.
            unit - The description label given to the chart's y-axis values.
            zero - If True, the y-axis always starts at 0. (Default: False).
            libs - The option to include Chart libraries (JS and CSS files).
                   Should be set to True (default) for the first time creating
                   a chart on a web page. If creating multiple charts on the
                   same web page, you won't need to re-import the libraries
                   when creating additional charts.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "area"
        self.__create_highchart(
            chart_name=chart_name, title=title, subtitle=subtitle,
            style=style, data_name=data_name, unit=unit, zero=zero, libs=libs)

    def __create_highchart(
            self, chart_name=None, title=None, subtitle=None,
            style=None, data_name=None, unit=None, zero=False, libs=True):
        """ Creates a JavaScript chart using the "HighCharts" library. """
        if not chart_name:
            chart_name = "default"
        if not title:
            title = ""
        if not subtitle:
            subtitle = ""
        if not style:
            style = "pie"
        if not data_name:
            data_name = "Series 1"
        if not unit:
            unit = "Values"
        title = title.replace("'", "\\'")
        subtitle = subtitle.replace("'", "\\'")
        unit = unit.replace("'", "\\'")
        self._chart_count += 1
        chart_libs = (
            """
            <script src="%s"></script>
            <script src="%s"></script>
            <script src="%s"></script>
            <script src="%s"></script>
            <script src="%s"></script>
            """ % (
                constants.JQuery.MIN_JS,
                constants.HighCharts.HC_JS,
                constants.HighCharts.EXPORTING_JS,
                constants.HighCharts.EXPORT_DATA_JS,
                constants.HighCharts.ACCESSIBILITY_JS))
        if not libs:
            chart_libs = ""
        chart_css = (
            """
            <style>
            .highcharts-figure, .highcharts-data-table table {
                min-width: 320px;
                max-width: 660px;
                margin: 1em auto;
            }
            .highcharts-data-table table {
                font-family: Verdana, sans-serif;
                border-collapse: collapse;
                border: 1px solid #EBEBEB;
                margin: 10px auto;
                text-align: center;
                width: 100%;
                max-width: 500px;
            }
            .highcharts-data-table caption {
                padding: 1em 0;
                font-size: 1.2em;
                color: #555;
            }
            .highcharts-data-table th {
                font-weight: 600;
                padding: 0.5em;
            }
            .highcharts-data-table td, .highcharts-data-table th,
            .highcharts-data-table caption {
                padding: 0.5em;
            }
            .highcharts-data-table thead tr,
            .highcharts-data-table tr:nth-child(even) {
                background: #f8f8f8;
            }
            .highcharts-data-table tr:hover {
                background: #f1f7ff;
            }
            </style>
            """)
        if not libs:
            chart_css = ""
        chart_description = ""
        chart_figure = (
            """
            <figure class="highcharts-figure">
                <div id="chartcontainer%s"></div>
                <p class="highcharts-description">%s</p>
            </figure>
            """ % (self._chart_count, chart_description))
        min_zero = ""
        if zero:
            min_zero = "min: 0,"
        chart_init_1 = (
            """
            <script>
            // Build the chart
            Highcharts.chart('chartcontainer%s', {
            credits: {
                enabled: false
            },
            title: {
                text: '%s'
            },
            subtitle: {
                text: '%s'
            },
            xAxis: { },
            yAxis: {
                %s
                title: {
                    text: '%s',
                    style: {
                        fontSize: '14px'
                    }
                },
                labels: {
                    useHTML: true,
                    style: {
                        fontSize: '14px'
                    }
                }
            },
            chart: {
                renderTo: 'statusChart',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: '%s'
            },
            """ % (self._chart_count, title, subtitle, min_zero, unit, style))
        #  "{series.name}:"
        point_format = (r'<b>{point.y}</b><br />'
                        r'<b>{point.percentage:.1f}%</b>')
        if style != "pie":
            point_format = (r'<b>{point.y}</b>')
        chart_init_2 = (
            """
            tooltip: {
                enabled: true,
                useHTML: true,
                style: {
                    padding: '6px',
                    fontSize: '14px'
                },
                pointFormat: '%s'
            },
            """ % point_format)
        chart_init_3 = (
            r"""
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false,
                        format: '{point.name}: {point.y:.1f}%'
                    },
                    states: {
                        hover: {
                            enabled: true
                        }
                    },
                    showInLegend: true
                }
            },
            """)
        if style != "pie":
            chart_init_3 = (
                """
                allowPointSelect: true,
                cursor: 'pointer',
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle'
                },
                states: {
                    hover: {
                        enabled: true
                    }
                },
                plotOptions: {
                    series: {
                        showInLegend: true,
                        animation: true,
                        shadow: false,
                        lineWidth: 3,
                        fillOpacity: 0.5,
                        marker: {
                            enabled: true
                        }
                    }
                },
                """)
        chart_init = chart_init_1 + chart_init_2 + chart_init_3
        color_by_point = "true"
        if style != "pie":
            color_by_point = "false"
        series = (
            """
            series: [{
            name: '%s',
            colorByPoint: %s,
            data: [
            """ % (data_name, color_by_point))
        new_chart = chart_libs + chart_css + chart_figure + chart_init + series
        self._chart_data[chart_name] = []
        self._chart_label[chart_name] = []
        self._chart_data[chart_name].append(new_chart)
        self._chart_first_series[chart_name] = True
        self._chart_series_count[chart_name] = 1

    def add_series_to_chart(self, data_name=None, chart_name=None):
        """ Add a new data series to an existing chart.
            This allows charts to have multiple data sets.
            @Params
            data_name - Set the series name. Useful for multi-series charts.
            chart_name - If creating multiple charts,
                         use this to select which one.
        """
        if not chart_name:
            chart_name = "default"
        self._chart_series_count[chart_name] += 1
        if not data_name:
            data_name = "Series %s" % self._chart_series_count[chart_name]
        series = (
            """
            ]
            },
            {
            name: '%s',
            colorByPoint: false,
            data: [
            """ % data_name)
        self._chart_data[chart_name].append(series)
        self._chart_first_series[chart_name] = False

    def add_data_point(self, label, value, color=None, chart_name=None):
        """ Add a data point to a SeleniumBase-generated chart.
            @Params
            label - The label name for the data point.
            value - The numeric value of the data point.
            color - The HTML color of the data point.
                    Can be an RGB color. Eg: "#55ACDC".
                    Can also be a named color. Eg: "Teal".
            chart_name - If creating multiple charts,
                         use this to select which one.
        """
        if not chart_name:
            chart_name = "default"
        if chart_name not in self._chart_data:
            # Create a chart if it doesn't already exist
            self.create_pie_chart(chart_name=chart_name)
        if not value:
            value = 0
        if not type(value) is int and not type(value) is float:
            raise Exception('Expecting a numeric value for "value"!')
        if not color:
            color = ""
        label = label.replace("'", "\\'")
        color = color.replace("'", "\\'")
        data_point = (
            """
            {
            name: '%s',
            y: %s,
            color: '%s'
            },
            """ % (label, value, color))
        self._chart_data[chart_name].append(data_point)
        if self._chart_first_series[chart_name]:
            self._chart_label[chart_name].append(label)

    def save_chart(self, chart_name=None, filename=None):
        """ Saves a SeleniumBase-generated chart to a file for later use.
            @Params
            chart_name - If creating multiple charts at the same time,
                         use this to select the one you wish to use.
            filename - The name of the HTML file that you wish to
                       save the chart to. (filename must end in ".html")
        """
        if not chart_name:
            chart_name = "default"
        if not filename:
            filename = "my_chart.html"
        if chart_name not in self._chart_data:
            raise Exception("Chart {%s} does not exist!" % chart_name)
        if not filename.endswith('.html'):
            raise Exception('Chart file must end in ".html"!')
        the_html = '<meta charset="utf-8">\n'
        for chart_data_point in self._chart_data[chart_name]:
            the_html += chart_data_point
        the_html += (
            """
            ]
                }]
            });
            </script>
            """)
        axis = "xAxis: {\n"
        axis += "                labels: {\n"
        axis += "                    useHTML: true,\n"
        axis += "                    style: {\n"
        axis += "                        fontSize: '14px',\n"
        axis += "                    },\n"
        axis += "                },\n"
        axis += "            categories: ["
        for label in self._chart_label[chart_name]:
            axis += "'%s'," % label
        axis += "], crosshair: false},"
        the_html = the_html.replace("xAxis: { },", axis)
        saved_charts_folder = constants.Charts.SAVED_FOLDER
        if saved_charts_folder.endswith("/"):
            saved_charts_folder = saved_charts_folder[:-1]
        if not os.path.exists(saved_charts_folder):
            try:
                os.makedirs(saved_charts_folder)
            except Exception:
                pass
        file_path = saved_charts_folder + "/" + filename
        out_file = codecs.open(file_path, "w+", encoding="utf-8")
        out_file.writelines(the_html)
        out_file.close()
        print('\n>>> [%s] was saved!' % file_path)
        return file_path

    def display_chart(self, chart_name=None, filename=None, interval=0):
        """ Displays a SeleniumBase-generated chart in the browser window.
            @Params
            chart_name - If creating multiple charts at the same time,
                         use this to select the one you wish to use.
            filename - The name of the HTML file that you wish to
                       save the chart to. (filename must end in ".html")
            interval - The delay time for auto-advancing charts. (in seconds)
                       If set to 0 (default), auto-advancing is disabled.
        """
        if self.headless:
            interval = 1  # Race through chart if running in headless mode
        if not chart_name:
            chart_name = "default"
        if not filename:
            filename = "my_chart.html"
        if not interval:
            interval = 0
        if not type(interval) is int and not type(interval) is float:
            raise Exception('Expecting a numeric value for "interval"!')
        if interval < 0:
            raise Exception('The "interval" cannot be a negative number!')
        if chart_name not in self._chart_data:
            raise Exception("Chart {%s} does not exist!" % chart_name)
        if not filename.endswith('.html'):
            raise Exception('Chart file must end in ".html"!')
        file_path = self.save_chart(chart_name=chart_name, filename=filename)
        self.open_html_file(file_path)
        chart_folder = constants.Charts.SAVED_FOLDER
        if interval == 0:
            try:
                print("\n*** Close the browser window to continue ***")
                # Will also continue if manually navigating to a new page
                while (len(self.driver.window_handles) > 0 and (
                        chart_folder in self.get_current_url())):
                    time.sleep(0.05)
            except Exception:
                pass
        else:
            try:
                start_ms = time.time() * 1000.0
                stop_ms = start_ms + (interval * 1000.0)
                for x in range(int(interval * 10)):
                    now_ms = time.time() * 1000.0
                    if now_ms >= stop_ms:
                        break
                    if len(self.driver.window_handles) == 0:
                        break
                    if chart_folder not in self.get_current_url():
                        break
                    time.sleep(0.1)
            except Exception:
                pass

    def extract_chart(self, chart_name=None):
        """ Extracts the HTML from a SeleniumBase-generated chart.
            @Params
            chart_name - If creating multiple charts at the same time,
                         use this to select the one you wish to use.
        """
        if not chart_name:
            chart_name = "default"
        if chart_name not in self._chart_data:
            raise Exception("Chart {%s} does not exist!" % chart_name)
        the_html = ""
        for chart_data_point in self._chart_data[chart_name]:
            the_html += chart_data_point
        the_html += (
            """
            ]
                }]
            });
            </script>
            """)
        axis = "xAxis: {\n"
        axis += "                labels: {\n"
        axis += "                    useHTML: true,\n"
        axis += "                    style: {\n"
        axis += "                        fontSize: '14px',\n"
        axis += "                    },\n"
        axis += "                },\n"
        axis += "            categories: ["
        for label in self._chart_label[chart_name]:
            axis += "'%s'," % label
        axis += "], crosshair: false},"
        the_html = the_html.replace("xAxis: { },", axis)
        return the_html

    ############

    def create_tour(self, name=None, theme=None):
        """ Creates a tour for a website. By default, the Shepherd JavaScript
            Library is used with the Shepherd "Light" / "Arrows" theme.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            theme - Sets the default theme for the tour.
                    Choose from "light"/"arrows", "dark", "default", "square",
                    and "square-dark". ("arrows" is used if None is selected.)
                    Alternatively, you may use a different JavaScript Library
                    as the theme. Those include "IntroJS", "DriverJS",
                    "Hopscotch", and "Bootstrap".
        """
        if not name:
            name = "default"

        if theme:
            if theme.lower() == "bootstrap":
                self.create_bootstrap_tour(name)
            elif theme.lower() == "hopscotch":
                self.create_hopscotch_tour(name)
            elif theme.lower() == "intro":
                self.create_introjs_tour(name)
            elif theme.lower() == "introjs":
                self.create_introjs_tour(name)
            elif theme.lower() == "driver":
                self.create_driverjs_tour(name)
            elif theme.lower() == "driverjs":
                self.create_driverjs_tour(name)
            elif theme.lower() == "shepherd":
                self.create_shepherd_tour(name, theme="light")
            elif theme.lower() == "light":
                self.create_shepherd_tour(name, theme="light")
            elif theme.lower() == "dark":
                self.create_shepherd_tour(name, theme="dark")
            elif theme.lower() == "arrows":
                self.create_shepherd_tour(name, theme="light")
            elif theme.lower() == "square":
                self.create_shepherd_tour(name, theme="square")
            elif theme.lower() == "square-dark":
                self.create_shepherd_tour(name, theme="square-dark")
            elif theme.lower() == "default":
                self.create_shepherd_tour(name, theme="default")
            else:
                self.create_shepherd_tour(name, theme)
        else:
            self.create_shepherd_tour(name, theme="light")

    def create_shepherd_tour(self, name=None, theme=None):
        """ Creates a Shepherd JS website tour.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            theme - Sets the default theme for the tour.
                    Choose from "light"/"arrows", "dark", "default", "square",
                    and "square-dark". ("light" is used if None is selected.)
        """

        shepherd_theme = "shepherd-theme-arrows"
        if theme:
            if theme.lower() == "default":
                shepherd_theme = "shepherd-theme-default"
            elif theme.lower() == "dark":
                shepherd_theme = "shepherd-theme-dark"
            elif theme.lower() == "light":
                shepherd_theme = "shepherd-theme-arrows"
            elif theme.lower() == "arrows":
                shepherd_theme = "shepherd-theme-arrows"
            elif theme.lower() == "square":
                shepherd_theme = "shepherd-theme-square"
            elif theme.lower() == "square-dark":
                shepherd_theme = "shepherd-theme-square-dark"

        if not name:
            name = "default"

        new_tour = (
            """
            // Shepherd Tour
            var tour = new Shepherd.Tour({
                defaults: {
                    classes: '%s',
                    scrollTo: true
                }
            });
            var allButtons = {
                skip: {
                    text: "Skip",
                    action: tour.cancel,
                    classes: 'shepherd-button-secondary tour-button-left'
                },
                back: {
                    text: "Back",
                    action: tour.back,
                    classes: 'shepherd-button-secondary'
                },
                next: {
                    text: "Next",
                    action: tour.next,
                    classes: 'shepherd-button-primary tour-button-right'
                },
            };
            var firstStepButtons = [allButtons.skip, allButtons.next];
            var midTourButtons = [allButtons.back, allButtons.next];
            """ % shepherd_theme)

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_bootstrap_tour(self, name=None):
        """ Creates a Bootstrap tour for a website.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = (
            """
            // Bootstrap Tour
            var tour = new Tour({
            });
            tour.addSteps([
            """)

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_driverjs_tour(self, name=None):
        """ Creates a DriverJS tour for a website.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = (
            """
            // DriverJS Tour
            var tour = new Driver({
                opacity: 0.24,  // Background opacity (0: no popover / overlay)
                padding: 6,    // Distance of element from around the edges
                allowClose: false, // Whether clicking on overlay should close
                overlayClickNext: false, // Move to next step on overlay click
                doneBtnText: 'Done', // Text that appears on the Done button
                closeBtnText: 'Close', // Text appearing on the Close button
                nextBtnText: 'Next', // Text that appears on the Next button
                prevBtnText: 'Previous', // Text appearing on Previous button
                showButtons: true, // This shows control buttons in the footer
                keyboardControl: true, // (escape to close, arrow keys to move)
                animate: true,   // Animate while changing highlighted element
            });
            tour.defineSteps([
            """)

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_hopscotch_tour(self, name=None):
        """ Creates a Hopscotch tour for a website.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = (
            """
            // Hopscotch Tour
            var tour = {
            id: "hopscotch_tour",
            steps: [
            """)

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_introjs_tour(self, name=None):
        """ Creates an IntroJS tour for a website.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = (
            """
            // IntroJS Tour
            function startIntro(){
            var intro = introJs();
            intro.setOptions({
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
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            title - Additional header text that appears above the message.
            theme - (NON-Bootstrap Tours ONLY) The styling of the tour step.
                    Choose from "light"/"arrows", "dark", "default", "square",
                    and "square-dark". ("arrows" is used if None is selected.)
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("top" is default, except for Hopscotch and DriverJS).
            duration - (Bootstrap Tours ONLY) The amount of time, in seconds,
                       before automatically advancing to the next tour step.
        """
        if not selector:
            selector = "html"
        if page_utils.is_name_selector(selector):
            name = page_utils.get_name_from_selector(selector)
            selector = '[name="%s"]' % name
        if page_utils.is_xpath_selector(selector):
            selector = self.convert_to_css_selector(selector, By.XPATH)
        selector = self.__escape_quotes_if_needed(selector)

        if not name:
            name = "default"
        if name not in self._tour_steps:
            # By default, will create an IntroJS tour if no tours exist
            self.create_tour(name=name, theme="introjs")

        if not title:
            title = ""
        title = self.__escape_quotes_if_needed(title)

        if message:
            message = self.__escape_quotes_if_needed(message)
        else:
            message = ""

        if not alignment or (
                alignment not in ["top", "bottom", "left", "right"]):
            t_name = self._tour_steps[name][0]
            if "Hopscotch" not in t_name and "DriverJS" not in t_name:
                alignment = "top"
            else:
                alignment = "bottom"

        if "Bootstrap" in self._tour_steps[name][0]:
            self.__add_bootstrap_tour_step(
                message, selector=selector, name=name, title=title,
                alignment=alignment, duration=duration)
        elif "DriverJS" in self._tour_steps[name][0]:
            self.__add_driverjs_tour_step(
                message, selector=selector, name=name, title=title,
                alignment=alignment)
        elif "Hopscotch" in self._tour_steps[name][0]:
            self.__add_hopscotch_tour_step(
                message, selector=selector, name=name, title=title,
                alignment=alignment)
        elif "IntroJS" in self._tour_steps[name][0]:
            self.__add_introjs_tour_step(
                message, selector=selector, name=name, title=title,
                alignment=alignment)
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
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
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
        buttons = "firstStepButtons"
        if len(self._tour_steps[name]) > 1:
            buttons = "midTourButtons"

        step = ("""
                tour.addStep('%s', {
                    title: '%s',
                    classes: '%s',
                    text: '%s',
                    attachTo: {element: '%s', on: '%s'},
                    buttons: %s,
                    advanceOn: '.docs-link click'
                });""" % (
                name, title, shepherd_classes, message, selector, alignment,
                buttons))

        self._tour_steps[name].append(step)

    def __add_bootstrap_tour_step(self, message, selector=None, name=None,
                                  title=None, alignment=None, duration=None):
        """ Allows the user to add tour steps for a website.
            @Params
            message - The message to display.
            selector - The CSS Selector of the Element to attach to.
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            title - Additional header text that appears above the message.
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("top" is the default alignment).
            duration - (Bootstrap Tours ONLY) The amount of time, in seconds,
                       before automatically advancing to the next tour step.
        """
        if selector != "html":
            selector = self.__make_css_match_first_element_only(selector)
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

    def __add_driverjs_tour_step(self, message, selector=None, name=None,
                                 title=None, alignment=None):
        """ Allows the user to add tour steps for a website.
            @Params
            message - The message to display.
            selector - The CSS Selector of the Element to attach to.
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            title - Additional header text that appears above the message.
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("top" is the default alignment).
        """
        message = (
            '<font size=\"3\" color=\"#33477B\"><b>' + message + '</b></font>')
        title_row = ""
        if not title:
            title_row = "title: '%s'," % message
            message = ""
        else:
            title_row = "title: '%s'," % title
        align_row = "position: '%s'," % alignment
        ani_row = "animate: true,"
        if not selector or selector == "html" or selector == "body":
            selector = "body"
            ani_row = "animate: false,"
            align_row = "position: '%s'," % "mid-center"
        element_row = "element: '%s'," % selector
        desc_row = "description: '%s'," % message

        step = ("""{
                %s
                %s
                popover: {
                  className: 'popover-class',
                  %s
                  %s
                  %s
                }
                },""" % (element_row, ani_row, title_row, desc_row, align_row))

        self._tour_steps[name].append(step)

    def __add_hopscotch_tour_step(self, message, selector=None, name=None,
                                  title=None, alignment=None):
        """ Allows the user to add tour steps for a website.
            @Params
            message - The message to display.
            selector - The CSS Selector of the Element to attach to.
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            title - Additional header text that appears above the message.
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("bottom" is the default alignment).
        """
        arrow_offset_row = None
        if not selector or selector == "html":
            selector = "head"
            alignment = "bottom"
            arrow_offset_row = "arrowOffset: '200',"
        else:
            arrow_offset_row = ""

        step = ("""{
                target: '%s',
                title: '%s',
                content: '%s',
                %s
                showPrevButton: 'true',
                scrollDuration: '550',
                placement: '%s'},
                """ % (selector, title, message, arrow_offset_row, alignment))

        self._tour_steps[name].append(step)

    def __add_introjs_tour_step(self, message, selector=None, name=None,
                                title=None, alignment=None):
        """ Allows the user to add tour steps for a website.
            @Params
            message - The message to display.
            selector - The CSS Selector of the Element to attach to.
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            title - Additional header text that appears above the message.
            alignment - Choose from "top", "bottom", "left", and "right".
                        ("top" is the default alignment).
        """
        if selector != "html":
            element_row = "element: '%s'," % selector
        else:
            element_row = ""

        if title:
            message = "<center><b>" + title + "</b></center><hr>" + message

        message = '<font size=\"3\" color=\"#33477B\">' + message + '</font>'

        step = ("""{%s
                intro: '%s',
                position: '%s'},
                """ % (element_row, message, alignment))

        self._tour_steps[name].append(step)

    def play_tour(self, name=None, interval=0):
        """ Plays a tour on the current website.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            interval - The delay time between autoplaying tour steps. (Seconds)
                       If set to 0 (default), the tour is fully manual control.
        """
        if self.headless:
            return  # Tours should not run in headless mode.

        if not name:
            name = "default"
        if name not in self._tour_steps:
            raise Exception("Tour {%s} does not exist!" % name)

        if "Bootstrap" in self._tour_steps[name][0]:
            tour_helper.play_bootstrap_tour(
                self.driver, self._tour_steps, self.browser,
                self.message_duration, name=name, interval=interval)
        elif "DriverJS" in self._tour_steps[name][0]:
            tour_helper.play_driverjs_tour(
                self.driver, self._tour_steps, self.browser,
                self.message_duration, name=name, interval=interval)
        elif "Hopscotch" in self._tour_steps[name][0]:
            tour_helper.play_hopscotch_tour(
                self.driver, self._tour_steps, self.browser,
                self.message_duration, name=name, interval=interval)
        elif "IntroJS" in self._tour_steps[name][0]:
            tour_helper.play_introjs_tour(
                self.driver, self._tour_steps, self.browser,
                self.message_duration, name=name, interval=interval)
        else:
            # "Shepherd"
            tour_helper.play_shepherd_tour(
                self.driver, self._tour_steps,
                self.message_duration, name=name, interval=interval)

    def export_tour(self, name=None, filename="my_tour.js", url=None):
        """ Exports a tour as a JS file.
            You can call self.export_tour() anywhere where you would
            normally use self.play_tour() to play a website tour.
            It will include necessary resources as well, such as jQuery.
            You'll be able to copy the tour directly into the Console of
            any web browser to play the tour outside of SeleniumBase runs.
            @Params
            name - If creating multiple tours at the same time,
                   use this to select the tour you wish to add steps to.
            filename - The name of the JavaScript file that you wish to
                       save the tour to.
            url - The URL where the tour starts. If not specified, the URL
                  of the current page will be used. """
        if not url:
            url = self.get_current_url()
        tour_helper.export_tour(
            self._tour_steps, name=name, filename=filename, url=url)

    def activate_jquery_confirm(self):
        """ See https://craftpip.github.io/jquery-confirm/ for usage. """
        js_utils.activate_jquery_confirm(self.driver)
        self.wait_for_ready_state_complete()

    def activate_messenger(self):
        js_utils.activate_messenger(self.driver)
        self.wait_for_ready_state_complete()

    def set_messenger_theme(self, theme="default", location="default",
                            max_messages="default"):
        """ Sets a theme for posting messages.
            Themes: ["flat", "future", "block", "air", "ice"]
            Locations: ["top_left", "top_center", "top_right",
                        "bottom_left", "bottom_center", "bottom_right"]
            max_messages is the limit of concurrent messages to display. """
        if not theme:
            theme = "default"  # "flat"
        if not location:
            location = "default"  # "bottom_right"
        if not max_messages:
            max_messages = "default"  # "8"
        else:
            max_messages = str(max_messages)  # Value must be in string format
        js_utils.set_messenger_theme(
            self.driver, theme=theme,
            location=location, max_messages=max_messages)

    def post_message(self, message, duration=None, pause=True, style="info"):
        """ Post a message on the screen with Messenger.
            Arguments:
                message: The message to display.
                duration: The time until the message vanishes. (Default: 2.55s)
                pause: If True, the program waits until the message completes.
                style: "info", "success", or "error".

            You can also post messages by using =>
                self.execute_script('Messenger().post("My Message")')
        """
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        js_utils.post_message(
            self.driver, message, duration, style=style)
        if pause:
            duration = float(duration) + 0.15
            time.sleep(float(duration))

    def post_message_and_highlight(
            self, message, selector, by=By.CSS_SELECTOR):
        """ Post a message on the screen and highlight an element.
            Arguments:
                message: The message to display.
                selector: The selector of the Element to highlight.
                by: The type of selector to search by. (Default: CSS Selector)
        """
        self.__highlight_with_assert_success(message, selector, by=by)

    def post_success_message(self, message, duration=None, pause=True):
        """ Post a success message on the screen with Messenger.
            Arguments:
                message: The success message to display.
                duration: The time until the message vanishes. (Default: 2.55s)
                pause: If True, the program waits until the message completes.
        """
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        js_utils.post_message(
            self.driver, message, duration, style="success")
        if pause:
            duration = float(duration) + 0.15
            time.sleep(float(duration))

    def post_error_message(self, message, duration=None, pause=True):
        """ Post an error message on the screen with Messenger.
            Arguments:
                message: The error message to display.
                duration: The time until the message vanishes. (Default: 2.55s)
                pause: If True, the program waits until the message completes.
        """
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        js_utils.post_message(
            self.driver, message, duration, style="error")
        if pause:
            duration = float(duration) + 0.15
            time.sleep(float(duration))

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
            self.wait_for_ready_state_complete()
        referral_link = ('''<body>'''
                         '''<a class='analytics referral test' href='%s' '''
                         '''style='font-family: Arial,sans-serif; '''
                         '''font-size: 30px; color: #18a2cd'>'''
                         '''Magic Link Button</a></body>''' % destination_page)
        self.execute_script(
            '''document.body.outerHTML = \"%s\"''' % referral_link)
        self.click(
            "a.analytics.referral.test", timeout=2)  # Clicks generated button
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
                                 timeout=None):
        """ Waits for an element to appear in the HTML of a page.
            The element does not need be visible (it may be hidden). """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)

    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Waits for an element to appear in the HTML of a page.
            The element must be visible (it cannot be hidden). """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)

    def get_element(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Same as wait_for_element_present() - returns the element.
            The element does not need be visible (it may be hidden). """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return self.wait_for_element_present(selector, by=by, timeout=timeout)

    def assert_element_present(self, selector, by=By.CSS_SELECTOR,
                               timeout=None):
        """ Similar to wait_for_element_present(), but returns nothing.
            Waits for an element to appear in the HTML of a page.
            The element does not need be visible (it may be hidden).
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        return True

    def find_element(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Same as wait_for_element_visible() - returns the element """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def assert_element(self, selector, by=By.CSS_SELECTOR, timeout=None):
        """ Similar to wait_for_element_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_visible(selector, by=by, timeout=timeout)

        if self.demo_mode:
            selector, by = self.__recalculate_selector(selector, by)
            a_t = "ASSERT"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD
                a_t = SD.translate_assert(self._language)
            messenger_post = "%s %s: %s" % (a_t, by.upper(), selector)
            self.__highlight_with_assert_success(messenger_post, selector, by)
        return True

    def assert_element_visible(self, selector, by=By.CSS_SELECTOR,
                               timeout=None):
        """ Same as self.assert_element()
            As above, will raise an exception if nothing can be found. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.assert_element(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_text_visible(self, text, selector="html", by=By.CSS_SELECTOR,
                              timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_text_visible(
            self.driver, text, selector, by, timeout)

    def wait_for_exact_text_visible(self, text, selector="html",
                                    by=By.CSS_SELECTOR,
                                    timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_exact_text_visible(
            self.driver, text, selector, by, timeout)

    def wait_for_text(self, text, selector="html", by=By.CSS_SELECTOR,
                      timeout=None):
        """ The shorter version of wait_for_text_visible() """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def find_text(self, text, selector="html", by=By.CSS_SELECTOR,
                  timeout=None):
        """ Same as wait_for_text_visible() - returns the element """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def assert_text_visible(self, text, selector="html", by=By.CSS_SELECTOR,
                            timeout=None):
        """ Same as assert_text() """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.assert_text(text, selector, by=by, timeout=timeout)

    def assert_text(self, text, selector="html", by=By.CSS_SELECTOR,
                    timeout=None):
        """ Similar to wait_for_text_visible()
            Raises an exception if the element or the text is not found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_text_visible(text, selector, by=by, timeout=timeout)

        if self.demo_mode:
            selector, by = self.__recalculate_selector(selector, by)
            a_t = "ASSERT TEXT"
            i_n = "in"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD
                a_t = SD.translate_assert_text(self._language)
                i_n = SD.translate_in(self._language)
            messenger_post = ("%s: {%s} %s %s: %s"
                              % (a_t, text, i_n, by.upper(), selector))
            self.__highlight_with_assert_success(messenger_post, selector, by)
        return True

    def assert_exact_text(self, text, selector="html", by=By.CSS_SELECTOR,
                          timeout=None):
        """ Similar to assert_text(), but the text must be exact, rather than
            exist as a subset of the full text.
            (Extra whitespace at the beginning or the end doesn't count.)
            Raises an exception if the element or the text is not found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_exact_text_visible(
            text, selector, by=by, timeout=timeout)

        if self.demo_mode:
            selector, by = self.__recalculate_selector(selector, by)
            a_t = "ASSERT EXACT TEXT"
            i_n = "in"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD
                a_t = SD.translate_assert_exact_text(self._language)
                i_n = SD.translate_in(self._language)
            messenger_post = ("%s: {%s} %s %s: %s"
                              % (a_t, text, i_n, by.upper(), selector))
            self.__highlight_with_assert_success(messenger_post, selector, by)
        return True

    ############

    def wait_for_link_text_present(self, link_text, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 5)):
            shared_utils.check_if_time_limit_exceeded()
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
        message = (
            "Link text {%s} was not present after %s seconds!"
            "" % (link_text, timeout))
        page_actions.timeout_exception("NoSuchElementException", message)

    def wait_for_partial_link_text_present(self, link_text, timeout=None):
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 5)):
            shared_utils.check_if_time_limit_exceeded()
            try:
                if not self.is_partial_link_text_present(link_text):
                    raise Exception(
                        "Partial Link text {%s} was not found!" % link_text)
                return
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.2)
        message = (
            "Partial Link text {%s} was not present after %s seconds!"
            "" % (link_text, timeout))
        page_actions.timeout_exception("NoSuchElementException", message)

    def wait_for_link_text_visible(self, link_text, timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(
            link_text, by=By.LINK_TEXT, timeout=timeout)

    def wait_for_link_text(self, link_text, timeout=None):
        """ The shorter version of wait_for_link_text_visible() """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def find_link_text(self, link_text, timeout=None):
        """ Same as wait_for_link_text_visible() - returns the element """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def assert_link_text(self, link_text, timeout=None):
        """ Similar to wait_for_link_text_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_link_text_visible(link_text, timeout=timeout)
        if self.demo_mode:
            a_t = "ASSERT LINK TEXT"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD
                a_t = SD.translate_assert_link_text(self._language)
            messenger_post = ("%s: {%s}" % (a_t, link_text))
            self.__highlight_with_assert_success(
                messenger_post, link_text, by=By.LINK_TEXT)
        return True

    def wait_for_partial_link_text(self, partial_link_text, timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(
            partial_link_text, by=By.PARTIAL_LINK_TEXT, timeout=timeout)

    def find_partial_link_text(self, partial_link_text, timeout=None):
        """ Same as wait_for_partial_link_text() - returns the element """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_partial_link_text(
            partial_link_text, timeout=timeout)

    def assert_partial_link_text(self, partial_link_text, timeout=None):
        """ Similar to wait_for_partial_link_text(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_partial_link_text(partial_link_text, timeout=timeout)
        if self.demo_mode:
            a_t = "ASSERT PARTIAL LINK TEXT"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD
                a_t = SD.translate_assert_link_text(self._language)
            messenger_post = ("%s: {%s}" % (a_t, partial_link_text))
            self.__highlight_with_assert_success(
                messenger_post, partial_link_text, by=By.PARTIAL_LINK_TEXT)
        return True

    ############

    def wait_for_element_absent(self, selector, by=By.CSS_SELECTOR,
                                timeout=None):
        """ Waits for an element to no longer appear in the HTML of a page.
            A hidden element still counts as appearing in the page HTML.
            If an element with "hidden" status is acceptable,
            use wait_for_element_not_visible() instead. """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_absent(
            self.driver, selector, by, timeout)

    def assert_element_absent(self, selector, by=By.CSS_SELECTOR,
                              timeout=None):
        """ Similar to wait_for_element_absent() - returns nothing.
            As above, will raise an exception if the element stays present.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_absent(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                     timeout=None):
        """ Waits for an element to no longer be visible on a page.
            The element can be non-existant in the HTML or hidden on the page
            to qualify as not visible. """
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_not_visible(
            self.driver, selector, by, timeout)

    def assert_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                   timeout=None):
        """ Similar to wait_for_element_not_visible() - returns nothing.
            As above, will raise an exception if the element stays visible.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_not_visible(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_text_not_visible(self, text, selector="html",
                                  by=By.CSS_SELECTOR,
                                  timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_text_not_visible(
            self.driver, text, selector, by, timeout)

    def assert_text_not_visible(self, text, selector="html",
                                by=By.CSS_SELECTOR,
                                timeout=None):
        """ Similar to wait_for_text_not_visible()
            Raises an exception if the element or the text is not found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_text_not_visible(text, selector, by=by, timeout=timeout)

    ############

    def wait_for_and_accept_alert(self, timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def wait_for_and_dismiss_alert(self, timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def wait_for_and_switch_to_alert(self, timeout=None):
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)

    ############

    def accept_alert(self, timeout=None):
        """ Same as wait_for_and_accept_alert(), but smaller default T_O """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def dismiss_alert(self, timeout=None):
        """ Same as wait_for_and_dismiss_alert(), but smaller default T_O """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def switch_to_alert(self, timeout=None):
        """ Same as wait_for_and_switch_to_alert(), but smaller default T_O """
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)

    ############

    def __assert_eq(self, *args, **kwargs):
        """ Minified assert_equal() using only the list diff. """
        minified_exception = None
        try:
            self.assertEqual(*args, **kwargs)
        except Exception as e:
            str_e = str(e)
            minified_exception = "\nAssertionError:\n"
            lines = str_e.split('\n')
            countdown = 3
            countdown_on = False
            for line in lines:
                if countdown_on:
                    minified_exception += line + '\n'
                    countdown = countdown - 1
                    if countdown == 0:
                        countdown_on = False
                elif line.startswith('F'):
                    countdown_on = True
                    countdown = 3
                    minified_exception += line + '\n'
                elif line.startswith('+') or line.startswith('-'):
                    minified_exception += line + '\n'
                elif line.startswith('?'):
                    minified_exception += line + '\n'
                elif line.strip().startswith('*'):
                    minified_exception += line + '\n'
        if minified_exception:
            raise Exception(minified_exception)

    def check_window(self, name="default", level=0, baseline=False):
        """ ***  Automated Visual Testing with SeleniumBase  ***

            The first time a test calls self.check_window() for a unique "name"
            parameter provided, it will set a visual baseline, meaning that it
            creates a folder, saves the URL to a file, saves the current window
            screenshot to a file, and creates the following three files
            with the listed data saved:
            tags_level1.txt  ->  HTML tags from the window
            tags_level2.txt  ->  HTML tags + attributes from the window
            tags_level3.txt  ->  HTML tags + attributes/values from the window

            Baseline folders are named based on the test name and the name
            parameter passed to self.check_window(). The same test can store
            multiple baseline folders.

            If the baseline is being set/reset, the "level" doesn't matter.

            After the first run of self.check_window(), it will compare the
            HTML tags of the latest window to the one from the initial run.
            Here's how the level system works:
            * level=0 ->
                DRY RUN ONLY - Will perform a comparison to the baseline, and
                               print out any differences that are found, but
                               won't fail the test even if differences exist.
            * level=1 ->
                HTML tags are compared to tags_level1.txt
            * level=2 ->
                HTML tags are compared to tags_level1.txt and
                HTML tags/attributes are compared to tags_level2.txt
            * level=3 ->
                HTML tags are compared to tags_level1.txt and
                HTML tags + attributes are compared to tags_level2.txt and
                HTML tags + attributes/values are compared to tags_level3.txt
            As shown, Level-3 is the most strict, Level-1 is the least strict.
            If the comparisons from the latest window to the existing baseline
            don't match, the current test will fail, except for Level-0 tests.

            You can reset the visual baseline on the command line by using:
                --visual_baseline
            As long as "--visual_baseline" is used on the command line while
            running tests, the self.check_window() method cannot fail because
            it will rebuild the visual baseline rather than comparing the html
            tags of the latest run to the existing baseline. If there are any
            expected layout changes to a website that you're testing, you'll
            need to reset the baseline to prevent unnecessary failures.

            self.check_window() will fail with "Page Domain Mismatch Failure"
            if the page domain doesn't match the domain of the baseline.

            If you want to use self.check_window() to compare a web page to
            a later version of itself from within the same test run, you can
            add the parameter "baseline=True" to the first time you call
            self.check_window() in a test to use that as the baseline. This
            only makes sense if you're calling self.check_window() more than
            once with the same name parameter in the same test.

            Automated Visual Testing with self.check_window() is not very
            effective for websites that have dynamic content that changes
            the layout and structure of web pages. For those, you're much
            better off using regular SeleniumBase functional testing.

            Example usage:
                self.check_window(name="testing", level=0)
                self.check_window(name="xkcd_home", level=1)
                self.check_window(name="github_page", level=2)
                self.check_window(name="wikipedia_page", level=3)
        """
        if level == "0":
            level = 0
        if level == "1":
            level = 1
        if level == "2":
            level = 2
        if level == "3":
            level = 3
        if level != 0 and level != 1 and level != 2 and level != 3:
            raise Exception('Parameter "level" must be set to 0, 1, 2, or 3!')

        if self.demo_mode:
            raise Exception(
                "WARNING: Using Demo Mode will break layout tests "
                "that use the check_window() method due to custom "
                "HTML edits being made on the page!\n"
                "Please rerun without using Demo Mode!")

        module = self.__class__.__module__
        if '.' in module and len(module.split('.')[-1]) > 1:
            module = module.split('.')[-1]
        test_id = "%s.%s" % (module, self._testMethodName)
        if not name or len(name) < 1:
            name = "default"
        name = str(name)
        from seleniumbase.core import visual_helper
        visual_helper.visual_baseline_folder_setup()
        baseline_dir = constants.VisualBaseline.STORAGE_FOLDER
        visual_baseline_path = baseline_dir + "/" + test_id + "/" + name
        page_url_file = visual_baseline_path + "/page_url.txt"
        screenshot_file = visual_baseline_path + "/screenshot.png"
        level_1_file = visual_baseline_path + "/tags_level_1.txt"
        level_2_file = visual_baseline_path + "/tags_level_2.txt"
        level_3_file = visual_baseline_path + "/tags_level_3.txt"

        set_baseline = False
        if baseline or self.visual_baseline:
            set_baseline = True
        if not os.path.exists(visual_baseline_path):
            set_baseline = True
            try:
                os.makedirs(visual_baseline_path)
            except Exception:
                pass  # Only reachable during multi-threaded test runs
        if not os.path.exists(page_url_file):
            set_baseline = True
        if not os.path.exists(screenshot_file):
            set_baseline = True
        if not os.path.exists(level_1_file):
            set_baseline = True
        if not os.path.exists(level_2_file):
            set_baseline = True
        if not os.path.exists(level_3_file):
            set_baseline = True

        page_url = self.get_current_url()
        soup = self.get_beautiful_soup()
        html_tags = soup.body.find_all()
        level_1 = [[tag.name] for tag in html_tags]
        level_1 = json.loads(json.dumps(level_1))  # Tuples become lists
        level_2 = [[tag.name, sorted(tag.attrs.keys())] for tag in html_tags]
        level_2 = json.loads(json.dumps(level_2))  # Tuples become lists
        level_3 = [[tag.name, sorted(tag.attrs.items())] for tag in html_tags]
        level_3 = json.loads(json.dumps(level_3))  # Tuples become lists

        if set_baseline:
            self.save_screenshot("screenshot.png", visual_baseline_path)
            out_file = codecs.open(page_url_file, "w+", encoding="utf-8")
            out_file.writelines(page_url)
            out_file.close()
            out_file = codecs.open(level_1_file, "w+", encoding="utf-8")
            out_file.writelines(json.dumps(level_1))
            out_file.close()
            out_file = codecs.open(level_2_file, "w+", encoding="utf-8")
            out_file.writelines(json.dumps(level_2))
            out_file.close()
            out_file = codecs.open(level_3_file, "w+", encoding="utf-8")
            out_file.writelines(json.dumps(level_3))
            out_file.close()

        if not set_baseline:
            f = open(page_url_file, 'r')
            page_url_data = f.read().strip()
            f.close()
            f = open(level_1_file, 'r')
            level_1_data = json.loads(f.read())
            f.close()
            f = open(level_2_file, 'r')
            level_2_data = json.loads(f.read())
            f.close()
            f = open(level_3_file, 'r')
            level_3_data = json.loads(f.read())
            f.close()

            domain_fail = (
                "\nPage Domain Mismatch Failure: "
                "Current Page Domain doesn't match the Page Domain of the "
                "Baseline! Can't compare two completely different sites! "
                "Run with --visual_baseline to reset the baseline!")
            level_1_failure = (
                "\n*\n*** Exception: <Level 1> Visual Diff Failure:\n"
                "* HTML tags don't match the baseline!")
            level_2_failure = (
                "\n*\n*** Exception: <Level 2> Visual Diff Failure:\n"
                "* HTML tag attribute names don't match the baseline!")
            level_3_failure = (
                "\n*\n*** Exception: <Level 3> Visual Diff Failure:\n"
                "* HTML tag attribute values don't match the baseline!")

            page_domain = self.get_domain_url(page_url)
            page_data_domain = self.get_domain_url(page_url_data)
            unittest.TestCase.maxDiff = 1000
            if level != 0:
                self.assertEqual(page_data_domain, page_domain, domain_fail)
            unittest.TestCase.maxDiff = None
            if level == 3:
                self.__assert_eq(level_3_data, level_3, level_3_failure)
            if level == 2:
                self.__assert_eq(level_2_data, level_2, level_2_failure)
            unittest.TestCase.maxDiff = 1000
            if level == 1:
                self.__assert_eq(level_1_data, level_1, level_1_failure)
            unittest.TestCase.maxDiff = None
            if level == 0:
                try:
                    unittest.TestCase.maxDiff = 1000
                    self.assertEqual(
                        page_domain, page_data_domain, domain_fail)
                    unittest.TestCase.maxDiff = None
                    self.__assert_eq(level_3_data, level_3, level_3_failure)
                except Exception as e:
                    print(e)  # Level-0 Dry Run (Only print the differences)

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
            exc_message = sys.exc_info()
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

    def __add_deferred_assert_failure(self):
        """ Add a deferred_assert failure to a list for future processing. """
        current_url = self.driver.current_url
        message = self.__get_exception_message()
        self.__deferred_assert_failures.append(
            "CHECK #%s: (%s)\n %s" % (
                self.__deferred_assert_count, current_url, message))

    ############

    def deferred_assert_element(self, selector, by=By.CSS_SELECTOR,
                                timeout=None):
        """ A non-terminating assertion for an element on a page.
            Failures will be saved until the process_deferred_asserts()
            method is called from inside a test, likely at the end of it. """
        if not timeout:
            timeout = settings.MINI_TIMEOUT
        if self.timeout_multiplier and timeout == settings.MINI_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__deferred_assert_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_deferred_assert:
                timeout = 1
            else:
                self.__last_url_of_deferred_assert = url
        except Exception:
            pass
        try:
            self.wait_for_element_visible(selector, by=by, timeout=timeout)
            return True
        except Exception:
            self.__add_deferred_assert_failure()
            return False

    def deferred_assert_text(self, text, selector="html", by=By.CSS_SELECTOR,
                             timeout=None):
        """ A non-terminating assertion for text from an element on a page.
            Failures will be saved until the process_deferred_asserts()
            method is called from inside a test, likely at the end of it. """
        if not timeout:
            timeout = settings.MINI_TIMEOUT
        if self.timeout_multiplier and timeout == settings.MINI_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__deferred_assert_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_deferred_assert:
                timeout = 1
            else:
                self.__last_url_of_deferred_assert = url
        except Exception:
            pass
        try:
            self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
            return True
        except Exception:
            self.__add_deferred_assert_failure()
            return False

    def process_deferred_asserts(self, print_only=False):
        """ To be used with any test that uses deferred_asserts, which are
            non-terminating verifications that only raise exceptions
            after this method is called.
            This is useful for pages with multiple elements to be checked when
            you want to find as many bugs as possible in a single test run
            before having all the exceptions get raised simultaneously.
            Might be more useful if this method is called after processing all
            the deferred asserts on a single html page so that the failure
            screenshot matches the location of the deferred asserts.
            If "print_only" is set to True, the exception won't get raised. """
        if self.__deferred_assert_failures:
            exception_output = ''
            exception_output += "\n*** DEFERRED ASSERTION FAILURES FROM: "
            exception_output += "%s\n" % self.id()
            all_failing_checks = self.__deferred_assert_failures
            self.__deferred_assert_failures = []
            for tb in all_failing_checks:
                exception_output += "%s\n" % tb
            if print_only:
                print(exception_output)
            else:
                raise Exception(exception_output)

    ############

    # Alternate naming scheme for the "deferred_assert" methods.

    def delayed_assert_element(self, selector, by=By.CSS_SELECTOR,
                               timeout=None):
        """ Same as self.deferred_assert_element() """
        return self.deferred_assert_element(
            selector=selector, by=by, timeout=timeout)

    def delayed_assert_text(self, text, selector="html", by=By.CSS_SELECTOR,
                            timeout=None):
        """ Same as self.deferred_assert_text() """
        return self.deferred_assert_text(
            text=text, selector=selector, by=by, timeout=timeout)

    def process_delayed_asserts(self, print_only=False):
        """ Same as self.process_deferred_asserts() """
        self.process_deferred_asserts(print_only=print_only)

    ############

    def __js_click(self, selector, by=By.CSS_SELECTOR):
        """ Clicks an element using pure JS. Does not use jQuery. """
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
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

    def __js_click_all(self, selector, by=By.CSS_SELECTOR):
        """ Clicks all matching elements using pure JS. (No jQuery) """
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = ("""var simulateClick = function (elem) {
                         var evt = new MouseEvent('click', {
                             bubbles: true,
                             cancelable: true,
                             view: window
                         });
                         var canceled = !elem.dispatchEvent(evt);
                     };
                     var $elements = document.querySelectorAll('%s');
                     var index = 0, length = $elements.length;
                     for(; index < length; index++){
                     simulateClick($elements[index]);}"""
                  % css_selector)
        self.execute_script(script)

    def __jquery_slow_scroll_to(self, selector, by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        dist = js_utils.get_scroll_distance_to_element(self.driver, element)
        time_offset = 0
        try:
            if dist and abs(dist) > SSMD:
                time_offset = int(float(abs(dist) - SSMD) / 12.5)
                if time_offset > 950:
                    time_offset = 950
        except Exception:
            time_offset = 0
        scroll_time_ms = 550 + time_offset
        sleep_time = 0.625 + (float(time_offset) / 1000.0)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        scroll_script = (
            """jQuery([document.documentElement, document.body]).animate({
            scrollTop: jQuery('%s').offset().top - 130}, %s);
            """ % (selector, scroll_time_ms))
        self.safe_execute_script(scroll_script)
        self.sleep(sleep_time)

    def __jquery_click(self, selector, by=By.CSS_SELECTOR):
        """ Clicks an element using jQuery. Different from using pure JS. """
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        click_script = """jQuery('%s')[0].click();""" % selector
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
        soup = self.get_beautiful_soup()
        drop_down_list = []
        for item in soup.select('li[class]'):
            drop_down_list.append(item)
        csstype = link_css.split('[')[1].split('=')[0]
        for item in drop_down_list:
            item_text_list = item.text.split('\n')
            if link_text in item_text_list and csstype in item.decode():
                dropdown_css = ""
                try:
                    for css_class in item['class']:
                        dropdown_css += '.'
                        dropdown_css += css_class
                except Exception:
                    continue
                dropdown_css = item.name + dropdown_css
                matching_dropdowns = self.find_visible_elements(dropdown_css)
                for dropdown in matching_dropdowns:
                    # The same class names might be used for multiple dropdowns
                    if dropdown.is_displayed():
                        try:
                            try:
                                page_actions.hover_element(
                                    self.driver, dropdown)
                            except Exception:
                                # If hovering fails, driver is likely outdated
                                # Time to go directly to the hidden link text
                                self.open(self.__get_href_from_link_text(
                                    link_text))
                                return True
                            page_actions.hover_element_and_click(
                                self.driver, dropdown, link_text,
                                click_by=By.LINK_TEXT, timeout=0.12)
                            return True
                        except Exception:
                            pass

        return False

    def __get_href_from_partial_link_text(self, link_text, hard_fail=True):
        href = self.get_partial_link_text_attribute(
            link_text, "href", hard_fail)
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

    def __click_dropdown_partial_link_text(self, link_text, link_css):
        """ When a partial link may be hidden under a dropdown, use this. """
        soup = self.get_beautiful_soup()
        drop_down_list = []
        for item in soup.select('li[class]'):
            drop_down_list.append(item)
        csstype = link_css.split('[')[1].split('=')[0]
        for item in drop_down_list:
            item_text_list = item.text.split('\n')
            if link_text in item_text_list and csstype in item.decode():
                dropdown_css = ""
                try:
                    for css_class in item['class']:
                        dropdown_css += '.'
                        dropdown_css += css_class
                except Exception:
                    continue
                dropdown_css = item.name + dropdown_css
                matching_dropdowns = self.find_visible_elements(dropdown_css)
                for dropdown in matching_dropdowns:
                    # The same class names might be used for multiple dropdowns
                    if dropdown.is_displayed():
                        try:
                            try:
                                page_actions.hover_element(
                                    self.driver, dropdown)
                            except Exception:
                                # If hovering fails, driver is likely outdated
                                # Time to go directly to the hidden link text
                                self.open(
                                    self.__get_href_from_partial_link_text(
                                        link_text))
                                return True
                            page_actions.hover_element_and_click(
                                self.driver, dropdown, link_text,
                                click_by=By.LINK_TEXT, timeout=0.12)
                            return True
                        except Exception:
                            pass
        return False

    def __recalculate_selector(self, selector, by):
        # Try to determine the type of selector automatically
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
        if page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
        if page_utils.is_partial_link_text_selector(selector):
            selector = page_utils.get_partial_link_text_from_selector(selector)
            by = By.PARTIAL_LINK_TEXT
        if page_utils.is_name_selector(selector):
            name = page_utils.get_name_from_selector(selector)
            selector = '[name="%s"]' % name
            by = By.CSS_SELECTOR
        return (selector, by)

    def __looks_like_a_page_url(self, url):
        """ Returns True if the url parameter looks like a URL. This method
            is slightly more lenient than page_utils.is_valid_url(url) due to
            possible typos when calling self.get(url), which will try to
            navigate to the page if a URL is detected, but will instead call
            self.get_element(URL_AS_A_SELECTOR) if the input in not a URL. """
        if (url.startswith("http:") or url.startswith("https:") or (
                url.startswith("://") or url.startswith("chrome:") or (
                url.startswith("about:") or url.startswith("data:") or (
                url.startswith("file:") or url.startswith("edge:") or (
                url.startswith("opera:")))))):
            return True
        else:
            return False

    def __make_css_match_first_element_only(self, selector):
        # Only get the first match
        return page_utils.make_css_match_first_element_only(selector)

    def __demo_mode_pause_if_active(self, tiny=False):
        if self.demo_mode:
            wait_time = settings.DEFAULT_DEMO_MODE_TIMEOUT
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            if not tiny:
                time.sleep(wait_time)
            else:
                time.sleep(wait_time / 3.4)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def __slow_mode_pause_if_active(self):
        if self.slow_mode:
            wait_time = settings.DEFAULT_DEMO_MODE_TIMEOUT
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            time.sleep(wait_time)

    def __demo_mode_scroll_if_active(self, selector, by):
        if self.demo_mode:
            self.slow_scroll_to(selector, by=by)

    def __demo_mode_highlight_if_active(self, selector, by):
        if self.demo_mode:
            # Includes self.slow_scroll_to(selector, by=by) by default
            self.highlight(selector, by=by)
        elif self.slow_mode:
            # Just do the slow scroll part of the highlight() method
            self.sleep(0.08)
            selector, by = self.__recalculate_selector(selector, by)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=settings.SMALL_TIMEOUT)
            try:
                scroll_distance = js_utils.get_scroll_distance_to_element(
                    self.driver, element)
                if abs(scroll_distance) > SSMD:
                    self.__jquery_slow_scroll_to(selector, by)
                else:
                    self.__slow_scroll_to_element(element)
            except (StaleElementReferenceException, ENI_Exception):
                self.wait_for_ready_state_complete()
                time.sleep(0.03)
                element = self.wait_for_element_visible(
                    selector, by=by, timeout=settings.SMALL_TIMEOUT)
                self.__slow_scroll_to_element(element)
            self.sleep(0.12)

    def __scroll_to_element(self, element, selector=None, by=By.CSS_SELECTOR):
        success = js_utils.scroll_to_element(self.driver, element)
        if not success and selector:
            self.wait_for_ready_state_complete()
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout=settings.SMALL_TIMEOUT)
        self.__demo_mode_pause_if_active(tiny=True)

    def __slow_scroll_to_element(self, element):
        js_utils.slow_scroll_to_element(self.driver, element, self.browser)

    def __highlight_with_assert_success(
            self, message, selector, by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't highlight if can't convert to CSS_SELECTOR
            return
        try:
            scroll_distance = js_utils.get_scroll_distance_to_element(
                self.driver, element)
            if abs(scroll_distance) > SSMD:
                self.__jquery_slow_scroll_to(selector, by)
            else:
                self.__slow_scroll_to_element(element)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.03)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=settings.SMALL_TIMEOUT)
            self.__slow_scroll_to_element(element)

        o_bs = ''  # original_box_shadow
        try:
            style = element.get_attribute('style')
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = self.wait_for_element_visible(
                selector, by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT)
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
        js_utils.highlight_with_js_2(
            self.driver, message, selector, o_bs, self.message_duration)

    def __highlight_with_jquery_2(self, message, selector, o_bs):
        js_utils.highlight_with_jquery_2(
            self.driver, message, selector, o_bs, self.message_duration)

    ############

    # Deprecated Methods (Replace these if they're still in your code!)

    @decorators.deprecated(
        "jq_format() is deprecated. Use re.escape() instead!")
    def jq_format(self, code):
        # DEPRECATED - re.escape() already performs the intended action!
        return js_utils._jq_format(code)

    ############

    def setUp(self, masterqa_mode=False):
        """
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass setUp() method:
        super(SubClassOfBaseCase, self).setUp()
        """
        self.masterqa_mode = masterqa_mode
        self.is_pytest = None
        try:
            # This raises an exception if the test is not coming from pytest
            self.is_pytest = sb_config.is_pytest
        except Exception:
            # Not using pytest (probably nosetests)
            self.is_pytest = False
        if self.is_pytest:
            # pytest-specific code
            test_id = self.__get_test_id()
            self.browser = sb_config.browser
            self.data = sb_config.data
            self.var1 = sb_config.var1
            self.var2 = sb_config.var2
            self.var3 = sb_config.var3
            self.slow_mode = sb_config.slow_mode
            self.demo_mode = sb_config.demo_mode
            self.demo_sleep = sb_config.demo_sleep
            self.highlights = sb_config.highlights
            self.time_limit = sb_config._time_limit
            sb_config.time_limit = sb_config._time_limit  # Reset between tests
            self.environment = sb_config.environment
            self.env = self.environment  # Add a shortened version
            self.with_selenium = sb_config.with_selenium  # Should be True
            self.headless = sb_config.headless
            self.headless_active = False
            self.headed = sb_config.headed
            self.locale_code = sb_config.locale_code
            self.start_page = sb_config.start_page
            self.log_path = sb_config.log_path
            self.with_testing_base = sb_config.with_testing_base
            self.with_basic_test_info = sb_config.with_basic_test_info
            self.with_screen_shots = sb_config.with_screen_shots
            self.with_page_source = sb_config.with_page_source
            self.with_db_reporting = sb_config.with_db_reporting
            self.with_s3_logging = sb_config.with_s3_logging
            self.servername = sb_config.servername
            self.port = sb_config.port
            self.proxy_string = sb_config.proxy_string
            self.user_agent = sb_config.user_agent
            self.mobile_emulator = sb_config.mobile_emulator
            self.device_metrics = sb_config.device_metrics
            self.cap_file = sb_config.cap_file
            self.cap_string = sb_config.cap_string
            self.settings_file = sb_config.settings_file
            self.database_env = sb_config.database_env
            self.message_duration = sb_config.message_duration
            self.js_checking_on = sb_config.js_checking_on
            self.ad_block_on = sb_config.ad_block_on
            self.block_images = sb_config.block_images
            self.verify_delay = sb_config.verify_delay
            self.disable_csp = sb_config.disable_csp
            self.enable_sync = sb_config.enable_sync
            self.use_auto_ext = sb_config.use_auto_ext
            self.no_sandbox = sb_config.no_sandbox
            self.disable_gpu = sb_config.disable_gpu
            self.incognito = sb_config.incognito
            self.guest_mode = sb_config.guest_mode
            self.devtools = sb_config.devtools
            self.swiftshader = sb_config.swiftshader
            self.user_data_dir = sb_config.user_data_dir
            self.extension_zip = sb_config.extension_zip
            self.extension_dir = sb_config.extension_dir
            self.maximize_option = sb_config.maximize_option
            self._reuse_session = sb_config.reuse_session
            self._crumbs = sb_config.crumbs
            self.save_screenshot_after_test = sb_config.save_screenshot
            self.visual_baseline = sb_config.visual_baseline
            self.timeout_multiplier = sb_config.timeout_multiplier
            self.pytest_html_report = sb_config.pytest_html_report
            self.report_on = False
            if self.pytest_html_report:
                self.report_on = True
            self.use_grid = False
            if self.servername != "localhost":
                # Use Selenium Grid (Use --server="127.0.0.1" for a local Grid)
                self.use_grid = True
            if self.with_db_reporting:
                import getpass
                import uuid
                from seleniumbase.core.application_manager import (
                    ApplicationManager)
                from seleniumbase.core.testcase_manager import (
                    ExecutionQueryPayload)
                from seleniumbase.core.testcase_manager import (
                    TestcaseDataPayload)
                from seleniumbase.core.testcase_manager import (
                    TestcaseManager)
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
                width = settings.HEADLESS_START_WIDTH
                height = settings.HEADLESS_START_HEIGHT
                try:
                    # from pyvirtualdisplay import Display  # Skip for own lib
                    from seleniumbase.virtual_display.display import Display
                    self.display = Display(visible=0, size=(width, height))
                    self.display.start()
                    self.headless_active = True
                except Exception:
                    # pyvirtualdisplay might not be necessary anymore because
                    # Chrome and Firefox now have built-in headless displays
                    pass
        else:
            # (Nosetests / Not Pytest)
            pass  # Setup performed in plugins

        # Verify that SeleniumBase is installed successfully
        if not hasattr(self, "browser"):
            raise Exception("""SeleniumBase plugins DID NOT load!\n\n"""
                            """*** Please REINSTALL SeleniumBase using: >\n"""
                            """    >>> "pip install -r requirements.txt"\n"""
                            """    >>> "python setup.py install" """)

        # Parse the settings file
        if self.settings_file:
            from seleniumbase.core import settings_parser
            settings_parser.set_settings(self.settings_file)

        # Mobile Emulator device metrics: CSS Width, CSS Height, & Pixel-Ratio
        if self.device_metrics:
            metrics_string = self.device_metrics
            metrics_string = metrics_string.replace(' ', '')
            metrics_list = metrics_string.split(',')
            exception_string = (
                'Invalid input for Mobile Emulator device metrics!\n'
                'Expecting a comma-separated string with three\n'
                'integer values for Width, Height, and Pixel-Ratio.\n'
                'Example: --metrics="411,731,3" ')
            if len(metrics_list) != 3:
                raise Exception(exception_string)
            try:
                self.__device_width = int(metrics_list[0])
                self.__device_height = int(metrics_list[1])
                self.__device_pixel_ratio = int(metrics_list[2])
                self.mobile_emulator = True
            except Exception:
                raise Exception(exception_string)
        if self.mobile_emulator:
            if not self.user_agent:
                # Use the Pixel 3 user agent by default if not specified
                self.user_agent = (
                    "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/76.0.3809.132 Mobile Safari/537.36")

        has_url = False
        if self._reuse_session:
            if not hasattr(sb_config, 'shared_driver'):
                sb_config.shared_driver = None
            if sb_config.shared_driver:
                try:
                    self._default_driver = sb_config.shared_driver
                    self.driver = sb_config.shared_driver
                    self._drivers_list = [sb_config.shared_driver]
                    url = self.get_current_url()
                    if len(url) > 3:
                        has_url = True
                    if self._crumbs:
                        self.driver.delete_all_cookies()
                except Exception:
                    pass
        if self._reuse_session and sb_config.shared_driver and has_url:
            if self.start_page and len(self.start_page) >= 4:
                if page_utils.is_valid_url(self.start_page):
                    self.open(self.start_page)
                else:
                    new_start_page = "http://" + self.start_page
                    if page_utils.is_valid_url(new_start_page):
                        self.open(new_start_page)
            elif self._crumbs:
                if self.get_current_url() != "data:,":
                    self.open("data:,")
            else:
                pass
        else:
            # Launch WebDriver for both Pytest and Nosetests
            self.driver = self.get_new_driver(browser=self.browser,
                                              headless=self.headless,
                                              locale_code=self.locale_code,
                                              servername=self.servername,
                                              port=self.port,
                                              proxy=self.proxy_string,
                                              agent=self.user_agent,
                                              switch_to=True,
                                              cap_file=self.cap_file,
                                              cap_string=self.cap_string,
                                              disable_csp=self.disable_csp,
                                              enable_sync=self.enable_sync,
                                              use_auto_ext=self.use_auto_ext,
                                              no_sandbox=self.no_sandbox,
                                              disable_gpu=self.disable_gpu,
                                              incognito=self.incognito,
                                              guest_mode=self.guest_mode,
                                              devtools=self.devtools,
                                              swiftshader=self.swiftshader,
                                              block_images=self.block_images,
                                              user_data_dir=self.user_data_dir,
                                              extension_zip=self.extension_zip,
                                              extension_dir=self.extension_dir,
                                              is_mobile=self.mobile_emulator,
                                              d_width=self.__device_width,
                                              d_height=self.__device_height,
                                              d_p_r=self.__device_pixel_ratio)
            self._default_driver = self.driver
            if self._reuse_session:
                sb_config.shared_driver = self.driver

        if self.browser in ["firefox", "ie", "safari"]:
            # Only Chromium-based browsers have the mobile emulator.
            # Some actions such as hover-clicking are different on mobile.
            self.mobile_emulator = False

        # Configure the test time limit (if used).
        self.set_time_limit(self.time_limit)

        # Set the start time for the test (in ms).
        # Although the pytest clock starts before setUp() begins,
        # the time-limit clock starts at the end of the setUp() method.
        sb_config.start_time_ms = int(time.time() * 1000.0)

    def __set_last_page_screenshot(self):
        """ self.__last_page_screenshot is only for pytest html report logs
            self.__last_page_screenshot_png is for all screenshot log files """
        if not self.__last_page_screenshot and (
                not self.__last_page_screenshot_png):
            try:
                element = self.driver.find_element(
                    by=By.TAG_NAME, value="body")
                if self.is_pytest and self.report_on:
                    self.__last_page_screenshot_png = (
                        self.driver.get_screenshot_as_png())
                    self.__last_page_screenshot = element.screenshot_as_base64
                else:
                    self.__last_page_screenshot_png = element.screenshot_as_png
            except Exception:
                if not self.__last_page_screenshot:
                    if self.is_pytest and self.report_on:
                        try:
                            self.__last_page_screenshot = (
                                self.driver.get_screenshot_as_base64())
                        except Exception:
                            pass
                if not self.__last_page_screenshot_png:
                    try:
                        self.__last_page_screenshot_png = (
                            self.driver.get_screenshot_as_png())
                    except Exception:
                        pass

    def __set_last_page_url(self):
        if not self.__last_page_url:
            try:
                self.__last_page_url = log_helper.get_last_page(self.driver)
            except Exception:
                self.__last_page_url = None

    def __set_last_page_source(self):
        if not self.__last_page_source:
            try:
                self.__last_page_source = (
                    log_helper.get_html_source_with_base_href(
                        self.driver, self.driver.page_source))
            except Exception:
                self.__last_page_source = None

    def __insert_test_result(self, state, err):
        from seleniumbase.core.testcase_manager import TestcaseDataPayload
        data_payload = TestcaseDataPayload()
        data_payload.runtime = int(time.time() * 1000) - self.case_start_time
        data_payload.guid = self.testcase_guid
        data_payload.execution_guid = self.execution_guid
        data_payload.state = state
        if err:
            import traceback
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
        if not self.__added_pytest_html_extra:
            try:
                if self.with_selenium:
                    if not self.__last_page_screenshot:
                        self.__set_last_page_screenshot()
                        self.__set_last_page_url()
                        self.__set_last_page_source()
                    if self.report_on:
                        extra_url = {}
                        extra_url['name'] = 'URL'
                        extra_url['format'] = 'url'
                        extra_url['content'] = self.get_current_url()
                        extra_url['mime_type'] = None
                        extra_url['extension'] = None
                        extra_image = {}
                        extra_image['name'] = 'Screenshot'
                        extra_image['format'] = 'image'
                        extra_image['content'] = self.__last_page_screenshot
                        extra_image['mime_type'] = 'image/png'
                        extra_image['extension'] = 'png'
                        self.__added_pytest_html_extra = True
                        self._html_report_extra.append(extra_url)
                        self._html_report_extra.append(extra_image)
            except Exception:
                pass

    def __quit_all_drivers(self):
        if self._reuse_session and sb_config.shared_driver:
            if len(self._drivers_list) > 0:
                sb_config.shared_driver = self._drivers_list[0]
                self._default_driver = self._drivers_list[0]
                self.switch_to_default_driver()
            if len(self._drivers_list) > 1:
                self._drivers_list = self._drivers_list[1:]
            else:
                self._drivers_list = []

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
        self._default_driver = None
        self._drivers_list = []

    def __has_exception(self):
        has_exception = False
        if hasattr(sys, 'last_traceback') and sys.last_traceback is not None:
            has_exception = True
        elif sys.version_info[0] >= 3 and hasattr(self, '_outcome'):
            if hasattr(self._outcome, 'errors') and self._outcome.errors:
                has_exception = True
        else:
            has_exception = sys.exc_info()[1] is not None
        return has_exception

    def __get_test_id(self):
        test_id = "%s.%s.%s" % (self.__class__.__module__,
                                self.__class__.__name__,
                                self._testMethodName)
        if self._sb_test_identifier and len(str(self._sb_test_identifier)) > 6:
            test_id = self._sb_test_identifier
        return test_id

    def __create_log_path_as_needed(self, test_logpath):
        if not os.path.exists(test_logpath):
            try:
                os.makedirs(test_logpath)
            except Exception:
                pass  # Only reachable during multi-threaded runs

    def save_teardown_screenshot(self):
        """ (Should ONLY be used at the start of custom tearDown() methods.)
            This method takes a screenshot of the current web page for a
            failing test (or when running your tests with --save-screenshot).
            That way your tearDown() method can navigate away from the last
            page where the test failed, and still get the correct screenshot
            before performing tearDown() steps on other pages. If this method
            is not included in your custom tearDown() method, a screenshot
            will still be taken after the last step of your tearDown(), where
            you should be calling "super(SubClassOfBaseCase, self).tearDown()"
        """
        if self.__has_exception() or self.save_screenshot_after_test:
            test_id = self.__get_test_id()
            test_logpath = self.log_path + "/" + test_id
            self.__create_log_path_as_needed(test_logpath)
            self.__set_last_page_screenshot()
            self.__set_last_page_url()
            self.__set_last_page_source()
            if self.is_pytest:
                self.__add_pytest_html_extra()

    def tearDown(self):
        """
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass's tearDown():
        super(SubClassOfBaseCase, self).tearDown()
        """
        try:
            is_pytest = self.is_pytest  # This fails if overriding setUp()
            if is_pytest:
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
        # *** Start tearDown() officially ***
        self.__slow_mode_pause_if_active()
        has_exception = self.__has_exception()
        if self.__deferred_assert_failures:
            print(
                "\nWhen using self.deferred_assert_*() methods in your tests, "
                "remember to call self.process_deferred_asserts() afterwards. "
                "Now calling in tearDown()...\nFailures Detected:")
            if not has_exception:
                self.process_deferred_asserts()
            else:
                self.process_deferred_asserts(print_only=True)
        if self.is_pytest:
            # pytest-specific code
            test_id = self.__get_test_id()
            if with_selenium:
                # Save a screenshot if logging is on when an exception occurs
                if has_exception:
                    self.__add_pytest_html_extra()
                if self.with_testing_base and not has_exception and (
                        self.save_screenshot_after_test):
                    test_logpath = self.log_path + "/" + test_id
                    self.__create_log_path_as_needed(test_logpath)
                    if not self.__last_page_screenshot_png:
                        self.__set_last_page_screenshot()
                        self.__set_last_page_url()
                        self.__set_last_page_source()
                    log_helper.log_screenshot(
                        test_logpath,
                        self.driver,
                        self.__last_page_screenshot_png)
                    self.__add_pytest_html_extra()
                if self.with_testing_base and has_exception:
                    test_logpath = self.log_path + "/" + test_id
                    self.__create_log_path_as_needed(test_logpath)
                    if ((not self.with_screen_shots) and (
                            not self.with_basic_test_info) and (
                            not self.with_page_source)):
                        # Log everything if nothing specified (if testing_base)
                        if not self.__last_page_screenshot_png:
                            self.__set_last_page_screenshot()
                            self.__set_last_page_url()
                            self.__set_last_page_source()
                        log_helper.log_screenshot(
                            test_logpath,
                            self.driver,
                            self.__last_page_screenshot_png)
                        log_helper.log_test_failure_data(
                            self, test_logpath, self.driver, self.browser,
                            self.__last_page_url)
                        log_helper.log_page_source(
                            test_logpath, self.driver, self.__last_page_source)
                    else:
                        if self.with_screen_shots:
                            if not self.__last_page_screenshot_png:
                                self.__set_last_page_screenshot()
                                self.__set_last_page_url()
                                self.__set_last_page_source()
                            log_helper.log_screenshot(
                                test_logpath,
                                self.driver,
                                self.__last_page_screenshot_png)
                        if self.with_basic_test_info:
                            log_helper.log_test_failure_data(
                                self, test_logpath, self.driver, self.browser,
                                self.__last_page_url)
                        if self.with_page_source:
                            log_helper.log_page_source(
                                test_logpath, self.driver,
                                self.__last_page_source)
                # (Pytest) Finally close all open browser windows
                self.__quit_all_drivers()
            if self.headless:
                if self.headless_active:
                    try:
                        self.display.stop()
                    except AttributeError:
                        pass
                    except Exception:
                        pass
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
                import uuid
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
                logging.info(
                    "\n\n*** Log files uploaded: ***\n%s\n" % index_file)
                if self.with_db_reporting:
                    from seleniumbase.core.testcase_manager import (
                        TestcaseDataPayload)
                    from seleniumbase.core.testcase_manager import (
                        TestcaseManager)
                    self.testcase_manager = TestcaseManager(self.database_env)
                    data_payload = TestcaseDataPayload()
                    data_payload.guid = self.testcase_guid
                    data_payload.logURL = index_file
                    self.testcase_manager.update_testcase_log_url(data_payload)
        else:
            # (Nosetests)
            if has_exception:
                test_id = self.__get_test_id()
                test_logpath = self.log_path + "/" + test_id
                self.__create_log_path_as_needed(test_logpath)
                log_helper.log_test_failure_data(
                    self, test_logpath, self.driver, self.browser,
                    self.__last_page_url)
                if len(self._drivers_list) > 0:
                    if not self.__last_page_screenshot_png:
                        self.__set_last_page_screenshot()
                        self.__set_last_page_url()
                        self.__set_last_page_source()
                    log_helper.log_screenshot(
                        test_logpath,
                        self.driver,
                        self.__last_page_screenshot_png)
                    log_helper.log_page_source(
                        test_logpath, self.driver, self.__last_page_source)
            elif self.save_screenshot_after_test:
                test_id = self.__get_test_id()
                test_logpath = self.log_path + "/" + test_id
                self.__create_log_path_as_needed(test_logpath)
                if not self.__last_page_screenshot_png:
                    self.__set_last_page_screenshot()
                    self.__set_last_page_url()
                    self.__set_last_page_source()
                log_helper.log_screenshot(
                    test_logpath,
                    self.driver,
                    self.__last_page_screenshot_png)
            if self.report_on:
                self._last_page_screenshot = self.__last_page_screenshot_png
                try:
                    self._last_page_url = self.get_current_url()
                except Exception:
                    self._last_page_url = "(Error: Unknown URL)"
            # Finally close all open browser windows
            self.__quit_all_drivers()
