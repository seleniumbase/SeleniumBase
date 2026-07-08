from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(ad_block=True)
sb.goto("https://www.etsy.com/")
sb.sleep(1)
search = "FIFA Keychains"
required_text = "keychain"
sb.type('input[data-id="search-query"]', search)
sb.sleep(1)
sb.click('button[aria-label="Search"]')
sb.sleep(2)
sb.click_if_visible('button[aria-label="Ok"]')
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    items = page.locator("div.v2-listing-card__info")
    num = 0
    for i in range(items.count()):
        title = items.nth(i).locator("h3.v2-listing-card__title").inner_text()
        price = items.nth(i).locator("div.n-listing-card__price").inner_text()
        if required_text.lower() in title.lower():
            num += 1
            title = " ".join(title.split()).strip()
            price = price.replace("Sale Price", "").strip().split("\n")[0]
            print(f"* <====== {num} ======>")
            print(title)
            print(price.strip().split("\n")[0])
    print(f"*** {num} total items found!")
