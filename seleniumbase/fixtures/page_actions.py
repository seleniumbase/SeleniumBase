"""
This module contains a set of methods that can be used for page loads and
for waiting for elements to appear on a page.

These methods improve on and expand existing WebDriver commands.
Improvements include making WebDriver commands more robust and more reliable
by giving page elements enough time to load before taking action on them.

The default option for searching for elements is by CSS Selector.
This can be changed by overriding the "By" parameter from this import:
> from selenium.webdriver.common.by import By
Options are:
By.CSS_SELECTOR        # "css selector"
By.CLASS_NAME          # "class name"
By.ID                  # "id"
By.NAME                # "name"
By.LINK_TEXT           # "link text"
By.XPATH               # "xpath"
By.TAG_NAME            # "tag name"
By.PARTIAL_LINK_TEXT   # "partial link text"
"""

import codecs
import os
import time
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from seleniumbase.common.exceptions import TextNotVisibleException
from seleniumbase.config import settings
from seleniumbase.fixtures import shared_utils


def is_element_present(driver, selector, by="css selector"):
    """
    Returns whether the specified element selector is present on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    @Returns
    Boolean (is element present)
    """
    try:
        driver.find_element(by=by, value=selector)
        return True
    except Exception:
        return False


def is_element_visible(driver, selector, by="css selector"):
    """
    Returns whether the specified element selector is visible on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    @Returns
    Boolean (is element visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed()
    except Exception:
        return False


def is_element_clickable(driver, selector, by="css selector"):
    """
    Returns whether the specified element selector is clickable.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    @Returns
    Boolean (is element clickable)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        if element.is_displayed() and element.is_enabled():
            return True
        return False
    except Exception:
        return False


