<!-- SeleniumBase Docs -->

<meta property="og:site_name" content="SeleniumBase">
<meta property="og:title" content="SeleniumBase: Python Web Automation and E2E Testing" />
<meta property="og:description" content="Fast, easy, and reliable Web/UI testing with Python." />
<meta property="og:keywords" content="Python, pytest, selenium, webdriver, testing, automation, seleniumbase, framework, dashboard, recorder, reports, screenshots">
<meta property="og:image" content="https://seleniumbase.github.io/cdn/img/mac_sb_logo_5b.png" />
<link rel="icon" href="https://seleniumbase.github.io/img/logo7.png" />

<h1>SeleniumBase</h1>

<h3 align="center"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/cdn/img/sb_logo_10t.png" alt="SeleniumBase" title="SeleniumBase" width="266" /></a></h3>

<h3 align="center">Create reliable end-to-end browser tests with Python</h3>

<p align="center"><a href="https://pypi.python.org/pypi/seleniumbase" target="_blank"><img src="https://img.shields.io/pypi/v/seleniumbase.svg?color=3399EE" alt="PyPI version" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/releases" target="_blank"><img src="https://img.shields.io/github/v/release/seleniumbase/SeleniumBase.svg?color=22AAEE" alt="GitHub version" /></a> <a href="https://seleniumbase.io"><img src="https://img.shields.io/badge/docs-seleniumbase.io-11BBAA.svg" alt="SeleniumBase Docs" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/actions" target="_blank"><img src="https://github.com/seleniumbase/SeleniumBase/workflows/CI%20build/badge.svg" alt="SeleniumBase GitHub Actions" /></a> <a href="https://gitter.im/seleniumbase/SeleniumBase" target="_blank"><img src="https://img.shields.io/gitter/room/seleniumbase/SeleniumBase.svg" alt="Gitter chat"/></a></p>

<p align="center">
<a href="#python_installation">🚀 Start</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/features_list.md">🏰 Features</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/ReadMe.md">📚 Examples</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md">🎛️ Options</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/console_scripts/ReadMe.md">🌠 Scripts</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/mobile_testing.md">📱 Phone</a>
<br />
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md">📘 APIs</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md"> 🔡 Formats</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md">📊 Dashboard</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/recorder_mode.md">🔴 Recorder</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/locale_codes.md">🗾 Locales</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md">🌐 Grid</a>
<br />
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/commander.md">🎖️ GUI</a> |
<a href="https://seleniumbase.io/demo_page">📰 TestPage</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/case_plans.md">🗂️ CasePlans</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/html_inspector.md">🕵️ Inspector</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/master_qa/ReadMe.md">🧬 Hybrid</a> |
<a href="https://seleniumbase.io/devices/?url=seleniumbase.com">💻 Farm</a>
<br />
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/how_it_works.md">👁️ How</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples/migration/raw_selenium">🚝 Migrate</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples/boilerplates">♻️ Templates</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/node_js">🚉 NodeGUI</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/chart_maker/ReadMe.md">📶 Charts</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md">🚎 Tours</a>
<br />
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/github/workflows/ReadMe.md">🤖 CI/CD</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/js_package_manager.md">🕹️ JSMgr</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/translations.md">🌏 Translator</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/ReadMe.md">🎞️ Presenter</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/dialog_boxes/ReadMe.md">🛂 Boxes</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/visual_testing/ReadMe.md">🖼️ Visual</a>
<br />
</p>

--------

<a id="multiple_examples"></a>
<p align="left"><b>Example:</b> <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_coffee_cart.py" target="_blank">test_coffee_cart.py</a> from <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples" target="_blank">./examples/</a></p>

```bash
cd examples/
pytest test_coffee_cart.py --demo
```

<p>(<code>--demo</code> mode slows down tests and highlights actions)</p>

<p align="left"><a href="https://seleniumbase.io/coffee/" target="_blank"><img src="https://seleniumbase.github.io/cdn/gif/coffee_cart.gif" width="480" alt="SeleniumBase Coffee Cart Test" title="SeleniumBase Coffee Cart Test" /></a></p>

* Here's a preview of that test:

```python
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

class CoffeeCartTest(BaseCase):
    def test_coffee_cart(self):
        self.open("https://seleniumbase.io/coffee/")
        self.assert_title("Coffee Cart")
        self.click('div[data-sb="Cappuccino"]')
        self.click('div[data-sb="Flat-White"]')
        self.click('div[data-sb="Cafe-Latte"]')
        self.click('a[aria-label="Cart page"]')
        self.assert_exact_text("Total: $53.00", "button.pay")
        self.click("button.pay")
        self.type("input#name", "Selenium Coffee")
        self.type("input#email", "test@test.test")
        self.click("button#submit-payment")
        self.assert_text("Thanks for your purchase.", "#app .success")
```

--------

<details>
<summary> ▶️ How is <b>SeleniumBase</b> different from raw Selenium? (<b>click to expand</b>)</summary>
<div>

<p>💡 SeleniumBase is a Python framework for browser automation and testing. SeleniumBase uses <a href="https://www.w3.org/TR/webdriver2/#endpoints" target="_blank">Selenium/WebDriver</a> APIs, and incorporates test-runners such as <code>pytest</code>, <code>nosetests</code>, and <code>behave</code> to provide organized structure, test discovery, test execution, test state (<i>eg. passed, failed, or skipped</i>), and command-line options for changing default settings (<i>such as choosing the browser to use</i>). With raw Selenium, you would need to set up your own options-parser for configuring tests from the command-line.</p>

<p>💡 With raw Selenium, commands that use selectors need to specify the type of selector (eg. <code>"css selector", "button#myButton"</code>). With SeleniumBase, there's auto-detection between CSS Selectors and XPath, which means you don't need to specify the type of selector in your commands (<i>but optionally you could</i>).</p>

<p>💡 SeleniumBase methods often perform multiple actions in a single method call. For example, <code>self.type(selector,text)</code> does the following:<br />1. Waits for the element to be visible.<br />2. Waits for the element to be interactive.<br />3. Clears the text field.<br />4. Types in the new text.<br />5. Presses Enter/Submit if the text ends in "\n".<br />With raw Selenium, those actions require multiple method calls.</p>

<p>💡 SeleniumBase uses default timeout values when not set:<br />
✅<code>self.click("button")</code><br />
With raw Selenium, methods would fail instantly (<i>by default</i>) if an element needed more time to load:<br />
❌<code>self.driver.find_element(by="css selector", value="button").click()</code><br />
(Reliable code is better than unreliable code.)</p>

<p>💡 SeleniumBase lets you change the explicit timeout values of methods:<br />
✅<code>self.click("button",timeout=10)</code><br />
With raw Selenium, that requires more code:<br />
❌<code>WebDriverWait(driver,10).until(EC.element_to_be_clickable("css selector", "button")).click()</code><br />
(Simple code is better than complex code.)</p>

<p>💡 SeleniumBase gives you clean error output when a test fails. With raw Selenium, error messages can get very messy.</p>

<p>💡 SeleniumBase gives you the option to generate a dashboard and reports for tests. It also saves screenshots from failing tests to the <code>./latest_logs/</code> folder. Raw <a href="https://www.selenium.dev/documentation/webdriver/" target="_blank">Selenium</a> does not have these options out-of-the-box.</p>

