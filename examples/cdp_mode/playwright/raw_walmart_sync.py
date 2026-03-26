from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en", guest=True)
sb.open("https://www.walmart.com/")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.wait_for_timeout(2800)
    page.click('input[aria-label="Search"]')
    page.wait_for_timeout(1800)
    search = "Settlers of Catan Board Game"
    required_text = "Catan"
    input_selector = 'input[aria-label="Search"]'
    search_box = page.locator(input_selector)
    search_box.press_sequentially(search + "\n", delay=80)
    page.wait_for_timeout(3200)
    sb.remove_elements('[data-testid="skyline-ad"]')
    sb.remove_elements('[data-testid="sba-container"]')
    print('*** Walmart Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item = []
    pop_up = '[data-automation-id="sb-btn-close-mark"]'
    if page.locator(pop_up).count() > 0:
        page.click(pop_up)
    page.wait_for_timeout(1200)
    page.wait_for_selector('[data-item-id]', timeout=10000)
    page.wait_for_timeout(600)
    items = page.locator('[data-item-id]')
    for i in range(items.count()):
        item = items.nth(i)
        if required_text in item.inner_text():
            description = item.locator('[data-automation-id="product-title"]')
            if (
                description
                and description.is_visible()
                and description.inner_text() not in unique_item
            ):
                unique_item.append(description.inner_text())
                price = item.locator('[data-automation-id="product-price"]')
                if price.count() > 0:
                    print("* " + description.inner_text())
                    price_text = price.inner_text()
                    price_text = price_text.split("current price Now ")[-1]
                    price_text = price_text.split("current price ")[-1]
                    price_text = price_text.split(" ")[0]
                    print("  (" + price_text + ")")
