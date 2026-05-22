from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True, locale="en", ad_block=True) as sb:
    sb.activate_cdp_mode()
    endpoint_url = sb.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        page.goto("https://browserscan.net/bot-detection")
        page.wait_for_timeout(500)
        sb.flash("Test Results", duration=1.5, pause=0.5)
        sb.assert_element('strong:contains("Normal")')
        print("Bot Not Detected")
        sb.flash('strong:contains("Normal")', pause=1)
