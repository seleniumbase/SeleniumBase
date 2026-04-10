"""Hybrid TestCase Example"""
from playwright.sync_api import sync_playwright, expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc")


class HybridTestCase(BaseCase):
    def test_add_item_to_cart(self):
        self.activate_cdp_mode()
        self.reconnect()  # Reconnects WebDriver to use Selenium
        driver = self.driver  # Selenium API
        endpoint_url = self.cdp.get_endpoint_url()
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            page = browser.contexts[0].pages[0]  # Playwright API

            # This section uses Selenium
            driver.get("https://www.saucedemo.com")
            by_css = By.CSS_SELECTOR  # "css selector"
            element = driver.find_element(by_css, "#user-name")
            element.send_keys("standard_user")
            element = driver.find_element(by_css, "#password")
            element.send_keys("secret_sauce")
            element.submit()
            driver.find_element(by_css, "div.inventory_list")
            element = driver.find_element(by_css, "span.title")
            self.assertEqual(element.text, "Products")

            # This section uses Playwright
            page.click('button[name*="backpack"]')
            page.click("#shopping_cart_container a")
            expect(page.locator("span.title")).to_have_text("Your Cart")
            expect(page.locator("div.cart_item")).to_contain_text("Backpack")

            # This section uses SeleniumBase
            self.click("#remove-sauce-labs-backpack")
            self.assert_element_not_visible("div.cart_item")

            # This section uses Selenium
            driver.find_element(by_css, "#react-burger-menu-btn").click()
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by_css, "a#logout_sidebar_link"))
            )
            element.click()
            driver.find_element(by_css, "input#login-button")
