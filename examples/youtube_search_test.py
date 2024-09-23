from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class YouTubeSearchTests(BaseCase):
    def test_youtube_autocomplete_results(self):
        """Verify YouTube autocomplete search results."""
        if self.headless or self.browser == "safari":
            self.open_if_not_url("about:blank")
            print("\n  Unsupported mode for this test.")
            self.skip("Unsupported mode for this test.")
        self.open("https://www.youtube.com/c/MichaelMintz")
        search_term = "seleniumbase"
        search_selector = "input#search"
        results_selector = '[role="listbox"]'
        self.click_if_visible('button[aria-label="Close"]')
        self.double_click(search_selector)
        self.sleep(0.15)
        self.type(search_selector, search_term)
        self.sleep(0.15)
        # First verify that an autocomplete result exists
        self.assert_element(results_selector)
        top_results = self.get_text(results_selector)
        # Now verify that the autocomplete result is good
        self.assert_true(
            search_term in top_results,
            'Expected text "%s" not found in top results! '
            'Actual text was "%s"!' % (search_term, top_results),
        )
        self.sleep(1)
