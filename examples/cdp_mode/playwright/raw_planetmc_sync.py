from playwright.sync_api import expect
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(incognito=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://www.planetminecraft.com/account")
    expect(page.locator('input[name="login"]')).to_be_visible()

    email_field = page.locator('input[name="email"]')
    email_field.press_sequentially("test@example.com", delay=55)
    page.locator('input[name="password"]').fill("Fake_Password")
    page.locator("input#autologin").click(force=True)

    if page.locator('input[disabled]').is_visible():
        sb.solve_captcha()  # Enables the input button
    expect(page.locator("input[disabled]")).to_be_hidden()
    page.wait_for_timeout(1500)
