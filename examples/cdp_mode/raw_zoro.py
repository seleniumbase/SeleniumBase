from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.zoro.com/"
    sb.activate_cdp_mode()
    sb.goto(url)
    sb.sleep(1.2)
    search_box = "input#searchInput"
    search = "Flir Thermal Camera"
    required_text = "Camera"
    if not sb.is_element_present(search_box):
        sb.evaluate("window.location.reload();")
        sb.sleep(1.2)
    sb.click(search_box)
    sb.sleep(1.2)
    sb.press_keys(search_box, search)
    sb.sleep(0.6)
    sb.click('button[data-za="searchButton"]')
    sb.sleep(3.2)
    sb.wait_for_element('[data-za="product-cards-list"]', timeout=5)
    print('*** Zoro Search for "%s":' % search)
    print('    (Results must contain "%s")' % required_text)
    unique_item_text = []
    soup = sb.get_beautiful_soup()
    items = soup.select('[data-za="search-product-card"]')
    for item in items:
        item_text = item.get_text()
        if required_text.lower() in item_text.lower():
            description_element = item.select_one("h2")
            if description_element:
                description_text = description_element.get_text(strip=True)
                if description_text.lower() not in unique_item_text:
                    unique_item_text.append(description_text.lower())
                    print("* " + description_text)
                    price_element = item.select_one("div.price-main")
                    if price_element:
                        price_text = " ".join(price_element.get_text().split())
                        print("  (" + price_text + ")")
