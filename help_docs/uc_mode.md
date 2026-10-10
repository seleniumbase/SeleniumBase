<!-- SeleniumBase Docs -->

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> UC Mode 👤</h2>

👤 <b translate="no">SeleniumBase</b> <b translate="no">UC Mode</b> (Undetected-Chromedriver Mode) makes bots appear human, which lets them evade detection from anti-bot services that try to block them or trigger CAPTCHAs on various websites.

> ### (For the successor to plain UC Mode, see **[CDP Mode 🐙](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/ReadMe.md)**)

---

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=5dMFI3e85ig"><img src="http://img.youtube.com/vi/5dMFI3e85ig/0.jpg" title="SeleniumBase on YouTube" width="296" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=5dMFI3e85ig">1st UC Mode tutorial on YouTube ▶️</a></b>)</p>

More "Undetectable Automation": <b><a href="https://www.youtube.com/watch?v=2pTpBtaE7SQ">2nd ▶️</a> - <a href="https://www.youtube.com/watch?v=-EpZlhGWo9k">3rd ▶️</a> - <a href="https://www.youtube.com/watch?v=Mr90iQmNsKM">4th ▶️</a> - <a href="https://www.youtube.com/watch?v=R9HNsnbYh8o">5th ▶️</a></b>

----

👤 <b translate="no">UC Mode</b> is based on <a href="https://github.com/ultrafunkamsterdam/undetected-chromedriver">undetected-chromedriver</a>. <span translate="no">UC Mode</span> includes multiple updates, fixes, and improvements, such as having special methods for bypassing CAPTCHAs.

👤 Here's a <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_uc_driver.py">UC Mode example</a> with the <b><code translate="no">Driver</code></b> manager:<br  /><em>(Bypasses both BrowserScan AND Sannysoft Bot-Detection)</em>

```python
from seleniumbase import Driver

driver = Driver(uc=True)
driver.get("https://browserscan.net/bot-detection")
driver.assert_element('strong:contains("Normal")')
driver.sleep(1)
driver.get("https://bot.sannysoft.com/")
driver.assert_element("#user-agent-result.passed")
driver.assert_element("#webdriver-result.passed")
driver.assert_element("#advanced-webdriver-result.passed")
driver.assert_element("#permissions-result.passed")
driver.assert_element("#plugins-length-result.passed")
driver.assert_element("#plugins-type-result.passed")
driver.sleep(1)
driver.quit()
```

<p align="center">
<img src="https://seleniumbase.github.io/cdn/img/results_normal.jpg" width="520" style="max-width: 100% !important; height: auto !important;" alt="BrowserScan Test Results: Normal" />
<br /><em>(All BrowserScan bot-detection tests passed successfully)</em>
</p>

<p align="center">
<img src="https://seleniumbase.github.io/other/sannysoft_success.jpg" width="428" style="max-width: 100% !important; height: auto !important;" alt="All Sannysoft tests passed successfully" />
<br /><em>(All Sannysoft bot-detection tests passed successfully)</em>
</p>

👤 Here's a <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_uc_mode.py">UC Mode example</a> with the <b><code translate="no">SB</code></b> manager:

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.goto("https://gitlab.com/users/sign_in")
    sb.solve_captcha()
    sb.highlight('h1:contains("GitLab")')
    sb.highlight('button:contains("Sign in")')
```

<img src="https://seleniumbase.github.io/other/gitlab_bypass.png" title="SeleniumBase" width="370">

(Note: If running UC Mode scripts on headless Linux machines, then you'll need to use the <b><code translate="no">SB</code></b> manager instead of the <b><code translate="no">Driver</code></b> manager because the <b><code translate="no">SB</code></b> manager includes a special virtual display that allows for <b><code translate="no">PyAutoGUI</code></b> actions.)

👤 Here's an example where clicking the checkbox is required:<br /><em>(Commonly seen on CAPTCHA-protected forms)</em>

<img src="https://seleniumbase.github.io/other/cf_turnstile2.png" title="SeleniumBase" width="300">

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.goto("https://seleniumbase.io/apps/turnstile")
    sb.solve_captcha()
    sb.assert_element("img#captcha-success", timeout=3)
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)
```

<img src="https://seleniumbase.github.io/other/turnstile_click.jpg" title="SeleniumBase" width="440">

