from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy and reuse")
        self.open("https://xkcd.com/1481/")
        title = self.get_attribute("#comic img", "title")
        self.assert_true("86,400 seconds per day" in title)
        self.click("link=Store")
        self.assert_element('[alt="The xkcd store"]')
        self.update_text("input.search-input", "xkcd book\n")
        self.assert_text("xkcd: volume 0", "h3")
        self.open("https://xkcd.com/1319/")
        self.assert_exact_text("Automation", "#ctitle")
