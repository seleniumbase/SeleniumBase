"""Long & Messy Raw Selenium Example - (ONLY Selenium / NO SeleniumBase)"""
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unittest import TestCase


class LongMessyRawSelenium(TestCase):
    def setUp(self):
        self.driver = None
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        if "linux" in sys.platform:
            options.add_argument("--headless=new")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"],
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

    def test_add_item_to_cart(self):
        self.driver.get("https://www.saucedemo.com")
        by_css = By.CSS_SELECTOR  # "css selector"
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, "#user-name"))
        )
        element.clear()
        element.send_keys("standard_user")
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, "#password"))
        )
        element.clear()
        element.send_keys("secret_sauce")
        element.submit()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by_css, "div.inventory_list"))
        )
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by_css, "span.title"))
        )
        self.assertEqual(element.text, "Products")
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, 'button[name*="backpack"]'))
        )
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, "#shopping_cart_container a"))
        )
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by_css, "span.title"))
        )
        self.assertEqual(element.text, "Your Cart")
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by_css, "div.cart_item"))
        )
        self.assertIn("Backpack", element.text)
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, "#remove-sauce-labs-backpack"))
        )
        element.click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element((by_css, "div.cart_item"))
        )
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, "#react-burger-menu-btn"))
        )
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by_css, "a#logout_sidebar_link"))
        )
        element.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by_css, "input#login-button"))
        )


# When run with "python" instead of "pytest" or "python -m unittest"
if __name__ == "__main__":
    from unittest import main
    main()
