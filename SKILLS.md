# SKILLS.md

Task-oriented playbooks for AI agents using or working on **SeleniumBase**, the Python framework for browser automation, E2E testing, scraping, and stealth. Each skill says when to use it, what to do, and what to avoid.

> Companion to `AGENTS.md` (repo conventions, layout, contribution rules). This file is about *doing things with* SeleniumBase. Method names below are taken from the README. For the full API see `help_docs/method_summary.md` (BaseCase/SB) and `help_docs/cdp_mode_methods.md` (CDP Mode), and verify a method exists there before using it.

## Skill index

1. [Choose the right syntax format](#1-choose-the-right-syntax-format)
2. [Write a pytest E2E test (BaseCase)](#2-write-a-pytest-e2e-test-basecase)
3. [Write a standalone automation script (SB / Driver)](#3-write-a-standalone-automation-script-sb--driver)
4. [Scrape or automate with stealth (Pure CDP Mode)](#4-scrape-or-automate-with-stealth-pure-cdp-mode)
5. [Handle bot-detection and CAPTCHAs (UC + CDP Mode)](#5-handle-bot-detection-and-captchas-uc--cdp-mode)
6. [Use Playwright through a stealthy browser](#6-use-playwright-through-a-stealthy-browser)
7. [Handle iframes, tabs, alerts, and JavaScript](#7-handle-iframes-tabs-alerts-and-javascript)
8. [Debug a failing or flaky test](#8-debug-a-failing-or-flaky-test)
9. [Run in CI, headless, or in parallel](#9-run-in-ci-headless-or-in-parallel)
10. [Scaffold a new test project](#10-scaffold-a-new-test-project)
11. [Generate tests with the Recorder](#11-generate-tests-with-the-recorder)
12. [Produce reports and dashboards](#12-produce-reports-and-dashboards)
13. [Migrate raw Selenium code](#13-migrate-raw-selenium-code)
14. [Configure proxies, user agents, and browsers](#14-configure-proxies-user-agents-and-browsers)

---

## 1. Choose the right syntax format

**Use when:** starting any new script or test.

| Need | Use | Run with |
| --- | --- | --- |
| Structured tests, pytest features, reports, CLI options | `BaseCase` class (`self.click(...)`) | `pytest` / `pynose` |
| Tests written as pytest functions | `sb` pytest fixture | `pytest` only |
| One-off automation or scraping script | `with SB(...) as sb:` | `python` |
| Drop-in improved Selenium driver | `Driver()` | `python` |
| Maximum stealth, no WebDriver | `sb_cdp.Chrome()` (Pure CDP Mode) | `python` |
| Gherkin/BDD | `behave` features | `behave` |

**Rule of thumb:** tests belong in `BaseCase` under pytest; scripts belong in `SB()` or `sb_cdp`; anything that must evade bot-detection should start with CDP Mode. See `help_docs/syntax_formats.md`.

## 2. Write a pytest E2E test (BaseCase)

**Use when:** verifying behavior of a web app.

```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)  # lets `python file.py` invoke pytest

class LoginTests(BaseCase):
    def test_login(self):
        self.goto("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")   # "\n" presses Enter
        self.assert_element("div.inventory_list")
        self.assert_exact_text("Products", "span.title")
```

**Steps**
1. Name the file `test_*.py` or `*_test.py`, and methods `test_*`. The class name can be anything.
2. Navigate with `self.goto(url)`. Interact with `self.click`, `self.type`, `self.select_option_by_text`, `self.hover_and_click`, `self.drag_and_drop`.
3. Verify with `assert_element`, `assert_text`, `assert_exact_text`, `assert_title`, `assert_downloaded_file`, `assert_no_404_errors`, `assert_no_js_errors`.
4. Run: `pytest test_login.py` (add `--headless` on servers).

**Guidelines**
- Selectors are CSS by default (XPath auto-detected). Use `:contains("text")` and `[attr*="partial"]` when handy.
- SeleniumBase methods wait automatically (default timeouts). Pass `timeout=N` to override. Do **not** add `time.sleep()` to fix timing.
- Use `self.type(sel, text)`, not `add_text`/`send_keys`, unless you deliberately don't want the field cleared.
- Batch several checks on one page with **deferred asserts** (`deferred_assert_element`, `deferred_assert_text`, ..., then `self.process_deferred_asserts()`). Call it before navigating to a new page.
- For conditionals use `is_element_visible`, `is_element_present`, `is_text_visible`, `is_link_text_visible`.

## 3. Write a standalone automation script (SB / Driver)

**Use when:** you need a script, not a test suite.

```python
from seleniumbase import SB

with SB(test=True) as sb:            # add uc=True for UC Mode, headless=True for headless
    sb.goto("seleniumbase.io/simple/login")
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.click('a:contains("Sign in")')
    sb.assert_exact_text("Welcome!", "h1")
```

`Driver()` gives an improved Selenium driver (same helper methods). Always close it:

```python
from seleniumbase import Driver
driver = Driver()
try:
    driver.goto("https://example.com")
finally:
    driver.quit()
```

Raw Selenium is available via `sb.driver` / `self.driver`. Run with plain `python script.py`. Name such files `raw_*.py` in `examples/` so pytest doesn't collect them.

## 4. Scrape or automate with stealth (Pure CDP Mode)

**Use when:** scraping or automating sites that fingerprint WebDriver. Requires a Chromium-based browser.

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()                 # options seen in docs: incognito=True, guest=True,
sb.goto("https://news.ycombinator.com/submitted?id=seleniumbase")  # locale="en", ad_block=True,
for el in sb.find_elements("span.titleline > a"):                   # use_chromium=True, cft=True
    print("* " + el.text)
sb.quit()
```

**Steps**
1. Create the browser with `sb_cdp.Chrome(...)`; navigate with `sb.goto(url)`.
2. Locate with `find_elements`, act with `click`/`type`, and check with `assert_element`/`assert_text`. Confirm names in `help_docs/cdp_mode_methods.md`.
3. Use `sb.highlight(...)`/`sb.flash(...)` only for demos; skip them in production scrapers.
4. Always call `sb.quit()` (use `try/finally`).

**Choosing a browser:** Google Chrome is the default. Alternatives via method args (`cft=True`, `use_chromium=True`, `browser="edge"`, `browser="brave"`) or CLI flags (`--cft`, `--chromium`, `--edge`, `--brave`). Only unbranded Chromium and Chrome-for-Testing auto-install.

**Avoid:** mixing this with Firefox/Safari (CDP Mode is Chromium-only).

## 5. Handle bot-detection and CAPTCHAs (UC + CDP Mode)

**Use when:** a page shows a Cloudflare-style challenge or Turnstile, or blocks a normal WebDriver session.

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    sb.activate_cdp_mode("https://gitlab.com/users/sign_in")
    sb.sleep(2)
    sb.solve_captcha()   # does nothing if no CAPTCHA is present
    sb.assert_element('label[for="user_login"]')
```

Or in Pure CDP Mode: `sb = sb_cdp.Chrome(incognito=True); sb.goto(url); sb.sleep(2); sb.solve_captcha()`.

**Guidance**
- Prefer **CDP Mode** (via `activate_cdp_mode` or `sb_cdp`) for maximum stealth. UC Mode alone is the older path.
- Use `sb.click_if_visible(selector)` for optional consent banners.
- Verify stealth against test pages such as browserscan.net/bot-detection or bot.sannysoft.com. Run **headed** when investigating detection problems; headless can change your fingerprint.
- Keep this to legitimate testing, monitoring, and scraping. Respect site terms and robots policies, and don't build tooling meant to attack or abuse sites.

## 6. Use Playwright through a stealthy browser

**Use when:** you already have Playwright code and want SeleniumBase's stealth.

```python
from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(guest=True)
endpoint_url = sb.get_endpoint_url()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    page = browser.contexts[0].pages[0]
    page.goto("https://bot.sannysoft.com/")
```

Install both packages: `pip install seleniumbase playwright`. Reuse the existing context and page (`contexts[0].pages[0]`) rather than creating new ones. Examples: `examples/cdp_mode/playwright/`.

## 7. Handle iframes, tabs, alerts, and JavaScript

- **iframes:** `self.switch_to_frame("iframe")` → act → `self.switch_to_parent_frame()`; or `with self.frame_switch("iframe"):` (nestable). Exit all with `self.switch_to_default_content()`.
- **Tabs/windows:** SeleniumBase auto-switches to new tabs that don't open `about:blank`. Otherwise `self.switch_to_window(1)`; back with `self.switch_to_default_window()`. Use `open_new_window()` to create one.
- **Alerts:** `self.accept_alert()` / `self.dismiss_alert()`. If `self.click()` dismisses the pop-up itself (it waits for `readyState`), use `self.find_element(SEL).click()` and then `accept_alert()`.
- **JavaScript:** `self.execute_script(...)`; call `self.activate_jquery()` first if you need jQuery on a page without it. On pages with a strict CSP, add `--disable-csp`.
- **Raw WebDriver escape hatch:** `self.driver.<selenium method>`.

## 8. Debug a failing or flaky test

Work through in order:

1. **Reproduce narrowly:** `pytest file.py::Class::test_name` (add `-x -v`).
2. **Watch it:** `--demo` (slows and highlights actions) or run headed.
3. **Read the evidence:** on failure, screenshots and logs are saved in `./latest_logs/`.
4. **Pause interactively:** `--pdb` (post-mortem, browser stays open) or `--trace` (debug from test start), or drop in `breakpoint()`. Never use these in CI.
5. **Check the selector:** inspect the page, prefer stable attributes over long chains; use `wait_for_element` / `assert_element` with a larger `timeout=`.
6. **Global timing slack:** `--timeout-multiplier=2`, or `--pls=eager` for slow pages.
7. **Retry as a last resort:** `--reruns=1 --reruns-delay=1`, or `@retry_on_exception()`. Retries hide bugs, so fix the root cause first.
8. **Stealth-related failures:** switch to CDP Mode (skill 5) and test headed.

`test_fail.py` is meant to fail. It's a logging demo, not a bug.

## 9. Run in CI, headless, or in parallel

```bash
pytest tests/ --headless --rs --html=report.html --junit-xml=report.xml
pytest tests/ -n=4 --headless            # parallel across 4 workers
pytest tests/ --xvfb                     # Linux virtual display when a headed browser is needed
```

- Linux runs headless by default; use `--headed` to force a GUI. `--headless2` supports extensions.
- `--rs` reuses one browser session for all tests (faster, but state leaks between tests; use `--crumbs` to clear cookies between them).
- Set `--driver-version=VER` to pin the driver.
- No `--pdb`, `--trace`, or `--show-report` in CI.
- Cache/allow downloads of browsers and drivers on first run. Offline runs work only if drivers were previously downloaded.
- Ready-made CI examples live in `integrations/` (GitHub Actions, Jenkins, Azure, Google Cloud). `sbase mkdir DIR --gha` adds a GitHub Actions workflow.
- Scale out with Selenium Grid: `--server=HOST --port=PORT` (see `seleniumbase/utilities/selenium_grid/`).

## 10. Scaffold a new test project

```bash
sbase mkdir ui_tests           # config files + sample tests + boilerplates
sbase mkdir ui_tests --basic   # only pytest.ini, setup.cfg, requirements.txt, __init__.py
sbase mkdir ui_tests --gha     # also adds a GitHub Actions workflow
```

- `pytest.ini` is the most important file (defaults for pytest); `setup.cfg` is for `pynose`.
- Each test folder needs an (empty) `__init__.py` so tests can import siblings.
- `sbase mkfile FILE.py` creates a single test file. Boilerplates for page objects and the `sb` fixture are included by the full scaffold.

## 11. Generate tests with the Recorder

```bash
sbase recorder                       # desktop app
sbase mkrec test_new.py              # (alias: codegen) start recording to a file
pytest test_new.py --rec             # ...or use the pytest options below
```

Recorder pytest flags include `--recorder`, `--rec-sb-mgr` (emit `SB()` code), `--rec-sb-cdp` (emit `sb_cdp` code), `--rec-behave`, and `--rec-print`. Treat recorded output as a draft: replace brittle selectors, remove needless `sleep` calls, and add real assertions. See `help_docs/recorder_mode.md`.

## 12. Produce reports and dashboards

| Goal | Command |
| --- | --- |
| Live dashboard (`dashboard.html`) | `pytest --dashboard --rs --headless` |
| pytest HTML report | `pytest --html=report.html` |
| Dashboard folded into the HTML report | `pytest --dashboard --html=report.html` |
| JUnit XML for CI | `pytest --junit-xml=report.xml` |
| pynose report | `pynose test_suite.py --report` (`--show-report` only locally) |
| behave | `behave features/ -D dashboard -D headless` |
| Allure | `pip install allure-pytest` (not bundled), then `pytest --alluredir=allure_results` |

Serve the dashboard locally: `python -m http.server 1948`, then open `http://localhost:1948/dashboard.html`.

## 13. Migrate raw Selenium code

| Raw Selenium | SeleniumBase |
| --- | --- |
| `WebDriverWait(...).until(EC.element_to_be_clickable(...)).click()` | `self.click(sel, timeout=10)` |
| `driver.find_element(By.CSS_SELECTOR, s).clear(); .send_keys(t)` | `self.type(s, t)` |
| Manual waits + `assert el.is_displayed()` | `self.assert_element(s)` |
| `driver.get(url)` | `self.goto(url)` |
| Hand-rolled argparse for browser choice | `--browser=...`, `--headless`, etc. |

Migration examples: `examples/migration/raw_selenium/`. CLI helper: `sbase convert WEBDRIVER_UNITTEST_FILE.py`. Keep raw `self.driver` calls only where no SeleniumBase equivalent exists.

## 14. Configure proxies, user agents, and browsers

```bash
pytest t.py --proxy=IP:PORT
pytest t.py --proxy=USER:PASS@IP:PORT       # authenticated (Chromium only)
pytest t.py --proxy="socks5://IP:PORT"      # socks4/socks5 supported
pytest t.py --proxy=proxy1                  # key from seleniumbase/config/proxy_list.py
pytest t.py --agent="USER AGENT STRING"     # Chromium and Firefox
pytest t.py --locale=en --mobile            # locale, mobile emulation
pytest t.py --chrome | --edge | --firefox | --safari | --brave | --chromium | --cft
```

- Per-run overrides of defaults (timeouts, credentials) go in a custom settings file: `--settings-file=custom_settings.py` (see `examples/custom_settings.py`).
- Pass test data with `--data`, `--var1..3`, `--variables`, `--env`, `--account`; read them via `self.data`, `self.var1`, `self.env`, etc.
- **Never hard-code real credentials.** Use environment variables or an untracked settings file.

---

## Cross-cutting rules for agents

- **Prefer the smallest change and the smallest test run.** Browser tests are slow and touch live sites.
- **Look up before you write.** Confirm a method or flag in `help_docs/` or the source (`seleniumbase/plugins/pytest_plugin.py` defines pytest options) instead of guessing.
- **Match runner to format.** `sb` fixture → `pytest` only; `raw_*.py` → `python`; BDD → `behave`.
- **Clean up.** Close browsers (`quit()`, context managers, `finally`), and don't commit `latest_logs/`, `archived_logs/`, `downloaded_files/`, or report files.
- **Be a good web citizen.** Rate-limit, respect site terms, and use stealth features only for legitimate automation.
