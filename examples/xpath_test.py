from seleniumbase import BaseCase


class XPathTests(BaseCase):
    def test_xpath(self):
        self.open("https://seleniumbase.io/demo_page")
        self.assert_element('//h1[(text()="Demo Page")]')
        self.type('//*[@id="myTextInput"]', "XPath Test!")
        self.click('//button[starts-with(text(),"Click Me")]')
        self.assert_element('//button[contains(., "Purple")]')
        self.assert_text("SeleniumBase", "//table/tbody/tr[1]/td[2]/h2")
