"""
This module contains a set of methods that can be used for loading pages and
waiting for elements to come in.

The default option we use to search for elements is CSS Selector.
This can be changed by setting the by paramter.  The enum class for options is:
from selenium.webdriver.common.by import By

Options are
By.CSS_SELECTOR
By.CLASS_NAME
By.ID
By.NAME
By.LINK_TEXT
By.XPATH
By.TAG_NAME
By.PARTIAL_LINK_TEXT
"""

import time
from seleniumbase.config import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException, \
                                                   NoSuchElementException, \
                                                   NoAlertPresentException


def wait_for_element_present(driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector.  Returns the
    element object if the element is present on the page.  The element can be
    invisible.  Raises an exception if the element does not appear in the
    specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator that is used (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds

    @returns
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
        raise NoSuchElementException("Element %s was not present in %s seconds!" %
                                     (selector, timeout))


def wait_for_element_visible(driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector.  Returns the
    element object if the element is present and visible on the page.
    Raises an exception if the element does not appear in the
    specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds

    @returns
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
        raise ElementNotVisibleException("Element %s was not visible in %s seconds!"\
                                         % (selector, timeout))


def wait_for_text_visible(driver, text, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text is present in the element and visible
    on the page. Raises an exception if the text or element do not appear
    in the specified timeout.
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator that is used (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds

    @returns
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
        raise ElementNotVisibleException("Expected text [%s] for element [%s] was not visible in %s seconds!"\
                                         % (text, selector, timeout))


def wait_for_element_absent(driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns void when
    element is no longer present on the page. Raises an exception if the
    element does still exist after the specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator that is used (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)
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


def wait_for_element_not_visible(driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns void when
    element is no longer visible on the page (or if the element is not
    present). Raises an exception if the element is still visible after the
    specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
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
    raise Exception("Element %s was still visible after %s seconds!"\
                                     % (selector, timeout))


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
    raise Exception("Page elements never fully loaded after %s seconds!"\
                                     % timeout)


def wait_for_and_accept_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for and accept an alert. Returns the text from the alert.
    @params
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
    @params
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
    as a drop-in replacement for driver.switch_to_alert() when the alert box may
    not exist yet.
    @params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """

    for x in range(int(timeout * 10)):
        try:
            alert = driver.switch_to_alert()
            dummy_variable = alert.text  # Raises exception if no alert present
            return alert
        except NoAlertPresentException:
            time.sleep(0.1)
    raise Exception("Alert was not present after %s seconds!" % timeout)
