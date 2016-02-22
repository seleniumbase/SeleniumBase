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
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import page_actions
import page_utils


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
        self._demo_mode_scroll_if_active(selector, by)
        element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        self._demo_mode_pause_if_active()

    def click_chain(self, selectors_list, by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT, spacing=0):
        """ This method clicks on a list of elements in succession.
            'spacing' is the amount of time to wait between clicks. (sec) """
        for selector in selectors_list:
            self.click(selector, by=by, timeout=timeout)
            if spacing > 0:
                time.sleep(spacing)

    def click_link_text(self, link_text, timeout=settings.SMALL_TIMEOUT):
        element = self.wait_for_link_text_visible(link_text, timeout=timeout)
        element.click()
        if settings.WAIT_FOR_RSC_ON_CLICKS:
            self.wait_for_ready_state_complete()
        self._demo_mode_pause_if_active()

    def add_text(self, selector, new_value, timeout=settings.SMALL_TIMEOUT):
        """ The more-reliable version of driver.send_keys()
            Similar to update_text(), but won't clear the text field first. """
        element = self.wait_for_element_visible(selector, timeout=timeout)
        element.send_keys(new_value)
        self._demo_mode_pause_if_active()

    def send_keys(self, selector, new_value, timeout=settings.SMALL_TIMEOUT):
        """ Same as add_text() -> more reliable, but less name confusion. """
        self.add_text(selector, new_value, timeout=timeout)

    def update_text_value(self, selector, new_value,
                          timeout=settings.SMALL_TIMEOUT, retry=False):
        """ This method updates an element's text value with a new value.
            @Params
            selector - the selector with the value to update
            new_value - the new value for setting the text field
            timeout - how long to wait for the selector to be visible
            retry - if True, use jquery if the selenium text update fails
        """
        element = self.wait_for_element_visible(selector, timeout=timeout)
        element.clear()
        self._demo_mode_pause_if_active(tiny=True)
        element.send_keys(new_value)
        if (retry and element.get_attribute('value') != new_value and (
                not new_value.endswith('\n'))):
            logging.debug('update_text_value is falling back to jQuery!')
            selector = self.jq_format(selector)
            self.set_value(selector, new_value)
        self._demo_mode_pause_if_active()

    def update_text(self, selector, new_value,
                    timeout=settings.SMALL_TIMEOUT, retry=False):
        """ The shorter version of update_text_value(), which
            clears existing text and adds new text into the text field.
            We want to keep the old version for backward compatibility. """
        self.update_text_value(selector, new_value,
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
            self.driver.execute_script("jQuery('html')")
            # Since that command worked, jQuery is defined. Let's return.
            return
        except Exception:
            # jQuery is not currently defined. Let's proceed by defining it.
            pass
        self.driver.execute_script(
            '''var script = document.createElement("script"); '''
            '''script.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/'''
            '''jquery.min.js"; document.getElementsByTagName("head")[0]'''
            '''.appendChild(script);''')
        for x in xrange(30):
            # jQuery needs a small amount of time to activate. (At most 3s)
            try:
                self.driver.execute_script("jQuery('html')")
                return
            except Exception:
                time.sleep(0.1)
        # Since jQuery still isn't activating, give up and raise an exception
        raise Exception("Exception: WebDriver could not activate jQuery!")

    def scroll_to(self, selector, wait=True):
        if wait:
            # Fail here if element isn't visible after SMALL_TIMEOUT seconds
            self.wait_for_element_visible(
                selector, timeout=settings.SMALL_TIMEOUT)
        else:
            # Might be a jQuery action to interact with an invisible element
            if not self.is_element_visible:
                time.sleep(0.05)  # Last chance to load before scrolling there
        scroll_script = "jQuery('%s')[0].scrollIntoView()" % selector
        try:
            self.driver.execute_script(scroll_script)
        except Exception:
            # The likely reason this fails is because: "jQuery is not defined"
            self.activate_jquery()  # It's a good thing we can define it here
            self.driver.execute_script(scroll_script)
        self._demo_mode_pause_if_active(tiny=True)

    def scroll_click(self, selector):
        self.scroll_to(selector)
        self.click(selector)

    def jquery_click(self, selector, wait=False):
        self.scroll_to(selector, wait=wait)
        self.driver.execute_script("jQuery('%s').click()" % selector)
        self._demo_mode_pause_if_active()

    def jq_format(self, code):
        return page_utils.jq_format(code)

    def set_value(self, selector, value, wait=False):
        self.scroll_to(selector, wait=wait)
        val = json.dumps(value)
        self.driver.execute_script("jQuery('%s').val(%s)" % (selector, val))
        self._demo_mode_pause_if_active()

    def jquery_update_text_value(self, selector, new_value,
                                 timeout=settings.SMALL_TIMEOUT):
        element = self.wait_for_element_visible(selector, timeout=timeout)
        self.scroll_to(selector)
        self.driver.execute_script("""jQuery('%s').val('%s')"""
                                   % (selector, self.jq_format(new_value)))
        if new_value.endswith('\n'):
            element.send_keys('\n')
        self._demo_mode_pause_if_active()

    def jquery_update_text(self, selector, new_value,
                           timeout=settings.SMALL_TIMEOUT):
        self.jquery_update_text_value(selector, new_value, timeout=timeout)

    def hover_on_element(self, selector):
        self.wait_for_element_visible(selector, timeout=settings.SMALL_TIMEOUT)
        self.scroll_to(selector)
        time.sleep(0.05)  # Settle down from scrolling before hovering
        return page_actions.hover_on_element(self.driver, selector)

    def hover_and_click(self, hover_selector, click_selector,
                        click_by=By.CSS_SELECTOR,
                        timeout=settings.SMALL_TIMEOUT):
        if click_selector.startswith('/'):
            click_by = By.XPATH
        self.wait_for_element_visible(hover_selector, timeout=timeout)
        self.scroll_to(hover_selector)
        # Settle down from the scrolling before hovering
        element = page_actions.hover_and_click(
            self.driver, hover_selector, click_selector, click_by, timeout)
        self._demo_mode_pause_if_active()
        return element

    def wait_for_element_present(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_element_present(
            self.driver, selector, by, timeout)

    def wait_for_element_visible(self, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_element_visible(
            self.driver, selector, by, timeout)

    def wait_for_element(self, selector, by=By.CSS_SELECTOR,
                         timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_element_visible() """
        return self.wait_for_element_visible(selector, by=by, timeout=timeout)

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

    def wait_for_link_text_visible(self, link_text,
                                   timeout=settings.LARGE_TIMEOUT):
        return self.wait_for_element_visible(
            link_text, by=By.LINK_TEXT, timeout=timeout)

    def wait_for_link_text(self, link_text, timeout=settings.LARGE_TIMEOUT):
        """ The shorter version of wait_for_link_text_visible() """
        return self.wait_for_link_text_visible(link_text, timeout=timeout)

    def wait_for_element_absent(self, selector, by=By.CSS_SELECTOR,
                                timeout=settings.LARGE_TIMEOUT):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
        return page_actions.wait_for_element_absent(
            self.driver, selector, by, timeout)

    def wait_for_element_not_visible(self, selector, by=By.CSS_SELECTOR,
                                     timeout=settings.LARGE_TIMEOUT):
        if selector.startswith('/') or selector.startswith('./'):
            by = By.XPATH
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

    def save_screenshot(self, name, folder=None):
        return page_actions.save_screenshot(self.driver, name, folder)

    def _demo_mode_pause_if_active(self, tiny=False):
        if self.demo_mode:
            if self.demo_sleep:
                wait_time = float(self.demo_sleep)
            else:
                wait_time = settings.DEFAULT_DEMO_MODE_TIMEOUT
            if not tiny:
                time.sleep(wait_time)
            else:
                time.sleep(wait_time/3.0)

    def _demo_mode_scroll_if_active(self, selector, by):
        if self.demo_mode:
            if by == By.CSS_SELECTOR:
                self.scroll_to(selector)


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
                print "\n\n*** Log files uploaded: ***\n%s\n" % index_file
                logging.error(
                    "\n\n*** Log files uploaded: ***\n%s\n" % index_file)
                if self.with_db_reporting:
                    self.testcase_manager = TestcaseManager(self.database_env)
                    data_payload = TestcaseDataPayload()
                    data_payload.guid = self.testcase_guid
                    data_payload.logURL = index_file
                    self.testcase_manager.update_testcase_log_url(data_payload)
