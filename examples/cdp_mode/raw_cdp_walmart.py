from seleniumbase import sb_cdp

url = "https://www.walmart.com/"
sb = sb_cdp.Chrome(url, locale="en", guest=True)
sb.sleep(3)
sb.click('input[aria-label="Search"]')
sb.sleep(1.4)
search = "Settlers of Catan Board Game"
required_text = "Catan"
sb.press_keys('input[aria-label="Search"]', search + "\n")
sb.sleep(3.8)
if sb.is_element_visible("#px-captcha"):
    sb.gui_click_and_hold("#px-captcha", 7.2)
    sb.sleep(4.2)
    if sb.is_element_visible("#px-captcha"):
        sb.gui_click_and_hold("#px-captcha", 4.2)
        sb.sleep(3.2)
sb.remove_elements('[data-testid="skyline-ad"]')
sb.remove_elements('[data-testid="sba-container"]')
print('*** Walmart Search for "%s":' % search)
print('    (Results must contain "%s".)' % required_text)
unique_item_text = []
items = sb.find_elements('div[data-testid="list-view"]')
for item in items:
    if required_text in item.text:
        description = item.querySelector(
            '[data-automation-id="product-title"]'
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
sb.driver.stop()
