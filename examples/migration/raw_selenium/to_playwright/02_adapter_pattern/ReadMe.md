<!-- SeleniumBase Docs -->

## 🎭 Migrating raw Selenium to Playwright (Adapter Pattern)

In the "Adapter Pattern" design, the test class acts as an interface while the underlying framework becomes a swappable engine. This allows tests to stay the same because all framework-specific code gets extracted into reusable fixtures.

When converting raw Selenium tests to Playwright using the Adapter Pattern, all you have to do is modify the fixtures without changing the tests themselves.

> 💡 Notice: In every single example below, the code inside test_add_item_to_cart remains 100% identical. Only the underlying "engine" methods change.

Here's a raw Selenium test script using the Adapter Pattern:

```python
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unittest import TestCase


class RawSeleniumAdapter(TestCase):
    def setUp(self):
        self.driver = None
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
        self.driver = webdriver.Chrome(options=options, service=service)

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
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, selector))
            )
        except Exception:
            raise Exception(
                "Element (%s) was not visible after %s seconds!"
                % (selector, timeout)
            )

    def wait_for_element_clickable(
        self, selector, by="css selector", timeout=10
    ):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
        except Exception:
            raise Exception(
                "Element (%s) was not visible/clickable after %s seconds!"
                % (selector, timeout)
            )

    def wait_for_element_not_visible(
        self, selector, by="css selector", timeout=10
    ):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element((by, selector))
            )
        except Exception:
            raise Exception(
                "Element (%s) was still visible after %s seconds!"
                % (selector, timeout)
            )

    def open(self, url):
        self.driver.get(url)

    def click(self, selector, by="css selector", timeout=7):
        el = self.wait_for_element_clickable(selector, by=by, timeout=timeout)
        el.click()

    def type(self, selector, text, by="css selector", timeout=10):
        el = self.wait_for_element_clickable(selector, by=by, timeout=timeout)
        el.clear()
        if not text.endswith("\n"):
            el.send_keys(text)
        else:
            el.send_keys(text[:-1])
            el.submit()

    def assert_element(self, selector, by="css selector", timeout=7):
        self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def assert_text(self, text, selector="html", by="css selector", timeout=7):
        el = self.wait_for_element_visible(selector, by=by, timeout=timeout)
        self.assertIn(text, el.text)

    def assert_exact_text(self, text, selector, by="css selector", timeout=7):
        el = self.wait_for_element_visible(selector, by=by, timeout=timeout)
        self.assertEqual(text, el.text)

    def assert_element_not_visible(
        self, selector, by="css selector", timeout=7
    ):
        self.wait_for_element_not_visible(selector, by=by, timeout=timeout)

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

That example converts into this Playwright test script:

```python
import sys
from playwright.sync_api import sync_playwright, expect
from unittest import TestCase


