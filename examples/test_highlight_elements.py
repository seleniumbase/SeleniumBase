from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class HighlightTest(BaseCase):
    def test_highlight_inputs(self):
        self.open("https://seleniumbase.io/demo_page")
        if self.headed:
            self.highlight_elements("input", loops=2)  # Default: 4
        else:
            self.highlight_elements("input", loops=1, limit=3)
