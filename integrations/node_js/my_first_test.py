from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("http://xkcd.com/353/")
        self.wait_for_element("div#comic")
        self.click('a[rel="license"]')
        text = self.wait_for_element('center').text
        self.assertTrue("reuse any of my drawings" in text)
        self.open("http://xkcd.com/1481/")
        self.click_link_text('Blag')
        self.wait_for_text("The blag", "header h2")
        self.update_text("input#s", "Robots!\n")
        self.wait_for_text("Hooray robots!", "#content")
        self.open("http://xkcd.com/1319/")
        self.wait_for_text("Automation", "div#ctitle")
