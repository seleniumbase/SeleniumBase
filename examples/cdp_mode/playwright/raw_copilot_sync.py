from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://copilot.microsoft.com")
    page.wait_for_selector("textarea#userInput")
    sb.sleep(1)
    query = "Playwright Python connect_over_cdp() sync example"
    page.fill("textarea#userInput", query)
    page.click('button[data-testid="submit-button"]')
    sb.sleep(3)
    sb.solve_captcha()
    page.wait_for_selector('button[data-testid*="-thumbs-up"]')
    sb.sleep(4)
    page.click('button[data-testid*="scroll-to-bottom"]')
    sb.sleep(3)
    chat_results = '[data-testid="highlighted-chats"]'
    result = page.locator(chat_results).inner_text()
    print(result.replace("\n\n", " \n"))
