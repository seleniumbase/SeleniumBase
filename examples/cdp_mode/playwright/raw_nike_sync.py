from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://www.nike.com/")
    page.click('[data-testid="user-tools-container"] search')
    search = "Pegasus"
    page.fill('input[type="search"]', search)
    sb.sleep(4)
    details = 'ul[data-testid*="products"] figure .details'
    items = page.locator(details)
    if items:
        print('**** Found results for "%s": ****' % search)
    for i in range(items.count()):
        item = items.nth(i)
        print(item.inner_text())
