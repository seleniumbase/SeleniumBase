"""Flaky Raw Selenium Example - (This test does NOT use SeleniumBase)"""
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest import TestCase


class FlakyMessyRawSelenium(TestCase):
    def setUp(self):
        self.driver = None
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        if "linux" in sys.platform:
            options.add_argument("--headless")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"],
        )
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        if self.driver:
            try:
                if self.driver.service.process:
                    self.driver.quit()
            except Exception:
                pass

    def is_element_visible(self, selector, by="css selector"):
        try:
            element = self.driver.find_element(by, selector)
            if element.is_displayed():
                return True
        except Exception:
            pass
        return False

    def test_add_item_to_cart(self):
        self.driver.get("https://www.saucedemo.com")
        by_css = By.CSS_SELECTOR  # "css selector"
        element = self.driver.find_element(by_css, "#user-name")
        element.clear()
        element.send_keys("standard_user")
        element = self.driver.find_element(by_css, "#password")
        element.clear()
        element.send_keys("secret_sauce")
        element.submit()
        self.driver.find_element(by_css, "div.inventory_list")
        element = self.driver.find_element(by_css, "span.title")
        self.assertEqual(element.text, "PRODUCTS")
        self.driver.find_element(by_css, 'button[name*="backpack"]').click()
        self.driver.find_element(by_css, "#shopping_cart_container a").click()
        element = self.driver.find_element(by_css, "span.title")
        self.assertEqual(element.text, "YOUR CART")
        element = self.driver.find_element(by_css, "div.cart_item")
        self.assertIn("Backpack", element.text)
        self.driver.find_element(by_css, "#remove-sauce-labs-backpack").click()
        self.assertFalse(self.is_element_visible("div.cart_item"))
        self.driver.find_element(by_css, "#react-burger-menu-btn").click()
        self.driver.find_element(by_css, "a#logout_sidebar_link").click()
        self.driver.find_element(by_css, "input#login-button")
