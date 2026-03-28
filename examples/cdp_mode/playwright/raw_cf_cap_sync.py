from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://www.cloudflare.com/login")
    page.wait_for_timeout(5000)
    sb.solve_captcha()
    page.wait_for_timeout(3000)
