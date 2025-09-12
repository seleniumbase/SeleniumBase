from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.researchgate.net/search/publication"
    sb.activate_cdp_mode(url)
    sb.sleep(2.2)
    shadow_head = "div.main-content div"
    if sb.is_element_present(shadow_head):
        sb.cdp.gui_click_element(shadow_head)
        sb.sleep(1.5)
    sb.assert_text("Discover the world's scientific knowledge")
    sb.click_if_visible('button[aria-label="Close"]')
    sb.highlight('h1[class*="nova"]')
    sb.highlight('input[name="q"]')
    sb.highlight("a.menu-item.selected")
    sb.sleep(1)
