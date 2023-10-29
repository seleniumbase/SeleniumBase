<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) How SeleniumBase Works 👁️

<a id="how_seleniumbase_works"></a>

👁️🔎 The primary [SeleniumBase syntax format](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md) works by extending [pytest](https://docs.pytest.org/en/latest/) as a direct plugin. SeleniumBase automatically spins up web browsers for tests (using [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)), and then gives those tests access to the SeleniumBase libraries through the [BaseCase class](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py). Tests are also given access to [SeleniumBase command-line options](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md) and [SeleniumBase methods](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md), which provide additional functionality.

👁️🔎 ``pytest`` uses a feature called test discovery to automatically find and run Python methods that start with ``test_`` when those methods are located in Python files that start with ``test_`` or end with ``_test.py``.

👁️🔎 The primary [SeleniumBase syntax format](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md) starts by importing ``BaseCase``:

```python
from seleniumbase import BaseCase
```

👁️🔎 This next line activates ``pytest`` when a file is called directly with ``python`` by accident:

```python
BaseCase.main(__name__, __file__)
```

👁️🔎 Classes can inherit ``BaseCase`` to gain SeleniumBase functionality:

```python
class MyTestClass(BaseCase):
```

👁️🔎 Test methods inside ``BaseCase`` classes become SeleniumBase tests: (These tests automatically launch a web browser before starting, and quit the web browser after ending. Default settings can be changed via command-line options.)

```python
class MyTestClass(BaseCase):
    def test_abc(self):
        # ...
```

👁️🔎 [SeleniumBase APIs](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md) can be called from tests via ``self``:

```python
class MyTestClass(BaseCase):
    def test_abc(self):
        self.open("https://example.com")
```

👁️🔎 Here's what a full test might look like:

```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

class TestSimpleLogin(BaseCase):
    def test_simple_login(self):
        self.open("https://seleniumbase.io/simple/login")
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        self.click('a:contains("Sign in")')
        self.assert_exact_text("Welcome!", "h1")
        self.assert_element("img#image1")
        self.highlight("#image1")
        self.click_link("Sign out")
        self.assert_text("signed out", "#top_message")
```

(See the example, [test_simple_login.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_simple_login.py), for reference.)

👁️🔎 Here are some examples of running tests with ``pytest``:

```bash
pytest test_mfa_login.py
pytest --headless -n8 --dashboard --html=report.html -v --rs --crumbs
pytest -m marker2
pytest -k agent
pytest offline_examples/
```

👁️🔎 Here's a [SeleniumBase syntax format](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md) that uses the raw `driver`. Unlike the format mentioned earlier, it can be run with `python` instead of `pytest`. The `driver` includes original `driver` methods and new ones added by SeleniumBase:

```python
from seleniumbase import Driver

driver = Driver()
try:
    driver.get("https://seleniumbase.io/simple/login")
    driver.type("#username", "demo_user")
    driver.type("#password", "secret_pass")
    driver.click('a:contains("Sign in")')
    driver.assert_exact_text("Welcome!", "h1")
    driver.assert_element("img#image1")
    driver.highlight("#image1")
    driver.click_link("Sign out")
    driver.assert_text("signed out", "#top_message")
finally:
    driver.quit()
```

(See the example, [raw_login_driver.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_login_driver.py), for reference.)

👁️🔎 Note that regular SeleniumBase formats (ones that use `BaseCase`, the `SB` context manager, or the `sb` `pytest` fixture) have more methods than the improved `driver` format. The regular formats also have more features. Some features, (such as the [SeleniumBase dashboard](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md)), require a `pytest` format.

--------

### ✅ No More Flaky Tests!

<p>SeleniumBase methods automatically wait for page elements to finish loading before interacting with them (<i>up to a timeout limit</i>). This means <b>you no longer need random <span><code>time.sleep()</code></span> statements</b> in your scripts.</p>
<img src="https://img.shields.io/badge/Flaky%20Tests%3F-%20NO%21-11BBDD.svg" alt="NO MORE FLAKY TESTS!" />

**There are three layers of protection that provide reliability for tests using SeleniumBase:**

* **(1)**: Selenium's default ``pageLoadStrategy`` is ``normal``: This strategy causes Selenium to wait for the full page to load, with HTML content and sub-resources downloaded and parsed.

* **(2)**: SeleniumBase includes methods such as ``wait_for_ready_state_complete()``, which run inside other SeleniumBase methods to ensure that it's safe to proceed with the next command.

* **(3)**: SeleniumBase methods automatically wait for elements to be visible and interactable before interacting with those elements.

**If you want to speed up your tests and you think the third level of protection is enough by itself, you can use command-line options to remove the first, the second, or both of those first two levels of protection:**

* ``--pls=none`` --> Set ``pageLoadStrategy`` to ``"none"``: This strategy causes Selenium to return immediately after the initial HTML content is fully received by the browser.

* ``--sjw`` --> Skip JS Waits, such as ``wait_for_ready_state_complete()``.

--------

<p><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/cdn/img/super_logo_sb.png" alt="SeleniumBase" title="SeleniumBase" width="300" /></a></p>
<p><a href="https://www.python.org/downloads/" target="_blank"><img src="https://img.shields.io/pypi/pyversions/seleniumbase.svg?color=22AAEE&logo=python&logoColor=FEDC54" title="Supported Python Versions" /></a></p>
