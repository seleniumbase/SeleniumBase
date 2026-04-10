"""Raw Selenium TestCase Example"""
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unittest import TestCase


class RawSeleniumTestCase(TestCase):
    def setUp(self):
        self.driver = None
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        if "linux" in sys.platform or "--headless" in sys.argv:
            options.add_argument("--headless")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"],
        )
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        options.add_experimental_option("prefs", prefs)
        service = Service(service_args=["--disable-build-check"])
        self.driver = webdriver.Chrome(options=options, service=service)

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
        element.send_keys("standard_user")
        element = self.driver.find_element(by_css, "#password")
        element.send_keys("secret_sauce")
        element.submit()
        self.driver.find_element(by_css, "div.inventory_list")
        element = self.driver.find_element(by_css, "span.title")
        self.assertEqual(element.text, "Products")

        self.driver.find_element(by_css, 'button[name*="backpack"]').click()
        self.driver.find_element(by_css, "#shopping_cart_container a").click()
        element = self.driver.find_element(by_css, "span.title")
        self.assertEqual(element.text, "Your Cart")
        element = self.driver.find_element(by_css, "div.cart_item")
        self.assertIn("Backpack", element.text)

        self.driver.find_element(by_css, "#remove-sauce-labs-backpack").click()
        self.assertFalse(self.is_element_visible("div.cart_item"))

        self.driver.find_element(by_css, "#react-burger-menu-btn").click()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, "a#logout_sidebar_link"))
        )
        element.click()
        self.driver.find_element(by_css, "input#login-button")


if __name__ == "__main__":
    from pytest import main
    main([__file__, "-s"])
