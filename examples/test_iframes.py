from seleniumbase import BaseCase


class FrameTests(BaseCase):
    def test_iframe_basics(self):
        self.open("https://seleniumbase.io/w3schools/iframes.html")
        self.switch_to_frame("iframeResult")  # Enter the iframe
        self.assert_text("HTML Iframes", "h2")
        self.switch_to_frame('[title*="Iframe"]')  # Enter iframe inside iframe
        self.assert_text("This page is displayed in an iframe", "h1")
        self.switch_to_default_content()  # Exit all iFrames
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")  # Go back inside 1st iframe
        self.highlight('iframe[title="Iframe Example"]')

    def test_set_content_to_frame(self):
        self.open("https://seleniumbase.io/w3schools/iframes.html")
        self.set_content_to_frame("iframeResult")
        self.highlight('iframe[title="Iframe Example"]')
        self.set_content_to_frame("iframe")
        self.assert_element_not_visible('iframe')
        self.highlight("body")
        self.set_content_to_default(nested=False)
        self.highlight('iframe[title="Iframe Example"]')
        self.set_content_to_default()
        self.click("button#runbtn")
        self.highlight("#iframeResult")
