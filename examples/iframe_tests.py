"""Use SeleniumBase methods to interact with iframes."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class FrameTests(BaseCase):
    def test_iframe_basics(self):
        self.open("https://seleniumbase.io/w3schools/iframes.html")
        self.assert_title("iframe Testing")
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")  # Enter the iframe
        self.assert_text("HTML Iframes", "h2")
        self.switch_to_frame('[title*="Iframe"]')  # Enter iframe inside iframe
        self.assert_text("This page is displayed in an iframe", "h1")
        self.switch_to_parent_frame()  # Exit only the inner iframe
        self.assert_text("Use CSS width & height to specify", "p")
        self.switch_to_frame('[title*="Iframe"]')  # Enter iframe inside iframe
        self.assert_text("seleniumbase.io/w3schools/iframes", "a")
        self.switch_to_default_content()  # Exit all iframes
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")  # Go back inside 1st iframe
        self.highlight('iframe[title="Iframe Example"]')

    def test_iframes_with_context_manager(self):
        self.open("https://seleniumbase.io/w3schools/iframes.html")
        self.assert_title("iframe Testing")
        self.click("button#runbtn")
        with self.frame_switch("iframeResult"):
            self.assert_text("HTML Iframes", "h2")
            with self.frame_switch('[title*="Iframe"]'):
                self.assert_text("This page is displayed in an iframe", "h1")
            self.assert_text("Use CSS width & height to specify", "p")
            with self.frame_switch('[title*="Iframe"]'):
                self.assert_text("seleniumbase.io/w3schools/iframes", "a")
        self.click("button#runbtn")
        with self.frame_switch("iframeResult"):
            self.highlight('iframe[title="Iframe Example"]')

    def test_set_content_to_frame(self):
        self.open("https://seleniumbase.io/w3schools/iframes.html")
        self.assert_title("iframe Testing")
        self.click("button#runbtn")
        self.set_content_to_frame("iframeResult")
        self.highlight('iframe[title="Iframe Example"]')
        self.set_content_to_frame("iframe")
        self.assert_element_not_visible("iframe")
        self.highlight("body")
        self.set_content_to_parent()
        self.highlight('iframe[title="Iframe Example"]')
        self.set_content_to_default()
        self.click("button#runbtn")
        self.highlight("#iframeResult")
