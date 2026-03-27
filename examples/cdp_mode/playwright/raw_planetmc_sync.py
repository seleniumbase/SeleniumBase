from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://www.planetminecraft.com/account/sign_in/")
    page.wait_for_timeout(2000)
    sb.solve_captcha()
    input_disabled = page.locator("input[disabled]")
    input_disabled.wait_for(state="hidden", timeout=5000)
    page.wait_for_timeout(2000)
