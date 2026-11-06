from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(use_chromium=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    search = "Reddit Scraping"
    sb.goto("https://www.reddit.com/r/webscraping/")
    sb.solve_captcha()  # Might not be needed
    sb.click("faceplate-search-input")
    sb.press_keys("html", search + "\n")
    page.wait_for_timeout(2500)
    post_title = '[data-testid="post-title"]'
    page.wait_for_selector(post_title)
    for i in range(8):
        sb.scroll_down(25)
        sb.sleep(0.25)
    print('*** Reddit Posts for "%s":' % search)
    items = page.locator(post_title)
    for i in range(items.count()):
        item_text = items.nth(i).inner_text()
        print("* " + item_text)
