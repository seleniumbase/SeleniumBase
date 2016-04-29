from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("http://xkcd.com/353/")
        self.find_element("div#comic")
        self.click('a[rel="license"]')
        text = self.get_text('center')
        self.assertTrue("reuse any of my drawings" in text)
        self.open("http://xkcd.com/1481/")
        self.click_link_text('Blag')
        self.find_text("The blag", "header h2")
        self.update_text("input#s", "Robots!\n")
        self.find_text("Hooray robots!", "#content")
        self.open("http://xkcd.com/1319/")
        self.find_text("Automation", "div#ctitle")
