from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(use_chromium=True)
sb.goto("https://www.net-a-porter.com/")
sb.sleep(3)
sb.click('icon[aria-label="Search"]')
sb.sleep(1)
search = "Leather gloves"
sb.press_keys("form input", search)
sb.sleep(3)
print('*** NET-A-PORTER Search for "%s":' % search)
unique_item_text = []
items = sb.find_elements("li.ProductSearchResults2__product")
for item in items:
    description = item.query_selector("span[data-product-id]")
    if description and description.text not in unique_item_text:
        unique_item_text.append(description.text)
        price_text = ""
        price = item.query_selector('div[class*="__price"]')
        if price:
            price_text = price.text
            print("* %s (%s)" % (description.text, price_text))
            item.flash(color="44CC88")
sb.quit()