class PlaywrightAdapter(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        headless = "linux" in sys.platform
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

    def open(self, url):
        self.page.goto(url)

    def click(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        self.page.click(selector, timeout=timeout)

    def type(self, selector, text, timeout=10):
        timeout = float(timeout) * 1000.0
        if text.endswith("\n"):
            self.page.fill(selector, text[:-1], timeout=timeout)
            self.page.press(selector, "Enter")
        else:
            self.page.fill(selector, text, timeout=timeout)

    def assert_element(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def assert_text(self, text, selector="html", timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_contain_text(
            text, timeout=timeout
        )

    def assert_exact_text(self, text, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_have_text(text, timeout=timeout)

    def assert_element_not_visible(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

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

(Note that the test portion stayed exactly the same.)

Migrating from raw Selenium to Playwright provides a number of advantages, such as improved debugging options with the Full Trace Viewer. Here's a modified version of the above example with the Tracing code added in:

```python
"""
Playwright Adapter Example with Tracing.
Trace logs are saved to: `latest_logs/[MODULE.CLASS.METHOD]/trace.zip`
To open Trace Viewer: `playwright show-trace [PATH_TO_LOGS]/trace.zip`
"""
import os
import sys
from playwright.sync_api import sync_playwright, expect
from unittest import TestCase


class PlaywrightAdapterWithTracing(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        headless = "linux" in sys.platform
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
        self.context.tracing.start(
            snapshots=True, screenshots=True, sources=True
        )
        self.page = self.context.new_page()

    def tearDown(self):
        # Close the session (browser runs until tearDownClass)
        log_folder = "latest_logs"
        test_id = "%s.%s.%s" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._testMethodName,
        )
        trace_path = os.path.join(log_folder, test_id, "trace.zip")
        self.context.tracing.stop(path=trace_path)
        self.page.close()
        self.context.close()

    def open(self, url):
        self.page.goto(url)

    def click(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        self.page.click(selector, timeout=timeout)

    def type(self, selector, text, timeout=10):
        timeout = float(timeout) * 1000.0
        if text.endswith("\n"):
            self.page.fill(selector, text[:-1], timeout=timeout)
            self.page.press(selector, "Enter")
        else:
            self.page.fill(selector, text, timeout=timeout)

    def assert_element(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        # expect() has built-in retry logic
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def assert_text(self, text, selector="html", timeout=7):
        timeout = float(timeout) * 1000.0
        # to_contain_text is the equivalent of "assertIn"
        expect(self.page.locator(selector)).to_contain_text(
            text, timeout=timeout
        )

    def assert_exact_text(self, text, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_have_text(text, timeout=timeout)

    def assert_element_not_visible(self, selector, timeout=7):
        timeout = float(timeout) * 1000.0
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

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

You can also implement the Adapter Pattern with SeleniumBase:

```python
from seleniumbase import SB
from unittest import TestCase


class SeleniumBaseAdapter(TestCase):
    def setUp(self):
        self.sb_context = SB()
        self.sb = self.sb_context.__enter__()

    def tearDown(self):
        self.sb_context.__exit__(None, None, None)

    def open(self, url):
        self.sb.open(url)

    def click(self, selector, by="css selector", timeout=7):
        self.sb.click(selector=selector, by=by, timeout=timeout)

    def type(self, selector, text, by="css selector", timeout=10):
        self.sb.type(selector, text=text, by=by, timeout=timeout)

    def assert_element(self, selector, by="css selector", timeout=7):
        self.sb.assert_element(selector, by=by, timeout=timeout)

    def assert_text(self, text, selector="html", by="css selector", timeout=7):
        self.sb.assert_text(text, selector=selector, by=by, timeout=timeout)

    def assert_exact_text(self, text, selector, by="css selector", timeout=7):
        self.sb.assert_exact_text(
            text, selector=selector, by=by, timeout=timeout
        )

    def assert_element_not_visible(
        self, selector, by="css selector", timeout=7
    ):
        self.sb.assert_element_not_visible(selector, by=by, timeout=timeout)

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

Since the target interface for that is the same as the one included with SeleniumBase's `BaseCase` class, you can remove the boilerplate code entirely to give you a very simplified script:

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

This demonstrates that if you extract out all framework-specific code into reusable fixtures, then you can switch frameworks easily without having to directly modify the tests themselves.

By using the Adapter Pattern, you're making it easy to scale up quickly if you need to switch frameworks, because instead of having to modify 1,000 tests, you'll only need to update *maybe* 10 methods.

> ⚠️ Note on Iframes: While the Adapter Pattern handles simple elements seamlessly, switching from Selenium to Playwright may require updating iframe logic. Selenium uses a "focus-shift" model (`switch_to.frame`), whereas Playwright uses a "targeting" model (`page.frame_locator`). If your suite relies heavily on iframes, your adapter methods for those specific interactions will need to account for this architectural difference.

--------

### 🗺️ Pattern Mapping

To understand how the Adapter Pattern applies to browser automation, it helps to map the testing components to their roles in the design pattern:

| Component | Role in the Pattern | Implementation in these Examples |
| :--- | :--- | :--- |
| **Client** | The consumer of the service. | The `test_add_item_to_cart()` method. |
| **Target (Interface)** | The set of commands the Client uses. | Methods like `open()`, `click()`, `type()`, and `assert_element()`. |
| **Adapter** | The wrapper that translates commands. | Classes like `PlaywrightAdapter` or `SeleniumBaseAdapter`. |
| **Adaptee** | The underlying "engine" being adapted. | The specific library (`playwright-python` or `selenium`). |

By keeping the **Client** code focused purely on the **Target** interface, you ensure that the **Adaptee** can be swapped out with minimal friction.

--------

[<img src="https://seleniumbase.github.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase)
