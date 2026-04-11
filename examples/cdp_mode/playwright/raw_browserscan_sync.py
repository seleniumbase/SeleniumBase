from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://www.browserscan.net/bot-detection")
    page.wait_for_timeout(1000)
    sb.flash("Test Results", duration=4)
    page.wait_for_timeout(1000)
    sb.assert_element('strong:contains("Normal")')
    sb.flash('strong:contains("Normal")', duration=4, pause=4)
