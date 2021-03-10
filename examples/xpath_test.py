from seleniumbase import BaseCase


class XPathTests(BaseCase):

    def test_xpath(self):
        self.open("https://xkcd.com/1319/")
        self.assert_element('//img')
        self.assert_element('/html/body/div[2]/div[2]/img')
        self.click("//ul/li[6]/a")
        self.assert_text("xkcd.com", "//h2")
