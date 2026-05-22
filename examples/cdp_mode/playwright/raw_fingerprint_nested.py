from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True, locale="en") as sb:
    sb.activate_cdp_mode()
    endpoint_url = sb.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        page.goto("https://demo.fingerprint.com/playground")
        page.wait_for_timeout(500)
        sb.flash('a[href*="browser-bot-detection"]', duration=3, pause=1)
        bot_row_selector = 'table:contains("Bot") tr:nth-of-type(3)'
        print(sb.get_text(bot_row_selector))
        sb.assert_text("Bot Not detected", bot_row_selector)
        sb.flash(bot_row_selector, duration=3, pause=2)
