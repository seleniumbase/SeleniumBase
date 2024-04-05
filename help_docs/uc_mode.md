<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) UC Mode 👤

👤 <b translate="no">SeleniumBase</b> <b translate="no">UC Mode</b> (Undetected-Chromedriver Mode) allows bots to appear human, which lets them evade detection from anti-bot services that try to block them or trigger CAPTCHAs on various websites.

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=5dMFI3e85ig"><img src="http://img.youtube.com/vi/5dMFI3e85ig/0.jpg" title="SeleniumBase on YouTube" width="400" /></a>
<!-- GitHub Only --><p>(<b><a href="https://www.youtube.com/watch?v=5dMFI3e85ig">Watch the UC Mode tutorial on YouTube! ▶️</a></b>)</p>

👤 <b translate="no">UC Mode</b> is based on [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver), but includes multiple updates, fixes, and improvements, such as:

* Automatically changing user agents to prevent detection.
* Automatically setting various chromium args as needed.
* Has special methods. Eg. `driver.uc_click(selector)`

👤 Here's an example with the <b><code translate="no">Driver</code></b> manager:

```python
from seleniumbase import Driver

driver = Driver(uc=True)
driver.uc_open_with_reconnect("https://gitlab.com/users/sign_in", 3)
driver.quit()
```

👤 Here's an example with the <b><code translate="no">SB</code></b> manager (which has more methods and functionality than the <b><code translate="no">Driver</code></b> format):

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

👤 Here's an example <b>where clicking the checkbox is required</b>, even for humans:<br />(Commonly seen on forms that are CAPTCHA-protected.)

<img src="https://seleniumbase.github.io/other/cf_turnstile.png" title="SeleniumBase" width="260">

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

<img src="https://seleniumbase.github.io/other/turnstile_click.jpg" title="SeleniumBase" width="440">

--------

👤 In <b translate="no">UC Mode</b>, <code translate="no">driver.get(url)</code> has been modified from its original version: If anti-bot services are detected from a <code translate="no">requests.get(url)</code> call that's made before navigating to the website, then <code translate="no">driver.uc_open_with_reconnect(url)</code> will be used instead. To open a URL normally in <b translate="no">UC Mode</b>, use <code translate="no">driver.default_get(url)</code>.

--------

### 👤 Here are some examples that use UC Mode:
* [SeleniumBase/examples/verify_undetected.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/verify_undetected.py)
* [SeleniumBase/examples/raw_bing_captcha.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_bing_captcha.py)
* [SeleniumBase/examples/raw_uc_mode.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_uc_mode.py)
* [SeleniumBase/examples/raw_pixelscan.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_pixelscan.py)

<img src="https://seleniumbase.github.io/other/pixelscan.jpg" title="SeleniumBase" width="540">

### 👤 Here are some UC Mode examples that bypass CAPTCHAs when clicking is required:
* [SeleniumBase/examples/raw_turnstile.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_turnstile.py)
* [SeleniumBase/examples/raw_form_turnstile.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_form_turnstile.py)
* [SeleniumBase/examples/uc_cdp_events.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/uc_cdp_events.py)

<img src="https://seleniumbase.github.io/other/cf_bypass.png" title="SeleniumBase" width="260">

### 👤 Here are the <b><code translate="no">driver</code></b>-specific methods added by SeleniumBase for UC Mode: `--uc` / <b><code translate="no">uc=True</code></b>

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

(Note that the <b><code translate="no">reconnect_time</code></b> is used to specify how long the driver should be disconnected from Chrome to prevent detection before reconnecting again.)

👤 Since <b><code translate="no">driver.get(url)</code></b> is slower in UC Mode for bypassing detection, use <b><code translate="no">driver.default_get(url)</code></b> for a standard page load instead:

```python
driver.default_get(url)  # Faster, but Selenium can be detected
```

👤 Here are some examples of using those special <b translate="no">UC Mode</b> methods: (Use <b><code translate="no">self.driver</code></b> for <b><code translate="no">BaseCase</code></b> formats. Use <b><code translate="no">sb.driver</code></b> for <b><code translate="no">SB()</code></b> formats):

```python
url = "https://gitlab.com/users/sign_in"
driver.uc_open_with_reconnect(url, reconnect_time=3)
driver.uc_open_with_reconnect(url, 3)

driver.reconnect(5)
driver.reconnect(timeout=5)
```

👤 You can also set the <b><code translate="no">reconnect_time</code></b> / <b><code translate="no">timeout</code></b> to <b><code translate="no">"breakpoint"</code></b> as a valid option. This allows the user to perform manual actions (until typing <b><code translate="no">c</code></b> and pressing <b><code translate="no">ENTER</code></b> to continue from the breakpoint):

