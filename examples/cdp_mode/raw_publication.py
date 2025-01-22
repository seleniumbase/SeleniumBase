from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", ad_block=True) as sb:
    url = "https://www.researchgate.net/search/publication"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    if sb.cdp.is_element_visible("p.spacer-bottom"):
        sb.uc_gui_click_captcha()
    shadow_head = "div.main-content div"
    if sb.is_element_present(shadow_head):
        sb.cdp.gui_click_element(shadow_head)
        sb.sleep(1.5)
    sb.cdp.click_if_visible('button[aria-label="Close"]')
    sb.cdp.remove_elements('div[class*="ad-container"]')
    sb.cdp.remove_elements("div.lite-page-ad")
    sb.sleep(0.5)
    sb.assert_text("Discover the world's scientific knowledge")
    sb.highlight('h1[class*="nova"]')
    sb.highlight('input[name="q"]')
    sb.highlight("a.menu-item.selected")
    sb.sleep(1)
