from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en", guest=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://www.walmart.com/")
    sb.sleep(3)
    page.click('input[aria-label="Search"]')
    sb.sleep(1.4)
    search = "Settlers of Catan Board Game"
    required_text = "Catan"
    sb.press_keys('input[aria-label="Search"]', search + "\n")
    sb.sleep(3.8)
    sb.remove_elements('[data-testid="skyline-ad"]')
    sb.remove_elements('[data-testid="sba-container"]')
    print('*** Walmart Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item = []
    items = page.locator('div[data-testid="list-view"]')
    for i in range(items.count()):
        item = items.nth(i)
        if required_text in item.inner_text():
            description = item.locator('[data-automation-id="product-title"]')
            if description and description.inner_text() not in unique_item:
                unique_item.append(description.inner_text())
                print("* " + description.inner_text())
                price = item.locator('[data-automation-id="product-price"]')
                if price:
                    price_text = price.inner_text()
                    price_text = price_text.split("current price Now ")[-1]
                    price_text = price_text.split("current price ")[-1]
                    price_text = price_text.split(" ")[0]
                    print("  (" + price_text + ")")
