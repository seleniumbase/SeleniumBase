from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://news.ycombinator.com/submitted?id=seleniumbase")
    items = page.locator("span.titleline > a")
    for i in range(items.count()):
        item_text = items.nth(i).inner_text()
        print("* " + item_text)
