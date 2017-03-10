from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open('http://xkcd.com/353/')                       # Opens the url
        self.assert_element('img[alt="Python"]')      # Asserts element on page
        self.click('a[rel="license"]')                 # Clicks element on page
        xkcd_license = self.get_text('center')    # Gets text from page element
        self.assertTrue('reuse any of my drawings' in xkcd_license)
        self.open('http://xkcd.com/1481/')
        image_object = self.find_element('#comic img')    # Returns the element
        caption = image_object.get_attribute('title')  # Gets attr from element
        self.assertTrue('connections to the server' in caption)
        self.click_link_text('Blag')          # Clicks link containing the text
        self.assert_text('The blag', 'header h2')     # Asserts text in element
        self.update_text('input#s', 'Robots!\n')  # Updates textfield with text
        self.assert_text('Hooray robots!', '#content')
        self.open('http://xkcd.com/1319/')
        self.assert_text('Automation', 'div#ctitle')

        ####

        #######################################################################
        #
        #    ****  NOTES / USEFUL INFO  ****
        #
        # 1. By default, CSS Selectors are used to identify elements.
        #    You can use other identification options like PARTIAL_LINK_TEXT:
        #    [
        #        from selenium.webdriver.common.by import By
        #        ...
        #        self.click('Next', by=By.PARTIAL_LINK_TEXT)
        #    ]
        #    For the full list of `By` options, type ``dir(By)`` into a python
        #    command prompt after importing it (or in ipdb debugger mode). Ex:
        #    {
        #        >>> dir(By)
        #        ['CLASS_NAME', 'CSS_SELECTOR', 'ID', 'LINK_TEXT', 'NAME', ...
        #    }
        #    XPath is used by default if the arg starts with "/" or "./". Ex:
        #    [
        #        self.click('/html/body/div[3]/div[4]/p[2]/a')
        #    ]
        #
        #    If you're completely new to CSS selectors, right-click on a
        #    web page and select "Inspect Element" to see the CSS in the html.
        #
        # 2. Most methods have the optional `timeout` argument. Ex:
        #    [
        #        self.get_text('center', timeout=15)
        #    ]
        #    The `timeout` argument tells the method how many seconds to wait
        #    for an element to appear before raising an exception. This is
        #    useful if a web page needs additional time to load an element.
        #    If you don't specify a `timeout`, a default timeout is used.
        #    Default timeouts are configured in seleniumbase/config/settings.py
        #
        # 3. There's usually more than one way to do the same thing. Ex:
        #    [
        #        xkcd_license = self.get_text('center')
        #        assert('reuse any of my drawings' in xkcd_license)
        #    ]
        #    Can be simplified to:
        #    [
        #        self.assert_text('reuse any of my drawings', 'center')
        #    ]
        #
        #    And the following line:
        #    [
        #        xkcd_license = self.get_text('center')
        #    ]
        #    Can also be written as:
        #    [
        #        xkcd_license = self.find_element('center').text
        #    ]
        #    ...and in many more ways!
        #
        #    For backwards-compatibilty, some methods have multiple names.
        #    Ex: wait_for_element_visible() is the same as find_element().
        #    Both search for and return the element, and raise an exception if
        #    the element does not appear on the page within the timeout limit.
        #    (See seleniumbase/fixtures/base_case.py for the full method list.)
