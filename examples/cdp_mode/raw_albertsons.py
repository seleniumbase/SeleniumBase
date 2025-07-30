from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.albertsons.com/recipes/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.remove_element("div > div > article")
    sb.cdp.scroll_into_view('input[type="search"]')
    close_btn = ".notification-alert-wrapper__close-button"
    sb.cdp.click_if_visible(close_btn)
    sb.cdp.click("input#search-suggestion-input")
    sb.sleep(0.2)
    search = "Avocado Smoked Salmon"
    required_text = "Salmon"
    sb.cdp.press_keys("input#search-suggestion-input", search)
    sb.sleep(0.8)
    sb.cdp.click("#suggestion-0 a span")
    sb.sleep(0.8)
    sb.cdp.click_if_visible(close_btn)
    sb.sleep(2.8)
    print('*** Albertsons Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    item_selector = 'a[href*="/meal-plans-recipes/shop/"]'
    items = sb.cdp.find_elements(item_selector)
    for item in items:
        sb.sleep(0.06)
        if required_text in item.text:
            item.flash(color="44CC88")
            sb.sleep(0.025)
            if item.text not in unique_item_text:
                unique_item_text.append(item.text)
                print("* " + item.text)
