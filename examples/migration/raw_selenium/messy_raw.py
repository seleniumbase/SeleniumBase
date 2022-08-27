"""Messy Raw Selenium Example - (This test does NOT use SeleniumBase)"""
import sys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unittest import TestCase


class MessyRawSelenium(TestCase):
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

    def wait_for_element_visible(
        self, selector, by="css selector", timeout=10
    ):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )

    def wait_for_element_clickable(
        self, selector, by="css selector", timeout=10
    ):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )

    def wait_for_element_not_visible(
        self, selector, by="css selector", timeout=10
    ):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element((by, selector))
        )

    def test_add_item_to_cart(self):
        self.driver.get("https://www.saucedemo.com")
        element = self.wait_for_element_clickable("#user-name")
        element.clear()
        element.send_keys("standard_user")
        element = self.wait_for_element_clickable("#password")
        element.clear()
        element.send_keys("secret_sauce")
        element.submit()
        self.wait_for_element_visible("div.inventory_list")
        element = self.wait_for_element_visible("span.title")
        self.assertEqual(element.text, "PRODUCTS")
        self.wait_for_element_clickable('button[name*="backpack"]').click()
        self.wait_for_element_clickable("#shopping_cart_container a").click()
        element = self.wait_for_element_visible("span.title")
        self.assertEqual(element.text, "YOUR CART")
        element = self.wait_for_element_visible("div.cart_item")
        self.assertIn("Backpack", element.text)
        self.wait_for_element_clickable("#remove-sauce-labs-backpack").click()
        self.wait_for_element_not_visible("div.cart_item")
        self.wait_for_element_clickable("#react-burger-menu-btn").click()
        self.wait_for_element_clickable("a#logout_sidebar_link").click()
        self.wait_for_element_visible("input#login-button")
