from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://gitlab.com/users/sign_in")
    sb.sleep(3)
    sb.solve_captcha()
    sb.sleep(1)
    page.locator('label[for="user_login"]').click()
    page.wait_for_selector('[data-testid="sign-in-button"]')
    page.locator("#user_login").fill("Username")
    sb.sleep(2)
