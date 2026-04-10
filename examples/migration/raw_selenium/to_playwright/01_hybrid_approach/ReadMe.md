<!-- SeleniumBase Docs -->

## 🎭 Migrating raw Selenium to Playwright (Hybrid approach)

Migrating tests from raw Selenium to Playwright can seem like an overwhelming effort. Fortunately, SeleniumBase provides a hybrid approach where the same test can call APIs from multiple different frameworks, allowing you to convert raw Selenium code to Playwright code in phases.

### 🗺️ The Hybrid Mapping

To understand how the Hybrid approach works, it helps to identify the role each component plays during the test execution:

| Component | Role in Migration | Purpose |
| :--- | :--- | :--- |
| **`self.driver`** | **Legacy Engine** | Executes your existing Raw Selenium code without changes. |
| **`self.page`** | **Modern Engine** | Executes new Playwright code for speed and better stability. |
| **`self`** | **The Bridge** | Uses SeleniumBase to manage the browser and CDP connection. |

By utilizing the Chrome DevTools Protocol (CDP), SeleniumBase allows these two engines to share the same browser session. Actions taken by the `driver` are immediately visible to the `page`, and vice versa.

Let's say your starting point is a test script like this:

```python
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
```

From here, instead of having to convert the entire script over to Playwright at once, you could swap out partitions to get to this:

```python
"""Hybrid Fixture TestCase Example"""
from playwright.sync_api import sync_playwright, expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc")


class HybridFixture(BaseCase):
    def setUp(self):
        super().setUp()
        self.activate_cdp_mode()
        self.reconnect()  # Reconnects WebDriver to use Selenium
        endpoint_url = self.cdp.get_endpoint_url()
        self.playwright = sync_playwright().start()
        browser = self.playwright.chromium.connect_over_cdp(endpoint_url)
        self.page = browser.contexts[0].pages[0]

    def tearDown(self):
        self.save_teardown_screenshot()  # If failure or "--screenshot"
        self.playwright.stop()
        super().tearDown()

    def test_add_item_to_cart(self):
        driver = self.driver  # Selenium API
        page = self.page  # Playwright API

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
```

The script above combines the APIs of raw Selenium, Playwright, and SeleniumBase, which gives you the flexibility to use any of them at any point in your test. SeleniumBase makes this possible with its adaptive API.

Now that you've included Playwright in your script, you can utilize some of its advanced features, such as the Full Trace Viewer. Here's an updated version of the hybrid script above that includes the Tracing feature:

```python
"""
Hybrid Fixture TestCase Example with Playwright Tracing.
Trace logs are saved to: `latest_logs/[MODULE.CLASS.METHOD]/trace.zip`
To open Trace Viewer: `playwright show-trace [PATH_TO_LOGS]/trace.zip`
"""
import os
from playwright.sync_api import sync_playwright, expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc")


class HybridFixtureWithTracing(BaseCase):
    def setUp(self):
        super().setUp()
        self.activate_cdp_mode()
        self.reconnect()  # Reconnects WebDriver to use Selenium
        endpoint_url = self.cdp.get_endpoint_url()
        self.playwright = sync_playwright().start()
        browser = self.playwright.chromium.connect_over_cdp(endpoint_url)
        self.context = browser.contexts[0]
        self.context.tracing.start(
            snapshots=True, screenshots=True, sources=True
        )
        self.page = self.context.pages[0]

    def tearDown(self):
        self.save_teardown_screenshot()  # If failure or "--screenshot"
        log_folder = "latest_logs"
        test_id = "%s.%s.%s" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._testMethodName,
        )
        trace_path = os.path.join(log_folder, test_id, "trace.zip")
        self.context.tracing.stop(path=trace_path)
        self.playwright.stop()
        super().tearDown()

    def test_add_item_to_cart(self):
        driver = self.driver  # Selenium API
        page = self.page  # Playwright API

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
```

Note that this hybrid mode gives you some flexibility in how you structure your test class. You could do it without the `setUp()` and `tearDown()` methods by using a context manager for Playwright like this:

```python
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
```

Eventually, once you've completed converting your script over to Playwright, you can remove the Selenium-specific code, and you'll have a full Playwright script that looks something like this:

```python
"""Playwright TestCase Example"""
import sys
from playwright.sync_api import sync_playwright, expect
from unittest import TestCase


class PlaywrightTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        headless = "linux" in sys.platform or "--headless" in sys.argv
        # Launch browser once for the whole class
        cls.browser = cls.playwright.chromium.launch(
            channel="chrome", headless=headless
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        # Create new session for every test
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        # Close the session (browser runs until tearDownClass)
        self.page.close()
        self.context.close()

    def test_add_item_to_cart(self):
        page = self.page

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
```

Or, you might decide to migrate over to SeleniumBase, and then your script for that test would look something like this:

```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class SeleniumBaseTestCase(BaseCase):
    def test_add_item_to_cart(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_text("Products", "span.title")

        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("Your Cart", "span.title")
        self.assert_text("Backpack", "div.cart_item")

        self.click("#remove-sauce-labs-backpack")
        self.assert_element_not_visible("div.cart_item")

        self.click("#react-burger-menu-btn")
        self.click("a#logout_sidebar_link")
        self.assert_element("input#login-button")
```

You've got lots of options and flexibility when the time comes to deciding how you want to migrate from raw Selenium to more modern frameworks like Playwright or SeleniumBase.

--------

[<img src="https://seleniumbase.github.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase)
