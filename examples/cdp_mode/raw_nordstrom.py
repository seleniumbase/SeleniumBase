from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://www.nordstrom.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.2)
    sb.cdp.click("input#keyword-search-input")
    sb.sleep(0.8)
    search = "cocktail dresses for women teal"
    sb.cdp.press_keys("input#keyword-search-input", search + "\n")
    sb.sleep(2.2)
    for i in range(16):
        sb.cdp.scroll_down(16)
        sb.sleep(0.16)
    print('*** Nordstrom Search for "%s":' % search)
    unique_item_text = []
    items = sb.cdp.find_elements("article")
    for item in items:
        description = item.querySelector("article h3")
        if description and description.text not in unique_item_text:
            unique_item_text.append(description.text)
            price_text = ""
            price = item.querySelector('div div span[aria-hidden="true"]')
            if price:
                price_text = price.text
            print("* %s (%s)" % (description.text, price_text))
