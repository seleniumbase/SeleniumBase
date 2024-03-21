<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) UC Mode 👤

👤 SeleniumBase <b>UC Mode</b> (Undetected-Chromedriver Mode) allows bots to appear human, which lets them evade detection from anti-bot services that try to block them or trigger CAPTCHAs on various websites.

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=5dMFI3e85ig"><img src="http://img.youtube.com/vi/5dMFI3e85ig/0.jpg" title="SeleniumBase on YouTube" width="335" /></a>
<!-- GitHub Only --><p>(<b><a href="https://www.youtube.com/watch?v=5dMFI3e85ig">Watch the UC Mode tutorial on YouTube</a></b>)</p>

👤 <b>UC Mode</b> is based on [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver), but includes multiple updates, fixes, and improvements to support a wider range of features and edge cases:

* Includes driver version-detection & management.
* Allows mismatched browser/driver versions.
* Automatically changes the user agent to prevent detection. (`HeadlessChrome` to `Chrome`)
* Automatically disconnects chromedriver from Chrome as needed. (And reconnects)
* Supports multithreaded tests in parallel via `pytest-xdist`.
* Adjusts configuration based on the environment. (Linux/Ubuntu vs Windows vs macOS)
* Has options for setting proxy and proxy-with-auth.
* Has ways of adjusting timings from default values.
* Includes multiple ways of structuring test scripts.

👤 Here's an example with the `Driver` manager:

```python
from seleniumbase import Driver

driver = Driver(uc=True)
driver.uc_open_with_reconnect("https://gitlab.com/users/sign_in", 3)
driver.quit()
```

👤 Here's an example with the `SB` manager: (Has more methods than the `Driver` format, and also quits the driver automatically after the `with` block ends.)

```python
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.driver.uc_open_with_reconnect("https://gitlab.com/users/sign_in", 3)
```

👤 Here's a longer example, which includes a retry if the CAPTCHA isn't bypassed on the first attempt:

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.driver.uc_open_with_reconnect(url, 3)
    if not sb.is_text_visible("Username", '[for="user_login"]'):
        sb.driver.uc_open_with_reconnect(url, 4)
    sb.assert_text("Username", '[for="user_login"]', timeout=3)
    sb.highlight('label[for="user_login"]', loops=3)
    sb.post_message("SeleniumBase wasn't detected", duration=4)
```

👤 Here's an example where clicking the checkbox is required, even for humans: (Commonly seen with forms that are CAPTCHA-protected.)

```python
from seleniumbase import SB

def open_the_turnstile_page(sb):
    sb.driver.uc_open_with_reconnect(
        "https://seleniumbase.io/apps/turnstile", reconnect_time=3,
    )

def click_turnstile_and_verify(sb):
    sb.switch_to_frame("iframe")
    sb.driver.uc_click("span.mark")
    sb.assert_element("img#captcha-success", timeout=3)

with SB(uc=True, test=True) as sb:
    open_the_turnstile_page(sb)
    try:
        click_turnstile_and_verify(sb)
    except Exception:
        open_the_turnstile_page(sb)
        click_turnstile_and_verify(sb)
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)
```

### 👤 Here are some examples that use UC Mode:
* [SeleniumBase/examples/verify_undetected.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/verify_undetected.py)
* [SeleniumBase/examples/uc_cdp_events.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/uc_cdp_events.py)
* [SeleniumBase/examples/raw_uc_mode.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_uc_mode.py)

### 👤 Here are some UC Mode examples where clicking is required:
* [SeleniumBase/examples/raw_turnstile.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_turnstile.py)
* [SeleniumBase/examples/raw_form_turnstile.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_form_turnstile.py)

### 👤 Here are `driver`-specific methods added by SeleniumBase for UC Mode: `--uc` / `uc=True`

```python
driver.uc_open(url)

driver.uc_open_with_tab(url)

driver.uc_open_with_reconnect(url, reconnect_time=None)

driver.reconnect(timeout)

driver.disconnect()

driver.connect()

driver.uc_click(
    selector, by="css selector",
    timeout=settings.SMALL_TIMEOUT, reconnect_time=None)

driver.uc_switch_to_frame(frame, reconnect_time=None)
```

(Note that the `reconnect_time` is used to specify how long the driver should be disconnected from Chrome to prevent detection before reconnecting again.)

👤 Since `driver.get(url)` is slower in UC Mode for bypassing detection, use `driver.default_get(url)` for a standard page load instead:

```python
driver.default_get(url)  # Faster, but Selenium can be detected
```

👤 Here are some examples of using those special UC Mode methods: (Use `self.driver` for `BaseCase` formats. Use `sb.driver` for `SB()` formats):

```python
url = "https://gitlab.com/users/sign_in"
driver.uc_open_with_reconnect(url, reconnect_time=3)
driver.uc_open_with_reconnect(url, 3)

driver.reconnect(5)
driver.reconnect(timeout=5)
```

👤 You can also set the `reconnect_time` / `timeout` to `"breakpoint"` as a valid option. This allows the user to perform manual actions (until typing `c` and pressing ENTER to continue from the breakpoint):

```python
url = "https://gitlab.com/users/sign_in"
driver.uc_open_with_reconnect(url, reconnect_time="breakpoint")
driver.uc_open_with_reconnect(url, "breakpoint")

driver.reconnect(timeout="breakpoint")
driver.reconnect("breakpoint")
```

(Note that while the special UC Mode breakpoint is active, you can't issue Selenium commands to the browser, and the browser can't detect Selenium.)

👤 The two main causes of getting detected in UC Mode (which are both easily handled) are:
* Timing. (UC Mode methods let you customize default values that aren't good enough for your environment.)
* Not using `driver.uc_click(selector)` when you need to remain undetected while clicking something.

👤 To find out if UC Mode will work at all on a specific site (before adjusting for timing), load your site with the following script:

```python
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.driver.uc_open_with_reconnect(URL, reconnect_time="breakpoint")
```

(If you remain undetected while loading the page and performing manual actions, then you know you can create a working script once you swap the breakpoint with a time, and add special methods like `uc_click` as needed.)

👤 <b>Multithreaded UC Mode:</b>

If you're using `pytest` for multithreaded UC Mode (which requires using one of the `pytest` [syntax formats](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md)), then all you have to do is set the number of threads when your script runs. (`-n NUM`) Eg:

```bash
pytest --uc -n 4
```

(Then `pytest-xdist` is automatically used to spin up and process the threads.)

If you don't want to use `pytest` for multithreading, then you'll need to do a little more work. That involves using a different multithreading library, (eg. `concurrent.futures`), and making sure that thread-locking is done correctly for processes that share resources. To handle that thread-locking, include `sys.argv.append("-n")` in your SeleniumBase file.

Here's a sample script that uses `concurrent.futures` for spinning up multiple processes:

```python
import sys
from concurrent.futures import ThreadPoolExecutor
from seleniumbase import Driver
sys.argv.append("-n")  # Tell SeleniumBase to do thread-locking as needed

def launch_driver(url):
    driver = Driver(uc=True)
    try:
        driver.get(url=url)
        driver.sleep(2)
    finally:
        driver.quit()

urls = ['https://seleniumbase.io/demo_page' for i in range(3)]
with ThreadPoolExecutor(max_workers=len(urls)) as executor:
    for url in urls:
        executor.submit(launch_driver, url)
```
