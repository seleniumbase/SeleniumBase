<!-- SeleniumBase Docs -->

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> Stealthy Playwright Mode 🎭</h2>

🎭 <b translate="no">Stealthy Playwright Mode</b> is a subset of **[SeleniumBase CDP Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md)** that launches **[Playwright](https://github.com/microsoft/playwright-python)** from an existing <b translate="no">SeleniumBase</b> browser to make <span translate="no">Playwright</span> stealthy (for bypassing bot-detection).  <span translate="no">Playwright</span> uses <code><b>connect_over_cdp()</b></code> to attach itself onto an existing <span translate="no">SeleniumBase</span> session via the <code>remote-debugging-port</code>. From here, APIs of both frameworks can be used together.

--------

### 🎭 Getting started with <b translate="no">Stealthy Playwright Mode</b>:

If `playwright` isn't already installed, then install it first:

```zsh
pip install playwright
```

Stealthy Playwright Mode comes in 3 formats:
1. `sb_cdp` sync format
2. `SB` nested sync format
3. `cdp_driver` async format


#### `sb_cdp` sync format (minimal boilerplate):

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://example.com")
```

#### `SB` nested sync format (minimal boilerplate):

```python
from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode()
    endpoint_url = sb.cdp.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto("https://example.com")
```

#### `cdp_driver` async format (minimal boilerplate):

```python
import asyncio
from seleniumbase import cdp_driver
from playwright.async_api import async_playwright

async def main():
    driver = await cdp_driver.start_async()
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        await page.goto("https://example.com")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```

### 🎭 <b translate="no">Stealthy Playwright Mode</b> details:

The `sb_cdp` and `cdp_driver` formats don't use WebDriver at all, meaning that `chromedriver` isn't needed. From these two formats, Stealthy Playwright Mode can call [CDP Mode methods](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/cdp_mode_methods.md) and Playwright methods.

The `SB()` format requires WebDriver, therefore `chromedriver` will be downloaded (as `uc_driver`) if the driver isn't already present on the local machine. The `SB()` format has access to Selenium WebDriver methods via [the SeleniumBase API](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md). Using Stealthy Playwright Mode from `SB()` grants access to all the APIs: Selenium, SeleniumBase, [UC Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/uc_mode.md), [CDP Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md), and Playwright.

In the sync formats, `get_endpoint_url()` also applies `nest-asyncio` so that nested event loops are allowed. (Python doesn't allow nested event loops by default). Without this, you'd get the error: `"Cannot run the event loop while another loop is running"` when calling CDP Mode methods (such as `solve_captcha()`) from within the Playwright context manager. This `nest-asyncio` call is done behind-the-scenes so that users don't need to handle this on their own.

### 🎭 <b translate="no">Stealthy Playwright Mode</b> examples:

Here's an example that queries Microsoft Copilot:

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://copilot.microsoft.com")
    page.wait_for_selector("textarea#userInput")
    sb.sleep(1)
    query = "Playwright Python connect_over_cdp() sync example"
    page.fill("textarea#userInput", query)
    page.click('button[data-testid="submit-button"]')
    sb.sleep(3)
    sb.solve_captcha()
    page.wait_for_selector('button[data-testid*="-thumbs-up"]')
    sb.sleep(4)
    page.click('button[data-testid*="scroll-to-bottom"]')
    sb.sleep(3)
    chat_results = '[data-testid="highlighted-chats"]'
    result = page.locator(chat_results).inner_text()
    print(result.replace("\n\n", " \n"))
```

Here's an example that solves the Bing CAPTCHA:

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    page.goto("https://www.bing.com/turing/captcha/challenge")
    sb.sleep(3)
    sb.solve_captcha()
    sb.sleep(3)
```

For more examples, see [examples/cdp_mode/playwright](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/playwright).

--------

<a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/img/logo6.png" alt="SeleniumBase" title="SeleniumBase" width="100" /></a><img src="https://seleniumbase.github.io/other/playwright_logo.png" alt="Playwright" title="Playwright" width="161">
