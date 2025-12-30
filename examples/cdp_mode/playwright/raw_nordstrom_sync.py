from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://www.nordstrom.com/")
    sb.sleep(2)
    page.click("input#keyword-search-input")
    sb.sleep(0.8)
    search = "cocktail dresses for women teal"
    sb.press_keys("input#keyword-search-input", search + "\n")
    sb.sleep(2.2)
    for i in range(17):
        sb.scroll_down(16)
        sb.sleep(0.14)
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
