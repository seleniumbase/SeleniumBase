from seleniumbase import SB

with SB(uc=True, test=True, incognito=True) as sb:
    url = "https://seleniumbase.io/other/drag_and_drop"
    sb.activate_cdp_mode(url)
    sb.assert_element_not_visible("#div1 img#drag1")
    sb.cdp.gui_drag_and_drop("#drag1", "#div1")
    sb.assert_element("#div1 img#drag1")
    sb.sleep(1)

with SB(uc=True, test=True, incognito=True) as sb:
    url = "https://jqueryui.com/draggable/"
    sb.activate_cdp_mode(url)
    sb.switch_to_frame("iframe")
    x, y = sb.get_gui_element_center("#draggable")
    sb.switch_to_default_content()
    sb.scroll_to_top()
    sb.cdp.gui_drag_drop_points(x, y, x + 180, y + 90)
    sb.cdp.gui_drag_drop_points(x + 180, y + 90, x + 60, y + 120)
    sb.cdp.gui_drag_drop_points(x + 60, y + 120, x + 40, y + 40)
    sb.sleep(1)
