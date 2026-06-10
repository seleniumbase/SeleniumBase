from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://google.com/ncr")
    sb.click_if_visible('button:contains("Accept all")')
    page.type('[name="q"]', "SeleniumBase GitHub page")
    sb.click('[value="Google Search"]')
    sb.sleep(4)  # The "AI Overview" sometimes loads
    print(page.title())
    sb.save_as_pdf("google_page.pdf", folder="./downloaded_files/")
    print("PDF saved to ./downloaded_files/google_page.pdf")
