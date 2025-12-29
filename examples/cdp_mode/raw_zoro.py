from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.zoro.com/"
    sb.activate_cdp_mode()
    sb.open(url)
    sb.sleep(1.2)
    search_box = "input#searchInput"
    search = "Flir Thermal Camera"
    required_text = "Camera"
    if not sb.is_element_present(search_box):
        sb.cdp.evaluate("window.location.reload();")
        sb.sleep(1.2)
    sb.click(search_box)
    sb.sleep(1.2)
    sb.press_keys(search_box, search)
    sb.sleep(0.6)
    sb.click('button[data-za="searchButton"]')
    sb.sleep(3.8)
    print('*** Zoro Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    items = sb.find_elements('div[data-za="search-product-card"]')
    for item in items:
        if required_text in item.text:
            description = item.querySelector('div[data-za="product-title"]')
            if description and description.text not in unique_item_text:
                unique_item_text.append(description.text)
                print("* " + description.text)
                price = item.querySelector("div.price-main")
                if price:
                    print("  (" + price.text + ")")
