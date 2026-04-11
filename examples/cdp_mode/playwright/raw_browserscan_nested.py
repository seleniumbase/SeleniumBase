from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True, locale="en") as sb:
    sb.activate_cdp_mode()
    endpoint_url = sb.cdp.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        page.goto("https://www.browserscan.net/bot-detection")
        page.wait_for_timeout(1000)
        sb.cdp.flash("Test Results", duration=4)
        page.wait_for_timeout(1000)
        sb.assert_element('strong:contains("Normal")')
        sb.cdp.flash('strong:contains("Normal")', duration=4, pause=4)
