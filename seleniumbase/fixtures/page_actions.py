"""
This module contains a set of methods that can be used for page loads and
for waiting for elements to appear on a page.

These methods improve on and expand existing WebDriver commands.
Improvements include making WebDriver commands more robust and more reliable
by giving page elements enough time to load before taking action on them.

The default option for searching for elements is by CSS Selector.
This can be changed by overriding the "By" parameter.
Options are:
By.CSS_SELECTOR
By.CLASS_NAME
By.ID
By.NAME
By.LINK_TEXT
By.XPATH
By.TAG_NAME
By.PARTIAL_LINK_TEXT
"""

import codecs
import os
import sys
import time
import traceback
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from selenium.webdriver.remote.errorhandler import NoAlertPresentException
from selenium.webdriver.remote.errorhandler import NoSuchFrameException
from selenium.webdriver.remote.errorhandler import NoSuchWindowException
from seleniumbase.config import settings


def is_element_present(driver, selector, by=By.CSS_SELECTOR):
    """
    Searches for the specified element by the given selector.  Returns whether
    the element object if the element is present on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is element present)
    """
    try:
        driver.find_element(by=by, value=selector)
        return True
    except Exception:
        return False


def is_element_visible(driver, selector, by=By.CSS_SELECTOR):
    """
    Searches for the specified element by the given selector.  Returns whether
    the element object if the element is present and visible on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is element visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed()
    except Exception:
        return False


def is_text_visible(driver, text, selector, by=By.CSS_SELECTOR):
    """
    Searches for the specified element by the given selector. Returns whether
    the element object if the element is present and visible on the page and
    contains the given text.
    @Params
    driver - the webdriver object (required)
    text - the text string to search for
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is text visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed() and text in element.text
    except Exception:
        return False


def hover_on_element(driver, selector, by=By.CSS_SELECTOR):
    """
    Fires the hover event for the specified element by the given selector.
    @Params
    driver - the webdriver object (required)
    selector - the locator (css selector) that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    """
    element = driver.find_element(by=by, value=selector)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()


def hover_and_click(driver, hover_selector, click_selector,
                    hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT):
    """
    Fires the hover event for a specified element by a given selector, then
    clicks on another element specified. Useful for dropdown hover based menus.
    @Params
    driver - the webdriver object (required)
    hover_selector - the css selector to hover over (required)
    click_selector - the css selector to click on (required)
    hover_by - the method to search by (Default: By.CSS_SELECTOR)
    click_by - the method to search by (Default: By.CSS_SELECTOR)
    timeout - number of seconds to wait for click element to appear after hover
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    element = driver.find_element(by=hover_by, value=hover_selector)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=click_by,
                                          value="%s" % click_selector).click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise NoSuchElementException(
        "Element {%s} was not present after %s seconds!" %
        (click_selector, timeout))


def hover_element_and_click(driver, element, click_selector,
                            click_by=By.CSS_SELECTOR,
                            timeout=settings.SMALL_TIMEOUT):
    """
    Similar to hover_and_click(), but assumes top element is already found.
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=click_by,
                                          value="%s" % click_selector).click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise NoSuchElementException(
        "Element {%s} was not present after %s seconds!" %
        (click_selector, timeout))


