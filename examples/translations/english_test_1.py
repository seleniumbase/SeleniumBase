from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_example_1(self):
        url = "https://store.xkcd.com/collections/posters"
        self.open(url)
        self.type("input.search-input", "xkcd book\n")
        self.assert_text("xkcd: volume 0", "h3")
        self.click("li.checkout-link")
        self.assert_text("Shopping Cart", "#page-title")
        self.assert_element("div#umbrella")
        self.open("https://xkcd.com/353/")
        self.assert_title("xkcd: Python")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("back to this page")
        self.go_back()
        self.click_link_text("About")
        self.assert_exact_text("xkcd.com", "h2")
