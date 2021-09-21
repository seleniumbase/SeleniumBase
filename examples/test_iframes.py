from seleniumbase import BaseCase


class FrameTests(BaseCase):
    def test_iframe_basics(self):
        self.open(
            "https://www.w3schools.com/html/tryit.asp"
            "?filename=tryhtml_iframe_height_width_css"
        )
        self.ad_block()  # Reduce noise during automation
        self.switch_to_frame("iframeResult")  # Enter the iFrame
        self.assert_text("HTML Iframes", "h2")
        self.switch_to_frame('[title*="Iframe"]')  # Enter iFrame inside iFrame
        self.assert_text("This page is displayed in an iframe", "h1")
        self.switch_to_default_content()  # Exit all iFrames
        self.switch_to_frame("iframeResult")  # Go back inside 1st iFrame
        self.highlight('iframe[title="Iframe Example"]')

    def test_set_content_to_frame(self):
        self.open(
            "https://www.w3schools.com/html/tryit.asp"
            "?filename=tryhtml_iframe_height_width_css"
        )
        self.set_content_to_frame("iframeResult")
        self.highlight('iframe[title="Iframe Example"]', loops=8)
