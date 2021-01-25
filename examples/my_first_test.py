from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basics(self):
        url = "https://store.xkcd.com/collections/posters"
        self.open(url)
        self.type('input[name="q"]', "xkcd book")
        self.click('input[value="Search"]')
        self.assert_text("xkcd: volume 0", "h3")
        self.open("https://xkcd.com/353/")
        self.assert_title("xkcd: Python")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy and reuse")
        self.go_back()
        self.click_link("About")
        self.assert_exact_text("xkcd.com", "h2")

        ####

        #######################################################################
        #
        #    ****  NOTES / USEFUL INFO  ****
        #
        # 1. By default, CSS Selectors are used to identify elements.
        #    CSS Guide: "https://www.w3schools.com/cssref/css_selectors.asp".
        #    Other selectors include: "LINK_TEXT", "PARTIAL_LINK_TEXT", "NAME",
        #    "CLASS_NAME", and "ID", but most of those can be expressed as CSS.
        #
        #    Here's an example of changing the "by":
        #    [
        #        from selenium.webdriver.common.by import By
        #        ...
        #        self.click('Next', by=By.PARTIAL_LINK_TEXT)
        #    ]
        #
        #    XPath is used by default if the arg starts with "/", "./", or "(":
        #    [
        #        self.click('/html/body/div[3]/div[4]/p[2]/a')
        #    ]
        #
        #    If you're completely new to CSS selectors, right-click on a
        #    web page and select "Inspect" to see the CSS in the html.
        #
        # 2. Most methods have the optional "timeout" argument.
        #    Here's an example of changing the "timeout":
        #    [
        #        self.assert_element('img[alt="Python"]', timeout=15)
        #    ]
        #    The "timeout" argument tells the method how many seconds to wait
        #    for an element to appear before failing the test. This is
        #    useful if a web page needs additional time to load an element.
        #    If you don't specify a "timeout", a default timeout is used.
        #    Default timeouts are configured in seleniumbase/config/settings.py
        #
        # 3. SeleniumBase methods often perform multiple actions. For example,
        #    self.type(SELECTOR, TEXT) will do the following:
        #    * Wait for the element to be visible
        #    * Wait for the element to be interactive
        #    * Clear the text field
        #    * Type in the new text
        #    * Press Enter/Submit if the text ends in "\n"
        #
        # 4. Duplicate method names may exist for the same method:
        #    (This makes it easier to switch over from other test frameworks.)
        #    Example:
        #    self.open() = self.visit() = self.open_url() = self.goto()
        #    self.type() = self.update_text() = self.input()
        #    self.send_keys() = self.add_text()
        #    self.get_element() = self.wait_for_element_present()
        #    self.find_element() = self.wait_for_element_visible()
        #                        = self.wait_for_element()
        #    self.assert_element() = self.assert_element_visible()
        #    self.assert_text() = self.assert_text_visible()
        #    self.find_text() = self.wait_for_text_visible()
        #                     = self.wait_for_text()
        #    self.click_link(text) = self.click(link=text)
        #                          = self.click_link_text(text)
        #    * self.get(url) is SPECIAL: *
        #    If {url} is a valid URL, self.get() works just like self.open()
        #    Otherwise {url} becomes a selector for calling self.get_element()
        #
        # 5. There's usually more than one way to do the same thing.
        #    Example 1:
        #    [
        #        self.assert_text("xkcd: volume 0", "h3")
        #    ]
        #    Is the same as:
        #    [
        #        text = self.get_text("h3")
        #        self.assert_true("xkcd: volume 0" in text)
        #    ]
        #    Is also the same as:
        #    [
        #        element = self.find_element("h3")
        #        text = element.text
        #        self.assert_true("xkcd: volume 0" in text)
        #    ]
        #
        #    Example 2:
        #    [
        #        self.assert_exact_text("xkcd.com", "h2")
        #    ]
        #    Is the same as:
        #    [
        #        text = self.get_text("h2").strip()
        #        self.assert_true("xkcd.com".strip() == text)
        #    ]
        #
        #    Example 3:
        #    [
        #        title = self.get_attribute("#comic img", "title")
        #    ]
        #    Is the same as:
        #    [
        #        element = self.find_element("#comic img")
        #        title = element.get_attribute("title")
        #    ]
        #
        # 6. self.assert_exact_text(TEXT) ignores leading and trailing
        #    whitespace in the TEXT assertion.
        #    So, self.assert_exact_text("Some Text") will find [" Some Text "].
        #
        # 7. If a URL starts with "://", then "https://" is automatically used.
        #    Example: [self.open("://URL")] becomes [self.open("https://URL")]
        #    This helps by reducing the line length by 5 characters.
        #
        # 8. For the full method list, see one of the following:
        #    * SeleniumBase/seleniumbase/fixtures/base_case.py
        #    * SeleniumBase/help_docs/method_summary.md
