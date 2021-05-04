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
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from seleniumbase.config import settings
from seleniumbase.fixtures import shared_utils as s_utils


def is_element_present(driver, selector, by=By.CSS_SELECTOR):
    """
    Returns whether the specified element selector is present on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
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
    Returns whether the specified element selector is visible on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is element visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed()
    except Exception:
        return False


def is_element_enabled(driver, selector, by=By.CSS_SELECTOR):
    """
    Returns whether the specified element selector is enabled on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is element enabled)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_enabled()
    except Exception:
        return False


def is_text_visible(driver, text, selector, by=By.CSS_SELECTOR):
    """
    Returns whether the specified text is visible in the specified selector.
    @Params
    driver - the webdriver object (required)
    text - the text string to search for
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
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
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    """
    element = driver.find_element(by=by, value=selector)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()


def hover_element(driver, element):
    """
    Similar to hover_on_element(), but uses found element, not a selector.
    """
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()


def timeout_exception(exception, message):
    exception, message = s_utils.format_exc(exception, message)
    raise exception(message)


def hover_and_click(
    driver,
    hover_selector,
    click_selector,
    hover_by=By.CSS_SELECTOR,
    click_by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT,
):
    """
    Fires the hover event for a specified element by a given selector, then
    clicks on another element specified. Useful for dropdown hover based menus.
    @Params
    driver - the webdriver object (required)
    hover_selector - the css selector to hover over (required)
    click_selector - the css selector to click on (required)
    hover_by - the hover selector type to search by (Default: By.CSS_SELECTOR)
    click_by - the click selector type to search by (Default: By.CSS_SELECTOR)
    timeout - number of seconds to wait for click element to appear after hover
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    element = driver.find_element(by=hover_by, value=hover_selector)
    hover = ActionChains(driver).move_to_element(element)
    for x in range(int(timeout * 10)):
        try:
            hover.perform()
            element = driver.find_element(by=click_by, value=click_selector)
            element.click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was not present after %s second%s!" % (
        click_selector,
        timeout,
        plural,
    )
    timeout_exception(NoSuchElementException, message)


def hover_element_and_click(
    driver,
    element,
    click_selector,
    click_by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT,
):
    """
    Similar to hover_and_click(), but assumes top element is already found.
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    hover = ActionChains(driver).move_to_element(element)
    for x in range(int(timeout * 10)):
        try:
            hover.perform()
            element = driver.find_element(by=click_by, value=click_selector)
            element.click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was not present after %s second%s!" % (
        click_selector,
        timeout,
        plural,
    )
    timeout_exception(NoSuchElementException, message)


def hover_element_and_double_click(
    driver,
    element,
    click_selector,
    click_by=By.CSS_SELECTOR,
    timeout=settings.SMALL_TIMEOUT,
):
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    hover = ActionChains(driver).move_to_element(element)
    for x in range(int(timeout * 10)):
        try:
            hover.perform()
            element_2 = driver.find_element(by=click_by, value=click_selector)
            actions = ActionChains(driver)
            actions.move_to_element(element_2)
            actions.double_click(element_2)
            actions.perform()
            return element_2
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Element {%s} was not present after %s second%s!" % (
        click_selector,
        timeout,
        plural,
    )
    timeout_exception(NoSuchElementException, message)


