from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode()
    endpoint_url = sb.cdp.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto("https://seleniumbase.io/simple/login")
        page.fill("#username", "demo_user")
        page.fill("#password", "secret_pass")
        page.click("#log-in")
        page.wait_for_selector("h1")
        sb.sleep(1)
