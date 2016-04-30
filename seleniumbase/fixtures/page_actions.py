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

import os
import time
from seleniumbase.config import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from selenium.webdriver.remote.errorhandler import NoAlertPresentException


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


def hover_on_element(driver, selector):
    """
    Fires the hover event for the specified element by the given selector.
    @Params
    driver - the webdriver object (required)
    selector - the locator (css selector) that is used (required)
    """
    driver.execute_script("jQuery('%s').mouseover()" % selector)


def hover_and_click(driver, hover_selector, click_selector,
                    click_by=By.CSS_SELECTOR, timeout=settings.SMALL_TIMEOUT):
    """
    Fires the hover event for a specified element by a given selector, then
    clicks on another element specified. Useful for dropdown hover based menus.
    @Params
    driver - the webdriver object (required)
    hover_selector - the css selector to hover over (required)
    click_selector - the css selector to click on (required)
    click_by - the method to search by (Default: By.CSS_SELECTOR)
    timeout - number of seconds to wait for click element to appear after hover
    """
    driver.execute_script("jQuery('%s').mouseover()" % (hover_selector))
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=click_by,
                                          value="%s" % click_selector).click()
            return element
        except Exception:
            time.sleep(0.1)
    raise NoSuchElementException(
        "Element %s was not present after %s seconds!" %
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
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            return element
        except Exception:
            time.sleep(0.1)
    if not element:
        raise NoSuchElementException(
            "Element %s was not present in %s seconds!" % (selector, timeout))


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
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            time.sleep(0.1)
    if not element:
        raise ElementNotVisibleException(
            "Element %s was not visible in %s seconds!" % (selector, timeout))


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
            time.sleep(0.1)
    if not element:
        raise ElementNotVisibleException(
            "Expected text [%s] for [%s] was not visible after %s seconds!" %
            (text, selector, timeout))


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

    for x in range(int(timeout * 10)):
        try:
            driver.find_element(by=by, value=selector)
            time.sleep(0.1)
        except Exception:
            return
    raise Exception("Element %s was still present after %s seconds!" %
                    (selector, timeout))


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

    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                time.sleep(0.1)
            else:
                return
        except Exception:
            return
    raise Exception(
        "Element %s was still visible after %s seconds!" % (selector, timeout))


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


def wait_for_ready_state_complete(driver, timeout=settings.EXTREME_TIMEOUT):
    """
    The DOM (Document Object Model) has a property called "readyState".
    When the value of this becomes "complete", page resources are considered
    fully loaded (although AJAX and other loads might still be happening).
    This method will wait until document.readyState == "complete".
    """

    for x in range(int(timeout * 10)):
        ready_state = driver.execute_script("return document.readyState")
        if ready_state == u'complete':
            return True
        else:
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
    as a drop-in replacement for driver.switch_to.alert() when the alert box
    may not exist yet.
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """

    for x in range(int(timeout * 10)):
        try:
            alert = driver.switch_to.alert()
            # Raises exception if no alert present
            dummy_variable = alert.text  # noqa
            return alert
        except NoAlertPresentException:
            time.sleep(0.1)
    raise Exception("Alert was not present after %s seconds!" % timeout)
