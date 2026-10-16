# Three stealth tests in one script!
from playwright.sync_api import expect, sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(incognito=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://browserscan.net/bot-detection")
    expect(page.locator('strong:has-text("Normal")')).to_be_visible()
    page.goto("https://bot.sannysoft.com/")
    expect(page.locator(".passed").first).to_be_visible()
    expect(page.locator(".failed")).not_to_be_visible()
    page.goto("https://www.planetminecraft.com/account")
    page.locator('[name="email"]').press_sequentially("Name123", delay=105)
    page.locator('[name="password"]').press_sequentially("Pass", delay=105)
    sb.solve_captcha()
    expect(page.locator('input[name="login"]')).to_be_visible()
    expect(page.locator("input[disabled]")).not_to_be_visible()
    page.wait_for_timeout(1000)
