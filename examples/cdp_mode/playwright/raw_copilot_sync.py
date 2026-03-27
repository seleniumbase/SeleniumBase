from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://copilot.microsoft.com")
    page.wait_for_selector("textarea#userInput")
    page.wait_for_timeout(1000)
    query = "Playwright Python connect_over_cdp() sync example"
    page.fill("textarea#userInput", query)
    page.click('button[data-testid="submit-button"]')
    page.wait_for_timeout(4000)
    sb.solve_captcha()
    page.wait_for_selector('button[data-testid*="-thumbs-up"]')
    page.wait_for_timeout(4000)
    page.click('button[data-testid*="scroll-to-bottom"]')
    page.wait_for_timeout(3000)
    chat_results = '[data-testid="highlighted-chats"]'
    result = page.locator(chat_results).inner_text()
    print(result.replace("\n\n", " \n"))
