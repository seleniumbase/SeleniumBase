from seleniumbase import BaseCase


class YouTubeSearchTests(BaseCase):
    def test_youtube_autocomplete_results(self):
        """ Verify YouTube autocomplete search results. """
        self.open("https://www.youtube.com/")
        search_term = "seleniumbase"
        search_selector = "input#search"
        result_selector = 'li[role="presentation"] b'
        self.click_if_visible('button[aria-label="Close"]')
        self.double_click(search_selector)
        self.type(search_selector, search_term)
        # First verify that an autocomplete result exists
        self.assert_element(result_selector)
        top_result = self.get_text(result_selector)
        # Now verify that the autocomplete result is good
        self.assert_true(
            search_term in top_result,
            'Expected text "%s" not found in top result! '
            'Actual text was "%s"!'
            % (search_term, top_result)
        )

    def test_youtube_search_results(self):
        """ Verify finding a specific video by performing a YouTube search. """
        self.open("https://www.youtube.com/")
        search_term = "SeleniumBase Common API Methods"
        search_selector = "input#search"
        self.type(search_selector, search_term + "\n")
        self.ad_block()
        self.demo_mode = True
        self.assert_element('.text-wrapper > div:contains("%s")' % search_term)
