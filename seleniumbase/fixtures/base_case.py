# -*- coding: utf-8 -*-
r"""----------------------------------------------------------------->
|    ______     __           _                  ____                 |
|   / ____/__  / /__  ____  (_)_  ______ ___   / _  \____  ________  |
|   \__ \/ _ \/ / _ \/ __ \/ / / / / __ `__ \ / /_) / __ \/ ___/ _ \ |
|  ___/ /  __/ /  __/ / / / / /_/ / / / / / // /_) / (_/ /__  /  __/ |
| /____/\___/_/\___/_/ /_/_/\__,_/_/ /_/ /_//_____/\__,_/____/\___/  |
|                                                                    |
--------------------------------------------------------------------->

The BaseCase class is the main gateway for using The SeleniumBase Framework.
It inherits Python's unittest.TestCase class and runs with pytest or nosetests.
All tests using BaseCase automatically launch WebDriver browsers for tests.

Example Test:

# --------------------------------------------------------------
from seleniumbase import BaseCase
class MyTestClass(BaseCase):
    def test_anything(self):
        # Write your code here. Example:
        self.open("https://github.com/")
        self.type("input.header-search-input", "SeleniumBase\n")
        self.click('a[href="/seleniumbase/SeleniumBase"]')
        self.assert_element("div.repository-content")
# --------------------------------------------------------------

SeleniumBase methods expand and improve on existing WebDriver commands.
Improvements include making WebDriver more robust, reliable, and flexible.
Page elements are given enough time to load before WebDriver acts on them.
Code becomes greatly simplified and easier to maintain.
"""

import codecs
import fasteners
import json
import logging
import math
import os
import re
import shutil
import sys
import textwrap
import time
import unittest
import urllib3
from contextlib import contextmanager
from selenium.common.exceptions import (
    ElementClickInterceptedException as ECI_Exception,
    ElementNotInteractableException as ENI_Exception,
    InvalidArgumentException,
    MoveTargetOutOfBoundsException,
    NoSuchElementException,
    NoSuchWindowException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
from seleniumbase import config as sb_config
from seleniumbase.__version__ import __version__
from seleniumbase.common import decorators
from seleniumbase.config import settings
from seleniumbase.core import download_helper
from seleniumbase.core import log_helper
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import css_to_xpath
from seleniumbase.fixtures import js_utils
from seleniumbase.fixtures import page_actions
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import shared_utils
from seleniumbase.fixtures import xpath_to_css

__all__ = ["BaseCase"]

logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
urllib3.disable_warnings()
LOGGER.setLevel(logging.WARNING)
is_windows = False
if sys.platform in ["win32", "win64", "x64"]:
    is_windows = True
python3 = True
if sys.version_info[0] < 3:
    python3 = False
    reload(sys)  # noqa: F821
    sys.setdefaultencoding("utf8")
selenium4_or_newer = False
if sys.version_info >= (3, 7):
    selenium4_or_newer = True


class BaseCase(unittest.TestCase):
    """<Class seleniumbase.BaseCase>"""

    def __init__(self, *args, **kwargs):
        super(BaseCase, self).__init__(*args, **kwargs)
        self.__initialize_variables()

    def __initialize_variables(self):
        self.driver = None
        self.environment = None
        self.env = None  # Add a shortened version of self.environment
        self.version_list = [
            int(i) for i in __version__.split(".") if i.isdigit()
        ]
        self.version_tuple = tuple(self.version_list)
        self.version_info = self.version_tuple
        self.__page_sources = []
        self.__extra_actions = []
        self.__js_start_time = 0
        self.__set_c_from_switch = False
        self.__frame_switch_layer = 0  # Used by Recorder-Mode
        self.__frame_switch_multi = False  # Used by Recorder-Mode
        self.__last_saved_url = None  # Used by Recorder-Mode
        self.__called_setup = False
        self.__called_teardown = False
        self.__start_time_ms = None
        self.__requests_timeout = None
        self.__screenshot_count = 0
        self.__level_0_visual_f = False
        self.__will_be_skipped = False
        self.__passed_then_skipped = False
        self.__visual_baseline_copies = []
        self.__last_url_of_deferred_assert = "about:blank"
        self.__last_page_load_url = "about:blank"
        self.__last_page_screenshot = None
        self.__last_page_screenshot_png = None
        self.__last_page_url = None
        self.__last_page_source = None
        self.__skip_reason = None
        self.__origins_to_save = []
        self.__actions_to_save = []
        self.__dont_record_open = False
        self.__dont_record_js_click = False
        self.__new_window_on_rec_open = True
        self.__overrided_default_timeouts = False
        self.__added_pytest_html_extra = None
        self.__deferred_assert_count = 0
        self.__deferred_assert_failures = []
        self.__device_width = None
        self.__device_height = None
        self.__device_pixel_ratio = None
        self.__changed_jqc_theme = False
        self.__jqc_default_theme = None
        self.__jqc_default_color = None
        self.__jqc_default_width = None
        # Requires self._* instead of self.__* for external class use
        self._language = "English"
        self._presentation_slides = {}
        self._presentation_transition = {}
        self._rec_overrides_switch = True  # Recorder-Mode uses set_c vs switch
        self._sb_test_identifier = None
        self._html_report_extra = []  # (Used by pytest_plugin.py)
        self._last_page_screenshot = None
        self._last_page_url = None
        self._final_debug = None
        self._default_driver = None
        self._drivers_list = []
        self._drivers_browser_map = {}
        self._was_skipped = False
        self._chart_data = {}
        self._chart_count = 0
        self._chart_label = {}
        self._chart_xcount = 0
        self._chart_first_series = {}
        self._chart_series_count = {}
        self._tour_steps = {}

    def open(self, url):
        """Navigates the current browser window to the specified page."""
        self.__check_scope()
        self.__check_browser()
        if self.__needs_minimum_wait():
            time.sleep(0.025)
            if self.undetectable:
                time.sleep(0.025)
        pre_action_url = None
        try:
            pre_action_url = self.driver.current_url
        except Exception:
            pass
        url = str(url).strip()  # Remove leading and trailing whitespace
        if not self.__looks_like_a_page_url(url):
            # url should start with one of the following:
            # "http:", "https:", "://", "data:", "file:",
            # "about:", "chrome:", "opera:", or "edge:".
            if page_utils.is_valid_url("https://" + url):
                url = "https://" + url
            else:
                raise Exception('Invalid URL: "%s"!' % url)
        self.__last_page_load_url = None
        js_utils.clear_out_console_logs(self.driver)
        if url.startswith("://"):
            # Convert URLs such as "://google.com" into "https://google.com"
            url = "https" + url
        if self.recorder_mode and not self.__dont_record_open:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["_url_", origin, url, time_stamp]
            self.__extra_actions.append(action)
        if self.recorder_mode and self.__new_window_on_rec_open:
            c_url = self.driver.current_url
            if ("http:") in c_url or ("https:") in c_url or ("file:") in c_url:
                if self.get_domain_url(url) != self.get_domain_url(c_url):
                    self.open_new_window(switch_to=True)
        try:
            self.driver.get(url)
        except Exception as e:
            if (
                "ERR_CONNECTION_TIMED_OUT" in e.msg
                or "ERR_CONNECTION_CLOSED" in e.msg
            ):
                time.sleep(0.5)
                self.driver.get(url)
            elif "Timed out receiving message from renderer" in e.msg:
                page_load_timeout = None
                if selenium4_or_newer:
                    page_load_timeout = self.driver.timeouts.page_load
                else:
                    if hasattr(settings, "PAGE_LOAD_TIMEOUT"):
                        page_load_timeout = settings.PAGE_LOAD_TIMEOUT
                    else:
                        page_load_timeout = 120
                logging.info(
                    "The page load timed out after %s seconds! Will retry..."
                    % page_load_timeout
                )
                try:
                    self.driver.get(url)
                except Exception as e:
                    if "Timed out receiving message from renderer" in e.msg:
                        raise Exception(
                            "Retry of page load timed out after %s seconds!"
                            % page_load_timeout
                        )
                    else:
                        raise
            elif (
                "cannot determine loading status" in e.msg
                or "unexpected command response" in e.msg
            ):
                pass  # Odd issue where the open did happen. Continue.
            else:
                raise Exception(e.msg)
        if self.driver.current_url == pre_action_url and pre_action_url != url:
            time.sleep(0.1)  # Make sure load happens
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.03)  # Force a minimum wait, even if skipping waits.
            if self.undetectable:
                time.sleep(0.02)
        self.__demo_mode_pause_if_active()

    def get(self, url):
        """If "url" looks like a page URL, open the URL in the web browser.
        Otherwise, return self.get_element(URL_AS_A_SELECTOR)
        Examples:
            self.get("https://seleniumbase.io")  # Navigates to the URL
            self.get("input.class")  # Finds and returns the WebElement
        """
        self.__check_scope()
        if self.__looks_like_a_page_url(url):
            self.open(url)
        else:
            return self.get_element(url)  # url is treated like a selector

    def click(
        self, selector, by="css selector", timeout=None, delay=0, scroll=True
    ):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        original_by = by
        selector, by = self.__recalculate_selector(selector, by)
        if delay and (type(delay) in [int, float]) and delay > 0:
            time.sleep(delay)
        if page_utils.is_link_text_selector(selector) or by == By.LINK_TEXT:
            if not self.is_link_text_visible(selector):
                # Handle a special case of links hidden in dropdowns
                self.click_link_text(selector, timeout=timeout)
                return
        if (
            page_utils.is_partial_link_text_selector(selector)
            or by == By.PARTIAL_LINK_TEXT
        ):
            if not self.is_partial_link_text_visible(selector):
                # Handle a special case of partial links hidden in dropdowns
                self.click_partial_link_text(selector, timeout=timeout)
                return
        if self.__is_shadow_selector(selector):
            self.__shadow_click(selector, timeout)
            return
        if self.browser == "safari":
            self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.022)
        element = page_actions.wait_for_element_visible(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )
        self.__demo_mode_highlight_if_active(original_selector, original_by)
        if scroll and not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        try:
            if (
                by == By.LINK_TEXT
                and (
                    self.browser == "ie" or self.browser == "safari"
                )
            ):
                self.__jquery_click(selector, by=by)
            else:
                href = None
                new_tab = False
                onclick = None
                try:
                    if self.headless and element.tag_name.lower() == "a":
                        # Handle a special case of opening a new tab (headless)
                        href = element.get_attribute("href").strip()
                        onclick = element.get_attribute("onclick")
                        target = element.get_attribute("target")
                        if target == "_blank":
                            new_tab = True
                        if new_tab and self.__looks_like_a_page_url(href):
                            if onclick:
                                try:
                                    self.execute_script(onclick)
                                except Exception:
                                    pass
                            current_window = self.driver.current_window_handle
                            self.open_new_window()
                            try:
                                self.open(href)
                            except Exception:
                                pass
                            self.switch_to_window(current_window)
                            return
                except Exception:
                    pass
                # Normal click
                element.click()
        except StaleElementReferenceException:
            self.wait_for_ready_state_complete()
            time.sleep(0.16)
            element = page_actions.wait_for_element_visible(
                self.driver,
                selector,
                by,
                timeout=timeout,
                original_selector=original_selector,
            )
            try:
                self.__scroll_to_element(element, selector, by)
            except Exception:
                pass
            if self.browser == "safari" and by == By.LINK_TEXT:
                self.__jquery_click(selector, by=by)
            else:
                element.click()
        except ENI_Exception:
            self.wait_for_ready_state_complete()
            time.sleep(0.1)
            element = page_actions.wait_for_element_visible(
                self.driver,
                selector,
                by,
                timeout=timeout,
                original_selector=original_selector,
            )
            href = None
            new_tab = False
            onclick = None
            try:
                if element.tag_name.lower() == "a":
                    # Handle a special case of opening a new tab (non-headless)
                    href = element.get_attribute("href").strip()
                    onclick = element.get_attribute("onclick")
                    target = element.get_attribute("target")
                    if target == "_blank":
                        new_tab = True
                    if new_tab and self.__looks_like_a_page_url(href):
                        if onclick:
                            try:
                                self.execute_script(onclick)
                            except Exception:
                                pass
                        current_window = self.driver.current_window_handle
                        self.open_new_window()
                        try:
                            self.open(href)
                        except Exception:
                            pass
                        self.switch_to_window(current_window)
                        return
            except Exception:
                pass
            self.__scroll_to_element(element, selector, by)
            if self.browser == "firefox" or self.browser == "safari":
                if by == By.LINK_TEXT or "contains(" in selector:
                    self.__jquery_click(selector, by=by)
                else:
                    self.__js_click(selector, by=by)
            else:
                element.click()
        except MoveTargetOutOfBoundsException:
            self.wait_for_ready_state_complete()
            try:
                self.__js_click(selector, by=by)
            except Exception:
                try:
                    self.__jquery_click(selector, by=by)
                except Exception:
                    # One more attempt to click on the element
                    element = page_actions.wait_for_element_visible(
                        self.driver,
                        selector,
                        by,
                        timeout=timeout,
                        original_selector=original_selector,
                    )
                    element.click()
        except WebDriverException as e:
            if (
                "cannot determine loading status" in e.msg
                or "unexpected command response" in e.msg
            ):
                pass  # Odd issue where the click did happen. Continue.
            else:
                self.wait_for_ready_state_complete()
                try:
                    self.__js_click(selector, by=by)
                except Exception:
                    try:
                        self.__jquery_click(selector, by=by)
                    except Exception:
                        # One more attempt to click on the element
                        element = page_actions.wait_for_element_visible(
                            self.driver,
                            selector,
                            by,
                            timeout=timeout,
                            original_selector=original_selector,
                        )
                        element.click()
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        elif (
            latest_window_count == pre_window_count - 1
            and latest_window_count > 0
        ):
            # If a click closes the active window,
            # switch to the last one if it exists.
            self.switch_to_window(-1)
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            try:
                self.wait_for_ready_state_complete()
            except Exception:
                pass
            if self.__needs_minimum_wait():
                time.sleep(0.05)
        else:
            # A smaller subset of self.wait_for_ready_state_complete()
            try:
                self.wait_for_angularjs(timeout=settings.MINI_TIMEOUT)
            except Exception:
                pass
            if self.__needs_minimum_wait():
                time.sleep(0.025)
                if self.undetectable:
                    time.sleep(0.025)
            try:
                if self.driver.current_url != pre_action_url:
                    self.__ad_block_as_needed()
                    self.__disable_beforeunload_as_needed()
                    if self.__needs_minimum_wait():
                        time.sleep(0.025)
                        if self.undetectable:
                            time.sleep(0.025)
            except Exception:
                try:
                    self.wait_for_ready_state_complete()
                except Exception:
                    pass
                if self.__needs_minimum_wait():
                    time.sleep(0.025)
                    if self.undetectable:
                        time.sleep(0.025)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        elif self.browser == "safari":
            self.wait_for_ready_state_complete()

    def slow_click(self, selector, by="css selector", timeout=None):
        """Similar to click(), but pauses for a brief moment before clicking.
        When used in combination with setting the user-agent, you can often
        bypass bot-detection by tricking websites into thinking that you're
        not a bot. (Useful on websites that block web automation tools.)
        To set the user-agent, use: ``--agent=AGENT``.
        Here's an example message from GitHub's bot-blocker:
        ``You have triggered an abuse detection mechanism...``
        """
        self.__check_scope()
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

    def double_click(self, selector, by="css selector", timeout=None):
        from selenium.webdriver.common.action_chains import ActionChains

        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        original_by = by
        selector, by = self.__recalculate_selector(selector, by)
        element = page_actions.wait_for_element_visible(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )
        self.__demo_mode_highlight_if_active(original_selector, original_by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.02)
        # Find the element one more time in case scrolling hid it
        element = page_actions.wait_for_element_visible(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )
        pre_action_url = self.driver.current_url
        try:
            if self.browser == "safari":
                # Jump to the "except" block where the other script should work
                raise Exception("This Exception will be caught.")
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
                targetElement1.dispatchEvent(clickEvent1);"""
                % css_selector
            )
            if ":contains\\(" not in css_selector:
                self.execute_script(double_click_script)
            else:
                double_click_script = (
                    """jQuery('%s').dblclick();""" % css_selector
                )
                self.safe_execute_script(double_click_script)
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        else:
            # A smaller subset of self.wait_for_ready_state_complete()
            self.wait_for_angularjs(timeout=settings.MINI_TIMEOUT)
            if self.driver.current_url != pre_action_url:
                self.__ad_block_as_needed()
                self.__disable_beforeunload_as_needed()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        elif self.__needs_minimum_wait():
            time.sleep(0.02)

    def click_chain(
        self, selectors_list, by="css selector", timeout=None, spacing=0
    ):
        """This method clicks on a list of elements in succession.
        @Params
        selectors_list - The list of selectors to click on.
        by - The type of selector to search by (Default: CSS_Selector).
        timeout - How long to wait for the selector to be visible.
        spacing - The amount of time to wait between clicks (in seconds).
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        for selector in selectors_list:
            self.click(selector, by=by, timeout=timeout)
            if spacing > 0:
                time.sleep(spacing)

    def update_text(
        self, selector, text, by="css selector", timeout=None, retry=False
    ):
        """This method updates an element's text field with new text.
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
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            self.__shadow_type(selector, text, timeout)
            return
        element = self.wait_for_element_clickable(
            selector, by=by, timeout=timeout
        )
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
            if self.__needs_minimum_wait():
                time.sleep(0.01)
        try:
            element.clear()  # May need https://stackoverflow.com/a/50691625
            backspaces = Keys.BACK_SPACE * 42  # Is the answer to everything
            element.send_keys(backspaces)  # In case autocomplete keeps text
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.16)
            element = self.wait_for_element_clickable(
                selector, by=by, timeout=timeout
            )
            try:
                element.clear()
            except Exception:
                pass  # Clearing the text field first might not be necessary
        except Exception:
            pass  # Clearing the text field first might not be necessary
        self.__demo_mode_pause_if_active(tiny=True)
        pre_action_url = self.driver.current_url
        text = self.__get_type_checked_text(text)
        try:
            if not text.endswith("\n"):
                element.send_keys(text)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
            else:
                element.send_keys(text[:-1])
                try:
                    element.send_keys(Keys.RETURN)
                except WebDriverException as e:
                    if (
                        "cannot determine loading status" in e.msg
                        or "unexpected command response" in e.msg
                    ):
                        pass  # Odd issue where the click did happen. Continue.
                    else:
                        raise e
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.16)
            element = self.wait_for_element_clickable(
                selector, by=by, timeout=timeout
            )
            element.clear()
            if not text.endswith("\n"):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
                try:
                    element.send_keys(Keys.RETURN)
                except WebDriverException as e:
                    if (
                        "cannot determine loading status" in e.msg
                        or "unexpected command response" in e.msg
                    ):
                        pass  # Odd issue where the click did happen. Continue.
                    else:
                        raise e
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
                    if self.__needs_minimum_wait():
                        time.sleep(0.01)
                        if self.undetectable:
                            time.sleep(0.015)
        if (
            retry
            and element.get_attribute("value") != text
            and not text.endswith("\n")
        ):
            logging.debug("update_text() is falling back to JavaScript!")
            self.set_value(selector, text, by=by)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def add_text(self, selector, text, by="css selector", timeout=None):
        """The more-reliable version of driver.send_keys()
        Similar to update_text(), but won't clear the text field first."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            self.__shadow_type(selector, text, timeout, clear_first=False)
            return
        if selector == "html" and text in ["\n", Keys.ENTER, Keys.RETURN]:
            # This is a shortcut for calling self.click_active_element().
            # Use after "\t" or Keys.TAB to cycle through elements first.
            self.click_active_element()
            return
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout
        )
        if (
            selector == "html" and text.count("\t") >= 1
            and text.count("\n") == 1 and text.endswith("\n")
            and text.replace("\t", "").replace("\n", "").replace(" ", "") == ""
        ):
            # Shortcut to send multiple tabs followed by click_active_element()
            self.wait_for_ready_state_complete()
            element.send_keys(Keys.TAB * text.count("\t"))
            self.click_active_element()
            return
        self.__demo_mode_highlight_if_active(selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.__scroll_to_element(element, selector, by)
        pre_action_url = self.driver.current_url
        text = self.__get_type_checked_text(text)
        try:
            if not text.endswith("\n"):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.16)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout
            )
            if not text.endswith("\n"):
                element.send_keys(text)
            else:
                element.send_keys(text[:-1])
                element.send_keys(Keys.RETURN)
                if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                    self.wait_for_ready_state_complete()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def type(
        self, selector, text, by="css selector", timeout=None, retry=False
    ):
        """Same as self.update_text()
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
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.update_text(selector, text, by=by, timeout=timeout, retry=retry)

    def send_keys(self, selector, text, by="css selector", timeout=None):
        """Same as self.add_text()
        Similar to update_text(), but won't clear the text field first."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.add_text(selector, text, by=by, timeout=timeout)

    def submit(self, selector, by="css selector"):
        """Alternative to self.driver.find_element_by_*(SELECTOR).submit()"""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        element.submit()
        self.__demo_mode_pause_if_active()

    def clear(self, selector, by="css selector", timeout=None):
        """This method clears an element's text field.
        A clear() is already included with most methods that type text,
        such as self.type(), self.update_text(), etc.
        Does not use Demo Mode highlights, mainly because we expect
        that some users will be calling an unnecessary clear() before
        calling a method that already includes clear() as part of it.
        In case websites trigger an autofill after clearing a field,
        add backspaces to make sure autofill doesn't undo the clear.
        @Params
        selector - the selector of the text field
        by - the type of selector to search by (Default: CSS Selector)
        timeout - how long to wait for the selector to be visible
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            self.__shadow_clear(selector, timeout)
            return
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout
        )
        self.scroll_to(selector, by=by, timeout=timeout)
        try:
            element.clear()
            backspaces = Keys.BACK_SPACE * 42  # Autofill Defense
            element.send_keys(backspaces)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.16)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout
            )
            element.clear()
            try:
                backspaces = Keys.BACK_SPACE * 42  # Autofill Defense
                element.send_keys(backspaces)
            except Exception:
                pass
        except Exception:
            element.clear()

    def focus(self, selector, by="css selector", timeout=None):
        """Make the current page focus on an interactable element.
        If the element is not interactable, only scrolls to it.
        The "tab" key is another way of setting the page focus."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout
        )
        self.scroll_to(selector, by=by, timeout=timeout)
        try:
            element.send_keys(Keys.NULL)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.12)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout
            )
            try:
                element.send_keys(Keys.NULL)
            except ENI_Exception:
                # Non-interactable element. Skip focus and continue.
                pass
        self.__demo_mode_pause_if_active()

    def refresh_page(self):
        self.__check_scope()
        self.__last_page_load_url = None
        js_utils.clear_out_console_logs(self.driver)
        self.driver.refresh()
        self.wait_for_ready_state_complete()

    def refresh(self):
        """The shorter version of self.refresh_page()"""
        self.refresh_page()

    def get_current_url(self):
        self.__check_scope()
        current_url = self.driver.current_url
        if "%" in current_url and python3:
            try:
                from urllib.parse import unquote

                current_url = unquote(current_url, errors="strict")
            except Exception:
                pass
        return current_url

    def get_origin(self):
        self.__check_scope()
        return self.execute_script("return window.location.origin;")

    def get_page_source(self):
        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait:
            time.sleep(0.02)
        return self.driver.page_source

    def get_page_title(self):
        self.wait_for_ready_state_complete()
        self.wait_for_element_present("title", timeout=settings.SMALL_TIMEOUT)
        time.sleep(0.03)
        return self.driver.title

    def get_title(self):
        """The shorter version of self.get_page_title()"""
        return self.get_page_title()

    def get_user_agent(self):
        self.__check_scope()
        self.__check_browser()
        user_agent = self.driver.execute_script("return navigator.userAgent;")
        return user_agent

    def get_locale_code(self):
        self.__check_scope()
        self.__check_browser()
        locale_code = self.driver.execute_script(
            "return navigator.language || navigator.languages[0];"
        )
        return locale_code

    def go_back(self):
        self.__check_scope()
        self.__last_page_load_url = None
        self.driver.back()
        if self.recorder_mode:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["go_bk", "", origin, time_stamp]
            self.__extra_actions.append(action)
        if self.browser == "safari":
            self.wait_for_ready_state_complete()
            self.driver.refresh()
        self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def go_forward(self):
        self.__check_scope()
        self.__last_page_load_url = None
        self.driver.forward()
        if self.recorder_mode:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["go_fw", "", origin, time_stamp]
            self.__extra_actions.append(action)
        self.wait_for_ready_state_complete()
        self.__demo_mode_pause_if_active()

    def open_start_page(self):
        """Navigates the current browser window to the start_page.
        You can set the start_page on the command-line in three ways:
        '--start_page=URL', '--start-page=URL', or '--url=URL'.
        If the start_page is not set, then "about:blank" will be used."""
        self.__check_scope()
        start_page = self.start_page
        if type(start_page) is str:
            start_page = start_page.strip()  # Remove extra whitespace
        if start_page and len(start_page) >= 4:
            if page_utils.is_valid_url(start_page):
                self.open(start_page)
            else:
                new_start_page = "https://" + start_page
                if page_utils.is_valid_url(new_start_page):
                    self.__dont_record_open = True
                    self.open(new_start_page)
                    self.__dont_record_open = False
                else:
                    logging.info('Invalid URL: "%s"!' % start_page)
                    if self.get_current_url() != "about:blank":
                        self.open("about:blank")
        else:
            if self.get_current_url() != "about:blank":
                self.open("about:blank")

    def open_if_not_url(self, url):
        """Opens the url in the browser if it's not the current url."""
        self.__check_scope()
        if self.driver.current_url != url:
            self.open(url)

    def is_element_present(self, selector, by="css selector"):
        self.wait_for_ready_state_complete()
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__is_shadow_element_present(selector)
        return page_actions.is_element_present(self.driver, selector, by)

    def is_element_visible(self, selector, by="css selector"):
        self.wait_for_ready_state_complete()
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__is_shadow_element_visible(selector)
        return page_actions.is_element_visible(self.driver, selector, by)

    def is_element_clickable(self, selector, by="css selector"):
        self.wait_for_ready_state_complete()
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__is_shadow_element_clickable(selector)
        return page_actions.is_element_clickable(self.driver, selector, by)

    def is_element_enabled(self, selector, by="css selector"):
        self.wait_for_ready_state_complete()
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__is_shadow_element_enabled(selector)
        return page_actions.is_element_enabled(self.driver, selector, by)

    def is_text_visible(self, text, selector="html", by="css selector"):
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__is_shadow_text_visible(text, selector)
        return page_actions.is_text_visible(
            self.driver, text, selector, by, self.browser
        )

    def is_attribute_present(
        self, selector, attribute, value=None, by="css selector"
    ):
        """Returns True if the element attribute/value is found.
        If the value is not specified, the attribute only needs to exist."""
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__is_shadow_attribute_present(
                selector, attribute, value
            )
        return page_actions.is_attribute_present(
            self.driver, selector, attribute, value, by
        )

    def is_link_text_visible(self, link_text):
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        return page_actions.is_element_visible(
            self.driver, link_text, by="link text"
        )

    def is_partial_link_text_visible(self, partial_link_text):
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        return page_actions.is_element_visible(
            self.driver, partial_link_text, by="partial link text"
        )

    def is_link_text_present(self, link_text):
        """Returns True if the link text appears in the HTML of the page.
        The element doesn't need to be visible,
        such as elements hidden inside a dropdown selection."""
        self.wait_for_ready_state_complete()
        soup = self.get_beautiful_soup()
        html_links = soup.find_all("a")
        for html_link in html_links:
            if html_link.text.strip() == link_text.strip():
                return True
        return False

    def is_partial_link_text_present(self, link_text):
        """Returns True if the partial link appears in the HTML of the page.
        The element doesn't need to be visible,
        such as elements hidden inside a dropdown selection."""
        self.wait_for_ready_state_complete()
        soup = self.get_beautiful_soup()
        html_links = soup.find_all("a")
        for html_link in html_links:
            if link_text.strip() in html_link.text.strip():
                return True
        return False

    def get_link_attribute(self, link_text, attribute, hard_fail=True):
        """Finds a link by link text and then returns the attribute's value.
        If the link text or attribute cannot be found, an exception will
        get raised if hard_fail is True (otherwise None is returned)."""
        self.wait_for_ready_state_complete()
        soup = self.get_beautiful_soup()
        html_links = soup.find_all("a")
        for html_link in html_links:
            if html_link.text.strip() == link_text.strip():
                if html_link.has_attr(attribute):
                    attribute_value = html_link.get(attribute)
                    return attribute_value
                if hard_fail:
                    raise Exception(
                        "Unable to find attribute {%s} from link text {%s}!"
                        % (attribute, link_text)
                    )
                else:
                    return None
        if hard_fail:
            raise Exception("Link text {%s} was not found!" % link_text)
        else:
            return None

    def get_link_text_attribute(self, link_text, attribute, hard_fail=True):
        """Same as self.get_link_attribute()
        Finds a link by link text and then returns the attribute's value.
        If the link text or attribute cannot be found, an exception will
        get raised if hard_fail is True (otherwise None is returned)."""
        return self.get_link_attribute(link_text, attribute, hard_fail)

    def get_partial_link_text_attribute(
        self, link_text, attribute, hard_fail=True
    ):
        """Finds a link by partial link text and then returns the attribute's
        value. If the partial link text or attribute cannot be found, an
        exception will get raised if hard_fail is True (otherwise None
        is returned)."""
        self.wait_for_ready_state_complete()
        soup = self.get_beautiful_soup()
        html_links = soup.find_all("a")
        for html_link in html_links:
            if link_text.strip() in html_link.text.strip():
                if html_link.has_attr(attribute):
                    attribute_value = html_link.get(attribute)
                    return attribute_value
                if hard_fail:
                    raise Exception(
                        "Unable to find attribute {%s} from "
                        "partial link text {%s}!" % (attribute, link_text)
                    )
                else:
                    return None
        if hard_fail:
            raise Exception(
                "Partial Link text {%s} was not found!" % link_text
            )
        else:
            return None

    def click_link_text(self, link_text, timeout=None):
        """This method clicks link text on a page."""
        # If using phantomjs, might need to extract and open the link directly
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        link_text = self.__get_type_checked_text(link_text)
        if self.browser == "phantomjs":
            if self.is_link_text_visible(link_text):
                element = self.wait_for_link_text_visible(
                    link_text, timeout=timeout
                )
                element.click()
                return
            self.open(self.__get_href_from_link_text(link_text))
            return
        if self.browser == "safari":
            if self.demo_mode:
                self.wait_for_link_text_present(link_text, timeout=timeout)
                try:
                    self.__jquery_slow_scroll_to(link_text, by="link text")
                except Exception:
                    element = self.wait_for_link_text_visible(
                        link_text, timeout=timeout
                    )
                    self.__slow_scroll_to_element(element)
                o_bs = ""  # original_box_shadow
                loops = settings.HIGHLIGHTS
                selector = self.convert_to_css_selector(
                    link_text, by="link text"
                )
                selector = self.__make_css_match_first_element_only(selector)
                try:
                    selector = re.escape(selector)
                    selector = self.__escape_quotes_if_needed(selector)
                    self.__highlight_with_jquery(selector, loops, o_bs)
                except Exception:
                    pass  # JQuery probably couldn't load. Skip highlighting.
            self.__jquery_click(link_text, by="link text")
            return
        if not self.is_link_text_present(link_text):
            self.wait_for_link_text_present(link_text, timeout=timeout)
        pre_action_url = self.get_current_url()
        try:
            element = self.wait_for_link_text_visible(link_text, timeout=0.2)
            self.__demo_mode_highlight_if_active(link_text, by="link text")
            try:
                element.click()
            except (
                StaleElementReferenceException,
                ENI_Exception,
                ECI_Exception,
            ):
                self.wait_for_ready_state_complete()
                time.sleep(0.16)
                element = self.wait_for_link_text_visible(
                    link_text, timeout=timeout
                )
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
                    if href.startswith("/") or page_utils.is_valid_url(href):
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
                        link_text, link_css
                    )
            if not success:
                element = self.wait_for_link_text_visible(
                    link_text, timeout=settings.MINI_TIMEOUT
                )
                element.click()
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        elif (
            latest_window_count == pre_window_count - 1
            and latest_window_count > 0
        ):
            # If a click closes the active window,
            # switch to the last one if it exists.
            self.switch_to_window(-1)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            try:
                self.wait_for_ready_state_complete()
            except Exception:
                pass
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def click_partial_link_text(self, partial_link_text, timeout=None):
        """This method clicks the partial link text on a page."""
        # If using phantomjs, might need to extract and open the link directly
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        partial_link_text = self.__get_type_checked_text(partial_link_text)
        if self.browser == "phantomjs":
            if self.is_partial_link_text_visible(partial_link_text):
                element = self.wait_for_partial_link_text(partial_link_text)
                element.click()
                return
            soup = self.get_beautiful_soup()
            html_links = soup.fetch("a")
            for html_link in html_links:
                if partial_link_text in html_link.text:
                    for html_attribute in html_link.attrs:
                        if html_attribute[0] == "href":
                            href = html_attribute[1]
                            if href.startswith("//"):
                                link = "http:" + href
                            elif href.startswith("/"):
                                url = self.driver.current_url
                                domain_url = self.get_domain_url(url)
                                link = domain_url + href
                            else:
                                link = href
                            self.open(link)
                            return
                    raise Exception(
                        "Could not parse link from partial link_text "
                        "{%s}" % partial_link_text
                    )
            raise Exception(
                "Partial link text {%s} was not found!" % partial_link_text
            )
        if not self.is_partial_link_text_present(partial_link_text):
            self.wait_for_partial_link_text_present(
                partial_link_text, timeout=timeout
            )
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        try:
            element = self.wait_for_partial_link_text(
                partial_link_text, timeout=0.2
            )
            self.__demo_mode_highlight_if_active(
                partial_link_text, by="link text"
            )
            try:
                element.click()
            except (
                StaleElementReferenceException,
                ENI_Exception,
                ECI_Exception,
            ):
                self.wait_for_ready_state_complete()
                time.sleep(0.16)
                element = self.wait_for_partial_link_text(
                    partial_link_text, timeout=timeout
                )
                element.click()
        except Exception:
            found_css = False
            text_id = self.get_partial_link_text_attribute(
                partial_link_text, "id", False
            )
            if text_id:
                link_css = '[id="%s"]' % partial_link_text
                found_css = True
            if not found_css:
                href = self.__get_href_from_partial_link_text(
                    partial_link_text, False
                )
                if href:
                    if href.startswith("/") or page_utils.is_valid_url(href):
                        link_css = '[href="%s"]' % href
                        found_css = True
            if not found_css:
                ngclick = self.get_partial_link_text_attribute(
                    partial_link_text, "ng-click", False
                )
                if ngclick:
                    link_css = '[ng-click="%s"]' % ngclick
                    found_css = True
            if not found_css:
                onclick = self.get_partial_link_text_attribute(
                    partial_link_text, "onclick", False
                )
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
                        partial_link_text, link_css
                    )
            if not success:
                element = self.wait_for_partial_link_text(
                    partial_link_text, timeout=settings.MINI_TIMEOUT
                )
                element.click()
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        elif (
            latest_window_count == pre_window_count - 1
            and latest_window_count > 0
        ):
            # If a click closes the active window,
            # switch to the last one if it exists.
            self.switch_to_window(-1)
        if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
            try:
                self.wait_for_ready_state_complete()
            except Exception:
                pass
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def get_text(self, selector, by="css selector", timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__get_shadow_text(selector, timeout)
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout
        )
        try:
            element_text = element.text
            if self.browser == "safari":
                if element.tag_name.lower() in ["input", "textarea"]:
                    element_text = element.get_attribute("value")
                else:
                    element_text = element.get_attribute("innerText")
            elif element.tag_name.lower() in ["input", "textarea"]:
                element_text = element.get_property("value")
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.14)
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout
            )
            element_text = element.text
            if self.browser == "safari":
                if element.tag_name.lower() in ["input", "textarea"]:
                    element_text = element.get_attribute("value")
                else:
                    element_text = element.get_attribute("innerText")
            elif element.tag_name.lower() in ["input", "textarea"]:
                element_text = element.get_property("value")
        return element_text

    def get_attribute(
        self,
        selector,
        attribute,
        by="css selector",
        timeout=None,
        hard_fail=True,
    ):
        """This method uses JavaScript to get the value of an attribute.
        If the attribute doesn't exist or isn't found, an exception will
        get raised if hard_fail is True (otherwise None is returned)."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        if self.__is_shadow_selector(selector):
            return self.__get_shadow_attribute(
                selector, attribute, timeout=timeout
            )
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        try:
            attribute_value = element.get_attribute(attribute)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.14)
            element = page_actions.wait_for_element_present(
                self.driver, selector, by, timeout
            )
            attribute_value = element.get_attribute(attribute)
        if attribute_value is not None:
            return attribute_value
        else:
            if hard_fail:
                raise Exception(
                    "Element {%s} has no attribute {%s}!"
                    % (selector, attribute)
                )
            else:
                return None

    def set_attribute(
        self,
        selector,
        attribute,
        value,
        by="css selector",
        timeout=None,
        scroll=False,
    ):
        """This method uses JavaScript to set/update an attribute.
        Only the first matching selector from querySelector() is used."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if scroll and self.is_element_visible(selector, by=by):
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
        script = (
            """document.querySelector('%s').setAttribute('%s','%s');"""
            % (css_selector, attribute, value)
        )
        self.execute_script(script)

    def set_attributes(self, selector, attribute, value, by="css selector"):
        """This method uses JavaScript to set/update a common attribute.
        All matching selectors from querySelectorAll() are used.
        Example => (Make all links on a website redirect to Google):
        self.set_attributes("a", "href", "https://google.com")"""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        attribute = re.escape(attribute)
        attribute = self.__escape_quotes_if_needed(attribute)
        value = re.escape(value)
        value = self.__escape_quotes_if_needed(value)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = """var $elements = document.querySelectorAll('%s');
                  var index = 0, length = $elements.length;
                  for(; index < length; index++){
                  $elements[index].setAttribute('%s','%s');}""" % (
            css_selector,
            attribute,
            value,
        )
        try:
            self.execute_script(script)
        except Exception:
            pass

    def set_attribute_all(self, selector, attribute, value, by="css selector"):
        """Same as set_attributes(), but using querySelectorAll naming scheme.
        This method uses JavaScript to set/update a common attribute.
        All matching selectors from querySelectorAll() are used.
        Example => (Make all links on a website redirect to Google):
        self.set_attribute_all("a", "href", "https://google.com")"""
        self.set_attributes(selector, attribute, value, by=by)

    def remove_attribute(
        self, selector, attribute, by="css selector", timeout=None
    ):
        """This method uses JavaScript to remove an attribute.
        Only the first matching selector from querySelector() is used."""
        self.__check_scope()
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
        script = """document.querySelector('%s').removeAttribute('%s');""" % (
            css_selector,
            attribute,
        )
        self.execute_script(script)

    def remove_attributes(self, selector, attribute, by="css selector"):
        """This method uses JavaScript to remove a common attribute.
        All matching selectors from querySelectorAll() are used."""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        attribute = re.escape(attribute)
        attribute = self.__escape_quotes_if_needed(attribute)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = """var $elements = document.querySelectorAll('%s');
                  var index = 0, length = $elements.length;
                  for(; index < length; index++){
                  $elements[index].removeAttribute('%s');}""" % (
            css_selector,
            attribute,
        )
        try:
            self.execute_script(script)
        except Exception:
            pass

    def get_property(
        self, selector, property, by="css selector", timeout=None
    ):
        """Returns the property value of an element.
        This is not the same as self.get_property_value(), which returns
        the value of an element's computed style using a different algorithm.
        If no result is found, an empty string (instead of None) is returned.
        Example:
            html_text = self.get_property(SELECTOR, "textContent")
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        time.sleep(0.01)
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        try:
            property_value = element.get_property(property)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.14)
            element = page_actions.wait_for_element_present(
                self.driver, selector, by, timeout
            )
            property_value = element.get_property(property)
        if not property_value:
            return ""
        return property_value

    def get_text_content(self, selector, by="css selector", timeout=None):
        """Returns the text that appears in the HTML for an element.
        This is different from "self.get_text(selector, by="css selector")"
        because that only returns the visible text on a page for an element,
        rather than the HTML text that's being returned from this method."""
        self.__check_scope()
        return self.get_property(
            selector, property="textContent", by=by, timeout=timeout
        )

    def get_property_value(
        self, selector, property, by="css selector", timeout=None
    ):
        """Returns the property value of a page element's computed style.
        Example:
            opacity = self.get_property_value("html body a", "opacity")
            self.assertTrue(float(opacity) > 0, "Element not visible!")"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't run action if can't convert to CSS_Selector for JavaScript
            raise Exception(
                "Exception: Could not convert {%s}(by=%s) to CSS_SELECTOR!"
                % (selector, by)
            )
        selector = re.escape(selector)
        selector = self.__escape_quotes_if_needed(selector)
        script = """var $elm = document.querySelector('%s');
                  $val = window.getComputedStyle($elm).getPropertyValue('%s');
                  return $val;""" % (
            selector,
            property,
        )
        value = self.execute_script(script)
        if value is not None:
            return value
        else:
            return ""  # Return an empty string if the property doesn't exist

    def get_image_url(self, selector, by="css selector", timeout=None):
        """Extracts the URL from an image element on the page."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.get_attribute(
            selector, attribute="src", by=by, timeout=timeout
        )

    def find_elements(self, selector, by="css selector", limit=0):
        """Returns a list of matching WebElements.
        Elements could be either hidden or visible on the page.
        If "limit" is set and > 0, will only return that many elements."""
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        time.sleep(0.05)
        elements = self.driver.find_elements(by=by, value=selector)
        if limit and limit > 0 and len(elements) > limit:
            elements = elements[:limit]
        return elements

    def find_visible_elements(self, selector, by="css selector", limit=0):
        """Returns a list of matching WebElements that are visible.
        If "limit" is set and > 0, will only return that many elements."""
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        time.sleep(0.05)
        v_elems = page_actions.find_visible_elements(self.driver, selector, by)
        if limit and limit > 0 and len(v_elems) > limit:
            v_elems = v_elems[:limit]
        return v_elems

    def click_visible_elements(
        self, selector, by="css selector", limit=0, timeout=None
    ):
        """Finds all matching page elements and clicks visible ones in order.
        If a click reloads or opens a new page, the clicking will stop.
        If no matching elements appear, an Exception will be raised.
        If "limit" is set and > 0, will only click that many elements.
        Also clicks elements that become visible from previous clicks.
        Works best for actions such as clicking all checkboxes on a page.
        Example:  self.click_visible_elements('input[type="checkbox"]')"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        elements = self.find_elements(selector, by=by)
        if self.browser == "safari":
            if not limit:
                limit = 0
            num_elements = len(elements)
            if num_elements == 0:
                raise Exception(
                    "No matching elements found for selector {%s}!" % selector
                )
            elif num_elements < limit or limit == 0:
                limit = num_elements
            selector, by = self.__recalculate_selector(selector, by)
            css_selector = self.convert_to_css_selector(selector, by=by)
            last_css_chunk = css_selector.split(" ")[-1]
            if ":" in last_css_chunk:
                self.__js_click_all(css_selector)
                self.wait_for_ready_state_complete()
                return
            else:
                for i in range(1, limit + 1):
                    new_selector = css_selector + ":nth-of-type(%s)" % str(i)
                    if self.is_element_visible(new_selector):
                        self.__js_click(new_selector)
                        self.wait_for_ready_state_complete()
                return
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
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
                time.sleep(0.12)
                try:
                    if element.is_displayed():
                        self.__scroll_to_element(element)
                        element.click()
                        click_count += 1
                        self.wait_for_ready_state_complete()
                except (StaleElementReferenceException, ENI_Exception):
                    latest_window_count = len(self.driver.window_handles)
                    if (
                        latest_window_count > pre_window_count
                        and (
                            self.recorder_mode
                            or (
                                settings.SWITCH_TO_NEW_TABS_ON_CLICK
                                and self.driver.current_url == pre_action_url
                            )
                        )
                    ):
                        self.__switch_to_newest_window_if_not_blank()
                    return  # Probably on new page / Elements are all stale
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()

    def click_nth_visible_element(
        self, selector, number, by="css selector", timeout=None
    ):
        """Finds all matching page elements and clicks the nth visible one.
        Example:  self.click_nth_visible_element('[type="checkbox"]', 5)
                    (Clicks the 5th visible checkbox on the page.)"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        elements = self.find_visible_elements(selector, by=by)
        if len(elements) < number:
            raise Exception(
                "Not enough matching {%s} elements of type {%s} to "
                "click number %s!" % (selector, by, number)
            )
        number = number - 1
        if number < 0:
            number = 0
        element = elements[number]
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        try:
            self.__scroll_to_element(element)
            element.click()
        except (StaleElementReferenceException, ENI_Exception, ECI_Exception):
            time.sleep(0.12)
            self.wait_for_ready_state_complete()
            self.wait_for_element_present(selector, by=by, timeout=timeout)
            elements = self.find_visible_elements(selector, by=by)
            if len(elements) < number:
                raise Exception(
                    "Not enough matching {%s} elements of type {%s} to "
                    "click number %s!" % (selector, by, number)
                )
            number = number - 1
            if number < 0:
                number = 0
            element = elements[number]
            element.click()
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()

    def click_if_visible(self, selector, by="css selector", timeout=0):
        """If the page selector exists and is visible, clicks on the element.
        This method only clicks on the first matching element found.
        Use click_visible_elements() to click all matching elements.
        If a "timeout" is provided, waits that long for the element
        to appear before giving up and returning without a click()."""
        self.wait_for_ready_state_complete()
        if self.is_element_visible(selector, by=by):
            self.click(selector, by=by)
        elif timeout > 0:
            try:
                self.wait_for_element_visible(
                    selector, by=by, timeout=timeout
                )
            except Exception:
                pass
            if self.is_element_visible(selector, by=by):
                self.click(selector, by=by)

    def click_active_element(self):
        self.wait_for_ready_state_complete()
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        self.execute_script("document.activeElement.click();")
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        else:
            # A smaller subset of self.wait_for_ready_state_complete()
            self.wait_for_angularjs(timeout=settings.MINI_TIMEOUT)
            if self.driver.current_url != pre_action_url:
                self.__ad_block_as_needed()
                self.__disable_beforeunload_as_needed()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def click_with_offset(
        self,
        selector,
        x,
        y,
        by="css selector",
        mark=None,
        timeout=None,
        center=None,
    ):
        """
        Click an element at an {X,Y}-offset location.
        {0,0} is the top-left corner of the element.
        If center==True, {0,0} becomes the center of the element.
        If mark==True, will draw a dot at location. (Useful for debugging)
        In Demo Mode, mark becomes True unless set to False. (Default: None)
        """
        self.__check_scope()
        self.__click_with_offset(
            selector,
            x,
            y,
            by=by,
            double=False,
            mark=mark,
            timeout=timeout,
            center=center,
        )

    def double_click_with_offset(
        self,
        selector,
        x,
        y,
        by="css selector",
        mark=None,
        timeout=None,
        center=None,
    ):
        """
        Double click an element at an {X,Y}-offset location.
        {0,0} is the top-left corner of the element.
        If center==True, {0,0} becomes the center of the element.
        If mark==True, will draw a dot at location. (Useful for debugging)
        In Demo Mode, mark becomes True unless set to False. (Default: None)
        """
        self.__check_scope()
        self.__click_with_offset(
            selector,
            x,
            y,
            by=by,
            double=True,
            mark=mark,
            timeout=timeout,
            center=center,
        )

    def is_checked(self, selector, by="css selector", timeout=None):
        """Determines if a checkbox or a radio button element is checked.
        Returns True if the element is checked.
        Returns False if the element is not checked.
        If the element is not present on the page, raises an exception.
        If the element is not a checkbox or radio, raises an exception."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        kind = self.get_attribute(selector, "type", by=by, timeout=timeout)
        if kind != "checkbox" and kind != "radio":
            raise Exception("Expecting a checkbox or a radio button element!")
        is_checked = self.get_attribute(
            selector, "checked", by=by, timeout=timeout, hard_fail=False
        )
        if is_checked:
            return True
        else:  # (NoneType)
            return False

    def is_selected(self, selector, by="css selector", timeout=None):
        """Same as is_checked()"""
        return self.is_checked(selector, by=by, timeout=timeout)

    def check_if_unchecked(self, selector, by="css selector"):
        """If a checkbox or radio button is not checked, will check it."""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        if not self.is_checked(selector, by=by):
            if self.is_element_visible(selector, by=by):
                self.click(selector, by=by)
            else:
                selector = self.convert_to_css_selector(selector, by=by)
                self.__dont_record_js_click = True
                self.js_click(selector, by="css selector")
                self.__dont_record_js_click = False

    def select_if_unselected(self, selector, by="css selector"):
        """Same as check_if_unchecked()"""
        self.check_if_unchecked(selector, by=by)

    def uncheck_if_checked(self, selector, by="css selector"):
        """If a checkbox is checked, will uncheck it."""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_checked(selector, by=by):
            if self.is_element_visible(selector, by=by):
                self.click(selector, by=by)
            else:
                selector = self.convert_to_css_selector(selector, by=by)
                self.__dont_record_js_click = True
                self.js_click(selector, by="css selector")
                self.__dont_record_js_click = False

    def unselect_if_selected(self, selector, by="css selector"):
        """Same as uncheck_if_checked()"""
        self.uncheck_if_checked(selector, by=by)

    def is_element_in_an_iframe(self, selector, by="css selector"):
        """Returns True if the selector's element is located in an iframe.
        Otherwise returns False."""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_element_present(selector, by=by):
            return False
        soup = self.get_beautiful_soup()
        iframe_list = soup.select("iframe")
        for iframe in iframe_list:
            iframe_identifier = None
            if iframe.has_attr("name") and len(iframe["name"]) > 0:
                iframe_identifier = iframe["name"]
            elif iframe.has_attr("id") and len(iframe["id"]) > 0:
                iframe_identifier = iframe["id"]
            elif iframe.has_attr("class") and len(iframe["class"]) > 0:
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

    def switch_to_frame_of_element(self, selector, by="css selector"):
        """Set driver control to the iframe containing element (assuming the
        element is in a single-nested iframe) and returns the iframe name.
        If element is not in an iframe, returns None, and nothing happens.
        May not work if multiple iframes are nested within each other."""
        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.02)
        selector, by = self.__recalculate_selector(selector, by)
        if self.is_element_present(selector, by=by):
            return None
        soup = self.get_beautiful_soup()
        iframe_list = soup.select("iframe")
        for iframe in iframe_list:
            iframe_identifier = None
            if iframe.has_attr("name") and len(iframe["name"]) > 0:
                iframe_identifier = iframe["name"]
            elif iframe.has_attr("id") and len(iframe["id"]) > 0:
                iframe_identifier = iframe["id"]
            elif iframe.has_attr("class") and len(iframe["class"]) > 0:
                iframe_class = " ".join(iframe["class"])
                iframe_identifier = '[class="%s"]' % iframe_class
            else:
                continue
            try:
                self.switch_to_frame(iframe_identifier, timeout=1)
                if self.__needs_minimum_wait():
                    time.sleep(0.02)
                if self.is_element_present(selector, by=by):
                    return iframe_identifier
            except Exception:
                pass
            self.switch_to_default_content()
            if self.__needs_minimum_wait():
                time.sleep(0.02)
        try:
            self.switch_to_frame(selector, timeout=1)
            return selector
        except Exception:
            if self.is_element_present(selector, by=by):
                return ""
            raise Exception(
                "Could not switch to iframe containing "
                "element {%s}!" % selector
            )

    def hover_on_element(self, selector, by="css selector"):
        self.__check_scope()
        original_selector = selector
        original_by = by
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_visible(
            original_selector, by=original_by, timeout=settings.SMALL_TIMEOUT
        )
        self.__demo_mode_highlight_if_active(original_selector, original_by)
        self.scroll_to(selector, by=by)
        time.sleep(0.05)  # Settle down from scrolling before hovering
        if self.browser != "chrome":
            return page_actions.hover_on_element(self.driver, selector, by)
        # Using Chrome
        # (Pure hover actions won't work on early chromedriver versions)
        try:
            return page_actions.hover_on_element(self.driver, selector, by)
        except WebDriverException as e:
            driver_capabilities = self.driver.capabilities
            if "version" in driver_capabilities:
                chrome_version = driver_capabilities["version"]
            else:
                chrome_version = driver_capabilities["browserVersion"]
            major_chrome_version = chrome_version.split(".")[0]
            chrome_dict = self.driver.capabilities["chrome"]
            chromedriver_version = chrome_dict["chromedriverVersion"]
            chromedriver_version = chromedriver_version.split(" ")[0]
            major_chromedriver_version = chromedriver_version.split(".")[0]
            install_sb = (
                "seleniumbase get chromedriver %s" % major_chrome_version
            )
            if int(major_chromedriver_version) < int(major_chrome_version):
                # Upgrading the driver is required for performing hover actions
                message = (
                    "You need a newer version of\n"
                    "chromedriver to perform hover actions!\n"
                    "Your version of chromedriver is: %s\n"
                    "And your version of Chrome is: %s\n"
                    "You can fix this issue by running:\n>>> %s\n"
                    % (chromedriver_version, chrome_version, install_sb)
                )
                raise Exception(message)
            else:
                raise Exception(e)

    def hover_and_click(
        self,
        hover_selector,
        click_selector,
        hover_by="css selector",
        click_by="css selector",
        timeout=None,
    ):
        """When you want to hover over an element or dropdown menu,
        and then click an element that appears after that."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = hover_selector
        original_by = hover_by
        hover_selector, hover_by = self.__recalculate_selector(
            hover_selector, hover_by
        )
        original_click_selector = click_selector
        click_selector, click_by = self.__recalculate_selector(
            click_selector, click_by
        )
        dropdown_element = self.wait_for_element_visible(
            original_selector, by=original_by, timeout=timeout
        )
        self.__demo_mode_highlight_if_active(original_selector, original_by)
        self.scroll_to(hover_selector, by=hover_by)
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        if hover_by == By.XPATH:
                            hover_selector = original_selector
                        if click_by == By.XPATH:
                            click_selector = original_click_selector
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        the_selectors = [hover_selector, click_selector]
                        action = ["ho_cl", the_selectors, origin, time_stamp]
                        self.__extra_actions.append(action)
        outdated_driver = False
        element = None
        try:
            if self.mobile_emulator:
                # On mobile, click to hover the element
                dropdown_element.click()
            else:
                page_actions.hover_element(self.driver, dropdown_element)
        except Exception:
            outdated_driver = True
            element = self.wait_for_element_present(
                click_selector, click_by, timeout
            )
            if click_by == By.LINK_TEXT:
                self.open(self.__get_href_from_link_text(click_selector))
            elif click_by == By.PARTIAL_LINK_TEXT:
                self.open(
                    self.__get_href_from_partial_link_text(click_selector)
                )
            else:
                self.__dont_record_js_click = True
                self.js_click(click_selector, by=click_by)
                self.__dont_record_js_click = False
        if outdated_driver:
            pass  # Already did the click workaround
        elif self.mobile_emulator:
            self.click(click_selector, by=click_by)
        elif not outdated_driver:
            element = page_actions.hover_and_click(
                self.driver,
                hover_selector,
                click_selector,
                hover_by,
                click_by,
                timeout,
            )
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        elif self.browser == "safari":
            # Release the hover by hovering elsewhere
            try:
                page_actions.hover_on_element(self.driver, "body")
            except Exception:
                pass
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        return element

    def hover_and_double_click(
        self,
        hover_selector,
        click_selector,
        hover_by="css selector",
        click_by="css selector",
        timeout=None,
    ):
        """When you want to hover over an element or dropdown menu,
        and then double-click an element that appears after that."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = hover_selector
        original_by = hover_by
        hover_selector, hover_by = self.__recalculate_selector(
            hover_selector, hover_by
        )
        hover_selector = self.convert_to_css_selector(hover_selector, hover_by)
        hover_by = By.CSS_SELECTOR
        click_selector, click_by = self.__recalculate_selector(
            click_selector, click_by
        )
        dropdown_element = self.wait_for_element_visible(
            original_selector, by=original_by, timeout=timeout
        )
        self.__demo_mode_highlight_if_active(original_selector, original_by)
        self.scroll_to(hover_selector, by=hover_by)
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        outdated_driver = False
        element = None
        try:
            page_actions.hover_element(self.driver, dropdown_element)
        except Exception:
            outdated_driver = True
            element = self.wait_for_element_present(
                click_selector, click_by, timeout
            )
            if click_by == By.LINK_TEXT:
                self.open(self.__get_href_from_link_text(click_selector))
            elif click_by == By.PARTIAL_LINK_TEXT:
                self.open(
                    self.__get_href_from_partial_link_text(click_selector)
                )
            else:
                self.__dont_record_js_click = True
                self.js_click(click_selector, click_by)
                self.__dont_record_js_click = False
        if not outdated_driver:
            element = page_actions.hover_element_and_double_click(
                self.driver,
                dropdown_element,
                click_selector,
                click_by="css selector",
                timeout=timeout,
            )
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        return element

    def drag_and_drop(
        self,
        drag_selector,
        drop_selector,
        drag_by="css selector",
        drop_by="css selector",
        timeout=None,
        jquery=False,
    ):
        """Drag and drop an element from one selector to another."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        drag_selector, drag_by = self.__recalculate_selector(
            drag_selector, drag_by
        )
        drop_selector, drop_by = self.__recalculate_selector(
            drop_selector, drop_by
        )
        drag_element = self.wait_for_element_clickable(
            drag_selector, by=drag_by, timeout=timeout
        )
        self.__demo_mode_highlight_if_active(drag_selector, drag_by)
        drop_element = self.wait_for_element_visible(
            drop_selector, by=drop_by, timeout=timeout
        )
        self.__demo_mode_highlight_if_active(drop_selector, drop_by)
        self.scroll_to(drop_selector, by=drop_by)
        drag_selector = self.convert_to_css_selector(drag_selector, drag_by)
        drop_selector = self.convert_to_css_selector(drop_selector, drop_by)
        if not jquery:
            drag_and_drop_script = js_utils.get_js_drag_and_drop_script()
            self.execute_script(
                drag_and_drop_script, drag_element, drop_element, 0, 0, 1, None
            )
        else:
            drag_and_drop_script = js_utils.get_drag_and_drop_script()
            self.safe_execute_script(
                drag_and_drop_script
                + (
                    "$('%s').simulateDragDrop("
                    "{dropTarget: "
                    "'%s'});" % (drag_selector, drop_selector)
                )
            )
        if self.demo_mode:
            self.__demo_mode_pause_if_active()
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        return drag_element

    def drag_and_drop_with_offset(
        self, selector, x, y, by="css selector", timeout=None
    ):
        """Drag and drop an element to an {X,Y}-offset location."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        element = self.wait_for_element_visible(css_selector, timeout=timeout)
        self.__demo_mode_highlight_if_active(css_selector, By.CSS_SELECTOR)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = js_utils.get_drag_and_drop_with_offset_script(
            css_selector, x, y
        )
        self.execute_script(script)
        if self.demo_mode:
            self.__demo_mode_pause_if_active()
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()
        return element

    def __select_option(
        self,
        dropdown_selector,
        option,
        dropdown_by="css selector",
        option_by="text",
        timeout=None,
    ):
        """Selects an HTML <select> option by specification.
        Option specifications are by "text", "index", or "value".
        Defaults to "text" if option_by is unspecified or unknown."""
        from selenium.webdriver.support.ui import Select

        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        dropdown_selector, dropdown_by = self.__recalculate_selector(
            dropdown_selector, dropdown_by
        )
        self.wait_for_ready_state_complete()
        element = self.wait_for_element_present(
            dropdown_selector, by=dropdown_by, timeout=timeout
        )
        try:
            element = self.wait_for_element_clickable(
                dropdown_selector, by=dropdown_by, timeout=1.2
            )
        except Exception:
            self.wait_for_ready_state_complete()
        if self.is_element_visible(dropdown_selector, by=dropdown_by):
            self.__demo_mode_highlight_if_active(
                dropdown_selector, dropdown_by
            )
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        try:
            if option_by == "index":
                Select(element).select_by_index(option)
            elif option_by == "value":
                Select(element).select_by_value(option)
            else:
                Select(element).select_by_visible_text(option)
            time.sleep(0.05)
            self.wait_for_ready_state_complete()
        except Exception:
            time.sleep(0.25)
            self.wait_for_ready_state_complete()
            element = self.wait_for_element_present(
                dropdown_selector, by=dropdown_by, timeout=timeout
            )
            try:
                element = self.wait_for_element_clickable(
                    dropdown_selector, by=dropdown_by, timeout=1.2
                )
            except Exception:
                self.wait_for_ready_state_complete()
            if option_by == "index":
                Select(element).select_by_index(option)
            elif option_by == "value":
                Select(element).select_by_value(option)
            else:
                Select(element).select_by_visible_text(option)
            time.sleep(0.05)
            self.wait_for_ready_state_complete()
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        else:
            # A smaller subset of self.wait_for_ready_state_complete()
            self.wait_for_angularjs(timeout=settings.MINI_TIMEOUT)
            if self.driver.current_url != pre_action_url:
                self.__ad_block_as_needed()
                self.__disable_beforeunload_as_needed()
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def select_option_by_text(
        self,
        dropdown_selector,
        option,
        dropdown_by="css selector",
        timeout=None,
    ):
        """Selects an HTML <select> option by option text.
        @Params
        dropdown_selector - the <select> selector.
        option - the text of the option.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__select_option(
            dropdown_selector,
            option,
            dropdown_by=dropdown_by,
            option_by="text",
            timeout=timeout,
        )

    def select_option_by_index(
        self,
        dropdown_selector,
        option,
        dropdown_by="css selector",
        timeout=None,
    ):
        """Selects an HTML <select> option by option index.
        @Params
        dropdown_selector - the <select> selector.
        option - the index number of the option.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__select_option(
            dropdown_selector,
            option,
            dropdown_by=dropdown_by,
            option_by="index",
            timeout=timeout,
        )

    def select_option_by_value(
        self,
        dropdown_selector,
        option,
        dropdown_by="css selector",
        timeout=None,
    ):
        """Selects an HTML <select> option by option value.
        @Params
        dropdown_selector - the <select> selector.
        option - the value property of the option.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__select_option(
            dropdown_selector,
            option,
            dropdown_by=dropdown_by,
            option_by="value",
            timeout=timeout,
        )

    def get_select_options(
        self,
        dropdown_selector,
        attribute="text",
        by="css selector",
        timeout=None,
    ):
        """Returns a list of select options as attribute text (configurable).
        @Params
        dropdown_selector - The selector of the "select" element.
        attribute - Choose from "text", "index", "value", or None (elements).
        by - The "by" of the "select" selector to use. Default: "css selector".
        timeout - Time to wait for "select". If None: settings.SMALL_TIMEOUT.
        """
        self.wait_for_ready_state_complete()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector = dropdown_selector
        allowed_attributes = ["text", "index", "value", None]
        if attribute not in allowed_attributes:
            raise Exception("The attribute must be in %s" % allowed_attributes)
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element(selector, by=by, timeout=timeout)
        if element.tag_name.lower() != "select":
            raise Exception(
                'Element tag_name for get_select_options(selector) must be a '
                '"select"! Actual tag_name found was: "%s"'
                % element.tag_name.lower()
            )
        if by != "css selector":
            selector = self.convert_to_css_selector(selector, by=by)
        option_selector = selector + " option"
        option_elements = self.find_elements(option_selector)
        if not attribute:
            return option_elements
        elif attribute == "text":
            return [e.text for e in option_elements]
        else:
            return [e.get_attribute(attribute) for e in option_elements]

    def load_html_string(self, html_string, new_page=True):
        """Loads an HTML string into the web browser.
        If new_page==True, the page will switch to: "data:text/html,"
        If new_page==False, will load HTML into the current page."""
        self.wait_for_ready_state_complete()
        new_lines = []
        lines = html_string.split("\n")
        for line in lines:
            if not line.strip().startswith("//"):
                new_lines.append(line)
        html_string = "\n".join(new_lines)
        soup = self.get_beautiful_soup(html_string)
        found_base = False
        links = soup.findAll("link")
        href = None
        for link in links:
            if link.get("rel") == ["canonical"] and link.get("href"):
                found_base = True
                href = link.get("href")
                href = self.get_domain_url(href)
        if (
            found_base
            and html_string.count("<head>") == 1
            and html_string.count("<base") == 0
        ):
            html_string = html_string.replace(
                "<head>", '<head><base href="%s">' % href
            )
        elif not found_base:
            bases = soup.findAll("base")
            for base in bases:
                if base.get("href"):
                    href = base.get("href")
        if href:
            html_string = html_string.replace('base: "."', 'base: "%s"' % href)

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
            html_head = html_head.replace("\\ ", " ")
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
            html_body = html_body.replace("\\ ", " ")
        html_string = re.escape(html_string)
        html_string = self.__escape_quotes_if_needed(html_string)
        html_string = html_string.replace("\\ ", " ")

        if new_page:
            self.open("data:text/html,<head></head><body></body>")
        inner_head = """document.getElementsByTagName("head")[0].innerHTML"""
        inner_body = """document.getElementsByTagName("body")[0].innerHTML"""
        try:
            self.wait_for_element_present("body", timeout=1)
        except Exception:
            pass
        if not found_body:
            self.execute_script('''%s = \"%s\"''' % (inner_body, html_string))
        elif found_body and not found_head:
            self.execute_script('''%s = \"%s\"''' % (inner_body, html_body))
        elif found_body and found_head:
            self.execute_script('''%s = \"%s\"''' % (inner_head, html_head))
            self.execute_script('''%s = \"%s\"''' % (inner_body, html_body))
        else:
            raise Exception("Logic Error!")

        for script in scripts:
            js_code = script.string
            js_src = script.get("src")
            if js_code and script.get("type") != "application/json":
                js_code_lines = js_code.split("\n")
                new_lines = []
                for line in js_code_lines:
                    line = line.strip()
                    new_lines.append(line)
                js_code = "\n".join(new_lines)
                js_code = re.escape(js_code)
                js_utils.add_js_code(self.driver, js_code)
            elif js_src:
                js_utils.add_js_link(self.driver, js_src)
            else:
                pass

    def set_content(self, html_string, new_page=False):
        """Same as load_html_string(), but "new_page" defaults to False."""
        self.load_html_string(html_string, new_page=new_page)

    def load_html_file(self, html_file, new_page=True):
        """Loads a local html file into the browser from a relative file path.
        If new_page==True, the page will switch to: "data:text/html,"
        If new_page==False, will load HTML into the current page.
        Local images and other local src content WILL BE IGNORED.
        """
        self.__check_scope()
        if self.__looks_like_a_page_url(html_file):
            self.open(html_file)
            return
        if len(html_file) < 6 or not html_file.endswith(".html"):
            raise Exception('Expecting a ".html" file!')
        abs_path = os.path.abspath(".")
        file_path = None
        if abs_path in html_file:
            file_path = html_file
        else:
            file_path = os.path.join(abs_path, html_file)
        html_string = None
        with open(file_path, "r") as f:
            html_string = f.read().strip()
        self.load_html_string(html_string, new_page)

    def open_html_file(self, html_file):
        """Opens a local html file into the browser from a relative file path.
        The URL displayed in the web browser will start with "file://".
        """
        self.__check_scope()
        if self.__looks_like_a_page_url(html_file):
            self.open(html_file)
            return
        if len(html_file) < 6 or not html_file.endswith(".html"):
            raise Exception('Expecting a ".html" file!')
        abs_path = os.path.abspath(".")
        file_path = None
        if abs_path in html_file:
            file_path = html_file
        else:
            file_path = os.path.join(abs_path, html_file)
        self.open("file://" + file_path)

    def execute_script(self, script, *args, **kwargs):
        self.__check_scope()
        self.__check_browser()
        if not python3:
            script = unicode(script.decode("latin-1"))  # noqa: F821
        return self.driver.execute_script(script, *args, **kwargs)

    def execute_async_script(self, script, timeout=None):
        self.__check_scope()
        self.__check_browser()
        if not timeout:
            timeout = settings.EXTREME_TIMEOUT
        return js_utils.execute_async_script(self.driver, script, timeout)

    def safe_execute_script(self, script, *args, **kwargs):
        """When executing a script that contains a jQuery command,
        it's important that the jQuery library has been loaded first.
        This method will load jQuery if it wasn't already loaded."""
        self.__check_scope()
        self.__check_browser()
        if not js_utils.is_jquery_activated(self.driver):
            self.activate_jquery()
        return self.driver.execute_script(script, *args, **kwargs)

    def set_window_rect(self, x, y, width, height):
        self.__check_scope()
        self.driver.set_window_rect(x, y, width, height)
        self.__demo_mode_pause_if_active()

    def set_window_size(self, width, height):
        self.__check_scope()
        self.driver.set_window_size(width, height)
        self.__demo_mode_pause_if_active()

    def maximize_window(self):
        self.__check_scope()
        self.driver.maximize_window()
        self.__demo_mode_pause_if_active()

    def switch_to_frame(self, frame, timeout=None):
        """Wait for an iframe to appear, and switch to it. This should be
        usable as a drop-in replacement for driver.switch_to.frame().
        The iframe identifier can be a selector, an index, an id, a name,
        or a web element, but scrolling to the iframe first will only occur
        for visible iframes with a string selector.
        @Params
        frame - the frame element, name, id, index, or selector
        timeout - the time to wait for the alert in seconds
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if self.__needs_minimum_wait():
            time.sleep(0.035)
        if type(frame) is str and self.is_element_visible(frame):
            try:
                self.scroll_to(frame, timeout=1)
                if self.__needs_minimum_wait():
                    time.sleep(0.01)
            except Exception:
                time.sleep(0.01)
        else:
            if self.__needs_minimum_wait():
                time.sleep(0.04)
        if self.recorder_mode and self._rec_overrides_switch:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    r_a = self.get_session_storage_item("recorder_activated")
                    if r_a == "yes":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["sk_op", "", origin, time_stamp]
                        self.__extra_actions.append(action)
                        self.__set_c_from_switch = True
                        self.set_content_to_frame(frame, timeout=timeout)
                        self.__set_c_from_switch = False
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["sw_fr", frame, origin, time_stamp]
                        self.__extra_actions.append(action)
                        return
        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.035)
        page_actions.switch_to_frame(self.driver, frame, timeout)
        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.015)

    def switch_to_default_content(self):
        """Brings driver control outside the current iframe.
        If the driver is currently set inside an iframe or nested iframes,
        then the driver control will exit from all entered iframes.
        If the driver is not currently set in an iframe, nothing happens."""
        self.__check_scope()
        if self.recorder_mode and self._rec_overrides_switch:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    r_a = self.get_session_storage_item("recorder_activated")
                    if r_a == "yes":
                        self.__set_c_from_switch = True
                        self.set_content_to_default()
                        self.__set_c_from_switch = False
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["sw_dc", "", origin, time_stamp]
                        self.__extra_actions.append(action)
                        return
        self.driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        """Brings driver control outside the current iframe.
        If the driver is currently set inside an iframe or nested iframes,
        the driver control will be set to one level above the current frame.
        If the driver is not currently set in an iframe, nothing happens."""
        self.__check_scope()
        if self.recorder_mode and self._rec_overrides_switch:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    r_a = self.get_session_storage_item("recorder_activated")
                    if r_a == "yes":
                        self.__set_c_from_switch = True
                        self.set_content_to_default(nested=True)
                        self.__set_c_from_switch = False
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["sw_pf", "", origin, time_stamp]
                        self.__extra_actions.append(action)
                        return
        self.driver.switch_to.parent_frame()

    @contextmanager
    def frame_switch(self, frame, timeout=None):
        """ Context Manager for switching into iframes.
        Usage example:
            with self.frame_switch("iframe"):
                # Perform actions here that should be done within the iframe.
            # The iframe is automatically exited after the "with" block ends.
        """
        if self.recorder_mode:
            self.__frame_switch_layer += 1
            if self.__frame_switch_layer >= 2:
                self.__frame_switch_multi = True
        self.switch_to_frame(frame, timeout=timeout)
        yield
        self.switch_to_parent_frame()
        if self.recorder_mode:
            self.__frame_switch_layer -= 1
            if self.__frame_switch_layer < 0:
                self.__frame_switch_layer = 0
                self.__frame_switch_multi = False
            if self.__frame_switch_layer == 0 and self.__frame_switch_multi:
                self.refresh()
                self.__frame_switch_multi = False

    def set_content_to_frame(self, frame, timeout=None):
        """Replaces the page html with an iframe's html from that page.
        If the iframe contains an "src" field that includes a valid URL,
        then instead of replacing the current html, this method will then
        open up the "src" URL of the iframe in a new browser tab.
        To return to default content, use: self.set_content_to_default().
        This method also sets the state of the browser window so that the
        self.set_content_to_default() method can bring the user back to
        the original content displayed, which is similar to how the methods
        self.switch_to_frame(frame) and self.switch_to_default_content()
        work together to get the user into frames and out of all of them."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        current_url = self.get_current_url()
        c_tab = self.driver.current_window_handle
        current_page_source = self.get_page_source()
        self.execute_script("document.cframe_swap = 0;")
        page_actions.switch_to_frame(self.driver, frame, timeout)
        iframe_html = self.get_page_source()
        self.driver.switch_to.default_content()
        self.wait_for_ready_state_complete()
        frame_found = False
        o_frame = frame
        if self.is_element_present(frame):
            frame_found = True
        elif " " not in frame:
            frame = 'iframe[name="%s"]' % frame
            if self.is_element_present(frame):
                frame_found = True
        url = None
        if frame_found:
            url = self.execute_script(
                """return document.querySelector('%s').src;""" % frame
            )
            if not python3:
                url = str(url)
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    pass
                else:
                    url = None
        cframe_tab = False
        if url:
            cframe_tab = True
        self.__page_sources.append([current_url, current_page_source, c_tab])

        if self.recorder_mode and not self.__set_c_from_switch:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["sk_op", "", origin, time_stamp]
            self.__extra_actions.append(action)

        if cframe_tab:
            self.execute_script("document.cframe_tab = 1;")
            self.open_new_window(switch_to=True)
            self.open(url)
            self.execute_script("document.cframe_tab = 1;")
        else:
            self.set_content(iframe_html)
            if not self.execute_script("return document.cframe_swap;"):
                self.execute_script("document.cframe_swap = 1;")
            else:
                self.execute_script("document.cframe_swap += 1;")

        if self.recorder_mode and not self.__set_c_from_switch:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["s_c_f", o_frame, origin, time_stamp]
            self.__extra_actions.append(action)

    def set_content_to_default(self, nested=False):
        """After using self.set_content_to_frame(), this reverts the page back.
        If self.set_content_to_frame() hasn't been called here, only refreshes.
        If "nested" is set to True when the content is set to a nested iframe,
        then the page control will only exit from the current iframe entered,
        instead of exiting out of all iframes entered."""
        self.__check_scope()
        swap_cnt = self.execute_script("return document.cframe_swap;")
        tab_sta = self.execute_script("return document.cframe_tab;")

        if self.recorder_mode and not self.__set_c_from_switch:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["sk_op", "", origin, time_stamp]
            self.__extra_actions.append(action)

        if not nested:
            # Sets the page to the outer-most content.
            # If page control was inside nested iframes, exits them all.
            # If only in one iframe, has the same effect as nested=True.
            if (
                len(self.__page_sources) > 0
                and (
                    (swap_cnt and int(swap_cnt) > 0)
                    or (tab_sta and int(tab_sta) > 0)
                )
            ):
                past_content = self.__page_sources[0]
                past_url = past_content[0]
                past_source = past_content[1]
                past_tab = past_content[2]
                current_tab = self.driver.current_window_handle
                if not current_tab == past_tab:
                    if past_tab in self.driver.window_handles:
                        self.switch_to_window(past_tab)
                url_of_past_tab = self.get_current_url()
                if url_of_past_tab == past_url:
                    self.set_content(past_source)
                else:
                    self.refresh_page()
            else:
                self.refresh_page()
            self.execute_script("document.cframe_swap = 0;")
            self.__page_sources = []
        else:
            # (If Nested is True)
            # Sets the page to the content outside the current nested iframe.
            # If only in one iframe, has the same effect as nested=True.
            just_refresh = False
            if swap_cnt and int(swap_cnt) > 0 and len(self.__page_sources) > 0:
                self.execute_script("document.cframe_swap -= 1;")
                current_url = self.get_current_url()
                past_content = self.__page_sources.pop()
                past_url = past_content[0]
                past_source = past_content[1]
                if current_url == past_url:
                    self.set_content(past_source)
                else:
                    just_refresh = True
            elif tab_sta and int(tab_sta) > 0 and len(self.__page_sources) > 0:
                past_content = self.__page_sources.pop()
                past_tab = past_content[2]
                if past_tab in self.driver.window_handles:
                    self.switch_to_window(past_tab)
                else:
                    just_refresh = True
            else:
                just_refresh = True
            if just_refresh:
                self.refresh_page()
                self.execute_script("document.cframe_swap = 0;")
                self.__page_sources = []

        if self.recorder_mode and not self.__set_c_from_switch:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["s_c_d", nested, origin, time_stamp]
            self.__extra_actions.append(action)

    def set_content_to_default_content(self, nested=False):
        """Same as self.set_content_to_default()."""
        self.set_content_to_default(nested=nested)

    def set_content_to_parent(self):
        """Same as self.set_content_to_parent_frame().
        Same as self.set_content_to_default(nested=True).
        Sets the page to the content outside the current nested iframe.
        Reverts self.set_content_to_frame()."""
        self.set_content_to_default(nested=True)

    def set_content_to_parent_frame(self):
        """Same as self.set_content_to_parent().
        Same as self.set_content_to_default(nested=True).
        Sets the page to the content outside the current nested iframe.
        Reverts self.set_content_to_frame()."""
        self.set_content_to_default(nested=True)

    def open_new_window(self, switch_to=True):
        """Opens a new browser tab/window and switches to it by default."""
        self.wait_for_ready_state_complete()
        if hasattr(self.driver, "tab_new"):
            self.driver.tab_new("about:blank")
            if switch_to:
                self.switch_to_newest_window()
            time.sleep(0.01)
            return
        if selenium4_or_newer and switch_to:
            self.driver.switch_to.new_window("tab")
        else:
            self.driver.execute_script("window.open('');")
        time.sleep(0.01)
        if self.browser == "safari":
            self.wait_for_ready_state_complete()
        if switch_to and not selenium4_or_newer:
            self.switch_to_newest_window()
            time.sleep(0.01)
            if self.browser == "safari":
                self.wait_for_ready_state_complete()

    def switch_to_window(self, window, timeout=None):
        """Switches control of the browser to the specified window.
        The window can be an integer: 0 -> 1st tab, 1 -> 2nd tab, etc...
            Or it can be a list item from self.driver.window_handles"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        page_actions.switch_to_window(self.driver, window, timeout)

    def switch_to_default_window(self):
        self.switch_to_window(0)

    def switch_to_newest_window(self):
        self.switch_to_window(len(self.driver.window_handles) - 1)

    def get_new_driver(
        self,
        browser=None,
        headless=None,
        locale_code=None,
        protocol=None,
        servername=None,
        port=None,
        proxy=None,
        proxy_bypass_list=None,
        proxy_pac_url=None,
        agent=None,
        switch_to=True,
        cap_file=None,
        cap_string=None,
        recorder_ext=None,
        disable_js=None,
        disable_csp=None,
        enable_ws=None,
        enable_sync=None,
        use_auto_ext=None,
        undetectable=None,
        uc_subprocess=None,
        no_sandbox=None,
        disable_gpu=None,
        headless2=None,
        incognito=None,
        guest_mode=None,
        devtools=None,
        remote_debug=None,
        enable_3d_apis=None,
        swiftshader=None,
        ad_block_on=None,
        block_images=None,
        do_not_track=None,
        chromium_arg=None,
        firefox_arg=None,
        firefox_pref=None,
        user_data_dir=None,
        extension_zip=None,
        extension_dir=None,
        page_load_strategy=None,
        use_wire=None,
        external_pdf=None,
        is_mobile=None,
        d_width=None,
        d_height=None,
        d_p_r=None,
    ):
        """This method spins up an extra browser for tests that require
        more than one. The first browser is already provided by tests
        that import base_case.BaseCase from seleniumbase. If parameters
        aren't specified, the method uses the same as the default driver.
        @Params
        browser - the browser to use. (Ex: "chrome", "firefox")
        headless - the option to run webdriver in headless mode
        locale_code - the Language Locale Code for the web browser
        protocol - if using a Selenium Grid, set the host protocol here
        servername - if using a Selenium Grid, set the host address here
        port - if using a Selenium Grid, set the host port here
        proxy - if using a proxy server, specify the "host:port" combo here
        proxy_bypass_list - ";"-separated hosts to bypass (Eg. "*.foo.com")
        proxy_pac_url - designates the proxy PAC URL to use (Chromium-only)
        switch_to - the option to switch to the new driver (default = True)
        cap_file - the file containing desired capabilities for the browser
        cap_string - the string with desired capabilities for the browser
        recorder_ext - the option to enable the SBase Recorder extension
        disable_js - the option to disable JavaScript (May break websites!)
        disable_csp - an option to disable Chrome's Content Security Policy
        enable_ws - the option to enable the Web Security feature (Chrome)
        enable_sync - the option to enable the Chrome Sync feature (Chrome)
        use_auto_ext - the option to enable Chrome's Automation Extension
        undetectable - the option to use an undetectable chromedriver
        uc_subprocess - use the undetectable chromedriver as a subprocess
        no_sandbox - the option to enable the "No-Sandbox" feature (Chrome)
        disable_gpu - the option to enable Chrome's "Disable GPU" feature
        headless2 - the option to use the newer headless mode (Chromium)
        incognito - the option to enable Chrome's Incognito mode (Chrome)
        guest - the option to enable Chrome's Guest mode (Chrome)
        devtools - the option to open Chrome's DevTools on start (Chrome)
        remote_debug - the option to enable Chrome's Remote Debugger
        enable_3d_apis - the option to enable WebGL and 3D APIs (Chrome)
        swiftshader - the option to use Chrome's swiftshader (Chrome-only)
        ad_block_on - the option to block ads from loading (Chromium-only)
        block_images - the option to block images from loading (Chrome)
        do_not_track - indicate that websites should not track you (Chrome)
        chromium_arg - the option to add a Chromium arg to Chrome/Edge
        firefox_arg - the option to add a Firefox arg to Firefox runs
        firefox_pref - the option to add a Firefox pref:value set (Firefox)
        user_data_dir - Chrome's User Data Directory to use (Chrome-only)
        extension_zip - A Chrome Extension ZIP file to use (Chrome-only)
        extension_dir - A Chrome Extension folder to use (Chrome-only)
        page_load_strategy - the option to change pageLoadStrategy (Chrome)
        use_wire - Use selenium-wire webdriver instead of the selenium one
        external_pdf - "plugins.always_open_pdf_externally": True. (Chrome)
        is_mobile - the option to use the mobile emulator (Chrome-only)
        d_width - the device width of the mobile emulator (Chrome-only)
        d_height - the device height of the mobile emulator (Chrome-only)
        d_p_r - the device pixel ratio of the mobile emulator (Chrome-only)
        """
        self.__check_scope()
        if self.browser == "remote" and self.servername == "localhost":
            raise Exception(
                'Cannot use "remote" browser driver on localhost!'
                " Did you mean to connect to a remote Grid server"
                " such as BrowserStack, LambdaTest, or Sauce Labs?"
                ' If so, you must specify the "server" and "port"'
                " parameters on the command line! "
                "Example: "
                "--server=user:key@hub.browserstack.com --port=80"
            )
        browserstack_ref = "https://browserstack.com/automate/capabilities"
        lambdatest_ref = "https://www.lambdatest.com/capabilities-generator"
        sauce_labs_ref = (
            "https://wiki.saucelabs.com/display/DOCS/Platform+Configurator#/"
        )
        if self.browser == "remote" and not (self.cap_file or self.cap_string):
            raise Exception(
                "Need to specify a desired capabilities file when "
                'using "--browser=remote". Add "--cap_file=FILE". '
                "File should be in the Python format used by: "
                "%s, "
                "%s, OR "
                "%s "
                "See SeleniumBase/examples/capabilities/sample_cap_file_BS.py,"
                " SeleniumBase/examples/capabilities/sample_cap_file_LT.py,"
                " and SeleniumBase/examples/capabilities/sample_cap_file_SL.py"
                % (browserstack_ref, lambdatest_ref, sauce_labs_ref)
            )
        if browser is None:
            browser = self.browser
        browser_name = browser
        if headless is None:
            headless = self.headless
        if locale_code is None:
            locale_code = self.locale_code
        if protocol is None:
            protocol = self.protocol
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
        if proxy_bypass_list is None:
            proxy_bypass_list = self.proxy_bypass_list
        if proxy_pac_url is None:
            proxy_pac_url = self.proxy_pac_url
        user_agent = agent
        if user_agent is None:
            user_agent = self.user_agent
        if recorder_ext is None:
            recorder_ext = self.recorder_ext
        if disable_js is None:
            disable_js = self.disable_js
        if disable_csp is None:
            disable_csp = self.disable_csp
        if enable_ws is None:
            enable_ws = self.enable_ws
        if enable_sync is None:
            enable_sync = self.enable_sync
        if use_auto_ext is None:
            use_auto_ext = self.use_auto_ext
        if undetectable is None:
            undetectable = self.undetectable
        if uc_subprocess is None:
            uc_subprocess = self.uc_subprocess
        if no_sandbox is None:
            no_sandbox = self.no_sandbox
        if disable_gpu is None:
            disable_gpu = self.disable_gpu
        if headless2 is None:
            headless2 = self.headless2
        if incognito is None:
            incognito = self.incognito
        if guest_mode is None:
            guest_mode = self.guest_mode
        if devtools is None:
            devtools = self.devtools
        if remote_debug is None:
            remote_debug = self.remote_debug
        if enable_3d_apis is None:
            enable_3d_apis = self.enable_3d_apis
        if swiftshader is None:
            swiftshader = self.swiftshader
        if ad_block_on is None:
            ad_block_on = self.ad_block_on
        if block_images is None:
            block_images = self.block_images
        if do_not_track is None:
            do_not_track = self.do_not_track
        if chromium_arg is None:
            chromium_arg = self.chromium_arg
        if firefox_arg is None:
            firefox_arg = self.firefox_arg
        if firefox_pref is None:
            firefox_pref = self.firefox_pref
        if user_data_dir is None:
            user_data_dir = self.user_data_dir
        if extension_zip is None:
            extension_zip = self.extension_zip
        if extension_dir is None:
            extension_dir = self.extension_dir
        if page_load_strategy is None:
            page_load_strategy = self.page_load_strategy
        if use_wire is None:
            use_wire = self.use_wire
        if external_pdf is None:
            external_pdf = self.external_pdf
        test_id = self.__get_test_id()
        if cap_file is None:
            cap_file = self.cap_file
        if cap_string is None:
            cap_string = self.cap_string
        if is_mobile is None:
            is_mobile = self.mobile_emulator
        if d_width is None:
            d_width = self.__device_width
        if d_height is None:
            d_height = self.__device_height
        if d_p_r is None:
            d_p_r = self.__device_pixel_ratio
        valid_browsers = constants.ValidBrowsers.valid_browsers
        if browser_name not in valid_browsers:
            raise Exception(
                "Browser: {%s} is not a valid browser option. "
                "Valid options = {%s}" % (browser, valid_browsers)
            )
        # Launch a web browser
        from seleniumbase.core import browser_launcher

        new_driver = browser_launcher.get_driver(
            browser_name=browser_name,
            headless=headless,
            locale_code=locale_code,
            use_grid=use_grid,
            protocol=protocol,
            servername=servername,
            port=port,
            proxy_string=proxy_string,
            proxy_bypass_list=proxy_bypass_list,
            proxy_pac_url=proxy_pac_url,
            user_agent=user_agent,
            cap_file=cap_file,
            cap_string=cap_string,
            recorder_ext=recorder_ext,
            disable_js=disable_js,
            disable_csp=disable_csp,
            enable_ws=enable_ws,
            enable_sync=enable_sync,
            use_auto_ext=use_auto_ext,
            undetectable=undetectable,
            uc_subprocess=uc_subprocess,
            no_sandbox=no_sandbox,
            disable_gpu=disable_gpu,
            headless2=headless2,
            incognito=incognito,
            guest_mode=guest_mode,
            devtools=devtools,
            remote_debug=remote_debug,
            enable_3d_apis=enable_3d_apis,
            swiftshader=swiftshader,
            ad_block_on=ad_block_on,
            block_images=block_images,
            do_not_track=do_not_track,
            chromium_arg=chromium_arg,
            firefox_arg=firefox_arg,
            firefox_pref=firefox_pref,
            user_data_dir=user_data_dir,
            extension_zip=extension_zip,
            extension_dir=extension_dir,
            page_load_strategy=page_load_strategy,
            use_wire=use_wire,
            external_pdf=external_pdf,
            test_id=test_id,
            mobile_emulator=is_mobile,
            device_width=d_width,
            device_height=d_height,
            device_pixel_ratio=d_p_r,
            browser=browser_name,
        )
        self._drivers_list.append(new_driver)
        self._drivers_browser_map[new_driver] = browser_name
        if switch_to:
            self.driver = new_driver
            self.browser = browser_name
            if self.headless or self.headless2 or self.xvfb:
                # Make sure the invisible browser window is big enough
                width = settings.HEADLESS_START_WIDTH
                height = settings.HEADLESS_START_HEIGHT
                if self.browser != "chrome" and self.browser != "edge":
                    try:
                        self.driver.set_window_size(width, height)
                        # self.wait_for_ready_state_complete()
                    except Exception:
                        # This shouldn't fail, but in case it does,
                        # get safely through setUp() so that
                        # WebDrivers can get closed during tearDown().
                        pass
            else:
                width = settings.CHROME_START_WIDTH
                height = settings.CHROME_START_HEIGHT
                if self.browser == "chrome" or self.browser == "edge":
                    try:
                        if self.maximize_option:
                            self.driver.maximize_window()
                            self.wait_for_ready_state_complete()
                        else:
                            pass  # Now handled in browser_launcher.py
                            # self.driver.set_window_size(width, height)
                    except Exception:
                        pass  # Keep existing browser resolution
                elif self.browser == "firefox":
                    try:
                        if self.maximize_option:
                            self.driver.maximize_window()
                            self.wait_for_ready_state_complete()
                        else:
                            self.driver.set_window_size(width, height)
                    except Exception:
                        pass  # Keep existing browser resolution
                elif self.browser == "safari":
                    if self.maximize_option:
                        try:
                            self.driver.maximize_window()
                            self.wait_for_ready_state_complete()
                        except Exception:
                            pass  # Keep existing browser resolution
                    else:
                        try:
                            self.driver.set_window_rect(10, 20, width, height)
                        except Exception:
                            pass
                elif self.browser == "opera":
                    if self.maximize_option:
                        try:
                            self.driver.maximize_window()
                            self.wait_for_ready_state_complete()
                        except Exception:
                            pass  # Keep existing browser resolution
                    else:
                        try:
                            self.driver.set_window_rect(10, 20, width, height)
                        except Exception:
                            pass
            if self.start_page and len(self.start_page) >= 4:
                if page_utils.is_valid_url(self.start_page):
                    self.open(self.start_page)
                else:
                    new_start_page = "https://" + self.start_page
                    if page_utils.is_valid_url(new_start_page):
                        self.__dont_record_open = True
                        self.open(new_start_page)
                        self.__dont_record_open = False
        return new_driver

    def switch_to_driver(self, driver):
        """Switches control of the browser to the specified driver.
        Also sets the self.driver variable to the specified driver.
        You may need this if using self.get_new_driver() in your code."""
        self.__check_scope()
        self.driver = driver
        if self.driver in self._drivers_browser_map:
            self.browser = self._drivers_browser_map[self.driver]
        self.bring_active_window_to_front()

    def switch_to_default_driver(self):
        """Sets self.driver to the default/initial driver."""
        self.__check_scope()
        self.driver = self._default_driver
        if self.driver in self._drivers_browser_map:
            self.browser = self._drivers_browser_map[self.driver]
        self.bring_active_window_to_front()

    def save_screenshot(
        self, name, folder=None, selector=None, by="css selector"
    ):
        """
        Saves a screenshot of the current page.
        If no folder is specified, uses the folder where pytest was called.
        The screenshot will include the entire page unless a selector is given.
        If a provided selector is not found, then takes a full-page screenshot.
        If the folder provided doesn't exist, it will get created.
        The screenshot will be in PNG format: (*.png)
        """
        self.wait_for_ready_state_complete()
        if selector and by:
            selector, by = self.__recalculate_selector(selector, by)
            if page_actions.is_element_present(self.driver, selector, by):
                return page_actions.save_screenshot(
                    self.driver, name, folder, selector, by
                )
        return page_actions.save_screenshot(self.driver, name, folder)

    def save_screenshot_to_logs(
        self, name=None, selector=None, by="css selector"
    ):
        """Saves a screenshot of the current page to the "latest_logs/" folder.
        Naming is automatic:
            If NO NAME provided: "_1_screenshot.png", "_2_screenshot.png", etc.
            If NAME IS provided, it becomes: "_1_name.png", "_2_name.png", etc.
        The screenshot will include the entire page unless a selector is given.
        If a provided selector is not found, then takes a full-page screenshot.
        (The last_page / failure screenshot is always "screenshot.png")
        The screenshot will be in PNG format."""
        self.wait_for_ready_state_complete()
        test_logpath = os.path.join(self.log_path, self.__get_test_id())
        self.__create_log_path_as_needed(test_logpath)
        if name:
            name = str(name)
        self.__screenshot_count += 1
        if not name or len(name) == 0:
            name = "_%s_screenshot.png" % self.__screenshot_count
        else:
            pre_name = "_%s_" % self.__screenshot_count
            if len(name) >= 4 and name[-4:].lower() == ".png":
                name = name[:-4]
                if len(name) == 0:
                    name = "screenshot"
            name = "%s%s.png" % (pre_name, name)
        if selector and by:
            selector, by = self.__recalculate_selector(selector, by)
            if page_actions.is_element_present(self.driver, selector, by):
                return page_actions.save_screenshot(
                    self.driver, name, test_logpath, selector, by
                )
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["ss_tl", "", origin, time_stamp]
                        self.__extra_actions.append(action)
        sb_config._has_logs = True
        return page_actions.save_screenshot(self.driver, name, test_logpath)

    def save_page_source(self, name, folder=None):
        """Saves the page HTML to the current directory (or given subfolder).
        If the folder specified doesn't exist, it will get created.
        @Params
        name - The file name to save the current page's HTML to.
        folder - The folder to save the file to. (Default = current folder)
        """
        self.wait_for_ready_state_complete()
        return page_actions.save_page_source(self.driver, name, folder)

    def save_cookies(self, name="cookies.txt"):
        """Saves the page cookies to the "saved_cookies" folder."""
        self.wait_for_ready_state_complete()
        cookies = self.driver.get_cookies()
        json_cookies = json.dumps(cookies)
        if name.endswith("/"):
            raise Exception("Invalid filename for Cookies!")
        if "/" in name:
            name = name.split("/")[-1]
        if "\\" in name:
            name = name.split("\\")[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = constants.SavedCookies.STORAGE_FOLDER
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        cookies_file_path = os.path.join(file_path, name)
        cookies_file = codecs.open(cookies_file_path, "w+", encoding="utf-8")
        cookies_file.writelines(json_cookies)
        cookies_file.close()

    def load_cookies(self, name="cookies.txt"):
        """Loads the page cookies from the "saved_cookies" folder."""
        self.wait_for_ready_state_complete()
        if name.endswith("/"):
            raise Exception("Invalid filename for Cookies!")
        if "/" in name:
            name = name.split("/")[-1]
        if "\\" in name:
            name = name.split("\\")[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = constants.SavedCookies.STORAGE_FOLDER
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, folder)
        cookies_file_path = os.path.join(file_path, name)
        json_cookies = None
        with open(cookies_file_path, "r") as f:
            json_cookies = f.read().strip()
        cookies = json.loads(json_cookies)
        for cookie in cookies:
            if "expiry" in cookie:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)

    def delete_all_cookies(self):
        """Deletes all cookies in the web browser.
        Does NOT delete the saved cookies file."""
        self.wait_for_ready_state_complete()
        self.driver.delete_all_cookies()
        if self.recorder_mode:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["d_a_c", "", origin, time_stamp]
            self.__extra_actions.append(action)

    def delete_saved_cookies(self, name="cookies.txt"):
        """Deletes the cookies file from the "saved_cookies" folder.
        Does NOT delete the cookies from the web browser."""
        self.wait_for_ready_state_complete()
        if name.endswith("/"):
            raise Exception("Invalid filename for Cookies!")
        if "/" in name:
            name = name.split("/")[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = constants.SavedCookies.STORAGE_FOLDER
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, folder)
        cookies_file_path = os.path.join(file_path, name)
        if os.path.exists(cookies_file_path):
            if cookies_file_path.endswith(".txt"):
                os.remove(cookies_file_path)

    def wait_for_ready_state_complete(self, timeout=None):
        """Waits for the "readyState" of the page to be "complete".
        Returns True when the method completes."""
        self.__check_scope()
        self.__check_browser()
        if not timeout:
            timeout = settings.EXTREME_TIMEOUT
        if self.timeout_multiplier and timeout == settings.EXTREME_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        js_utils.wait_for_ready_state_complete(self.driver, timeout)
        self.wait_for_angularjs(timeout=settings.MINI_TIMEOUT)
        if self.js_checking_on:
            self.assert_no_js_errors()
        self.__ad_block_as_needed()
        self.__disable_beforeunload_as_needed()
        if (
            self.undetectable
            and self.page_load_strategy == "none"
            and hasattr(settings, "SKIP_JS_WAITS")
            and settings.SKIP_JS_WAITS
        ):
            time.sleep(0.05)
        return True

    def wait_for_angularjs(self, timeout=None, **kwargs):
        """Waits for Angular components of the page to finish loading.
        Returns True when the method completes."""
        self.__check_scope()
        if not timeout:
            timeout = settings.MINI_TIMEOUT
        if self.timeout_multiplier and timeout == settings.MINI_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        js_utils.wait_for_angularjs(self.driver, timeout, **kwargs)
        return True

    def sleep(self, seconds):
        self.__check_scope()
        if (
            not hasattr(sb_config, "time_limit")
            or (hasattr(sb_config, "time_limit") and not sb_config.time_limit)
        ):
            time.sleep(seconds)
        elif seconds < 0.4:
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
        if (
            self.recorder_mode
            and hasattr(sb_config, "record_sleep")
            and sb_config.record_sleep
        ):
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["sleep", seconds, origin, time_stamp]
            self.__extra_actions.append(action)

    def install_addon(self, xpi_file):
        """Installs a Firefox add-on instantly at run-time.
        @Params
        xpi_file - A file archive in .xpi format.
        """
        self.wait_for_ready_state_complete()
        if self.browser != "firefox":
            raise Exception(
                "install_addon(xpi_file) is for Firefox ONLY!\n"
                "To load a Chrome extension, use the comamnd-line:\n"
                "--extension_zip=CRX_FILE  OR  --extension_dir=DIR"
            )
        xpi_path = os.path.abspath(xpi_file)
        self.driver.install_addon(xpi_path, temporary=True)

    def activate_jquery(self):
        """If "jQuery is not defined", use this method to activate it for use.
        This happens because jQuery is not always defined on web sites."""
        self.wait_for_ready_state_complete()
        js_utils.activate_jquery(self.driver)
        self.wait_for_ready_state_complete()

    def activate_demo_mode(self):
        self.demo_mode = True

    def deactivate_demo_mode(self):
        self.demo_mode = False

    def activate_design_mode(self):
        # Activate Chrome's Design Mode, which lets you edit a site directly.
        # See: https://twitter.com/sulco/status/1177559150563344384
        self.wait_for_ready_state_complete()
        script = """document.designMode = 'on';"""
        self.execute_script(script)

    def deactivate_design_mode(self):
        # Deactivate Chrome's Design Mode.
        self.wait_for_ready_state_complete()
        script = """document.designMode = 'off';"""
        self.execute_script(script)

    def activate_recorder(self):
        from seleniumbase.js_code.recorder_js import recorder_js

        if not self.is_chromium():
            raise Exception(
                "The Recorder is only for Chromium browsers: (Chrome or Edge)"
            )
        url = self.driver.current_url
        if (
            url.startswith("data:") or url.startswith("about:")
            or url.startswith("chrome:") or url.startswith("edge:")
        ):
            message = (
                "The URL in Recorder-Mode cannot start with: "
                '"data:", "about:", "chrome:", or "edge:"!'
            )
            print("\n" + message)
            return
        if self.recorder_ext:
            return  # The Recorder extension is already active
        try:
            recorder_on = self.get_session_storage_item("recorder_activated")
            if not recorder_on == "yes":
                self.execute_script(recorder_js)
            self.recorder_mode = True
            message = "Recorder Mode ACTIVE. [ESC]: Pause. [~`]: Resume."
            print("\n" + message)
            p_msg = "Recorder Mode ACTIVE.<br>[ESC]: Pause. [~`]: Resume."
            self.post_message(p_msg, pause=False, style="error")
        except Exception:
            pass

    def save_recorded_actions(self):
        """(When using Recorder Mode, use this method if you plan on
            navigating to a different domain/origin in the same tab.)
        This method saves recorded actions from the active tab so that
        a complete recording can be exported as a SeleniumBase file at the
        end of the test. This is only needed in special cases because most
        actions that result in a new origin, (such as clicking on a link),
        should automatically open a new tab while Recorder Mode is enabled."""
        url = self.get_current_url()
        if url and len(url) > 0:
            if ("http:") in url or ("https:") in url or ("file:") in url:
                origin = self.get_origin()
                self.__origins_to_save.append(origin)
                tab_actions = self.__get_recorded_actions_on_active_tab()
                for n in range(len(tab_actions)):
                    if (
                        n > 2
                        and tab_actions[n - 2][0] == "sw_fr"
                        and tab_actions[n - 1][0] == "sk_fo"
                        and tab_actions[n][0] != "_url_"
                    ):
                        origin = tab_actions[n - 2][2]
                        time_stamp = str(int(tab_actions[n][3]) - 1)
                        new_action = ["sw_pf", "", origin, time_stamp]
                        tab_actions.append(new_action)
                self.__actions_to_save.append(tab_actions)

    def __get_recorded_actions_on_active_tab(self):
        url = self.driver.current_url
        if (
            url.startswith("data:") or url.startswith("about:")
            or url.startswith("chrome:") or url.startswith("edge:")
        ):
            return []
        self.__origins_to_save.append(self.get_origin())
        actions = self.get_session_storage_item("recorded_actions")
        if actions:
            actions = json.loads(actions)
            return actions
        else:
            return []

    def __process_recorded_actions(self):
        import colorama

        raw_actions = []  # All raw actions from sessionStorage
        srt_actions = []
        cleaned_actions = []
        sb_actions = []
        action_dict = {}
        for window in self.driver.window_handles:
            self.switch_to_window(window)
            tab_actions = self.__get_recorded_actions_on_active_tab()
            for n in range(len(tab_actions)):
                if (
                    n > 2
                    and tab_actions[n - 2][0] == "sw_fr"
                    and tab_actions[n - 1][0] == "sk_fo"
                    and tab_actions[n][0] != "_url_"
                ):
                    origin = tab_actions[n - 2][2]
                    time_stamp = str(int(tab_actions[n][3]) - 1)
                    new_action = ["sw_pf", "", origin, time_stamp]
                    tab_actions.append(new_action)
            for action in tab_actions:
                if action not in raw_actions:
                    raw_actions.append(action)
        for tab_actions in self.__actions_to_save:
            for action in tab_actions:
                if action not in raw_actions:
                    raw_actions.append(action)
        for action in self.__extra_actions:
            if action not in raw_actions:
                raw_actions.append(action)
        for action in raw_actions:
            if int(action[3]) < int(self.__js_start_time):
                continue
            # Use key for sorting and preventing duplicates
            key = str(action[3]) + "-" + str(action[0])
            action_dict[key] = action
        for key in sorted(action_dict):
            # print(action_dict[key])  # For debugging purposes
            srt_actions.append(action_dict[key])
        for n in range(len(srt_actions)):
            if srt_actions[n][0] == "sk_fo":
                srt_actions[n][0] = "sk_op"
        for n in range(len(srt_actions)):
            if (
                (srt_actions[n][0] == "begin" or srt_actions[n][0] == "_url_")
                and n > 0
                and srt_actions[n - 1][0] == "sk_op"
            ):
                srt_actions[n][0] = "_skip"
        for n in range(len(srt_actions)):
            if (
                (srt_actions[n][0] == "begin" or srt_actions[n][0] == "_url_")
                and n > 1
                and srt_actions[n - 1][0] == "_skip"
                and srt_actions[n - 2][0] == "sk_op"
                and srt_actions[n][2] == srt_actions[n - 1][2]
            ):
                srt_actions[n][0] = "_skip"
        for n in range(len(srt_actions)):
            if (
                (srt_actions[n][0] == "begin" or srt_actions[n][0] == "_url_")
                and n > 0
                and (
                    srt_actions[n - 1][0] == "click"
                    or srt_actions[n - 1][0] == "js_cl"
                    or srt_actions[n - 1][0] == "js_ca"
                )
            ):
                sel1 = srt_actions[n - 1][1]
                url1 = srt_actions[n - 1][2]
                if (
                    srt_actions[n - 1][0] == "js_cl"
                    or srt_actions[n - 1][0] == "js_ca"
                ):
                    url1 = srt_actions[n - 1][2][0]
                if url1.endswith("/#/"):
                    url1 = url1[:-3]
                elif url1.endswith("/"):
                    url1 = url1[:-1]
                url2 = srt_actions[n][2]
                if url2.endswith("/#/"):
                    url2 = url1[:-3]
                elif url2.endswith("/"):
                    url2 = url2[:-1]
                if (
                    url1 == url2
                    or url1 == url2.replace("www.", "")
                    or url1 == url2.replace("https://", "http://")
                    or sel1.split(" ")[-1].startswith("a[href=")
                    or (len(url1) > 0
                        and (url2.startswith(url1) or "?search" in url1)
                        and (int(srt_actions[n][3]) - int(
                            srt_actions[n - 1][3]) < 6500))
                ):
                    srt_actions[n][0] = "f_url"
        for n in range(len(srt_actions)):
            if (
                (srt_actions[n][0] == "begin" or srt_actions[n][0] == "_url_")
                and n > 0
                and (
                    srt_actions[n - 1][0] == "begin"
                    or srt_actions[n - 1][0] == "_url_"
                )
            ):
                url1 = srt_actions[n - 1][2]
                if url1.endswith("/#/"):
                    url1 = url1[:-3]
                elif url1.endswith("/"):
                    url1 = url1[:-1]
                url2 = srt_actions[n][2]
                if url2.endswith("/#/"):
                    url2 = url1[:-3]
                elif url2.endswith("/"):
                    url2 = url2[:-1]
                if url1.replace("www.", "") == url2.replace("www.", ""):
                    srt_actions[n - 1][0] = "_skip"
                elif url1.replace("http://", "https://") == url2:
                    srt_actions[n - 1][0] = "_skip"
                elif url2.startswith(url1):
                    srt_actions[n][0] = "f_url"
        for n in range(len(srt_actions)):
            if (
                srt_actions[n][0] == "input"
                and n > 0
                and srt_actions[n - 1][0] == "input"
                and srt_actions[n - 1][2] == ""
            ):
                srt_actions[n - 1][0] = "_skip"
            elif (
                srt_actions[n][0] == "input"
                and n > 1
                and srt_actions[n - 2][0] == "input"
                and srt_actions[n - 1][0] == "submi"
                and srt_actions[n - 2][1].startswith("textarea")
                and srt_actions[n - 2][1] == srt_actions[n][1]
            ):
                srt_actions[n - 2][0] = "_skip"
        for n in range(len(srt_actions)):
            if (
                (srt_actions[n][0] == "begin" or srt_actions[n][0] == "_url_")
                and n > 0
                and (
                    srt_actions[n - 1][0] == "click"
                    or srt_actions[n - 1][0] == "js_cl"
                    or srt_actions[n - 1][0] == "js_ca"
                    or srt_actions[n - 1][0] == "input"
                )
                and (
                    int(srt_actions[n][3]) - int(srt_actions[n - 1][3]) < 6500
                )
            ):
                if (
                    srt_actions[n - 1][0] == "click"
                    or srt_actions[n - 1][0] == "js_cl"
                    or srt_actions[n - 1][0] == "js_ca"
                ):
                    if (
                        srt_actions[n - 1][1].startswith("input")
                        or srt_actions[n - 1][1].startswith("button")
                    ):
                        srt_actions[n][0] = "f_url"
                elif srt_actions[n - 1][0] == "input":
                    if srt_actions[n - 1][2].endswith("\n"):
                        srt_actions[n][0] = "f_url"
        for n in range(len(srt_actions)):
            if (
                srt_actions[n][0] == "cho_f"
                and n > 0
                and srt_actions[n - 1][0] == "chfil"
            ):
                srt_actions[n - 1][0] = "_skip"
                srt_actions[n][2] = srt_actions[n - 1][1][1]
        for n in range(len(srt_actions)):
            if (
                srt_actions[n][0] == "input"
                and n > 0
                and srt_actions[n - 1][0] == "e_mfa"
            ):
                srt_actions[n][0] = "_skip"
        for n in range(len(srt_actions)):
            if (
                (srt_actions[n][0] == "begin" or srt_actions[n][0] == "_url_")
                and n > 0
                and (
                    srt_actions[n - 1][0] == "submi"
                    or srt_actions[n - 1][0] == "e_mfa"
                )
            ):
                srt_actions[n][0] = "f_url"
        origins = []
        for n in range(len(srt_actions)):
            if (
                srt_actions[n][0] == "begin"
                or srt_actions[n][0] == "_url_"
                or srt_actions[n][0] == "f_url"
            ):
                origin = srt_actions[n][1]
                if origin.endswith("/"):
                    origin = origin[0:-1]
                if origin not in origins:
                    origins.append(origin)
        for origin in self.__origins_to_save:
            origins.append(origin)
        for n in range(len(srt_actions)):
            if (
                srt_actions[n][0] == "click"
                and n > 0
                and srt_actions[n - 1][0] == "ho_cl"
                and srt_actions[n - 1][2] in origins
            ):
                srt_actions[n - 1][0] = "_skip"
                srt_actions[n][0] = "h_clk"
                srt_actions[n][1] = srt_actions[n - 1][1][0]
                srt_actions[n][2] = srt_actions[n - 1][1][1]
        for n in range(len(srt_actions)):
            if srt_actions[n][0] == "chfil" and srt_actions[n][2] in origins:
                srt_actions[n][0] = "cho_f"
                srt_actions[n][2] = srt_actions[n][1][1]
                srt_actions[n][1] = srt_actions[n][1][0]
        for n in range(len(srt_actions)):
            if (
                srt_actions[n][0] == "sh_fc"
                and n > 0
                and srt_actions[n - 1][0] == "sh_fc"
            ):
                srt_actions[n - 1][0] = "_skip"
        ext_actions = []
        ext_actions.append("_url_")
        ext_actions.append("js_cl")
        ext_actions.append("js_ca")
        ext_actions.append("js_ty")
        ext_actions.append("as_el")
        ext_actions.append("as_ep")
        ext_actions.append("asenv")
        ext_actions.append("hi_li")
        ext_actions.append("as_lt")
        ext_actions.append("as_ti")
        ext_actions.append("as_tc")
        ext_actions.append("as_df")
        ext_actions.append("do_fi")
        ext_actions.append("as_at")
        ext_actions.append("as_te")
        ext_actions.append("astnv")
        ext_actions.append("as_et")
        ext_actions.append("wf_el")
        ext_actions.append("sw_fr")
        ext_actions.append("sw_dc")
        ext_actions.append("sw_pf")
        ext_actions.append("s_c_f")
        ext_actions.append("s_c_d")
        ext_actions.append("sleep")
        ext_actions.append("sh_fc")
        ext_actions.append("c_l_s")
        ext_actions.append("c_s_s")
        ext_actions.append("d_a_c")
        ext_actions.append("e_mfa")
        ext_actions.append("go_bk")
        ext_actions.append("go_fw")
        ext_actions.append("ss_tl")
        ext_actions.append("da_el")
        ext_actions.append("da_ep")
        ext_actions.append("da_te")
        ext_actions.append("da_et")
        ext_actions.append("pr_da")
        for n in range(len(srt_actions)):
            if srt_actions[n][0] in ext_actions:
                origin = srt_actions[n][2]
                if (
                    srt_actions[n][0] == "js_cl"
                    or srt_actions[n][0] == "js_ca"
                ):
                    origin = srt_actions[n][2][1]
                if origin.endswith("/"):
                    origin = origin[0:-1]
                if srt_actions[n][0] == "js_ty":
                    srt_actions[n][2] = srt_actions[n][1][1]
                    srt_actions[n][1] = srt_actions[n][1][0]
                if srt_actions[n][0] == "e_mfa":
                    srt_actions[n][2] = srt_actions[n][1][1]
                    srt_actions[n][1] = srt_actions[n][1][0]
                if srt_actions[n][0] == "_url_" and origin not in origins:
                    origins.append(origin)
                if origin not in origins:
                    srt_actions[n][0] = "_skip"
        for n in range(len(srt_actions)):
            if (
                srt_actions[n][0] == "input"
                and n > 0
                and srt_actions[n - 1][0] == "js_ty"
                and srt_actions[n][2] == srt_actions[n - 1][2]
            ):
                srt_actions[n][0] = "_skip"
        for n in range(len(srt_actions)):
            cleaned_actions.append(srt_actions[n])
        for action in srt_actions:
            if action[0] == "begin" or action[0] == "_url_":
                if "%" in action[2] and python3:
                    try:
                        from urllib.parse import unquote

                        action[2] = unquote(action[2], errors="strict")
                    except Exception:
                        pass
                if '"' not in action[2]:
                    sb_actions.append('self.open("%s")' % action[2])
                elif "'" not in action[2]:
                    sb_actions.append("self.open('%s')" % action[2])
                else:
                    sb_actions.append(
                        'self.open("%s")' % action[2].replace('"', '\\"')
                    )
            elif action[0] == "f_url":
                if "%" in action[2] and python3:
                    try:
                        from urllib.parse import unquote

                        action[2] = unquote(action[2], errors="strict")
                    except Exception:
                        pass
                if '"' not in action[2]:
                    sb_actions.append('self.open_if_not_url("%s")' % action[2])
                elif "'" not in action[2]:
                    sb_actions.append("self.open_if_not_url('%s')" % action[2])
                else:
                    sb_actions.append(
                        'self.open_if_not_url("%s")'
                        % action[2].replace('"', '\\"')
                    )
            elif action[0] == "click":
                method = "click"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "js_cl":
                method = "js_click"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "js_ca":
                method = "js_click_all"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "canva":
                method = "click_with_offset"
                selector = action[1][0]
                p_x = action[1][1]
                p_y = action[1][2]
                if '"' not in selector:
                    sb_actions.append(
                        'self.%s("%s", %s, %s)' % (method, selector, p_x, p_y)
                    )
                else:
                    sb_actions.append(
                        "self.%s('%s', %s, %s)" % (method, selector, p_x, p_y)
                    )
            elif action[0] == "input" or action[0] == "js_ty":
                method = "type"
                if action[0] == "js_ty":
                    method = "js_type"
                text = action[2].replace("\n", "\\n")
                if '"' not in action[1] and '"' not in text:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, action[1], text)
                    )
                elif '"' not in action[1] and '"' in text:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')' % (method, action[1], text)
                    )
                elif '"' in action[1] and '"' not in text:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")' % (method, action[1], text)
                    )
                elif '"' in action[1] and '"' in text:
                    sb_actions.append(
                        "self.%s('%s', '%s')" % (method, action[1], text)
                    )
            elif action[0] == "e_mfa":
                method = "enter_mfa_code"
                text = action[2].replace("\n", "\\n")
                if '"' not in action[1] and '"' not in text:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, action[1], text)
                    )
                elif '"' not in action[1] and '"' in text:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')' % (method, action[1], text)
                    )
                elif '"' in action[1] and '"' not in text:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")' % (method, action[1], text)
                    )
                elif '"' in action[1] and '"' in text:
                    sb_actions.append(
                        "self.%s('%s', '%s')" % (method, action[1], text)
                    )
            elif action[0] == "h_clk":
                method = "hover_and_click"
                if '"' not in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, action[1], action[2])
                    )
                elif '"' not in action[1] and '"' in action[2]:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' in action[2]:
                    sb_actions.append(
                        "self.%s('%s', '%s')" % (method, action[1], action[2])
                    )
            elif action[0] == "ddrop":
                method = "drag_and_drop"
                if '"' not in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, action[1], action[2])
                    )
                elif '"' not in action[1] and '"' in action[2]:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' in action[2]:
                    sb_actions.append(
                        "self.%s('%s', '%s')" % (method, action[1], action[2])
                    )
            elif action[0] == "s_opt":
                method = "select_option_by_text"
                if '"' not in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, action[1], action[2])
                    )
                elif '"' not in action[1] and '"' in action[2]:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' in action[2]:
                    sb_actions.append(
                        "self.%s('%s', '%s')" % (method, action[1], action[2])
                    )
            elif action[0] == "set_v":
                method = "set_value"
                if '"' not in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, action[1], action[2])
                    )
                elif '"' not in action[1] and '"' in action[2]:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' in action[2]:
                    sb_actions.append(
                        "self.%s('%s', '%s')" % (method, action[1], action[2])
                    )
            elif action[0] == "cho_f":
                method = "choose_file"
                action[2] = action[2].replace("\\", "\\\\")
                if '"' not in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, action[1], action[2])
                    )
                elif '"' not in action[1] and '"' in action[2]:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' not in action[2]:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")'
                        % (method, action[1], action[2])
                    )
                elif '"' in action[1] and '"' in action[2]:
                    sb_actions.append(
                        "self.%s('%s', '%s')" % (method, action[1], action[2])
                    )
            elif action[0] == "sw_fr":
                method = "switch_to_frame"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "sw_dc":
                sb_actions.append("self.switch_to_default_content()")
            elif action[0] == "sw_pf":
                sb_actions.append("self.switch_to_parent_frame()")
            elif action[0] == "s_c_f":
                method = "set_content_to_frame"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "s_c_d":
                method = "set_content_to_default"
                nested = action[1]
                if nested:
                    method = "set_content_to_parent"
                    sb_actions.append("self.%s()" % method)
                else:
                    sb_actions.append("self.%s()" % method)
            elif action[0] == "sleep":
                method = "sleep"
                sb_actions.append("self.%s(%s)" % (method, action[1]))
            elif action[0] == "wf_el":
                method = "wait_for_element"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "as_el":
                method = "assert_element"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "as_ep":
                method = "assert_element_present"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "asenv":
                method = "assert_element_not_visible"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "hi_li":
                method = "highlight"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "as_lt":
                method = "assert_link_text"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "as_ti":
                method = "assert_title"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "as_tc":
                method = "assert_title_contains"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "as_df":
                method = "assert_downloaded_file"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "do_fi":
                method = "download_file"
                file_url = action[1][0]
                dest = action[1][1]
                if not dest:
                    sb_actions.append('self.%s("%s")' % (method, file_url))
                else:
                    sb_actions.append(
                        'self.%s("%s", "%s")' % (method, file_url, dest)
                    )
            elif action[0] == "as_at":
                method = "assert_attribute"
                if ('"' not in action[1][0]) and action[1][2]:
                    sb_actions.append(
                        'self.%s("%s", "%s", "%s")'
                        % (method, action[1][0], action[1][1], action[1][2])
                    )
                elif ('"' not in action[1][0]) and not action[1][2]:
                    sb_actions.append(
                        'self.%s("%s", "%s")'
                        % (method, action[1][0], action[1][1])
                    )
                elif ('"' in action[1][0]) and action[1][2]:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s", "%s")'
                        % (method, action[1][0], action[1][1], action[1][2])
                    )
                else:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")'
                        % (method, action[1][0], action[1][1])
                    )
            elif (
                action[0] == "as_te"
                or action[0] == "as_et"
                or action[0] == "astnv"
                or action[0] == "da_te"
                or action[0] == "da_et"
            ):
                import unicodedata

                action[1][0] = unicodedata.normalize("NFKC", action[1][0])
                action[1][0] = action[1][0].replace("\n", "\\n")
                method = "assert_text"
                if action[0] == "as_et":
                    method = "assert_exact_text"
                elif action[0] == "astnv":
                    method = "assert_text_not_visible"
                elif action[0] == "da_te":
                    method = "deferred_assert_text"
                elif action[0] == "da_et":
                    method = "deferred_assert_exact_text"
                if action[1][1] != "html":
                    if '"' not in action[1][0] and '"' not in action[1][1]:
                        sb_actions.append(
                            'self.%s("%s", "%s")'
                            % (method, action[1][0], action[1][1])
                        )
                    elif '"' not in action[1][0] and '"' in action[1][1]:
                        sb_actions.append(
                            'self.%s("%s", \'%s\')'
                            % (method, action[1][0], action[1][1])
                        )
                    elif '"' in action[1] and '"' not in action[1][1]:
                        sb_actions.append(
                            'self.%s(\'%s\', "%s")'
                            % (method, action[1][0], action[1][1])
                        )
                    elif '"' in action[1] and '"' in action[1][1]:
                        sb_actions.append(
                            "self.%s('%s', '%s')"
                            % (method, action[1][0], action[1][1])
                        )
                else:
                    if '"' not in action[1][0]:
                        sb_actions.append(
                            'self.%s("%s")' % (method, action[1][0])
                        )
                    else:
                        sb_actions.append(
                            "self.%s('%s')" % (method, action[1][0])
                        )
            elif action[0] == "da_el":
                method = "deferred_assert_element"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "da_ep":
                method = "deferred_assert_element_present"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))
            elif action[0] == "ss_tl":
                method = "save_screenshot_to_logs"
                sb_actions.append("self.%s()" % method)
            elif action[0] == "sh_fc":
                method = "show_file_choosers"
                sb_actions.append("self.%s()" % method)
            elif action[0] == "pr_da":
                sb_actions.append("self.process_deferred_asserts()")
            elif action[0] == "c_l_s":
                sb_actions.append("self.clear_local_storage()")
            elif action[0] == "c_s_s":
                sb_actions.append("self.clear_session_storage()")
            elif action[0] == "d_a_c":
                sb_actions.append("self.delete_all_cookies()")
            elif action[0] == "go_bk":
                sb_actions.append("self.go_back()")
            elif action[0] == "go_fw":
                sb_actions.append("self.go_forward()")
            elif action[0] == "c_box":
                method = "check_if_unchecked"
                if action[2] == "no":
                    method = "uncheck_if_checked"
                if '"' not in action[1]:
                    sb_actions.append('self.%s("%s")' % (method, action[1]))
                else:
                    sb_actions.append("self.%s('%s')" % (method, action[1]))

        filename = self.__get_filename()
        classname = self.__class__.__name__
        methodname = self._testMethodName
        context_filename = None
        if (
            hasattr(sb_config, "is_context_manager")
            and sb_config.is_context_manager
            and (filename == "base_case.py" or methodname == "runTest")
        ):
            import traceback

            stack_base = traceback.format_stack()[0].split(os.sep)[-1]
            test_base = stack_base.split(", in ")[0]
            if hasattr(self, "cm_filename") and self.cm_filename:
                filename = self.cm_filename
            else:
                filename = test_base.split('"')[0]
            classname = "SB"
            methodname = "test_line_" + test_base.split(", line ")[-1]
            context_filename = filename.split(".")[0] + "_rec.py"
        if hasattr(self, "is_behave") and self.is_behave:
            classname = sb_config.behave_feature.name
            classname = classname.replace("/", " ").replace(" & ", " ")
            classname = re.sub(r"[^\w" + r"_ " + r"]", "", classname)
            classname_parts = classname.split(" ")
            new_classname = ""
            for part in classname_parts:
                new_classname += (part[0].upper() + part[1:])
            classname = new_classname
            methodname = sb_config.behave_scenario.name
            methodname = methodname.replace("/", "_").replace(" & ", "_")
            methodname = methodname.replace(" + ", " plus ")
            methodname = methodname.replace(" - ", " minus ")
            methodname = methodname.replace(" × ", " times ")
            methodname = methodname.replace(" ÷ ", " divided by ")
            methodname = methodname.replace(" = ", " equals ")
            methodname = methodname.replace(" %% ", " percent ")
            methodname = re.sub(r"[^\w" + r"_ " + r"]", "", methodname)
            methodname = methodname.replace(" _ ", "_").lower()
            methodname = methodname.replace(" ", "_").lower()
            if not methodname.startswith("test_"):
                methodname = "test_" + methodname
        new_file = False
        data = []
        if filename not in sb_config._recorded_actions:
            new_file = True
            sb_config._recorded_actions[filename] = []
            data.append("from seleniumbase import BaseCase")
            data.append("")
            data.append("")
            data.append("class %s(BaseCase):" % classname)
        else:
            data = sb_config._recorded_actions[filename]
        data.append("    def %s(self):" % methodname)
        if len(sb_actions) > 0:
            for action in sb_actions:
                data.append("        " + action)
        else:
            data.append("        pass")
        data.append("")
        sb_config._recorded_actions[filename] = data

        recordings_folder = constants.Recordings.SAVED_FOLDER
        if recordings_folder.endswith("/"):
            recordings_folder = recordings_folder[:-1]
        if not os.path.exists(recordings_folder):
            try:
                os.makedirs(recordings_folder)
            except Exception:
                pass

        file_name = self.__class__.__module__.split(".")[-1] + "_rec.py"
        if hasattr(self, "is_behave") and self.is_behave:
            file_name = sb_config.behave_scenario.filename.replace(".", "_")
            file_name = file_name.split("/")[-1].split("\\")[-1]
            file_name = file_name + "_rec.py"
        elif context_filename:
            file_name = context_filename
        file_path = os.path.join(recordings_folder, file_name)
        out_file = codecs.open(file_path, "w+", "utf-8")
        out_file.writelines("\r\n".join(data))
        out_file.close()
        rec_message = ">>> RECORDING SAVED as: "
        if not new_file:
            rec_message = ">>> RECORDING ADDED to: "
        star_len = len(rec_message) + len(file_path)
        try:
            terminal_size = os.get_terminal_size().columns
            if terminal_size > 30 and star_len > terminal_size:
                star_len = terminal_size
        except Exception:
            pass
        spc = "\n\n"
        if hasattr(self, "rec_print") and self.rec_print:
            spc = ""
            print()
            if " " not in file_path:
                os.system("sbase print %s -n" % file_path)
            elif '"' not in file_path:
                os.system('sbase print "%s" -n' % file_path)
            else:
                os.system("sbase print '%s' -n" % file_path)
        stars = "*" * star_len
        c1 = ""
        c2 = ""
        cr = ""
        if "linux" not in sys.platform:
            colorama.init(autoreset=True)
            c1 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
            c2 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTYELLOW_EX
            cr = colorama.Style.RESET_ALL
            rec_message = rec_message.replace(">>>", c2 + ">>>" + cr)
        print("%s%s%s%s%s\n%s" % (spc, rec_message, c1, file_path, cr, stars))
        if hasattr(self, "rec_behave") and self.rec_behave:
            # Also generate necessary behave-gherkin files.
            self.__process_recorded_behave_actions(srt_actions, colorama)

    def __process_recorded_behave_actions(self, srt_actions, colorama):
        from seleniumbase.behave import behave_helper

        behave_actions = behave_helper.generate_gherkin(srt_actions)
        filename = self.__get_filename()
        feature_class = None
        scenario_test = None
        if hasattr(self, "is_behave") and self.is_behave:
            feature_class = sb_config.behave_feature.name
            scenario_test = sb_config.behave_scenario.name
        else:
            feature_class = self.__class__.__name__
            scenario_test = self._testMethodName
        new_file = False
        data = []
        if filename not in sb_config._behave_recorded_actions:
            new_file = True
            sb_config._behave_recorded_actions[filename] = []
            data.append("Feature: %s" % feature_class)
            data.append("")
        else:
            data = sb_config._behave_recorded_actions[filename]
        data.append("  Scenario: %s" % scenario_test)
        if len(behave_actions) > 0:
            count = 0
            for action in behave_actions:
                if count == 0:
                    data.append("    Given " + action)
                else:
                    data.append("    And " + action)
                count += 1
        data.append("")
        sb_config._behave_recorded_actions[filename] = data

        recordings_folder = constants.Recordings.SAVED_FOLDER
        if recordings_folder.endswith("/"):
            recordings_folder = recordings_folder[:-1]
        if not os.path.exists(recordings_folder):
            try:
                os.makedirs(recordings_folder)
            except Exception:
                pass
        features_folder = os.path.join(recordings_folder, "features")
        if not os.path.exists(features_folder):
            try:
                os.makedirs(features_folder)
            except Exception:
                pass
        steps_folder = os.path.join(features_folder, "steps")
        if not os.path.exists(steps_folder):
            try:
                os.makedirs(steps_folder)
            except Exception:
                pass

        file_name = filename.split(".")[0] + "_rec.feature"
        if hasattr(self, "is_behave") and self.is_behave:
            file_name = sb_config.behave_scenario.filename.replace(".", "_")
            file_name = file_name.split("/")[-1].split("\\")[-1]
            file_name = file_name + "_rec.feature"
        file_path = os.path.join(features_folder, file_name)
        out_file = codecs.open(file_path, "w+", "utf-8")
        out_file.writelines("\r\n".join(data))
        out_file.close()

        rec_message = ">>> RECORDING SAVED as: "
        if not new_file:
            rec_message = ">>> RECORDING ADDED to: "
        star_len = len(rec_message) + len(file_path)
        try:
            terminal_size = os.get_terminal_size().columns
            if terminal_size > 30 and star_len > terminal_size:
                star_len = terminal_size
        except Exception:
            pass
        spc = "\n"
        if hasattr(self, "rec_print") and self.rec_print:
            spc = ""
            print()
            if " " not in file_path:
                os.system("sbase print %s -n" % file_path)
            elif '"' not in file_path:
                os.system('sbase print "%s" -n' % file_path)
            else:
                os.system("sbase print '%s' -n" % file_path)
        stars = "*" * star_len
        c1 = ""
        c2 = ""
        cr = ""
        if "linux" not in sys.platform:
            colorama.init(autoreset=True)
            c1 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
            c2 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTYELLOW_EX
            cr = colorama.Style.RESET_ALL
            rec_message = rec_message.replace(">>>", c2 + ">>>" + cr)
        print("%s%s%s%s%s\n%s" % (spc, rec_message, c1, file_path, cr, stars))

        data = []
        data.append("")
        file_name = "__init__.py"
        file_path = os.path.join(features_folder, file_name)
        if not os.path.exists(file_path):
            out_file = codecs.open(file_path, "w+", "utf-8")
            out_file.writelines("\r\n".join(data))
            out_file.close()
            print("Created recordings/features/__init__.py")

        data = []
        data.append("[behave]")
        data.append("show_skipped=false")
        data.append("show_timings=false")
        data.append("")
        file_name = "behave.ini"
        file_path = os.path.join(features_folder, file_name)
        if not os.path.exists(file_path):
            out_file = codecs.open(file_path, "w+", "utf-8")
            out_file.writelines("\r\n".join(data))
            out_file.close()
            print("Created recordings/features/behave.ini")

        data = []
        data.append("from seleniumbase import BaseCase")
        data.append("from seleniumbase.behave import behave_sb")
        data.append(
            "behave_sb.set_base_class(BaseCase)  # Accepts a BaseCase subclass"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import before_all  # noqa"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import before_feature  # noqa"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import before_scenario  # noqa"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import before_step  # noqa"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import after_step  # noqa"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import after_scenario  # noqa"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import after_feature  # noqa"
        )
        data.append(
            "from seleniumbase.behave.behave_sb import after_all  # noqa"
        )
        data.append("")
        file_name = "environment.py"
        file_path = os.path.join(features_folder, file_name)
        if not os.path.exists(file_path):
            out_file = codecs.open(file_path, "w+", "utf-8")
            out_file.writelines("\r\n".join(data))
            out_file.close()
            print("Created recordings/features/environment.py")

        data = []
        data.append("")
        file_name = "__init__.py"
        file_path = os.path.join(steps_folder, file_name)
        if not os.path.exists(file_path):
            out_file = codecs.open(file_path, "w+", "utf-8")
            out_file.writelines("\r\n".join(data))
            out_file.close()
            print("Created recordings/features/steps/__init__.py")

        data = []
        data.append("from seleniumbase.behave import steps  # noqa")
        data.append("")
        file_name = "imported.py"
        file_path = os.path.join(steps_folder, file_name)
        if not os.path.exists(file_path):
            out_file = codecs.open(file_path, "w+", "utf-8")
            out_file.writelines("\r\n".join(data))
            out_file.close()
            print("Created recordings/features/steps/imported.py")

    def bring_active_window_to_front(self):
        """Brings the active browser window to the front.
        This is useful when multiple drivers are being used."""
        self.__check_scope()
        try:
            if not self.__is_in_frame():
                # Only bring the window to the front if not in a frame
                # because the driver resets itself to default content.
                self.switch_to_window(self.driver.current_window_handle)
        except Exception:
            pass

    def bring_to_front(self, selector, by="css selector"):
        """Updates the Z-index of a page element to bring it into view.
        Useful when getting a WebDriverException, such as the one below:
            { Element is not clickable at point (#, #).
              Other element would receive the click: ... }"""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't run action if can't convert to CSS_Selector for JavaScript
            return
        selector = re.escape(selector)
        selector = self.__escape_quotes_if_needed(selector)
        script = (
            """document.querySelector('%s').style.zIndex = '999999';"""
            % selector
        )
        self.execute_script(script)

    def highlight_click(
        self, selector, by="css selector", loops=3, scroll=True
    ):
        self.__check_scope()
        if not self.demo_mode:
            self.highlight(selector, by=by, loops=loops, scroll=scroll)
        self.click(selector, by=by)

    def highlight_update_text(
        self, selector, text, by="css selector", loops=3, scroll=True
    ):
        """Highlights the element and then types text into the field."""
        self.__check_scope()
        if not self.demo_mode:
            self.highlight(selector, by=by, loops=loops, scroll=scroll)
        self.update_text(selector, text, by=by)

    def highlight_type(
        self, selector, text, by="css selector", loops=3, scroll=True
    ):
        """Same as self.highlight_update_text()
        As above, highlights the element and then types text into the field."""
        self.__check_scope()
        if not self.demo_mode:
            self.highlight(selector, by=by, loops=loops, scroll=scroll)
        self.update_text(selector, text, by=by)

    def highlight(self, selector, by="css selector", loops=None, scroll=True):
        """This method uses fancy JavaScript to highlight an element.
        Used during demo_mode.
        @Params
        selector - the selector of the element to find
        by - the type of selector to search by (Default: CSS)
        loops - # of times to repeat the highlight animation
                (Default: 4. Each loop lasts for about 0.18s)
        scroll - the option to scroll to the element first (Default: True)
        """
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by, xp_ok=False)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        if not loops:
            loops = settings.HIGHLIGHTS
        if scroll:
            try:
                if self.browser != "safari":
                    scroll_distance = js_utils.get_scroll_distance_to_element(
                        self.driver, element
                    )
                    if abs(scroll_distance) > constants.Values.SSMD:
                        self.__jquery_slow_scroll_to(selector, by)
                    else:
                        self.__slow_scroll_to_element(element)
                else:
                    self.__jquery_slow_scroll_to(selector, by)
            except Exception:
                self.wait_for_ready_state_complete()
                time.sleep(0.12)
                element = self.wait_for_element_visible(
                    selector, by=by, timeout=settings.SMALL_TIMEOUT
                )
                self.__slow_scroll_to_element(element)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't highlight if can't convert to CSS_SELECTOR
            return

        if self.highlights:
            loops = self.highlights
        if self.browser == "ie":
            loops = 1  # Override previous setting because IE is slow
        loops = int(loops)
        if self.headless or self.headless2 or self.xvfb:
            # Headless modes have less need for highlighting elements.
            # However, highlight() may be used as a sleep alternative.
            loops = int(math.ceil(loops * 0.5))

        o_bs = ""  # original_box_shadow
        try:
            style = element.get_attribute("style")
        except Exception:
            self.wait_for_ready_state_complete()
            time.sleep(0.12)
            element = self.wait_for_element_visible(
                selector, by="css selector", timeout=settings.SMALL_TIMEOUT
            )
            style = element.get_attribute("style")
        if style:
            if "box-shadow: " in style:
                box_start = style.find("box-shadow: ")
                box_end = style.find(";", box_start) + 1
                original_box_shadow = style[box_start:box_end]
                o_bs = original_box_shadow

        orig_selector = selector
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
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["hi_li", orig_selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        time.sleep(0.065)

    def press_up_arrow(self, selector="html", times=1, by="css selector"):
        """Simulates pressing the UP Arrow on the keyboard.
        By default, "html" will be used as the CSS Selector target.
        You can specify how many times in-a-row the action happens."""
        self.__check_scope()
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

    def press_down_arrow(self, selector="html", times=1, by="css selector"):
        """Simulates pressing the DOWN Arrow on the keyboard.
        By default, "html" will be used as the CSS Selector target.
        You can specify how many times in-a-row the action happens."""
        self.__check_scope()
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

    def press_left_arrow(self, selector="html", times=1, by="css selector"):
        """Simulates pressing the LEFT Arrow on the keyboard.
        By default, "html" will be used as the CSS Selector target.
        You can specify how many times in-a-row the action happens."""
        self.__check_scope()
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

    def press_right_arrow(self, selector="html", times=1, by="css selector"):
        """Simulates pressing the RIGHT Arrow on the keyboard.
        By default, "html" will be used as the CSS Selector target.
        You can specify how many times in-a-row the action happens."""
        self.__check_scope()
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

    def scroll_to(self, selector, by="css selector", timeout=None):
        """Fast scroll to destination"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if self.demo_mode or self.slow_mode:
            self.slow_scroll_to(selector, by=by, timeout=timeout)
            return
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout
        )
        try:
            self.__scroll_to_element(element, selector, by)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.12)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=timeout
            )
            self.__scroll_to_element(element, selector, by)

    def scroll_to_element(self, selector, by="css selector", timeout=None):
        self.scroll_to(selector, by=by, timeout=timeout)

    def slow_scroll_to(self, selector, by="css selector", timeout=None):
        """Slow motion scroll to destination"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        original_by = by
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_visible(
            original_selector, by=original_by, timeout=timeout
        )
        try:
            if self.browser != "safari":
                scroll_distance = js_utils.get_scroll_distance_to_element(
                    self.driver, element
                )
                if abs(scroll_distance) > constants.Values.SSMD:
                    self.__jquery_slow_scroll_to(selector, by)
                else:
                    self.__slow_scroll_to_element(element)
            else:
                self.__jquery_slow_scroll_to(selector, by)
        except Exception:
            self.wait_for_ready_state_complete()
            time.sleep(0.12)
            element = self.wait_for_element_visible(
                original_selector, by=original_by, timeout=timeout
            )
            self.__slow_scroll_to_element(element)

    def slow_scroll_to_element(
        self, selector, by="css selector", timeout=None
    ):
        self.slow_scroll_to(selector, by=by, timeout=timeout)

    def scroll_to_top(self):
        """Scroll to the top of the page."""
        self.__check_scope()
        scroll_script = "window.scrollTo(0, 0);"
        try:
            self.execute_script(scroll_script)
            time.sleep(0.012)
            return True
        except Exception:
            return False

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.__check_scope()
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
        self.click(xpath, by="xpath")

    def js_click(
        self, selector, by="css selector", all_matches=False, scroll=True
    ):
        """Clicks an element using JavaScript.
        Can be used to click hidden / invisible elements.
        If "all_matches" is False, only the first match is clicked.
        If "scroll" is False, won't scroll unless running in Demo Mode."""
        self.wait_for_ready_state_complete()
        selector, by = self.__recalculate_selector(selector, by, xp_ok=False)
        if by == By.LINK_TEXT:
            message = (
                "Pure JavaScript doesn't support clicking by Link Text. "
                "You may want to use self.jquery_click() instead, which "
                "allows this with :contains(), assuming jQuery isn't blocked. "
                "For now, self.js_click() will use a regular WebDriver click."
            )
            logging.debug(message)
            self.click(selector, by=by)
            return
        element = self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        if not page_actions.is_element_clickable(self.driver, selector, by):
            self.wait_for_ready_state_complete()
        scroll_done = False
        if self.is_element_visible(selector, by=by):
            scroll_done = True
            self.__demo_mode_highlight_if_active(selector, by)
            if scroll and not self.demo_mode and not self.slow_mode:
                success = js_utils.scroll_to_element(self.driver, element)
                if not success:
                    self.wait_for_ready_state_complete()
                    timeout = settings.SMALL_TIMEOUT
                    element = page_actions.wait_for_element_present(
                        self.driver, selector, by, timeout=timeout
                    )
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        action = None
        pre_action_url = self.driver.current_url
        pre_window_count = len(self.driver.window_handles)
        if self.recorder_mode and not self.__dont_record_js_click:
            time_stamp = self.execute_script("return Date.now();")
            tag_name = None
            href = ""
            if ":contains\\(" not in css_selector:
                tag_name = self.execute_script(
                    "return document.querySelector('%s').tagName.toLowerCase()"
                    ";" % css_selector
                )
            if tag_name == "a":
                href = self.execute_script(
                    "return document.querySelector('%s').href;" % css_selector
                )
            origin = self.get_origin()
            href_origin = [href, origin]
            action = ["js_cl", selector, href_origin, time_stamp]
            if all_matches:
                action[0] = "js_ca"
        if not self.is_element_visible(selector, by=by):
            self.wait_for_ready_state_complete()
            if self.is_element_visible(selector, by=by):
                if scroll and not scroll_done:
                    success = js_utils.scroll_to_element(self.driver, element)
                    if not success:
                        timeout = settings.SMALL_TIMEOUT
                        element = page_actions.wait_for_element_present(
                            self.driver, selector, by, timeout=timeout
                        )
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
        if self.recorder_mode and action:
            self.__extra_actions.append(action)
        latest_window_count = len(self.driver.window_handles)
        if (
            latest_window_count > pre_window_count
            and (
                self.recorder_mode
                or (
                    settings.SWITCH_TO_NEW_TABS_ON_CLICK
                    and self.driver.current_url == pre_action_url
                )
            )
        ):
            self.__switch_to_newest_window_if_not_blank()
        elif (
            latest_window_count == pre_window_count - 1
            and latest_window_count > 0
        ):
            # If a click closes the active window,
            # switch to the last one if it exists.
            self.switch_to_window(-1)
        try:
            self.wait_for_ready_state_complete()
        except Exception:
            pass
        self.__demo_mode_pause_if_active()

    def js_click_if_present(self, selector, by="css selector", timeout=0):
        """If the page selector exists, js_click() the element.
        This method only clicks on the first matching element found.
        If a "timeout" is provided, waits that long for the element to
        be present before giving up and returning without a js_click()."""
        self.wait_for_ready_state_complete()
        if self.is_element_present(selector, by=by):
            self.js_click(selector, by=by)
        elif timeout > 0:
            try:
                self.wait_for_element_present(
                    selector, by=by, timeout=timeout
                )
            except Exception:
                pass
            if self.is_element_present(selector, by=by):
                self.js_click(selector, by=by)

    def js_click_if_visible(self, selector, by="css selector", timeout=0):
        """If the page selector exists and is visible, js_click() the element.
        This method only clicks on the first matching element found.
        If a "timeout" is provided, waits that long for the element
        to appear before giving up and returning without a js_click()."""
        self.wait_for_ready_state_complete()
        if self.is_element_visible(selector, by=by):
            self.js_click(selector, by=by)
        elif timeout > 0:
            try:
                self.wait_for_element_visible(
                    selector, by=by, timeout=timeout
                )
            except Exception:
                pass
            if self.is_element_visible(selector, by=by):
                self.js_click(selector, by=by)

    def js_click_all(self, selector, by="css selector"):
        """Clicks all matching elements using pure JS. (No jQuery)"""
        self.js_click(selector, by="css selector", all_matches=True)

    def jquery_click(self, selector, by="css selector"):
        """Clicks an element using jQuery. (Different from using pure JS.)
        Can be used to click hidden / invisible elements."""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by, xp_ok=False)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        click_script = """jQuery('%s')[0].click();""" % selector
        self.safe_execute_script(click_script)
        self.__demo_mode_pause_if_active()

    def jquery_click_all(self, selector, by="css selector"):
        """Clicks all matching elements using jQuery."""
        self.__check_scope()
        selector, by = self.__recalculate_selector(selector, by, xp_ok=False)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        click_script = """jQuery('%s').click();""" % css_selector
        self.safe_execute_script(click_script)
        self.__demo_mode_pause_if_active()

    def hide_element(self, selector, by="css selector"):
        """Hide the first element on the page that matches the selector."""
        self.__check_scope()
        try:
            self.wait_for_element_visible("body", timeout=1.5)
            self.wait_for_element_present(selector, by=by, timeout=0.5)
        except Exception:
            pass
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        if ":contains(" in css_selector:
            selector = self.__make_css_match_first_element_only(css_selector)
            script = """jQuery('%s').hide();""" % selector
            self.safe_execute_script(script)
        else:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = (
                'const e = document.querySelector("%s");'
                'e.style.display="none";e.style.visibility="hidden";'
                % css_selector)
            self.execute_script(script)

    def hide_elements(self, selector, by="css selector"):
        """Hide all elements on the page that match the selector."""
        self.__check_scope()
        try:
            self.wait_for_element_visible("body", timeout=1.5)
        except Exception:
            pass
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        if ":contains(" in css_selector:
            script = """jQuery('%s').hide();""" % css_selector
            self.safe_execute_script(script)
        else:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = (
                """var $elements = document.querySelectorAll('%s');
                var index = 0, length = $elements.length;
                for(; index < length; index++){
                $elements[index].style.display="none";
                $elements[index].style.visibility="hidden";}"""
                % css_selector
            )
            self.execute_script(script)

    def show_element(self, selector, by="css selector"):
        """Show the first element on the page that matches the selector."""
        self.__check_scope()
        try:
            self.wait_for_element_visible("body", timeout=1.5)
            self.wait_for_element_present(selector, by=by, timeout=1)
        except Exception:
            pass
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        if ":contains(" in css_selector:
            selector = self.__make_css_match_first_element_only(css_selector)
            script = """jQuery('%s').show(0);""" % selector
            self.safe_execute_script(script)
        else:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = (
                'const e = document.querySelector("%s");'
                'e.style.display="";e.style.visibility="visible";'
                % css_selector
            )
            self.execute_script(script)

    def show_elements(self, selector, by="css selector"):
        """Show all elements on the page that match the selector."""
        self.__check_scope()
        try:
            self.wait_for_element_visible("body", timeout=1.5)
        except Exception:
            pass
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        if ":contains(" in css_selector:
            script = """jQuery('%s').show(0);""" % css_selector
            self.safe_execute_script(script)
        else:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = (
                """var $elements = document.querySelectorAll('%s');
                var index = 0, length = $elements.length;
                for(; index < length; index++){
                $elements[index].style.display="";
                $elements[index].style.visibility="visible";}"""
                % css_selector
            )
            self.execute_script(script)

    def remove_element(self, selector, by="css selector"):
        """Remove the first element on the page that matches the selector."""
        self.__check_scope()
        try:
            self.wait_for_element_visible("body", timeout=1.5)
            self.wait_for_element_present(selector, by=by, timeout=0.5)
        except Exception:
            pass
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        if ":contains(" in css_selector:
            selector = self.__make_css_match_first_element_only(css_selector)
            script = """jQuery('%s').remove();""" % selector
            self.safe_execute_script(script)
        else:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = (
                'const e = document.querySelector("%s");'
                'e.parentElement.removeChild(e);'
                % css_selector
            )
            self.execute_script(script)

    def remove_elements(self, selector, by="css selector"):
        """Remove all elements on the page that match the selector."""
        self.__check_scope()
        try:
            self.wait_for_element_visible("body", timeout=1.5)
        except Exception:
            pass
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        if ":contains(" in css_selector:
            script = """jQuery('%s').remove();""" % css_selector
            self.safe_execute_script(script)
        else:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = (
                """var $elements = document.querySelectorAll('%s');
                var index = 0, length = $elements.length;
                for(; index < length; index++){
                $elements[index].remove();}"""
                % css_selector
            )
            self.execute_script(script)

    def ad_block(self):
        """Block ads that appear on the current web page."""
        from seleniumbase.config import ad_block_list

        self.__check_scope()  # Using wait_for_RSC would cause an infinite loop
        for css_selector in ad_block_list.AD_BLOCK_LIST:
            css_selector = re.escape(css_selector)  # Add "\\" to special chars
            css_selector = self.__escape_quotes_if_needed(css_selector)
            script = (
                """var $elements = document.querySelectorAll('%s');
                var index = 0, length = $elements.length;
                for(; index < length; index++){
                $elements[index].remove();}"""
                % css_selector
            )
            try:
                self.execute_script(script)
            except Exception:
                pass  # Don't fail test if ad_blocking fails

    def show_file_choosers(self):
        """Display hidden file-chooser input fields on sites if present."""
        self.wait_for_ready_state_complete()
        css_selector = 'input[type="file"]'
        try:
            self.wait_for_element_present(
                css_selector, timeout=settings.MINI_TIMEOUT
            )
        except Exception:
            pass
        if self.__needs_minimum_wait():
            time.sleep(0.05)
        try:
            self.show_elements(css_selector)
        except Exception:
            pass
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = (
            """var $elements = document.querySelectorAll('%s');
            var index = 0, length = $elements.length;
            for(; index < length; index++){
            the_class = $elements[index].getAttribute('class');
            new_class = the_class.replaceAll('hidden', 'visible');
            $elements[index].setAttribute('class', new_class);}"""
            % css_selector
        )
        try:
            self.execute_script(script)
        except Exception:
            pass
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["sh_fc", "", origin, time_stamp]
                        self.__extra_actions.append(action)

    def disable_beforeunload(self):
        """This prevents: "Leave Site? Changes you made may not be saved."
                          on Chromium browsers (Chrome or Edge).
        SB already sets "dom.disable_beforeunload" for Firefox options."""
        self.__check_scope()
        self.__check_browser()
        if (
            self.is_chromium()
            and self.driver.current_url.startswith("http")
        ):
            try:
                self.driver.execute_script("window.onbeforeunload=null;")
            except Exception:
                pass

    def get_domain_url(self, url):
        self.__check_scope()
        return page_utils.get_domain_url(url)

    def get_beautiful_soup(self, source=None):
        """BeautifulSoup is a toolkit for dissecting an HTML document
        and extracting what you need. It's great for screen-scraping!
        See: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        """
        from bs4 import BeautifulSoup

        if not source:
            try:
                self.wait_for_element_visible(
                    "body", timeout=settings.MINI_TIMEOUT
                )
            except Exception:
                pass
            source = self.get_page_source()
        soup = BeautifulSoup(source, "html.parser")
        return soup

    def get_unique_links(self):
        """Get all unique links in the html of the page source.
        Page links include those obtained from:
        "a"->"href", "img"->"src", "link"->"href", and "script"->"src".
        """
        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.05)
            if self.undetectable:
                time.sleep(0.05)
        try:
            self.wait_for_element_present("body", timeout=1.5)
            self.wait_for_element_visible("body", timeout=1.5)
        except Exception:
            pass
        if self.__needs_minimum_wait():
            time.sleep(0.25)
            if self.undetectable:
                time.sleep(0.123)
        soup = self.get_beautiful_soup(self.get_page_source())
        page_url = self.get_current_url()
        links = page_utils._get_unique_links(page_url, soup)
        return links

    def get_link_status_code(
        self,
        link,
        allow_redirects=False,
        timeout=5,
        verify=False,
    ):
        """Get the status code of a link.
        If the timeout is set to less than 1, it becomes 1.
        If the timeout is exceeded by requests.head(), it will return a 404.
        If "verify" is False, will ignore certificate errors.
        For a list of available status codes, see:
        https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        """
        if self.__requests_timeout:
            timeout = self.__requests_timeout
        if timeout < 1:
            timeout = 1
        status_code = page_utils._get_link_status_code(
            link,
            allow_redirects=allow_redirects,
            timeout=timeout,
            verify=verify,
        )
        return status_code

    def assert_link_status_code_is_not_404(self, link):
        status_code = str(self.get_link_status_code(link))
        bad_link_str = 'Error: "%s" returned a 404!' % link
        self.assertNotEqual(status_code, "404", bad_link_str)

    def __get_link_if_404_error(self, link):
        status_code = str(self.get_link_status_code(link))
        if status_code == "404":
            # Verify again to be sure. (In case of multi-threading overload.)
            status_code = str(self.get_link_status_code(link))
            if status_code == "404":
                return link
            else:
                return None
        else:
            return None

    def assert_no_404_errors(self, multithreaded=True, timeout=None):
        """Assert no 404 errors from page links obtained from:
        "a"->"href", "img"->"src", "link"->"href", and "script"->"src".
        Timeout is on a per-link basis using the "requests" library.
        If timeout is None, uses the one set in get_link_status_code().
        (That timeout value is currently set to 5 seconds per link.)
        (A 404 error represents a broken link on a web page.)
        """
        all_links = self.get_unique_links()
        links = []
        for link in all_links:
            if (
                "data:" not in link
                and "mailto:" not in link
                and "javascript:" not in link
                and "://fonts.gstatic.com" not in link
                and "://fonts.googleapis.com" not in link
                and "://googleads.g.doubleclick.net" not in link
            ):
                links.append(link)
        if timeout:
            if not type(timeout) is int and not type(timeout) is float:
                raise Exception('Expecting a numeric value for "timeout"!')
            if timeout < 0:
                raise Exception('The "timeout" cannot be a negative number!')
            self.__requests_timeout = timeout
        broken_links = []
        if multithreaded:
            from multiprocessing.dummy import Pool as ThreadPool

            pool = ThreadPool(10)
            results = pool.map(self.__get_link_if_404_error, links)
            pool.close()
            pool.join()
            for result in results:
                if result:
                    broken_links.append(result)
        else:
            broken_links = []
            for link in links:
                if self.__get_link_if_404_error(link):
                    broken_links.append(link)
        self.__requests_timeout = None  # Reset the requests.head() timeout
        if len(broken_links) > 0:
            broken_links = sorted(broken_links)
            bad_links_str = "\n".join(broken_links)
            if len(broken_links) == 1:
                self.fail("Broken link detected:\n%s" % bad_links_str)
            elif len(broken_links) > 1:
                self.fail("Broken links detected:\n%s" % bad_links_str)
        if self.demo_mode:
            a_t = "ASSERT NO 404 ERRORS"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert_no_404_errors(self._language)
            messenger_post = "%s" % a_t
            self.__highlight_with_assert_success(messenger_post, "html")

    def print_unique_links_with_status_codes(self):
        """Finds all unique links in the html of the page source
        and then prints out those links with their status codes.
        Format:  ["link"  ->  "status_code"]  (per line)
        Page links include those obtained from:
        "a"->"href", "img"->"src", "link"->"href", and "script"->"src".
        """
        page_url = self.get_current_url()
        soup = self.get_beautiful_soup(self.get_page_source())
        page_utils._print_unique_links_with_status_codes(page_url, soup)

    def __fix_unicode_conversion(self, text):
        """Fixing Chinese characters when converting from PDF to HTML."""
        text = text.replace("\u2f8f", "\u884c")
        text = text.replace("\u2f45", "\u65b9")
        text = text.replace("\u2f08", "\u4eba")
        text = text.replace("\u2f70", "\u793a")
        text = text.replace("\xe2\xbe\x8f", "\xe8\xa1\x8c")
        text = text.replace("\xe2\xbd\xb0", "\xe7\xa4\xba")
        text = text.replace("\xe2\xbe\x8f", "\xe8\xa1\x8c")
        text = text.replace("\xe2\xbd\x85", "\xe6\x96\xb9")
        return text

    def __get_type_checked_text(self, text):
        """Do type-checking on text. Then return it when valid.
        If the text is acceptable, return the text or str(text).
        If the text is not acceptable, raise a Python Exception.
        """
        if type(text) is str:
            return text
        elif type(text) is int or type(text) is float:
            return str(text)  # Convert num to string
        elif type(text) is bool:
            raise Exception("text must be a string! Boolean found!")
        elif type(text).__name__ == "NoneType":
            raise Exception("text must be a string! NoneType found!")
        elif type(text) is list:
            raise Exception("text must be a string! List found!")
        elif type(text) is tuple:
            raise Exception("text must be a string! Tuple found!")
        elif type(text) is set:
            raise Exception("text must be a string! Set found!")
        elif type(text) is dict:
            raise Exception("text must be a string! Dict found!")
        elif not python3 and type(text) is unicode:  # noqa: F821
            return text  # (For old Python versions with unicode)
        else:
            return str(text)

    def get_pdf_text(
        self,
        pdf,
        page=None,
        maxpages=None,
        password=None,
        codec="utf-8",
        wrap=False,
        nav=False,
        override=False,
        caching=True,
    ):
        """Gets text from a PDF file.
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
               from a PDF don't get broken up into separate lines when
               getting converted into text format.
        nav - If PDF is a URL, navigates to the URL in the browser first.
              (Not needed because the PDF will be downloaded anyway.)
        override - If the PDF file to be downloaded already exists in the
                   downloaded_files/ folder, that PDF will be used
                   instead of downloading it again.
        caching - If resources should be cached via pdfminer."""
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            pip_find_lock = fasteners.InterProcessLock(
                constants.PipInstall.FINDLOCK
            )
            with pip_find_lock:
                try:
                    from pdfminer.high_level import extract_text
                except Exception:
                    shared_utils.pip_install("pdfminer.six")
                    from pdfminer.high_level import extract_text
        if not password:
            password = ""
        if not maxpages:
            maxpages = 0
        if not pdf.lower().endswith(".pdf"):
            raise Exception("%s is not a PDF file! (Expecting a .pdf)" % pdf)
        file_path = None
        if page_utils.is_valid_url(pdf):
            downloads_folder = download_helper.get_downloads_folder()
            if nav:
                if self.get_current_url() != pdf:
                    self.open(pdf)
            file_name = pdf.split("/")[-1]
            file_path = os.path.join(downloads_folder, file_name)
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
            file_path,
            password="",
            page_numbers=page_search,
            maxpages=maxpages,
            caching=caching,
            codec=codec,
        )
        pdf_text = self.__fix_unicode_conversion(pdf_text)
        if wrap:
            pdf_text = pdf_text.replace(" \n", " ")
        pdf_text = pdf_text.strip()  # Remove leading and trailing whitespace
        return pdf_text

    def assert_pdf_text(
        self,
        pdf,
        text,
        page=None,
        maxpages=None,
        password=None,
        codec="utf-8",
        wrap=True,
        nav=False,
        override=False,
        caching=True,
    ):
        """Asserts text in a PDF file.
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
               from a PDF don't get broken up into separate lines when
               getting converted into text format.
        nav - If PDF is a URL, navigates to the URL in the browser first.
              (Not needed because the PDF will be downloaded anyway.)
        override - If the PDF file to be downloaded already exists in the
                   downloaded_files/ folder, that PDF will be used
                   instead of downloading it again.
        caching - If resources should be cached via pdfminer."""
        text = self.__fix_unicode_conversion(text)
        if not codec:
            codec = "utf-8"
        pdf_text = self.get_pdf_text(
            pdf,
            page=page,
            maxpages=maxpages,
            password=password,
            codec=codec,
            wrap=wrap,
            nav=nav,
            override=override,
            caching=caching,
        )
        if type(page) is int:
            if text not in pdf_text:
                raise Exception(
                    "PDF [%s] is missing expected text [%s] on "
                    "page [%s]!" % (pdf, text, page)
                )
        else:
            if text not in pdf_text:
                raise Exception(
                    "PDF [%s] is missing expected text [%s]!" % (pdf, text)
                )
        return True

    def create_folder(self, folder):
        """Creates a folder of the given name if it doesn't already exist."""
        if folder.endswith("/"):
            folder = folder[:-1]
        if len(folder) < 1:
            raise Exception("Minimum folder name length = 1.")
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception:
                pass

    def choose_file(
        self, selector, file_path, by="css selector", timeout=None
    ):
        """This method is used to choose a file to upload to a website.
        It works by populating a file-chooser "input" field of type="file".
        A relative file_path will get converted into an absolute file_path.

        Example usage:
            self.choose_file('input[type="file"]', "my_dir/my_file.txt")
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        abs_path = os.path.abspath(file_path)
        element = self.wait_for_element_present(
            selector, by=by, timeout=timeout
        )
        if self.is_element_visible(selector, by=by):
            self.__demo_mode_highlight_if_active(selector, by)
            if not self.demo_mode and not self.slow_mode:
                self.__scroll_to_element(element, selector, by)
        else:
            choose_file_selector = 'input[type="file"]'
            if self.is_element_present(choose_file_selector):
                if not self.is_element_visible(choose_file_selector):
                    self.show_file_choosers()
                    if self.is_element_visible(selector, by=by):
                        self.__demo_mode_highlight_if_active(selector, by)
                        if not self.demo_mode and not self.slow_mode:
                            self.__scroll_to_element(element, selector, by)
        pre_action_url = self.driver.current_url
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        sele_file_path = [selector, file_path]
                        action = ["chfil", sele_file_path, origin, time_stamp]
                        self.__extra_actions.append(action)
        if type(abs_path) is int or type(abs_path) is float:
            abs_path = str(abs_path)
        try:
            if self.browser == "safari":
                try:
                    element.send_keys(abs_path)
                except NoSuchElementException:
                    pass  # May get this error on Safari even if upload works.
            else:
                element.send_keys(abs_path)
        except (StaleElementReferenceException, ENI_Exception):
            self.wait_for_ready_state_complete()
            time.sleep(0.16)
            element = self.wait_for_element_present(
                selector, by=by, timeout=timeout
            )
            if self.browser == "safari":
                try:
                    element.send_keys(abs_path)
                except NoSuchElementException:
                    pass  # May get this error on Safari even if upload works.
            else:
                element.send_keys(abs_path)
        if self.demo_mode:
            if self.driver.current_url != pre_action_url:
                self.__demo_mode_pause_if_active()
            else:
                self.__demo_mode_pause_if_active(tiny=True)
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def save_element_as_image_file(
        self, selector, file_name, folder=None, overlay_text=""
    ):
        """Take a screenshot of an element and save it as an image file.
        If no folder is specified, will save it to the current folder.
        If overlay_text is provided, will add that to the saved image."""
        element = self.wait_for_element_visible(selector)
        element_png = element.screenshot_as_png
        if len(file_name.split(".")[0]) < 1:
            raise Exception("Error: file_name length must be > 0.")
        if not file_name.endswith(".png"):
            file_name = file_name + ".png"
        image_file_path = None
        if folder:
            if folder.endswith(os.sep):
                folder = folder[:-1]
            if len(folder) > 0:
                self.create_folder(folder)
                image_file_path = os.path.join(folder, file_name)
        if not image_file_path:
            image_file_path = file_name
        with open(image_file_path, "wb") as file:
            file.write(element_png)
        # Add a text overlay if given
        if type(overlay_text) is str and len(overlay_text) > 0:
            try:
                from PIL import Image, ImageDraw
            except Exception:
                shared_utils.pip_install("Pillow")
                from PIL import Image, ImageDraw

            text_rows = overlay_text.split("\n")
            len_text_rows = len(text_rows)
            max_width = 0
            for text_row in text_rows:
                if len(text_row) > max_width:
                    max_width = len(text_row)
            image = Image.open(image_file_path)
            draw = ImageDraw.Draw(image)
            draw.rectangle(
                (0, 0, (max_width * 6) + 6, 16 * len_text_rows),
                fill=(236, 236, 28),
            )
            draw.text(
                (4, 2),  # Coordinates
                overlay_text,  # Text
                (8, 38, 176),  # Color
            )
            image.save(image_file_path, "PNG", quality=100, optimize=True)

    def download_file(self, file_url, destination_folder=None):
        """Downloads the file from the url to the destination folder.
        If no destination folder is specified, the default one is used.
        (The default [Downloads Folder] = "./downloaded_files")"""
        if not destination_folder:
            destination_folder = constants.Files.DOWNLOADS_FOLDER
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        page_utils._download_file_to(file_url, destination_folder)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        url_dest = [file_url, destination_folder]
                        action = ["do_fi", url_dest, origin, time_stamp]
                        self.__extra_actions.append(action)

    def save_file_as(self, file_url, new_file_name, destination_folder=None):
        """Similar to self.download_file(), except that you get to rename the
        file being downloaded to whatever you want."""
        if not destination_folder:
            destination_folder = constants.Files.DOWNLOADS_FOLDER
        page_utils._download_file_to(
            file_url, destination_folder, new_file_name
        )

    def save_data_as(self, data, file_name, destination_folder=None):
        """Saves the data specified to a file of the name specified.
        If no destination folder is specified, the default one is used.
        (The default [Downloads Folder] = "./downloaded_files")"""
        if not destination_folder:
            destination_folder = constants.Files.DOWNLOADS_FOLDER
        page_utils._save_data_as(data, destination_folder, file_name)

    def get_downloads_folder(self):
        """Returns the path of the SeleniumBase "downloaded_files/" folder.
        Calling self.download_file(file_url) will put that file in here.
        With the exception of Safari, IE, and Chromium Guest Mode,
          any clicks that download files will also use this folder
          rather than using the browser's default "downloads/" path."""
        self.__check_scope()
        return download_helper.get_downloads_folder()

    def get_browser_downloads_folder(self):
        """Returns the path that is used when a click initiates a download.
        SeleniumBase overrides the system path to be "downloaded_files/"
        The path can't be changed on Safari, IE, or Chromium Guest Mode.
        The same problem occurs when using an out-of-date chromedriver.
        """
        self.__check_scope()
        if self.is_chromium() and self.guest_mode and not self.headless:
            # Guest Mode (non-headless) can force the default downloads path
            return os.path.join(os.path.expanduser("~"), "downloads")
        elif self.browser == "safari" or self.browser == "ie":
            # Can't change the system [Downloads Folder] on Safari or IE
            return os.path.join(os.path.expanduser("~"), "downloads")
        elif (
            self.driver.capabilities["browserName"].lower() == "chrome"
            and int(self.get_chromedriver_version().split(".")[0]) < 73
            and self.headless
        ):
            return os.path.join(os.path.expanduser("~"), "downloads")
        else:
            return download_helper.get_downloads_folder()
        return os.path.join(os.path.expanduser("~"), "downloads")

    def get_path_of_downloaded_file(self, file, browser=False):
        """Returns the OS path of the downloaded file."""
        if browser:
            return os.path.join(self.get_browser_downloads_folder(), file)
        else:
            return os.path.join(self.get_downloads_folder(), file)

    def is_downloaded_file_present(self, file, browser=False):
        """Returns True if the file exists in the pre-set [Downloads Folder].
        For browser click-initiated downloads, SeleniumBase will override
            the system [Downloads Folder] to be "./downloaded_files/",
            but that path can't be overridden when using Safari, IE,
            or Chromium Guest Mode, which keeps the default system path.
        self.download_file(file_url) will always use "./downloaded_files/".
        @Params
        file - The filename of the downloaded file.
        browser - If True, uses the path set by click-initiated downloads.
                  If False, uses the self.download_file(file_url) path.
                  Those paths are often the same. (browser-dependent)
                  (Default: False).
        """
        return os.path.exists(
            self.get_path_of_downloaded_file(file, browser=browser)
        )

    def delete_downloaded_file_if_present(self, file, browser=False):
        """Deletes the file from the [Downloads Folder] if the file exists.
        For browser click-initiated downloads, SeleniumBase will override
            the system [Downloads Folder] to be "./downloaded_files/",
            but that path can't be overridden when using Safari, IE,
            or Chromium Guest Mode, which keeps the default system path.
        self.download_file(file_url) will always use "./downloaded_files/".
        @Params
        file - The filename to be deleted from the [Downloads Folder].
        browser - If True, uses the path set by click-initiated downloads.
                  If False, uses the self.download_file(file_url) path.
                  Those paths are usually the same. (browser-dependent)
                  (Default: False).
        """
        if self.is_downloaded_file_present(file, browser=browser):
            file_path = self.get_path_of_downloaded_file(file, browser=browser)
            try:
                os.remove(file_path)
            except Exception:
                pass

    def delete_downloaded_file(self, file, browser=False):
        """Same as self.delete_downloaded_file_if_present()
        Deletes the file from the [Downloads Folder] if the file exists.
        For browser click-initiated downloads, SeleniumBase will override
            the system [Downloads Folder] to be "./downloaded_files/",
            but that path can't be overridden when using Safari, IE,
            or Chromium Guest Mode, which keeps the default system path.
        self.download_file(file_url) will always use "./downloaded_files/".
        @Params
        file - The filename to be deleted from the [Downloads Folder].
        browser - If True, uses the path set by click-initiated downloads.
                  If False, uses the self.download_file(file_url) path.
                  Those paths are usually the same. (browser-dependent)
                  (Default: False).
        """
        if self.is_downloaded_file_present(file, browser=browser):
            file_path = self.get_path_of_downloaded_file(file, browser=browser)
            try:
                os.remove(file_path)
            except Exception:
                pass

    def assert_downloaded_file(self, file, timeout=None, browser=False):
        """Asserts that the file exists in SeleniumBase's [Downloads Folder].
        For browser click-initiated downloads, SeleniumBase will override
            the system [Downloads Folder] to be "./downloaded_files/",
            but that path can't be overridden when using Safari, IE,
            or Chromium Guest Mode, which keeps the default system path.
        self.download_file(file_url) will always use "./downloaded_files/".
        @Params
        file - The filename of the downloaded file.
        timeout - The time (seconds) to wait for the download to complete.
        browser - If True, uses the path set by click-initiated downloads.
                  If False, uses the self.download_file(file_url) path.
                  Those paths are often the same. (browser-dependent)
                  (Default: False).
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        downloaded_file_path = self.get_path_of_downloaded_file(file, browser)
        found = False
        for x in range(int(timeout)):
            shared_utils.check_if_time_limit_exceeded()
            try:
                self.assertTrue(
                    os.path.exists(downloaded_file_path),
                    "File [%s] was not found in the downloads folder [%s]!"
                    % (file, self.get_downloads_folder()),
                )
                found = True
                break
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(1)
        if not found and not os.path.exists(downloaded_file_path):
            message = (
                "File {%s} was not found in the downloads folder {%s} "
                "after %s seconds! (Or the download didn't complete!)"
                % (file, self.get_downloads_folder(), timeout)
            )
            page_actions.timeout_exception("NoSuchFileException", message)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["as_df", file, origin, time_stamp]
                        self.__extra_actions.append(action)
        if self.demo_mode:
            messenger_post = "ASSERT DOWNLOADED FILE: [%s]" % file
            try:
                js_utils.activate_jquery(self.driver)
                js_utils.post_messenger_success_message(
                    self.driver, messenger_post, self.message_duration
                )
            except Exception:
                pass

    def assert_true(self, expr, msg=None):
        """Asserts that the expression is True.
        Will raise an exception if the statement if False."""
        self.assertTrue(expr, msg=msg)

    def assert_false(self, expr, msg=None):
        """Asserts that the expression is False.
        Will raise an exception if the statement if True."""
        self.assertFalse(expr, msg=msg)

    def assert_equal(self, first, second, msg=None):
        """Asserts that the two values are equal.
        Will raise an exception if the values are not equal."""
        self.assertEqual(first, second, msg=msg)

    def assert_not_equal(self, first, second, msg=None):
        """Asserts that the two values are not equal.
        Will raise an exception if the values are equal."""
        self.assertNotEqual(first, second, msg=msg)

    def assert_in(self, first, second, msg=None):
        """Asserts that the first string is in the second string.
        Will raise an exception if the first string is not in the second."""
        self.assertIn(first, second, msg=msg)

    def assert_not_in(self, first, second, msg=None):
        """Asserts that the first string is not in the second string.
        Will raise an exception if the first string is in the second string."""
        self.assertNotIn(first, second, msg=msg)

    def assert_raises(self, *args, **kwargs):
        """Asserts that the following block of code raises an exception.
        Will raise an exception if the block of code has no exception.
        Usage Example =>
                # Verify that the expected exception is raised.
                with self.assert_raises(Exception):
                    raise Exception("Expected Exception!")
        """
        return self.assertRaises(*args, **kwargs)

    def wait_for_attribute(
        self, selector, attribute, value=None, by="css selector", timeout=None
    ):
        """Raises an exception if the element attribute/value is not found.
        If the value is not specified, the attribute only needs to exist.
        Returns the element that contains the attribute if successful.
        Default timeout = LARGE_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_attribute_present(
                selector, attribute, value=value, timeout=timeout
            )
        return page_actions.wait_for_attribute(
            self.driver,
            selector,
            attribute,
            value=value,
            by=by,
            timeout=timeout,
        )

    def assert_attribute(
        self, selector, attribute, value=None, by="css selector", timeout=None
    ):
        """Raises an exception if the element attribute/value is not found.
        If the value is not specified, the attribute only needs to exist.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_attribute(
            selector, attribute, value=value, by=by, timeout=timeout
        )
        if (
            self.demo_mode
            and not self.__is_shadow_selector(selector)
            and self.is_element_visible(selector, by=by)
        ):
            a_a = "ASSERT ATTRIBUTE"
            i_n = "in"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_a = SD.translate_assert_attribute(self._language)
                i_n = SD.translate_in(self._language)
            if not value:
                messenger_post = "%s: [%s] %s %s: %s" % (
                    a_a,
                    attribute,
                    i_n,
                    by.upper(),
                    selector,
                )
            else:
                messenger_post = '%s: [%s="%s"] %s %s: %s' % (
                    a_a,
                    attribute,
                    value,
                    i_n,
                    by.upper(),
                    selector,
                )
            self.__highlight_with_assert_success(messenger_post, selector, by)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        value = value.replace("\\", "\\\\")
                        sel_att_val = [selector, attribute, value]
                        action = ["as_at", sel_att_val, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    def assert_title(self, title):
        """Asserts that the web page title matches the expected title.
        When a web page initially loads, the title starts as the URL,
            but then the title switches over to the actual page title.
        In Recorder Mode, this assertion is skipped because the Recorder
            changes the page title to the selector of the hovered element.
        """
        self.wait_for_ready_state_complete()
        expected = title.strip()
        actual = self.get_page_title().strip()
        error = (
            "Expected page title [%s] does not match the actual title [%s]!"
        )
        try:
            if not self.recorder_mode:
                self.assertEqual(expected, actual, error % (expected, actual))
        except Exception:
            self.wait_for_ready_state_complete()
            time.sleep(2)
            actual = self.get_page_title().strip()
            try:
                self.assertEqual(expected, actual, error % (expected, actual))
            except Exception:
                self.wait_for_ready_state_complete()
                time.sleep(2)
                actual = self.get_page_title().strip()
                self.assertEqual(expected, actual, error % (expected, actual))
        if self.demo_mode and not self.recorder_mode:
            a_t = "ASSERT TITLE"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert_title(self._language)
            messenger_post = "%s: {%s}" % (a_t, expected)
            self.__highlight_with_assert_success(messenger_post, "html")
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["as_ti", expected, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    def assert_title_contains(self, substring):
        """Asserts that the title substring appears in the web page title.
        When a web page initially loads, the title starts as the URL,
            but then the title switches over to the actual page title.
        In Recorder Mode, this assertion is skipped because the Recorder
            changes the page title to the selector of the hovered element.
        """
        self.wait_for_ready_state_complete()
        expected = substring.strip()
        actual = self.get_page_title().strip()
        error = (
            "Expected title substring [%s] does not appear "
            "in the actual page title [%s]!"
        )
        try:
            if not self.recorder_mode:
                self.assertIn(expected, actual, error % (expected, actual))
        except Exception:
            self.wait_for_ready_state_complete()
            time.sleep(2)
            actual = self.get_page_title().strip()
            try:
                self.assertIn(expected, actual, error % (expected, actual))
            except Exception:
                self.wait_for_ready_state_complete()
                time.sleep(2)
                actual = self.get_page_title().strip()
                self.assertIn(expected, actual, error % (expected, actual))
        if self.demo_mode and not self.recorder_mode:
            a_t = "ASSERT TITLE CONTAINS"
            messenger_post = "%s: {%s}" % (a_t, expected)
            self.__highlight_with_assert_success(messenger_post, "html")
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["as_tc", expected, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    def assert_no_js_errors(self, exclude=[]):
        """Asserts current URL has no "SEVERE"-level JavaScript errors.
        Works ONLY on Chromium browsers (Chrome or Edge).
        Does NOT work on Firefox, IE, Safari, or some other browsers:
            * See https://github.com/SeleniumHQ/selenium/issues/1161
        Based on the following Stack Overflow solution:
            * https://stackoverflow.com/a/41150512/7058266
        @Params
        exclude -->
            A list of substrings or a single comma-separated string of
            substrings for filtering out error URLs that contain them.
            URLs that contain any excluded substring will get excluded
            from the final errors list that's used with the assertion.
        Examples:
            self.assert_no_js_errors()
            self.assert_no_js_errors(exclude=["/api.", "/analytics."])
            self.assert_no_js_errors(exclude="//api.go,/analytics.go")
            self.assert_no_js_errors(exclude=["Uncaught SyntaxError"])
            self.assert_no_js_errors(exclude=["TypeError", "SyntaxE"])
        """
        self.__check_scope()
        if (
            exclude
            and not type(exclude) is list
            and not type(exclude) is tuple
        ):
            exclude = str(exclude).replace(" ", "").split(",")
        time.sleep(0.1)  # May take a moment for errors to appear after loads.
        try:
            browser_logs = self.driver.get_log("browser")
        except (ValueError, WebDriverException):
            # If unable to get browser logs, skip the assert and return.
            return
        messenger_library = "//cdnjs.cloudflare.com/ajax/libs/messenger"
        underscore_library = "//cdnjs.cloudflare.com/ajax/libs/underscore"
        errors = []
        for entry in browser_logs:
            if entry["level"] == "SEVERE":
                if (
                    messenger_library not in entry["message"]
                    and underscore_library not in entry["message"]
                ):
                    # Add errors if not caused by SeleniumBase dependencies
                    if not exclude:
                        errors.append(entry)
                    else:
                        found = False
                        message = entry["message"]
                        if message.count(" - Failed to load resource") == 1:
                            message = message.split(
                                " - Failed to load resource"
                            )[0]
                        for substring in exclude:
                            substring = str(substring)
                            if (
                                len(substring) > 0
                                and substring in message
                            ):
                                found = True
                                break
                        if not found:
                            errors.append(entry)
        if len(errors) > 0:
            for n in range(len(errors)):
                f_t_l_r = " - Failed to load resource"
                u_c_s_e = " Uncaught SyntaxError: "
                u_c_t_e = " Uncaught TypeError: "
                if f_t_l_r in errors[n]["message"]:
                    url = errors[n]["message"].split(f_t_l_r)[0]
                    errors[n] = {"Error 404 (broken link)": url}
                elif u_c_s_e in errors[n]["message"]:
                    url = errors[n]["message"].split(u_c_s_e)[0]
                    error = errors[n]["message"].split(u_c_s_e)[1]
                    errors[n] = {"Uncaught SyntaxError (%s)" % error: url}
                elif u_c_t_e in errors[n]["message"]:
                    url = errors[n]["message"].split(u_c_t_e)[0]
                    error = errors[n]["message"].split(u_c_t_e)[1]
                    errors[n] = {"Uncaught TypeError (%s)" % error: url}
            er_str = str(errors)
            er_str = er_str.replace("[{", "[\n{").replace("}, {", "},\n{")
            current_url = self.get_current_url()
            raise Exception(
                "JavaScript errors found on %s => %s" % (current_url, er_str)
            )
        if self.demo_mode:
            if self.browser == "chrome" or self.browser == "edge":
                a_t = "ASSERT NO JS ERRORS"
                if self._language != "English":
                    from seleniumbase.fixtures.words import SD

                    a_t = SD.translate_assert_no_js_errors(self._language)
                messenger_post = "%s" % a_t
                self.__highlight_with_assert_success(messenger_post, "html")

    def __activate_html_inspector(self):
        self.wait_for_ready_state_complete()
        time.sleep(0.05)
        js_utils.activate_html_inspector(self.driver)

    def inspect_html(self):
        """Inspects the Page HTML with HTML-Inspector.
        (https://github.com/philipwalton/html-inspector)
        (https://cdnjs.com/libraries/html-inspector)
        Prints the results and also returns them."""
        self.__activate_html_inspector()
        self.wait_for_ready_state_complete()
        script = """HTMLInspector.inspect();"""
        try:
            self.execute_script(script)
        except Exception:
            # If unable to load the JavaScript, skip inspection and return.
            msg = "(Unable to load HTML-Inspector JS! Inspection Skipped!)"
            print("\n" + msg)
            return msg
        time.sleep(0.1)
        browser_logs = []
        try:
            browser_logs = self.driver.get_log("browser")
        except (ValueError, WebDriverException):
            # If unable to get browser logs, skip the assert and return.
            msg = "(Unable to Inspect HTML! -> Only works on Chromium!)"
            print("\n" + msg)
            return msg
        messenger_library = "//cdnjs.cloudflare.com/ajax/libs/messenger"
        url = self.get_current_url()
        header = "\n* HTML Inspection Results: %s" % url
        results = [header]
        row_count = 0
        for entry in browser_logs:
            message = entry["message"]
            if "0:6053 " in message:
                message = message.split("0:6053")[1]
            message = message.replace("\\u003C", "<")
            if message.startswith(' "') and message.count('"') == 2:
                message = message.split('"')[1]
            message = "⚠️  " + message
            if messenger_library not in message:
                if message not in results:
                    results.append(message)
                    row_count += 1
        if row_count > 0:
            results.append("* (See the Console output for details!)")
        else:
            results.append("* (No issues detected!)")
        results = "\n".join(results)
        print(results)
        return results

    def is_valid_url(self, url):
        """Return True if the url is a valid url."""
        return page_utils.is_valid_url(url)

    def is_chromium(self):
        """Return True if the browser is Chrome, Edge, or Opera."""
        self.__check_scope()
        chromium = False
        browser_name = self.driver.capabilities["browserName"]
        if browser_name.lower() in ("chrome", "edge", "msedge", "opera"):
            chromium = True
        return chromium

    def __fail_if_not_using_chrome(self, method):
        chrome = False
        browser_name = self.driver.capabilities["browserName"]
        if browser_name.lower() == "chrome":
            chrome = True
        if not chrome:
            from seleniumbase.common.exceptions import NotUsingChromeException

            message = (
                'Error: "%s" should only be called '
                'by tests running with self.browser == "chrome"! '
                'You should add an "if" statement to your code before calling '
                "this method if using browsers that are Not Chrome! "
                'The browser detected was: "%s".' % (method, browser_name)
            )
            raise NotUsingChromeException(message)

    def get_chrome_version(self):
        self.__check_scope()
        self.__fail_if_not_using_chrome("get_chrome_version()")
        driver_capabilities = self.driver.capabilities
        if "version" in driver_capabilities:
            chrome_version = driver_capabilities["version"]
        else:
            chrome_version = driver_capabilities["browserVersion"]
        return chrome_version

    def get_chromedriver_version(self):
        self.__check_scope()
        self.__fail_if_not_using_chrome("get_chromedriver_version()")
        chrome_dict = self.driver.capabilities["chrome"]
        chromedriver_version = chrome_dict["chromedriverVersion"]
        chromedriver_version = chromedriver_version.split(" ")[0]
        return chromedriver_version

    def is_chromedriver_too_old(self):
        """Before chromedriver 73, there was no version check, which
        means it's possible to run a new Chrome with old drivers."""
        self.__check_scope()
        self.__fail_if_not_using_chrome("is_chromedriver_too_old()")
        if int(self.get_chromedriver_version().split(".")[0]) < 73:
            return True  # chromedriver is too old! Please upgrade!
        return False

    def get_mfa_code(self, totp_key=None):
        """Same as get_totp_code() and get_google_auth_password().
        Returns a time-based one-time password based on the
        Google Authenticator algorithm for multi-factor authentication.
        If the "totp_key" is not specified, this method defaults
        to using the one provided in [seleniumbase/config/settings.py].
        Google Authenticator codes expire & change at 30-sec intervals.
        If the fetched password expires in the next 1.5 seconds, waits
        for a new one before returning it (may take up to 1.5 seconds).
        See https://pyotp.readthedocs.io/en/latest/ for details."""
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

    def enter_mfa_code(
        self, selector, totp_key=None, by="css selector", timeout=None
    ):
        """Enters into the field a Multi-Factor Authentication TOTP Code.
        If the "totp_key" is not specified, this method defaults
        to using the one provided in [seleniumbase/config/settings.py].
        The TOTP code is generated by the Google Authenticator Algorithm.
        This method will automatically press ENTER after typing the code."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        self.wait_for_element_visible(selector, by=by, timeout=timeout)
        if self.recorder_mode:
            css_selector = self.convert_to_css_selector(selector, by=by)
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    origin = self.get_origin()
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        sel_key = [css_selector, totp_key]
                        action = ["e_mfa", sel_key, origin, time_stamp]
                        self.__extra_actions.append(action)
                    # Sometimes Sign-In leaves the origin... Save work first.
                    self.save_recorded_actions()
        mfa_code = self.get_mfa_code(totp_key)
        self.update_text(selector, mfa_code + "\n", by=by, timeout=timeout)

    def convert_css_to_xpath(self, css):
        return css_to_xpath.convert_css_to_xpath(css)

    def convert_xpath_to_css(self, xpath):
        return xpath_to_css.convert_xpath_to_css(xpath)

    def convert_to_css_selector(self, selector, by):
        """This method converts a selector to a CSS_SELECTOR.
        jQuery commands require a CSS_SELECTOR for finding elements.
        This method should only be used for jQuery/JavaScript actions.
        Pure JavaScript doesn't support using a:contains("LINK_TEXT")."""
        if by == By.CSS_SELECTOR:
            return selector
        elif by == By.ID:
            return "#%s" % selector
        elif by == By.CLASS_NAME:
            return ".%s" % selector
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
                "Exception: Could not convert {%s}(by=%s) to CSS_SELECTOR!"
                % (selector, by)
            )

    def set_value(
        self, selector, text, by="css selector", timeout=None, scroll=True
    ):
        """This method uses JavaScript to update a text field."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by, xp_ok=False)
        self.wait_for_ready_state_complete()
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        orginal_selector = selector
        css_selector = self.convert_to_css_selector(selector, by=by)
        self.__demo_mode_highlight_if_active(orginal_selector, by)
        if scroll and not self.demo_mode and not self.slow_mode:
            self.scroll_to(orginal_selector, by=by, timeout=timeout)
        text = self.__get_type_checked_text(text)
        value = re.escape(text)
        value = self.__escape_quotes_if_needed(value)
        pre_escape_css_selector = css_selector
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        the_type = None
        if ":contains\\(" not in css_selector:
            get_type_script = (
                """return document.querySelector('%s').getAttribute('type');"""
                % css_selector
            )
            the_type = self.execute_script(get_type_script)  # Used later
            script = """document.querySelector('%s').value='%s';""" % (
                css_selector,
                value,
            )
            self.execute_script(script)
            if self.recorder_mode:
                time_stamp = self.execute_script("return Date.now();")
                origin = self.get_origin()
                sel_tex = [pre_escape_css_selector, text]
                action = ["js_ty", sel_tex, origin, time_stamp]
                self.__extra_actions.append(action)
        else:
            script = """jQuery('%s')[0].value='%s';""" % (css_selector, value)
            self.safe_execute_script(script)
        if text.endswith("\n"):
            element = self.wait_for_element_present(
                orginal_selector, by=by, timeout=timeout
            )
            element.send_keys(Keys.RETURN)
            if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                self.wait_for_ready_state_complete()
        else:
            if the_type == "range" and ":contains\\(" not in css_selector:
                # Some input sliders need a mouse event to trigger listeners.
                try:
                    mouse_move_script = (
                        """m_elm = document.querySelector('%s');"""
                        """m_evt = new Event('mousemove');"""
                        """m_elm.dispatchEvent(m_evt);""" % css_selector
                    )
                    self.execute_script(mouse_move_script)
                except Exception:
                    pass
        self.__demo_mode_pause_if_active()

    def js_update_text(self, selector, text, by="css selector", timeout=None):
        """JavaScript + send_keys are used to update a text field.
        Performs self.set_value() and triggers event listeners.
        If text ends in "\n", set_value() presses RETURN after.
        Works faster than send_keys() alone due to the JS call.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        text = self.__get_type_checked_text(text)
        self.set_value(selector, text, by=by, timeout=timeout)
        if not text.endswith("\n"):
            try:
                element = page_actions.wait_for_element_present(
                    self.driver, selector, by, timeout=0.2
                )
                element.send_keys(" " + Keys.BACK_SPACE)
            except Exception:
                pass

    def js_type(self, selector, text, by="css selector", timeout=None):
        """Same as self.js_update_text()
        JavaScript + send_keys are used to update a text field.
        Performs self.set_value() and triggers event listeners.
        If text ends in "\n", set_value() presses RETURN after.
        Works faster than send_keys() alone due to the JS call.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.js_update_text(selector, text, by=by, timeout=timeout)

    def set_text(self, selector, text, by="css selector", timeout=None):
        """Same as self.js_update_text()
        JavaScript + send_keys are used to update a text field.
        Performs self.set_value() and triggers event listeners.
        If text ends in "\n", set_value() presses RETURN after.
        Works faster than send_keys() alone due to the JS call.
        If not an input or textarea, sets textContent instead."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        if element.tag_name.lower() in ["input", "textarea"]:
            self.js_update_text(selector, text, by=by, timeout=timeout)
        else:
            self.set_text_content(selector, text, by=by, timeout=timeout)

    def set_text_content(
        self, selector, text, by="css selector", timeout=None, scroll=False
    ):
        """This method uses JavaScript to set an element's textContent.
        If the element is an input or textarea, sets the value instead."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        element = page_actions.wait_for_element_present(
            self.driver, selector, by, timeout
        )
        if element.tag_name.lower() in ["input", "textarea"]:
            self.js_update_text(selector, text, by=by, timeout=timeout)
            return
        orginal_selector = selector
        css_selector = self.convert_to_css_selector(selector, by=by)
        if scroll:
            self.__demo_mode_highlight_if_active(orginal_selector, by)
            if not self.demo_mode and not self.slow_mode:
                self.scroll_to(orginal_selector, by=by, timeout=timeout)
        text = self.__get_type_checked_text(text)
        value = re.escape(text)
        value = self.__escape_quotes_if_needed(value)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        if ":contains\\(" not in css_selector:
            script = """document.querySelector('%s').textContent='%s';""" % (
                css_selector,
                value,
            )
            self.execute_script(script)
        else:
            script = """jQuery('%s')[0].textContent='%s';""" % (
                css_selector,
                value,
            )
            self.safe_execute_script(script)
        self.__demo_mode_pause_if_active()

    def jquery_update_text(
        self, selector, text, by="css selector", timeout=None
    ):
        """This method uses jQuery to update a text field.
        If the text string ends with the newline character,
        Selenium finishes the call, which simulates pressing
        {Enter/Return} after the text is entered."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by, xp_ok=False)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=timeout
        )
        self.__demo_mode_highlight_if_active(selector, by)
        self.scroll_to(selector, by=by)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        selector = self.__escape_quotes_if_needed(selector)
        text = re.escape(text)
        text = self.__escape_quotes_if_needed(text)
        update_text_script = """jQuery('%s').val('%s');""" % (selector, text)
        self.safe_execute_script(update_text_script)
        if text.endswith("\n"):
            element.send_keys("\n")
        self.__demo_mode_pause_if_active()

    def get_value(self, selector, by="css selector", timeout=None):
        """This method uses JavaScript to get the value of an input field.
        (Works on both input fields and textarea fields.)"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_ready_state_complete()
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        orginal_selector = selector
        css_selector = self.convert_to_css_selector(selector, by=by)
        self.__demo_mode_highlight_if_active(orginal_selector, by)
        if not self.demo_mode and not self.slow_mode:
            self.scroll_to(orginal_selector, by=by, timeout=timeout)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        if ":contains\\(" not in css_selector:
            script = """return document.querySelector('%s').value;""" % (
                css_selector
            )
            value = self.execute_script(script)
        else:
            script = """return jQuery('%s')[0].value;""" % css_selector
            value = self.safe_execute_script(script)
        return value

    def set_time_limit(self, time_limit):
        self.__check_scope()
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

    def set_default_timeout(self, timeout):
        """This method changes the default timeout values of test methods
        for the duration of the current test.
        Effected timeouts: (used by methods that wait for elements)
            * settings.SMALL_TIMEOUT - (default value: 6 seconds)
            * settings.LARGE_TIMEOUT - (default value: 10 seconds)
        The minimum allowable default timeout is: 0.5 seconds.
        The maximum allowable default timeout is: 60.0 seconds.
        (Test methods can still override timeouts outside that range.)
        """
        self.__check_scope()
        if not type(timeout) is int and not type(timeout) is float:
            raise Exception('Expecting a numeric value for "timeout"!')
        if timeout < 0:
            raise Exception('The "timeout" cannot be a negative number!')
        timeout = float(timeout)
        # Min default timeout: 0.5 seconds. Max default timeout: 60.0 seconds.
        min_timeout = 0.5
        max_timeout = 60.0
        if timeout < min_timeout:
            logging.info("Minimum default timeout = %s" % min_timeout)
            timeout = min_timeout
        elif timeout > max_timeout:
            logging.info("Maximum default timeout = %s" % max_timeout)
            timeout = max_timeout
        self.__overrided_default_timeouts = True
        sb_config._is_timeout_changed = True
        settings.SMALL_TIMEOUT = timeout
        settings.LARGE_TIMEOUT = timeout

    def reset_default_timeout(self):
        """Reset default timeout values to the original from settings.py
        This method reverts the changes made by set_default_timeout()"""
        if self.__overrided_default_timeouts:
            if sb_config._SMALL_TIMEOUT and sb_config._LARGE_TIMEOUT:
                settings.SMALL_TIMEOUT = sb_config._SMALL_TIMEOUT
                settings.LARGE_TIMEOUT = sb_config._LARGE_TIMEOUT
                sb_config._is_timeout_changed = False
                self.__overrided_default_timeouts = False

    def skip(self, reason=""):
        """Mark the test as Skipped."""
        self.__check_scope()
        if self.dashboard:
            test_id = self.__get_test_id_2()
            if hasattr(self, "_using_sb_fixture"):
                test_id = sb_config._test_id
            if (
                test_id in sb_config._results.keys()
                and sb_config._results[test_id] == "Passed"
            ):
                # Duplicate tearDown() called where test already passed
                self.__passed_then_skipped = True
            self.__will_be_skipped = True
            sb_config._results[test_id] = "Skipped"
        if hasattr(self, "with_db_reporting") and self.with_db_reporting:
            if self.is_pytest:
                self.__skip_reason = reason
            else:
                self._nose_skip_reason = reason
        # Add skip reason to the logs
        if not hasattr(self, "_using_sb_fixture"):
            test_id = self.__get_test_id()  # Recalculate the test id
        test_logpath = os.path.join(self.log_path, test_id)
        self.__create_log_path_as_needed(test_logpath)
        browser = self.browser
        if not reason:
            reason = "No skip reason given"
        log_helper.log_skipped_test_data(
            self, test_logpath, self.driver, browser, reason
        )
        self._was_skipped = True
        # Finally skip the test for real
        self.skipTest(reason)

    ############

    # Console Log controls

    def start_recording_console_logs(self):
        """
        Starts recording console logs. Logs are saved to: "console.logs".
        To get those logs later, call "self.get_recorded_console_logs()".
        If navigating to a new page, then the current recorded logs will be
        lost, and you'll have to call start_recording_console_logs() again.
        # Link1: https://stackoverflow.com/a/19846113/7058266
        # Link2: https://stackoverflow.com/a/74196986/7058266
        """
        self.driver.execute_script(
            """
            console.stdlog = console.log.bind(console);
            console.logs = [];
            console.log = function(){
                console.logs.push(Array.from(arguments));
                console.stdlog.apply(console, arguments);
            }
            """
        )

    def console_log_string(self, string):
        """
        Log a string to the Web Browser's Console.
        Example:
        self.console_log_string("Hello World!")
        """
        self.driver.execute_script("""console.log(`%s`);""" % string)

    def console_log_script(self, script):
        """
        Log output of JavaScript to the Web Browser's Console.
        Example:
        self.console_log_script('document.querySelector("h2").textContent')
        """
        self.driver.execute_script("""console.log(%s);""" % script)

    def get_recorded_console_logs(self):
        """
        Returns console logs recorded after "start_recording_console_logs()".
        """
        logs = []
        try:
            logs = self.driver.execute_script("return console.logs;")
        except Exception:
            pass
        return logs

    ############

    # Application "Local Storage" controls

    def __is_valid_storage_url(self):
        url = self.get_current_url()
        if url and len(url) > 0:
            if ("http:") in url or ("https:") in url or ("file:") in url:
                return True
        return False

    def set_local_storage_item(self, key, value):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Local Storage is not available here!")
        self.execute_script(
            "window.localStorage.setItem('{}', '{}');".format(key, value)
        )

    def get_local_storage_item(self, key):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Local Storage is not available here!")
        return self.execute_script(
            "return window.localStorage.getItem('{}');".format(key)
        )

    def remove_local_storage_item(self, key):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Local Storage is not available here!")
        self.execute_script(
            "window.localStorage.removeItem('{}');".format(key)
        )

    def clear_local_storage(self):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            return
        self.execute_script("window.localStorage.clear();")
        if self.recorder_mode:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["c_l_s", "", origin, time_stamp]
            self.__extra_actions.append(action)

    def get_local_storage_keys(self):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Local Storage is not available here!")
        return self.execute_script(
            "var ls = window.localStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys;"
        )

    def get_local_storage_items(self):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Local Storage is not available here!")
        return self.execute_script(
            r"var ls = window.localStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items;"
        )

    # Application "Session Storage" controls

    def set_session_storage_item(self, key, value):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Session Storage is not available here!")
        self.execute_script(
            "window.sessionStorage.setItem('{}', '{}');".format(key, value)
        )

    def get_session_storage_item(self, key):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Session Storage is not available here!")
        return self.execute_script(
            "return window.sessionStorage.getItem('{}');".format(key)
        )

    def remove_session_storage_item(self, key):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Session Storage is not available here!")
        self.execute_script(
            "window.sessionStorage.removeItem('{}');".format(key)
        )

    def clear_session_storage(self):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            return
        if not self.recorder_mode:
            self.execute_script("window.sessionStorage.clear();")
        else:
            recorder_keys = [
                "recorder_mode",
                "recorded_actions",
                "recorder_title",
                "pause_recorder",
                "recorder_activated",
            ]
            keys = self.get_session_storage_keys()
            for key in keys:
                if key not in recorder_keys:
                    self.remove_session_storage_item(key)
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["c_s_s", "", origin, time_stamp]
            self.__extra_actions.append(action)

    def get_session_storage_keys(self):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Session Storage is not available here!")
        return self.execute_script(
            "var ls = window.sessionStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys;"
        )

    def get_session_storage_items(self):
        self.__check_scope()
        if not self.__is_valid_storage_url():
            raise WebDriverException("Session Storage is not available here!")
        return self.execute_script(
            r"var ls = window.sessionStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items;"
        )

    ############

    # Methods ONLY for the selenium-wire integration ("--wire")

    def set_wire_proxy(self, string):
        """Set a proxy server for selenium-wire mode ("--wire")
        NOTE: This method ONLY works while using "--wire" mode!
        Examples:
            self.set_wire_proxy("SERVER:PORT")
            self.set_wire_proxy("socks5://SERVER:PORT")
            self.set_wire_proxy("USERNAME:PASSWORD@SERVER:PORT")
        """
        if not string:
            self.driver.proxy = {}
            return
        the_http = "http"
        the_https = "https"
        if string.startswith("socks4://"):
            the_http = "socks4"
            the_https = "socks4"
        elif string.startswith("socks5://"):
            the_http = "socks5"
            the_https = "socks5"
        string = string.split("//")[-1]
        self.driver.proxy = {
            "http": "%s://%s" % (the_http, string),
            "https": "%s://%s" % (the_https, string),
            "no_proxy": "localhost,127.0.0.1",
        }

    ############

    # Duplicates (Avoids name confusion when migrating from other frameworks.)

    def open_url(self, url):
        """Same as self.open()"""
        self.open(url)

    def visit(self, url):
        """Same as self.open()"""
        self.open(url)

    def visit_url(self, url):
        """Same as self.open()"""
        self.open(url)

    def goto(self, url):
        """Same as self.open()"""
        self.open(url)

    def go_to(self, url):
        """Same as self.open()"""
        self.open(url)

    def reload(self):
        """Same as self.refresh_page()"""
        self.refresh_page()

    def reload_page(self):
        """Same as self.refresh_page()"""
        self.refresh_page()

    def open_new_tab(self, switch_to=True):
        """Same as self.open_new_window()"""
        self.open_new_window(switch_to=switch_to)

    def switch_to_tab(self, tab, timeout=None):
        """Same as self.switch_to_window()
        Switches control of the browser to the specified window.
        The window can be an integer: 0 -> 1st tab, 1 -> 2nd tab, etc...
            Or it can be a list item from self.driver.window_handles"""
        self.switch_to_window(window=tab, timeout=timeout)

    def switch_to_default_tab(self):
        """Same as self.switch_to_default_window()"""
        self.switch_to_default_window()

    def switch_to_newest_tab(self):
        """Same as self.switch_to_newest_window()"""
        self.switch_to_newest_window()

    def input(
        self, selector, text, by="css selector", timeout=None, retry=False
    ):
        """Same as self.update_text()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.update_text(selector, text, by=by, timeout=timeout, retry=retry)

    def fill(
        self, selector, text, by="css selector", timeout=None, retry=False
    ):
        """Same as self.update_text()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.update_text(selector, text, by=by, timeout=timeout, retry=retry)

    def write(
        self, selector, text, by="css selector", timeout=None, retry=False
    ):
        """Same as self.update_text()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        self.update_text(selector, text, by=by, timeout=timeout, retry=retry)

    def click_link(self, link_text, timeout=None):
        """Same as self.click_link_text()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.click_link_text(link_text, timeout=timeout)

    def click_partial_link(self, partial_link_text, timeout=None):
        """Same as self.click_partial_link_text()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.click_partial_link_text(partial_link_text, timeout=timeout)

    def wait_for_element_visible(
        self, selector, by="css selector", timeout=None
    ):
        """Same as self.wait_for_element()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_element_visible(selector, timeout)
        return page_actions.wait_for_element_visible(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )

    def wait_for_element_clickable(
        self, selector, by="css selector", timeout=None
    ):
        """Waits for the element to be clickable, but does NOT click it."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            # If a shadow selector, use visible instead of clickable
            return self.__wait_for_shadow_element_visible(selector, timeout)
        return page_actions.wait_for_element_clickable(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )

    def wait_for_element_not_present(
        self, selector, by="css selector", timeout=None
    ):
        """Same as self.wait_for_element_absent()
        Waits for an element to no longer appear in the HTML of a page.
        A hidden element still counts as appearing in the page HTML.
        If waiting for elements to be hidden instead of nonexistent,
        use wait_for_element_not_visible() instead.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_absent(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )

    def assert_element_not_present(
        self, selector, by="css selector", timeout=None
    ):
        """Same as self.assert_element_absent()
        Will raise an exception if the element stays present.
        A hidden element counts as a present element, which fails this assert.
        If you want to assert that elements are hidden instead of nonexistent,
        use assert_element_not_visible() instead.
        (Note that hidden elements are still present in the HTML of the page.)
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_absent(selector, by=by, timeout=timeout)
        return True

    def get_google_auth_password(self, totp_key=None):
        """Same as self.get_mfa_code()"""
        return self.get_mfa_code(totp_key=totp_key)

    def get_google_auth_code(self, totp_key=None):
        """Same as self.get_mfa_code()"""
        return self.get_mfa_code(totp_key=totp_key)

    def get_totp_code(self, totp_key=None):
        """Same as self.get_mfa_code()"""
        return self.get_mfa_code(totp_key=totp_key)

    def enter_totp_code(
        self, selector, totp_key=None, by="css selector", timeout=None
    ):
        """Same as self.enter_mfa_code()"""
        return self.enter_mfa_code(
            selector=selector, totp_key=totp_key, by=by, timeout=timeout
        )

    def clear_all_cookies(self):
        """Same as self.delete_all_cookies()"""
        self.delete_all_cookies()

    def assert_no_broken_links(self, multithreaded=True):
        """Same as self.assert_no_404_errors()"""
        self.assert_no_404_errors(multithreaded=multithreaded)

    def wait(self, seconds):
        """Same as self.sleep() - Some JS frameworks use this method name."""
        self.sleep(seconds)

    def block_ads(self):
        """Same as self.ad_block()"""
        self.ad_block()

    def _print(self, msg):
        """Same as Python's print(), but also prints during multithreaded runs.
        Normally, Python's print() command won't print for multithreaded tests.
        Here's an example of running tests using multithreading: "pytest -n=4".
        Here's how to print directly from sys without using a print() command:
        To force a print during multithreaded tests, use: "sys.stderr.write()".
        To print without the new-line character end, use: "sys.stdout.write()".
        """
        if hasattr(sb_config, "_multithreaded") and sb_config._multithreaded:
            if type(msg) is not str:
                try:
                    msg = str(msg)
                except Exception:
                    pass
            sys.stderr.write(msg + "\n")
        else:
            print(msg)

    ############

    def add_css_link(self, css_link):
        self.__check_scope()
        self.__check_browser()
        js_utils.add_css_link(self.driver, css_link)

    def add_js_link(self, js_link):
        self.__check_scope()
        self.__check_browser()
        js_utils.add_js_link(self.driver, js_link)

    def add_css_style(self, css_style):
        self.__check_scope()
        self.__check_browser()
        js_utils.add_css_style(self.driver, css_style)

    def add_js_code_from_link(self, js_link):
        self.__check_scope()
        self.__check_browser()
        js_utils.add_js_code_from_link(self.driver, js_link)

    def add_js_code(self, js_code):
        self.__check_scope()
        self.__check_browser()
        js_utils.add_js_code(self.driver, js_code)

    def add_meta_tag(self, http_equiv=None, content=None):
        self.__check_scope()
        self.__check_browser()
        js_utils.add_meta_tag(
            self.driver, http_equiv=http_equiv, content=content
        )

    ############

    def activate_messenger(self):
        self.__check_scope()
        self.__check_browser()
        js_utils.activate_messenger(self.driver)
        self.wait_for_ready_state_complete()

    def set_messenger_theme(
        self, theme="default", location="default", max_messages="default"
    ):
        """Sets a theme for posting messages.
        Themes: ["flat", "future", "block", "air", "ice"]
        Locations: ["top_left", "top_center", "top_right",
                    "bottom_left", "bottom_center", "bottom_right"]
        max_messages is the limit of concurrent messages to display.
        """
        self.__check_scope()
        self.__check_browser()
        if not theme:
            theme = "default"  # "flat"
        if not location:
            location = "default"  # "bottom_right"
        if not max_messages:
            max_messages = "default"  # "8"
        else:
            max_messages = str(max_messages)  # Value must be in string format
        js_utils.set_messenger_theme(
            self.driver,
            theme=theme,
            location=location,
            max_messages=max_messages,
        )

    def post_message(self, message, duration=None, pause=True, style="info"):
        """Post a message on the screen with Messenger.
        Arguments:
            message: The message to display.
            duration: The time until the message vanishes. (Default: 2.55s)
            pause: If True, the program waits until the message completes.
            style: "info", "success", or "error".

        You can also post messages by using =>
            self.execute_script('Messenger().post("My Message")')
        """
        self.__check_scope()
        self.__check_browser()
        if style not in ["info", "success", "error"]:
            style = "info"
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        if (
            (self.headless or self.headless2 or self.xvfb)
            and float(duration) > 0.75
        ):
            duration = 0.75
        try:
            js_utils.post_message(self.driver, message, duration, style=style)
        except Exception:
            print(" * %s message: %s" % (style.upper(), message))
        if pause:
            duration = float(duration) + 0.15
            time.sleep(float(duration))

    def post_message_and_highlight(self, message, selector, by="css selector"):
        """Post a message on the screen and highlight an element.
        Arguments:
            message: The message to display.
            selector: The selector of the Element to highlight.
            by: The type of selector to search by. (Default: CSS Selector)
        """
        self.__check_scope()
        self.__highlight_with_assert_success(message, selector, by=by)

    def post_success_message(self, message, duration=None, pause=True):
        """Post a success message on the screen with Messenger.
        Arguments:
            message: The success message to display.
            duration: The time until the message vanishes. (Default: 2.55s)
            pause: If True, the program waits until the message completes.
        """
        self.__check_scope()
        self.__check_browser()
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        if (
            (self.headless or self.headless2 or self.xvfb)
            and float(duration) > 0.75
        ):
            duration = 0.75
        try:
            js_utils.post_message(
                self.driver, message, duration, style="success"
            )
        except Exception:
            print(" * SUCCESS message: %s" % message)
        if pause:
            duration = float(duration) + 0.15
            time.sleep(float(duration))

    def post_error_message(self, message, duration=None, pause=True):
        """Post an error message on the screen with Messenger.
        Arguments:
            message: The error message to display.
            duration: The time until the message vanishes. (Default: 2.55s)
            pause: If True, the program waits until the message completes.
        """
        self.__check_scope()
        self.__check_browser()
        if not duration:
            if not self.message_duration:
                duration = settings.DEFAULT_MESSAGE_DURATION
            else:
                duration = self.message_duration
        if (
            (self.headless or self.headless2 or self.xvfb)
            and float(duration) > 0.75
        ):
            duration = 0.75
        try:
            js_utils.post_message(
                self.driver, message, duration, style="error"
            )
        except Exception:
            print(" * ERROR message: %s" % message)
        if pause:
            duration = float(duration) + 0.15
            time.sleep(float(duration))

    ############

    def generate_referral(self, start_page, destination_page, selector=None):
        """This method opens the start_page, creates a referral link there,
        and clicks on that link, which goes to the destination_page.
        If a selector is given, clicks that on the destination_page,
        which can prevent an artificial rise in website bounce-rate.
        (This generates real traffic for testing analytics software.)"""
        self.__check_scope()
        if not page_utils.is_valid_url(destination_page):
            raise Exception(
                "Exception: destination_page {%s} is not a valid URL!"
                % destination_page
            )
        if start_page:
            if not page_utils.is_valid_url(start_page):
                raise Exception(
                    "Exception: start_page {%s} is not a valid URL! "
                    "(Use an empty string or None to start from current page.)"
                    % start_page
                )
            self.open(start_page)
            time.sleep(0.08)
            self.wait_for_ready_state_complete()
        referral_link = (
            """<body>"""
            """<a class='analytics referral test' href='%s' """
            """style='font-family: Arial,sans-serif; """
            """font-size: 30px; color: #18a2cd'>"""
            """Magic Link Button</a></body>""" % destination_page
        )
        self.execute_script(
            '''document.body.outerHTML = \"%s\"''' % referral_link
        )
        # Now click the generated button
        self.click("a.analytics.referral.test", timeout=2)
        time.sleep(0.15)
        if selector:
            self.click(selector)
            time.sleep(0.15)

    def generate_traffic(
        self, start_page, destination_page, loops=1, selector=None
    ):
        """Similar to generate_referral(), but can do multiple loops.
        If a selector is given, clicks that on the destination_page,
        which can prevent an artificial rise in website bounce-rate."""
        self.__check_scope()
        for loop in range(loops):
            self.generate_referral(
                start_page, destination_page, selector=selector
            )
            time.sleep(0.05)

    def generate_referral_chain(self, pages):
        """Use this method to chain the action of creating button links on
        one website page that will take you to the next page.
        (When you want to create a referral to a website for traffic
        generation without increasing the bounce rate, you'll want to visit
        at least one additional page on that site with a button click.)"""
        self.__check_scope()
        if not type(pages) is tuple and not type(pages) is list:
            raise Exception(
                "Exception: Expecting a list of website pages for chaining!"
            )
        if len(pages) < 2:
            raise Exception(
                "Exception: At least two website pages required for chaining!"
            )
        for page in pages:
            # Find out if any of the web pages are invalid before continuing
            if not page_utils.is_valid_url(page):
                raise Exception(
                    "Exception: Website page {%s} is not a valid URL!" % page
                )
        for page in pages:
            self.generate_referral(None, page)

    def generate_traffic_chain(self, pages, loops=1):
        """Similar to generate_referral_chain(), but for multiple loops."""
        self.__check_scope()
        for loop in range(loops):
            self.generate_referral_chain(pages)
            time.sleep(0.05)

    ############

    def wait_for_element_present(
        self, selector, by="css selector", timeout=None
    ):
        """Waits for an element to appear in the HTML of a page.
        The element does not need be visible (it may be hidden)."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_element_present(selector, timeout)
        return page_actions.wait_for_element_present(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )

    def wait_for_element(self, selector, by="css selector", timeout=None):
        """Waits for an element to appear in the HTML of a page.
        The element must be visible (it cannot be hidden)."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        if by == By.XPATH:
                            selector = original_selector
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["wf_el", selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_element_visible(selector, timeout)
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout
        )

    def get_element(self, selector, by="css selector", timeout=None):
        """Same as wait_for_element_present() - returns the element.
        The element does not need be visible (it may be hidden)."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return self.wait_for_element_present(selector, by=by, timeout=timeout)

    def wait_for_query_selector(
        self, selector, by="css selector", timeout=None
    ):
        """Waits for an element to appear in the HTML of a page.
        The element does not need be visible (it may be hidden).
        This method uses document.querySelector() over Selenium."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        css_selector = self.convert_to_css_selector(selector, by=by)
        return js_utils.wait_for_css_query_selector(
            self.driver, css_selector, timeout
        )

    def assert_element_present(
        self, selector, by="css selector", timeout=None
    ):
        """Similar to wait_for_element_present(), but returns nothing.
        Waits for an element to appear in the HTML of a page.
        The element does not need be visible (it may be hidden).
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if type(selector) is list:
            self.assert_elements_present(selector, by=by, timeout=timeout)
            return True
        if self.__is_shadow_selector(selector):
            self.__assert_shadow_element_present(selector)
            return True
        self.wait_for_element_present(selector, by=by, timeout=timeout)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["as_ep", selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    def assert_elements_present(self, *args, **kwargs):
        """Similar to self.assert_element_present(),
            but can assert that multiple elements are present in the HTML.
        The input is a list of elements.
        Optional kwargs include "by" and "timeout" (used by all selectors).
        Raises an exception if any of the elements are not visible.
        Examples:
            self.assert_elements_present("head", "style", "script", "body")
            OR
            self.assert_elements_present(["head", "body", "h1", "h2"])
        """
        self.__check_scope()
        selectors = []
        timeout = None
        by = By.CSS_SELECTOR
        for kwarg in kwargs:
            if kwarg == "timeout":
                timeout = kwargs["timeout"]
            elif kwarg == "by":
                by = kwargs["by"]
            elif kwarg == "selector":
                selector = kwargs["selector"]
                if type(selector) is str:
                    selectors.append(selector)
                elif type(selector) is list:
                    selectors_list = selector
                    for selector in selectors_list:
                        if type(selector) is str:
                            selectors.append(selector)
            else:
                raise Exception('Unknown kwarg: "%s"!' % kwarg)
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        for arg in args:
            if type(arg) is list:
                for selector in arg:
                    if type(selector) is str:
                        selectors.append(selector)
            elif type(arg) is str:
                selectors.append(arg)
        for selector in selectors:
            if self.__is_shadow_selector(selector):
                self.__assert_shadow_element_visible(selector)
                continue
            self.wait_for_element_present(selector, by=by, timeout=timeout)
            continue
        return True

    def find_element(self, selector, by="css selector", timeout=None):
        """Same as wait_for_element_visible() - returns the element"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def assert_element(self, selector, by="css selector", timeout=None):
        """Similar to wait_for_element_visible(), but returns nothing.
        As above, will raise an exception if nothing can be found.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        if type(selector) is list:
            self.assert_elements(selector, by=by, timeout=timeout)
            return True
        if self.__is_shadow_selector(selector):
            self.__assert_shadow_element_visible(selector)
            return True
        self.wait_for_element_visible(selector, by=by, timeout=timeout)
        original_selector = selector
        if self.demo_mode:
            selector, by = self.__recalculate_selector(
                selector, by, xp_ok=False
            )
            a_t = "ASSERT"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert(self._language)
            messenger_post = "%s %s: %s" % (a_t, by.upper(), selector)
            self.__highlight_with_assert_success(messenger_post, selector, by)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        if by == By.XPATH:
                            selector = original_selector
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["as_el", selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    def assert_element_visible(
        self, selector, by="css selector", timeout=None
    ):
        """Same as self.assert_element()
        As above, will raise an exception if nothing can be found."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.assert_element(selector, by=by, timeout=timeout)
        return True

    def assert_elements(self, *args, **kwargs):
        """Similar to self.assert_element(), but can assert multiple elements.
        The input is a list of elements.
        Optional kwargs include "by" and "timeout" (used by all selectors).
        Raises an exception if any of the elements are not visible.
        Examples:
            self.assert_elements("h1", "h2", "h3")
            OR
            self.assert_elements(["h1", "h2", "h3"])"""
        self.__check_scope()
        selectors = []
        timeout = None
        by = By.CSS_SELECTOR
        for kwarg in kwargs:
            if kwarg == "timeout":
                timeout = kwargs["timeout"]
            elif kwarg == "by":
                by = kwargs["by"]
            elif kwarg == "selector":
                selector = kwargs["selector"]
                if type(selector) is str:
                    selectors.append(selector)
                elif type(selector) is list:
                    selectors_list = selector
                    for selector in selectors_list:
                        if type(selector) is str:
                            selectors.append(selector)
            else:
                raise Exception('Unknown kwarg: "%s"!' % kwarg)
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        for arg in args:
            if type(arg) is list:
                for selector in arg:
                    if type(selector) is str:
                        selectors.append(selector)
            elif type(arg) is str:
                selectors.append(arg)
        for selector in selectors:
            if self.__is_shadow_selector(selector):
                self.__assert_shadow_element_visible(selector)
                continue
            self.wait_for_element_visible(selector, by=by, timeout=timeout)
            if self.demo_mode:
                selector, by = self.__recalculate_selector(selector, by)
                a_t = "ASSERT"
                if self._language != "English":
                    from seleniumbase.fixtures.words import SD

                    a_t = SD.translate_assert(self._language)
                messenger_post = "%s %s: %s" % (a_t, by.upper(), selector)
                self.__highlight_with_assert_success(
                    messenger_post, selector, by
                )
            continue
        return True

    def assert_elements_visible(self, *args, **kwargs):
        """Same as self.assert_elements()
        Raises an exception if any element cannot be found."""
        return self.assert_elements(*args, **kwargs)

    ############

    def wait_for_text_visible(
        self, text, selector="html", by="css selector", timeout=None
    ):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        text = self.__get_type_checked_text(text)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_shadow_text_visible(text, selector, timeout)
        return page_actions.wait_for_text_visible(
            self.driver, text, selector, by, timeout, self.browser
        )

    def wait_for_exact_text_visible(
        self, text, selector="html", by="css selector", timeout=None
    ):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            return self.__wait_for_exact_shadow_text_visible(
                text, selector, timeout
            )
        return page_actions.wait_for_exact_text_visible(
            self.driver, text, selector, by, timeout, self.browser
        )

    def wait_for_text(
        self, text, selector="html", by="css selector", timeout=None
    ):
        """The shorter version of wait_for_text_visible()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout
        )

    def find_text(
        self, text, selector="html", by="css selector", timeout=None
    ):
        """Same as wait_for_text_visible() - returns the element"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_text_visible(
            text, selector, by=by, timeout=timeout
        )

    def assert_text_visible(
        self, text, selector="html", by="css selector", timeout=None
    ):
        """Same as assert_text()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.assert_text(text, selector, by=by, timeout=timeout)

    def assert_text(
        self, text, selector="html", by="css selector", timeout=None
    ):
        """Similar to wait_for_text_visible()
        Raises an exception if the element or the text is not found.
        The text only needs to be a subset within the complete text.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            self.__assert_shadow_text_visible(text, selector, timeout)
            return True
        self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
        if self.demo_mode:
            a_t = "ASSERT TEXT"
            i_n = "in"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert_text(self._language)
                i_n = SD.translate_in(self._language)
            messenger_post = "%s: {%s} %s %s: %s" % (
                a_t,
                text,
                i_n,
                by.upper(),
                selector,
            )
            self.__highlight_with_assert_success(messenger_post, selector, by)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        if by == By.XPATH:
                            selector = original_selector
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        text_selector = [text, selector]
                        action = ["as_te", text_selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    def assert_exact_text(
        self, text, selector="html", by="css selector", timeout=None
    ):
        """Similar to assert_text(), but the text must be exact,
        rather than exist as a subset of the full text.
        (Extra whitespace at the beginning or the end doesn't count.)
        Raises an exception if the element or the text is not found.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        if self.__is_shadow_selector(selector):
            self.__assert_exact_shadow_text_visible(text, selector, timeout)
            return True
        self.wait_for_exact_text_visible(
            text, selector, by=by, timeout=timeout
        )
        if self.demo_mode:
            a_t = "ASSERT EXACT TEXT"
            i_n = "in"
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert_exact_text(self._language)
                i_n = SD.translate_in(self._language)
            messenger_post = "%s: {%s} %s %s: %s" % (
                a_t,
                text,
                i_n,
                by.upper(),
                selector,
            )
            self.__highlight_with_assert_success(messenger_post, selector, by)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        if by == By.XPATH:
                            selector = original_selector
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        text_selector = [text, selector]
                        action = ["as_et", text_selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    ############

    def wait_for_link_text_present(self, link_text, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 5)):
            shared_utils.check_if_time_limit_exceeded()
            try:
                if not self.is_link_text_present(link_text):
                    raise Exception(
                        "Link text {%s} was not found!" % link_text
                    )
                return
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.2)
        message = "Link text {%s} was not present after %s seconds!" % (
            link_text,
            timeout,
        )
        page_actions.timeout_exception("NoSuchElementException", message)

    def wait_for_partial_link_text_present(self, link_text, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for x in range(int(timeout * 5)):
            shared_utils.check_if_time_limit_exceeded()
            try:
                if not self.is_partial_link_text_present(link_text):
                    raise Exception(
                        "Partial Link text {%s} was not found!" % link_text
                    )
                return
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.2)
        message = (
            "Partial Link text {%s} was not present after %s seconds!"
            "" % (link_text, timeout)
        )
        page_actions.timeout_exception("NoSuchElementException", message)

    def wait_for_link_text_visible(self, link_text, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(
            link_text, by="link text", timeout=timeout
        )

    def wait_for_link_text(self, link_text, timeout=None):
        """The shorter version of wait_for_link_text_visible()"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def find_link_text(self, link_text, timeout=None):
        """Same as wait_for_link_text_visible() - returns the element"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def assert_link_text(self, link_text, timeout=None):
        """Similar to wait_for_link_text_visible(), but returns nothing.
        As above, will raise an exception if nothing can be found.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
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
            messenger_post = "%s: {%s}" % (a_t, link_text)
            self.__highlight_with_assert_success(
                messenger_post, link_text, by="link text"
            )
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["as_lt", link_text, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    def wait_for_partial_link_text(self, partial_link_text, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_element_visible(
            partial_link_text, by="partial link text", timeout=timeout
        )

    def find_partial_link_text(self, partial_link_text, timeout=None):
        """Same as wait_for_partial_link_text() - returns the element"""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_partial_link_text(
            partial_link_text, timeout=timeout
        )

    def assert_partial_link_text(self, partial_link_text, timeout=None):
        """Similar to wait_for_partial_link_text(), but returns nothing.
        As above, will raise an exception if nothing can be found.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
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
            messenger_post = "%s: {%s}" % (a_t, partial_link_text)
            self.__highlight_with_assert_success(
                messenger_post, partial_link_text, by="partial link text"
            )
        return True

    ############

    def wait_for_element_absent(
        self, selector, by="css selector", timeout=None
    ):
        """Waits for an element to no longer appear in the HTML of a page.
        A hidden element counts as a present element, which fails this assert.
        If waiting for elements to be hidden instead of nonexistent,
        use wait_for_element_not_visible() instead.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_absent(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )

    def assert_element_absent(self, selector, by="css selector", timeout=None):
        """Similar to wait_for_element_absent()
        As above, will raise an exception if the element stays present.
        A hidden element counts as a present element, which fails this assert.
        If you want to assert that elements are hidden instead of nonexistent,
        use assert_element_not_visible() instead.
        (Note that hidden elements are still present in the HTML of the page.)
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_absent(selector, by=by, timeout=timeout)
        return True

    ############

    def wait_for_element_not_visible(
        self, selector, by="css selector", timeout=None
    ):
        """Waits for an element to no longer be visible on a page.
        The element can be non-existent in the HTML or hidden on the page
        to qualify as not visible."""
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        original_selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_element_not_visible(
            self.driver,
            selector,
            by,
            timeout=timeout,
            original_selector=original_selector,
        )

    def assert_element_not_visible(
        self, selector, by="css selector", timeout=None
    ):
        """Similar to wait_for_element_not_visible()
        As above, will raise an exception if the element stays visible.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_element_not_visible(selector, by=by, timeout=timeout)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["asenv", selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    ############

    def wait_for_text_not_visible(
        self, text, selector="html", by="css selector", timeout=None
    ):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_text_not_visible(
            self.driver, text, selector, by, timeout, self.browser
        )

    def assert_text_not_visible(
        self, text, selector="html", by="css selector", timeout=None
    ):
        """Similar to wait_for_text_not_visible()
        Raises an exception if the text is still visible after timeout.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.wait_for_text_not_visible(text, selector, by=by, timeout=timeout)
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        text_selector = [text, selector]
                        action = ["astnv", text_selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        return True

    ############

    def wait_for_attribute_not_present(
        self, selector, attribute, value=None, by="css selector", timeout=None
    ):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        return page_actions.wait_for_attribute_not_present(
            self.driver, selector, attribute, value, by, timeout
        )

    def assert_attribute_not_present(
        self, selector, attribute, value=None, by="css selector", timeout=None
    ):
        """Similar to wait_for_attribute_not_present()
        Raises an exception if the attribute is still present after timeout.
        Returns True if successful. Default timeout = SMALL_TIMEOUT."""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return self.wait_for_attribute_not_present(
            selector, attribute, value=value, by=by, timeout=timeout
        )

    ############

    def wait_for_and_accept_alert(self, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def wait_for_and_dismiss_alert(self, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def wait_for_and_switch_to_alert(self, timeout=None):
        self.__check_scope()
        if not timeout:
            timeout = settings.LARGE_TIMEOUT
        if self.timeout_multiplier and timeout == settings.LARGE_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)

    ############

    def accept_alert(self, timeout=None):
        """Same as wait_for_and_accept_alert(), but smaller default T_O"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_accept_alert(self.driver, timeout)

    def dismiss_alert(self, timeout=None):
        """Same as wait_for_and_dismiss_alert(), but smaller default T_O"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_dismiss_alert(self.driver, timeout)

    def switch_to_alert(self, timeout=None):
        """Same as wait_for_and_switch_to_alert(), but smaller default T_O"""
        self.__check_scope()
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        return page_actions.wait_for_and_switch_to_alert(self.driver, timeout)

    ############

    def quit_extra_driver(self, driver=None):
        """Quits the driver only if it's not the default/initial driver.
        If a driver is given, quits that, otherwise quits the active driver.
        Raises an Exception if quitting the default/initial driver.
        Should only be called if a test has already called get_new_driver().
        Afterwards, self.driver points to the default/initial driver
        if self.driver was the one being quit.
        ----
        If a test never calls get_new_driver(), this method isn't needed.
        SeleniumBase automatically quits browsers after tests have ended.
        Even if tests do call get_new_driver(), you don't need to use this
        method unless you want to quit extra browsers before a test ends.
        ----
        Terminology and important details:
        * Active driver: The one self.driver is set to. Used within methods.
        * Default/initial driver: The one that is spun up when tests start.
        Initially, the active driver and the default driver are the same.
        The active driver can change when one of these methods is called:
        > self.get_new_driver()
        > self.switch_to_default_driver()
        > self.switch_to_driver()
        > self.quit_extra_driver()
        """
        self.__check_scope()
        if not driver:
            driver = self.driver
        if type(driver).__name__ == "NoneType":
            raise Exception("The driver to quit was a NoneType variable!")
        elif (
            not hasattr(driver, "get")
            or not hasattr(driver, "name")
            or not hasattr(driver, "quit")
            or not hasattr(driver, "capabilities")
            or not hasattr(driver, "window_handles")
        ):
            raise Exception("The driver to quit does not match a Driver!")
        elif self._reuse_session and driver == self._default_driver:
            raise Exception(
                "Cannot quit the initial driver in --reuse-session mode!\n"
                "This is done automatically after all tests have ended.\n"
                "Use this method only if get_new_driver() has been called."
            )
        elif (
            driver == self._default_driver
            or (driver in self._drivers_list and len(self._drivers_list) == 1)
        ):
            raise Exception(
                "Cannot quit the default/initial driver!\n"
                "This is done automatically at the end of each test.\n"
                "Use this method only if get_new_driver() has been called."
            )
        try:
            if (
                not is_windows
                or self.browser == "ie"
                or driver.service.process
            ):
                driver.quit()
        except AttributeError:
            pass
        except Exception:
            pass
        if driver in self._drivers_list:
            self._drivers_list.remove(driver)
            if driver in self._drivers_browser_map:
                del self._drivers_browser_map[driver]
        # If the driver to quit was the active driver, switch drivers
        if driver == self.driver:
            self.switch_to_default_driver()

    ############

    def __assert_eq(self, *args, **kwargs):
        """Minified assert_equal() using only the list diff."""
        minified_exception = None
        try:
            self.assertEqual(*args, **kwargs)
        except Exception as e:
            str_e = str(e)
            minified_exception = "\nAssertionError:\n"
            lines = str_e.split("\n")
            countdown = 3
            countdown_on = False
            first_differing = False
            skip_lines = False
            for line in lines:
                if countdown_on:
                    if not skip_lines:
                        minified_exception += line + "\n"
                    countdown = countdown - 1
                    if countdown == 0:
                        countdown_on = False
                        skip_lines = False
                elif line.startswith("First differing"):
                    first_differing = True
                    countdown_on = True
                    countdown = 3
                    minified_exception += line + "\n"
                elif line.startswith("First list"):
                    countdown_on = True
                    countdown = 3
                    if not first_differing:
                        minified_exception += line + "\n"
                    else:
                        skip_lines = True
                elif line.startswith("F"):
                    countdown_on = True
                    countdown = 3
                    minified_exception += line + "\n"
                elif line.startswith("+") or line.startswith("-"):
                    minified_exception += line + "\n"
                elif line.startswith("?"):
                    minified_exception += line + "\n"
                elif line.strip().startswith("*"):
                    minified_exception += line + "\n"
        if minified_exception:
            from seleniumbase.common.exceptions import VisualException

            raise VisualException(minified_exception)

    def _process_visual_baseline_logs(self):
        if sys.version_info < (3, 11):
            return
        self.__process_visual_baseline_logs()

    def __process_visual_baseline_logs(self):
        """Save copies of baseline PNGs in "./latest_logs" during failures.
        Also create a side_by_side.html file for visual comparisons."""
        test_logpath = os.path.join(self.log_path, self.__get_test_id())
        for baseline_copy_tuple in self.__visual_baseline_copies:
            baseline_path = baseline_copy_tuple[0]
            baseline_copy_name = baseline_copy_tuple[1]
            b_c_alt_name = baseline_copy_tuple[2]
            latest_png_path = baseline_copy_tuple[3]
            latest_copy_name = baseline_copy_tuple[4]
            l_c_alt_name = baseline_copy_tuple[5]
            baseline_copy_path = os.path.join(test_logpath, baseline_copy_name)
            b_c_alt_path = os.path.join(test_logpath, b_c_alt_name)
            latest_copy_path = os.path.join(test_logpath, latest_copy_name)
            l_c_alt_path = os.path.join(test_logpath, l_c_alt_name)
            if len(self.__visual_baseline_copies) == 1:
                baseline_copy_path = b_c_alt_path
                latest_copy_path = l_c_alt_path
            if (
                os.path.exists(baseline_path)
                and not os.path.exists(baseline_copy_path)
            ):
                self.__create_log_path_as_needed(test_logpath)
                shutil.copy(baseline_path, baseline_copy_path)
            if (
                os.path.exists(latest_png_path)
                and not os.path.exists(latest_copy_path)
            ):
                self.__create_log_path_as_needed(test_logpath)
                shutil.copy(latest_png_path, latest_copy_path)
        if len(self.__visual_baseline_copies) != 1:
            return  # Skip the rest when deferred visual asserts are used
        from seleniumbase.core import visual_helper

        the_html = visual_helper.get_sbs_html()
        file_path = os.path.join(test_logpath, constants.SideBySide.HTML_FILE)
        out_file = codecs.open(file_path, "w+", encoding="utf-8")
        out_file.writelines(the_html)
        out_file.close()

    def check_window(
        self,
        name="default",
        level=0,
        baseline=False,
        check_domain=True,
        full_diff=False,
    ):
        """***  Automated Visual Testing with SeleniumBase  ***

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
            DRY RUN ONLY - Will perform comparisons to the baseline (and
                           print out any differences that are found) but
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
        if the page domain doesn't match the domain of the baseline,
        unless "check_domain" is set to False when calling check_window().

        If you want to use self.check_window() to compare a web page to
        a later version of itself from within the same test run, you can
        add the parameter "baseline=True" to the first time you call
        self.check_window() in a test to use that as the baseline. This
        only makes sense if you're calling self.check_window() more than
        once with the same name parameter in the same test.

        If "full_diff" is set to False, the error output will only
        include the first differing element in the list comparison.
        Set "full_diff" to True if you want to see the full output.

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
        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.05)  # Force a minimum wait, even if skipping waits.
        try:
            self.wait_for_element_visible(
                "body", timeout=settings.MINI_TIMEOUT
            )
        except Exception:
            pass
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
            message = (
                "WARNING: Using check_window() from Demo Mode may lead "
                "to unexpected results caused by Demo Mode HTML changes."
            )
            logging.info(message)

        test_id = self.__get_display_id().split("::")[-1]

        if not name or len(name) < 1:
            name = "default"
        name = str(name)
        from seleniumbase.core import visual_helper

        visual_helper.visual_baseline_folder_setup()
        baseline_dir = constants.VisualBaseline.STORAGE_FOLDER
        visual_baseline_path = os.path.join(baseline_dir, test_id, name)
        page_url_file = os.path.join(visual_baseline_path, "page_url.txt")
        baseline_png = "baseline.png"
        baseline_png_path = os.path.join(visual_baseline_path, baseline_png)
        latest_png = "latest.png"
        latest_png_path = os.path.join(visual_baseline_path, latest_png)
        level_1_file = os.path.join(visual_baseline_path, "tags_level_1.txt")
        level_2_file = os.path.join(visual_baseline_path, "tags_level_2.txt")
        level_3_file = os.path.join(visual_baseline_path, "tags_level_3.txt")

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
        if not os.path.exists(baseline_png_path):
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
            self.save_screenshot(
                baseline_png, visual_baseline_path, selector="body"
            )
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

        baseline_path = os.path.join(visual_baseline_path, baseline_png)
        baseline_copy_name = "baseline_%s.png" % name
        b_c_alt_name = "baseline.png"
        latest_copy_name = "baseline_diff_%s.png" % name
        l_c_alt_name = "baseline_diff.png"
        baseline_copy_tuple = (
            baseline_path, baseline_copy_name, b_c_alt_name,
            latest_png_path, latest_copy_name, l_c_alt_name,
        )
        self.__visual_baseline_copies.append(baseline_copy_tuple)

        is_level_0_failure = False
        if not set_baseline:
            self.save_screenshot(
                latest_png, visual_baseline_path, selector="body"
            )
            f = open(page_url_file, "r")
            page_url_data = f.read().strip()
            f.close()
            f = open(level_1_file, "r")
            level_1_data = json.loads(f.read())
            f.close()
            f = open(level_2_file, "r")
            level_2_data = json.loads(f.read())
            f.close()
            f = open(level_3_file, "r")
            level_3_data = json.loads(f.read())
            f.close()

            domain_fail = (
                "\n*\nPage Domain Mismatch Failure: "
                "Current Page Domain doesn't match the Page Domain of the "
                "Baseline! Can't compare two completely different sites! "
                "Run with --visual_baseline to reset the baseline!"
            )
            level_1_failure = (
                "\n*\n*** Exception: <Level 1> Visual Diff Failure:\n"
                "* HTML tags don't match the baseline!"
            )
            level_2_failure = (
                "\n*\n*** Exception: <Level 2> Visual Diff Failure:\n"
                "* HTML tag attribute names don't match the baseline!"
            )
            level_3_failure = (
                "\n*\n*** Exception: <Level 3> Visual Diff Failure:\n"
                "* HTML tag attribute values don't match the baseline!"
            )

            page_domain = self.get_domain_url(page_url)
            page_data_domain = self.get_domain_url(page_url_data)
            unittest.TestCase.maxDiff = 65536  # 2^16
            if level != 0 and check_domain:
                self.assertEqual(page_data_domain, page_domain, domain_fail)
            if level == 3:
                if not full_diff:
                    self.__assert_eq(level_3_data, level_3, level_3_failure)
                else:
                    self.assertEqual(level_3_data, level_3, level_3_failure)
            if level == 2:
                if not full_diff:
                    self.__assert_eq(level_2_data, level_2, level_2_failure)
                else:
                    self.assertEqual(level_2_data, level_2, level_2_failure)
            if level == 1:
                if not full_diff:
                    self.__assert_eq(level_1_data, level_1, level_1_failure)
                else:
                    self.assertEqual(level_1_data, level_1, level_1_failure)
            if level == 0:
                try:
                    if check_domain:
                        self.assertEqual(
                            page_domain, page_data_domain, domain_fail
                        )
                    try:
                        if not full_diff:
                            self.__assert_eq(
                                level_1_data, level_1, level_1_failure
                            )
                        else:
                            self.assertEqual(
                                level_1_data, level_1, level_1_failure
                            )
                    except Exception as e:
                        print(e)
                    try:
                        if not full_diff:
                            self.__assert_eq(
                                level_2_data, level_2, level_2_failure
                            )
                        else:
                            self.assertEqual(
                                level_2_data, level_2, level_2_failure
                            )
                    except Exception as e:
                        print(e)
                    if not full_diff:
                        self.__assert_eq(
                            level_3_data, level_3, level_3_failure
                        )
                    else:
                        self.assertEqual(
                            level_3_data, level_3, level_3_failure
                        )
                except Exception as e:
                    print(e)  # Level-0 Dry Run (Only print the differences)
                    is_level_0_failure = True
            unittest.TestCase.maxDiff = None  # Reset unittest.TestCase.maxDiff
        # Since the check passed, do not save an extra copy of the baseline
        del self.__visual_baseline_copies[-1]  # .pop() returns the element
        if is_level_0_failure:
            # Generating the side_by_side.html file for Level-0 failures
            test_logpath = os.path.join(self.log_path, self.__get_test_id())
            if (
                not os.path.exists(baseline_path)
                or not os.path.exists(latest_png_path)
            ):
                return
            self.__level_0_visual_f = True
            if not os.path.exists(test_logpath):
                self.__create_log_path_as_needed(test_logpath)
            baseline_copy_path = os.path.join(test_logpath, baseline_copy_name)
            latest_copy_path = os.path.join(test_logpath, latest_copy_name)
            if (
                not os.path.exists(baseline_copy_path)
                and not os.path.exists(latest_copy_path)
            ):
                shutil.copy(baseline_path, baseline_copy_path)
                shutil.copy(latest_png_path, latest_copy_path)
            the_html = visual_helper.get_sbs_html(
                baseline_copy_name, latest_copy_name
            )
            alpha_n_d_name = "".join([x if x.isalnum() else "_" for x in name])
            side_by_side_name = "side_by_side_%s.html" % alpha_n_d_name
            file_path = os.path.join(test_logpath, side_by_side_name)
            out_file = codecs.open(file_path, "w+", encoding="utf-8")
            out_file.writelines(the_html)
            out_file.close()

    ############

    def __get_new_timeout(self, timeout):
        """When using --timeout_multiplier=#.#"""
        self.__check_scope()
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

    def __check_scope(self):
        if hasattr(self, "browser"):  # self.browser stores the type of browser
            return  # All good: setUp() already initialized variables in "self"
        else:
            from seleniumbase.common.exceptions import OutOfScopeException

            message = (
                "\n It looks like you are trying to call a SeleniumBase method"
                "\n from outside the scope of your test class's `self` object,"
                "\n which is initialized by calling BaseCase's setUp() method."
                "\n The `self` object is where all test variables are defined."
                "\n If you created a custom setUp() method (that overrided the"
                "\n the default one), make sure to call super().setUp() in it."
                "\n When using page objects, be sure to pass the `self` object"
                "\n from your test class into your page object methods so that"
                "\n they can call BaseCase class methods with all the required"
                "\n variables, which are initialized during the setUp() method"
                "\n that runs automatically before all tests called by pytest."
            )
            raise OutOfScopeException(message)

    ############

    def __check_browser(self):
        """This method raises an exception if the window was already closed."""
        active_window = None
        try:
            active_window = self.driver.current_window_handle  # Fails if None
        except Exception:
            pass
        if not active_window:
            raise NoSuchWindowException("Active window was already closed!")

    ############

    def __get_exception_message(self):
        """This method extracts the message from an exception if there
        was an exception that occurred during the test, assuming
        that the exception was in a try/except block and not thrown."""
        exception_info = sys.exc_info()[1]
        if hasattr(exception_info, "msg"):
            exc_message = exception_info.msg
        elif hasattr(exception_info, "message"):
            exc_message = exception_info.message
        else:
            exc_message = sys.exc_info()
        return exc_message

    def __add_deferred_assert_failure(self, fs=False):
        """Add a deferred_assert failure to a list for future processing."""
        self.__check_scope()
        current_url = self.driver.current_url
        message = self.__get_exception_message()
        count = self.__deferred_assert_count
        self.__deferred_assert_failures.append(
            "DEFERRED ASSERT #%s: (%s) %s\n" % (count, current_url, message)
        )
        if fs:
            self.save_screenshot_to_logs(name="deferred_#%s" % count)

    ############

    def deferred_assert_element(
        self, selector, by="css selector", timeout=None, fs=False
    ):
        """A non-terminating assertion for an element visible on the page.
        Failures will be saved until the process_deferred_asserts()
        method is called from inside a test, likely at the end of it.
        If "fs" is set to True, a failure screenshot is saved to the
        "latest_logs/" folder for that assertion failure. Otherwise,
        only the last page screenshot is taken for all failures when
        calling the process_deferred_asserts() method.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.MINI_TIMEOUT
        if self.timeout_multiplier and timeout == settings.MINI_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__deferred_assert_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_deferred_assert:
                timeout = 0.6  # Was already on page (full wait not needed)
            else:
                self.__last_url_of_deferred_assert = url
        except Exception:
            pass
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["da_el", selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        try:
            self.wait_for_element_visible(selector, by=by, timeout=timeout)
            return True
        except Exception:
            self.__add_deferred_assert_failure(fs=fs)
            return False

    def deferred_assert_element_present(
        self, selector, by="css selector", timeout=None, fs=False
    ):
        """A non-terminating assertion for an element present in the page html.
        Failures will be saved until the process_deferred_asserts()
        method is called from inside a test, likely at the end of it.
        If "fs" is set to True, a failure screenshot is saved to the
        "latest_logs/" folder for that assertion failure. Otherwise,
        only the last page screenshot is taken for all failures when
        calling the process_deferred_asserts() method.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.MINI_TIMEOUT
        if self.timeout_multiplier and timeout == settings.MINI_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__deferred_assert_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_deferred_assert:
                timeout = 0.6  # Was already on page (full wait not needed)
            else:
                self.__last_url_of_deferred_assert = url
        except Exception:
            pass
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        action = ["da_ep", selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        try:
            self.wait_for_element_present(selector, by=by, timeout=timeout)
            return True
        except Exception:
            self.__add_deferred_assert_failure(fs=fs)
            return False

    def deferred_assert_text(
        self, text, selector="html", by="css selector", timeout=None, fs=False
    ):
        """A non-terminating assertion for text from an element on a page.
        Failures will be saved until the process_deferred_asserts()
        method is called from inside a test, likely at the end of it.
        If "fs" is set to True, a failure screenshot is saved to the
        "latest_logs/" folder for that assertion failure. Otherwise,
        only the last page screenshot is taken for all failures when
        calling the process_deferred_asserts() method.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.MINI_TIMEOUT
        if self.timeout_multiplier and timeout == settings.MINI_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__deferred_assert_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_deferred_assert:
                timeout = 0.6  # Was already on page (full wait not needed)
            else:
                self.__last_url_of_deferred_assert = url
        except Exception:
            pass
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        text_selector = [text, selector]
                        action = ["da_te", text_selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        try:
            self.wait_for_text_visible(text, selector, by=by, timeout=timeout)
            return True
        except Exception:
            self.__add_deferred_assert_failure(fs=fs)
            return False

    def deferred_assert_exact_text(
        self, text, selector="html", by="css selector", timeout=None, fs=False
    ):
        """A non-terminating assertion for exact text from an element.
        Failures will be saved until the process_deferred_asserts()
        method is called from inside a test, likely at the end of it.
        If "fs" is set to True, a failure screenshot is saved to the
        "latest_logs/" folder for that assertion failure. Otherwise,
        only the last page screenshot is taken for all failures when
        calling the process_deferred_asserts() method.
        """
        self.__check_scope()
        if not timeout:
            timeout = settings.MINI_TIMEOUT
        if self.timeout_multiplier and timeout == settings.MINI_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__deferred_assert_count += 1
        try:
            url = self.get_current_url()
            if url == self.__last_url_of_deferred_assert:
                timeout = 0.6  # Was already on page (full wait not needed)
            else:
                self.__last_url_of_deferred_assert = url
        except Exception:
            pass
        if self.recorder_mode:
            url = self.get_current_url()
            if url and len(url) > 0:
                if ("http:") in url or ("https:") in url or ("file:") in url:
                    if self.get_session_storage_item("pause_recorder") == "no":
                        time_stamp = self.execute_script("return Date.now();")
                        origin = self.get_origin()
                        text_selector = [text, selector]
                        action = ["da_et", text_selector, origin, time_stamp]
                        self.__extra_actions.append(action)
        try:
            self.wait_for_exact_text_visible(
                text, selector, by=by, timeout=timeout
            )
            return True
        except Exception:
            self.__add_deferred_assert_failure(fs=fs)
            return False

    def deferred_check_window(
        self,
        name="default",
        level=0,
        baseline=False,
        check_domain=True,
        full_diff=False,
        fs=False,
    ):
        """A non-terminating assertion for the check_window() method.
        Failures will be saved until the process_deferred_asserts()
        method is called from inside a test, likely at the end of it.
        If "fs" is set to True, a failure screenshot is saved to the
        "latest_logs/" folder for that assertion failure. Otherwise,
        only the last page screenshot is taken for all failures when
        calling the process_deferred_asserts() method.
        """
        self.__check_scope()
        self.__deferred_assert_count += 1
        try:
            self.check_window(
                name=name,
                level=level,
                baseline=baseline,
                check_domain=check_domain,
                full_diff=full_diff,
            )
            return True
        except Exception:
            self.__add_deferred_assert_failure(fs=fs)
            return False

    def process_deferred_asserts(self, print_only=False):
        """To be used with any test that uses deferred_asserts, which are
        non-terminating verifications that only raise exceptions
        after this method is called.
        This is useful for pages with multiple elements to be checked when
        you want to find as many bugs as possible in a single test run
        before having all the exceptions get raised simultaneously.
        Might be more useful if this method is called after processing all
        the deferred asserts on a single html page so that the failure
        screenshot matches the location of the deferred asserts.
        If "print_only" is set to True, the exception won't get raised."""
        if self.recorder_mode:
            time_stamp = self.execute_script("return Date.now();")
            origin = self.get_origin()
            action = ["pr_da", "", origin, time_stamp]
            self.__extra_actions.append(action)
        if self.__deferred_assert_failures:
            exception_output = ""
            exception_output += "\n***** DEFERRED ASSERTION FAILURES:\n"
            exception_output += "TEST: %s\n\n" % self.id()
            all_failing_checks = self.__deferred_assert_failures
            self.__deferred_assert_failures = []
            for tb in all_failing_checks:
                exception_output += "%s\n" % tb
            if print_only:
                print(exception_output)
            else:
                raise Exception(exception_output.replace("\\n", "\n"))

    ############

    # Alternate naming scheme for the "deferred_assert" methods.

    def delayed_assert_element(
        self, selector, by="css selector", timeout=None, fs=False
    ):
        """Same as self.deferred_assert_element()"""
        return self.deferred_assert_element(
            selector=selector, by=by, timeout=timeout, fs=fs
        )

    def delayed_assert_element_present(
        self, selector, by="css selector", timeout=None, fs=False
    ):
        """Same as self.deferred_assert_element_present()"""
        return self.deferred_assert_element_present(
            selector=selector, by=by, timeout=timeout, fs=fs
        )

    def delayed_assert_text(
        self, text, selector="html", by="css selector", timeout=None, fs=False
    ):
        """Same as self.deferred_assert_text()"""
        return self.deferred_assert_text(
            text=text, selector=selector, by=by, timeout=timeout, fs=fs
        )

    def delayed_assert_exact_text(
        self, text, selector="html", by="css selector", timeout=None, fs=False
    ):
        """Same as self.deferred_assert_exact_text()"""
        return self.deferred_assert_exact_text(
            text=text, selector=selector, by=by, timeout=timeout, fs=fs
        )

    def delayed_check_window(
        self,
        name="default",
        level=0,
        baseline=False,
        check_domain=True,
        full_diff=False,
        fs=False,
    ):
        """Same as self.deferred_check_window()"""
        return self.deferred_check_window(
            name=name,
            level=level,
            baseline=baseline,
            check_domain=check_domain,
            full_diff=full_diff,
            fs=fs,
        )

    def process_delayed_asserts(self, print_only=False):
        """Same as self.process_deferred_asserts()"""
        self.process_deferred_asserts(print_only=print_only)

    ############

    def create_presentation(
        self, name=None, theme="default", transition="default"
    ):
        """Creates a Reveal-JS presentation that you can add slides to.
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
        valid_themes = [
            "serif",
            "white",
            "black",
            "beige",
            "simple",
            "sky",
            "league",
            "moon",
            "night",
            "blood",
            "solarized",
        ]
        theme = theme.lower()
        if theme not in valid_themes:
            raise Exception(
                "Theme {%s} not found! Valid themes: %s"
                % (theme, valid_themes)
            )
        if not transition or transition == "default":
            transition = "none"
        valid_transitions = [
            "none",
            "slide",
            "fade",
            "zoom",
            "convex",
            "concave",
        ]
        transition = transition.lower()
        if transition not in valid_transitions:
            raise Exception(
                "Transition {%s} not found! Valid transitions: %s"
                % (transition, valid_transitions)
            )

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
            "<html>\n"
            "<head>\n"
            '<meta charset="utf-8">\n'
            '<meta http-equiv="Content-Type" content="text/html">\n'
            '<meta name="viewport" content="shrink-to-fit=no">\n'
            '<link rel="stylesheet" href="%s">\n'
            '<link rel="stylesheet" href="%s">\n'
            "<style>\n"
            "pre{background-color:#fbe8d4;border-radius:8px;}\n"
            "div[flex_div]{height:68vh;margin:0;align-items:center;"
            "justify-content:center;}\n"
            "img[rounded]{border-radius:16px;max-width:64%%;}\n"
            "</style>\n"
            "</head>\n\n"
            "<body>\n"
            "<!-- Generated by SeleniumBase - https://seleniumbase.io -->\n"
            '<div class="reveal">\n'
            '<div class="slides">\n'
            % (constants.Reveal.MIN_CSS, reveal_theme_css)
        )

        self._presentation_slides[name] = []
        self._presentation_slides[name].append(new_presentation)
        self._presentation_transition[name] = transition

    def add_slide(
        self,
        content=None,
        image=None,
        code=None,
        iframe=None,
        content2=None,
        notes=None,
        transition=None,
        name=None,
    ):
        """Allows the user to add slides to a presentation.
        @Params
        content - The HTML content to display on the presentation slide.
        image - Attach an image (from a URL link) to the slide.
        code - Attach code of any programming language to the slide.
               Language-detection will be used to add syntax formatting.
        iframe - Attach an iframe (from a URL link) to the slide.
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
        valid_transitions = [
            "none",
            "slide",
            "fade",
            "zoom",
            "convex",
            "concave",
        ]
        transition = transition.lower()
        if transition not in valid_transitions:
            raise Exception(
                "Transition {%s} not found! Valid transitions: %s"
                "" % (transition, valid_transitions)
            )
        add_line = ""
        if content.startswith("<"):
            add_line = "\n"
        html = '\n<section data-transition="%s">%s%s' % (
            transition,
            add_line,
            content,
        )
        if image:
            html += '\n<div flex_div><img rounded src="%s" /></div>' % image
        if code:
            html += "\n<div></div>"
            html += '\n<pre class="prettyprint">\n%s</pre>' % code
        if iframe:
            html += (
                "\n<div></div>"
                '\n<iframe src="%s" style="width:92%%;height:550px;" '
                'title="iframe content"></iframe>' % iframe
            )
        add_line = ""
        if content2.startswith("<"):
            add_line = "\n"
        if content2:
            html += "%s%s" % (add_line, content2)
        html += '\n<aside class="notes">%s</aside>' % notes
        html += "\n</section>\n"

        self._presentation_slides[name].append(html)

    def save_presentation(
        self, name=None, filename=None, show_notes=False, interval=0
    ):
        """Saves a Reveal-JS Presentation to a file for later use.
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
        if not filename.endswith(".html"):
            raise Exception('Presentation file must end in ".html"!')
        if not interval:
            interval = 0
        if interval == 0 and self.interval:
            interval = float(self.interval)
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
            "\n</div>\n"
            "</div>\n"
            '<script src="%s"></script>\n'
            '<script src="%s"></script>\n'
            "<script>Reveal.initialize("
            "{showNotes: %s, slideNumber: true, progress: true, hash: false, "
            "autoSlide: %s,});"
            "</script>\n"
            "</body>\n"
            "</html>\n"
            % (
                constants.Reveal.MIN_JS,
                constants.PrettifyJS.RUN_PRETTIFY_JS,
                show_notes_str,
                interval_ms,
            )
        )

        # Remove duplicate ChartMaker library declarations
        chart_libs = """
            <script src="%s"></script>
            <script src="%s"></script>
            <script src="%s"></script>
            <script src="%s"></script>
            """ % (
            constants.HighCharts.HC_JS,
            constants.HighCharts.EXPORTING_JS,
            constants.HighCharts.EXPORT_DATA_JS,
            constants.HighCharts.ACCESSIBILITY_JS,
        )
        if the_html.count(chart_libs) > 1:
            chart_libs_comment = "<!-- HighCharts Libraries Imported -->"
            the_html = the_html.replace(chart_libs, chart_libs_comment)
            # Only need to import the HighCharts libraries once
            the_html = the_html.replace(chart_libs_comment, chart_libs, 1)

        saved_presentations_folder = constants.Presentations.SAVED_FOLDER
        if saved_presentations_folder.endswith("/"):
            saved_presentations_folder = saved_presentations_folder[:-1]
        if not os.path.exists(saved_presentations_folder):
            try:
                os.makedirs(saved_presentations_folder)
            except Exception:
                pass
        file_path = os.path.join(saved_presentations_folder, filename)
        out_file = codecs.open(file_path, "w+", encoding="utf-8")
        out_file.writelines(the_html)
        out_file.close()
        print("\n>>> [%s] was saved!\n" % file_path)
        return file_path

    def begin_presentation(
        self, name=None, filename=None, show_notes=False, interval=0
    ):
        """Begin a Reveal-JS Presentation in the web browser.
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
        if self.headless or self.headless2 or self.xvfb:
            return  # Presentations should not run in headless mode.
        if not name:
            name = "default"
        if not filename:
            filename = "my_presentation.html"
        if name not in self._presentation_slides:
            raise Exception("Presentation {%s} does not exist!" % name)
        if not filename.endswith(".html"):
            raise Exception('Presentation file must end in ".html"!')
        if not interval:
            interval = 0
        if interval == 0 and self.interval:
            interval = float(self.interval)
        if not type(interval) is int and not type(interval) is float:
            raise Exception('Expecting a numeric value for "interval"!')
        if interval < 0:
            raise Exception('The "interval" cannot be a negative number!')

        end_slide = (
            '\n<section data-transition="none">\n'
            '<p class="End_Presentation_Now"> </p>\n</section>\n'
        )
        self._presentation_slides[name].append(end_slide)
        file_path = self.save_presentation(
            name=name,
            filename=filename,
            show_notes=show_notes,
            interval=interval,
        )
        self._presentation_slides[name].pop()

        self.open_html_file(file_path)
        presentation_folder = constants.Presentations.SAVED_FOLDER
        try:
            while (
                len(self.driver.window_handles) > 0
                and presentation_folder in self.get_current_url()
            ):
                time.sleep(0.05)
                if self.is_element_visible(
                    "section.present p.End_Presentation_Now"
                ):
                    break
                time.sleep(0.05)
        except Exception:
            pass

    ############

    def create_pie_chart(
        self,
        chart_name=None,
        title=None,
        subtitle=None,
        data_name=None,
        unit=None,
        libs=True,
        labels=True,
        legend=True,
    ):
        """Creates a JavaScript pie chart using "HighCharts".
        @Params
        chart_name - If creating multiple charts,
                     use this to select which one.
        title - The title displayed for the chart.
        subtitle - The subtitle displayed for the chart.
        data_name - The series name. Useful for multi-series charts.
                    If no data_name, will default to using "Series 1".
        unit - The description label given to the chart's y-axis values.
        libs - The option to include Chart libraries (JS and CSS files).
               Should be set to True (default) for the first time creating
               a chart on a web page. If creating multiple charts on the
               same web page, you won't need to re-import the libraries
               when creating additional charts.
        labels - If True, displays labels on the chart for data points.
        legend - If True, displays the data point legend on the chart.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "pie"
        self.__create_highchart(
            chart_name=chart_name,
            title=title,
            subtitle=subtitle,
            style=style,
            data_name=data_name,
            unit=unit,
            libs=libs,
            labels=labels,
            legend=legend,
        )

    def create_bar_chart(
        self,
        chart_name=None,
        title=None,
        subtitle=None,
        data_name=None,
        unit=None,
        libs=True,
        labels=True,
        legend=True,
    ):
        """Creates a JavaScript bar chart using "HighCharts".
        @Params
        chart_name - If creating multiple charts,
                     use this to select which one.
        title - The title displayed for the chart.
        subtitle - The subtitle displayed for the chart.
        data_name - The series name. Useful for multi-series charts.
                    If no data_name, will default to using "Series 1".
        unit - The description label given to the chart's y-axis values.
        libs - The option to include Chart libraries (JS and CSS files).
               Should be set to True (default) for the first time creating
               a chart on a web page. If creating multiple charts on the
               same web page, you won't need to re-import the libraries
               when creating additional charts.
        labels - If True, displays labels on the chart for data points.
        legend - If True, displays the data point legend on the chart.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "bar"
        self.__create_highchart(
            chart_name=chart_name,
            title=title,
            subtitle=subtitle,
            style=style,
            data_name=data_name,
            unit=unit,
            libs=libs,
            labels=labels,
            legend=legend,
        )

    def create_column_chart(
        self,
        chart_name=None,
        title=None,
        subtitle=None,
        data_name=None,
        unit=None,
        libs=True,
        labels=True,
        legend=True,
    ):
        """Creates a JavaScript column chart using "HighCharts".
        @Params
        chart_name - If creating multiple charts,
                     use this to select which one.
        title - The title displayed for the chart.
        subtitle - The subtitle displayed for the chart.
        data_name - The series name. Useful for multi-series charts.
                    If no data_name, will default to using "Series 1".
        unit - The description label given to the chart's y-axis values.
        libs - The option to include Chart libraries (JS and CSS files).
               Should be set to True (default) for the first time creating
               a chart on a web page. If creating multiple charts on the
               same web page, you won't need to re-import the libraries
               when creating additional charts.
        labels - If True, displays labels on the chart for data points.
        legend - If True, displays the data point legend on the chart.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "column"
        self.__create_highchart(
            chart_name=chart_name,
            title=title,
            subtitle=subtitle,
            style=style,
            data_name=data_name,
            unit=unit,
            libs=libs,
            labels=labels,
            legend=legend,
        )

    def create_line_chart(
        self,
        chart_name=None,
        title=None,
        subtitle=None,
        data_name=None,
        unit=None,
        zero=False,
        libs=True,
        labels=True,
        legend=True,
    ):
        """Creates a JavaScript line chart using "HighCharts".
        @Params
        chart_name - If creating multiple charts,
                     use this to select which one.
        title - The title displayed for the chart.
        subtitle - The subtitle displayed for the chart.
        data_name - The series name. Useful for multi-series charts.
                    If no data_name, will default to using "Series 1".
        unit - The description label given to the chart's y-axis values.
        zero - If True, the y-axis always starts at 0. (Default: False).
        libs - The option to include Chart libraries (JS and CSS files).
               Should be set to True (default) for the first time creating
               a chart on a web page. If creating multiple charts on the
               same web page, you won't need to re-import the libraries
               when creating additional charts.
        labels - If True, displays labels on the chart for data points.
        legend - If True, displays the data point legend on the chart.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "line"
        self.__create_highchart(
            chart_name=chart_name,
            title=title,
            subtitle=subtitle,
            style=style,
            data_name=data_name,
            unit=unit,
            zero=zero,
            libs=libs,
            labels=labels,
            legend=legend,
        )

    def create_area_chart(
        self,
        chart_name=None,
        title=None,
        subtitle=None,
        data_name=None,
        unit=None,
        zero=False,
        libs=True,
        labels=True,
        legend=True,
    ):
        """Creates a JavaScript area chart using "HighCharts".
        @Params
        chart_name - If creating multiple charts,
                     use this to select which one.
        title - The title displayed for the chart.
        subtitle - The subtitle displayed for the chart.
        data_name - The series name. Useful for multi-series charts.
                    If no data_name, will default to using "Series 1".
        unit - The description label given to the chart's y-axis values.
        zero - If True, the y-axis always starts at 0. (Default: False).
        libs - The option to include Chart libraries (JS and CSS files).
               Should be set to True (default) for the first time creating
               a chart on a web page. If creating multiple charts on the
               same web page, you won't need to re-import the libraries
               when creating additional charts.
        labels - If True, displays labels on the chart for data points.
        legend - If True, displays the data point legend on the chart.
        """
        if not chart_name:
            chart_name = "default"
        if not data_name:
            data_name = ""
        style = "area"
        self.__create_highchart(
            chart_name=chart_name,
            title=title,
            subtitle=subtitle,
            style=style,
            data_name=data_name,
            unit=unit,
            zero=zero,
            libs=libs,
            labels=labels,
            legend=legend,
        )

    def __create_highchart(
        self,
        chart_name=None,
        title=None,
        subtitle=None,
        style=None,
        data_name=None,
        unit=None,
        zero=False,
        libs=True,
        labels=True,
        legend=True,
    ):
        """Creates a JavaScript chart using the "HighCharts" library."""
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
        if labels:
            labels = "true"
        else:
            labels = "false"
        if legend:
            legend = "true"
        else:
            legend = "false"
        title = title.replace("'", "\\'")
        subtitle = subtitle.replace("'", "\\'")
        unit = unit.replace("'", "\\'")
        self._chart_count += 1
        # If chart_libs format is changed, also change: save_presentation()
        chart_libs = """
            <script src="%s"></script>
            <script src="%s"></script>
            <script src="%s"></script>
            <script src="%s"></script>
            """ % (
            constants.HighCharts.HC_JS,
            constants.HighCharts.EXPORTING_JS,
            constants.HighCharts.EXPORT_DATA_JS,
            constants.HighCharts.ACCESSIBILITY_JS,
        )
        if not libs:
            chart_libs = ""
        chart_css = """
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
            """
        if not libs:
            chart_css = ""
        chart_description = ""
        chart_figure = """
            <figure class="highcharts-figure">
                <div id="chartcontainer_num_%s"></div>
                <p class="highcharts-description">%s</p>
            </figure>
            """ % (
            self._chart_count,
            chart_description,
        )
        min_zero = ""
        if zero:
            min_zero = "min: 0,"
        chart_init_1 = """
            <script>
            // Build the chart
            Highcharts.chart('chartcontainer_num_%s', {
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
            """ % (
            self._chart_count,
            title,
            subtitle,
            min_zero,
            unit,
            style,
        )
        #  "{series.name}:"
        point_format = (
            r"<b>{point.y}</b><br />" r"<b>{point.percentage:.1f}%</b>"
        )
        if style != "pie":
            point_format = r"<b>{point.y}</b>"
        chart_init_2 = (
            """
            tooltip: {
                enabled: true,
                useHTML: true,
                style: {
                    padding: '6px',
                    fontSize: '14px'
                },
                backgroundColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, 'rgba(255, 255, 255, 0.78)'],
                        [0.5, 'rgba(235, 235, 235, 0.76)'],
                        [1, 'rgba(244, 252, 255, 0.74)']
                    ]
                },
                hideDelay: 40,
                pointFormat: '%s'
            },
            """
            % point_format
        )
        chart_init_3 = """
            accessibility: {
                point: {
                    valueSuffix: '%%'
                }
            },
            plotOptions: {
                series: {
                    states: {
                        inactive: {
                            opacity: 0.85
                        }
                    }
                },
                pie: {
                    size: "95%%",
                    allowPointSelect: true,
                    animation: false,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: %s,
                        formatter: function() {
                          if (this.y > 0) {
                            return this.point.name + ': ' + this.point.y
                          }
                        }
                    },
                    states: {
                        hover: {
                            enabled: true
                        }
                    },
                    showInLegend: %s
                }
            },
            """ % (
            labels,
            legend,
        )
        if style != "pie":
            chart_init_3 = """
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
                        dataLabels: {
                            enabled: %s
                        },
                        showInLegend: %s,
                        animation: false,
                        shadow: false,
                        lineWidth: 3,
                        fillOpacity: 0.5,
                        marker: {
                            enabled: true
                        }
                    }
                },
                """ % (
                labels,
                legend,
            )
        chart_init = chart_init_1 + chart_init_2 + chart_init_3
        color_by_point = "true"
        if style != "pie":
            color_by_point = "false"
        series = """
            series: [{
            name: '%s',
            colorByPoint: %s,
            data: [
            """ % (
            data_name,
            color_by_point,
        )
        new_chart = chart_libs + chart_css + chart_figure + chart_init + series
        new_chart = textwrap.dedent(new_chart)
        self._chart_data[chart_name] = []
        self._chart_label[chart_name] = []
        self._chart_data[chart_name].append(new_chart)
        self._chart_first_series[chart_name] = True
        self._chart_series_count[chart_name] = 1

    def add_series_to_chart(self, data_name=None, chart_name=None):
        """Add a new data series to an existing chart.
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
            """
            % data_name
        )
        self._chart_data[chart_name].append(series)
        self._chart_first_series[chart_name] = False

    def add_data_point(self, label, value, color=None, chart_name=None):
        """Add a data point to a SeleniumBase-generated chart.
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
        data_point = """
            {
            name: '%s',
            y: %s,
            color: '%s'
            },
            """ % (
            label,
            value,
            color,
        )
        data_point = textwrap.dedent(data_point)
        self._chart_data[chart_name].append(data_point)
        if self._chart_first_series[chart_name]:
            self._chart_label[chart_name].append(label)

    def save_chart(self, chart_name=None, filename=None, folder=None):
        """Saves a SeleniumBase-generated chart to a file for later use.
        @Params
        chart_name - If creating multiple charts at the same time,
                     use this to select the one you wish to use.
        filename - The name of the HTML file that you wish to
                   save the chart to. (filename must end in ".html")
        folder - The name of the folder where you wish to
                 save the HTML file. (Default: "./saved_charts/")
        """
        if not chart_name:
            chart_name = "default"
        if not filename:
            filename = "my_chart.html"
        if chart_name not in self._chart_data:
            raise Exception("Chart {%s} does not exist!" % chart_name)
        if not filename.endswith(".html"):
            raise Exception('Chart file must end in ".html"!')
        the_html = '<meta charset="utf-8">\n'
        the_html += '<meta http-equiv="Content-Type" content="text/html">\n'
        the_html += '<meta name="viewport" content="shrink-to-fit=no">\n'
        for chart_data_point in self._chart_data[chart_name]:
            the_html += chart_data_point
        the_html += """
            ]
                }]
            });
            </script>
            """
        axis = "xAxis: {\n"
        axis += "    labels: {\n"
        axis += "        useHTML: true,\n"
        axis += "        style: {\n"
        axis += "            fontSize: '14px',\n"
        axis += "        },\n"
        axis += "    },\n"
        axis += "categories: ["
        for label in self._chart_label[chart_name]:
            axis += "'%s'," % label
        axis += "], crosshair: false},"
        the_html = the_html.replace("xAxis: { },", axis)
        if not folder:
            saved_charts_folder = constants.Charts.SAVED_FOLDER
        else:
            saved_charts_folder = folder
        if saved_charts_folder.endswith("/"):
            saved_charts_folder = saved_charts_folder[:-1]
        if not os.path.exists(saved_charts_folder):
            try:
                os.makedirs(saved_charts_folder)
            except Exception:
                pass
        file_path = os.path.join(saved_charts_folder, filename)
        out_file = codecs.open(file_path, "w+", encoding="utf-8")
        out_file.writelines(the_html)
        out_file.close()
        print("\n>>> [%s] was saved!" % file_path)
        return file_path

    def display_chart(self, chart_name=None, filename=None, interval=0):
        """Displays a SeleniumBase-generated chart in the browser window.
        @Params
        chart_name - If creating multiple charts at the same time,
                     use this to select the one you wish to use.
        filename - The name of the HTML file that you wish to
                   save the chart to. (filename must end in ".html")
        interval - The delay time for auto-advancing charts. (in seconds)
                   If set to 0 (default), auto-advancing is disabled.
        """
        if self.headless or self.headless2 or self.xvfb:
            interval = 1  # Race through chart if running in headless mode
        if not chart_name:
            chart_name = "default"
        if not filename:
            filename = "my_chart.html"
        if not interval:
            interval = 0
        if interval == 0 and self.interval:
            interval = float(self.interval)
        if not type(interval) is int and not type(interval) is float:
            raise Exception('Expecting a numeric value for "interval"!')
        if interval < 0:
            raise Exception('The "interval" cannot be a negative number!')
        if chart_name not in self._chart_data:
            raise Exception("Chart {%s} does not exist!" % chart_name)
        if not filename.endswith(".html"):
            raise Exception('Chart file must end in ".html"!')
        file_path = self.save_chart(chart_name=chart_name, filename=filename)
        self.open_html_file(file_path)
        chart_folder = constants.Charts.SAVED_FOLDER
        if interval == 0:
            try:
                print("\n*** Close the browser window to continue ***")
                # Will also continue if manually navigating to a new page
                while len(self.driver.window_handles) > 0 and (
                    chart_folder in self.get_current_url()
                ):
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
        """Extracts the HTML from a SeleniumBase-generated chart.
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
        the_html += """
            ]
                }]
            });
            </script>
            """
        axis = "xAxis: {\n"
        axis += "    labels: {\n"
        axis += "        useHTML: true,\n"
        axis += "        style: {\n"
        axis += "            fontSize: '14px',\n"
        axis += "        },\n"
        axis += "    },\n"
        axis += "categories: ["
        for label in self._chart_label[chart_name]:
            axis += "'%s'," % label
        axis += "], crosshair: false},"
        the_html = the_html.replace("xAxis: { },", axis)
        self._chart_xcount += 1
        the_html = the_html.replace(
            "chartcontainer_num_", "chartcontainer_%s_" % self._chart_xcount
        )
        return the_html

    ############

    def create_tour(self, name=None, theme=None):
        """Creates a guided tour for any website.
        The default theme is the IntroJS Library.
        @Params
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        theme - Sets the default theme for the website tour. Available themes:
                "Bootstrap", "DriverJS", "Hopscotch", "IntroJS", "Shepherd".
                The "Shepherd" library also contains multiple variation themes:
                "light"/"arrows", "dark", "default", "square", "square-dark".
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
            elif theme.lower() == "arrows":
                self.create_shepherd_tour(name, theme="light")
            elif theme.lower() == "dark":
                self.create_shepherd_tour(name, theme="dark")
            elif theme.lower() == "square":
                self.create_shepherd_tour(name, theme="square")
            elif theme.lower() == "square-dark":
                self.create_shepherd_tour(name, theme="square-dark")
            elif theme.lower() == "default":
                self.create_shepherd_tour(name, theme="default")
            else:
                self.create_introjs_tour(name)
        else:
            self.create_introjs_tour(name)

    def create_shepherd_tour(self, name=None, theme=None):
        """Creates a Shepherd JS website tour.
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
            """
            % shepherd_theme
        )
        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_bootstrap_tour(self, name=None):
        """Creates a Bootstrap tour for a website.
        @Params
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = """
            // Bootstrap Tour
            var tour = new Tour({
            container: 'body',
            animation: true,
            keyboard: true,
            orphan: true,
            smartPlacement: true,
            autoscroll: true,
            backdrop: true,
            backdropContainer: 'body',
            backdropPadding: 3,
            });
            tour.addSteps([
            """

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_driverjs_tour(self, name=None):
        """Creates a DriverJS tour for a website.
        @Params
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = """
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
            """

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_hopscotch_tour(self, name=None):
        """Creates a Hopscotch tour for a website.
        @Params
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        """
        if not name:
            name = "default"

        new_tour = """
            // Hopscotch Tour
            var tour = {
            id: "hopscotch_tour",
            steps: [
            """

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def create_introjs_tour(self, name=None):
        """Creates an IntroJS tour for a website.
        @Params
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        """
        if not hasattr(sb_config, "introjs_theme_color"):
            sb_config.introjs_theme_color = constants.TourColor.theme_color
        if not hasattr(sb_config, "introjs_hover_color"):
            sb_config.introjs_hover_color = constants.TourColor.hover_color
        if not name:
            name = "default"

        new_tour = """
            // IntroJS Tour
            function startIntro(){
            var intro = introJs();
            intro.setOptions({
            steps: [
            """

        self._tour_steps[name] = []
        self._tour_steps[name].append(new_tour)

    def set_introjs_colors(self, theme_color=None, hover_color=None):
        """Use this method to set the theme colors for IntroJS tours.
        Args must be hex color values that start with a "#" sign.
        If a color isn't specified, the color will reset to the default.
        The border color of buttons is set to the hover color.
        @Params
        theme_color - The color of buttons.
        hover_color - The color of buttons after hovering over them.
        """
        if not hasattr(sb_config, "introjs_theme_color"):
            sb_config.introjs_theme_color = constants.TourColor.theme_color
        if not hasattr(sb_config, "introjs_hover_color"):
            sb_config.introjs_hover_color = constants.TourColor.hover_color
        if theme_color:
            match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", theme_color)
            if not match:
                raise Exception(
                    'Expecting a hex value color that starts with "#"!'
                )
            sb_config.introjs_theme_color = theme_color
        else:
            sb_config.introjs_theme_color = constants.TourColor.theme_color
        if hover_color:
            match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", hover_color)
            if not match:
                raise Exception(
                    'Expecting a hex value color that starts with "#"!'
                )
            sb_config.introjs_hover_color = hover_color
        else:
            sb_config.introjs_hover_color = constants.TourColor.hover_color

    def add_tour_step(
        self,
        message,
        selector=None,
        name=None,
        title=None,
        theme=None,
        alignment=None,
        duration=None,
    ):
        """Allows the user to add tour steps for a website.
        @Params
        message - The message to display.
        selector - The CSS Selector of the Element to attach to.
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        title - Additional header text that appears above the message.
        theme - (Shepherd Tours ONLY) The styling of the tour step.
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

        if not alignment or alignment not in [
            "top",
            "bottom",
            "left",
            "right",
        ]:
            t_name = self._tour_steps[name][0]
            if "Hopscotch" not in t_name and "DriverJS" not in t_name:
                alignment = "top"
            else:
                alignment = "bottom"

        if "Bootstrap" in self._tour_steps[name][0]:
            self.__add_bootstrap_tour_step(
                message,
                selector=selector,
                name=name,
                title=title,
                alignment=alignment,
                duration=duration,
            )
        elif "DriverJS" in self._tour_steps[name][0]:
            self.__add_driverjs_tour_step(
                message,
                selector=selector,
                name=name,
                title=title,
                alignment=alignment,
            )
        elif "Hopscotch" in self._tour_steps[name][0]:
            self.__add_hopscotch_tour_step(
                message,
                selector=selector,
                name=name,
                title=title,
                alignment=alignment,
            )
        elif "IntroJS" in self._tour_steps[name][0]:
            self.__add_introjs_tour_step(
                message,
                selector=selector,
                name=name,
                title=title,
                alignment=alignment,
            )
        else:
            self.__add_shepherd_tour_step(
                message,
                selector=selector,
                name=name,
                title=title,
                theme=theme,
                alignment=alignment,
            )

    def __add_shepherd_tour_step(
        self,
        message,
        selector=None,
        name=None,
        title=None,
        theme=None,
        alignment=None,
    ):
        """Allows the user to add tour steps for a website.
        @Params
        message - The message to display.
        selector - The CSS Selector of the Element to attach to.
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        title - Additional header text that appears above the message.
        theme - (Shepherd Tours ONLY) The styling of the tour step.
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
                self._tour_steps[name][0],
            ).group(1)
            shepherd_theme = shepherd_base_theme

        shepherd_classes = shepherd_theme
        if selector == "html":
            shepherd_classes += " shepherd-orphan"
        buttons = "firstStepButtons"
        if len(self._tour_steps[name]) > 1:
            buttons = "midTourButtons"

        step = """tour.addStep('%s', {
                    title: '%s',
                    classes: '%s',
                    text: '%s',
                    attachTo: {element: '%s', on: '%s'},
                    buttons: %s,
                    advanceOn: '.docs-link click'
                });""" % (
            name,
            title,
            shepherd_classes,
            message,
            selector,
            alignment,
            buttons,
        )

        self._tour_steps[name].append(step)

    def __add_bootstrap_tour_step(
        self,
        message,
        selector=None,
        name=None,
        title=None,
        alignment=None,
        duration=None,
    ):
        """Allows the user to add tour steps for a website.
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

        bd = "backdrop: true,"
        if selector == "html":
            bd = "backdrop: false,"

        step = """{
                %s
                title: '%s',
                content: '%s',
                orphan: true,
                autoscroll: true,
                %s
                placement: '%s',
                smartPlacement: true,
                duration: %s,
                },""" % (
            element_row,
            title,
            message,
            bd,
            alignment,
            duration,
        )

        self._tour_steps[name].append(step)

    def __add_driverjs_tour_step(
        self, message, selector=None, name=None, title=None, alignment=None
    ):
        """Allows the user to add tour steps for a website.
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
            '<font size="3" color="#33477B"><b>' + message + "</b></font>"
        )
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

        step = """{
                %s
                %s
                popover: {
                  className: 'popover-class',
                  %s
                  %s
                  %s
                }
                },""" % (
            element_row,
            ani_row,
            title_row,
            desc_row,
            align_row,
        )

        self._tour_steps[name].append(step)

    def __add_hopscotch_tour_step(
        self, message, selector=None, name=None, title=None, alignment=None
    ):
        """Allows the user to add tour steps for a website.
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

        step = """{
                target: '%s',
                title: '%s',
                content: '%s',
                %s
                showPrevButton: 'true',
                scrollDuration: '550',
                placement: '%s'},
                """ % (
            selector,
            title,
            message,
            arrow_offset_row,
            alignment,
        )

        self._tour_steps[name].append(step)

    def __add_introjs_tour_step(
        self, message, selector=None, name=None, title=None, alignment=None
    ):
        """Allows the user to add tour steps for a website.
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

        message = '<font size="3" color="#33477B">' + message + "</font>"

        step = """{%s
            intro: '%s',
            position: '%s'},""" % (
            element_row,
            message,
            alignment,
        )

        self._tour_steps[name].append(step)

    def play_tour(self, name=None, interval=0):
        """Plays a tour on the current website.
        @Params
        name - If creating multiple tours at the same time,
               use this to select the tour you wish to add steps to.
        interval - The delay time between autoplaying tour steps. (Seconds)
                   If set to 0 (default), the tour is fully manual control.
        """
        from seleniumbase.core import tour_helper

        if self.headless or self.headless2 or self.xvfb:
            return  # Tours should not run in headless mode.

        self.wait_for_ready_state_complete()

        if not interval:
            interval = 0
        if interval == 0 and self.interval:
            interval = float(self.interval)

        if not name:
            name = "default"
        if name not in self._tour_steps:
            raise Exception("Tour {%s} does not exist!" % name)

        if "Bootstrap" in self._tour_steps[name][0]:
            tour_helper.play_bootstrap_tour(
                self.driver,
                self._tour_steps,
                self.browser,
                self.message_duration,
                name=name,
                interval=interval,
            )
        elif "DriverJS" in self._tour_steps[name][0]:
            tour_helper.play_driverjs_tour(
                self.driver,
                self._tour_steps,
                self.browser,
                self.message_duration,
                name=name,
                interval=interval,
            )
        elif "Hopscotch" in self._tour_steps[name][0]:
            tour_helper.play_hopscotch_tour(
                self.driver,
                self._tour_steps,
                self.browser,
                self.message_duration,
                name=name,
                interval=interval,
            )
        elif "IntroJS" in self._tour_steps[name][0]:
            tour_helper.play_introjs_tour(
                self.driver,
                self._tour_steps,
                self.browser,
                self.message_duration,
                name=name,
                interval=interval,
            )
        else:
            tour_helper.play_shepherd_tour(
                self.driver,
                self._tour_steps,
                self.message_duration,
                name=name,
                interval=interval,
            )

    def start_tour(self, name=None, interval=0):
        """Same as self.play_tour()"""
        self.play_tour(name=name, interval=interval)

    def export_tour(self, name=None, filename="my_tour.js", url=None):
        """Exports a tour as a JS file.
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
              of the current page will be used.
        """
        from seleniumbase.core import tour_helper

        if not url:
            url = self.get_current_url()
        tour_helper.export_tour(
            self._tour_steps, name=name, filename=filename, url=url
        )

    ############

    def activate_jquery_confirm(self):
        """See https://craftpip.github.io/jquery-confirm/ for usage."""
        self.__check_scope()
        self.__check_browser()
        js_utils.activate_jquery_confirm(self.driver)
        self.wait_for_ready_state_complete()

    def set_jqc_theme(self, theme, color=None, width=None):
        """Sets the default jquery-confirm theme and width (optional).
        Available themes: "bootstrap", "modern", "material", "supervan",
                          "light", "dark", and "seamless".
        Available colors: (This sets the BORDER color, NOT the button color.)
            "blue", "default", "green", "red", "purple", "orange", "dark".
        Width can be set using percent or pixels. Eg: "36.0%", "450px".
        """
        if not self.__changed_jqc_theme:
            self.__jqc_default_theme = constants.JqueryConfirm.DEFAULT_THEME
            self.__jqc_default_color = constants.JqueryConfirm.DEFAULT_COLOR
            self.__jqc_default_width = constants.JqueryConfirm.DEFAULT_WIDTH
        valid_themes = [
            "bootstrap",
            "modern",
            "material",
            "supervan",
            "light",
            "dark",
            "seamless",
        ]
        if theme.lower() not in valid_themes:
            raise Exception(
                "%s is not a valid jquery-confirm theme! "
                "Select from %s" % (theme.lower(), valid_themes)
            )
        constants.JqueryConfirm.DEFAULT_THEME = theme.lower()
        if color:
            valid_colors = [
                "blue",
                "default",
                "green",
                "red",
                "purple",
                "orange",
                "dark",
            ]
            if color.lower() not in valid_colors:
                raise Exception(
                    "%s is not a valid jquery-confirm border color! "
                    "Select from %s" % (color.lower(), valid_colors)
                )
            constants.JqueryConfirm.DEFAULT_COLOR = color.lower()
        if width:
            if type(width) is int or type(width) is float:
                # Convert to a string if a number is given
                width = str(width)
            if width.isnumeric():
                if int(width) <= 0:
                    raise Exception("Width must be set to a positive number!")
                elif int(width) <= 100:
                    width = str(width) + "%"
                else:
                    width = str(width) + "px"  # Use pixels if width is > 100
            if not width.endswith("%") and not width.endswith("px"):
                raise Exception(
                    "jqc width must end with %% for percent or px for pixels!"
                )
            value = None
            if width.endswith("%"):
                value = width[:-1]
            if width.endswith("px"):
                value = width[:-2]
            try:
                value = float(value)
            except Exception:
                raise Exception("%s is not a numeric value!" % value)
            if value <= 0:
                raise Exception("%s is not a positive number!" % value)
            constants.JqueryConfirm.DEFAULT_WIDTH = width

    def reset_jqc_theme(self):
        """Resets the jqc theme settings to factory defaults."""
        if self.__changed_jqc_theme:
            constants.JqueryConfirm.DEFAULT_THEME = self.__jqc_default_theme
            constants.JqueryConfirm.DEFAULT_COLOR = self.__jqc_default_color
            constants.JqueryConfirm.DEFAULT_WIDTH = self.__jqc_default_width
            self.__changed_jqc_theme = False

    def get_jqc_button_input(self, message, buttons, options=None):
        """
        Pop up a jquery-confirm box and return the text of the button clicked.
        If running in headless mode, the last button text is returned.
        @Params
        message: The message to display in the jquery-confirm dialog.
        buttons: A list of tuples for text and color.
            Example: [("Yes!", "green"), ("No!", "red")]
            Available colors: blue, green, red, orange, purple, default, dark.
            A simple text string also works: "My Button". (Uses default color.)
        options: A list of tuples for options to set.
            Example: [("theme", "bootstrap"), ("width", "450px")]
            Available theme options: bootstrap, modern, material, supervan,
                                     light, dark, and seamless.
            Available colors: (For the BORDER color, NOT the button color.)
                "blue", "default", "green", "red", "purple", "orange", "dark".
            Example option for changing the border color: ("color", "default")
            Width can be set using percent or pixels. Eg: "36.0%", "450px".
        """
        from seleniumbase.core import jqc_helper

        if message and type(message) is not str:
            raise Exception('Expecting a string for arg: "message"!')
        if not type(buttons) is list and not type(buttons) is tuple:
            raise Exception('Expecting a list or tuple for arg: "button"!')
        if len(buttons) < 1:
            raise Exception('List "buttons" requires at least one button!')
        new_buttons = []
        for button in buttons:
            if (
                (type(button) is list or type(button) is tuple)
                and (len(button) == 1)
            ):
                new_buttons.append(button[0])
            elif (
                (type(button) is list or type(button) is tuple)
                and (len(button) > 1)
            ):
                new_buttons.append((button[0], str(button[1]).lower()))
            else:
                new_buttons.append((str(button), ""))
        buttons = new_buttons
        if options:
            for option in options:
                if not type(option) is list and not type(option) is tuple:
                    raise Exception('"options" should be a list of tuples!')
        if self.headless or self.headless2 or self.xvfb:
            return buttons[-1][0]
        jqc_helper.jquery_confirm_button_dialog(
            self.driver, message, buttons, options
        )
        time.sleep(0.02)
        jf = "document.querySelector('.jconfirm-box').focus();"
        try:
            self.execute_script(jf)
        except Exception:
            pass
        waiting_for_response = True
        while waiting_for_response:
            time.sleep(0.05)
            jqc_open = self.execute_script("return jconfirm.instances.length;")
            if str(jqc_open) == "0":
                break
        time.sleep(0.1)
        status = None
        try:
            status = self.execute_script("return $jqc_status;")
        except Exception:
            status = self.execute_script("return jconfirm.lastButtonText;")
        return status

    def get_jqc_text_input(self, message, button=None, options=None):
        """
        Pop up a jquery-confirm box and return the text submitted by the input.
        If running in headless mode, the text returned is "" by default.
        @Params
        message: The message to display in the jquery-confirm dialog.
        button: A 2-item list or tuple for text and color. Or just the text.
            Example: ["Submit", "blue"] -> (default button if not specified)
            Available colors: blue, green, red, orange, purple, default, dark.
            A simple text string also works: "My Button". (Uses default color.)
        options: A list of tuples for options to set.
            Example: [("theme", "bootstrap"), ("width", "450px")]
            Available theme options: bootstrap, modern, material, supervan,
                                     light, dark, and seamless.
            Available colors: (For the BORDER color, NOT the button color.)
                "blue", "default", "green", "red", "purple", "orange", "dark".
            Example option for changing the border color: ("color", "default")
            Width can be set using percent or pixels. Eg: "36.0%", "450px".
        """
        from seleniumbase.core import jqc_helper

        if message and type(message) is not str:
            raise Exception('Expecting a string for arg: "message"!')
        if button:
            if (
                (type(button) is list or type(button) is tuple)
                and (len(button) == 1)
            ):
                button = (str(button[0]), "")
            elif (
                (type(button) is list or type(button) is tuple)
                and (len(button) > 1)
            ):
                valid_colors = [
                    "blue",
                    "default",
                    "green",
                    "red",
                    "purple",
                    "orange",
                    "dark",
                ]
                detected_color = str(button[1]).lower()
                if str(button[1]).lower() not in valid_colors:
                    raise Exception(
                        "%s is an invalid jquery-confirm button color!\n"
                        "Select from %s" % (detected_color, valid_colors)
                    )
                button = (str(button[0]), str(button[1]).lower())
            else:
                button = (str(button), "")
        else:
            button = ("Submit", "blue")

        if options:
            for option in options:
                if not type(option) is list and not type(option) is tuple:
                    raise Exception('"options" should be a list of tuples!')
        if self.headless or self.headless2 or self.xvfb:
            return ""
        jqc_helper.jquery_confirm_text_dialog(
            self.driver, message, button, options
        )
        time.sleep(0.02)
        jf = "document.querySelector('.jconfirm-box input.jqc_input').focus();"
        try:
            self.execute_script(jf)
        except Exception:
            pass
        waiting_for_response = True
        while waiting_for_response:
            time.sleep(0.05)
            jqc_open = self.execute_script("return jconfirm.instances.length;")
            if str(jqc_open) == "0":
                break
        time.sleep(0.1)
        status = None
        try:
            status = self.execute_script("return $jqc_input;")
        except Exception:
            status = self.execute_script("return jconfirm.lastInputText;")
        return status

    def get_jqc_form_inputs(self, message, buttons, options=None):
        """
        Pop up a jquery-confirm box and return the input/button texts as tuple.
        If running in headless mode, returns the ("", buttons[-1][0]) tuple.
        @Params
        message: The message to display in the jquery-confirm dialog.
        buttons: A list of tuples for text and color.
            Example: [("Yes!", "green"), ("No!", "red")]
            Available colors: blue, green, red, orange, purple, default, dark.
            A simple text string also works: "My Button". (Uses default color.)
        options: A list of tuples for options to set.
            Example: [("theme", "bootstrap"), ("width", "450px")]
            Available theme options: bootstrap, modern, material, supervan,
                                     light, dark, and seamless.
            Available colors: (For the BORDER color, NOT the button color.)
                "blue", "default", "green", "red", "purple", "orange", "dark".
            Example option for changing the border color: ("color", "default")
            Width can be set using percent or pixels. Eg: "36.0%", "450px".
        """
        from seleniumbase.core import jqc_helper

        if message and type(message) is not str:
            raise Exception('Expecting a string for arg: "message"!')
        if not type(buttons) is list and not type(buttons) is tuple:
            raise Exception('Expecting a list or tuple for arg: "button"!')
        if len(buttons) < 1:
            raise Exception('List "buttons" requires at least one button!')
        new_buttons = []
        for button in buttons:
            if (
                (type(button) is list or type(button) is tuple)
                and (len(button) == 1)
            ):
                new_buttons.append(button[0])
            elif (
                (type(button) is list or type(button) is tuple)
                and (len(button) > 1)
            ):
                new_buttons.append((button[0], str(button[1]).lower()))
            else:
                new_buttons.append((str(button), ""))
        buttons = new_buttons
        if options:
            for option in options:
                if not type(option) is list and not type(option) is tuple:
                    raise Exception('"options" should be a list of tuples!')
        if self.headless or self.headless2 or self.xvfb:
            return ("", buttons[-1][0])
        jqc_helper.jquery_confirm_full_dialog(
            self.driver, message, buttons, options
        )
        time.sleep(0.02)
        jf = "document.querySelector('.jconfirm-box input.jqc_input').focus();"
        try:
            self.execute_script(jf)
        except Exception:
            pass
        waiting_for_response = True
        while waiting_for_response:
            time.sleep(0.05)
            jqc_open = self.execute_script("return jconfirm.instances.length;")
            if str(jqc_open) == "0":
                break
        time.sleep(0.1)
        text_status = None
        button_status = None
        try:
            text_status = self.execute_script("return $jqc_input;")
            button_status = self.execute_script("return $jqc_status;")
        except Exception:
            text_status = self.execute_script("return jconfirm.lastInputText;")
            button_status = self.execute_script(
                "return jconfirm.lastButtonText;"
            )
        return (text_status, button_status)

    ############

    def __are_quotes_escaped(self, string):
        return js_utils.are_quotes_escaped(string)

    def __escape_quotes_if_needed(self, string):
        return js_utils.escape_quotes_if_needed(string)

    def __is_in_frame(self):
        return js_utils.is_in_frame(self.driver)

    ############

    def __js_click(self, selector, by="css selector"):
        """Clicks an element using pure JS. Does not use jQuery."""
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        is_visible = self.is_element_visible(selector, by=by)
        current_url = self.get_current_url()
        script = (
            """var simulateClick = function (elem) {
                   var evt = new MouseEvent('click', {
                       bubbles: true,
                       cancelable: true,
                       view: window
                   });
                   var canceled = !elem.dispatchEvent(evt);
               };
               var someLink = document.querySelector('%s');
               simulateClick(someLink);"""
            % css_selector
        )
        try:
            self.execute_script(script)
        except Exception as e:
            # If element was visible but no longer, or on a different page now,
            # assume that the click actually worked and continue with the test.
            if (
                (is_visible and not self.is_element_visible(selector, by=by))
                or current_url != self.get_current_url()
            ):
                return  # The click worked, but threw an Exception. Keep going.
            # It appears the first click didn't work. Make another attempt.
            self.wait_for_ready_state_complete()
            if "Cannot read properties of null" in e.msg:
                page_actions.wait_for_element_present(
                    self.driver, selector, by, timeout=5
                )
                if not page_actions.is_element_clickable(
                    self.driver, selector, by
                ):
                    try:
                        self.wait_for_element_clickable(
                            selector, by, timeout=1.2
                        )
                    except Exception:
                        pass
            # If the regular mouse-simulated click fails, do a basic JS click
            script = (
                """document.querySelector('%s').click();"""
                % css_selector
            )
            self.execute_script(script)

    def __js_click_all(self, selector, by="css selector"):
        """Clicks all matching elements using pure JS. (No jQuery)"""
        selector, by = self.__recalculate_selector(selector, by)
        css_selector = self.convert_to_css_selector(selector, by=by)
        css_selector = re.escape(css_selector)  # Add "\\" to special chars
        css_selector = self.__escape_quotes_if_needed(css_selector)
        script = (
            """var simulateClick = function (elem) {
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
            % css_selector
        )
        self.execute_script(script)

    def __click_with_offset(
        self,
        selector,
        x,
        y,
        by="css selector",
        double=False,
        mark=None,
        timeout=None,
        center=None,
    ):
        from selenium.webdriver.common.action_chains import ActionChains

        self.wait_for_ready_state_complete()
        if self.__needs_minimum_wait():
            time.sleep(0.05)  # Force a minimum wait, even if skipping waits.
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        selector, by = self.__recalculate_selector(selector, by)
        element = page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout
        )
        if self.demo_mode:
            self.highlight(selector, by=by, loops=1)
        elif self.slow_mode:
            self.__slow_scroll_to_element(element)
        else:
            self.__scroll_to_element(element, selector, by)
        self.wait_for_ready_state_complete()
        if self.demo_mode and mark is None:
            mark = True
        if mark:
            selector = self.convert_to_css_selector(selector, by=by)
            selector = re.escape(selector)
            selector = self.__escape_quotes_if_needed(selector)
            m_x = x
            m_y = y
            if center:
                element_rect = element.rect
                left_offset = element_rect["width"] / 2
                top_offset = element_rect["height"] / 2
                m_x = left_offset + (m_x or 0)
                m_y = top_offset + (m_y or 0)
            px = m_x - 3
            py = m_y - 3
            script = (
                "var canvas = document.querySelector('%s');"
                "var ctx = canvas.getContext('2d');"
                "ctx.fillStyle = '#F8F808';"
                "ctx.fillRect(%s, %s, 7, 7);"
                "ctx.fillStyle = '#F80808';"
                "ctx.fillRect(%s+1, %s+1, 5, 5);" % (selector, px, py, px, py)
            )
            self.execute_script(script)
        try:
            element_location = element.location["y"]
            element_location = element_location - constants.Scroll.Y_OFFSET + y
            if element_location < 0:
                element_location = 0
            scroll_script = "window.scrollTo(0, %s);" % element_location
            self.driver.execute_script(scroll_script)
            time.sleep(0.1)
        except Exception:
            time.sleep(0.05)
        if self.__needs_minimum_wait():
            time.sleep(0.05)
        try:
            if selenium4_or_newer and not center:
                element_rect = element.rect
                left_offset = element_rect["width"] / 2
                top_offset = element_rect["height"] / 2
                x = -left_offset + (x or 0)
                y = -top_offset + (y or 0)
            elif selenium4_or_newer and center:
                pass
            elif not selenium4_or_newer and not center:
                pass
            else:
                # not selenium4_or_newer and center:
                element_rect = element.rect
                left_offset = element_rect["width"] / 2
                top_offset = element_rect["height"] / 2
                x = left_offset + x
                y = top_offset + y
            action_chains = ActionChains(self.driver)
            action_chains.move_to_element_with_offset(element, x, y)
            if not double:
                action_chains.click().perform()
            else:
                action_chains.double_click().perform()
        except MoveTargetOutOfBoundsException:
            message = (
                "Target coordinates for click are out-of-bounds!\n"
                "The offset must stay inside the target element!"
            )
            raise Exception(message)
        except InvalidArgumentException as e:
            if not self.browser == "chrome":
                raise Exception(e)
            driver_capabilities = self.driver.capabilities
            if "version" in driver_capabilities:
                chrome_version = driver_capabilities["version"]
            else:
                chrome_version = driver_capabilities["browserVersion"]
            major_chrome_version = chrome_version.split(".")[0]
            chrome_dict = self.driver.capabilities["chrome"]
            chromedriver_version = chrome_dict["chromedriverVersion"]
            chromedriver_version = chromedriver_version.split(" ")[0]
            major_chromedriver_version = chromedriver_version.split(".")[0]
            if (
                int(major_chromedriver_version) >= 76
                and int(major_chrome_version) >= 76
            ):
                raise Exception(e)
            install_sb = (
                "seleniumbase get chromedriver %s" % major_chrome_version
            )
            if int(major_chromedriver_version) < int(major_chrome_version):
                # Upgrading the driver is needed for performing canvas actions
                message = (
                    "You need to upgrade to a newer\n"
                    "version of chromedriver to perform canvas actions!\n"
                    "Reason: github.com/SeleniumHQ/selenium/issues/7000"
                    "\nYour version of chromedriver is: %s\n"
                    "And your version of Chrome is: %s\n"
                    "You can fix this issue by running:\n>>> %s\n"
                    % (chromedriver_version, chrome_version, install_sb)
                )
                raise Exception(message)
            else:
                raise Exception(e)
        if self.demo_mode:
            self.__demo_mode_pause_if_active()
        elif self.slow_mode:
            self.__slow_mode_pause_if_active()

    def __jquery_slow_scroll_to(self, selector, by="css selector"):
        selector, by = self.__recalculate_selector(selector, by)
        element = self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        dist = js_utils.get_scroll_distance_to_element(self.driver, element)
        time_offset = 0
        try:
            if dist and abs(dist) > constants.Values.SSMD:
                time_offset = int(
                    float(abs(dist) - constants.Values.SSMD) / 12.5
                )
                if time_offset > 950:
                    time_offset = 950
        except Exception:
            time_offset = 0
        scroll_time_ms = 550 + time_offset
        sleep_time = 0.625 + (float(time_offset) / 1000.0)
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        scroll_script = (
            """jQuery([document.documentElement, document.body]).animate({"""
            """scrollTop: jQuery('%s').offset().top - %s}, %s);"""
            % (selector, constants.Scroll.Y_OFFSET, scroll_time_ms)
        )
        if js_utils.is_jquery_activated(self.driver):
            self.execute_script(scroll_script)
        else:
            self.__slow_scroll_to_element(element)
        time.sleep(sleep_time)

    def __jquery_click(self, selector, by="css selector"):
        """Clicks an element using jQuery. Different from using pure JS."""
        selector, by = self.__recalculate_selector(selector, by)
        self.wait_for_element_present(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        selector = self.convert_to_css_selector(selector, by=by)
        selector = self.__make_css_match_first_element_only(selector)
        click_script = """jQuery('%s')[0].click();""" % selector
        self.safe_execute_script(click_script)

    def __get_major_browser_version(self):
        try:
            version = self.driver.__dict__["caps"]["browserVersion"]
        except Exception:
            try:
                version = self.driver.__dict__["caps"]["version"]
            except Exception:
                version = str(self.driver.__dict__["capabilities"]["version"])
            self.driver.__dict__["caps"]["browserVersion"] = version
        major_browser_version = version.split(".")[0]
        return major_browser_version

    def __get_href_from_link_text(self, link_text, hard_fail=True):
        href = self.get_link_attribute(link_text, "href", hard_fail)
        if not href:
            return None
        if href.startswith("//"):
            link = "http:" + href
        elif href.startswith("/"):
            url = self.driver.current_url
            domain_url = self.get_domain_url(url)
            link = domain_url + href
        else:
            link = href
        return link

    def __click_dropdown_link_text(self, link_text, link_css):
        """When a link may be hidden under a dropdown menu, use this."""
        soup = self.get_beautiful_soup()
        drop_down_list = []
        for item in soup.select("li[class]"):
            drop_down_list.append(item)
        csstype = link_css.split("[")[1].split("=")[0]
        for item in drop_down_list:
            item_text_list = item.text.split("\n")
            if link_text in item_text_list and csstype in item.decode():
                dropdown_css = ""
                try:
                    for css_class in item["class"]:
                        dropdown_css += "."
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
                                    self.driver,
                                    dropdown,
                                )
                            except Exception:
                                # If hovering fails, driver is likely outdated
                                # Time to go directly to the hidden link text
                                self.open(
                                    self.__get_href_from_link_text(link_text)
                                )
                                return True
                            page_actions.hover_element_and_click(
                                self.driver,
                                dropdown,
                                link_text,
                                click_by="link text",
                                timeout=0.12,
                            )
                            return True
                        except Exception:
                            pass

        return False

    def __get_href_from_partial_link_text(self, link_text, hard_fail=True):
        href = self.get_partial_link_text_attribute(
            link_text, "href", hard_fail
        )
        if not href:
            return None
        if href.startswith("//"):
            link = "http:" + href
        elif href.startswith("/"):
            url = self.driver.current_url
            domain_url = self.get_domain_url(url)
            link = domain_url + href
        else:
            link = href
        return link

    def __click_dropdown_partial_link_text(self, link_text, link_css):
        """When a partial link may be hidden under a dropdown, use this."""
        soup = self.get_beautiful_soup()
        drop_down_list = []
        for item in soup.select("li[class]"):
            drop_down_list.append(item)
        csstype = link_css.split("[")[1].split("=")[0]
        for item in drop_down_list:
            item_text_list = item.text.split("\n")
            if link_text in item_text_list and csstype in item.decode():
                dropdown_css = ""
                try:
                    for css_class in item["class"]:
                        dropdown_css += "."
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
                                    self.driver, dropdown
                                )
                            except Exception:
                                # If hovering fails, driver is likely outdated
                                # Time to go directly to the hidden link text
                                self.open(
                                    self.__get_href_from_partial_link_text(
                                        link_text
                                    )
                                )
                                return True
                            page_actions.hover_element_and_click(
                                self.driver,
                                dropdown,
                                link_text,
                                click_by="link text",
                                timeout=0.12,
                            )
                            return True
                        except Exception:
                            pass
        return False

    def __recalculate_selector(self, selector, by, xp_ok=True):
        """Use autodetection to return the correct selector with "by" updated.
        If "xp_ok" is False, don't call convert_css_to_xpath(), which is
        used to make the ":contains()" selector valid outside of JS calls."""
        _type = type(selector)  # First make sure the selector is a string
        not_string = False
        if not python3:
            if _type is not str and _type is not unicode:  # noqa: F821
                not_string = True
        else:
            if _type is not str:
                not_string = True
        if not_string:
            msg = "Expecting a selector of type: \"<class 'str'>\" (string)!"
            raise Exception('Invalid selector type: "%s"\n%s' % (_type, msg))
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
        if xp_ok:
            if ":contains(" in selector and by == By.CSS_SELECTOR:
                selector = self.convert_css_to_xpath(selector)
                by = By.XPATH
        return (selector, by)

    def __looks_like_a_page_url(self, url):
        """Returns True if the url parameter looks like a URL. This method
        is slightly more lenient than page_utils.is_valid_url(url) due to
        possible typos when calling self.get(url), which will try to
        navigate to the page if a URL is detected, but will instead call
        self.get_element(URL_AS_A_SELECTOR) if the input in not a URL."""
        if (
            url.startswith("http:")
            or url.startswith("https:")
            or url.startswith("://")
            or url.startswith("chrome:")
            or url.startswith("about:")
            or url.startswith("data:")
            or url.startswith("file:")
            or url.startswith("edge:")
            or url.startswith("opera:")
            or url.startswith("view-source:")
        ):
            return True
        else:
            return False

    def __make_css_match_first_element_only(self, selector):
        # Only get the first match
        return page_utils.make_css_match_first_element_only(selector)

    def __switch_to_newest_window_if_not_blank(self):
        current_window = self.driver.current_window_handle
        try:
            self.switch_to_window(len(self.driver.window_handles) - 1)
            if self.get_current_url() == "about:blank":
                self.switch_to_window(current_window)
        except Exception:
            self.switch_to_window(current_window)

    def __needs_minimum_wait(self):
        if (
            self.page_load_strategy == "none"
            and hasattr(settings, "SKIP_JS_WAITS")
            and settings.SKIP_JS_WAITS
        ):
            return True
        else:
            return False

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
            time.sleep(0.08)
            selector, by = self.__recalculate_selector(selector, by)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=settings.SMALL_TIMEOUT
            )
            try:
                if self.browser != "safari":
                    scroll_distance = js_utils.get_scroll_distance_to_element(
                        self.driver, element
                    )
                    if abs(scroll_distance) > constants.Values.SSMD:
                        self.__jquery_slow_scroll_to(selector, by)
                    else:
                        self.__slow_scroll_to_element(element)
                else:
                    self.__jquery_slow_scroll_to(selector, by)
            except (StaleElementReferenceException, ENI_Exception):
                self.wait_for_ready_state_complete()
                time.sleep(0.12)
                element = self.wait_for_element_visible(
                    selector, by=by, timeout=settings.SMALL_TIMEOUT
                )
                self.__slow_scroll_to_element(element)
            time.sleep(0.12)

    def __scroll_to_element(self, element, selector=None, by="css selector"):
        success = js_utils.scroll_to_element(self.driver, element)
        if not success and selector:
            self.wait_for_ready_state_complete()
            element = page_actions.wait_for_element_visible(
                self.driver, selector, by, timeout=settings.SMALL_TIMEOUT
            )
        self.__demo_mode_pause_if_active(tiny=True)

    def __slow_scroll_to_element(self, element):
        try:
            js_utils.slow_scroll_to_element(self.driver, element, self.browser)
        except Exception:
            # Scroll to the element instantly if the slow scroll fails
            js_utils.scroll_to_element(self.driver, element)

    def __highlight_with_js(self, selector, loops, o_bs):
        self.wait_for_ready_state_complete()
        js_utils.highlight_with_js(self.driver, selector, loops, o_bs)

    def __highlight_with_jquery(self, selector, loops, o_bs):
        self.wait_for_ready_state_complete()
        js_utils.highlight_with_jquery(self.driver, selector, loops, o_bs)

    def __highlight_with_js_2(self, message, selector, o_bs):
        duration = self.message_duration
        if not duration:
            duration = settings.DEFAULT_MESSAGE_DURATION
        if (
            (self.headless or self.headless2 or self.xvfb)
            and float(duration) > 0.75
        ):
            duration = 0.75
        js_utils.highlight_with_js_2(
            self.driver, message, selector, o_bs, duration
        )

    def __highlight_with_jquery_2(self, message, selector, o_bs):
        duration = self.message_duration
        if not duration:
            duration = settings.DEFAULT_MESSAGE_DURATION
        if (
            (self.headless or self.headless2 or self.xvfb)
            and float(duration) > 0.75
        ):
            duration = 0.75
        js_utils.highlight_with_jquery_2(
            self.driver, message, selector, o_bs, duration
        )

    def __highlight_with_assert_success(
        self, message, selector, by="css selector"
    ):
        selector, by = self.__recalculate_selector(selector, by, xp_ok=False)
        element = self.wait_for_element_visible(
            selector, by=by, timeout=settings.SMALL_TIMEOUT
        )
        try:
            if self.browser != "safari":
                scroll_distance = js_utils.get_scroll_distance_to_element(
                    self.driver, element
                )
                if abs(scroll_distance) > constants.Values.SSMD:
                    self.__jquery_slow_scroll_to(selector, by)
                else:
                    self.__slow_scroll_to_element(element)
            else:
                self.__jquery_slow_scroll_to(selector, by)
        except Exception:
            self.wait_for_ready_state_complete()
            time.sleep(0.12)
            element = self.wait_for_element_visible(
                selector, by=by, timeout=settings.SMALL_TIMEOUT
            )
            self.__slow_scroll_to_element(element)
        try:
            selector = self.convert_to_css_selector(selector, by=by)
        except Exception:
            # Don't highlight if can't convert to CSS_SELECTOR
            return

        o_bs = ""  # original_box_shadow
        try:
            style = element.get_attribute("style")
        except Exception:
            self.wait_for_ready_state_complete()
            time.sleep(0.12)
            element = self.wait_for_element_visible(
                selector, by="css selector", timeout=settings.SMALL_TIMEOUT
            )
            style = element.get_attribute("style")
        if style:
            if "box-shadow: " in style:
                box_start = style.find("box-shadow: ")
                box_end = style.find(";", box_start) + 1
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

    def __activate_virtual_display_as_needed(self):
        if self.headless or self.headless2 or self.xvfb:
            width = settings.HEADLESS_START_WIDTH
            height = settings.HEADLESS_START_HEIGHT
            try:
                from sbvirtualdisplay import Display

                self.display = Display(visible=0, size=(width, height))
                self.display.start()
                self.headless_active = True
                sb_config.headless_active = True
            except Exception:
                pass

    def __ad_block_as_needed(self):
        """This is an internal method for handling ad-blocking.
        Use "pytest --ad-block" to enable this during tests.
        When not Chromium or in headless mode, use the hack."""
        if self.ad_block_on and (self.headless or not self.is_chromium()):
            # (Chromium browsers in headed mode use the extension instead)
            current_url = self.get_current_url()
            if not current_url == self.__last_page_load_url:
                if page_actions.is_element_present(
                    self.driver, "iframe", By.CSS_SELECTOR
                ):
                    self.ad_block()
                self.__last_page_load_url = current_url

    def __disable_beforeunload_as_needed(self):
        """Disables beforeunload as needed. Also resets frame_switch state."""
        if (
            hasattr(self, "_disable_beforeunload")
            and self._disable_beforeunload
        ):
            self.disable_beforeunload()
        if self.recorder_mode:
            try:
                current_url = self.get_current_url
            except Exception:
                current_url = None
                self.__last_saved_url = None
            if current_url != self.__last_saved_url:
                self.__frame_switch_layer = 0
                self.__frame_switch_multi = False
                self.__last_saved_url = current_url

    ############

    @decorators.deprecated("You should use re.escape() instead.")
    def jq_format(self, code):
        # DEPRECATED - re.escape() already performs the intended action.
        return js_utils._jq_format(code)

    ############

    # Shadow DOM / Shadow-root methods

    def __get_shadow_element(
        self, selector, timeout=None, must_be_visible=False
    ):
        self.wait_for_ready_state_complete()
        if timeout is None:
            timeout = settings.SMALL_TIMEOUT
        elif timeout == 0:
            timeout = 0.1  # Use for: is_shadow_element_* (* = present/visible)
        if self.timeout_multiplier and timeout == settings.SMALL_TIMEOUT:
            timeout = self.__get_new_timeout(timeout)
        self.__fail_if_invalid_shadow_selector_usage(selector)
        if "::shadow " not in selector:
            raise Exception(
                'A Shadow DOM selector must contain at least one "::shadow "!'
            )
        selectors = selector.split("::shadow ")
        element = self.get_element(selectors[0])
        selector_chain = selectors[0]
        is_present = False
        for selector_part in selectors[1:]:
            shadow_root = None
            if (
                selenium4_or_newer
                and self.is_chromium()
                and int(self.__get_major_browser_version()) >= 96
            ):
                try:
                    shadow_root = element.shadow_root
                except Exception:
                    if self.browser == "chrome":
                        chrome_dict = self.driver.capabilities["chrome"]
                        chrome_dr_version = chrome_dict["chromedriverVersion"]
                        chromedriver_version = chrome_dr_version.split(" ")[0]
                        major_c_dr_version = chromedriver_version.split(".")[0]
                        if int(major_c_dr_version) < 96:
                            upgrade_to = "latest"
                            major_browser_version = (
                                self.__get_major_browser_version()
                            )
                            if int(major_browser_version) >= 96:
                                upgrade_to = str(major_browser_version)
                            message = (
                                "You need to upgrade to a newer\n"
                                "version of chromedriver to interact\n"
                                "with Shadow root elements!\n"
                                "(Current driver version is: %s)"
                                "\n(Minimum driver version is: 96.*)"
                                "\nTo upgrade, run this:"
                                '\n"seleniumbase get chromedriver %s"'
                                % (chromedriver_version, upgrade_to)
                            )
                            raise Exception(message)
                    if timeout != 0.1:  # Skip wait for special 0.1 (See above)
                        time.sleep(2)
                    try:
                        shadow_root = element.shadow_root
                    except Exception:
                        raise Exception(
                            "Element {%s} has no shadow root!" % selector_chain
                        )
            else:  # This part won't work on Chrome 96 or newer.
                # If using Chrome 96 or newer (and on an old Python version),
                #     you'll need to upgrade in order to access Shadow roots.
                # Firefox users will likely hit:
                #     https://github.com/mozilla/geckodriver/issues/1711
                #     When Firefox adds support, switch to element.shadow_root
                try:
                    shadow_root = self.execute_script(
                        "return arguments[0].shadowRoot;", element
                    )
                except Exception:
                    time.sleep(2)
                    shadow_root = self.execute_script(
                        "return arguments[0].shadowRoot;", element
                    )
            if timeout == 0.1 and not shadow_root:
                raise Exception(
                    "Element {%s} has no shadow root!" % selector_chain
                )
            elif not shadow_root:
                time.sleep(2)  # Wait two seconds for the shadow root to appear
                shadow_root = self.execute_script(
                    "return arguments[0].shadowRoot;", element
                )
                if not shadow_root:
                    raise Exception(
                        "Element {%s} has no shadow root!" % selector_chain
                    )
            selector_chain += "::shadow "
            selector_chain += selector_part
            try:
                if (
                    selenium4_or_newer
                    and self.is_chromium()
                    and int(self.__get_major_browser_version()) >= 96
                ):
                    if timeout == 0.1:
                        element = shadow_root.find_element(
                            By.CSS_SELECTOR, value=selector_part
                        )
                    else:
                        found = False
                        for i in range(int(timeout) * 4):
                            try:
                                element = shadow_root.find_element(
                                    By.CSS_SELECTOR, value=selector_part
                                )
                                is_present = True
                                if must_be_visible:
                                    if not element.is_displayed():
                                        raise Exception(
                                            "Shadow Root element not visible!"
                                        )
                                found = True
                                break
                            except Exception:
                                time.sleep(0.2)
                                continue
                        if not found:
                            element = shadow_root.find_element(
                                By.CSS_SELECTOR, value=selector_part
                            )
                            is_present = True
                            if must_be_visible and not element.is_displayed():
                                raise Exception(
                                    "Shadow Root element not visible!"
                                )
                else:
                    element = page_actions.wait_for_element_present(
                        shadow_root,
                        selector_part,
                        by="css selector",
                        timeout=timeout,
                    )
            except Exception:
                error = "not present"
                the_exception = "NoSuchElementException"
                if must_be_visible and is_present:
                    error = "not visible"
                    the_exception = "ElementNotVisibleException"
                msg = (
                    "Shadow DOM Element {%s} was %s after %s seconds!"
                    % (selector_chain, error, timeout)
                )
                page_actions.timeout_exception(the_exception, msg)
        return element

    def __fail_if_invalid_shadow_selector_usage(self, selector):
        if selector.strip().endswith("::shadow"):
            msg = (
                "A Shadow DOM selector cannot end on a shadow root element!"
                " End the selector with an element inside the shadow root!"
            )
            raise Exception(msg)

    def __is_shadow_selector(self, selector):
        self.__fail_if_invalid_shadow_selector_usage(selector)
        if "::shadow " in selector:
            return True
        return False

    def __shadow_click(self, selector, timeout):
        element = self.__get_shadow_element(
            selector, timeout=timeout, must_be_visible=True
        )
        element.click()

    def __shadow_type(self, selector, text, timeout, clear_first=True):
        element = self.__get_shadow_element(
            selector, timeout=timeout, must_be_visible=True
        )
        if clear_first:
            try:
                element.clear()
                backspaces = Keys.BACK_SPACE * 42  # Autofill Defense
                element.send_keys(backspaces)
            except Exception:
                pass
        text = self.__get_type_checked_text(text)
        if not text.endswith("\n"):
            element.send_keys(text)
            if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                self.wait_for_ready_state_complete()
        else:
            element.send_keys(text[:-1])
            element.send_keys(Keys.RETURN)
            if settings.WAIT_FOR_RSC_ON_PAGE_LOADS:
                self.wait_for_ready_state_complete()

    def __shadow_clear(self, selector, timeout):
        element = self.__get_shadow_element(
            selector, timeout=timeout, must_be_visible=True
        )
        try:
            element.clear()
            backspaces = Keys.BACK_SPACE * 42  # Autofill Defense
            element.send_keys(backspaces)
        except Exception:
            pass

    def __get_shadow_text(self, selector, timeout):
        element = self.__get_shadow_element(
            selector, timeout=timeout, must_be_visible=True
        )
        element_text = element.text
        if self.browser == "safari":
            element_text = element.get_attribute("innerText")
        return element_text

    def __get_shadow_attribute(self, selector, attribute, timeout):
        element = self.__get_shadow_element(selector, timeout=timeout)
        return element.get_attribute(attribute)

    def __wait_for_shadow_text_visible(self, text, selector, timeout):
        text = str(text)
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (settings.SMALL_TIMEOUT * 1000.0)
        for x in range(int(settings.SMALL_TIMEOUT * 10)):
            try:
                actual_text = self.__get_shadow_text(
                    selector, timeout=1
                ).strip()
                text = text.strip()
                if text not in actual_text:
                    msg = (
                        "Expected text {%s} in element {%s} was not visible!"
                        % (text, selector)
                    )
                    page_actions.timeout_exception(
                        "ElementNotVisibleException", msg
                    )
                return True
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        actual_text = self.__get_shadow_text(selector, timeout=1).strip()
        text = text.strip()
        if text not in actual_text:
            msg = "Expected text {%s} in element {%s} was not visible!" % (
                text,
                selector,
            )
            page_actions.timeout_exception("ElementNotVisibleException", msg)
        return True

    def __wait_for_exact_shadow_text_visible(self, text, selector, timeout):
        text = str(text)
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (settings.SMALL_TIMEOUT * 1000.0)
        for x in range(int(settings.SMALL_TIMEOUT * 10)):
            try:
                actual_text = self.__get_shadow_text(
                    selector, timeout=1
                ).strip()
                text = text.strip()
                if text != actual_text:
                    msg = (
                        "Expected exact text {%s} in element {%s} not visible!"
                        "" % (text, selector)
                    )
                    page_actions.timeout_exception(
                        "ElementNotVisibleException", msg
                    )
                return True
            except Exception:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        actual_text = self.__get_shadow_text(selector, timeout=1).strip()
        text = text.strip()
        if text != actual_text:
            msg = (
                "Expected exact text {%s} in element {%s} was not visible!"
                % (text, selector)
            )
            page_actions.timeout_exception("ElementNotVisibleException", msg)
        return True

    def __assert_shadow_text_visible(self, text, selector, timeout):
        self.__wait_for_shadow_text_visible(text, selector, timeout)
        if self.demo_mode:
            a_t = "ASSERT TEXT"
            i_n = "in"
            by = By.CSS_SELECTOR
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert_text(self._language)
                i_n = SD.translate_in(self._language)
            messenger_post = "%s: {%s} %s %s: %s" % (
                a_t,
                text,
                i_n,
                by.upper(),
                selector,
            )
            try:
                js_utils.activate_jquery(self.driver)
                js_utils.post_messenger_success_message(
                    self.driver, messenger_post, self.message_duration
                )
            except Exception:
                pass

    def __assert_exact_shadow_text_visible(self, text, selector, timeout):
        self.__wait_for_exact_shadow_text_visible(text, selector, timeout)
        if self.demo_mode:
            a_t = "ASSERT EXACT TEXT"
            i_n = "in"
            by = By.CSS_SELECTOR
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert_exact_text(self._language)
                i_n = SD.translate_in(self._language)
            messenger_post = "%s: {%s} %s %s: %s" % (
                a_t,
                text,
                i_n,
                by.upper(),
                selector,
            )
            try:
                js_utils.activate_jquery(self.driver)
                js_utils.post_messenger_success_message(
                    self.driver, messenger_post, self.message_duration
                )
            except Exception:
                pass

    def __is_shadow_element_present(self, selector):
        try:
            element = self.__get_shadow_element(selector, timeout=0.1)
            return element is not None
        except Exception:
            return False

    def __is_shadow_element_visible(self, selector):
        try:
            element = self.__get_shadow_element(selector, timeout=0.1)
            return element.is_displayed()
        except Exception:
            return False

    def __is_shadow_element_clickable(self, selector):
        try:
            element = self.__get_shadow_element(selector, timeout=0.1)
            if element.is_displayed() and element.is_enabled():
                return True
            return False
        except Exception:
            return False

    def __is_shadow_element_enabled(self, selector):
        try:
            element = self.__get_shadow_element(selector, timeout=0.1)
            return element.is_enabled()
        except Exception:
            return False

    def __is_shadow_text_visible(self, text, selector):
        text = str(text)
        try:
            element = self.__get_shadow_element(selector, timeout=0.1)
            if self.browser == "safari":
                return (
                    element.is_displayed()
                    and text in element.get_attribute("innerText")
                )
            return element.is_displayed() and text in element.text
        except Exception:
            return False

    def __is_shadow_attribute_present(self, selector, attribute, value=None):
        try:
            element = self.__get_shadow_element(selector, timeout=0.1)
            found_value = element.get_attribute(attribute)
            if found_value is None:
                return False
            if value is not None:
                if found_value == value:
                    return True
                else:
                    return False
            else:
                return True
        except Exception:
            return False

    def __wait_for_shadow_element_present(self, selector, timeout):
        element = self.__get_shadow_element(selector, timeout=timeout)
        return element

    def __wait_for_shadow_element_visible(self, selector, timeout):
        element = self.__get_shadow_element(
            selector, timeout=timeout, must_be_visible=True
        )
        return element

    def __wait_for_shadow_attribute_present(
        self, selector, attribute, value=None, timeout=None
    ):
        element = self.__get_shadow_element(selector, timeout=timeout)
        actual_value = element.get_attribute(attribute)
        plural = "s"
        if timeout == 1:
            plural = ""
        if value is None:
            # The element attribute only needs to exist
            if actual_value is not None:
                return element
            else:
                # The element does not have the attribute
                message = (
                    "Expected attribute {%s} of element {%s} "
                    "was not present after %s second%s!"
                    % (attribute, selector, timeout, plural)
                )
                page_actions.timeout_exception(
                    "NoSuchAttributeException", message
                )
        else:
            if actual_value == value:
                return element
            else:
                message = (
                    "Expected value {%s} for attribute {%s} of element "
                    "{%s} was not present after %s second%s! "
                    "(The actual value was {%s})"
                    % (
                        value,
                        attribute,
                        selector,
                        timeout,
                        plural,
                        actual_value,
                    )
                )
                page_actions.timeout_exception(
                    "NoSuchAttributeException", message
                )

    def __assert_shadow_element_present(self, selector):
        self.__get_shadow_element(selector)
        if self.demo_mode:
            a_t = "ASSERT"
            by = By.CSS_SELECTOR
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert(self._language)
            messenger_post = "%s %s: %s" % (a_t, by.upper(), selector)
            try:
                js_utils.activate_jquery(self.driver)
                js_utils.post_messenger_success_message(
                    self.driver, messenger_post, self.message_duration
                )
            except Exception:
                pass

    def __assert_shadow_element_visible(self, selector):
        element = self.__get_shadow_element(selector)
        if not element.is_displayed():
            msg = "Shadow DOM Element {%s} was not visible!" % selector
            page_actions.timeout_exception("NoSuchElementException", msg)
        if self.demo_mode:
            a_t = "ASSERT"
            by = By.CSS_SELECTOR
            if self._language != "English":
                from seleniumbase.fixtures.words import SD

                a_t = SD.translate_assert(self._language)
            messenger_post = "%s %s: %s" % (a_t, by.upper(), selector)
            try:
                js_utils.activate_jquery(self.driver)
                js_utils.post_messenger_success_message(
                    self.driver, messenger_post, self.message_duration
                )
            except Exception:
                pass

    ############

    def setUp(self, masterqa_mode=False):
        """
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass setUp() method:
        super(SubClassOfBaseCase, self).setUp()
        """
        if not hasattr(self, "_using_sb_fixture") and self.__called_setup:
            # This test already called setUp()
            return
        self.__called_setup = True
        self.__called_teardown = False
        self.masterqa_mode = masterqa_mode
        self.is_pytest = None
        try:
            # This raises an exception if the test is not coming from pytest
            self.is_pytest = sb_config.is_pytest
        except Exception:
            # Not using pytest (could be nosetests, behave, or raw Python)
            self.is_pytest = False
        if self.is_pytest:
            # pytest-specific code
            test_id = self.__get_test_id()
            self.test_id = test_id
            self.is_behave = False
            if hasattr(self, "_using_sb_fixture"):
                self.test_id = sb_config._test_id
                if hasattr(sb_config, "_sb_pdb_driver"):
                    sb_config._sb_pdb_driver = None
            self.browser = sb_config.browser
            self.account = sb_config.account
            self.data = sb_config.data
            self.var1 = sb_config.var1
            self.var2 = sb_config.var2
            self.var3 = sb_config.var3
            variables = sb_config.variables
            if variables and type(variables) is str and len(variables) > 0:
                import ast

                bad_input = False
                if (
                    not variables.startswith("{")
                    or not variables.endswith("}")
                ):
                    bad_input = True
                else:
                    try:
                        variables = ast.literal_eval(variables)
                        if not type(variables) is dict:
                            bad_input = True
                    except Exception:
                        bad_input = True
                if bad_input:
                    raise Exception(
                        '\nExpecting a Python dictionary for "variables"!'
                        "\nEg. --variables=\"{'KEY1':'VALUE', 'KEY2':123}\""
                    )
            else:
                variables = {}
            sb_config.variables = variables
            self.variables = sb_config.variables
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
            sb_config.headless_active = False
            self.headed = sb_config.headed
            self.xvfb = sb_config.xvfb
            self.locale_code = sb_config.locale_code
            self.interval = sb_config.interval
            self.start_page = sb_config.start_page
            self.log_path = sb_config.log_path
            self.with_testing_base = sb_config.with_testing_base
            self.with_basic_test_info = sb_config.with_basic_test_info
            self.with_screen_shots = sb_config.with_screen_shots
            self.with_page_source = sb_config.with_page_source
            self.with_db_reporting = sb_config.with_db_reporting
            self.with_s3_logging = sb_config.with_s3_logging
            self.protocol = sb_config.protocol
            self.servername = sb_config.servername
            self.port = sb_config.port
            self.proxy_string = sb_config.proxy_string
            self.proxy_bypass_list = sb_config.proxy_bypass_list
            self.proxy_pac_url = sb_config.proxy_pac_url
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
            self.do_not_track = sb_config.do_not_track
            self.chromium_arg = sb_config.chromium_arg
            self.firefox_arg = sb_config.firefox_arg
            self.firefox_pref = sb_config.firefox_pref
            self.verify_delay = sb_config.verify_delay
            self.recorder_mode = sb_config.recorder_mode
            self.recorder_ext = sb_config.recorder_mode
            self.rec_print = sb_config.rec_print
            self.rec_behave = sb_config.rec_behave
            self.record_sleep = sb_config.record_sleep
            if self.rec_print and not self.recorder_mode:
                self.recorder_mode = True
                self.recorder_ext = True
            elif self.rec_behave and not self.recorder_mode:
                self.recorder_mode = True
                self.recorder_ext = True
            elif self.record_sleep and not self.recorder_mode:
                self.recorder_mode = True
                self.recorder_ext = True
            self.disable_js = sb_config.disable_js
            self.disable_csp = sb_config.disable_csp
            self.disable_ws = sb_config.disable_ws
            self.enable_ws = sb_config.enable_ws
            if not self.disable_ws:
                self.enable_ws = True
            self.enable_sync = sb_config.enable_sync
            self.use_auto_ext = sb_config.use_auto_ext
            self.undetectable = sb_config.undetectable
            self.uc_subprocess = sb_config.uc_subprocess
            self.no_sandbox = sb_config.no_sandbox
            self.disable_gpu = sb_config.disable_gpu
            self.headless2 = sb_config.headless2
            self.incognito = sb_config.incognito
            self.guest_mode = sb_config.guest_mode
            self.devtools = sb_config.devtools
            self.remote_debug = sb_config.remote_debug
            self._multithreaded = sb_config._multithreaded
            self._reuse_session = sb_config.reuse_session
            self._crumbs = sb_config.crumbs
            self._disable_beforeunload = sb_config._disable_beforeunload
            self.dashboard = sb_config.dashboard
            self._dash_initialized = sb_config._dashboard_initialized
            if self.dashboard and self._multithreaded:
                self.dash_lock = fasteners.InterProcessLock(
                    constants.Dashboard.LOCKFILE
                )
            self.enable_3d_apis = sb_config.enable_3d_apis
            self.swiftshader = sb_config.swiftshader
            self.user_data_dir = sb_config.user_data_dir
            self.extension_zip = sb_config.extension_zip
            self.extension_dir = sb_config.extension_dir
            self.page_load_strategy = sb_config.page_load_strategy
            self.use_wire = sb_config.use_wire
            self.external_pdf = sb_config.external_pdf
            self._final_debug = sb_config.final_debug
            self.window_size = sb_config.window_size
            window_size = self.window_size
            if window_size:
                if window_size.count(",") != 1:
                    message = (
                        '\n\n  window_size expects a "width,height" string!'
                        '\n  (Your input was: "%s")\n' % window_size
                    )
                    raise Exception(message)
                window_size = window_size.replace(" ", "")
                width = None
                height = None
                try:
                    width = int(window_size.split(",")[0])
                    height = int(window_size.split(",")[1])
                except Exception:
                    message = (
                        '\n\n  Expecting integer values for "width,height"!'
                        '\n  (window_size input was: "%s")\n' % window_size
                    )
                    raise Exception(message)
                settings.CHROME_START_WIDTH = width
                settings.CHROME_START_HEIGHT = height
                settings.HEADLESS_START_WIDTH = width
                settings.HEADLESS_START_HEIGHT = height
            self.maximize_option = sb_config.maximize_option
            self.save_screenshot_after_test = sb_config.save_screenshot
            self.no_screenshot_after_test = sb_config.no_screenshot
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
                    ApplicationManager,
                )
                from seleniumbase.core.testcase_manager import (
                    ExecutionQueryPayload,
                )
                from seleniumbase.core.testcase_manager import (
                    TestcaseDataPayload,
                )
                from seleniumbase.core.testcase_manager import TestcaseManager

                self.execution_guid = str(uuid.uuid4())
                self.testcase_guid = None
                self.execution_start_time = 0
                self.case_start_time = 0
                self.testcase_manager = None
                self.testcase_manager = TestcaseManager(self.database_env)
                #
                exec_payload = ExecutionQueryPayload()
                exec_payload.execution_start_time = int(time.time() * 1000.0)
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
                    self
                )
                data_payload.env = application.split(".")[0]
                data_payload.start_time = application.split(".")[1]
                data_payload.state = constants.State.UNTESTED
                self.__skip_reason = None
                self.testcase_manager.insert_testcase_data(data_payload)
                self.case_start_time = int(time.time() * 1000.0)
            self.__activate_virtual_display_as_needed()
        elif hasattr(self, "is_behave") and self.is_behave:
            self.__initialize_variables()
            self.__activate_virtual_display_as_needed()
        elif hasattr(self, "is_nosetest") and self.is_nosetest:
            pass  # Setup performed in plugins for nosetests
        else:
            # Pure Python run
            self.__activate_virtual_display_as_needed()

        # Verify that SeleniumBase is installed successfully
        if not hasattr(self, "browser"):
            raise Exception(
                "SeleniumBase plugins DID NOT load! * Please REINSTALL!\n"
                "*** Either install SeleniumBase in Dev Mode from a clone:\n"
                '    >>> "pip install -e ."     (Run in DIR with setup.py)\n'
                "*** Or install the latest SeleniumBase version from PyPI:\n"
                '    >>> "pip install -U seleniumbase"    (Run in any DIR)'
            )

        if not hasattr(sb_config, "_is_timeout_changed"):
            # Should only be reachable from pure Python runs
            sb_config._is_timeout_changed = False
            sb_config._SMALL_TIMEOUT = settings.SMALL_TIMEOUT
            sb_config._LARGE_TIMEOUT = settings.LARGE_TIMEOUT

        if sb_config._is_timeout_changed:
            if sb_config._SMALL_TIMEOUT and sb_config._LARGE_TIMEOUT:
                settings.SMALL_TIMEOUT = sb_config._SMALL_TIMEOUT
                settings.LARGE_TIMEOUT = sb_config._LARGE_TIMEOUT

        if not hasattr(sb_config, "_recorded_actions"):
            # Only filled when Recorder Mode is enabled
            sb_config._recorded_actions = {}
            sb_config._behave_recorded_actions = {}

        if not hasattr(settings, "SWITCH_TO_NEW_TABS_ON_CLICK"):
            # If using an older settings file, set the new definitions manually
            settings.SWITCH_TO_NEW_TABS_ON_CLICK = True

        # Parse the settings file
        if self.settings_file:
            from seleniumbase.core import settings_parser

            settings_parser.set_settings(self.settings_file)

        # Set variables that may be useful to developers
        self.log_abspath = os.path.abspath(self.log_path)
        self.data_path = os.path.join(self.log_path, self.__get_test_id())
        self.data_abspath = os.path.abspath(self.data_path)

        # Add _test_logpath value to sb_config
        test_id = self.__get_test_id()
        test_logpath = os.path.join(self.log_path, test_id)
        sb_config._test_logpath = test_logpath

        # Add _process_dashboard_entry method to sb_config
        sb_config._process_dashboard_entry = self._process_dashboard_entry

        # Add _add_pytest_html_extra method to sb_config
        sb_config._add_pytest_html_extra = self._add_pytest_html_extra

        # Add _process_visual_baseline_logs method to sb_config
        sb_config._process_v_baseline_logs = self._process_visual_baseline_logs

        # Add _log_fail_data method to sb_config
        sb_config._log_fail_data = self._log_fail_data

        # Reset the last_page_screenshot variables
        sb_config._last_page_screenshot = None
        sb_config._last_page_screenshot_png = None

        # Indictate to pytest reports that SeleniumBase is being used
        sb_config._sbase_detected = True
        sb_config._only_unittest = False

        # Mobile Emulator device metrics: CSS Width, CSS Height, & Pixel-Ratio
        if self.device_metrics:
            metrics_string = self.device_metrics
            metrics_string = metrics_string.replace(" ", "")
            metrics_list = metrics_string.split(",")
            exception_string = (
                "Invalid input for Mobile Emulator device metrics!\n"
                "Expecting a comma-separated string with three\n"
                "integer values for Width, Height, and Pixel-Ratio.\n"
                'Example: --metrics="411,731,3" '
            )
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
                # Use the Pixel 4 user agent by default if not specified
                self.user_agent = (
                    "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/89.0.4389.105 Mobile Safari/537.36"
                )

        if self.browser in ["firefox", "ie", "safari", "opera"]:
            # The Recorder Mode browser extension is only for Chrome/Edge.
            if self.recorder_mode:
                message = (
                    "Recorder Mode ONLY supports Chrome and Edge!\n"
                    '(Your browser choice was: "%s")' % self.browser
                )
                raise Exception(message)

        # Dashboard pre-processing:
        if self.dashboard:
            if self._multithreaded:
                with self.dash_lock:
                    if not self._dash_initialized:
                        sb_config._dashboard_initialized = True
                        self._dash_initialized = True
                        self.__process_dashboard(False, init=True)
            else:
                if not self._dash_initialized:
                    sb_config._dashboard_initialized = True
                    self._dash_initialized = True
                    self.__process_dashboard(False, init=True)

        # Set the JS start time for Recorder Mode.
        # Use this to skip saving recorded actions from previous tests.
        if self.recorder_mode:
            self.__js_start_time = int(time.time() * 1000.0)

        has_url = False
        if self._reuse_session:
            if not hasattr(sb_config, "shared_driver"):
                sb_config.shared_driver = None
            if sb_config.shared_driver:
                try:
                    self._default_driver = sb_config.shared_driver
                    self.driver = sb_config.shared_driver
                    self._drivers_list = [sb_config.shared_driver]
                    url = self.get_current_url()
                    if url is not None:
                        has_url = True
                    if len(self.driver.window_handles) > 1:
                        while len(self.driver.window_handles) > 1:
                            self.switch_to_window(
                                len(self.driver.window_handles) - 1
                            )
                            self.driver.close()
                        self.switch_to_window(0)
                    if self._crumbs:
                        self.driver.delete_all_cookies()
                except Exception:
                    pass
        if self._reuse_session and sb_config.shared_driver and has_url:
            good_start_page = False
            if self.recorder_ext:
                self.__js_start_time = int(time.time() * 1000.0)
            if self.start_page and len(self.start_page) >= 4:
                if page_utils.is_valid_url(self.start_page):
                    good_start_page = True
                    self.__new_window_on_rec_open = False
                    self.open(self.start_page)
                    self.__new_window_on_rec_open = True
                else:
                    new_start_page = "https://" + self.start_page
                    if page_utils.is_valid_url(new_start_page):
                        good_start_page = True
                        self.__dont_record_open = True
                        self.open(new_start_page)
                        self.__dont_record_open = False
            if self.recorder_ext or (self._crumbs and not good_start_page):
                if self.get_current_url() != "about:blank":
                    self.__new_window_on_rec_open = False
                    self.open("about:blank")
                    self.__new_window_on_rec_open = True
                    if self.recorder_ext:
                        self.__js_start_time = int(time.time() * 1000.0)
        else:
            # Launch WebDriver for both Pytest and Nosetests
            self.driver = self.get_new_driver(
                browser=self.browser,
                headless=self.headless,
                locale_code=self.locale_code,
                protocol=self.protocol,
                servername=self.servername,
                port=self.port,
                proxy=self.proxy_string,
                proxy_bypass_list=self.proxy_bypass_list,
                proxy_pac_url=self.proxy_pac_url,
                agent=self.user_agent,
                switch_to=True,
                cap_file=self.cap_file,
                cap_string=self.cap_string,
                recorder_ext=self.recorder_ext,
                disable_js=self.disable_js,
                disable_csp=self.disable_csp,
                enable_ws=self.enable_ws,
                enable_sync=self.enable_sync,
                use_auto_ext=self.use_auto_ext,
                undetectable=self.undetectable,
                uc_subprocess=self.uc_subprocess,
                no_sandbox=self.no_sandbox,
                disable_gpu=self.disable_gpu,
                headless2=self.headless2,
                incognito=self.incognito,
                guest_mode=self.guest_mode,
                devtools=self.devtools,
                remote_debug=self.remote_debug,
                enable_3d_apis=self.enable_3d_apis,
                swiftshader=self.swiftshader,
                ad_block_on=self.ad_block_on,
                block_images=self.block_images,
                do_not_track=self.do_not_track,
                chromium_arg=self.chromium_arg,
                firefox_arg=self.firefox_arg,
                firefox_pref=self.firefox_pref,
                user_data_dir=self.user_data_dir,
                extension_zip=self.extension_zip,
                extension_dir=self.extension_dir,
                page_load_strategy=self.page_load_strategy,
                use_wire=self.use_wire,
                external_pdf=self.external_pdf,
                is_mobile=self.mobile_emulator,
                d_width=self.__device_width,
                d_height=self.__device_height,
                d_p_r=self.__device_pixel_ratio,
            )
            if selenium4_or_newer and self.driver.timeouts.implicit_wait > 0:
                self.driver.implicitly_wait(0)
            elif not selenium4_or_newer:
                self.driver.implicitly_wait(0)
            self._default_driver = self.driver
            if self._reuse_session:
                sb_config.shared_driver = self.driver
            if len(self._drivers_list) == 0:
                # The user is overriding self.get_new_driver()
                # (Otherwise this code shouldn't be reachable)
                self._drivers_list.append(self.driver)
                self._drivers_browser_map[self.driver] = self.browser

        if self.browser in ["firefox", "ie", "safari", "opera"]:
            # Only Chrome and Edge browsers have the mobile emulator.
            # Some actions such as hover-clicking are different on mobile.
            self.mobile_emulator = False

        # Configure the test time limit (if used).
        self.set_time_limit(self.time_limit)

        # Configure the page load timeout
        if hasattr(settings, "PAGE_LOAD_TIMEOUT"):
            self.driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)
        else:
            self.driver.set_page_load_timeout(120)  # Selenium uses 300

        # Set the start time for the test (in ms).
        # Although the pytest clock starts before setUp() begins,
        # the time-limit clock starts at the end of the setUp() method.
        sb_config.start_time_ms = int(time.time() * 1000.0)
        self.__start_time_ms = sb_config.start_time_ms

    def __set_last_page_screenshot(self):
        """self.__last_page_screenshot is only for pytest html report logs.
        self.__last_page_screenshot_png is for all screenshot log files."""
        SCREENSHOT_SKIPPED = constants.Warnings.SCREENSHOT_SKIPPED
        SCREENSHOT_UNDEFINED = constants.Warnings.SCREENSHOT_UNDEFINED
        if (
            hasattr(self, "no_screenshot_after_test")
            and self.no_screenshot_after_test
        ):
            from seleniumbase.core import encoded_images

            NO_SCREENSHOT = encoded_images.get_no_screenshot_png()
            self.__last_page_screenshot = NO_SCREENSHOT
            self.__last_page_screenshot_png = SCREENSHOT_SKIPPED
            sb_config._last_page_screenshot_png = NO_SCREENSHOT
            return
        element = None
        if (
            not self.__last_page_screenshot
            and not self.__last_page_screenshot_png
        ):
            try:
                try:
                    element = page_actions.wait_for_element_visible(
                        self.driver,
                        "body",
                        "css selector",
                        timeout=0.1,
                        ignore_test_time_limit=True,
                    )
                except Exception:
                    element = page_actions.wait_for_element_present(
                        self.driver,
                        "body",
                        "css selector",
                        timeout=0.1,
                        ignore_test_time_limit=True,
                    )
                try:
                    self.__last_page_screenshot = element.screenshot_as_base64
                except Exception:
                    try:
                        self.__last_page_screenshot = (
                            self.driver.get_screenshot_as_base64()
                        )
                    except Exception:
                        pass
            except Exception:
                pass
            if not self.__last_page_screenshot:
                self.__last_page_screenshot = SCREENSHOT_UNDEFINED
                self.__last_page_screenshot_png = SCREENSHOT_UNDEFINED
                if element:
                    try:
                        self.__last_page_screenshot_png = (
                            element.screenshot_as_png
                        )
                    except Exception:
                        try:
                            self.__last_page_screenshot_png = (
                                self.driver.get_screenshot_as_png()
                            )
                        except Exception:
                            pass
            else:
                import base64

                try:
                    self.__last_page_screenshot_png = (
                        base64.b64decode(self.__last_page_screenshot)
                    )
                except Exception:
                    if element:
                        try:
                            self.__last_page_screenshot_png = (
                                element.screenshot_as_png
                            )
                        except Exception:
                            try:
                                self.__last_page_screenshot_png = (
                                    self.driver.get_screenshot_as_png()
                                )
                            except Exception:
                                pass
        sb_config._last_page_screenshot_png = self.__last_page_screenshot_png

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
                        self.driver, self.driver.page_source
                    )
                )
            except Exception:
                self.__last_page_source = (
                    constants.Warnings.PAGE_SOURCE_UNDEFINED
                )
            sb_config._last_page_source = self.__last_page_source

    def __get_exception_info(self):
        exc_message = None
        if (
            python3
            and hasattr(self, "_outcome")
            and (hasattr(self._outcome, "errors") and self._outcome.errors)
        ):
            try:
                exc_message = self._outcome.errors[0][1][1]
            except Exception:
                exc_message = "(Unknown Exception)"
        else:
            try:
                exc_message = sys.last_value
            except Exception:
                exc_message = "(Unknown Exception)"
        return str(exc_message)

    def __insert_test_result(self, state, err):
        from seleniumbase.core.testcase_manager import TestcaseDataPayload

        data_payload = TestcaseDataPayload()
        data_payload.runtime = int(time.time() * 1000.0) - self.case_start_time
        data_payload.guid = self.testcase_guid
        data_payload.execution_guid = self.execution_guid
        data_payload.state = state
        if err:
            import traceback

            tb_string = traceback.format_exc()
            if "Message: " in tb_string:
                data_payload.message = (
                    "Message: " + tb_string.split("Message: ")[-1]
                )
            elif "Exception: " in tb_string:
                data_payload.message = tb_string.split("Exception: ")[-1]
            elif "Error: " in tb_string:
                data_payload.message = tb_string.split("Error: ")[-1]
            else:
                data_payload.message = self.__get_exception_info()
        else:
            test_id = self.__get_test_id_2()
            if (
                self.is_pytest
                and test_id in sb_config._results.keys()
                and (sb_config._results[test_id] == "Skipped")
            ):
                if self.__skip_reason:
                    data_payload.message = "Skipped:   " + self.__skip_reason
                else:
                    data_payload.message = "Skipped:   (no reason given)"
        self.testcase_manager.update_testcase_data(data_payload)

    def _add_pytest_html_extra(self):
        if sys.version_info < (3, 11):
            return
        self.__add_pytest_html_extra()

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
                        extra_url["name"] = "URL"
                        extra_url["format"] = "url"
                        extra_url["format_type"] = "url"
                        extra_url["content"] = self.__last_page_url
                        extra_url["mime_type"] = None
                        extra_url["extension"] = None
                        extra_image = {}
                        extra_image["name"] = "Screenshot"
                        extra_image["format"] = "image"
                        extra_image["format_type"] = "image"
                        extra_image["content"] = self.__last_page_screenshot
                        extra_image["mime_type"] = "image/png"
                        extra_image["extension"] = "png"
                        self.__added_pytest_html_extra = True
                        if self.__last_page_screenshot != (
                            constants.Warnings.SCREENSHOT_UNDEFINED
                        ):
                            self._html_report_extra.append(extra_url)
                            self._html_report_extra.append(extra_image)
            except Exception:
                pass

    def __delay_driver_quit(self):
        delay_driver_quit = False
        if (
            hasattr(self, "_using_sb_fixture")
            and self._using_sb_fixture
            and "--pdb" in sys.argv
            and self.__has_exception()
            and len(self._drivers_list) == 1
            and self.driver == self._default_driver
        ):
            # Special case: Using sb fixture, --pdb, and has error.
            # Keep the driver open for debugging and quit it later.
            delay_driver_quit = True
        return delay_driver_quit

    def __quit_all_drivers(self):
        if self._reuse_session and sb_config.shared_driver:
            if len(self._drivers_list) > 0:
                if self._drivers_list[0] != sb_config.shared_driver:
                    if sb_config.shared_driver in self._drivers_list:
                        self._drivers_list.remove(sb_config.shared_driver)
                    self._drivers_list.insert(0, sb_config.shared_driver)
                self._default_driver = self._drivers_list[0]
                self.switch_to_default_driver()
            if len(self._drivers_list) > 1:
                self._drivers_list = self._drivers_list[1:]
            else:
                self._drivers_list = []
        # Close all open browser windows
        delay_driver_quit = self.__delay_driver_quit()
        self._drivers_list.reverse()  # Last In, First Out
        for driver in self._drivers_list:
            try:
                if (
                    not is_windows
                    or self.browser == "ie"
                    or self.servername != "localhost"
                    or (
                        hasattr(driver, "service")
                        and driver.service.process
                    )
                ):
                    if not delay_driver_quit:
                        driver.quit()
                    else:
                        # Save it for later to quit it later.
                        sb_config._sb_pdb_driver = driver
            except AttributeError:
                pass
            except Exception:
                pass
        if not delay_driver_quit:
            self.driver = None
            self._default_driver = None
            self._drivers_list = []

    def __has_exception(self):
        has_exception = False
        if hasattr(sys, "last_traceback") and sys.last_traceback is not None:
            has_exception = True
        elif hasattr(self, "is_context_manager") and self.is_context_manager:
            if self.with_testing_base and self._has_failure:
                return True
            else:
                return False
        elif (
            python3
            and hasattr(self, "_outcome")
            and hasattr(self._outcome, "errors")
        ):
            if self._outcome.errors:
                has_exception = True
        else:
            if python3:
                has_exception = sys.exc_info()[1] is not None
            else:
                if not hasattr(self, "_using_sb_fixture_class") and (
                    not hasattr(self, "_using_sb_fixture_no_class")
                ):
                    has_exception = sys.exc_info()[1] is not None
                else:
                    has_exception = len(str(sys.exc_info()[1]).strip()) > 0
        if (
            self.__will_be_skipped
            and (hasattr(self, "_using_sb_fixture") or not python3)
        ):
            has_exception = False
        return has_exception

    def __get_test_id(self):
        """The id used in various places such as the test log path."""
        if hasattr(self, "is_behave") and self.is_behave:
            file_name = sb_config.behave_scenario.filename
            file_name = file_name.replace("/", ".").replace("\\", ".")
            scenario_name = sb_config.behave_scenario.name
            if " -- @" in scenario_name:
                scenario_name = scenario_name.split(" # ")[0].rstrip()
            scenario_name = re.sub(r"[^\w" + r"_ " + r"]", "", scenario_name)
            scenario_name = scenario_name.replace(" ", "_")
            test_id = "%s.%s" % (file_name, scenario_name)
            return test_id
        elif hasattr(self, "is_context_manager") and self.is_context_manager:
            filename = self.__class__.__module__.split(".")[-1] + ".py"
            methodname = self._testMethodName
            context_id = None
            if filename == "base_case.py" or methodname == "runTest":
                import traceback

                stack_base = traceback.format_stack()[0].split(", in ")[0]
                test_base = stack_base.split(", in ")[0].split(os.sep)[-1]
                if hasattr(self, "cm_filename") and self.cm_filename:
                    filename = self.cm_filename
                else:
                    filename = test_base.split('"')[0]
                methodname = ".line_" + test_base.split(", line ")[-1]
                context_id = filename.split(".")[0] + methodname
                return context_id
        test_id = "%s.%s.%s" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._testMethodName,
        )
        if self._sb_test_identifier and len(str(self._sb_test_identifier)) > 6:
            test_id = self._sb_test_identifier
            test_id = test_id.replace(".py::", ".").replace("::", ".")
            test_id = test_id.replace("/", ".")
        return test_id

    def __get_test_id_2(self):
        """The id for SeleniumBase Dashboard entries."""
        if "PYTEST_CURRENT_TEST" in os.environ:
            return os.environ["PYTEST_CURRENT_TEST"].split(" ")[0]
        if hasattr(self, "is_behave") and self.is_behave:
            return self.__get_test_id()
        test_id = "%s.%s.%s" % (
            self.__class__.__module__.split(".")[-1],
            self.__class__.__name__,
            self._testMethodName,
        )
        if self._sb_test_identifier and len(str(self._sb_test_identifier)) > 6:
            test_id = self._sb_test_identifier
            if test_id.count(".") > 1:
                test_id = ".".join(test_id.split(".")[1:])
        return test_id

    def __get_display_id(self):
        """The id for running a test from pytest. (Displayed on Dashboard)"""
        if "PYTEST_CURRENT_TEST" in os.environ:
            return os.environ["PYTEST_CURRENT_TEST"].split(" ")[0]
        if hasattr(self, "is_behave") and self.is_behave:
            file_name = sb_config.behave_scenario.filename
            line_num = sb_config.behave_line_num
            scenario_name = sb_config.behave_scenario.name
            if " -- @" in scenario_name:
                scenario_name = scenario_name.split(" # ")[0].rstrip()
            test_id = "%s:%s => %s" % (file_name, line_num, scenario_name)
            return test_id
        test_id = "%s.py::%s::%s" % (
            self.__class__.__module__.replace(".", "/"),
            self.__class__.__name__,
            self._testMethodName,
        )
        if self._sb_test_identifier and len(str(self._sb_test_identifier)) > 6:
            test_id = self._sb_test_identifier
            if hasattr(self, "_using_sb_fixture_class"):
                if test_id.count(".") >= 2:
                    parts = test_id.split(".")
                    full = parts[-3] + ".py::" + parts[-2] + "::" + parts[-1]
                    test_id = full
            elif hasattr(self, "_using_sb_fixture_no_class"):
                if test_id.count(".") >= 1:
                    parts = test_id.split(".")
                    full = parts[-2] + ".py::" + parts[-1]
                    test_id = full
        return test_id

    def __get_filename(self):
        """The filename of the current SeleniumBase test. (NOT Path)"""
        filename = None
        if "PYTEST_CURRENT_TEST" in os.environ:
            test_id = os.environ["PYTEST_CURRENT_TEST"].split(" ")[0]
            filename = test_id.split("::")[0].split("/")[-1]
        elif hasattr(self, "is_behave") and self.is_behave:
            filename = sb_config.behave_scenario.filename
            filename = filename.split("/")[-1].split("\\")[-1]
        else:
            filename = self.__class__.__module__.split(".")[-1] + ".py"
        return filename

    def __create_log_path_as_needed(self, test_logpath):
        if not os.path.exists(test_logpath):
            try:
                os.makedirs(test_logpath)
            except Exception:
                pass  # Only reachable during multi-threaded runs

    def _process_dashboard_entry(self, has_exception, init=False):
        if self._multithreaded:
            self.dash_lock = fasteners.InterProcessLock(
                constants.Dashboard.LOCKFILE
            )
            with self.dash_lock:
                self.__process_dashboard(has_exception, init)
        else:
            self.__process_dashboard(has_exception, init)

    def __process_dashboard(self, has_exception, init=False):
        """SeleniumBase Dashboard Processing"""
        if self._multithreaded:
            existing_res = sb_config._results  # For recording "Skipped" tests
            abs_path = os.path.abspath(".")
            dash_json_loc = constants.Dashboard.DASH_JSON
            dash_jsonpath = os.path.join(abs_path, dash_json_loc)
            if not init and os.path.exists(dash_jsonpath):
                with open(dash_jsonpath, "r") as f:
                    dash_json = f.read().strip()
                dash_data, d_id, dash_rt, tlp, d_stats = json.loads(dash_json)
                num_passed, num_failed, num_skipped, num_untested = d_stats
                sb_config._results = dash_data
                sb_config._display_id = d_id
                sb_config._duration = dash_rt  # Dashboard Run Time
                sb_config._d_t_log_path = tlp  # Test Log Path
                sb_config.item_count_passed = num_passed
                sb_config.item_count_failed = num_failed
                sb_config.item_count_skipped = num_skipped
                sb_config.item_count_untested = num_untested
        if len(sb_config._extra_dash_entries) > 0:
            # First take care of existing entries from non-SeleniumBase tests
            for test_id in sb_config._extra_dash_entries:
                if test_id in sb_config._results.keys():
                    if sb_config._results[test_id] == "Skipped":
                        sb_config.item_count_skipped += 1
                        sb_config.item_count_untested -= 1
                    elif sb_config._results[test_id] == "Failed":
                        sb_config.item_count_failed += 1
                        sb_config.item_count_untested -= 1
                    elif sb_config._results[test_id] == "Passed":
                        sb_config.item_count_passed += 1
                        sb_config.item_count_untested -= 1
                    else:  # Mark "Skipped" if unknown
                        sb_config.item_count_skipped += 1
                        sb_config.item_count_untested -= 1
            sb_config._extra_dash_entries = []  # Reset the list to empty
        # Process new entries
        log_dir = self.log_path
        ft_id = self.__get_test_id()  # Full test id with path to log files
        test_id = self.__get_test_id_2()  # The test id used by the DashBoard
        dud = "seleniumbase/plugins/pytest_plugin.py::BaseClass::base_method"
        dud2 = "pytest_plugin.BaseClass.base_method"
        if hasattr(self, "_using_sb_fixture") and self.__will_be_skipped:
            test_id = sb_config._test_id
        if not init:
            duration_ms = int(time.time() * 1000.0) - self.__start_time_ms
            duration = float(duration_ms) / 1000.0
            duration = "{:.2f}".format(duration)
            sb_config._duration[test_id] = duration
            if (
                has_exception
                or self.save_screenshot_after_test
                or self.__screenshot_count > 0
                or self.__level_0_visual_f
                or self.__will_be_skipped
            ):
                sb_config._d_t_log_path[test_id] = os.path.join(log_dir, ft_id)
            else:
                sb_config._d_t_log_path[test_id] = None
            if test_id not in sb_config._display_id.keys():
                sb_config._display_id[test_id] = self.__get_display_id()
            if sb_config._display_id[test_id] == dud:
                return
            if (
                hasattr(self, "_using_sb_fixture")
                and test_id not in sb_config._results.keys()
            ):
                if test_id.count(".") > 1:
                    alt_test_id = ".".join(test_id.split(".")[1:])
                    if alt_test_id in sb_config._results.keys():
                        sb_config._results.pop(alt_test_id)
                elif test_id.count(".") == 1:
                    alt_test_id = sb_config._display_id[test_id]
                    alt_test_id = alt_test_id.replace(".py::", ".")
                    alt_test_id = alt_test_id.replace("::", ".")
                    if alt_test_id in sb_config._results.keys():
                        sb_config._results.pop(alt_test_id)
            if test_id in sb_config._results.keys() and (
                sb_config._results[test_id] == "Skipped"
            ):
                if self.__passed_then_skipped:
                    # Multiple calls of setUp() and tearDown() in the same test
                    sb_config.item_count_passed -= 1
                    sb_config.item_count_untested += 1
                    self.__passed_then_skipped = False
                sb_config._results[test_id] = "Skipped"
                sb_config.item_count_skipped += 1
                sb_config.item_count_untested -= 1
            elif (
                self._multithreaded
                and test_id in existing_res.keys()
                and existing_res[test_id] == "Skipped"
            ):
                sb_config._results[test_id] = "Skipped"
                sb_config.item_count_skipped += 1
                sb_config.item_count_untested -= 1
            elif has_exception:
                if test_id not in sb_config._results.keys():
                    sb_config._results[test_id] = "Failed"
                    sb_config.item_count_failed += 1
                    sb_config.item_count_untested -= 1
                elif not sb_config._results[test_id] == "Failed":
                    # tearDown() was called more than once in the test
                    if sb_config._results[test_id] == "Passed":
                        # Passed earlier, but last run failed
                        sb_config._results[test_id] = "Failed"
                        sb_config.item_count_failed += 1
                        sb_config.item_count_passed -= 1
                    else:
                        sb_config._results[test_id] = "Failed"
                        sb_config.item_count_failed += 1
                        sb_config.item_count_untested -= 1
                else:
                    # pytest-rerunfailures caused a duplicate failure
                    sb_config._results[test_id] = "Failed"
            else:
                if (
                    test_id in sb_config._results.keys()
                    and sb_config._results[test_id] == "Failed"
                ):
                    # pytest-rerunfailures reran a test that failed
                    sb_config._d_t_log_path[test_id] = os.path.join(
                        log_dir, ft_id
                    )
                    sb_config.item_count_failed -= 1
                    sb_config.item_count_untested += 1
                elif (
                    test_id in sb_config._results.keys()
                    and sb_config._results[test_id] == "Passed"
                ):
                    # tearDown() was called more than once in the test
                    sb_config.item_count_passed -= 1
                    sb_config.item_count_untested += 1
                sb_config._results[test_id] = "Passed"
                sb_config.item_count_passed += 1
                sb_config.item_count_untested -= 1
        else:
            pass  # Only initialize the Dashboard on the first processing
        num_passed = sb_config.item_count_passed
        num_failed = sb_config.item_count_failed
        num_skipped = sb_config.item_count_skipped
        num_untested = sb_config.item_count_untested
        self.create_pie_chart(title=constants.Dashboard.TITLE)
        self.add_data_point("Passed", num_passed, color="#84d474")
        self.add_data_point("Untested", num_untested, color="#eaeaea")
        self.add_data_point("Skipped", num_skipped, color="#efd8b4")
        self.add_data_point("Failed", num_failed, color="#f17476")
        style = (
            '<link rel="stylesheet" charset="utf-8" '
            'href="%s">' % constants.Dashboard.STYLE_CSS
        )
        auto_refresh_html = ""
        if num_untested > 0:
            # Refresh every X seconds when waiting for more test results
            auto_refresh_html = constants.Dashboard.META_REFRESH_HTML
        else:
            # The tests are complete
            if sb_config._using_html_report:
                # Add the pie chart to the pytest html report
                sb_config._saved_dashboard_pie = self.extract_chart()
                if self._multithreaded:
                    abs_path = os.path.abspath(".")
                    dash_pie = json.dumps(sb_config._saved_dashboard_pie)
                    dash_pie_loc = constants.Dashboard.DASH_PIE
                    pie_path = os.path.join(abs_path, dash_pie_loc)
                    pie_file = codecs.open(pie_path, "w+", encoding="utf-8")
                    pie_file.writelines(dash_pie)
                    pie_file.close()
        if python3:
            DASH_PIE_PNG_1 = constants.Dashboard.get_dash_pie_1()
        else:
            from seleniumbase.core import encoded_images

            DASH_PIE_PNG_1 = encoded_images.get_dash_pie_png1()
        head = (
            '<head><meta charset="utf-8">'
            '<meta name="viewport" content="shrink-to-fit=no">'
            '<link rel="shortcut icon" href="%s">'
            "%s"
            "<title>Dashboard</title>"
            "%s</head>"
            % (DASH_PIE_PNG_1, auto_refresh_html, style)
        )
        table_html = (
            "<div></div>"
            '<table border="1px solid #e6e6e6;" width="100%;" padding: 5px;'
            ' font-size="12px;" text-align="left;" id="results-table">'
            '<thead id="results-table-head">'
            '<tr style="background-color: #F7F7FD;">'
            '<th col="result">Result</th><th col="name">Test</th>'
            '<th col="duration">Duration</th><th col="links">Links</th>'
            "</tr></thead>"
        )
        the_failed = []
        the_skipped = []
        the_passed_hl = []  # Passed and has logs
        the_passed_nl = []  # Passed and no logs
        the_untested = []
        if dud2 in sb_config._results.keys():
            sb_config._results.pop(dud2)
        for key in sb_config._results.keys():
            t_res = sb_config._results[key]
            t_dur = sb_config._duration[key]
            t_d_id = sb_config._display_id[key]
            t_l_path = sb_config._d_t_log_path[key]
            res_low = t_res.lower()
            if sb_config._results[key] == "Failed":
                if not sb_config._d_t_log_path[key]:
                    sb_config._d_t_log_path[key] = os.path.join(log_dir, ft_id)
                the_failed.append([res_low, t_res, t_d_id, t_dur, t_l_path])
            elif sb_config._results[key] == "Skipped":
                the_skipped.append([res_low, t_res, t_d_id, t_dur, t_l_path])
            elif sb_config._results[key] == "Passed" and t_l_path:
                the_passed_hl.append([res_low, t_res, t_d_id, t_dur, t_l_path])
            elif sb_config._results[key] == "Passed" and not t_l_path:
                the_passed_nl.append([res_low, t_res, t_d_id, t_dur, t_l_path])
            elif sb_config._results[key] == "Untested":
                the_untested.append([res_low, t_res, t_d_id, t_dur, t_l_path])
        for row in the_failed:
            row = (
                '<tbody class="%s results-table-row">'
                '<tr style="background-color: #FFF8F8;">'
                '<td class="col-result">%s</td><td>%s</td><td>%s</td>'
                '<td><a href="%s">Logs</a> / <a href="%s/">Data</a>'
                "</td></tr></tbody>"
                "" % (row[0], row[1], row[2], row[3], log_dir, row[4])
            )
            table_html += row
        for row in the_skipped:
            if not row[4]:
                row = (
                    '<tbody class="%s results-table-row">'
                    '<tr style="background-color: #FEFEF9;">'
                    '<td class="col-result">%s</td><td>%s</td><td>%s</td>'
                    "<td>-</td></tr></tbody>"
                    % (row[0], row[1], row[2], row[3])
                )
            else:
                row = (
                    '<tbody class="%s results-table-row">'
                    '<tr style="background-color: #FEFEF9;">'
                    '<td class="col-result">%s</td><td>%s</td><td>%s</td>'
                    '<td><a href="%s">Logs</a> / <a href="%s/">Data</a>'
                    "</td></tr></tbody>"
                    "" % (row[0], row[1], row[2], row[3], log_dir, row[4])
                )
            table_html += row
        for row in the_passed_hl:
            # Passed and has logs
            row = (
                '<tbody class="%s results-table-row">'
                '<tr style="background-color: #F8FFF8;">'
                '<td class="col-result">%s</td><td>%s</td><td>%s</td>'
                '<td><a href="%s">Logs</a> / <a href="%s/">Data</a>'
                "</td></tr></tbody>"
                "" % (row[0], row[1], row[2], row[3], log_dir, row[4])
            )
            table_html += row
        for row in the_passed_nl:
            # Passed and no logs
            row = (
                '<tbody class="%s results-table-row">'
                '<tr style="background-color: #F8FFF8;">'
                '<td class="col-result">%s</td><td>%s</td><td>%s</td>'
                "<td>-</td></tr></tbody>" % (row[0], row[1], row[2], row[3])
            )
            table_html += row
        for row in the_untested:
            row = (
                '<tbody class="%s results-table-row"><tr>'
                '<td class="col-result">%s</td><td>%s</td><td>%s</td>'
                "<td>-</td></tr></tbody>" % (row[0], row[1], row[2], row[3])
            )
            table_html += row
        table_html += "</table>"
        add_more = "<br /><b>Last updated:</b> "
        timestamp, the_date, the_time = log_helper.get_master_time()
        last_updated = "%s at %s" % (the_date, the_time)
        add_more = add_more + "%s" % last_updated
        status = "<p></p><div><b>Status:</b> Awaiting results..."
        status += " (Refresh the page for updates)"
        if num_untested == 0:
            status = "<p></p><div><b>Status:</b> Test Run Complete:"
            if num_failed == 0:
                if num_passed > 0:
                    if num_skipped == 0:
                        status += " <b>Success!</b> (All tests passed)"
                    else:
                        status += " <b>Success!</b> (No failing tests)"
                else:
                    status += " All tests were skipped!"
            else:
                latest_logs_dir = "latest_logs/"
                log_msg = "See latest logs for details"
                if num_failed == 1:
                    status += (
                        " <b>1 test failed!</b> --- "
                        '(<b><a href="%s">%s</a></b>)'
                        "" % (latest_logs_dir, log_msg)
                    )
                else:
                    status += (
                        " <b>%s tests failed!</b> --- "
                        '(<b><a href="%s">%s</a></b>)'
                        "" % (num_failed, latest_logs_dir, log_msg)
                    )
        status += "</div><p></p>"
        add_more = add_more + status
        gen_by = (
            '<p><div>Generated by: <b><a href="https://seleniumbase.io/">'
            "SeleniumBase</a></b></div></p><p></p>"
        )
        add_more = add_more + gen_by
        # Have dashboard auto-refresh on updates when using an http server
        refresh_line = (
            '<script type="text/javascript" src="%s">'
            "</script>" % constants.Dashboard.LIVE_JS
        )
        if num_untested == 0 and sb_config._using_html_report:
            sb_config._dash_final_summary = status
        add_more = add_more + refresh_line
        the_html = (
            '<html lang="en">'
            + head
            + self.extract_chart()
            + table_html
            + add_more
        )
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, "dashboard.html")
        out_file = codecs.open(file_path, "w+", encoding="utf-8")
        out_file.writelines(the_html)
        out_file.close()
        sb_config._dash_html = the_html
        if self._multithreaded:
            d_stats = (num_passed, num_failed, num_skipped, num_untested)
            _results = sb_config._results
            _display_id = sb_config._display_id
            _rt = sb_config._duration  # Run Time (RT)
            _tlp = sb_config._d_t_log_path  # Test Log Path (TLP)
            dash_json = json.dumps((_results, _display_id, _rt, _tlp, d_stats))
            dash_json_loc = constants.Dashboard.DASH_JSON
            dash_jsonpath = os.path.join(abs_path, dash_json_loc)
            dash_json_file = codecs.open(dash_jsonpath, "w+", encoding="utf-8")
            dash_json_file.writelines(dash_json)
            dash_json_file.close()

    def __activate_behave_post_mortem_debug_mode(self):
        """Activate Post Mortem Debug Mode for failing tests that use Behave"""
        import pdb

        pdb.post_mortem(sb_config.behave_step.exc_traceback)
        # Post Mortem Debug Mode ("behave -D pdb")

    def __activate_debug_mode_in_teardown(self):
        """Activate Debug Mode in tearDown() when using "--final-debug"."""
        import pdb

        pdb.set_trace()
        # Final Debug Mode ("--final-debug")

    def has_exception(self):
        """(This method should ONLY be used in custom tearDown() methods.)
        This method returns True if the test failed or raised an exception.
        This is useful for performing additional steps in your tearDown()
        method (based on whether or not the test passed or failed).
        Example use cases:
            * Performing cleanup steps if a test didn't complete.
            * Sending test data and/or results to a dashboard service.
        """
        return self.__has_exception()

    def save_teardown_screenshot(self):
        """(Should ONLY be used at the start of custom tearDown() methods.)
        This method takes a screenshot of the active page for FAILING tests
        (or when using "--screenshot" / "--save-screenshot" / "--ss").
        That way your tearDown() method can navigate away from the last
        page where the test failed, and still get the correct screenshot
        before performing tearDown() steps on other pages. If this method
        is not included in your custom tearDown() method, a screenshot
        will still be taken after the last step of your tearDown(), where
        you should be calling "super(SubClassOfBaseCase, self).tearDown()"
        or "super().tearDown()".
        This method also saves recorded actions when using Recorder Mode.
        """
        try:
            self.__check_scope()
        except Exception:
            return
        if self.recorder_mode:
            # In case tearDown() leaves the origin, save actions first.
            self.save_recorded_actions()
        if (
            self.__has_exception()
            or self.save_screenshot_after_test
            or sys.version_info >= (3, 11)
        ):
            self.__set_last_page_screenshot()
            self.__set_last_page_url()
            self.__set_last_page_source()
            if self.__has_exception() or self.save_screenshot_after_test:
                if self.is_pytest:
                    self.__add_pytest_html_extra()

    def _log_fail_data(self):
        if sys.version_info < (3, 11):
            return
        test_id = self.__get_test_id()
        test_logpath = os.path.join(self.log_path, test_id)
        log_helper.log_test_failure_data(
            self,
            test_logpath,
            self.driver,
            self.browser,
            self.__last_page_url,
        )

    def _get_browser_version(self):
        driver_capabilities = None
        if hasattr(self, "driver") and hasattr(self.driver, "capabilities"):
            driver_capabilities = self.driver.capabilities
        elif hasattr(sb_config, "_browser_version"):
            return sb_config._browser_version
        else:
            return "(Unknown Version)"
        if "version" in driver_capabilities:
            browser_version = driver_capabilities["version"]
        else:
            browser_version = driver_capabilities["browserVersion"]
        return browser_version

    def _get_driver_name_and_version(self):
        if not hasattr(self.driver, "capabilities"):
            if hasattr(sb_config, "_driver_name_version"):
                return sb_config._driver_name_version
            else:
                return None
        driver = self.driver
        if driver.capabilities["browserName"].lower() == "chrome":
            cap_dict = driver.capabilities["chrome"]
            return (
                "chromedriver", cap_dict["chromedriverVersion"].split(" ")[0]
            )
        elif driver.capabilities["browserName"].lower() == "msedge":
            cap_dict = driver.capabilities["msedge"]
            return (
                "msedgedriver", cap_dict["msedgedriverVersion"].split(" ")[0]
            )
        elif driver.capabilities["browserName"].lower() == "opera":
            cap_dict = driver.capabilities["opera"]
            return (
                "operadriver", cap_dict["operadriverVersion"].split(" ")[0]
            )
        elif driver.capabilities["browserName"].lower() == "firefox":
            return (
                "geckodriver", driver.capabilities["moz:geckodriverVersion"]
            )
        elif self.browser == "safari":
            return ("safaridriver", self._get_browser_version())
        elif self.browser == "ie":
            return ("iedriver", self._get_browser_version())
        else:
            return None

    def tearDown(self):
        """
        Be careful if a subclass of BaseCase overrides setUp()
        You'll need to add the following line to the subclass's tearDown():
        super(SubClassOfBaseCase, self).tearDown()
        """
        if not hasattr(self, "_using_sb_fixture") and self.__called_teardown:
            # This test already called tearDown()
            return
        if self.recorder_mode:
            self.__process_recorded_actions()
        self.__called_teardown = True
        self.__called_setup = False
        try:
            is_pytest = self.is_pytest  # This fails if overriding setUp()
            if is_pytest:
                with_selenium = self.with_selenium
        except Exception:
            sub_class_name = (
                str(self.__class__.__bases__[0]).split(".")[-1].split("'")[0]
            )
            sub_file_name = str(self.__class__.__bases__[0]).split(".")[-2]
            sub_file_name = sub_file_name + ".py"
            class_name = str(self.__class__).split(".")[-1].split("'")[0]
            file_name = str(self.__class__).split(".")[-2] + ".py"
            class_name_used = sub_class_name
            file_name_used = sub_file_name
            if sub_class_name == "BaseCase":
                class_name_used = class_name
                file_name_used = file_name
            fix_setup = "super(%s, self).setUp()" % class_name_used
            fix_teardown = "super(%s, self).tearDown()" % class_name_used
            message = (
                "You're overriding SeleniumBase's BaseCase setUp() "
                "method with your own setUp() method, which breaks "
                "SeleniumBase. You can fix this by going to your "
                "%s class located in your %s file and adding the "
                "following line of code AT THE BEGINNING of your "
                "setUp() method:\n%s\n\nAlso make sure "
                "you have added the following line of code AT THE "
                "END of your tearDown() method:\n%s\n"
                % (class_name_used, file_name_used, fix_setup, fix_teardown)
            )
            raise Exception(message)
        # *** Start tearDown() officially ***
        self.__slow_mode_pause_if_active()
        has_exception = self.__has_exception()
        sb_config._has_exception = has_exception
        sb_config._browser_version = self._get_browser_version()
        sb_config._driver_name_version = self._get_driver_name_and_version()

        if self.__overrided_default_timeouts:
            # Reset default timeouts in case there are more tests
            # These were changed in set_default_timeout()
            if sb_config._SMALL_TIMEOUT and sb_config._LARGE_TIMEOUT:
                settings.SMALL_TIMEOUT = sb_config._SMALL_TIMEOUT
                settings.LARGE_TIMEOUT = sb_config._LARGE_TIMEOUT
                sb_config._is_timeout_changed = False
                self.__overrided_default_timeouts = False
        deferred_exception = None
        if self.__deferred_assert_failures:
            print(
                "\nWhen using self.deferred_assert_*() methods in your tests, "
                "remember to call self.process_deferred_asserts() afterwards. "
                "Now calling in tearDown()...\nFailures Detected:"
            )
            if not has_exception:
                try:
                    self.process_deferred_asserts()
                except Exception as e:
                    deferred_exception = e
            else:
                self.process_deferred_asserts(print_only=True)
        if self.is_pytest:
            # pytest-specific code
            test_id = self.__get_test_id()
            if with_selenium:
                # Save a screenshot if logging is on when an exception occurs
                if has_exception:
                    self.__add_pytest_html_extra()
                    sb_config._has_exception = True
                    sb_config._has_logs = True
                if (
                    self.with_testing_base
                    and not has_exception
                    and self.save_screenshot_after_test
                ):
                    test_logpath = os.path.join(self.log_path, test_id)
                    self.__create_log_path_as_needed(test_logpath)
                    if not self.__last_page_screenshot_png:
                        self.__set_last_page_screenshot()
                        self.__set_last_page_url()
                        self.__set_last_page_source()
                    log_helper.log_screenshot(
                        test_logpath,
                        self.driver,
                        self.__last_page_screenshot_png,
                    )
                    self.__add_pytest_html_extra()
                    sb_config._has_logs = True
                elif sys.version_info >= (3, 11) and not has_exception:
                    # Handle a bug on Python 3.11 where exceptions aren't seen
                    self.__set_last_page_screenshot()
                    self.__set_last_page_url()
                    self.__set_last_page_source()
                if self.with_testing_base and has_exception:
                    test_logpath = os.path.join(self.log_path, test_id)
                    self.__create_log_path_as_needed(test_logpath)
                    if (
                        not self.with_screen_shots
                        and not self.with_basic_test_info
                        and not self.with_page_source
                    ):
                        # Log everything if nothing specified (if testing_base)
                        if not self.__last_page_screenshot_png:
                            self.__set_last_page_screenshot()
                            self.__set_last_page_url()
                            self.__set_last_page_source()
                        log_helper.log_screenshot(
                            test_logpath,
                            self.driver,
                            self.__last_page_screenshot_png,
                        )
                        log_helper.log_test_failure_data(
                            self,
                            test_logpath,
                            self.driver,
                            self.browser,
                            self.__last_page_url,
                        )
                        log_helper.log_page_source(
                            test_logpath, self.driver, self.__last_page_source
                        )
                    else:
                        if self.with_screen_shots:
                            if not self.__last_page_screenshot_png:
                                self.__set_last_page_screenshot()
                                self.__set_last_page_url()
                                self.__set_last_page_source()
                            log_helper.log_screenshot(
                                test_logpath,
                                self.driver,
                                self.__last_page_screenshot_png,
                            )
                        if self.with_basic_test_info:
                            log_helper.log_test_failure_data(
                                self,
                                test_logpath,
                                self.driver,
                                self.browser,
                                self.__last_page_url,
                            )
                        if self.with_page_source:
                            log_helper.log_page_source(
                                test_logpath,
                                self.driver,
                                self.__last_page_source,
                            )
                if self.dashboard:
                    if self._multithreaded:
                        with self.dash_lock:
                            self.__process_dashboard(has_exception)
                    else:
                        self.__process_dashboard(has_exception)
                if self._final_debug:
                    self.__activate_debug_mode_in_teardown()
                # (Pytest) Finally close all open browser windows
                self.__quit_all_drivers()
            if self.headless or self.headless2 or self.xvfb:
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
                    self.__insert_test_result(constants.State.FAILED, True)
                else:
                    test_id = self.__get_test_id_2()
                    if test_id in sb_config._results.keys() and (
                        sb_config._results[test_id] == "Skipped"
                    ):
                        self.__insert_test_result(
                            constants.State.SKIPPED, False
                        )
                    else:
                        self.__insert_test_result(
                            constants.State.PASSED, False
                        )
                runtime = int(time.time() * 1000.0) - self.execution_start_time
                self.testcase_manager.update_execution_data(
                    self.execution_guid, runtime
                )
            if self.with_s3_logging and has_exception:
                """If enabled, upload logs to S3 during test exceptions."""
                import uuid
                from seleniumbase.core.s3_manager import S3LoggingBucket

                s3_bucket = S3LoggingBucket()
                guid = str(uuid.uuid4().hex)
                path = os.path.join(self.log_path, test_id)
                uploaded_files = []
                for logfile in os.listdir(path):
                    logfile_name = "%s/%s/%s" % (
                        guid,
                        test_id,
                        logfile.split(path)[-1],
                    )
                    s3_bucket.upload_file(
                        logfile_name, "%s" % os.path.join(path, logfile)
                    )
                    uploaded_files.append(logfile_name)
                s3_bucket.save_uploaded_file_names(uploaded_files)
                index_file = s3_bucket.upload_index_file(test_id, guid)
                print("\n\n*** Log files uploaded: ***\n%s\n" % index_file)
                logging.info(
                    "\n\n*** Log files uploaded: ***\n%s\n" % index_file
                )
                if self.with_db_reporting:
                    from seleniumbase.core.testcase_manager import (
                        TestcaseDataPayload,
                    )
                    from seleniumbase.core.testcase_manager import (
                        TestcaseManager,
                    )

                    self.testcase_manager = TestcaseManager(self.database_env)
                    data_payload = TestcaseDataPayload()
                    data_payload.guid = self.testcase_guid
                    data_payload.logURL = index_file
                    self.testcase_manager.update_testcase_log_url(data_payload)
        else:
            # (Nosetests / Behave / Pure Python)
            if hasattr(self, "is_behave") and self.is_behave:
                import colorama

                if sb_config.behave_scenario.status.name == "failed":
                    has_exception = True
                    sb_config._has_exception = True
                    msg = "   ❌ Scenario Failed!  (Skipping remaining steps:)"
                    if is_windows:
                        c1 = colorama.Fore.RED + colorama.Back.LIGHTRED_EX
                        cr = colorama.Style.RESET_ALL
                        colorama.init(autoreset=True)
                        msg = msg.replace("❌", c1 + "><" + cr)
                    print(msg)
                else:
                    msg = "   ✅ Scenario Passed!"
                    if is_windows:
                        c2 = colorama.Fore.GREEN + colorama.Back.LIGHTGREEN_EX
                        cr = colorama.Style.RESET_ALL
                        colorama.init(autoreset=True)
                        msg = msg.replace("✅", c2 + "<>" + cr)
                    print(msg)
                if self.dashboard:
                    self.__process_dashboard(has_exception)
                if self.headless or self.headless2 or self.xvfb:
                    if self.headless_active:
                        try:
                            self.display.stop()
                        except AttributeError:
                            pass
                        except Exception:
                            pass
                        self.display = None
            if has_exception:
                test_id = self.__get_test_id()
                test_logpath = os.path.join(self.log_path, test_id)
                self.__create_log_path_as_needed(test_logpath)
                log_helper.log_test_failure_data(
                    self,
                    test_logpath,
                    self.driver,
                    self.browser,
                    self.__last_page_url,
                )
                if len(self._drivers_list) > 0:
                    if not self.__last_page_screenshot_png:
                        self.__set_last_page_screenshot()
                        self.__set_last_page_url()
                        self.__set_last_page_source()
                    log_helper.log_screenshot(
                        test_logpath,
                        self.driver,
                        self.__last_page_screenshot_png,
                    )
                    log_helper.log_page_source(
                        test_logpath, self.driver, self.__last_page_source
                    )
            elif self.save_screenshot_after_test:
                test_id = self.__get_test_id()
                test_logpath = os.path.join(self.log_path, test_id)
                self.__create_log_path_as_needed(test_logpath)
                if not self.__last_page_screenshot_png:
                    self.__set_last_page_screenshot()
                    self.__set_last_page_url()
                    self.__set_last_page_source()
                log_helper.log_screenshot(
                    test_logpath, self.driver, self.__last_page_screenshot_png
                )
            if self.report_on:
                self._last_page_screenshot = self.__last_page_screenshot_png
                try:
                    self._last_page_url = self.get_current_url()
                except Exception:
                    self._last_page_url = "(Error: Unknown URL)"
            if hasattr(self, "is_behave") and self.is_behave and has_exception:
                if hasattr(sb_config, "pdb_option") and sb_config.pdb_option:
                    self.__activate_behave_post_mortem_debug_mode()
            if self._final_debug:
                self.__activate_debug_mode_in_teardown()
            # (Nosetests / Behave / Pure Python) Close all open browser windows
            self.__quit_all_drivers()
        # Resume tearDown() for all test runners, (Pytest / Nosetests / Behave)
        if self.__visual_baseline_copies:
            sb_config._visual_baseline_copies = True
            if has_exception:
                self.__process_visual_baseline_logs()
        if deferred_exception:
            # User forgot to call "self.process_deferred_asserts()" in test
            raise deferred_exception


r"""----------------------------------------------------------------->
|    ______     __           _                  ____                 |
|   / ____/__  / /__  ____  (_)_  ______ ___   / _  \____  ________  |
|   \__ \/ _ \/ / _ \/ __ \/ / / / / __ `__ \ / /_) / __ \/ ___/ _ \ |
|  ___/ /  __/ /  __/ / / / / /_/ / / / / / // /_) / (_/ /__  /  __/ |
| /____/\___/_/\___/_/ /_/_/\__,_/_/ /_/ /_//_____/\__,_/____/\___/  |
|                                                                    |
------------------------------------------------------------------>"""
