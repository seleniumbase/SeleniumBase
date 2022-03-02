from seleniumbase import BaseCase


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
            return [color['0'], color['1'], color['2']]

    def test_canvas_actions(self):
        self.open("https://seleniumbase.io/canvas/")
        self.highlight("canvas")
        rgb = self.get_pixel_colors()
        self.assert_equal(rgb, [221, 242, 231])  # Looks greenish
        self.click_with_offset("canvas", 500, 350)
        self.highlight("canvas")
        rgb = self.get_pixel_colors()
        self.assert_equal(rgb, [39, 42, 56])  # Blue by hamburger

    def test_canvas_click(self):
        self.open("https://seleniumbase.io/other/canvas")
        self.click_with_offset("canvas", 300, 200)
        self.sleep(1)  # Not needed (Lets you see the alert pop up)
        alert = self.switch_to_alert()
        self.assert_equal(alert.text, "You clicked on the square!")
        self.accept_alert()
        self.sleep(1)  # Not needed (Lets you see the alert go away)
