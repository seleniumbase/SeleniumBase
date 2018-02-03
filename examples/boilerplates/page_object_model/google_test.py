'''
Google.com testing example
'''

from seleniumbase import BaseCase
from google_objects import HomePage, ResultsPage


class GoogleTests(BaseCase):

    def test_google_dot_com(self):
        self.open('http://www.google.com')
        self.assert_element_present(HomePage.google_logo)
        self.update_text(HomePage.search_box, "github\n")
        self.assert_text("github.com", ResultsPage.search_results)
        self.click_link_text("Images")
        self.assert_element('img[alt="Image result for github"]')
