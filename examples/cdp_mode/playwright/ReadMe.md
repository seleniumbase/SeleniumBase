<!-- SeleniumBase Docs -->

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> Stealthy Playwright Mode 🎭</h2>

🎭 <b translate="no">Stealthy Playwright Mode</b> is a subset of **[SeleniumBase CDP Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md)** that launches **[Playwright](https://github.com/microsoft/playwright-python)** from an existing <b translate="no">SeleniumBase</b> browser to make <span translate="no">Playwright</span> stealthy (for bypassing bot-detection).  <span translate="no">Playwright</span> uses <code><b>connect_over_cdp()</b></code> to attach itself onto an existing <span translate="no">SeleniumBase</span> session via the <code>remote-debugging-port</code>. From here, APIs of both frameworks can be used together.

--------

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=PnFD_gSmGUc"><img src="https://github.com/user-attachments/assets/4c9a12e3-0ae0-446b-b38f-2178827c8377" title="Stealthy Playwright Mode on YouTube" width="360" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=PnFD_gSmGUc">See Stealthy Playwright Mode on YouTube! ▶️</a></b>)</p>

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

Default timeout values are different between Playwright and SeleniumBase. For instance, a 30-second default timeout in a Playwright method might only be 10 seconds in the equivalent SeleniumBase method.

When specifying custom timeout values, Playwright uses milliseconds, whereas SeleniumBase uses seconds. Eg. `page.wait_for_timeout(2000)` is the equivalent of `sb.sleep(2)`. Although adding random sleeps to a script is generally discouraged, it helps the automation look more human-like for stealth, and it can prevent exceeding rate limits that trigger a block when automation performs actions too quickly.

Playwright's `:has-text()` selector is the equivalent of SeleniumBase's `:contains()` selector, except for one small difference: `:has-text()` isn't case-sensitive, but `:contains()` is.

Unlike normal Playwright, you don't need to run `playwright install` before running Stealthy Playwright Mode scripts because the system Chrome will be used. There's also the option of setting `use_chromium=True` to use the unbranded Chromium browser instead, which still supports extensions.

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
    page.wait_for_timeout(1000)
    query = "Playwright Python connect_over_cdp() sync example"
    page.fill("textarea#userInput", query)
    page.click('button[data-testid="submit-button"]')
    page.wait_for_timeout(4000)
    sb.solve_captcha()
    page.wait_for_selector('button[data-testid*="-thumbs-up"]')
    page.wait_for_timeout(4000)
    page.click('button[data-testid*="scroll-to-bottom"]')
    page.wait_for_timeout(3000)
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
    page.wait_for_timeout(2000)
    sb.solve_captcha()
    page.wait_for_timeout(2000)
```

--------

### 🎭 Proxy with auth in <b translate="no">Stealthy Playwright Mode</b>:

To use an authenticated proxy in Stealthy Playwright Mode, **do these two things**:<br />**1.** Set the`proxy` arg when launching Chrome.
-- Eg: `sb_cdp.Chrome(proxy="USER:PASS@IP:PORT")` or `cdp_driver.start_async("USER:PASS@IP:PORT")`.<br />**2.** Open the URL with SeleniumBase **before** using `endpoint_url` to connect to the browser with Playwright.

⚠️ If any trouble with the above, set `use_chromium=True` so that you can use the base Chromium browser, which still allows extensions, unlike regular branded Chrome, which removed the `--load-extension` command-line switch. (*An extension is used to set the auth for the proxy, which is needed when CDP can't set the proxy alone, such as for navigation after the initial page load*).

In the sync format, use `sb.open(url)` to open the url before connecting Playwright:
```python
sb = sb_cdp.Chrome(use_chromium=True, proxy="user:pass@server:port")
sb.open(url)
endpoint_url = sb.get_endpoint_url()
# ...
```

In the async format, use, `driver.get(url)` to open the url before connecting Playwright:
```python
driver = await cdp_driver.start_async(use_chromium=True, proxy="user:pass@server:port")
await driver.get(url)
endpoint_url = driver.get_endpoint_url()
# ...
```

Here's an example of using an authenticated proxy with Stealthy Playwright Mode:<br />(The URL is opened before attaching Playwright so that proxy settings take effect)
```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(use_chromium=True, proxy="user:pass@server:port")
sb.open(url)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    context = browser.contexts[0]
    page = context.pages[0]
    # ...
```
(Fill in the `url` and the `proxy` details to complete the script.)

Here's the same thing for the `async` format:
```python
import asyncio
from playwright.async_api import async_playwright
from seleniumbase import cdp_driver

async def main():
    driver = await cdp_driver.start_async(use_chromium=True, proxy="user:pass@server:port")
    await driver.get(url)
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = context.pages[0]
        # ...

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```
(Fill in the `url` and the `proxy` details to complete the script.)

--------

For more examples, see [examples/cdp_mode/playwright](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/playwright).

--------

<a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/img/logo6.png" alt="SeleniumBase" title="SeleniumBase" width="100" /></a><img src="https://seleniumbase.github.io/other/playwright_logo.png" alt="Playwright" title="Playwright" width="161">
