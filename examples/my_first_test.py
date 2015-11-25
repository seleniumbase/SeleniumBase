from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("http://xkcd.com/353/")
        self.wait_for_element_visible("div#comic")
        self.click('a[rel="license"]')
        text = self.wait_for_element_visible('center').text
        self.assertTrue("reuse any of my drawings" in text)
        self.assertTrue("You can use them freely" in text)
        self.open("http://xkcd.com/1481/")
        self.click_link_text('Blag')
        self.wait_for_text_visible("The blag of the webcomic", "#site-description")
        self.update_text_value("input#s", "Robots!\n")
        self.wait_for_text_visible("Hooray robots!", "#content")
        self.open("http://xkcd.com/1319/")
        self.wait_for_text_visible("Automation", "div#ctitle")
