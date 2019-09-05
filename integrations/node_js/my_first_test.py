from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.assert_title("xkcd: Python")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy and reuse")
        self.go_back()
        self.click("link=About")
        self.assert_text("xkcd.com", "h2")
        self.open("https://store.xkcd.com/collections/everything")
        self.update_text("input.search-input", "xkcd book\n")
        self.assert_exact_text("xkcd: volume 0", "h3")
