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
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException
from selenium.webdriver.remote.errorhandler import NoSuchElementException


def is_element_present(driver, selector, by=By.CSS_SELECTOR):
    """
    Searches for the specified element by the given selector.  Returns whether 
    the element object if the element is present on the page.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)

    @returns
    Boolean Whether the element is present
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
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)

    @returns
    Boolean Whether the element is present and visible
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed()
    except Exception:
        return False


def is_text_visible(driver, text, selector, by=By.CSS_SELECTOR):
    """
    Searches for the specified element by the given selector.  Returns whether 
    the element object if the element is present and visible on the page and 
    contains the given text.
    @Params
    driver - the webdriver object (required)
    text - the text string to search for
    selector - the locator that is used (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)

    @returns
    Boolean Whether the element is present and visible
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed() and text in element.text
    except Exception:
        return False


def find_visible_element(driver, selector, by=By.CSS_SELECTOR):
    """
    Finds a WebElement that matches a selector and is visible. 
    Similar to webdriver.find_element.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used to search the DOM (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)
    """
    element = driver.find_element(by=by, value=selector)
    if element.is_displayed():
        return element
    else:
        return None


def find_visible_elements(driver, selector, by=By.CSS_SELECTOR):
    """
    Finds all WebElements that matche a selector and are visible. 
    Similar to webdriver.find_elements.
    @Params
    driver - the webdriver object (required)
    selector - the locator that is used to search the DOM (required)
    by - the method to search for hte locator (Default- By.CSS_SELECTOR)
    """
    elements = driver.find_elements(by=by, value=selector)
    
    return [element for element in elements if element.is_displayed()]


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
    Fires the hover event for a specified element by a given selector, then clicks on
    another element specified. Useful for dropdown hover based menus.
    @Params
    driver - the webdriver object (required)
    hover_selector - the locator (css selector) that is used to hover (required)
    click_selector - the locator that is used to click (required)
    click_by - the method to search for hte locator (Default- By.CSS_SELECTOR)
    timeout - number of seconds to wait between hover and click (Default- 5 seconds)
    """
    driver.execute_script("jQuery('%s').mouseover()" % (hover_selector))
    for x in range(timeout * 10):
        try:
            element = driver.find_element(by=click_by, value="%s" % 
                                          click_selector).click()
            return element
        except Exception:
            time.sleep(0.1)
    raise NoSuchElementException("Element %s was not present in %s" %
                                (click_selector, timeout))
