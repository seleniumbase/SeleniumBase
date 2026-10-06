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
    sb.sleep(0.2)
    sb.click('[value="Google Search"]')
    sb.sleep(4)  # The "AI Overview" sometimes loads
    print(page.title())
    sb.save_as_pdf("google_page.pdf", folder="./downloaded_files/")
    print("* PDF saved to ./downloaded_files/google_page.pdf")
    sb.click_if_visible('h3:contains("seleniumbase/SeleniumBase")')
    sb.sleep(1)
    sb.save_as_pdf("seleniumbase.pdf", folder="./downloaded_files/")
    print("* PDF saved to ./downloaded_files/seleniumbase.pdf")
