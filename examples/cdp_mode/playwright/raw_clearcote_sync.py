from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://www.clearcotelabs.com/audit")
    sb.click('button[aria-label="Marker 1"]')
    sb.click('button[aria-label="Marker 2"]')
    sb.click('button[aria-label="Marker 3"]')
    sb.press_keys("input", "audit")
    sb.set_value('input[type="range"]', "100")
    sb.click_and_hold("button[data-interaction-hold]")
    sb.select_option_by_text("select", "Mouse")
    sb.click('button:contains("Run the audit")')
    sb.sleep(6)
    sb.assert_element("div.text-successText", timeout=10)
    try:
        sb.assert_text("100", "div.text-successText", timeout=5)
        sb.highlight('div.text-successText:contains("100")')
        print(" ✅ The browser fingerprint is clean! Score: 100")
    except Exception:
        score = sb.get_text("div.text-successText")
        print(f" ❌ Fingerprint tampering detected! Score: {score}")
    sb.sleep(1)
