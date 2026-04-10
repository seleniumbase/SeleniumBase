<!-- SeleniumBase Docs -->

## 🛠️ Standalone Automation Scripts (Non-Test)

This folder contains examples for users who need to perform web automation **without** using a test runner like `pytest` or `unittest`.

By using the hybrid approach seen in [raw_hybrid_script.py](./raw_hybrid_script.py), SeleniumBase has effectively bridged the gap between raw Selenium and Playwright in order to ease the migration process.

```python
"""Hybrid Script Example"""
from playwright.sync_api import sync_playwright, expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import SB


with SB(uc=True) as sb:  # SeleniumBase API
    sb.activate_cdp_mode()
    sb.reconnect()  # Reconnects WebDriver to use Selenium
    driver = sb.driver  # Selenium API
    endpoint_url = sb.cdp.get_endpoint_url()
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
        assert element.text == "Products"

        # This section uses Playwright
        page.click('button[name*="backpack"]')
        page.click("#shopping_cart_container a")
        expect(page.locator("span.title")).to_have_text("Your Cart")
        expect(page.locator("div.cart_item")).to_contain_text("Backpack")

        # This section uses SeleniumBase
        sb.click("#remove-sauce-labs-backpack")
        sb.assert_element_not_visible("div.cart_item")

        # This section uses Selenium
        driver.find_element(by_css, "#react-burger-menu-btn").click()
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((by_css, "a#logout_sidebar_link"))
        )
        element.click()
        driver.find_element(by_css, "input#login-button")
```

This folder also includes standalone scripts for raw Selenium, Playwright, and SeleniumBase, which serve as foundational components for the hybrid script that integrates all three.

### 💡 Why use Standalone Scripts?
While test runners are excellent for verification and reporting, standalone scripts are often preferred for:
* **Web Scraping:** Extracting data from sites without the overhead of a test framework.
* **DevOps/Utility Tasks:** Automating repetitive browser-based tasks or health checks.
* **Rapid Prototyping:** Testing out a new automation flow quickly before formalizing it into a test suite.

### 🌉 The "SB" Advantage
The `raw_hybrid_script.py` example demonstrates how to use the **`SB()` context manager**. This is a powerful feature of SeleniumBase that allows you to:
1. **Bridge Engines:** Effortlessly connect Playwright to a browser session already managed by SeleniumBase.
2. **Stealth by Default:** Use `uc=True` (Undetected Mode) to bypass bot-detection systems that standard Playwright configurations often fail.
3. **Automatic Cleanup:** The context manager handles closing the browser and cleaning up processes automatically, even if the script encounters an error.

---

### 🚀 Quick Start

To run any of these examples, simply execute them with Python:

```bash
python raw_hybrid_script.py
```

--------

[<img src="https://seleniumbase.github.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase)
