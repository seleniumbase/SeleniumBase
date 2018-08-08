'''
Bing.com testing example
'''

from seleniumbase import BaseCase
from .bing_objects import Page


class BingTests(BaseCase):

    def test_bing(self):
        self.open('https://bing.com')
        self.assert_text('Bing', Page.logo_box)
        self.update_text(Page.search_box, 'github')
        self.assert_element('li[query="github"]')
        self.click(Page.search_button)
        self.assert_text('github.com', Page.search_results)
        self.click_link_text('Images')
        self.assert_element('img[alt="Image result for github"]')
