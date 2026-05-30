from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True, guest=True) as sb:
    sb.activate_cdp_mode()
    endpoint_url = sb.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        page.goto("https://bot.sannysoft.com/")
        page.wait_for_timeout(500)
        sb.flash("#user-agent-result.passed")
        sb.flash("#webdriver-result.passed")
        sb.flash("#advanced-webdriver-result.passed")
        sb.flash("#chrome-result.passed")
        sb.flash("#permissions-result.passed")
        sb.flash("#plugins-length-result.passed")
        sb.flash("#plugins-type-result.passed")
        sb.flash("#languages-result.passed")
        sb.flash("#webgl-vendor.passed")
        sb.flash("#webgl-renderer.passed")
        sb.flash("#broken-image-dimensions.passed")
        print("Bot Not Detected")
        sb.sleep(1)
