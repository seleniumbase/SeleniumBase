from seleniumbase import BaseCase


class XPathTests(BaseCase):
    def test_xpath(self):
        self.open("https://seleniumbase.io/demo_page")
        self.assert_element("/html/body/form/table/tbody/tr[1]/td[1]/h1")
        self.type('//*[@id="myTextInput"]', "XPath Test!")
        self.click("/html/body/form/table/tbody/tr[3]/td[4]/button")
        self.assert_text("SeleniumBase", '//table/tbody/tr[1]/td[2]/h2')
