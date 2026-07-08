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
    soup = sb.get_beautiful_soup()
    items = soup.select('div.product-data')
    for item in items:
        description_element = item.select_one("a.name-link")
        if description_element:
            description_text = description_element.get_text(strip=True)
            if description_text not in unique_item_text:
                unique_item_text.append(description_text)
                print(f"* {description_text}")
                price_element = item.select_one('span[title="Price"]')
                if price_element:
                    price_text = " ".join(price_element.get_text().split())
                    print(f"  ({price_text})")
                    sb.scroll_down(20)
