from seleniumbase import SB

with SB(uc=True, test=True, locale="en", guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("www.ralphlauren.com.au/women/clothing/dresses-and-jumpsuits")
    sb.sleep(2.2)
    if not sb.is_element_present("div.product-data"):
        sb.evaluate("window.location.reload();")
        sb.sleep(2.2)
    print("*** Ralph Lauren Search for Dresses:")
    unique_item_text = []
    items = sb.find_elements('div.product-data')
    for item in items:
        description = item.query_selector("a.name-link")
        if description and description.text not in unique_item_text:
            unique_item_text.append(description.text)
            print("* " + description.text)
            price = item.query_selector('span[title="Price"]')
            if price:
                print("  (" + price.text.replace("   ", " ") + ")")
                item.scroll_into_view()
