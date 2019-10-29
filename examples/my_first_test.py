from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.assert_title("xkcd: Python")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy and reuse")
        self.go_back()
        self.click("link=About")
        self.assert_text("xkcd.com", "h2")
        self.open("https://store.xkcd.com/collections/everything")
        self.update_text("input.search-input", "xkcd book\n")
        self.assert_exact_text("xkcd: volume 0", "h3")

        ####

        #######################################################################
        #
        #    ****  NOTES / USEFUL INFO  ****
        #
        # 1. By default, CSS Selectors are used to identify elements.
        #    Other options include: "LINK_TEXT", "PARTIAL_LINK_TEXT", "NAME",
        #    "CLASS_NAME", and "ID", but most of those can be expressed as CSS.
        #    Here's an example of changing the "by":
        #    [
        #        from selenium.webdriver.common.by import By
        #        ...
        #        self.click('Next', by=By.PARTIAL_LINK_TEXT)
        #    ]
        #    XPath is used by default if the arg starts with "/", "./", or "(":
        #    [
        #        self.click('/html/body/div[3]/div[4]/p[2]/a')
        #    ]
        #
        #    If you're completely new to CSS selectors, right-click on a
        #    web page and select "Inspect" to see the CSS in the html.
        #
        # 2. Most methods have the optional `timeout` argument. Ex:
        #    [
        #        self.assert_element('img[alt="Python"]', timeout=15)
        #    ]
        #    The `timeout` argument tells the method how many seconds to wait
        #    for an element to appear before raising an exception. This is
        #    useful if a web page needs additional time to load an element.
        #    If you don't specify a `timeout`, a default timeout is used.
        #    Default timeouts are configured in seleniumbase/config/settings.py
        #
        # 3. SeleniumBase methods are very versatile. For example,
        #    self.update_text(SELECTOR, TEXT) does the following:
        #    * Waits for the element to be visible
        #    * Waits for the element to be interactive
        #    * Clears the text field
        #    * Types in the new text
        #    * Hits Enter/Submit (if the text ends in "\n")
        #
        #    self.update_text(S, T) can also be written as self.type(S, T)
        #
        # 4. There's usually more than one way to do the same thing. Ex:
        #    [
        #        self.assert_text("xkcd: volume 0", "h3")
        #    ]
        #    Is the same as:
        #    [
        #        text = self.get_text("h3")
        #        self.assert_true("xkcd: volume 0" in text)
        #    ]
        #    Or:
        #    [
        #        text = self.find_element("h3").text
        #        self.assert_true("xkcd: volume 0" in text)
        #    ]
        #
        #    And the following line:
        #    [
        #        title = self.get_attribute("#comic img", "title")
        #    ]
        #    Can also be written as:
        #    [
        #        element = self.find_element("#comic img")
        #        title = element.get_attribute("title")
        #    ]
        #
        # 5. self.assert_exact_text(TEXT) ignores leading and trailing
        #    whitespace in the TEXT assertion.
        #    So, self.assert_exact_text("Some Text") will find [" Some Text "].
        #
        # 6. For backwards-compatibilty, some SeleniumBase methods that do the
        #    same thing have multiple names, kept on from previous versions.
        #    Ex: wait_for_element_visible() is the same as find_element().
        #    Both search for and return the element, and raise an exception if
        #    the element does not appear on the page within the timeout limit.
        #    And assert_element() also does this (minus returning the element).
        #
        # 7. For the full method list, see one of the following:
        #    * SeleniumBase/seleniumbase/fixtures/base_case.py
        #    * SeleniumBase/help_docs/method_summary.md
