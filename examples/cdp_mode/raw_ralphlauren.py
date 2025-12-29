from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://www.ralphlauren.com.au/"
    sb.activate_cdp_mode()
    sb.open(url)
    sb.sleep(1.2)
    if not sb.is_element_present('[title="Locate Stores"]'):
        sb.cdp.evaluate("window.location.reload();")
        sb.sleep(1.2)
    category = "women"
    search = "Dresses"
    sb.click('a[data-cgid="%s"]' % category)
    sb.sleep(2.2)
    sb.click('a:contains("%s")' % search)
    sb.sleep(3.8)
    for i in range(6):
        sb.scroll_down(34)
        sb.sleep(0.25)
    print('*** Ralph Lauren Search for "%s":' % search)
    unique_item_text = []
    items = sb.find_elements('div.product-data')
    for item in items:
        description = item.querySelector("a.name-link")
        if description and description.text not in unique_item_text:
            unique_item_text.append(description.text)
            print("* " + description.text)
            price = item.querySelector('span[title="Price"]')
            if price:
                print("  (" + price.text.replace("   ", " ") + ")")
