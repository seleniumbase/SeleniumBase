"""
These methods improve on and expand existing WebDriver commands.
Improvements include making WebDriver commands more robust and more reliable
by giving page elements enough time to load before taking action on them.
"""

import getpass
import json
import logging
import os
import pytest
import sys
import time
import traceback
import unittest
import uuid
from BeautifulSoup import BeautifulSoup
from pyvirtualdisplay import Display
from seleniumbase.config import settings
from seleniumbase.core.application_manager import ApplicationManager
from seleniumbase.core.s3_manager import S3LoggingBucket
from seleniumbase.core.testcase_manager import ExecutionQueryPayload
from seleniumbase.core.testcase_manager import TestcaseDataPayload
from seleniumbase.core.testcase_manager import TestcaseManager
from seleniumbase.core import browser_launcher
from seleniumbase.core import log_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import page_actions
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import xpath_to_css
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        self.page_check_count = 0
        self.page_check_failures = []

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
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        pre_action_url = self.driver.current_url
        try:
            element.click()
        except StaleElementReferenceException:
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
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        pre_action_url = self.driver.current_url
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.double_click(element)
            actions.perform()
        except StaleElementReferenceException:
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
        for selector in selectors_list:
            self.click(selector, by=by, timeout=timeout)
            if spacing > 0:
                time.sleep(spacing)

    def click_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ This method clicks link text on a page """
        # If using phantomjs, might need to extract and open the link directly
        if self.browser == 'phantomjs':
            if self.is_link_text_visible(link_text):
                element = self.wait_for_link_text_visible(link_text)
                element.click()
                return
            source = self.driver.page_source
            soup = BeautifulSoup(source)
            html_links = soup.fetch('a')
            for html_link in html_links:
                if html_link.text == link_text:
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
                        'Could not parse link from link_text [%s]' % link_text)
            raise Exception("Link text [%s] was not found!" % link_text)
        # Not using phantomjs
        element = self.wait_for_link_text_visible(link_text, timeout=timeout)
        self._demo_mode_highlight_if_active(link_text, by=By.LINK_TEXT)
        pre_action_url = self.driver.current_url
        try:
            element.click()
        except StaleElementReferenceException:
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = self.wait_for_link_text_visible(
                link_text, timeout=timeout)
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
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)
        try:
            element_text = element.text
        except StaleElementReferenceException:
            self.wait_for_ready_state_complete()
            time.sleep(0.06)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout)
            element_text = element.text
        return element_text

    def get_attribute(self, selector, attribute, by=By.CSS_SELECTOR,
                      timeout=settings.SMALL_TIMEOUT):
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)
        try:
            attribute_value = element.get_attribute(attribute)
        except StaleElementReferenceException:
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

    def add_text(self, selector, new_value, by=By.CSS_SELECTOR,
                 timeout=settings.SMALL_TIMEOUT):
        """ The more-reliable version of driver.send_keys()
            Similar to update_text(), but won't clear the text field first. """
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
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
        except StaleElementReferenceException:
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
                  timeout=settings.SMALL_TIMEOUT):
        """ Same as add_text() -> more reliable, but less name confusion. """
        self.add_text(selector, new_value, by=by, timeout=timeout)

    def update_text_value(self, selector, new_value, by=By.CSS_SELECTOR,
                          timeout=settings.SMALL_TIMEOUT, retry=False):
        """ This method updates an element's text value with a new value.
            @Params
            selector - the selector with the value to update
            new_value - the new value for setting the text field
            by - the type of selector to search by (Default: CSS)
            timeout - how long to wait for the selector to be visible
            retry - if True, use jquery if the selenium text update fails
        """
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        try:
            element.clear()
        except StaleElementReferenceException:
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
        except StaleElementReferenceException:
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
                    timeout=settings.SMALL_TIMEOUT, retry=False):
        """ The shorter version of update_text_value(), which
            clears existing text and adds new text into the text field.
            We want to keep the old version for backward compatibility. """
        self.update_text_value(selector, new_value, by=by,
                               timeout=timeout, retry=retry)

    def is_element_present(self, selector, by=By.CSS_SELECTOR):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.is_element_present(self.driver, selector, by)

    def is_element_visible(self, selector, by=By.CSS_SELECTOR):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.is_element_visible(self.driver, selector, by)

    def is_link_text_visible(self, link_text):
        return page_actions.is_element_visible(self.driver, link_text,
                                               by=By.LINK_TEXT)

    def is_text_visible(self, text, selector, by=By.CSS_SELECTOR):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.is_text_visible(self.driver, text, selector, by)

    def find_visible_elements(self, selector, by=By.CSS_SELECTOR):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.find_visible_elements(self.driver, selector, by)

    def execute_script(self, script):
        return self.driver.execute_script(script)

    def set_window_size(self, width, height):
        return self.driver.set_window_size(width, height)
        self._demo_mode_pause_if_active()

    def maximize_window(self):
        return self.driver.maximize_window()
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
            '''script.src = "http://code.jquery.com/jquery-3.1.0.min.js"; '''
            '''document.getElementsByTagName("head")[0]'''
            '''.appendChild(script);''')
        for x in xrange(30):
            # jQuery needs a small amount of time to activate. (At most 3s)
            try:
                self.execute_script("jQuery('html')")
                return
            except Exception:
                time.sleep(0.1)
        # Since jQuery still isn't activating, give up and raise an exception
        raise Exception("Exception: WebDriver could not activate jQuery!")

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
        element = self.find_element(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if scroll:
            self._slow_scroll_to_element(element)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't highlight if can't convert to CSS_SELECTOR for jQuery
            return

        # Only get the first match
        last_syllable = selector.split(' ')[-1]
        if ':' not in last_syllable:
            selector += ':first'

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
        try:
            self.execute_script(script)
        except Exception:
            self.activate_jquery()
            self.execute_script(script)
        if self.highlights:
            loops = self.highlights
        loops = int(loops)
        for n in xrange(loops):
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
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        try:
            self._scroll_to_element(element)
        except StaleElementReferenceException:
            self.wait_for_ready_state_complete()
            time.sleep(0.05)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout)
            self._scroll_to_element(element)

    def slow_scroll_to(self, selector, by=By.CSS_SELECTOR,
                       timeout=settings.SMALL_TIMEOUT):
        ''' Slow motion scroll to destination '''
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._slow_scroll_to_element(element)

    def scroll_click(self, selector, by=By.CSS_SELECTOR):
        self.scroll_to(selector, by=by)
        self.click(selector, by=by)

    def jquery_click(self, selector, by=By.CSS_SELECTOR):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        selector = self.convert_to_css_selector(selector, by=by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        if self.is_element_visible(selector, by=by):
            self._demo_mode_highlight_if_active(selector, by)

        # Only get the first match
        last_syllable = selector.split(' ')[-1]
        if ':' not in last_syllable:
            selector += ':first'

        click_script = """jQuery('%s')[0].click()""" % selector
        try:
            self.execute_script(click_script)
        except Exception:
            # The likely reason this fails is because: "jQuery is not defined"
            self.activate_jquery()  # It's a good thing we can define it here
            self.execute_script(click_script)
        self._demo_mode_pause_if_active()

    def jq_format(self, code):
        return page_utils.jq_format(code)

    def get_domain_url(self, url):
        return page_utils.get_domain_url(url)

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
                  timeout=settings.SMALL_TIMEOUT):
        """ This method uses jQuery to update a text field. """
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        selector = self.convert_to_css_selector(selector, by=by)
        self._demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by, timeout=timeout)
        value = json.dumps(new_value)

        # Only get the first match
        last_syllable = selector.split(' ')[-1]
        if ':' not in last_syllable:
            selector += ':first'

        set_value_script = """jQuery('%s').val(%s)""" % (selector, value)
        try:
            self.execute_script(set_value_script)
        except Exception:
            # The likely reason this fails is because: "jQuery is not defined"
            self.activate_jquery()  # It's a good thing we can define it here
            self.execute_script(set_value_script)
        self._demo_mode_pause_if_active()

    def jquery_update_text_value(self, selector, new_value, by=By.CSS_SELECTOR,
                                 timeout=settings.SMALL_TIMEOUT):
        """ This method uses jQuery to update a text field.
            If the new_value string ends with the newline character,
            WebDriver will finish the call, which simulates pressing
            {Enter/Return} after the text is entered.  """
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout)
        self._demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        selector = self.convert_to_css_selector(selector, by=by)

        # Only get the first match
        last_syllable = selector.split(' ')[-1]
        if ':' not in last_syllable:
            selector += ':first'

        update_text_script = """jQuery('%s').val('%s')""" % (
            selector, self.jq_format(new_value))
        try:
            self.execute_script(update_text_script)
        except Exception:
            # The likely reason this fails is because: "jQuery is not defined"
            self.activate_jquery()  # It's a good thing we can define it here
            self.execute_script(update_text_script)
        if new_value.endswith('\n'):
            element.send_keys('\n')
        self._demo_mode_pause_if_active()

    def jquery_update_text(self, selector, new_value, by=By.CSS_SELECTOR,
                           timeout=settings.SMALL_TIMEOUT):
        """ The shorter version of jquery_update_text_value()
            (The longer version remains for backwards compatibility.) """
        self.jquery_update_text_value(
            selector, new_value, by=by, timeout=timeout)

    def hover_on_element(self, selector, by=By.CSS_SELECTOR):
        self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT)
        self._demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        time.sleep(0.05)  # Settle down from scrolling before hovering
        return page_actions.hover_on_element(self.driver, selector)

    def hover_and_click(self, hover_selector, click_selector,
                        hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                        timeout=settings.SMALL_TIMEOUT):
        if hover_selector.startswith('/') or hover_selector.startswith('./'):
            hover_by = By.XPATH
        if click_selector.startswith('/') or click_selector.startswith('./'):
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

    ############

    def wait_for_element_present(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to appear in the HTML of a page.
            The element does not need be visible (it may be hidden). """
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)

    def assert_element_present(self, selector, by=By.CSS_SELECTOR,
                               timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_present(), but returns nothing.
            Waits for an element to appear in the HTML of a page.
            The element does not need be visible (it may be hidden).
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
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
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)

    def wait_for_element(self, selector, by=By.CSS_SELECTOR,
                         timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_element_visible() """
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def find_element(self, selector, by=By.CSS_SELECTOR,
                     timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_element_visible() - returns the element """
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def assert_element(self, selector, by=By.CSS_SELECTOR,
                       timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        self.wait_for_element_visible(selector, by=by, timeout=timeout)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_text_visible(self, text, selector, by=By.CSS_SELECTOR,
                              timeout=settings.LARGE_TIMEOUT):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_text_visible(
            self.driver, text, selector, by, timeout)

    def wait_for_text(self, text, selector, by=By.CSS_SELECTOR,
                      timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_text_visible() """
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def find_text(self, text, selector, by=By.CSS_SELECTOR,
                  timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_text_visible() - returns the element """
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout)

    def assert_text(self, text, selector, by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_text_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
        return True

    # For backwards compatibility, earlier method names of the next
    # four methods have remained even though they do the same thing,
    # with the exception of assert_*, which won't return the element,
    # but like the others, will raise an exception if the call fails.

    def wait_for_link_text_visible(self, link_text,
                                   timeout=settings.LARGE_TIMEOUT):
        return self.wait_for_element_visible(
            link_text, by=By.LINK_TEXT, timeout=timeout)

    def wait_for_link_text(self, link_text, timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_link_text_visible() """
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def find_link_text(self, link_text, timeout=settings.LARGE_TIMEOUT):
        """ Same as wait_for_link_text_visible() - returns the element """
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def assert_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_link_text_visible(), but returns nothing.
            As above, will raise an exception if nothing can be found.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        self.wait_for_link_text_visible(link_text, timeout=timeout)
        return True

    ############

    def wait_for_element_absent(self, selector, by=By.CSS_SELECTOR,
                                timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to no longer appear in the HTML of a page.
            A hidden element still counts as appearing in the page HTML.
            If an element with "hidden" status is acceptable,
            use wait_for_element_not_visible() instead. """
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_element_absent(
            self.driver, selector, by, timeout)

    def assert_element_absent(self, selector, by=By.CSS_SELECTOR,
                              timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_absent() - returns nothing.
            As above, will raise an exception if the element stays present.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        self.wait_for_element_absent(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                     timeout=settings.LARGE_TIMEOUT):
        """ Waits for an element to no longer be visible on a page.
            The element can be non-existant in the HTML or hidden on the page
            to qualify as not visible. """
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_element_not_visible(
            self.driver, selector, by, timeout)

    def assert_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                   timeout=settings.SMALL_TIMEOUT):
        """ Similar to wait_for_element_not_visible() - returns nothing.
            As above, will raise an exception if the element stays visible.
            Returns True if successful. Default timeout = SMALL_TIMEOUT. """
        self.wait_for_element_not_visible(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_ready_state_complete(self, timeout=settings.EXTREME_TIMEOUT):
        return page_actions.wait_for_ready_state_complete(self.driver, timeout)

    def wait_for_and_accept_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def wait_for_and_dismiss_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def wait_for_and_switch_to_alert(self, timeout=settings.LARGE_TIMEOUT):
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)

    def save_screenshot(self, name, folder=None):
        return page_actions.save_screenshot(self.driver, name, folder)

    ############

    def _get_exception_message(self):
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

    def _package_check(self):
        current_url = self.driver.current_url
        message = self._get_exception_message()
        self.page_check_failures.append(
                "CHECK #%s: (%s)\n %s" % (
                    self.page_check_count, current_url, message))

    def check_assert_element(self, selector, by=By.CSS_SELECTOR,
                             timeout=settings.MINI_TIMEOUT):
        """ A non-terminating assertion for an element on a page.
            Any and all exceptions will be saved until the process_checks()
            method is called from inside a test, likely at the end of it. """
        self.page_check_count += 1
        try:
            self.wait_for_element_visible(selector, by=by, timeout=timeout)
            return True
        except Exception:
            self._package_check()
            return False

    def check_assert_text(self, text, selector, by=By.CSS_SELECTOR,
                          timeout=settings.MINI_TIMEOUT):
        """ A non-terminating assertion for text from an element on a page.
            Any and all exceptions will be saved until the process_checks()
            method is called from inside a test, likely at the end of it. """
        self.page_check_count += 1
        try:
            self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
            return True
        except Exception:
            self._package_check()
            return False

    def process_checks(self):
        """ To be used at the end of any test that uses checks, which are
            non-terminating verifications that will only raise an exception
            after this method is called. Useful for pages with multiple
            elements to be checked when you want to find as many failures
            as possible on a page before making fixes.
            Might be more useful if this method is called after processing
            all the checks for a single html page, otherwise the screenshot
            in the logs file won't match the location of the checks. """
        if self.page_check_failures:
            exception_output = ''
            exception_output += "\n*** FAILED CHECKS FOR: %s\n" % self.id()
            all_failing_checks = self.page_check_failures
            self.page_check_failures = []
            for tb in all_failing_checks:
                exception_output += "%s\n" % tb
            raise Exception(exception_output)

    ############

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
        self.execute_script(scroll_script)
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
            for y in xrange(int(total_steps)):
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


# PyTest-Specific Code #

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
            self.database_env = pytest.config.option.database_env
            self.log_path = pytest.config.option.log_path
            self.browser = pytest.config.option.browser
            self.data = pytest.config.option.data
            self.demo_mode = pytest.config.option.demo_mode
            self.demo_sleep = pytest.config.option.demo_sleep
            self.highlights = pytest.config.option.highlights
            self.verify_delay = pytest.config.option.verify_delay
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
                self.display = Display(visible=0, size=(1200, 800))
                self.display.start()
                self.headless_active = True
            if self.with_selenium:
                self.driver = browser_launcher.get_driver(self.browser)

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

    def tearDown(self):
        """
        pytest-specific code
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass's tearDown():
        super(SubClassOfBaseCase, self).tearDown()
        """
        if self.page_check_failures:
            # self.process_checks() was not called after checks were made.
            # We will log those now here, but without raising an exception.
            exception_output = ''
            exception_output += "\n*** FAILED CHECKS FOR: %s\n" % self.id()
            for tb in self.page_check_failures:
                exception_output += "%s\n" % tb
            logging.exception(exception_output)
        self.is_pytest = None
        try:
            # This raises an exception if the test is not coming from pytest
            self.is_pytest = pytest.config.option.is_pytest
        except Exception:
            # Not using pytest (probably nosetests)
            self.is_pytest = False
        if self.is_pytest:
            test_id = "%s.%s.%s" % (self.__class__.__module__,
                                    self.__class__.__name__,
                                    self._testMethodName)
            if self.with_selenium:
                # Save a screenshot if logging is on when an exception occurs
                if self.with_testing_base and (sys.exc_info()[1] is not None):
                    test_logpath = self.log_path + "/" + test_id
                    if not os.path.exists(test_logpath):
                        os.makedirs(test_logpath)
                    if ((not self.with_screen_shots) and
                            (not self.with_basic_test_info) and
                            (not self.with_page_source)):
                        # Log everything if nothing specified (if testing_base)
                        log_helper.log_screenshot(test_logpath, self.driver)
                        log_helper.log_test_failure_data(
                            test_logpath, self.driver, self.browser)
                        log_helper.log_page_source(test_logpath, self.driver)
                    else:
                        if self.with_screen_shots:
                            log_helper.log_screenshot(
                                test_logpath, self.driver)
                        if self.with_basic_test_info:
                            log_helper.log_test_failure_data(
                                test_logpath, self.driver, self.browser)
                        if self.with_page_source:
                            log_helper.log_page_source(
                                test_logpath, self.driver)
                # Finally close the browser
                self.driver.quit()
            if self.headless:
                if self.headless_active:
                    self.display.stop()
            if self.with_db_reporting:
                if sys.exc_info()[1] is not None:
                    self.__insert_test_result(constants.State.ERROR, True)
                else:
                    self.__insert_test_result(constants.State.PASS, False)
                runtime = int(time.time() * 1000) - self.execution_start_time
                self.testcase_manager.update_execution_data(
                    self.execution_guid, runtime)
            if self.with_s3_logging and (sys.exc_info()[1] is not None):
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
