"""Use SeleniumBase methods to interact with "canvas" elements."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CanvasTests(BaseCase):
    def get_pixel_colors(self):
        # Return the RGB colors of the canvas element's top left pixel
        x = 0
        y = 0
        if self.browser == "safari":
            x = 1
            y = 1
        color = self.execute_script(
            "return document.querySelector('canvas').getContext('2d')"
            ".getImageData(%s,%s,1,1).data;" % (x, y)
        )
        if self.is_chromium():
            return [color[0], color[1], color[2]]
        else:
            return [color["0"], color["1"], color["2"]]

    def test_canvas_click_from_center(self):
        self.open("https://seleniumbase.io/other/canvas")
        self.assert_title_contains("Canvas")
        self.click_with_offset("canvas", 0, 0, mark=True, center=True)
        self.sleep(0.55)  # Not needed (Lets you see the alert pop up)
        alert = self.switch_to_alert()
        self.assert_equal(alert.text, "You clicked on the square!")
        self.accept_alert()
        self.sleep(0.55)  # Not needed (Lets you see the alert go away)
        if self.browser == "safari" and self._reuse_session:
            # Alerts can freeze Safari if reusing the browser session
            self.driver.quit()

    def test_click_with_offset(self):
        self.open("https://seleniumbase.io/canvas/")
        if self.undetectable:
            self.open_if_not_url("about:blank")
            print("Skip this test in undetectable mode.")
            self.skip("Skip this test in undetectable mode.")
        self.assert_title_contains("Canvas")
        self.highlight("canvas")
        rgb = self.get_pixel_colors()
        self.assert_equal(rgb, [221, 242, 231])  # Looks greenish
        self.click_with_offset("canvas", 500, 350)
        self.highlight("canvas", loops=5)
        rgb = self.get_pixel_colors()
        self.assert_equal(rgb, [39, 42, 56])  # Blue by hamburger