```python
url = "https://gitlab.com/users/sign_in"
driver.uc_open_with_reconnect(url, reconnect_time="breakpoint")
driver.uc_open_with_reconnect(url, "breakpoint")

driver.reconnect(timeout="breakpoint")
driver.reconnect("breakpoint")
```

(Note that while the special <b><code translate="no">UC Mode</code></b> breakpoint is active, you can't use <b><code translate="no">Selenium</code></b> commands in the browser, and the browser can't detect <b><code translate="no">Selenium</code></b>.)

👤 The two main causes of getting detected in <b translate="no">UC Mode</b> (which are both easily handled) are:

<li>Timing. (<b translate="no">UC Mode</b> methods let you customize default values that aren't good enough for your environment.)</li>
<li>Not using <b><code translate="no">driver.uc_click(selector)</code></b> when you need to remain undetected while clicking something.</li>

👤 To find out if <b translate="no">UC Mode</b> will work at all on a specific site (before adjusting for timing), load your site with the following script:

```python
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.driver.uc_open_with_reconnect(URL, reconnect_time="breakpoint")
```

(If you remain undetected while loading the page and performing manual actions, then you know you can create a working script once you swap the breakpoint with a time and add special methods like <b><code translate="no">driver.uc_click</code></b> as needed.)

👤 <b>Multithreaded UC Mode:</b>

If you're using <b><code translate="no">pytest</code></b> for multithreaded <b translate="no">UC Mode</b> (which requires using one of the <b><code translate="no">pytest</code></b> [syntax formats](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md)), then all you have to do is set the number of threads when your script runs. (`-n NUM`) Eg:

```bash
pytest --uc -n 4
```

(Then <b><code translate="no">pytest-xdist</code></b> is automatically used to spin up and process the threads.)

If you don't want to use <b><code translate="no">pytest</code></b> for multithreading, then you'll need to do a little more work. That involves using a different multithreading library, (eg. <b><code translate="no">concurrent.futures</code></b>), and making sure that thread-locking is done correctly for processes that share resources. To handle that thread-locking, include <b><code translate="no">sys.argv.append("-n")</code></b> in your <b>SeleniumBase</b> file.

Here's a sample script that uses <b><code translate="no">concurrent.futures</code></b> for spinning up multiple processes:

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

--------

👥 <b>Double Duty:</b> Here's an example of handling two CAPTCHAs on one page:

<img src="https://seleniumbase.github.io/other/nopecha.png" title="SeleniumBase" align="center" width="630">

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.driver.uc_open_with_reconnect("nopecha.com/demo/turnstile", 3.4)
    if sb.is_element_visible("#example-container0 iframe"):
        sb.switch_to_frame("#example-container0 iframe")
        if not sb.is_element_visible("circle.success-circle"):
            sb.driver.uc_click("span.mark", reconnect_time=3)
            sb.switch_to_frame("#example-container0 iframe")
        sb.switch_to_default_content()

    sb.switch_to_frame("#example-container5 iframe")
    sb.driver.uc_click("span.mark", reconnect_time=2.5)
    sb.switch_to_frame("#example-container5 iframe")
    sb.assert_element("svg#success-icon", timeout=3)
    sb.switch_to_parent_frame()

    if sb.is_element_visible("#example-container0 iframe"):
        sb.switch_to_frame("#example-container0 iframe")
        sb.assert_element("circle.success-circle")
        sb.switch_to_parent_frame()

    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected!", duration=3)
```

--------

👤 <b>What makes UC Mode work?</b>

Here are the 3 primary things that <b translate="no">UC Mode</b> does to make bots appear human:

<li>Modifies <b><code translate="no">chromedriver</code></b> to rename <b translate="no">Chrome DevTools Console</b> variables.</li>
<li>Launches <b translate="no">Chrome</b> browsers before attaching <b><code translate="no">chromedriver</code></b> to them.</li>
<li>Disconnects <b><code translate="no">chromedriver</code></b> from <b translate="no">Chrome</b> during stealthy actions.</li>

For example, if the <b translate="no">Chrome DevTools Console</b> variables aren't renamed, you can expect to find them easily when using <b><code translate="no">selenium</code></b> for browser automation:

<img src="https://seleniumbase.github.io/other/cdc_args.png" title="SeleniumBase" width="380">

(If those variables are still there, then websites can easily detect your bots.)

If you launch <b translate="no">Chrome</b> using <b><code translate="no">chromedriver</code></b>, then there will be settings that make your browser look like a bot. (Instead, <b translate="no">UC Mode</b> connects <b><code translate="no">chromedriver</code></b> to <b translate="no">Chrome</b> after the browser is launched, which makes <b translate="no">Chrome</b> look like a normal, human-controlled web browser.)

While <b><code translate="no">chromedriver</code></b> is connected to <b translate="no">Chrome</b>, website services can detect it. Thankfully, raw <b><code translate="no">selenium</code></b> already includes <b><code translate="no">driver.service.stop()</code></b> for stopping the <b><code translate="no">chromedriver</code></b> service, <b><code translate="no">driver.service.start()</code></b> for starting the <b><code translate="no">chromedriver</code></b> service, and <b><code translate="no">driver.start_session(capabilities)</code></b> for reviving the active browser session with the given capabilities. (<b translate="no"><code>SeleniumBase</code> UC Mode</b> methods automatically use those raw <b><code translate="no">selenium</code></b> methods as needed.)

Links to those <a href="https://github.com/SeleniumHQ/selenium">raw <b>Selenium</b></a> method definitions have been provided for reference (but you don't need to call those methods directly):

<li><b><code translate="no"><a href="https://github.com/SeleniumHQ/selenium/blob/9c6ccdbf40356284fad342f70fbdc0afefd27bd3/py/selenium/webdriver/common/service.py#L135">driver.service.stop()</a></code></b></li>
<li><b><code translate="no"><a href="https://github.com/SeleniumHQ/selenium/blob/9c6ccdbf40356284fad342f70fbdc0afefd27bd3/py/selenium/webdriver/common/service.py#L91">driver.service.start()</a></code></b></li>
<li><b><code translate="no"><a href="https://github.com/SeleniumHQ/selenium/blob/9c6ccdbf40356284fad342f70fbdc0afefd27bd3/py/selenium/webdriver/remote/webdriver.py#L284">driver.start_session(capabilities)</a></code></b></li>

Also note that <b><code translate="no">chromedriver</code></b> isn't detectable in a browser tab if it never touches that tab. Here's a JS command that lets you open a URL in a new tab (from your current tab):

<li><b><code translate="no">window.open("URL");</code></b> --> (Info: <a href="https://www.w3schools.com/jsref/met_win_open.asp" target="_blank">W3Schools</a>)</li>

The above JS method is used within <b translate="no"><code>SeleniumBase</code></b> <b translate="no">UC Mode</b> methods for opening URLs in a stealthy way. Since some websites try to detect if your browser is a bot on the initial page load, this allows you to bypass detection in those situations. After a few seconds (customizable), <b translate="no">UC Mode</b> tells <b><code translate="no">chromedriver</code></b> to connect to that tab so that automated commands can now be issued. At that point, <b><code translate="no">chromedriver</code></b> could be detected if websites are looking for it (but generally websites only look for it during specific events, such as page loads, form submissions, and button clicks).

Avoiding detection while clicking is easy if you schedule your clicks to happen at a future point when the <b><code translate="no">chromedriver</code></b> service has been stopped. Here's a JS command that lets you schedule events (such as clicks) to happen in the future:

<li><b><code translate="no">
window.setTimeout(function() { SCRIPT }, MS);</code></b> --> (Info: <a href="https://www.w3schools.com/jsref/met_win_settimeout.asp" target="_blank">W3Schools</a>)</li>

The above JS method is used within the <b><code translate="no">SeleniumBase</code></b> <b translate="no">UC Mode</b> method: <b><code translate="no">driver.uc_click(selector)</code></b> so that clicking can be done in a stealthy way. <b translate="no">UC Mode</b> schedules your click, disconnects <b><code translate="no">chromedriver</code></b> from <b translate="no">Chrome</b>, waits a little (customizable), and reconnects.

--------

🏆 <b>Choosing the right CAPTCHA service</b> for your business / website:

<img src="https://seleniumbase.github.io/other/me_se_conf.jpg" title="SeleniumBase" width="340">

As an ethical hacker / cybersecurity researcher who builds bots that bypass CAPTCHAs for sport, <b>the CAPTCHA service that I personally recommend</b> for keeping bots out is <b translate="no">Google's reCAPTCHA</b>:

<img src="https://seleniumbase.github.io/other/g_recaptcha.png" title="SeleniumBase" width="315">

Since Google makes Chrome, Google's own <b translate="no">reCAPTCHA</b> service has access to more data than other CAPTCHA services (eg. hCaptcha, CloudFlare, DataDome, etc.), and can therefore use that data to make better decisions about whether or not web activity is coming from real humans or automated bots.

--------

<img src="https://seleniumbase.github.io/cdn/img/sb_text_f.png" alt="SeleniumBase" title="SeleniumBase" align="center" width="335">

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/cdn/img/sb_logo_gs.png" alt="SeleniumBase" title="SeleniumBase" width="335" /></a></div>