<p>💡 SeleniumBase includes desktop GUI apps for running tests, such as <b>SeleniumBase Commander</b> for <code>pytest</code>, and <b>SeleniumBase Behave GUI.</b></p>

<p>💡 SeleniumBase has its own Recorder & Test Generator that can create tests from manual browser actions. SeleniumBase also has many other useful tools and console scripts for getting things done quickly. (<i>See the documentation for more details!</i>)</p>

</div>
</details>

--------

<details>
<summary> ▶️ Learn about different ways of writing tests (<b>click to expand</b>)</summary>
<div>

<p align="left">📘📝 An example test with the <b>BaseCase</b> class. Runs with <b><a href="https://docs.pytest.org/en/latest/how-to/usage.html">pytest</a></b> or <b>nosetests</b>. (<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/ReadMe.md">Learn more</a>)</p>

```python
from seleniumbase import BaseCase

class TestMFALogin(BaseCase):
    def test_mfa_login(self):
        self.open("https://seleniumbase.io/realworld/login")
        self.type("#username", "demo_user")
        self.type("#password", "secret_pass")
        self.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
        self.assert_exact_text("Welcome!", "h1")
        self.assert_element("img#image1")
        self.click('a:contains("This Page")')
        self.save_screenshot_to_logs()
```

<p align="left">📗📝 An example test with the <b><code>sb</code></b> <code>pytest</code> fixture. Runs with <b><a href="https://docs.pytest.org/en/latest/how-to/usage.html">pytest</a></b>.</p>

```python
def test_mfa_login(sb):
    sb.open("https://seleniumbase.io/realworld/login")
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
    sb.assert_exact_text("Welcome!", "h1")
    sb.assert_element("img#image1")
    sb.click('a:contains("This Page")')
    sb.save_screenshot_to_logs()
```

<p align="left">📙📝 An example test with the <b><code>SB</code></b> Context Manager. Runs with pure <b><code>python</code></b>.</p>

```python
from seleniumbase import SB

with SB() as sb:  # By default, browser="chrome" if not set.
    sb.open("https://seleniumbase.io/realworld/login")
    sb.type("#username", "demo_user")
    sb.type("#password", "secret_pass")
    sb.enter_mfa_code("#totpcode", "GAXG2MTEOR3DMMDG")  # 6-digit
    sb.assert_text("Welcome!", "h1")
    sb.highlight("img#image1")  # A fancier assert_element() call
    sb.click('a:contains("This Page")')  # Use :contains() on any tag
    sb.click_link("Sign out")  # Link must be "a" tag. Not "button".
    sb.assert_element('a:contains("Sign in")')
    sb.assert_exact_text("You have been signed out!", "#top_message")
```

<p align="left">📕📝 An example test with <b>behave-BDD</b> <a href="https://behave.readthedocs.io/en/stable/gherkin.html" target="_blank">Gherkin</a> structure. Runs with <b><code>behave</code></b>. (<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/behave_bdd/ReadMe.md">Learn more</a>)</p>

```gherkin
Feature: SeleniumBase scenarios for the RealWorld App

  Scenario: Verify RealWorld App
    Given Open "seleniumbase.io/realworld/login"
    When Type "demo_user" into "#username"
    And Type "secret_pass" into "#password"
    And Do MFA "GAXG2MTEOR3DMMDG" into "#totpcode"
    Then Assert exact text "Welcome!" in "h1"
    And Assert element "img#image1"
    And Click 'a:contains("This Page")'
    And Save screenshot to logs
```

</div>
</details>

--------

<a id="python_installation"></a>
<h2><img src="https://seleniumbase.github.io/cdn/img/python_logo.png" title="SeleniumBase" width="42" /> Set up Python & Git:</h2>

🔵 Add <b><a href="https://www.python.org/downloads/">Python</a></b> and <b><a href="https://git-scm.com/">Git</a></b> to your System PATH.

🔵 Using a <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md">Python virtual env</a> is recommended.

<a id="install_seleniumbase"></a>
<h2><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Install SeleniumBase:</h2>

**You can install ``seleniumbase`` from [GitHub](https://github.com/seleniumbase/SeleniumBase) or [PyPI](https://pypi.org/project/seleniumbase/):**

🔵 **Installing ``seleniumbase`` from a GitHub clone:**

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install -e .
```

**To upgrade an existing install from a GitHub clone:**

```bash
git pull
pip install -e .
```

🔵 **Installing ``seleniumbase`` from PyPI:**

```bash
pip install seleniumbase
```

* (Add ``--upgrade`` OR ``-U`` to upgrade SeleniumBase.)
* (Add ``--force-reinstall`` to upgrade indirect libraries.)
* (Use ``pip3`` if multiple versions of Python are present.)

**To upgrade an existing install from PyPI:**

```bash
pip install -U seleniumbase
```

🔵 Type ``seleniumbase`` or ``sbase`` to verify that SeleniumBase was installed successfully:

```bash
   ______     __           _                  ____                
  / ____/__  / /__  ____  (_)_  ______ ___   / _  \____  ________ 
  \__ \/ _ \/ / _ \/ __ \/ / / / / __ `__ \ / /_) / __ \/ ___/ _ \
 ___/ /  __/ /  __/ / / / / /_/ / / / / / // /_) / (_/ /__  /  __/
/____/\___/_/\___/_/ /_/_/\__,_/_/ /_/ /_//_____/\__,_/____/\___/ 
------------------------------------------------------------------

 * USAGE: "seleniumbase [COMMAND] [PARAMETERS]"
 *    OR:        "sbase [COMMAND] [PARAMETERS]"

COMMANDS:
      get / install    [DRIVER] [OPTIONS]
      methods          (List common Python methods)
      options          (List common pytest options)
      behave-options   (List common behave options)
      gui / commander  [OPTIONAL PATH or TEST FILE]
      behave-gui       (SBase Commander for Behave)
      caseplans        [OPTIONAL PATH or TEST FILE]
      mkdir            [DIRECTORY] [OPTIONS]
      mkfile           [FILE.py] [OPTIONS]
      mkrec / codegen  [FILE.py] [OPTIONS]
      recorder         (Open Recorder Desktop App.)
      record           (If args: mkrec. Else: App.)
      mkpres           [FILE.py] [LANG]
      mkchart          [FILE.py] [LANG]
      print            [FILE] [OPTIONS]
      translate        [SB_FILE.py] [LANG] [ACTION]
      convert          [WEBDRIVER_UNITTEST_FILE.py]
      extract-objects  [SB_FILE.py]
      inject-objects   [SB_FILE.py] [OPTIONS]
      objectify        [SB_FILE.py] [OPTIONS]
      revert-objects   [SB_FILE.py] [OPTIONS]
      encrypt / obfuscate
      decrypt / unobfuscate
      download server  (Get Selenium Grid JAR file)
      grid-hub         [start|stop] [OPTIONS]
      grid-node        [start|stop] --hub=[HOST/IP]
 * (EXAMPLE: "sbase get chromedriver latest") *

    Type "sbase help [COMMAND]" for specific command info.
    For info on all commands, type: "seleniumbase --help".
    Use "pytest" for running tests.
```


<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Downloading web drivers:</h3>

✅ SeleniumBase automatically downloads web drivers as needed, such as ``chromedriver``, ``edgedriver``, and ``geckodriver``.

✅ To manually download a webdriver, see [Console Scripts](https://seleniumbase.io/seleniumbase/console_scripts/ReadMe/) OR [Webdriver Installation](https://seleniumbase.io/help_docs/webdriver_installation/).


<a id="basic_example_and_usage"></a>
<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Basic Example & Usage:</h3>

🔵 If you've cloned SeleniumBase, you can run tests from the [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder.

<p align="left">Here's <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py">my_first_test.py</a>:</p>

```bash
cd examples/
pytest my_first_test.py
```

> (Uses ``--chrome`` by default.)

<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py"><img src="https://seleniumbase.github.io/cdn/gif/swag_labs_4.gif" alt="SeleniumBase Test" title="SeleniumBase Test" width="480" /></a>

<p align="left"><b>Here's the code for <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py">my_first_test.py</a>:</b></p>

```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):
    def test_swag_labs(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_text("PRODUCTS", "span.title")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_text("YOUR CART", "span.title")
        self.assert_text("Backpack", "div.cart_item")
        self.click("button#checkout")
        self.type("#first-name", "SeleniumBase")
        self.type("#last-name", "Automation")
        self.type("#postal-code", "77123")
        self.click("input#continue")
        self.assert_text("CHECKOUT: OVERVIEW")
        self.assert_text("Backpack", "div.cart_item")
        self.click("button#finish")
        self.assert_exact_text("THANK YOU FOR YOUR ORDER", "h2")
        self.assert_element('img[alt="Pony Express"]')
        self.js_click("a#logout_sidebar_link")
        self.assert_element("div#login_button_container")
```

* By default, **[CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp)** are used for finding page elements.
* If you're new to CSS Selectors, games like [CSS Diner](http://flukeout.github.io/) can help you learn.
* For more reading, [here's an advanced guide on CSS attribute selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors).


<a id="common_methods"></a>
<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Here are some common SeleniumBase methods that you might find in tests:</h3>

```python
self.open(url)  # Navigate the browser window to the URL.
self.type(selector, text)  # Update the field with the text.
self.click(selector)  # Click the element with the selector.
self.click_link(link_text)  # Click the link containing text.
self.go_back()  # Navigate back to the previous URL.
self.select_option_by_text(dropdown_selector, option)
self.hover_and_click(hover_selector, click_selector)
self.drag_and_drop(drag_selector, drop_selector)
self.get_text(selector)  # Get the text from the element.
self.get_current_url()  # Get the URL of the current page.
self.get_page_source()  # Get the HTML of the current page.
self.get_attribute(selector, attribute)  # Get element attribute.
self.get_title()  # Get the title of the current page.
self.switch_to_frame(frame)  # Switch into the iframe container.
self.switch_to_default_content()  # Leave the iframe container.
self.open_new_window()  # Open a new window in the same browser.
self.switch_to_window(window)  # Switch to the browser window.
self.switch_to_default_window()  # Switch to the original window.
self.get_new_driver(OPTIONS)  # Open a new driver with OPTIONS.
self.switch_to_driver(driver)  # Switch to the browser driver.
self.switch_to_default_driver()  # Switch to the original driver.
self.wait_for_element(selector)  # Wait until element is visible.
self.is_element_visible(selector)  # Return element visibility.
self.is_text_visible(text, selector)  # Return text visibility.
self.sleep(seconds)  # Do nothing for the given amount of time.
self.save_screenshot(name)  # Save a screenshot in .png format.
self.assert_element(selector)  # Verify the element is visible.
self.assert_text(text, selector)  # Verify text in the element.
self.assert_title(title)  # Verify the title of the web page.
self.assert_downloaded_file(file)  # Verify file was downloaded.
self.assert_no_404_errors()  # Verify there are no broken links.
self.assert_no_js_errors()  # Verify there are no JS errors.
```

🔵 For the complete list of SeleniumBase methods, see: <b><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md">Method Summary</a></b>


<a id="fun_facts"></a>
<h2><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Fun Facts / Learn More:</h2>

<p>✅ SeleniumBase automatically handles common <a href="https://www.selenium.dev/documentation/webdriver/" target="_blank">WebDriver</a> actions such as launching web browsers before tests, saving screenshots during failures, and closing web browsers after tests.</p>

<p>✅ SeleniumBase lets you <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md">customize test runs from the command-line</a>.</p>

<p>✅ SeleniumBase uses simple syntax for commands. Example:</p>

```python
self.type("input", "dogs\n")
```

SeleniumBase tests can be run with <code>pytest</code> or <code>nosetests</code>. (There's also a <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/behave_bdd/ReadMe.md">behave BDD</a> format.)

```bash
pytest my_first_test.py --chrome

nosetests test_suite.py --firefox
```

<p>✅ <code>pytest</code> includes automatic test discovery. If you don't specify a specific file or folder to run, <code>pytest</code> will automatically search through all subdirectories for tests to run based on the following criteria:</p>

* Python files that start with ``test_`` or end with ``_test.py``.
* Python methods that start with ``test_``.

With a SeleniumBase [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/pytest.ini) file present, you can modify default discovery settings. The Python class name can be anything because ``seleniumbase.BaseCase`` inherits ``unittest.TestCase``, which triggers autodiscovery.

<p>✅ You can do a pre-flight check to see which tests would get discovered by <code>pytest</code> before the real flight:</p>

```bash
pytest --collect-only -q
```

<p>✅ You can be more specific when calling <code>pytest</code> on a file:</p>

```bash
pytest [FILE_NAME.py]::[CLASS_NAME]::[METHOD_NAME]

nosetests [FILE_NAME.py]:[CLASS_NAME].[METHOD_NAME]
```

<p>✅ No More Flaky Tests! SeleniumBase methods automatically wait for page elements to finish loading before interacting with them (<i>up to a timeout limit</i>). This means <b>you no longer need random <span><code>time.sleep()</code></span> statements</b> in your scripts.</p>
<img src="https://img.shields.io/badge/Flaky%20Tests%3F-%20NO%21-11BBDD.svg" alt="NO MORE FLAKY TESTS!" />

✅ SeleniumBase supports all major browsers and operating systems:
<p><b>Browsers:</b> Chrome, Edge, Firefox, and Safari.</p>
<p><b>Systems: </b>Linux/Ubuntu, macOS, and Windows.</p>

✅ SeleniumBase works on all popular CI/CD platforms:
<p><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/github/workflows/ReadMe.md"><img alt="GitHub Actions integration" src="https://img.shields.io/badge/GitHub_Actions-12B2C2.svg?logo=GitHubActions&logoColor=CFFFC2" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/jenkins/ReadMe.md"><img alt="Jenkins integration" src="https://img.shields.io/badge/Jenkins-32B242.svg?logo=jenkins&logoColor=white" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/azure_pipelines/ReadMe.md"><img alt="Azure integration" src="https://img.shields.io/badge/Azure-2288EE.svg?logo=AzurePipelines&logoColor=white" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/google_cloud/ReadMe.md"><img alt="Google Cloud integration" src="https://img.shields.io/badge/Google_Cloud-11CAE8.svg?logo=GoogleCloud&logoColor=EE0066" /></a> <a href="#utilizing_advanced_features"><img alt="AWS integration" src="https://img.shields.io/badge/AWS-4488DD.svg?logo=AmazonAWS&logoColor=FFFF44" /></a> <a href="https://en.wikipedia.org/wiki/Personal_computer" target="_blank"><img alt="Your Computer" src="https://img.shields.io/badge/💻_Your_Computer-44E6E6.svg" /></a></p>

<p>✅ SeleniumBase includes an automated/manual hybrid solution called <b><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/master_qa/ReadMe.md">MasterQA</a></b>, which speeds up manual testing by having automation perform all the browser actions while the manual tester handles validation.</p>

<p>✅ For a full list of SeleniumBase features, <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/features_list.md">Click Here</a>.</p>


<a id="detailed_instructions"></a>
<h2><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Detailed Instructions:</h2>

<a id="seleniumbase_demo_mode"></a>
🔵 <b>Demo Mode</b> helps you see what a test is doing. If a test is moving too fast for your eyes, run it in <b>Demo Mode</b>, which pauses the browser briefly between actions, highlights page elements being acted on, and displays assertions:

```bash
pytest my_first_test.py --demo
```

🔵 You can use the following calls in your scripts to help you debug issues:

```python
import time; time.sleep(5)  # Makes the test wait and do nothing for 5 seconds.
import pdb; pdb.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
import pytest; pytest.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
```

🔵 To pause an active test that throws an exception or error, (*and keep the browser window open while **Debug Mode** begins in the console*), add **``--pdb``** as a ``pytest`` option:

```bash
pytest my_first_test.py --pdb
```

(**``pdb``** console commands: ``n``, ``c``, ``s`` => ``next``, ``continue``, ``step``).

<a id="pytest_options"></a>
🔵 Here are some useful command-line options that come with <code>pytest</code>:

```bash
-v  # Verbose mode. Prints the full name of each test and shows more details.
-q  # Quiet mode. Print fewer details in the console output when running tests.
-x  # Stop running the tests after the first failure is reached.
--html=report.html  # Creates a detailed pytest-html report after tests finish.
--collect-only | --co  # Show what tests would get run. (Without running them)
-n=NUM  # Multithread the tests using that many threads. (Speed up test runs!)
-s  # See print statements. (Should be on by default with pytest.ini present.)
--junit-xml=report.xml  # Creates a junit-xml report after tests finish.
--pdb  # If a test fails, enter Post Mortem Debug Mode. (Don't use with CI!)
--trace  # Enter Debug Mode at the beginning of each test. (Don't use with CI!)
-m=MARKER  # Run tests with the specified pytest marker.
```

<a id="new_pytest_options"></a>
🔵 SeleniumBase provides additional <code>pytest</code> command-line options for tests:

```bash
--browser=BROWSER  # (The web browser to use. Default: "chrome".)
--chrome  # (Shortcut for "--browser=chrome". On by default.)
--edge  # (Shortcut for "--browser=edge".)
--firefox  # (Shortcut for "--browser=firefox".)
--safari  # (Shortcut for "--browser=safari".)
--settings-file=FILE  # (Override default SeleniumBase settings.)
--env=ENV  # (Set the test env. Access with "self.env" in tests.)
--account=STR  # (Set account. Access with "self.account" in tests.)
--data=STRING  # (Extra test data. Access with "self.data" in tests.)
--var1=STRING  # (Extra test data. Access with "self.var1" in tests.)
--var2=STRING  # (Extra test data. Access with "self.var2" in tests.)
--var3=STRING  # (Extra test data. Access with "self.var3" in tests.)
--variables=DICT  # (Extra test data. Access with "self.variables".)
--user-data-dir=DIR  # (Set the Chrome user data directory to use.)
--protocol=PROTOCOL  # (The Selenium Grid protocol: http|https.)
--server=SERVER  # (The Selenium Grid server/IP used for tests.)
--port=PORT  # (The Selenium Grid port used by the test server.)
--cap-file=FILE  # (The web browser's desired capabilities to use.)
--cap-string=STRING  # (The web browser's desired capabilities to use.)
--proxy=SERVER:PORT  # (Connect to a proxy server:port as tests are running)
--proxy=USERNAME:PASSWORD@SERVER:PORT  # (Use an authenticated proxy server)
--proxy-bypass-list=STRING # (";"-separated hosts to bypass, Eg "*.foo.com")
--proxy-pac-url=URL  # (Connect to a proxy server using a PAC_URL.pac file.)
--proxy-pac-url=USERNAME:PASSWORD@URL  # (Authenticated proxy with PAC URL.)
--proxy-driver  # (If a driver download is needed, will use: --proxy=PROXY.)
--multi-proxy  # (Allow multiple authenticated proxies when multi-threaded.)
--agent=STRING  # (Modify the web browser's User-Agent string.)
--mobile  # (Use the mobile device emulator while running tests.)
--metrics=STRING  # (Set mobile metrics: "CSSWidth,CSSHeight,PixelRatio".)
--chromium-arg="ARG=N,ARG2"  # (Set Chromium args, ","-separated, no spaces.)
--firefox-arg="ARG=N,ARG2"  # (Set Firefox args, comma-separated, no spaces.)
--firefox-pref=SET  # (Set a Firefox preference:value set, comma-separated.)
--extension-zip=ZIP  # (Load a Chrome Extension .zip|.crx, comma-separated.)
--extension-dir=DIR  # (Load a Chrome Extension directory, comma-separated.)
--binary-location=PATH  # (Set path of the Chromium browser binary to use.)
--sjw  # (Skip JS Waits for readyState to be "complete" or Angular to load.)
--pls=PLS  # (Set pageLoadStrategy on Chrome: "normal", "eager", or "none".)
--headless  # (Run tests in headless mode. The default arg on Linux OS.)
--headless2  # (Use the new headless mode, which supports extensions.)
--headed  # (Run tests in headed/GUI mode on Linux OS, where not default.)
--xvfb  # (Run tests using the Xvfb virtual display server on Linux OS.)
--locale=LOCALE_CODE  # (Set the Language Locale Code for the web browser.)
--interval=SECONDS  # (The autoplay interval for presentations & tour steps)
--start-page=URL  # (The starting URL for the web browser when tests begin.)
--archive-logs  # (Archive existing log files instead of deleting them.)
--archive-downloads  # (Archive old downloads instead of deleting them.)
--time-limit=SECONDS  # (Safely fail any test that exceeds the time limit.)
--slow  # (Slow down the automation. Faster than using Demo Mode.)
--demo  # (Slow down and visually see test actions as they occur.)
--demo-sleep=SECONDS  # (Set the wait time after Slow & Demo Mode actions.)
--highlights=NUM  # (Number of highlight animations for Demo Mode actions.)
--message-duration=SECONDS  # (The time length for Messenger alerts.)
--check-js  # (Check for JavaScript errors after page loads.)
--ad-block  # (Block some types of display ads from loading.)
--block-images  # (Block images from loading during tests.)
--do-not-track  # (Indicate to websites that you don't want to be tracked.)
--verify-delay=SECONDS  # (The delay before MasterQA verification checks.)
--recorder  # (Enables the Recorder for turning browser actions into code.)
--rec-behave  # (Same as Recorder Mode, but also generates behave-gherkin.)
--rec-sleep  # (If the Recorder is enabled, also records self.sleep calls.)
--rec-print  # (If the Recorder is enabled, prints output after tests end.)
--disable-js  # (Disable JavaScript on websites. Pages might break!)
--disable-csp  # (Disable the Content Security Policy of websites.)
--disable-ws  # (Disable Web Security on Chromium-based browsers.)
--enable-ws  # (Enable Web Security on Chromium-based browsers.)
--enable-sync  # (Enable "Chrome Sync" on websites.)
--uc | --undetected  # (Use undetected-chromedriver to evade bot-detection.)
--uc-cdp-events  # (Capture CDP events when running in "--undetected" mode.)
--remote-debug  # (Sync to Chrome Remote Debugger chrome://inspect/#devices)
--final-debug  # (Enter Debug Mode after each test ends. Don't use with CI!)
--dashboard  # (Enable the SeleniumBase Dashboard. Saved at: dashboard.html)
--dash-title=STRING  # (Set the title shown for the generated dashboard.)
--swiftshader  # (Use Chrome's "--use-gl=swiftshader" feature.)
--incognito  # (Enable Chrome's Incognito mode.)
--guest  # (Enable Chrome's Guest mode.)
--devtools  # (Open Chrome's DevTools when the browser opens.)
--reuse-session | --rs  # (Reuse browser session for all tests.)
--reuse-class-session | --rcs  # (Reuse session for tests in class.)
--crumbs  # (Delete all cookies between tests reusing a session.)
--disable-beforeunload  # (Disable the "beforeunload" event on Chrome.)
--window-size=WIDTH,HEIGHT  # (Set the browser's starting window size.)
--maximize  # (Start tests with the browser window maximized.)
--screenshot  # (Save a screenshot at the end of each test.)
--no-screenshot  # (No screenshots saved unless tests directly ask it.)
--visual-baseline  # (Set the visual baseline for Visual/Layout tests.)
--wire  # (Use selenium-wire's webdriver for replacing selenium webdriver.)
--external-pdf  # (Set Chromium "plugins.always_open_pdf_externally":True.)
--timeout-multiplier=MULTIPLIER  # (Multiplies the default timeout values.)
--list-fail-page  # (After each failing test, list the URL of the failure.)
```

(See the full list of command-line option definitions **[here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py)**. For detailed examples of command-line options, see **[customizing_test_runs.md](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md)**)

🔵 During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you add --archive_logs to command-line options, or have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), otherwise log files with be cleaned up at the start of the next test run. The ``test_suite.py`` collection contains tests that fail on purpose so that you can see how logging works.

```bash
cd examples/

pytest test_suite.py --browser=chrome

pytest test_suite.py --browser=firefox
```

An easy way to override seleniumbase/config/settings.py is by using a custom settings file.
Here's the command-line option to add to tests: (See [examples/custom_settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/custom_settings.py))
``--settings_file=custom_settings.py``
(Settings include default timeout values, a two-factor auth key, DB credentials, S3 credentials, and other important settings used by tests.)

🔵 To pass additional data from the command-line to tests, add ``--data="ANY STRING"``.
Inside your tests, you can use ``self.data`` to access that.


<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Test Directory Configuration:</h3>

🔵 When running tests with **pytest**, you'll want a copy of **[pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini)** in your root folders. When running tests with **nosetests**, you'll want a copy of **[setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg)** in your root folders. These files specify default configuration details for tests. Folders should also include a blank ``__init__.py`` file, which allows your tests to import files from that folder.

🔵 ``sbase mkdir DIR`` creates a folder with config files and sample tests:

```bash
sbase mkdir ui_tests
```

> That new folder will have these files:

```bash
ui_tests/
├── __init__.py
├── my_first_test.py
├── parameterized_test.py
├── pytest.ini
├── requirements.txt
├── setup.cfg
├── test_demo_site.py
└── boilerplates/
    ├── __init__.py
    ├── base_test_case.py
    ├── boilerplate_test.py
    ├── classic_obj_test.py
    ├── page_objects.py
    ├── sb_fixture_test.py
    └── samples/
        ├── __init__.py
        ├── google_objects.py
        ├── google_test.py
        ├── sb_swag_test.py
        └── swag_labs_test.py
```

<b>ProTip™:</b> You can also create a boilerplate folder without any sample tests in it by adding ``-b`` or ``--basic`` to the ``sbase mkdir`` command:

```bash
sbase mkdir ui_tests --basic
```

> That new folder will have these files:

```bash
ui_tests/
├── __init__.py
├── pytest.ini
├── requirements.txt
└── setup.cfg
```

Of those files, the ``pytest.ini`` config file is the most important, followed by a blank ``__init__.py`` file. There's also a ``setup.cfg`` file (only needed for nosetests). Finally, the ``requirements.txt`` file can be used to help you install seleniumbase into your environments (if it's not already installed).

--------

<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Log files from failed tests:</h3>

Let's try an example of a test that fails:

```python
""" test_fail.py """
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_find_army_of_robots_on_xkcd_desert_island(self):
        self.open("https://xkcd.com/731/")
        self.assert_element("div#ARMY_OF_ROBOTS", timeout=1)  # This should fail
```

You can run it from the ``examples/`` folder like this:

```bash
pytest test_fail.py
```

🔵 You'll notice that a logs folder, "latest_logs", was created to hold information about the failing test, and screenshots. During test runs, past results get moved to the archived_logs folder if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), or if your run tests with ``--archive-logs``. If you choose not to archive existing logs, they will be deleted and replaced by the logs of the latest test run.

--------

<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> The SeleniumBase Dashboard:</h3>

🔵 The ``--dashboard`` option for pytest generates a SeleniumBase Dashboard located at ``dashboard.html``, which updates automatically as tests run and produce results. Example:

```bash
pytest --dashboard --rs --headless
```

<img src="https://seleniumbase.github.io/cdn/img/dashboard_1.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="380" />

🔵 Additionally, you can host your own SeleniumBase Dashboard Server on a port of your choice. Here's an example of that using Python 3's ``http.server``:

```bash
python -m http.server 1948
```

🔵 Now you can navigate to ``http://localhost:1948/dashboard.html`` in order to view the dashboard as a web app. This requires two different terminal windows: one for running the server, and another for running the tests, which should be run from the same directory. (Use ``CTRL+C`` to stop the http server.)

🔵 Here's a full example of what the SeleniumBase Dashboard may look like:

```bash
pytest test_suite.py --dashboard --rs --headless
```

<img src="https://seleniumbase.github.io/cdn/img/dashboard_2.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="480" />

--------

<a id="creating_visual_reports"></a>
<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Generating Test Reports:</h3>

<h4><b>Pytest Reports:</b></h4>

🔵 Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```

<img src="https://seleniumbase.github.io/cdn/img/html_report.png" alt="Example Pytest Report" title="Example Pytest Report" width="520" />

🔵 When combining pytest html reports with SeleniumBase Dashboard usage, the pie chart from the Dashboard will get added to the html report. Additionally, if you set the html report URL to be the same as the Dashboard URL when also using the dashboard, (example: ``--dashboard --html=dashboard.html``), then the Dashboard will become an advanced html report when all the tests complete.

🔵 Here's an example of an upgraded html report:

```bash
pytest test_suite.py --dashboard --html=report.html
```

<img src="https://seleniumbase.github.io/cdn/img/dash_report.jpg" alt="Dashboard Pytest HTML Report" title="Dashboard Pytest HTML Report" width="520" />

If viewing pytest html reports in [Jenkins](https://www.jenkins.io/), you may need to [configure Jenkins settings](https://stackoverflow.com/a/46197356) for the html to render correctly. This is due to [Jenkins CSP changes](https://www.jenkins.io/doc/book/system-administration/security/configuring-content-security-policy/).

You can also use ``--junit-xml=report.xml`` to get an xml report instead. Jenkins can use this file to display better reporting for your tests.

```bash
pytest test_suite.py --junit-xml=report.xml
```

<h4><b>Nosetest Reports:</b></h4>

The ``--report`` option gives you a fancy report after your test suite completes.

```bash
nosetests test_suite.py --report
```

<img src="https://seleniumbase.github.io/cdn/img/nose_report.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(NOTE: You can add ``--show-report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show-report`` when running tests locally because it pauses the test run.)

<h4><b>Behave Dashboard & Reports:</b></h4>

(The [behave_bdd/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/behave_bdd) folder can be found in the [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder.)

```bash
behave behave_bdd/features/ -D dashboard -D headless
```

<img src="https://seleniumbase.github.io/cdn/img/sb_behave_dashboard.png" title="SeleniumBase" width="500">

You can also use ``--junit`` to get ``.xml`` reports for each Behave feature. Jenkins can use these files to display better reporting for your tests.

```bash
behave behave_bdd/features/ --junit -D rs -D headless
```

<h4><b>Allure Reports:</b></h4>

See: [https://docs.qameta.io/allure/](https://docs.qameta.io/allure/#_pytest)

SeleniumBase no longer includes ``allure-pytest`` as part of installed dependencies. If you want to use it, install it first:

```bash
pip install allure-pytest
```

Now your tests can create Allure results files, which can be processed by Allure Reports.

```bash
pytest test_suite.py --alluredir=allure_results
```


<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Using a Proxy Server:</h3>

If you wish to use a proxy server for your browser tests (Chromium or Firefox), you can add ``--proxy=IP_ADDRESS:PORT`` as an argument on the command line.

```bash
pytest proxy_test.py --proxy=IP_ADDRESS:PORT
```

If the proxy server that you wish to use requires authentication, you can do the following (Chromium only):

```bash
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT
```

SeleniumBase also supports SOCKS4 and SOCKS5 proxies:

```bash
pytest proxy_test.py --proxy="socks4://IP_ADDRESS:PORT"

pytest proxy_test.py --proxy="socks5://IP_ADDRESS:PORT"
```

To make things easier, you can add your frequently-used proxies to PROXY_LIST in [proxy_list.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/proxy_list.py), and then use ``--proxy=KEY_FROM_PROXY_LIST`` to use the IP_ADDRESS:PORT of that key.

```bash
pytest proxy_test.py --proxy=proxy1
```


<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Changing the User-Agent:</h3>

🔵 If you wish to change the User-Agent for your browser tests (Chromium and Firefox only), you can add ``--agent="USER AGENT STRING"`` as an argument on the command-line.

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```


<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Handling Pop-Up / Pop Up Alerts:</h3>

🔵 <code>self.accept_alert()</code> automatically waits for and accepts alert pop-ups. <code>self.dismiss_alert()</code> automatically waits for and dismisses alert pop-ups. On occasion, some methods like <code>self.click(SELECTOR)</code> might dismiss a pop-up on its own because they call JavaScript to make sure that the <code>readyState</code> of the page is <code>complete</code> before advancing. If you're trying to accept a pop-up that got dismissed this way, use this workaround: Call <code>self.find_element(SELECTOR).click()</code> instead, (which will let the pop-up remain on the screen), and then use <code>self.accept_alert()</code> to accept the pop-up (<a href="https://github.com/seleniumbase/SeleniumBase/issues/600#issuecomment-647270426">more on that here</a>). If pop-ups are intermittent, wrap code in a try/except block.


<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Building Guided Tours for Websites:</h3>

🔵 Learn about <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md">SeleniumBase Interactive Walkthroughs</a> (in the ``examples/tour_examples/`` folder). It's great for prototyping a website onboarding experience.


<a id="utilizing_advanced_features"></a>

--------

<div></div>
<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Production Environments & Integrations:</h3>

<div></div>
<details>
<summary> ▶️ Here are some things you can do to set up a production environment for your testing. (<b>click to expand</b>)</summary>

<ul>
<li>You can set up a <a href="https://jenkins.io/" target="_blank">Jenkins</a> build server for running tests at regular intervals. For a real-world Jenkins example of headless browser automation in action, check out the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/jenkins/ReadMe.md">SeleniumBase Jenkins example on Azure</a> or the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/google_cloud/ReadMe.md">SeleniumBase Jenkins example on Google Cloud</a>.</li>

<li>You can use <a href="https://selenium.dev/documentation/en/grid/" target="_blank">the Selenium Grid</a> to scale your testing by distributing tests on several machines with parallel execution. To do this, check out the <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid">SeleniumBase selenium_grid folder</a>, which should have everything you need, including the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md">Selenium Grid ReadMe</a>, which will help you get started.</li>

<li>If you're using the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/mysql_installation.md">SeleniumBase MySQL feature</a> to save results from tests running on a server machine, you can install <a href="https://dev.mysql.com/downloads/tools/workbench/">MySQL Workbench</a> to help you read & write from your DB more easily.</li>

<li>If you're using AWS, you can set up an <a href="https://aws.amazon.com/s3/" target="_blank">Amazon S3</a> account for saving log files and screenshots from your tests. To activate this feature, modify <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py">settings.py</a> with connection details in the S3 section, and add <code>--with-s3-logging</code> on the command-line when running your tests.</li>
</ul>

Here's an example of running tests with some additional features enabled:

```bash
pytest [YOUR_TEST_FILE.py] --with-db-reporting --with-s3-logging
```

</details>


<a id="detailed_method_specifications"></a>
<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Detailed Method Specifications and Examples:</h3>

🔵 Navigating to a web page: (and related commands)

```python
self.open("https://xkcd.com/378/")  # This method opens the specified page.

self.go_back()  # This method navigates the browser to the previous page.

self.go_forward()  # This method navigates the browser forward in history.

self.refresh_page()  # This method reloads the current page.

self.get_current_url()  # This method returns the current page URL.

self.get_page_source()  # This method returns the current page source.
```

<b>ProTip™:</b> You can use the <code>self.get_page_source()</code> method with Python's <code>find()</code> command to parse through HTML to find something specific. (For more advanced parsing, see the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_parse_soup.py">BeautifulSoup example</a>.)

```python
source = self.get_page_source()
head_open_tag = source.find('<head>')
head_close_tag = source.find('</head>', head_open_tag)
everything_inside_head = source[head_open_tag+len('<head>'):head_close_tag]
```

🔵 Clicking:

To click an element on the page:

```python
self.click("div#my_id")
```

**ProTip™:** In most web browsers, you can right-click on a page and select ``Inspect Element`` to see the CSS selector details that you'll need to create your own scripts.

🔵 Typing Text:

<code>self.type(selector, text)</code>  # updates the text from the specified element with the specified value. An exception is raised if the element is missing or if the text field is not editable. Example:

```python
self.type("input#id_value", "2012")
```

You can also use <code>self.add_text()</code> or the <a href="https://www.selenium.dev/documentation/webdriver/" target="_blank">WebDriver</a> <code>.send_keys()</code> command, but those won't clear the text box first if there's already text inside.

🔵 Getting the text from an element on a page:

```python
text = self.get_text("header h2")
```

🔵 Getting the attribute value from an element on a page:

```python
attribute = self.get_attribute("#comic img", "title")
```

🔵 Asserting existence of an element on a page within some number of seconds:

```python
self.wait_for_element_present("div.my_class", timeout=10)
```

(NOTE: You can also use: ``self.assert_element_present(ELEMENT)``)

🔵 Asserting visibility of an element on a page within some number of seconds:

```python
self.wait_for_element_visible("a.my_class", timeout=5)
```

(NOTE: The short versions of that are ``self.find_element(ELEMENT)`` and ``self.assert_element(ELEMENT)``. The ``find_element()`` version returns the element.)

Since the line above returns the element, you can combine that with ``.click()`` as shown below:

```python
self.find_element("a.my_class", timeout=5).click()

# But you're better off using the following statement, which does the same thing:

self.click("a.my_class")  # DO IT THIS WAY!
```

**ProTip™:** You can use dots to signify class names (Ex: ``div.class_name``) as a simplified version of ``div[class="class_name"]`` within a CSS selector. 

You can also use ``*=`` to search for any partial value in a CSS selector as shown below:

```python
self.click('a[name*="partial_name"]')
```

🔵 Asserting visibility of text inside an element on a page within some number of seconds:

```python
self.assert_text("Make it so!", "div#trek div.picard div.quotes")
self.assert_text("Tea. Earl Grey. Hot.", "div#trek div.picard div.quotes", timeout=3)
```

(NOTE: ``self.find_text(TEXT, ELEMENT)`` and ``self.wait_for_text(TEXT, ELEMENT)`` also do this. For backwards compatibility, older method names were kept, but the default timeout may be different.)

🔵 Asserting Anything:

```python
self.assert_true(var1 == var2)

self.assert_false(var1 == var2)

self.assert_equal(var1, var2)
```

🔵 Useful Conditional Statements: (with creative examples)

❓ ``is_element_visible(selector):``  (visible on the page)

```python
if self.is_element_visible('div#warning'):
    print("Red Alert: Something bad might be happening!")
```

❓ ``is_element_present(selector):``  (present in the HTML)

```python
if self.is_element_present('div#top_secret img.tracking_cookie'):
    self.contact_cookie_monster()  # Not a real SeleniumBase method
else:
    current_url = self.get_current_url()
    self.contact_the_nsa(url=current_url, message="Dark Zone Found")  # Not a real SeleniumBase method
```

```python
def is_there_a_cloaked_klingon_ship_on_this_page():
    if self.is_element_present("div.ships div.klingon"):
        return not self.is_element_visible("div.ships div.klingon")
    return False
```

❓ ``is_text_visible(text, selector):``  (text visible on element)

```python
if self.is_text_visible("You Shall Not Pass!", "h1"):
    self.open("https://www.youtube.com/watch?v=3xYXUeSmb-Y")
```

<div></div>
<details>
<summary> ▶️ Click for a longer example of <code>is_text_visible():</code></summary>

```python
def get_mirror_universe_captain_picard_superbowl_ad(superbowl_year):
    selector = "div.superbowl_%s div.commercials div.transcript div.picard" % superbowl_year
    if self.is_text_visible("Yes, it was I who summoned you all here.", selector):
        return "Picard Paramount+ Superbowl Ad 2020"
    elif self.is_text_visible("Commander, signal the following: Our Network is Secure!"):
        return "Picard Mirror Universe iboss Superbowl Ad 2018"
    elif self.is_text_visible("For the Love of Marketing and Earl Grey Tea!", selector):
        return "Picard Mirror Universe HubSpot Superbowl Ad 2015"
    elif self.is_text_visible("Delivery Drones... Engage", selector):
        return "Picard Mirror Universe Amazon Superbowl Ad 2015"
    elif self.is_text_visible("Bing it on Screen!", selector):
        return "Picard Mirror Universe Microsoft Superbowl Ad 2015"
    elif self.is_text_visible("OK Glass, Make it So!", selector):
        return "Picard Mirror Universe Google Superbowl Ad 2015"
    elif self.is_text_visible("Number One, I've Never Seen Anything Like It.", selector):
        return "Picard Mirror Universe Tesla Superbowl Ad 2015"
    elif self.is_text_visible("Let us make sure history never forgets the name ... Facebook", selector):
        return "Picard Mirror Universe Facebook Superbowl Ad 2015"
    elif self.is_text_visible("""With the first link, the chain is forged.
                              The first speech censored, the first thought forbidden,
                              the first freedom denied, chains us all irrevocably.""", selector):
        return "Picard Mirror Universe Wikimedia Superbowl Ad 2015"
    else:
        raise Exception("Reports of my assimilation are greatly exaggerated.")
```

</details>

❓ ``is_link_text_visible(link_text):``

```python
if self.is_link_text_visible("Stop! Hammer time!"):
    self.click_link("Stop! Hammer time!")
```

🔵 Switching Tabs:

<p>If your test opens up a new tab/window, you can switch to it. (SeleniumBase automatically switches to new tabs that don't open to <code>about:blank</code> URLs.)</p>

```python
self.switch_to_window(1)  # This switches to the new tab (0 is the first one)
```

🔵 <b>ProTip™:</b> iframes follow the same principle as new windows - you need to specify the iframe if you want to take action on something in there

```python
self.switch_to_frame('ContentManagerTextBody_ifr')
# Now you can act inside the iframe
# .... Do something cool (here)
self.switch_to_default_content()  # Exit the iframe when you're done
```

🔵 Executing Custom jQuery Scripts:

<p>jQuery is a powerful JavaScript library that allows you to perform advanced actions in a web browser.
If the web page you're on already has jQuery loaded, you can start executing jQuery scripts immediately.
You'd know this because the web page would contain something like the following in the HTML:</p>

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
```

🔵 It's OK if you want to use jQuery on a page that doesn't have it loaded yet. To do so, run the following command first:

```python
self.activate_jquery()
```

<div></div>
<details>
<summary> ▶️ Here are some examples of using jQuery in your scripts. (<b>click to expand</b>)</summary>

```python
self.execute_script("jQuery, window.scrollTo(0, 600)")  # Scrolling the page

self.execute_script("jQuery('#annoying-widget').hide()")  # Hiding elements on a page

self.execute_script("jQuery('#hidden-widget').show(0)")  # Showing hidden elements on a page

self.execute_script("jQuery('#annoying-button a').remove()")  # Removing elements on a page

self.execute_script("jQuery('%s').mouseover()" % (mouse_over_item))  # Mouse-over elements on a page

self.execute_script("jQuery('input#the_id').val('my_text')")  # Fast text input on a page

self.execute_script("jQuery('div#dropdown a.link').click()")  # Click elements on a page

self.execute_script("return jQuery('div#amazing')[0].text")  # Returns the css "text" of the element given

self.execute_script("return jQuery('textarea')[2].value")  # Returns the css "value" of the 3rd textarea element on the page
```

(Most of the above commands can be done directly with built-in SeleniumBase methods.)

</details>

🔵 Some websites have a restrictive [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) to prevent users from loading jQuery and other external libraries onto their websites. If you need to use jQuery or another JS library on such a website, add ``--disable-csp`` on the command-line.

<div></div>
<details>
<summary> ▶️ In this example, JavaScript creates a referral button on a page, which is then clicked. (<b>click to expand</b>)</summary>

```python
start_page = "https://xkcd.com/465/"
destination_page = "https://github.com/seleniumbase/SeleniumBase"
self.open(start_page)
referral_link = '''<a class='analytics test' href='%s'>Free-Referral Button!</a>''' % destination_page
self.execute_script('''document.body.innerHTML = \"%s\"''' % referral_link)
self.click("a.analytics")  # Clicks the generated button
```

(Due to popular demand, this traffic generation example has been included in SeleniumBase with the <code>self.generate_referral(start_page, end_page)</code> and the <code>self.generate_traffic(start_page, end_page, loops)</code> methods.)

</details>

🔵 Using deferred asserts:

<p>Let's say you want to verify multiple different elements on a web page in a single test, but you don't want the test to fail until you verified several elements at once so that you don't have to rerun the test to find more missing elements on the same page. That's where deferred asserts come in. Here's the example:</p>

```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_deferred_asserts(self):
        self.open('https://xkcd.com/993/')
        self.wait_for_element('#comic')
        self.deferred_assert_element('img[alt="Brand Identity"]')
        self.deferred_assert_element('img[alt="Rocket Ship"]')  # Will Fail
        self.deferred_assert_element('#comicmap')
        self.deferred_assert_text('Fake Item', '#middleContainer')  # Will Fail
        self.deferred_assert_text('Random', '#middleContainer')
        self.deferred_assert_element('a[name="Super Fake !!!"]')  # Will Fail
        self.process_deferred_asserts()
```

<code>deferred_assert_element()</code> and <code>deferred_assert_text()</code> will save any exceptions that would be raised.
To flush out all the failed deferred asserts into a single exception, make sure to call <code>self.process_deferred_asserts()</code> at the end of your test method. If your test hits multiple pages, you can call <code>self.process_deferred_asserts()</code> before navigating to a new page so that the screenshot from your log files matches the URL where the deferred asserts were made.

🔵 Accessing Raw <a href="https://www.selenium.dev/documentation/webdriver/" target="_blank">WebDriver</a>:

<p>If you need access to any commands that come with standard <a href="https://www.selenium.dev/documentation/webdriver/" target="_blank">WebDriver</a>, you can call them directly like this:</p>

```python
self.driver.delete_all_cookies()
capabilities = self.driver.capabilities
self.driver.find_elements("partial link text", "GitHub")
```

(In general, you'll want to use the SeleniumBase versions of methods when available.)

🔵 Retrying failing tests automatically:

<p>You can use <code>--reruns=NUM</code> to retry failing tests that many times. Use <code>--reruns-delay=SECONDS</code> to wait that many seconds between retries. Example:</p>

```bash
pytest --reruns=1 --reruns-delay=1
```

<p>You can use the <code>@retry_on_exception()</code> decorator to retry failing methods. (First import: <code>from seleniumbase import decorators</code>). To learn more about SeleniumBase decorators, <a href="https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/common">click here</a>.</p>


<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Wrap-Up</h3>

<b>Congratulations on getting started with SeleniumBase!</b>

<p>
<div><b>If you see something, say something!</b></div>
<div><a href="https://github.com/seleniumbase/SeleniumBase/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/seleniumbase/SeleniumBase.svg?color=22BB88" title="Closed Issues" /></a>   <a href="https://github.com/seleniumbase/SeleniumBase/pulls?q=is%3Apr+is%3Aclosed"><img src="https://img.shields.io/github/issues-pr-closed/seleniumbase/SeleniumBase.svg?logo=github&logoColor=white&color=22BB99" title="Closed Pull Requests" /></a></div>
</p>

<p>
<div><b>If you like SeleniumBase, star us! ⭐</b></div>
<div><a href="https://github.com/seleniumbase/SeleniumBase/stargazers"><img src="https://img.shields.io/github/stars/seleniumbase/seleniumbase.svg?color=19A57B" title="Stargazers" /></a></div>
</p>
<p><div><a href="https://github.com/mdmintz">https://github.com/mdmintz</a></div></p>

<div><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="220" /></a></div> <div><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" title="SeleniumBase" /></a> <a href="https://gitter.im/seleniumbase/SeleniumBase" target="_blank"><img src="https://img.shields.io/gitter/room/seleniumbase/SeleniumBase.svg" alt="Gitter chat"/></a></div> <div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://img.shields.io/badge/tested%20with-SeleniumBase-04C38E.svg" alt="Tested with SeleniumBase" /></a></div> <div><a href="https://seleniumbase.io"><img src="https://img.shields.io/badge/docs-seleniumbase.io-11BBAA.svg" alt="SeleniumBase Docs" /></a></div>
<p><a href="https://pepy.tech/project/seleniumbase" target="_blank"><img src="https://pepy.tech/badge/seleniumbase" alt="SeleniumBase PyPI downloads" /></a></p>

<p><div>
<span><a href="https://www.youtube.com/playlist?list=PLp9uKicxkBc5UIlGi2BuE3aWC7JyXpD3m"><img src="https://seleniumbase.github.io/cdn/img/youtube.png" title="SeleniumBase Playlist on YouTube" alt="SeleniumBase Playlist on YouTube" width="54" /></a></span>
<span><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/img/social/share_github.svg" title="SeleniumBase on GitHub" alt="SeleniumBase on GitHub" width="50" /></a></span>
<span><a href="https://gitter.im/seleniumbase/SeleniumBase" target="_blank"><img src="https://seleniumbase.github.io/img/social/share_gitter.svg" title="SeleniumBase on Gitter" alt="SeleniumBase on Gitter" width="38" /></a></span>
</div></p>

--------

<p><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/cdn/img/sb_logo_b.png" alt="SeleniumBase" title="SeleniumBase" width="300" /></a></p>
<p><a href="https://www.python.org/downloads/" target="_blank"><img src="https://img.shields.io/pypi/pyversions/seleniumbase.svg?color=22AAEE&logo=python&logoColor=FEDC54" title="Supported Python Versions" /></a></p>
