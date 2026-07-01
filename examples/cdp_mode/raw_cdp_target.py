from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.target.com/")
sb.sleep(1.5)
sb.click("input#search")
sb.sleep(0.5)
search = "Settlers of Catan Board Game"
required_text = "Catan"
sb.type("input#search", search)
sb.sleep(0.5)
sb.click('button[aria-label="search"]')
sb.sleep(2.5)
print('*** Target Search for "%s":' % search)
print('    (Results must contain "%s".)' % required_text)
unique_item_text = []
items = sb.find_elements('[data-test="product-details"]')
for item in items:
    if required_text.lower() in item.text.lower():
        description = item.querySelector('a[data-test*="Card/title"]')
        if description and description.text not in unique_item_text:
            unique_item_text.append(description.text)
            print("* " + description.text)
            price = item.querySelector('[data-test="current-price"]')
            if price:
                print("  (" + price.text + ")")
                item.scroll_into_view()
