from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.walmart.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.mouse_click('input[aria-label="Search"]')
    sb.sleep(1.2)
    search = "Settlers of Catan Board Game"
    required_text = "Catan"
    sb.cdp.press_keys('input[aria-label="Search"]', search + "\n")
    sb.sleep(3.8)
    print('*** Walmart Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    items = sb.cdp.find_elements('div[data-testid="list-view"]')
    for item in items:
        if required_text in item.text:
            description = item.querySelector(
                '[data-automation-id="product-price"] + span'
            )
            if description and description.text not in unique_item_text:
                unique_item_text.append(description.text)
                print("* " + description.text)
                price = item.querySelector(
                    '[data-automation-id="product-price"]'
                )
                if price:
                    price_text = price.text
                    price_text = price_text.split("current price Now ")[-1]
                    price_text = price_text.split("current price ")[-1]
                    price_text = price_text.split(" ")[0]
                    print("  (" + price_text + ")")
