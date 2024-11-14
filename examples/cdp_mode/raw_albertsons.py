from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.albertsons.com/recipes/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.remove_element("div > div > article")
    sb.cdp.scroll_into_view('input[type="search"]')
    sb.cdp.click_if_visible("button.banner-close-button")
    sb.cdp.click("input#search-suggestion-input")
    sb.sleep(0.2)
    search = "Avocado Smoked Salmon"
    required_text = "Salmon"
    sb.cdp.press_keys("input#search-suggestion-input", search)
    sb.sleep(0.8)
    sb.cdp.click("#suggestion-0 a span")
    sb.sleep(3.2)
    sb.cdp.click_if_visible("button.banner-close-button")
    sb.sleep(1.2)
    print('*** Albertsons Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    item_selector = 'a[href*="/meal-plans-recipes/shop/"]'
    info_selector = 'span[data-test-id*="recipe-thumb-title"]'
    items = sb.cdp.find_elements("%s %s" % (item_selector, info_selector))
    for item in items:
        sb.sleep(0.03)
        item.scroll_into_view()
        sb.sleep(0.025)
        if required_text in item.text:
            item.flash(color="44CC88")
            sb.sleep(0.025)
            if item.text not in unique_item_text:
                unique_item_text.append(item.text)
                print("* " + item.text)
