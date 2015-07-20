from test_framework import BaseCase

class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("http://xkcd.com/1513/")
        self.click('a[href="http://blag.xkcd.com"]')
        self.wait_for_text_visible("The blag of the webcomic", "#site-description")
        self.update_text_value("input#s", "Robots!\n")
        self.wait_for_text_visible("Hooray robots!", "#content")
        self.open("http://xkcd.com/1481/")
        self.wait_for_element_visible("div#comic")
        self.click('a[rel="license"]')
        text = self.wait_for_element_visible('center').text
        self.assertTrue("reuse any of my drawings" in text)
        self.assertTrue("You can use them freely" in text)
