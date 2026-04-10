import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def is_element_visible(driver, selector, by="css selector"):
    try:
        element = driver.find_element(by, selector)
        if element.is_displayed():
            return True
    except Exception:
        pass
    return False


options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
if "linux" in sys.platform:
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


with webdriver.Chrome(options=options, service=service) as driver:
    driver.get("https://www.saucedemo.com")
    by_css = By.CSS_SELECTOR  # "css selector"
    element = driver.find_element(by_css, "#user-name")
    element.send_keys("standard_user")
    element = driver.find_element(by_css, "#password")
    element.send_keys("secret_sauce")
    element.submit()
    driver.find_element(by_css, "div.inventory_list")
    element = driver.find_element(by_css, "span.title")
    assert element.text == "Products"

    driver.find_element(by_css, 'button[name*="backpack"]').click()
    driver.find_element(by_css, "#shopping_cart_container a").click()
    element = driver.find_element(by_css, "span.title")
    assert element.text == "Your Cart"
    element = driver.find_element(by_css, "div.cart_item")
    assert "Backpack" in element.text

    driver.find_element(by_css, "#remove-sauce-labs-backpack").click()
    assert not is_element_visible(driver, "div.cart_item")

    driver.find_element(by_css, "#react-burger-menu-btn").click()
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by_css, "a#logout_sidebar_link"))
    )
    element.click()
    driver.find_element(by_css, "input#login-button")
