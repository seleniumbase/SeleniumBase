from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.homedepot.com/")
    sb.sleep(1.5)
    sb.click_if_visible('[data-testid="CloseIcon"]', timeout=3)
    sb.sleep(1.2)
    search_box = "input#typeahead-search-field-input"
    search = "Computer Chair"
    category = "Gaming Chairs"
    required_text = "Chair"
    sb.click(search_box)
    sb.sleep(0.8)
    sb.press_keys(search_box, search)
    sb.sleep(0.6)
    sb.click("button#typeahead-search-icon-button")
    sb.sleep(3.8)
    sb.click('a[aria-label="%s"]' % category)
    sb.sleep(3.8)
    print('*** Home Depot Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    product_pod = 'div[data-testid="product-pod"]'
    sb.wait_for_element(product_pod)
    soup = sb.get_beautiful_soup()
    items = soup.select(product_pod)
    for item in items:
        item_text = item.get_text()
        if required_text in item_text:
            description = item.select_one(
                'span[data-testid="attribute-product-label"]'
            )
            if description:
                description_text = description.get_text(strip=True)
                if description_text not in unique_item_text:
                    unique_item_text.append(description_text)
                    print("* " + description_text)
                    price = item.select_one('[class*="sm:sui-text-4xl"]')
                    if price:
                        price_text = "$%s" % price.get_text(strip=True)
                        print("   (" + price_text + ")")