def wait_for_element_present(
    driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if it exists in the HTML. (The element can be invisible.)
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object
    """
    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        message = "Element {%s} was not present after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(NoSuchElementException, message)


def wait_for_element_visible(
    driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the element is present and visible on the page.
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises ElementNotVisibleException if the element exists in the HTML,
    but is not visible (eg. opacity is "0") within the specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object
    """
    element = None
    is_present = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
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
        if not is_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        # The element exists in the HTML, but is not visible
        message = "Element {%s} was not visible after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotVisibleException, message)
    if not element and by == By.LINK_TEXT:
        message = "Link text {%s} was not visible after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotVisibleException, message)


def wait_for_text_visible(
    driver, text, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text is present in the element and visible
    on the page.
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises ElementNotVisibleException if the element exists in the HTML,
    but the text is not visible within the specified timeout.
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    is_present = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if element.is_displayed() and text in element.text:
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
        if not is_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        # The element exists in the HTML, but the text is not visible
        message = (
            "Expected text {%s} for {%s} was not visible after %s second%s!"
            % (text, selector, timeout, plural)
        )
        timeout_exception(ElementNotVisibleException, message)


def wait_for_exact_text_visible(
    driver, text, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text matches exactly with the text in the element,
    and the text is visible.
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises ElementNotVisibleException if the element exists in the HTML,
    but the exact text is not visible within the specified timeout.
    @Params
    driver - the webdriver object (required)
    text - the exact text that is expected for the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    is_present = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if element.is_displayed() and text.strip() == element.text.strip():
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
        if not is_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        # The element exists in the HTML, but the exact text is not visible
        message = (
            "Expected exact text {%s} for {%s} was not visible "
            "after %s second%s!" % (text, selector, timeout, plural)
        )
        timeout_exception(ElementNotVisibleException, message)


def wait_for_attribute(
    driver,
    selector,
    attribute,
    value=None,
    by=By.CSS_SELECTOR,
    timeout=settings.LARGE_TIMEOUT,
):
    """
    Searches for the specified element attribute by the given selector.
    Returns the element object if the expected attribute is present
    and the expected attribute value is present (if specified).
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises NoSuchAttributeException if the element exists in the HTML,
    but the expected attribute/value is not present within the timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    attribute - the attribute that is expected for the element (required)
    value - the attribute value that is expected (Default: None)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the expected attribute/value
    """
    element = None
    element_present = False
    attribute_present = False
    found_value = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            element_present = True
            attribute_present = False
            found_value = element.get_attribute(attribute)
            if found_value is not None:
                attribute_present = True
            else:
                element = None
                raise Exception()

            if value is not None:
                if found_value == value:
                    return element
                else:
                    element = None
                    raise Exception()
            else:
                return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        if not element_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        if not attribute_present:
            # The element does not have the attribute
            message = (
                "Expected attribute {%s} of element {%s} was not present "
                "after %s second%s!" % (attribute, selector, timeout, plural)
            )
            timeout_exception(NoSuchAttributeException, message)
        # The element attribute exists, but the expected value does not match
        message = (
            "Expected value {%s} for attribute {%s} of element {%s} was not "
            "present after %s second%s! (The actual value was {%s})"
            % (value, attribute, selector, timeout, plural, found_value)
        )
        timeout_exception(NoSuchAttributeException, message)


def wait_for_element_absent(
    driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still present after the
    specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
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
    message = "Element {%s} was still present after %s second%s!" % (
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def wait_for_element_not_visible(
    driver, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still visible after the
    specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for the element in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
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
    message = "Element {%s} was still visible after %s second%s!" % (
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def wait_for_text_not_visible(
    driver, text, selector, by=By.CSS_SELECTOR, timeout=settings.LARGE_TIMEOUT
):
    """
    Searches for the text in the element of the given selector on the page.
    Returns True if the text is not visible on the page within the timeout.
    Raises an exception if the text is still present after the timeout.
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        if not is_text_visible(driver, text, selector, by=by):
            return True
        now_ms = time.time() * 1000.0
        if now_ms >= stop_ms:
            break
        time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Text {%s} in {%s} was still visible after %s second%s!" % (
        text,
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def find_visible_elements(driver, selector, by=By.CSS_SELECTOR):
    """
    Finds all WebElements that match a selector and are visible.
    Similar to webdriver.find_elements.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    """
    elements = driver.find_elements(by=by, value=selector)
    try:
        v_elems = [element for element in elements if element.is_displayed()]
        return v_elems
    except (StaleElementReferenceException, ElementNotInteractableException):
        time.sleep(0.1)
        elements = driver.find_elements(by=by, value=selector)
        v_elems = []
        for element in elements:
            if element.is_displayed():
                v_elems.append(element)
        return v_elems


def save_screenshot(driver, name, folder=None):
    """
    Saves a screenshot to the current directory (or to a subfolder if provided)
    If the folder provided doesn't exist, it will get created.
    The screenshot will be in PNG format.
    """
    if not name.endswith(".png"):
        name = name + ".png"
    if folder:
        abs_path = os.path.abspath(".")
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        screenshot_path = "%s/%s" % (file_path, name)
    else:
        screenshot_path = name
    try:
        element = driver.find_element(by=By.TAG_NAME, value="body")
        element_png = element.screenshot_as_png
        with open(screenshot_path, "wb") as file:
            file.write(element_png)
    except Exception:
        if driver:
            driver.get_screenshot_as_file(screenshot_path)
        else:
            pass


def save_page_source(driver, name, folder=None):
    """
    Saves the page HTML to the current directory (or given subfolder).
    If the folder specified doesn't exist, it will get created.
    @Params
    name - The file name to save the current page's HTML to.
    folder - The folder to save the file to. (Default = current folder)
    """
    from seleniumbase.core import log_helper

    if not name.endswith(".html"):
        name = name + ".html"
    if folder:
        abs_path = os.path.abspath(".")
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        html_file_path = "%s/%s" % (file_path, name)
    else:
        html_file_path = name
    page_source = driver.page_source
    html_file = codecs.open(html_file_path, "w+", "utf-8")
    rendered_source = log_helper.get_html_source_with_base_href(
        driver, page_source
    )
    html_file.write(rendered_source)
    html_file.close()


def _get_last_page(driver):
    try:
        last_page = driver.current_url
    except Exception:
        last_page = "[WARNING! Browser Not Open!]"
    if len(last_page) < 5:
        last_page = "[WARNING! Browser Not Open!]"
    return last_page


def save_test_failure_data(driver, name, browser_type, folder=None):
    """
    Saves failure data to the current directory (or to a subfolder if provided)
    If the folder provided doesn't exist, it will get created.
    """
    import traceback

    if folder:
        abs_path = os.path.abspath(".")
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
    data_to_save.append(
        "Traceback: "
        + "".join(
            traceback.format_exception(
                sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
            )
        )
    )
    failure_data_file.writelines("\r\n".join(data_to_save))
    failure_data_file.close()


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
        s_utils.check_if_time_limit_exceeded()
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
    message = "Alert was not present after %s seconds!" % timeout
    timeout_exception(Exception, message)


def switch_to_frame(driver, frame, timeout=settings.SMALL_TIMEOUT):
    """
    Wait for an iframe to appear, and switch to it. This should be
    usable as a drop-in replacement for driver.switch_to.frame().
    @Params
    driver - the webdriver object (required)
    frame - the frame element, name, id, index, or selector
    timeout - the time to wait for the alert in seconds
    """
    from seleniumbase.fixtures import page_utils

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        s_utils.check_if_time_limit_exceeded()
        try:
            driver.switch_to.frame(frame)
            return True
        except NoSuchFrameException:
            if type(frame) is str:
                by = None
                if page_utils.is_xpath_selector(frame):
                    by = By.XPATH
                else:
                    by = By.CSS_SELECTOR
                if is_element_visible(driver, frame, by=by):
                    try:
                        element = driver.find_element(by=by, value=frame)
                        driver.switch_to.frame(element)
                        return True
                    except Exception:
                        pass
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = "Frame {%s} was not visible after %s second%s!" % (
        frame,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


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
            s_utils.check_if_time_limit_exceeded()
            try:
                window_handle = driver.window_handles[window]
                driver.switch_to.window(window_handle)
                return True
            except IndexError:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        message = "Window {%s} was not present after %s second%s!" % (
            window,
            timeout,
            plural,
        )
        timeout_exception(Exception, message)
    else:
        window_handle = window
        for x in range(int(timeout * 10)):
            s_utils.check_if_time_limit_exceeded()
            try:
                driver.switch_to.window(window_handle)
                return True
            except NoSuchWindowException:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        message = "Window {%s} was not present after %s second%s!" % (
            window,
            timeout,
            plural,
        )
        timeout_exception(Exception, message)