Sometimes you need to add <code translate="no">incognito=True</code> with <code translate="no">uc=True</code> to maximize your anti-detection abilities. (Some websites can detect you if you don't do that.)

👤 Here's a <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_ahrefs.py">UC Mode example</a> where a CAPTCHA appears after submitting a form:

```python
from seleniumbase import SB

with SB(uc=True, test=True, incognito=True, locale="en") as sb:
    sb.goto("https://ahrefs.com/website-authority-checker")
    search_term = "github.com/seleniumbase/SeleniumBase"
    sb.type('input[placeholder="Enter domain"]', search_term)
    sb.scroll_down(36)
    sb.click('span:contains("Check Authority")')
    sb.sleep(2)
    sb.solve_captcha()
    sb.sleep(3)
    sb.wait_for_text_not_visible("Checking", timeout=15)
    sb.click_if_visible('button[data-cky-tag="close-button"]')
    sb.highlight('p:contains("github.com/seleniumbase/SeleniumBase")')
    sb.highlight('a:contains("Top 100 backlinks")')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
```

<img src="https://seleniumbase.github.io/other/ahrefs_bypass.png" title="SeleniumBase" width="540">

--------

👤 <b>On Linux</b>, use `sb.solve_captcha()` to handle CAPTCHAs:

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "https://www.virtualmanager.com/en/login"
    sb.goto(url)
    print(sb.get_page_title())
    sb.solve_captcha()  # Only used if needed
    sb.assert_element('input[name*="email"]')
    print(sb.get_page_title())
    sb.assert_element('input[name*="login"]')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
```

<a href="https://github.com/mdmintz/undetected-testing/actions/runs/9637461606/job/26576722411"><img width="540" alt="uc_gui_click_captcha on Linux" src="https://github.com/seleniumbase/SeleniumBase/assets/6788579/6aceb2a3-2a32-4521-b30a-f79446d2ce28"></a>

The 2nd <code translate="no">print()</code> should output <code translate="no">Virtual Manager</code>, which means that the automation successfully passed the Turnstile.

(Note: <span translate="no">UC Mode</span> has a special virtual display on Linux: <code>Xvfb</code>, which is enabled by default when not changing headed/headless settings.)

--------

👤 Here's a <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_pixelscan.py">UC Mode example</a> of bypassing bot-detection on Pixelscan:

```python
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode(ad_block=True)
    sb.goto("https://pixelscan.net/fingerprint-check")
    sb.remove_element("div.header-promo")
    sb.remove_element("pxlscn-dynamic-ad")
    sb.sleep(1.8)
    sb.assert_text("No automated behavior", "pxlscn-bot-detection")
    sb.assert_text("No masking detected", "pxlscn-fingerprint-masking")
    sb.assert_text("consistent", "span.status-success")
    sb.sleep(0.5)
    sb.cdp.highlight("span.status-success")
    sb.cdp.highlight("pxlscn-fingerprint-masking p")
    sb.cdp.highlight("pxlscn-bot-detection p")
    print("Bot Not Detected")
```

<img src="https://seleniumbase.github.io/other/pixelscan.jpg" title="SeleniumBase" width="540">

--------

👤 In <b translate="no">UC Mode</b>, <code translate="no">driver.get(url)</code> has been modified from its original version: If anti-bot services are detected from a <code translate="no">requests.get(url)</code> call that's made before navigating to the website, then <code translate="no">driver.uc_open_with_reconnect(url)</code> will be used instead. To open a URL normally in <b translate="no">UC Mode</b>, use <code translate="no">driver.default_get(url)</code>, which does not have stealth.

--------

### 👤 Here are the SeleniumBase UC Mode methods: (**`--uc`** / **`uc=True`**)

```python
driver.uc_open(url)

driver.uc_open_with_tab(url)

driver.uc_open_with_reconnect(url, reconnect_time=None)

driver.uc_open_with_disconnect(url, timeout=None)

driver.reconnect(timeout)

driver.disconnect()

driver.connect()

driver.uc_click(
    selector, by="css selector",
    timeout=settings.SMALL_TIMEOUT, reconnect_time=None)

driver.uc_gui_press_key(key)

driver.uc_gui_press_keys(keys)

driver.uc_gui_write(text)

driver.uc_gui_click_x_y(x, y, timeframe=0.25)

driver.uc_gui_click_captcha(frame="iframe", retry=False, blind=False)
# driver.uc_gui_click_cf(frame="iframe", retry=False, blind=False)
# driver.uc_gui_click_rc(frame="iframe", retry=False, blind=False)

driver.uc_gui_handle_captcha(frame="iframe")
# driver.uc_gui_handle_cf(frame="iframe")
# driver.uc_gui_handle_rc(frame="iframe")
```

(Note that the <b><code translate="no">reconnect_time</code></b> is used to specify how long the driver should be disconnected from Chrome to prevent detection before reconnecting again.)

👤 Since <b><code translate="no">driver.get(url)</code></b> is slower in <span translate="no">UC Mode</span> for bypassing detection, use <b><code translate="no">driver.default_get(url)</code></b> for a standard page load instead:

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

--------

👤 <b>On Linux</b>, use <code translate="no">xvfb=True</code> / `--xvfb` to activate a special virtual display. This allows you to run a regular browser in an environment that has no GUI. This is important for two reasons: One: <span translate="no">UC Mode</span> may be detectable in headless mode. Two: <code translate="no">pyautogui</code> doesn't work in headless mode. (Note that some methods such as <code translate="no">uc_gui_click_captcha()</code> require <code translate="no">pyautogui</code> for performing special actions.)

--------

👤 <b>Multithreaded UC Mode:</b>

If you're using <b><code translate="no">pytest</code></b> for multithreaded <b translate="no">UC Mode</b> (which requires using one of the <b><code translate="no">pytest</code></b> [syntax formats](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md)), then all you have to do is set the number of threads when your script runs. (<code translate="no">-n NUM</code>) Eg:

```zsh
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

👤 <b>What makes UC Mode work?</b>

Here are the 3 primary things that <b translate="no">UC Mode</b> does to make bots appear human:

<ul>
<li>Modifies <b><code translate="no">chromedriver</code></b> to rename <b translate="no">Chrome DevTools Console</b> variables.</li>
<li>Launches <b translate="no">Chrome</b> browsers before attaching <b><code translate="no">chromedriver</code></b> to them.</li>
<li>Disconnects <b><code translate="no">chromedriver</code></b> from <b translate="no">Chrome</b> during stealthy actions.</li>
</ul>

For example, if the <b translate="no">Chrome DevTools Console</b> variables aren't renamed, you can expect to find them easily when using <b><code translate="no">selenium</code></b> for browser automation:

<img src="https://seleniumbase.github.io/other/cdc_args.png" title="SeleniumBase" width="390">

(If those variables are still there, then websites can easily detect your bots.)

If you launch <b translate="no">Chrome</b> using <b><code translate="no">chromedriver</code></b>, then there will be settings that make your browser look like a bot. (Instead, <b translate="no">UC Mode</b> connects <b><code translate="no">chromedriver</code></b> to <b translate="no">Chrome</b> after the browser is launched, which makes <b translate="no">Chrome</b> look like a normal, human-controlled web browser.)

While <b><code translate="no">chromedriver</code></b> is connected to <b translate="no">Chrome</b>, website services can detect it. Thankfully, raw <b><code translate="no">selenium</code></b> already includes <b><code translate="no">driver.service.stop()</code></b> for stopping the <b><code translate="no">chromedriver</code></b> service, <b><code translate="no">driver.service.start()</code></b> for starting the <b><code translate="no">chromedriver</code></b> service, and <b><code translate="no">driver.start_session(capabilities)</code></b> for reviving the active browser session with the given capabilities. (<b translate="no"><code>SeleniumBase</code> <span translate="no">UC Mode</span></b> methods automatically use those raw <b><code translate="no">selenium</code></b> methods as needed.)

Links to those <a href="https://github.com/SeleniumHQ/selenium">raw <b>Selenium</b></a> method definitions have been provided for reference (but you don't need to call those methods directly):

<ul>
<li><b><code translate="no"><a href="https://github.com/SeleniumHQ/selenium/blob/9c6ccdbf40356284fad342f70fbdc0afefd27bd3/py/selenium/webdriver/common/service.py#L135">driver.service.stop()</a></code></b></li>
<li><b><code translate="no"><a href="https://github.com/SeleniumHQ/selenium/blob/9c6ccdbf40356284fad342f70fbdc0afefd27bd3/py/selenium/webdriver/common/service.py#L91">driver.service.start()</a></code></b></li>
<li><b><code translate="no"><a href="https://github.com/SeleniumHQ/selenium/blob/9c6ccdbf40356284fad342f70fbdc0afefd27bd3/py/selenium/webdriver/remote/webdriver.py#L284">driver.start_session(capabilities)</a></code></b></li>
</ul>

Also note that <b><code translate="no">chromedriver</code></b> isn't detectable in a browser tab if it never touches that tab. Here's a JS command that lets you open a URL in a new tab (from your current tab):

<ul>
<li><b><code translate="no">window.open("URL");</code></b> --> (Info: <a href="https://www.w3schools.com/jsref/met_win_open.asp" target="_blank">W3Schools</a>)</li>
</ul>

The above JS method is used within <b translate="no"><code>SeleniumBase</code></b> <b translate="no">UC Mode</b> methods for opening URLs in a stealthy way. Since some websites try to detect if your browser is a bot on the initial page load, this allows you to bypass detection in those situations. After a few seconds (customizable), <b translate="no">UC Mode</b> tells <b><code translate="no">chromedriver</code></b> to connect to that tab so that automated commands can now be issued. At that point, <b><code translate="no">chromedriver</code></b> could be detected if websites are looking for it (but generally websites only look for it during specific events, such as page loads, form submissions, and button clicks).

Avoiding detection while clicking is easy if you schedule your clicks to happen at a future point when the <b><code translate="no">chromedriver</code></b> service has been stopped. Here's a JS command that lets you schedule events (such as clicks) to happen in the future:

<li><b><code translate="no">window.setTimeout(function() { SCRIPT }, MS);</code></b> --> (Info: <a href="https://www.w3schools.com/jsref/met_win_settimeout.asp" target="_blank">W3Schools</a>)</li>

The above JS method is used within the <b><code translate="no">SeleniumBase</code></b> <b translate="no">UC Mode</b> method: <b><code translate="no">sb.uc_click(selector)</code></b> so that clicking can be done in a stealthy way. <b translate="no">UC Mode</b> schedules your click, disconnects <b><code translate="no">chromedriver</code></b> from <b translate="no">Chrome</b>, waits a little (customizable), and reconnects.

--------

🏆 <b>Choosing the right CAPTCHA service</b> for your business / website:

<img src="https://seleniumbase.github.io/other/me_se_conf.jpg" title="SeleniumBase" width="370">

As an ethical hacker / cybersecurity researcher who builds bots that bypass CAPTCHAs for sport, <b>the CAPTCHA service that I personally recommend</b> for keeping bots out is <b translate="no">Google reCAPTCHA</b>:

<img src="https://seleniumbase.github.io/other/g_recaptcha.png" title="SeleniumBase" width="315">

Since Google makes Chrome, Google's own <b translate="no">reCAPTCHA</b> service has access to more data than other CAPTCHA services, and can therefore use that data to make better decisions about whether or not web activity is coming from real humans or automated bots.

--------

⚖️ <b>Legal implications of web-scraping</b>:

Based on the following article, https://nubela.co/blog/meta-lost-the-scraping-legal-battle-to-bright-data/, (which outlines a court case where social-networking company: Meta lost the legal battle to data-scraping company: Bright Data), it was determined that web scraping is 100% legal in the eyes of the courts as long as:
1. The scraping is only done with <b>public data</b> and <b>not private data</b>.
2. The scraping isn’t done while logged in on the site being scraped.

If the above criteria are met, then scrape away! (According to the article)

(Note: I'm not a lawyer, so I can't officially offer legal advice, but I can direct people to existing articles online where people can find their own answers.)

--------

### ▶️ "Undetectable Automation" YouTube tutorials:

--------

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=5dMFI3e85ig"><img src="http://img.youtube.com/vi/5dMFI3e85ig/0.jpg" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=5dMFI3e85ig">Watch the 1st UC Mode tutorial on YouTube! ▶️</a></b>)</p>

----

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=2pTpBtaE7SQ"><img src="http://img.youtube.com/vi/2pTpBtaE7SQ/0.jpg" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=2pTpBtaE7SQ">Watch the 2nd UC Mode tutorial on YouTube! ▶️</a></b>)</p>

----

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=-EpZlhGWo9k"><img src="http://img.youtube.com/vi/-EpZlhGWo9k/0.jpg" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=-EpZlhGWo9k">Watch the 3rd UC Mode tutorial on YouTube! ▶️</a></b>)</p>

----

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=Mr90iQmNsKM"><img src="http://img.youtube.com/vi/Mr90iQmNsKM/0.jpg" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=Mr90iQmNsKM">Watch the 4th Edition on YouTube! ▶️</a></b>)</p>

----

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=R9HNsnbYh8o"><img src="https://github.com/user-attachments/assets/9d04fa89-44b0-4077-96d1-5b84f5a2e5fe" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=R9HNsnbYh8o">Watch the 5th Edition on YouTube! ▶️</a></b>)</p>

--------

<img src="https://seleniumbase.github.io/cdn/img/sb_text_f.png" alt="SeleniumBase" title="SeleniumBase" align="center" width="335">

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/cdn/img/sb_logo_gs.png" alt="SeleniumBase" title="SeleniumBase" width="335" /></a></div>
