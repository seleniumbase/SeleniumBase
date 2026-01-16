from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(use_chromium=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    search = "reddit+scraper"
    url = f"https://www.reddit.com/r/webscraping/search/?q={search}"
    page.goto(url)
    sb.solve_captcha()  # Might not be needed
    sb.sleep(1)
    post_title = '[data-testid="post-title"]'
    page.wait_for_selector(post_title)
    for i in range(8):
        sb.scroll_down(25)
        sb.sleep(0.2)
    print('*** Reddit Posts for "%s":' % search)
    items = page.locator(post_title)
    for i in range(items.count()):
        item_text = items.nth(i).inner_text()
        print("* " + item_text)