def is_element_enabled(driver, selector, by="css selector"):
    """
    Returns whether the specified element selector is enabled on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    @Returns
    Boolean (is element enabled)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_enabled()
    except Exception:
        return False


def is_text_visible(driver, text, selector, by="css selector", browser=None):
    """
    Returns whether the text substring is visible in the given selector.
    @Params
    driver - the webdriver object (required)
    text - the text string to search for (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    @Returns
    Boolean (is text visible)
    """
    text = str(text)
    try:
        element = driver.find_element(by=by, value=selector)
        element_text = element.text
        if browser == "safari":
            if element.tag_name.lower() in ["input", "textarea"]:
                element_text = element.get_attribute("value")
            else:
                element_text = element.get_attribute("innerText")
        elif element.tag_name.lower() in ["input", "textarea"]:
            element_text = element.get_property("value")
        return element.is_displayed() and text in element_text
    except Exception:
        return False


def is_attribute_present(
    driver, selector, attribute, value=None, by="css selector"
):
    """
    Returns whether the specified attribute is present in the given selector.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    attribute - the attribute that is expected for the element (required)
    value - the attribute value that is expected (Default: None)
    by - the type of selector being used (Default: "css selector")
    @Returns
    Boolean (is attribute present)
    """
    try:
        element = driver.find_element(by=by, value=selector)
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


def hover_on_element(driver, selector, by="css selector"):
    """
    Fires the hover event for the specified element by the given selector.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
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
    exc, msg = shared_utils.format_exc(exception, message)
    raise exc(msg)


def hover_and_click(
    driver,
    hover_selector,
    click_selector,
    hover_by="css selector",
    click_by="css selector",
    timeout=settings.SMALL_TIMEOUT,
):
    """
    Fires the hover event for a specified element by a given selector, then
    clicks on another element specified. Useful for dropdown hover based menus.
    @Params
    driver - the webdriver object (required)
    hover_selector - the css selector to hover over (required)
    click_selector - the css selector to click on (required)
    hover_by - the hover selector type to search by (Default: "css selector")
    click_by - the click selector type to search by (Default: "css selector")
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
    click_by="css selector",
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
    click_by="css selector",
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
    driver,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    original_selector=None,
    ignore_test_time_limit=False,
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if it exists in the HTML. (The element can be invisible.)
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for elements in seconds
    original_selector - handle pre-converted ":contains(TEXT)" selector
    ignore_test_time_limit - ignore test time limit (NOT related to timeout)
    @Returns
    A web element object
    """
    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        if not ignore_test_time_limit:
            shared_utils.check_if_time_limit_exceeded()
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
        if (
            original_selector
            and ":contains(" in original_selector
            and "contains(." in selector
        ):
            selector = original_selector
        message = "Element {%s} was not present after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(NoSuchElementException, message)
    else:
        return element


def wait_for_element_visible(
    driver,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    original_selector=None,
    ignore_test_time_limit=False,
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
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for elements in seconds
    original_selector - handle pre-converted ":contains(TEXT)" selector
    ignore_test_time_limit - ignore test time limit (NOT related to timeout)
    @Returns
    A web element object
    """
    element = None
    is_present = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        if not ignore_test_time_limit:
            shared_utils.check_if_time_limit_exceeded()
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
    if not element and by != "link text":
        if (
            original_selector
            and ":contains(" in original_selector
            and "contains(." in selector
        ):
            selector = original_selector
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
    elif not element and by == "link text":
        message = "Link text {%s} was not visible after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotVisibleException, message)
    else:
        return element


def wait_for_text_visible(
    driver,
    text,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    browser=None,
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
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for elements in seconds
    browser - used to handle a special edge case when using Safari
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    is_present = False
    full_text = None
    text = str(text)
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
        full_text = None
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if (
                element.tag_name.lower() in ["input", "textarea"]
                and browser != "safari"
            ):
                if (
                    element.is_displayed()
                    and text in element.get_property("value")
                ):
                    return element
                else:
                    if element.is_displayed():
                        full_text = element.get_property("value").strip()
                    element = None
                    raise Exception()
            elif browser == "safari":
                text_attr = "innerText"
                if element.tag_name.lower() in ["input", "textarea"]:
                    text_attr = "value"
                if (
                    element.is_displayed()
                    and text in element.get_attribute(text_attr)
                ):
                    return element
                else:
                    if element.is_displayed():
                        full_text = element.get_attribute(text_attr)
                        full_text = full_text.strip()
                    element = None
                    raise Exception()
            else:
                if element.is_displayed() and text in element.text:
                    return element
                else:
                    if element.is_displayed():
                        full_text = element.text.strip()
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
        message = None
        if not full_text or len(str(full_text.replace("\n", ""))) > 320:
            message = (
                "Expected text substring {%s} for {%s} was not visible "
                "after %s second%s!" % (text, selector, timeout, plural)
            )
        else:
            full_text = full_text.replace("\n", "\\n ")
            message = (
                "Expected text substring {%s} for {%s} was not visible "
                "after %s second%s!\n (Actual string found was {%s})"
                % (text, selector, timeout, plural, full_text)
            )
        timeout_exception(TextNotVisibleException, message)
    else:
        return element


def wait_for_exact_text_visible(
    driver,
    text,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    browser=None,
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
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for elements in seconds
    browser - used to handle a special edge case when using Safari
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    is_present = False
    actual_text = None
    text = str(text)
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
        actual_text = None
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if element.tag_name.lower() in ["input", "textarea"]:
                if (
                    element.is_displayed()
                    and text.strip() == element.get_property("value").strip()
                ):
                    return element
                else:
                    if element.is_displayed():
                        actual_text = element.get_property("value").strip()
                    element = None
                    raise Exception()
            elif browser == "safari":
                text_attr = "innerText"
                if element.tag_name.lower() in ["input", "textarea"]:
                    text_attr = "value"
                if element.is_displayed() and (
                    text.strip() == element.get_attribute(text_attr).strip()
                ):
                    return element
                else:
                    if element.is_displayed():
                        actual_text = element.get_attribute(text_attr)
                        actual_text = actual_text.strip()
                    element = None
                    raise Exception()
            else:
                if (
                    element.is_displayed()
                    and text.strip() == element.text.strip()
                ):
                    return element
                else:
                    if element.is_displayed():
                        actual_text = element.text.strip()
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
        message = None
        if not actual_text or len(str(actual_text)) > 120:
            message = (
                "Expected exact text {%s} for {%s} was not visible "
                "after %s second%s!" % (text, selector, timeout, plural)
            )
        else:
            actual_text = actual_text.replace("\n", "\\n")
            message = (
                "Expected exact text {%s} for {%s} was not visible "
                "after %s second%s!\n (Actual text was {%s})"
                % (text, selector, timeout, plural, actual_text)
            )
        timeout_exception(TextNotVisibleException, message)
    else:
        return element


def wait_for_attribute(
    driver,
    selector,
    attribute,
    value=None,
    by="css selector",
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
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for the element attribute in seconds
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
        shared_utils.check_if_time_limit_exceeded()
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
    else:
        return element


def wait_for_element_clickable(
    driver,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    original_selector=None,
):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the element is present, visible, & clickable on the page.
    Raises NoSuchElementException if the element does not exist in the HTML
    within the specified timeout.
    Raises ElementNotVisibleException if the element exists in the HTML,
    but is not visible (eg. opacity is "0") within the specified timeout.
    Raises ElementNotInteractableException if the element is not clickable.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for elements in seconds
    original_selector - handle pre-converted ":contains(TEXT)" selector
    @Returns
    A web element object
    """
    element = None
    is_present = False
    is_visible = False
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
        try:
            element = driver.find_element(by=by, value=selector)
            is_present = True
            if element.is_displayed():
                is_visible = True
                if element.is_enabled():
                    return element
                else:
                    element = None
                    raise Exception()
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
    if not element and by != "link text":
        if (
            original_selector
            and ":contains(" in original_selector
            and "contains(." in selector
        ):
            selector = original_selector
        if not is_present:
            # The element does not exist in the HTML
            message = "Element {%s} was not present after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(NoSuchElementException, message)
        if not is_visible:
            # The element exists in the HTML, but is not visible
            message = "Element {%s} was not visible after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
            timeout_exception(ElementNotVisibleException, message)
        # The element is visible in the HTML, but is not clickable
        message = "Element {%s} was not clickable after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotInteractableException, message)
    elif not element and by == "link text" and not is_visible:
        message = "Link text {%s} was not visible after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotVisibleException, message)
    elif not element and by == "link text" and is_visible:
        message = "Link text {%s} was not clickable after %s second%s!" % (
            selector,
            timeout,
            plural,
        )
        timeout_exception(ElementNotInteractableException, message)
    else:
        return element


def wait_for_element_absent(
    driver,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    original_selector=None,
):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still present after the
    specified timeout.
    @Params
    driver - the webdriver object
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for elements in seconds
    original_selector - handle pre-converted ":contains(TEXT)" selector
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
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
    if (
        original_selector
        and ":contains(" in original_selector
        and "contains(." in selector
    ):
        selector = original_selector
    message = "Element {%s} was still present after %s second%s!" % (
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def wait_for_element_not_visible(
    driver,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    original_selector=None,
):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still visible after the
    specified timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for the element in seconds
    original_selector - handle pre-converted ":contains(TEXT)" selector
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
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
    if (
        original_selector
        and ":contains(" in original_selector
        and "contains(." in selector
    ):
        selector = original_selector
    message = "Element {%s} was still visible after %s second%s!" % (
        selector,
        timeout,
        plural,
    )
    timeout_exception(Exception, message)


def wait_for_text_not_visible(
    driver,
    text,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
    browser=None,
):
    """
    Searches for the text in the element of the given selector on the page.
    Returns True if the text is not visible on the page within the timeout.
    Raises an exception if the text is still present after the timeout.
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    text = str(text)
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
        if not is_text_visible(driver, text, selector, by=by, browser=browser):
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


def wait_for_attribute_not_present(
    driver,
    selector,
    attribute,
    value=None,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
):
    """
    Searches for the specified element attribute by the given selector.
    Returns True if the attribute isn't present on the page within the timeout.
    Also returns True if the element is not present within the timeout.
    Raises an exception if the attribute is still present after the timeout.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    attribute - the element attribute (required)
    value - the attribute value (Default: None)
    by - the type of selector being used (Default: "css selector")
    timeout - the time to wait for the element attribute in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        shared_utils.check_if_time_limit_exceeded()
        if not is_attribute_present(
            driver, selector, attribute, value=value, by=by
        ):
            return True
        now_ms = time.time() * 1000.0
        if now_ms >= stop_ms:
            break
        time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    message = (
        "Attribute {%s} of element {%s} was still present after %s second%s!"
        "" % (attribute, selector, timeout, plural)
    )
    if value:
        message = (
            "Value {%s} for attribute {%s} of element {%s} was still present "
            "after %s second%s!"
            "" % (value, attribute, selector, timeout, plural)
        )
    timeout_exception(Exception, message)


def find_visible_elements(driver, selector, by="css selector"):
    """
    Finds all WebElements that match a selector and are visible.
    Similar to webdriver.find_elements.
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: "css selector")
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


def save_screenshot(
    driver, name, folder=None, selector=None, by="css selector"
):
    """
    Saves a screenshot of the current page.
    If no folder is specified, uses the folder where pytest was called.
    The screenshot will include the entire page unless a selector is given.
    If a provided selector is not found, then takes a full-page screenshot.
    If the folder provided doesn't exist, it will get created.
    The screenshot will be in PNG format: (*.png)
    """
    if not name.endswith(".png"):
        name = name + ".png"
    if folder:
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        screenshot_path = os.path.join(file_path, name)
    else:
        screenshot_path = name
    if selector:
        try:
            element = driver.find_element(by=by, value=selector)
            element_png = element.screenshot_as_png
            with open(screenshot_path, "wb") as file:
                file.write(element_png)
        except Exception:
            if driver:
                driver.get_screenshot_as_file(screenshot_path)
            else:
                pass
    else:
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
        file_path = os.path.join(abs_path, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        html_file_path = os.path.join(file_path, name)
    else:
        html_file_path = name
    page_source = driver.page_source
    html_file = codecs.open(html_file_path, "w+", "utf-8")
    rendered_source = log_helper.get_html_source_with_base_href(
        driver, page_source
    )
    html_file.write(rendered_source)
    html_file.close()


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
        shared_utils.check_if_time_limit_exceeded()
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
        shared_utils.check_if_time_limit_exceeded()
        try:
            driver.switch_to.frame(frame)
            return True
        except Exception:
            if type(frame) is str:
                by = None
                if page_utils.is_xpath_selector(frame):
                    by = "xpath"
                else:
                    by = "css selector"
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
        caps = driver.capabilities
        if (
            caps["browserName"].lower() == "safari"
            and "safari:platformVersion" in caps
            and caps["safari:platformVersion"].split(".") < ["10", "15"]
        ):
            # Fix reversed window_handles on Safari 10.14 or lower
            window = len(driver.window_handles) - 1 - window
            if window < 0:
                window = 0
        for x in range(int(timeout * 10)):
            shared_utils.check_if_time_limit_exceeded()
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
            shared_utils.check_if_time_limit_exceeded()
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


############

# Duplicates for easier use without BaseCase

def wait_for_element(
    driver,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
):
    return wait_for_element_visible(
        driver=driver,
        selector=selector,
        by=by,
        timeout=timeout,
    )


def wait_for_text(
    driver,
    text,
    selector,
    by="css selector",
    timeout=settings.LARGE_TIMEOUT,
):
    browser = None  # Only used for covering a Safari edge case
    try:
        if "safari:platformVersion" in driver.capabilities:
            browser = "safari"
    except Exception:
        pass
    return wait_for_text_visible(
        driver=driver,
        text=text,
        selector=selector,
        by=by,
        timeout=timeout,
        browser=browser,
    )
