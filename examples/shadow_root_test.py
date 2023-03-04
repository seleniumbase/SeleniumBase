"""Piercing through shadow-root elements with the "::shadow" selector.
To confirm that "::shadow" works, print text and assert exact text."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ShadowRootTest(BaseCase):
    def test_shadow_root(self):
        if self.recorder_mode:
            self.open_if_not_url("about:blank")
            message = "Skipping test in Recorder Mode."
            print(message)
            self.skip(message)
        elif self.browser == "safari":
            self.open_if_not_url("about:blank")
            message = "Skipping test for using Safari."
            print(message)
            self.skip(message)
        self.open("https://seleniumbase.io/other/shadow_dom")
        print("")
        self.click("button.tab_1")
        print(self.get_text("fancy-tabs::shadow #panels"))
        self.assert_exact_text("Content Panel 1", "fancy-tabs::shadow #panels")
        self.click("button.tab_2")
        print(self.get_text("fancy-tabs::shadow #panels"))
        self.assert_exact_text("Content Panel 2", "fancy-tabs::shadow #panels")
        self.click("button.tab_3")
        print(self.get_text("fancy-tabs::shadow #panels"))
        self.assert_exact_text("Content Panel 3", "fancy-tabs::shadow #panels")
