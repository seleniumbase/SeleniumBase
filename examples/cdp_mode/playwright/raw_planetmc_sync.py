from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://www.planetminecraft.com/account/sign_in/")
    sb.sleep(2)
    sb.solve_captcha()
    sb.wait_for_element_absent("input[disabled]")
    sb.sleep(2)
