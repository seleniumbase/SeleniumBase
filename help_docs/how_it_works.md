<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) How SeleniumBase Works 👁️

<a id="how_seleniumbase_works"></a>

👁️🔎 At the core, SeleniumBase works by extending [pytest](https://docs.pytest.org/en/latest/) as a direct plugin. SeleniumBase automatically spins up web browsers for tests (using [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)), and then gives those tests access to the SeleniumBase libraries through the [BaseCase class](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py). Tests are also given access to [SeleniumBase command-line arguments](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md) and [SeleniumBase methods](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md), which provide additional functionality.

👁️🔎 ``pytest`` uses a feature called test discovery to automatically find and run Python methods that start with ``test_`` when those methods are located in Python files that start with ``test_`` or end with ``_test.py``.

👁️🔎 The most common way of using **SeleniumBase** is by inheriting ``BaseCase``:

```python
from seleniumbase import BaseCase
```

Then have your test classes inherit ``BaseCase``:

```python
class MyTestClass(BaseCase):
```

Here's what a full test might look like:

```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

class TestMFALogin(BaseCase):
    def test_mfa_login(self):
        self.open("https://seleniumbase.io/realworld/login")
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        self.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
        self.assert_text("Welcome!", "h1")
        self.highlight("img#image1")  # A fancier assert_element() call
        self.click('a:contains("This Page")')  # Use :contains() on any tag
        self.save_screenshot_to_logs()  # ("./latest_logs" folder for test)
        self.click_link("Sign out")  # Link must be "a" tag. Not "button".
        self.assert_element('a:contains("Sign in")')
        self.assert_exact_text("You have been signed out!", "#top_message")
```

(See the example, [test_mfa_login.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_mfa_login.py), for reference.)

👁️🔎 Here are some examples of running tests with ``pytest``:

```bash
pytest --headless --rs --dashboard --html=report.html -v -n=4
pytest test_mfa_login.py
pytest -m marker2
pytest offline_examples/
pytest -k agent
```

(See <a href="https://seleniumbase.io/help_docs/syntax_formats/">SyntaxFormats</a> for more ways of using <b>SeleniumBase</b>.)

--------

### ✅ No More Flaky Tests!

<p>SeleniumBase methods automatically wait for page elements to finish loading before interacting with them (<i>up to a timeout limit</i>). This means <b>you no longer need random <span><code>time.sleep()</code></span> statements</b> in your scripts.</p>
<img src="https://img.shields.io/badge/Flaky%20Tests%3F-%20NO%21-11BBDD.svg" alt="NO MORE FLAKY TESTS!" />

**There are three layers of protection that provide reliability for tests using SeleniumBase:**

* **(1)**: Selenium's default ``pageLoadStrategy`` is ``normal``: This strategy causes Selenium to wait for the full page to load, with HTML content and sub-resources downloaded and parsed.

* **(2)**: SeleniumBase includes methods such as ``wait_for_ready_state_complete()`` and ``wait_for_angularjs()``, which run inside other SeleniumBase methods to ensure that it's safe to proceed with the next command.

* **(3)**: SeleniumBase methods automatically wait for elements to be visible and interactable before interacting with those elements.

**If you want to speed up your tests and you think the third level of protection is enough by itself, you can use command-line options to remove the first, the second, or both of those first two levels of protection:**

* ``--pls=none`` --> Set ``pageLoadStrategy`` to ``"none"``: This strategy causes Selenium to return immediately after the initial HTML content is fully received by the browser.

* ``--sjw`` --> Skip JS Waits, which include ``wait_for_ready_state_complete()`` and ``wait_for_angularjs()``.

--------

<p><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/cdn/img/super_logo_sb.png" alt="SeleniumBase" title="SeleniumBase" width="300" /></a></p>
<p><a href="https://www.python.org/downloads/" target="_blank"><img src="https://img.shields.io/pypi/pyversions/seleniumbase.svg?color=22AAEE&logo=python" title="Supported Python Versions" /></a></p>
