<!-- SeleniumBase Docs -->

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> Stealthy Playwright Mode 🎭</h2>

🎭 <b translate="no">Stealthy Playwright Mode</b> is a subset of **[SeleniumBase CDP Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md)** where  <b translate="no">[Playwright](https://github.com/microsoft/playwright-python)</b> attaches to a stealthy browser session via the remote-debugging URL. This lets <span translate="no">Playwright</span> bypass bot-detection while allowing APIs of both frameworks to work in tandem. Under the hood, Playwright calls <code><b>connect_over_cdp()</b></code> to achieve this stealth.

--------

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=PnFD_gSmGUc"><img src="https://github.com/user-attachments/assets/4c9a12e3-0ae0-446b-b38f-2178827c8377" title="Stealthy Playwright Mode on YouTube" width="360" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=PnFD_gSmGUc">See Stealthy Playwright Mode on YouTube! ▶️</a></b>)</p>

--------

## 🛠️ Installation

To use **Stealthy Playwright Mode**, simply install the necessary Python packages:

```zsh
pip install seleniumbase playwright
```

> **Note:** Just as standard Playwright can use `channel="chrome"` to bypass internal binary downloads, Stealthy Playwright Mode achieves the same by attaching to the system Chrome browser launched by SeleniumBase. This lets you skip the large `playwright install` step entirely.

## 💻 Usage

**Stealthy Playwright Mode** comes in three different formats:
1. `sb_cdp` "sync" format
2. `SB()` "nested sync" format
3. `cdp_driver` "async" format

### 1. The lightweight "sync" format (`sb_cdp`)

Ideal for standalone scripts that primarily use Playwright but need SeleniumBase's stealth and CAPTCHA-solving power without the overhead of WebDriver.

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://example.com")
```

### 2. The full-suite "nested sync" format (`SB()`)

Best for hybrid projects where you need to switch between WebDriver and Playwright APIs in the same session.

```python
from playwright.sync_api import sync_playwright
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.activate_cdp_mode()
    endpoint_url = sb.cdp.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        page.goto("https://example.com")
```

### 3. The "async" format (`cdp_driver`)

Designed for modern asynchronous Python. This allows you to run multiple concurrent stealth sessions using `async/await` and Playwright's `async_api`.

```python
import asyncio
from seleniumbase import cdp_driver
from playwright.async_api import async_playwright

async def main():
    driver = await cdp_driver.start_async()
    endpoint_url = driver.get_endpoint_url()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].pages[0]
        await page.goto("https://example.com")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```

### 💡 Key differences of the 3 stealthy formats:

-   **`sb_cdp`**: Simplest setup. CDP launches a stealthy browser. (No WebDriver)
    
-   **`SB()`**: Maximum utility. Gives you the full range of APIs: WebDriver, CDP, and Playwright. (WebDriver launches a stealthy browser.)
    
-   **`cdp_driver`**: Best for performance. `asyncio` handles non-blocking tasks. CDP launches a stealthy browser. (No WebDriver)

--------

### 🎭 Converting regular <b translate="no">Playwright</b> scripts to <b translate="no">Stealthy Playwright Mode</b>:

If you have a regular Playwright script that looks like this:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_context().new_page()
    page.goto("https://example.com")
```

Then the Stealthy Playwright Mode version of that would look like this:

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://example.com")
```

--------

### 🎭 <b translate="no">Stealthy Playwright Mode</b> details:

The `sb_cdp` and `cdp_driver` formats don't use WebDriver at all, meaning that `chromedriver` isn't needed. From these two formats, Stealthy Playwright Mode can call [CDP Mode methods](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/cdp_mode_methods.md) and Playwright methods.

The `SB()` format requires WebDriver, therefore `chromedriver` will be downloaded, modified for stealth, and renamed as `uc_driver` if not already present. The `SB()` format has access to Selenium WebDriver methods via [the SeleniumBase API](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md). When using Stealthy Playwright Mode from the `SB()` format, all the APIs are accessible: Selenium, SeleniumBase, [UC Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/uc_mode.md), [CDP Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md), and Playwright.

Default timeout values are different between Playwright and SeleniumBase. For instance, a 30-second default timeout in a Playwright method might only be 10 seconds in the equivalent SeleniumBase method.

When specifying custom timeout values, Playwright uses milliseconds, whereas SeleniumBase uses seconds. Eg. `page.wait_for_timeout(2000)` in Playwright is the equivalent of `sb.sleep(2)` in SeleniumBase.

Although hard sleeps are generally discouraged, they become a tactical tool in stealth mode because that extra waiting helps the automation look more human. Hard sleeps are used in multiple examples to prevent rate limits from being exceeded.

--------

### 🎭 A few examples of <b translate="no">Stealthy Playwright Mode</b>:

🎭 Here's an example that queries Microsoft Copilot:

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
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

(From [examples/cdp_mode/playwright/raw_copilot_sync.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/playwright/raw_copilot_sync.py))

🎭 Here's an example that solves the Bing CAPTCHA:

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(locale="en")
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://www.bing.com/turing/captcha/challenge")
    page.wait_for_timeout(2000)
    sb.solve_captcha()
    page.wait_for_timeout(2000)
```

(From [examples/cdp_mode/playwright/raw_bing_cap_sync.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/playwright/raw_bing_cap_sync.py))

#### 🎭 For all included examples, see [examples/cdp_mode/playwright](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/playwright).

--------

### 🎭 More details about <b translate="no">Stealthy Playwright Mode</b>:

Stealthy Playwright Mode uses the system's Chrome browser by default. There's also the option of setting `use_chromium=True` to use the unbranded Chromium browser instead, which still supports extensions. (With regular Playwright, you would generally need to run `playwright install` to download a special version of Chrome before running Playwright scripts, unless you set `channel="chrome"` to use the system's Chrome browser instead.)

Playwright's `:has-text()` selector is the equivalent of SeleniumBase's `:contains()` selector, except for one small difference: `:has-text()` isn't case-sensitive, but `:contains()` is.

In the sync formats, `get_endpoint_url()` also applies `nest-asyncio` so that nested event loops are allowed. (Python doesn't allow nested event loops by default). Without this, you'd get the error: `"Cannot run the event loop while another loop is running"` when calling CDP Mode methods (such as `solve_captcha()`) from within the Playwright context manager. This `nest-asyncio` call is done behind-the-scenes so that users don't need to handle this on their own.

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
    page = browser.contexts[0].pages[0]
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
        page = browser.contexts[0].pages[0]
        # ...

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```
(Fill in the `url` and the `proxy` details to complete the script.)

--------

#### 🎭 This flowchart shows how Stealthy Playwright Mode fits into CDP Mode:</h3>

<img src="https://seleniumbase.github.io/other/sb_stealth.png" width="596" alt="Stealthy architecture flowchart" />

(See the [**CDP Mode** ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md) for more information about that.)

#### 🎭 See [examples/cdp_mode/playwright](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/playwright) for Stealthy Playwight Mode examples.

--------

<a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/img/logo6.png" alt="SeleniumBase" title="SeleniumBase" width="100" /></a><img src="https://seleniumbase.github.io/other/playwright_logo.png" alt="Playwright" title="Playwright" width="161">
