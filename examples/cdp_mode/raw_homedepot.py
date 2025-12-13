from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.homedepot.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(1.8)
    search_box = "input#typeahead-search-field-input"
    search = "Computer Chair"
    category = "Gaming Chairs"
    required_text = "Chair"
    sb.click(search_box)
    sb.sleep(1.2)
    sb.press_keys(search_box, search)
    sb.sleep(0.6)
    sb.click("button#typeahead-search-icon-button")
    sb.sleep(3.8)
    sb.click('a[aria-label="%s"]' % category)
    sb.sleep(3.2)
    print('*** Home Depot Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    items = sb.find_elements('div[data-testid="product-pod"]')
    for item in items:
        if required_text in item.text:
            description = item.querySelector(
                'span[data-testid="attribute-product-label"]'
            )
            if description and description.text not in unique_item_text:
                unique_item_text.append(description.text)
                print("* " + description.text)
                price = item.querySelector('[class*="sm:sui-text-4xl"]')
                if price:
                    price_text = "$%s" % price.text
                    print("  (" + price_text + ")")
