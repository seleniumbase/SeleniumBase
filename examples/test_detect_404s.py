from seleniumbase import BaseCase


class BrokenLinkTests(BaseCase):
    def test_link_checking(self):
        self.open("https://seleniumbase.io/other/broken_page.html")
        print("\n(This test should fail)")
        self.assert_no_404_errors()
