'''
Google.com testing example
'''

from seleniumbase import BaseCase
from .google_objects import HomePage, ResultsPage


class GoogleTests(BaseCase):

    def test_google_dot_com(self):
        self.open('https://google.com')
        self.update_text(HomePage.search_box, 'github')
        self.assert_element(HomePage.list_box)
        self.assert_element(HomePage.search_button)
        self.assert_element(HomePage.feeling_lucky_button)
        self.click(HomePage.search_button)
        self.assert_text('github.com', ResultsPage.search_results)
        self.click_link_text('Images')
        source = self.get_page_source()
        self.assertTrue("Image result for github" in source)
