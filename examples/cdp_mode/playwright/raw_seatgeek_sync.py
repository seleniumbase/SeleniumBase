from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en", ad_block=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://seatgeek.com/")
    input_field = 'input[name="search"]'
    page.wait_for_selector(input_field)
    page.wait_for_timeout(1600)
    query = "Jerry Seinfeld"
    search_box = page.locator(input_field)
    search_box.press_sequentially(query, delay=80)
    page.wait_for_timeout(1600)
    page.click("li#active-result-item")
    page.wait_for_timeout(4200)
    print('*** SeatGeek Search for "%s":' % query)
    items = page.locator('[data-testid="listing-item"]')
    for i in range(items.count()):
        item_text = items.nth(i).inner_text()
        print(item_text.replace("\n\n", "\n"))
