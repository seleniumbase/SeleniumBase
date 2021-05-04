from seleniumbase import BaseCase


class MyTestClass(BaseCase):
    def test_basics(self):
        self.open("https://store.xkcd.com/search")
        self.type('input[name="q"]', "xkcd book\n")
        self.assert_text("xkcd book", "div.results")
        self.open("https://xkcd.com/353/")
        self.click('a[rel="license"]')
        self.go_back()
        self.click_link("About")
        self.click_link("comic #249")
        self.assert_element('img[alt*="Chess"]')
