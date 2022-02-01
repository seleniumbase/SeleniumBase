""" Testing EventFiringWebDriver with AbstractEventListener """

from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener
from seleniumbase import BaseCase


class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        print("Before navigating to: %s" % url)

    def after_navigate_to(self, url, driver):
        print("After navigating to: %s" % url)

    def before_find(self, by, value, driver):
        print('Before find "%s" (by = %s)' % (value, by))

    def after_find(self, by, value, driver):
        print('After find "%s" (by = %s)' % (value, by))

    def before_click(self, element, driver):
        print('Before clicking on element with text: "%s"' % element.text)

    def after_click(self, element, driver):
        print("Click complete!")


class EventFiringTests(BaseCase):
    def test_event_firing_webdriver(self):
        self.driver = EventFiringWebDriver(self.driver, MyListener())
        print("\n* EventFiringWebDriver example *")
        self.open("https://xkcd.com/1862/")
        self.click("link=About")
        self.open("https://xkcd.com/1820/")
        self.assert_text("Security Advice", "#ctitle")
        self.click('a:contains("Next >")')
        self.assert_text("Incinerator", "#ctitle")
        self.click('a[rel="next"]')
        self.assert_text("Existential Bug Reports", "#ctitle")