def wait_for_element_present(driver, selector, by=By.CSS_SELECTOR,
                             timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the element is present on the page. The element can be
    invisible. Raises an exception if the element does not appear in the
    specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object
    """

    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    if not element:
        raise NoSuchElementException(
            "Element {%s} was not present after %s seconds!" % (
                selector, timeout))


def wait_for_element_visible(driver, selector, by=By.CSS_SELECTOR,
                             timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the element is present and visible on the page.
    Raises an exception if the element does not appear in the
    specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds

    @Returns
    A web element object
    """

    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element and by != By.LINK_TEXT:
        raise ElementNotVisibleException(
            "Element {%s} was not visible after %s second%s!" % (
                selector, timeout, plural))
    if not element and by == By.LINK_TEXT:
        raise ElementNotVisibleException(
            "Link text {%s} was not visible after %s second%s!" % (
                selector, timeout, plural))


def wait_for_text_visible(driver, text, selector, by=By.CSS_SELECTOR,
                          timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text is present in the element and visible
    on the page. Raises an exception if the text or element do not appear
    in the specified timeout.
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """

    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                if text in element.text:
                    return element
                else:
                    element = None
                    raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        raise ElementNotVisibleException(
            "Expected text {%s} for {%s} was not visible after %s second%s!" %
            (text, selector, timeout, plural))


def wait_for_element_absent(driver, selector, by=By.CSS_SELECTOR,
                            timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still present after the
    specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    """

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            driver.find_element(by=by, value=selector)
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        except Exception:
            return True
    plural = "s"
    if timeout == 1:
        plural = ""
    raise Exception("Element {%s} was still present after %s second%s!" %
                    (selector, timeout, plural))


def wait_for_element_not_visible(driver, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still visible after the
    specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    timeout - the time to wait for the element in seconds
    """

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
            else:
                return True
        except Exception:
            return True
    plural = "s"
    if timeout == 1:
        plural = ""
    raise Exception(
        "Element {%s} was still visible after %s second%s!" % (
            selector, timeout, plural))


def find_visible_elements(driver, selector, by=By.CSS_SELECTOR):
    """
    Finds all WebElements that match a selector and are visible.
    Similar to webdriver.find_elements.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used to search the DOM (required)
    by - the method to search for the locator (Default: By.CSS_SELECTOR)
    """
    elements = driver.find_elements(by=by, value=selector)
    return [element for element in elements if element.is_displayed()]


def save_screenshot(driver, name, folder=None):
    """
    Saves a screenshot to the current directory (or to a subfolder if provided)
    If the folder provided doesn't exist, it will get created.
    """
    if folder:
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        screenshot_file = "%s/%s" % (file_path, name)
    else:
        screenshot_file = name
    driver.get_screenshot_as_file(screenshot_file)


def _get_last_page(driver):
    try:
        last_page = driver.current_url
    except Exception:
        last_page = '[WARNING! Browser Not Open!]'
    if len(last_page) < 5:
        last_page = '[WARNING! Browser Not Open!]'
    return last_page


def save_test_failure_data(driver, name, browser_type, folder=None):
    """
    Saves failure data to the current directory (or to a subfolder if provided)
    If the folder provided doesn't exist, it will get created.
    """
    if folder:
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        failure_data_file_path = "%s/%s" % (file_path, name)
    else:
        failure_data_file_path = name
    failure_data_file = codecs.open(failure_data_file_path, "w+", "utf-8")
    last_page = _get_last_page(driver)
    data_to_save = []
    data_to_save.append("Last_Page: %s" % last_page)
    data_to_save.append("Browser: %s " % browser_type)
    data_to_save.append("Traceback: " + ''.join(
        traceback.format_exception(sys.exc_info()[0],
                                   sys.exc_info()[1],
                                   sys.exc_info()[2])))
    failure_data_file.writelines("\r\n".join(data_to_save))
    failure_data_file.close()


def wait_for_ready_state_complete(driver, timeout=settings.EXTREME_TIMEOUT):
    """
    The DOM (Document Object Model) has a property called "readyState".
    When the value of this becomes "complete", page resources are considered
    fully loaded (although AJAX and other loads might still be happening).
    This method will wait until document.readyState == "complete".
    """

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            ready_state = driver.execute_script("return document.readyState")
        except WebDriverException:
            # Bug fix for: [Permission denied to access property "document"]
            time.sleep(0.03)
            return True
        if ready_state == u'complete':
            time.sleep(0.01)  # Better be sure everything is done loading
            return True
        else:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise Exception(
        "Page elements never fully loaded after %s seconds!" % timeout)


def wait_for_and_accept_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for and accept an alert. Returns the text from the alert.
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    alert = wait_for_and_switch_to_alert(driver, timeout)
    alert_text = alert.text
    alert.accept()
    return alert_text


def wait_for_and_dismiss_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for and dismiss an alert. Returns the text from the alert.
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    alert = wait_for_and_switch_to_alert(driver, timeout)
    alert_text = alert.text
    alert.dismiss()
    return alert_text


def wait_for_and_switch_to_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for a browser alert to appear, and switch to it. This should be usable
    as a drop-in replacement for driver.switch_to.alert when the alert box
    may not exist yet.
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            alert = driver.switch_to.alert
            # Raises exception if no alert present
            dummy_variable = alert.text  # noqa
            return alert
        except NoAlertPresentException:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise Exception("Alert was not present after %s seconds!" % timeout)


def switch_to_frame(driver, frame, timeout=settings.SMALL_TIMEOUT):
    """
    Wait for an iframe to appear, and switch to it. This should be usable
    as a drop-in replacement for driver.switch_to.frame().
    @Params
    driver - the webdriver object (required)
    frame - the frame element, name, or index
    timeout - the time to wait for the alert in seconds
    """

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            driver.switch_to.frame(frame)
            return True
        except NoSuchFrameException:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise Exception("Frame was not present after %s seconds!" % timeout)


def switch_to_window(driver, window, timeout=settings.SMALL_TIMEOUT):
    """
    Wait for a window to appear, and switch to it. This should be usable
    as a drop-in replacement for driver.switch_to.window().
    @Params
    driver - the webdriver object (required)
    window - the window index or window handle
    timeout - the time to wait for the window in seconds
    """

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    if isinstance(window, int):
        for x in range(int(timeout * 10)):
            try:
                window_handle = driver.window_handles[window]
                driver.switch_to.window(window_handle)
                return True
            except IndexError:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        raise Exception("Window was not present after %s seconds!" % timeout)
    else:
        window_handle = window
        for x in range(int(timeout * 10)):
            try:
                driver.switch_to.window(window_handle)
                return True
            except NoSuchWindowException:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        raise Exception("Window was not present after %s seconds!" % timeout)
