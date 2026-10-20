from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(fast=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://hn.algolia.com/?query=seleniumbase")
    items = page.locator("div.Story_title > a")
    for i in range(items.count()):
        item_text = items.nth(i).inner_text()
        print("* " + item_text)
