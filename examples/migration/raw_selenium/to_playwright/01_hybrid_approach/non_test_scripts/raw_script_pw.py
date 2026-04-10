from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_context().new_page()
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.press("#password", "Enter")
    expect(page.locator("div.inventory_list")).to_be_visible()
    expect(page.locator("span.title")).to_contain_text("Products")

    page.click('button[name*="backpack"]')
    page.click("#shopping_cart_container a")
    expect(page.locator("span.title")).to_have_text("Your Cart")
    expect(page.locator("div.cart_item")).to_contain_text("Backpack")

    page.click("#remove-sauce-labs-backpack")
    expect(page.locator("div.cart_item")).to_be_hidden()

    page.click("#react-burger-menu-btn")
    page.click("a#logout_sidebar_link")
    expect(page.locator("input#login-button")).to_be_visible()
