from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://pixelscan.net/fingerprint-check")
    sb.sleep(4)
    expect(
        page.locator("pxlscn-bot-detection")
    ).to_contain_text("No automated behavior", timeout=4000)
    page.wait_for_selector("span.status-success", timeout=4000)
    expect(
        page.locator("pxlscn-fingerprint-masking")
    ).to_contain_text("No masking detected", timeout=4000)
    sb.sleep(2)
    print("Bot Not Detected")
