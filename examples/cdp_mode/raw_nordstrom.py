from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.nordstrom.com/")
    sb.sleep(2.2)
    sb.click("input#keyword-search-input")
    sb.sleep(0.8)
    search = "cocktail dresses for women teal"
    sb.press_keys("input#keyword-search-input", search + "\n")
    sb.sleep(2.2)
    print('*** Nordstrom Search for "%s":' % search)
    unique_item_text = []
    items = sb.find_elements("article")
    for item in items:
        description = item.querySelector("article h3")
        if description and description.text not in unique_item_text:
            unique_item_text.append(description.text)
            price_text = ""
            price = item.querySelector('div div span[aria-hidden="true"]')
            if price:
                price_text = price.text
                print("* %s (%s)" % (description.text, price_text))
                item.flash(color="44CC88")
