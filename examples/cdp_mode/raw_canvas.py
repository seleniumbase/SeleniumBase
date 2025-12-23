"""Use SeleniumBase to interact with "canvas" elements."""
from seleniumbase import SB


def get_canvas_pixel_colors_at_top_left(sb):
    # Return the RGB colors of the canvas's top left pixel
    color = sb.cdp.evaluate(
        "document.querySelector('canvas').getContext('2d')"
        ".getImageData(%s,%s,1,1).data;" % (0, 0)
    )
    return [color["0"], color["1"], color["2"]]


with SB(uc=True, test=True) as sb:
    # Testing sb.cdp.click_with_offset()
    url = "https://seleniumbase.io/canvas/"
    sb.activate_cdp_mode(url)
    sb.assert_title_contains("Canvas")
    sb.highlight("canvas")
    rgb = get_canvas_pixel_colors_at_top_left(sb)
    sb.assert_equal(rgb, [221, 242, 231])  # Looks greenish
    sb.cdp.click_with_offset("canvas", 500, 350)
    sb.highlight("canvas", loops=5)
    rgb = get_canvas_pixel_colors_at_top_left(sb)
    sb.assert_equal(rgb, [39, 43, 56])  # Blue by hamburger

with SB(uc=True, test=True) as sb:
    # Testing sb.cdp.gui_click_with_offset()
    url = "https://seleniumbase.io/other/canvas"
    sb.activate_cdp_mode(url)
    sb.assert_title_contains("Canvas")
    sb.cdp.click_with_offset("canvas", 0, 0, center=True)
    sb.sleep(1)
    sb.uc_gui_press_key("ENTER")
    sb.sleep(0.5)
