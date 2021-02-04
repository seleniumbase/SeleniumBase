<meta property="og:site_name" content="SeleniumBase">
<meta property="og:title" content="SeleniumBase: Python Web Automation and E2E Testing" />
<meta property="og:description" content="Build fast, reliable, end-to-end tests." />
<meta property="og:keywords" content="Python, pytest, selenium, webdriver, test automation, testing, seleniumbase, test framework, RPA, reports, website tours, presentations">
<meta property="og:image" content="https://seleniumbase.io/cdn/img/mac_sb_logo_5.png" />
<link rel="icon" href="https://seleniumbase.io/img/logo6.png" />

<p align="center"><a href="https://github.com/seleniumbase/SeleniumBase/">
<img src="https://seleniumbase.io/img/sb_logo_10.png" alt="SeleniumBase" title="SeleniumBase" width="280" /></a></p>
<p align="center">
<b>Build fast, reliable, end-to-end tests.</b>
</p>

<!-- View on GitHub -->
<p align="center"><a href="https://github.com/seleniumbase/SeleniumBase/releases">
<img src="https://img.shields.io/github/v/release/seleniumbase/SeleniumBase.svg?color=2277EE" alt="Latest Release on GitHub" /></a> <a href="https://pypi.python.org/pypi/seleniumbase">
<img src="https://img.shields.io/pypi/v/seleniumbase.svg?color=22AAEE" alt="Latest Release on PyPI" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/actions">
<img src="https://github.com/seleniumbase/SeleniumBase/workflows/CI%20build/badge.svg" alt="SeleniumBase GitHub Actions" /></a> <a href="https://dev.azure.com/seleniumbase/seleniumbase/_build/latest?definitionId=1&branchName=master"> <img src="https://dev.azure.com/seleniumbase/seleniumbase/_apis/build/status/seleniumbase.SeleniumBase?branchName=master" alt="SeleniumBase Azure Pipelines" /></a> <a href="https://gitter.im/seleniumbase/SeleniumBase">
<img src="https://badges.gitter.im/seleniumbase/SeleniumBase.svg" alt="SeleniumBase" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/stargazers"><img src="https://img.shields.io/github/stars/seleniumbase/seleniumbase.svg?color=19A57B" title="Stargazers" /></a> <a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20seleniumbase.io-22BBAA.svg" alt="SeleniumBase.io Docs" /></a></p>

<p>
SeleniumBase is a Python framework for web automation, end-to-end testing, and more.
Tests are run with "pytest". Browsers are controlled by WebDriver.
</p>

<p align="center">
<a href="#python_installation">🚀 Start</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/features_list.md">🗂️ Features</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md">🖥️ CLI</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/ReadMe.md">👨‍🏫 Examples</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/tree/master/examples/boilerplates">♻️ Boilerplates</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/locale_codes.md">🗾 Locales</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/js_package_manager.md">🗄️ PkgManager</a>
<br />
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md">📗 API</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md">📊 Reports</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/console_scripts/ReadMe.md">💻 Scripts</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/mobile_testing.md">📱 Mobile</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md">🔡 Syntax Formats</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md">🌐 Grid Hub</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_ide/ReadMe.md">⏺️ Recorder</a>
<br />
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/github/workflows/ReadMe.md">🤖 CI</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/translations.md">🌏 Translate</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md">🗺️ Tours</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/visual_testing/ReadMe.md">🖼️ VisualTest</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/presenter/ReadMe.md">📑 Presenter</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/chart_maker/ReadMe.md">📈 ChartMaker</a> |
<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/master_qa/ReadMe.md">🛂 MasterQA</a>
</p>

✅ Has a [complete API](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md) for Web-UI testing.<br />
✅ Expands pytest [command-line options](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md).<br />
✅ Includes [scripts](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/console_scripts/ReadMe.md) for driver management.<br />
✅ Includes tools for [dashboards & reports](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md).<br />

--------

<p align="center">(Example: <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_swag_labs.py">test_swag_labs.py</a> in Demo Mode.)</p>

```bash
pytest test_swag_labs.py --demo
```

<p align="center"><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_swag_labs.py"><img src="https://seleniumbase.io/cdn/gif/swag_demo_2.gif" alt="SeleniumBase Demo Mode" title="SeleniumBase Demo Mode" /></a></p>

<a id="python_installation"></a>
<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Python Setup:</h2>

🔵 Add **[Python](https://www.python.org/downloads/)** and **[Git](https://git-scm.com/)** to your System PATH.

🔵 Create a **[Python virtual environment](https://seleniumbase.io/help_docs/virtualenv_instructions/)**.

<a id="install_seleniumbase"></a>
<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Install SeleniumBase:</h2>

🔵 You can install ``seleniumbase`` from [GitHub](https://github.com/seleniumbase/SeleniumBase):

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install .  # Normal installation
pip install -e .  # Editable install
```

> (When using a virtual env, the Editable install is faster.)

🔵 You can also install ``seleniumbase`` from [pypi](https://pypi.python.org/pypi/seleniumbase):

```bash
pip install seleniumbase
```

> (Add ``--upgrade`` OR ``-U`` to upgrade an installation.)
> (Add ``--force-reinstall`` to upgrade dependencies.)
> (Use ``pip3`` if multiple versions of Python are installed.)

🔵 Type ``seleniumbase`` or ``sbase`` to verify that SeleniumBase was installed successfully:

```bash
   ______     __           _                 ____                
  / ____/__  / /__  ____  (_)_  ______ ___  / _  \____  ________ 
  \__ \/ _ \/ / _ \/ __ \/ / / / / __ `__ \/ /_) / __ \/ ___/ _ \
 ___/ /  __/ /  __/ / / / / /_/ / / / / / / /_) / (_/ /__  /  __/
/____/\___/_/\___/_/ /_/_/\__,_/_/ /_/ /_/_____/\__,_/____/\___/ 
-----------------------------------------------------------------

 * USAGE: "seleniumbase [COMMAND] [PARAMETERS]"
 *    OR:        "sbase [COMMAND] [PARAMETERS]"

COMMANDS:
      install         [DRIVER] [OPTIONS]
      methods         (List common Python methods)
      options         (List common pytest options)
      mkdir           [DIRECTORY] [OPTIONS]
      mkfile          [FILE.py] [OPTIONS]
      mkpres          [FILE.py] [LANG]
      print           [FILE] [OPTIONS]
      translate       [SB_FILE.py] [LANG] [ACTION]
      convert         [WEBDRIVER_UNITTEST_FILE.py]
      extract-objects [SB_FILE.py]
      inject-objects  [SB_FILE.py] [OPTIONS]
      objectify       [SB_FILE.py] [OPTIONS]
      revert-objects  [SB_FILE.py] [OPTIONS]
      encrypt         (OR: obfuscate)
      decrypt         (OR: unobfuscate)
      download server (The Selenium Grid JAR file)
      grid-hub        [start|stop] [OPTIONS]
      grid-node       [start|stop] --hub=[HOST/IP]
 * (EXAMPLE: "sbase install chromedriver latest")  *

    Type "sbase help [COMMAND]" for specific command info.
    For info on all commands, type: "seleniumbase --help".
 * (Use "pytest" for running tests) *
```

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Download a webdriver:</h3>

✅ SeleniumBase can download webdrivers to the [seleniumbase/drivers](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/drivers) folder with the ``install`` command:

```bash
sbase install chromedriver
```

* You need a different webdriver for each browser to automate: ``chromedriver`` for Chrome, ``edgedriver`` for Edge, ``geckodriver`` for Firefox, and ``operadriver`` for Opera.
* If you have the latest version of Chrome installed, get the latest chromedriver (<i>otherwise it defaults to chromedriver 2.44 for compatibility reasons</i>):

```bash
sbase install chromedriver latest
```

* If you run a test without the correct webdriver installed, the driver will be downloaded automatically.

(See [seleniumbase.io/seleniumbase/console_scripts/ReadMe/](https://seleniumbase.io/seleniumbase/console_scripts/ReadMe/) for more information on SeleniumBase console scripts.)

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Running tests:</h3>

🔵 <b>If you've cloned SeleniumBase from GitHub, you can run sample tests from the [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder:</b>

```bash
cd examples/
pytest test_demo_site.py
```

> (Chrome is the default browser if not specified with ``--browser=BROWSER``. On Linux, ``--headless`` is the default behavior. You can also run in headless mode on any OS. If your Linux machine has a GUI and you want to see the web browser as tests run, add ``--headed`` or ``--gui``.)

<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_demo_site.py"><img src="https://seleniumbase.io/cdn/gif/demo_page_1.gif" title="SeleniumBase Demo Page" /></a><br />

🔵 <b>Here are more examples that you can run:</b>

```bash
pytest my_first_test.py

pytest test_swag_labs.py
```

🔵 <b>Run [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) in Demo Mode:</b>

```bash
pytest my_first_test.py --demo
```

<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py"><img src="https://seleniumbase.io/cdn/gif/my_first_test_1.gif" title="SeleniumBase" /></a>

<b>Here's the code for [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py):</b>

```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_basics(self):
        url = "https://store.xkcd.com/collections/posters"
        self.open(url)
        self.type('input[name="q"]', "xkcd book")
        self.click('input[value="Search"]')
        self.assert_text("xkcd: volume 0", "h3")
        self.open("https://xkcd.com/353/")
        self.assert_title("xkcd: Python")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy and reuse")
        self.go_back()
        self.click_link("About")
        self.assert_exact_text("xkcd.com", "h2")
```

* By default, **[CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp)** are used for finding page elements.
* If you're new to CSS Selectors, games like [Flukeout](http://flukeout.github.io/) can help you learn.
* Here are some common ``SeleniumBase`` methods you might find in tests:

```python
self.open(URL)  # Navigate to the web page
self.click(SELECTOR)  # Click a page element
self.type(SELECTOR, TEXT)  # Type text (Add "\n" to text for pressing enter/return.)
self.assert_element(SELECTOR)  # Assert element is visible
self.assert_text(TEXT)  # Assert text is visible (has optional SELECTOR arg)
self.assert_title(PAGE_TITLE)  # Assert page title
self.assert_no_404_errors()  # Assert no 404 errors from files on the page
self.assert_no_js_errors()  # Assert no JavaScript errors on the page (Chrome-ONLY)
self.execute_script(JAVASCRIPT)  # Execute JavaScript code
self.go_back()  # Navigate to the previous URL
self.get_text(SELECTOR)  # Get text from a selector
self.get_attribute(SELECTOR, ATTRIBUTE)  # Get a specific attribute from a selector
self.is_element_visible(SELECTOR)  # Determine if an element is visible on the page
self.is_text_visible(TEXT)  # Determine if text is visible on the page (optional SELECTOR)
self.hover_and_click(HOVER_SELECTOR, CLICK_SELECTOR)  # Mouseover element & click another
self.select_option_by_text(DROPDOWN_SELECTOR, OPTION_TEXT)  # Select a dropdown option
self.switch_to_frame(FRAME_NAME)  # Switch webdriver control to an iframe on the page
self.switch_to_default_content()  # Switch webdriver control out of the current iframe
self.switch_to_window(WINDOW_NUMBER)  # Switch to a different window/tab
self.save_screenshot(FILE_NAME)  # Save a screenshot of the current page
```

🔵 For the complete list of SeleniumBase methods, see: <b><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md">Method Summary</a></b>

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Learn More:</h2>

✅ Automatic WebDriver Abilities:
<p>SeleniumBase automatically handles common WebDriver actions such as spinning up web browsers and saving screenshots during test failures. (<i><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md">Read more about customizing test runs</a>.</i>)</p>

✅ Simplified Code:
<p>SeleniumBase uses simple syntax for commands. Example:</p>

```python
self.type("input", "dogs\n")
```

SeleniumBase tests can be run with both ``pytest`` and ``nosetests``, but using ``pytest`` is recommended. (``chrome`` is the default browser if not specified.)

```bash
pytest my_first_test.py --browser=chrome

nosetests test_suite.py --browser=firefox
```

✅ Automatic Test Discovery:
<p>All Python methods that start with <code>test_</code> will automatically be run when using <code>pytest</code> or <code>nosetests</code> on a Python file, (<i>or on folders containing Python files</i>). You can also be more specific on what to run within a file by using the following: (<i>Note that the syntax is different for pytest vs nosetests.</i>)</p>

```bash
pytest [FILE_NAME.py]::[CLASS_NAME]::[METHOD_NAME]

nosetests [FILE_NAME.py]:[CLASS_NAME].[METHOD_NAME]
```

✅ No More Flaky Tests:
<p>SeleniumBase methods automatically wait for page elements to finish loading before interacting with them (<i>up to a timeout limit</i>). This means you <b>no longer need</b> random <span><b>time.sleep()</b></span> statements in your scripts.</p>
<img src="https://img.shields.io/badge/Flaky Tests%3F-%20NO%21-11BBDD.svg" alt="NO MORE FLAKY TESTS!" />

✅ Automated/Manual Hybrid Mode:</h4>
<p>SeleniumBase includes a solution called <b><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/masterqa/ReadMe.md">MasterQA</a></b>, which speeds up manual testing by having automation perform all the browser actions while the manual tester handles validation.</p>

✅ Feature-Rich:
<p>For a full list of SeleniumBase features, <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/features_list.md">Click Here</a>.</p>


<a id="detailed_instructions"></a>
<img src="https://seleniumbase.io/cdn/img/mac_sb_logo_5.png" title="SeleniumBase" width="300">

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Detailed Instructions:</h2>

<a id="seleniumbase_demo_mode"></a> <b>Use Demo Mode to help you see what tests are asserting.</b>

🔵 If the example test is moving too fast for your eyes, you can run it in **Demo Mode** by adding ``--demo`` on the command-line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real time:

```bash
pytest my_first_test.py --demo
```

🔵 ``Pytest`` includes test discovery. If you don't specify a specific file or folder to run from, ``pytest`` will search all subdirectories automatically for tests to run based on the following matching criteria:
Python filenames that start with ``test_`` or end with ``_test.py``.
Python methods that start with ``test_``.
The Python class name can be anything since SeleniumBase's ``BaseCase`` class inherits from the ``unittest.TestCase`` class.
You can see which tests are getting discovered by ``pytest`` by using:

```bash
pytest --collect-only -q
```

🔵 You can use the following calls in your scripts to help you debug issues:

```python
import time; time.sleep(5)  # Makes the test wait and do nothing for 5 seconds.
import ipdb; ipdb.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
import pytest; pytest.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
```

🔵 To pause an active test that throws an exception or error, add ``--pdb``:

```bash
pytest my_first_test.py --pdb
```

The code above will leave your browser window open in case there's a failure. (ipdb commands: 'n', 'c', 's' => next, continue, step).

🔵 Here are some useful command-line options that come with ``pytest``:

```bash
-v  # Verbose mode. Prints the full name of each test run.
-q  # Quiet mode. Print fewer details in the console output when running tests.
-x  # Stop running the tests after the first failure is reached.
--html=report.html  # Creates a detailed pytest-html report after tests finish.
--collect-only | --co  # Show what tests would get run. (Without running them)
-n=NUM  # Multithread the tests using that many threads. (Speed up test runs!)
-s  # See print statements. (Should be on by default with pytest.ini present.)
--junit-xml=report.xml  # Creates a junit-xml report after tests finish.
--pdb  # If a test fails, pause run and enter debug mode. (Don't use with CI!)
-m=MARKER  # Run tests with the specified pytest marker.
```

🔵 SeleniumBase provides additional ``pytest`` command-line options for tests:

```bash
--browser=BROWSER  # (The web browser to use. Default: "chrome".)
--chrome  # (Shortcut for "--browser=chrome". On by default.)
--edge  # (Shortcut for "--browser=edge".)
--firefox  # (Shortcut for "--browser=firefox".)
--opera  # (Shortcut for "--browser=opera".)
--safari  # (Shortcut for "--browser=safari".)
--cap-file=FILE  # (The web browser's desired capabilities to use.)
--cap-string=STRING  # (The web browser's desired capabilities to use.)
--settings-file=FILE  # (Override default SeleniumBase settings.)
--env=ENV  # (Set a test environment. Use "self.env" to use this in tests.)
--data=DATA  # (Extra test data. Access with "self.data" in tests.)
--var1=DATA  # (Extra test data. Access with "self.var1" in tests.)
--var2=DATA  # (Extra test data. Access with "self.var2" in tests.)
--var3=DATA  # (Extra test data. Access with "self.var3" in tests.)
--user-data-dir=DIR  # (Set the Chrome user data directory to use.)
--server=SERVER  # (The Selenium Grid server/IP used for tests.)
--port=PORT  # (The Selenium Grid port used by the test server.)
--proxy=SERVER:PORT  # (Connect to a proxy server:port for tests.)
--proxy=USERNAME:PASSWORD@SERVER:PORT  # (Use authenticated proxy server.)
--agent=STRING  # (Modify the web browser's User-Agent string.)
--mobile  # (Use the mobile device emulator while running tests.)
--metrics=STRING  # (Set mobile metrics: "CSSWidth,CSSHeight,PixelRatio".)
--extension-zip=ZIP  # (Load a Chrome Extension .zip|.crx, comma-separated.)
--extension-dir=DIR  # (Load a Chrome Extension directory, comma-separated.)
--headless  # (Run tests headlessly. Default mode on Linux OS.)
--headed  # (Run tests with a GUI on Linux OS.)
--locale=LOCALE_CODE  # (Set the Language Locale Code for the web browser.)
--start-page=URL  # (The starting URL for the web browser when tests begin.)
--archive-logs  # (Archive old log files instead of deleting them.)
--time-limit=SECONDS  # (Safely fail any test that exceeds the time limit.)
--slow  # (Slow down the automation. Faster than using Demo Mode.)
--demo  # (Slow down and visually see test actions as they occur.)
--demo-sleep=SECONDS  # (Set the wait time after Demo Mode actions.)
--highlights=NUM  # (Number of highlight animations for Demo Mode actions.)
--message-duration=SECONDS  # (The time length for Messenger alerts.)
--check-js  # (Check for JavaScript errors after page loads.)
--ad-block  # (Block some types of display ads after page loads.)
--block-images  # (Block images from loading during tests.)
--verify-delay=SECONDS  # (The delay before MasterQA verification checks.)
--disable-csp  # (Disable the Content Security Policy of websites.)
--disable-ws  # (Disable Web Security on Chromium-based browsers.)
--enable-ws  # (Enable Web Security on Chromium-based browsers.)
--enable-sync  # (Enable "Chrome Sync".)
--use-auto-ext  # (Use Chrome's automation extension.)
--remote-debug  # (Enable Chrome's Remote Debugger on http://localhost:9222)
--dashboard  # (Enable the SeleniumBase Dashboard. Saved at: dashboard.html)
--swiftshader  # (Use Chrome's "--use-gl=swiftshader" feature.)
--incognito  #  (Enable Chrome's Incognito mode.)
--guest  # (Enable Chrome's Guest mode.)
--devtools  # (Open Chrome's DevTools when the browser opens.)
--reuse-session  # (Reuse the browser session between tests.)
--crumbs  # (Delete all cookies between tests reusing a session.)
--maximize-window  # (Start tests with the web browser window maximized.)
--save-screenshot  # (Save a screenshot at the end of each test.)
--visual-baseline  # (Set the visual baseline for Visual/Layout tests.)
--timeout-multiplier=MULTIPLIER  # (Multiplies the default timeout values.)
```

(For more details, see the full list of command-line options **[here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py)**.)

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


<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Test Directory Configuration:</h3>

🔵 When running tests with **pytest**, you'll want a copy of **[pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini)** in your root folders. When running tests with **nosetests**, you'll want a copy of **[setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg)** in your root folders. These files specify default configuration details for tests. Folders should also include a blank ``__init__.py`` file, which allows your tests to import files from that folder.

🔵 ``sbase mkdir DIR`` creates a folder with config files and sample tests:

```bash
sbase mkdir ui_tests
```

> That new folder will have these files:

```bash
ui_tests/
├── __init__.py
├── boilerplates/
│   ├── __init__.py
│   ├── base_test_case.py
│   ├── boilerplate_test.py
│   ├── page_objects.py
│   └── samples/
│       ├── __init__.py
│       ├── google_objects.py
│       └── google_test.py
├── my_first_test.py
├── parameterized_test.py
├── pytest.ini
├── requirements.txt
├── setup.cfg
└── test_demo_site.py
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

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Log files from failed tests:</h3>

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

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> The SeleniumBase Dashboard:</h3>

🔵 The ``--dashboard`` option for pytest generates a SeleniumBase Dashboard located at ``dashboard.html``, which updates automatically as tests run and produce results. Example:

```bash
pytest --dashboard --rs --headless
```

<img src="https://seleniumbase.io/cdn/img/dashboard_1.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="360" />

🔵 Additionally, you can host your own SeleniumBase Dashboard Server on a port of your choice. Here's an example of that using Python 3's ``http.server``:

```bash
python -m http.server 1948
```

🔵 Now you can navigate to ``http://localhost:1948/dashboard.html`` in order to view the dashboard as a web app. This requires two different terminal windows: one for running the server, and another for running the tests, which should be run from the same directory. (Use ``CTRL-C`` to stop the http server.)

🔵 Here's a full example of what the SeleniumBase Dashboard may look like:

```bash
pytest test_suite.py --dashboard --rs --headless
```

<img src="https://seleniumbase.io/cdn/img/dashboard_2.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="480" />

--------

<a id="creating_visual_reports"></a>
<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Creating Visual Test Reports:</h3>

<h4><b>Pytest Reports:</b></h4>

🔵 Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```

<img src="https://seleniumbase.io/cdn/img/html_report.png" alt="Example Pytest Report" title="Example Pytest Report" width="520" />

🔵 When combining pytest html reports with SeleniumBase Dashboard usage, the pie chart from the Dashboard will get added to the html report. Additionally, if you set the html report URL to be the same as the Dashboard URL when also using the dashboard, (example: ``--dashboard --html=dashboard.html``), then the Dashboard will become an advanced html report when all the tests complete.

🔵 Here's an example of an upgraded html report:

```bash
pytest test_suite.py --dashboard --html=report.html
```

<img src="https://seleniumbase.io/cdn/img/dash_report.jpg" alt="Dashboard Pytest HTML Report" title="Dashboard Pytest HTML Report" width="520" />

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

<img src="https://seleniumbase.io/cdn/img/nose_report.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(NOTE: You can add ``--show-report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show-report`` when running tests locally because it pauses the test run.)

<h4><b>Allure Reports:</b></h4>

See: [https://docs.qameta.io/allure/](https://docs.qameta.io/allure/#_pytest)

```bash
pytest test_suite.py --alluredir=allure_results
```


<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Using a Proxy Server:</h3>

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


<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Changing the User-Agent:</h3>

🔵 If you wish to change the User-Agent for your browser tests (Chromium and Firefox only), you can add ``--agent="USER AGENT STRING"`` as an argument on the command-line.

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```


<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Building Guided Tours for Websites:</h3>

🔵 Learn about <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md">SeleniumBase Interactive Walkthroughs</a> (in the ``examples/tour_examples/`` folder). It's great for prototyping a website onboarding experience.


<a id="utilizing_advanced_features"></a>
<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Production Environments & Integrations:</h3>

🔵 Here are some things you can do to set up a production environment for your testing:

* You can set up a [Jenkins](https://jenkins.io/) build server for running tests at regular intervals. For a real-world Jenkins example of headless browser automation in action, check out the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/jenkins/ReadMe.md">SeleniumBase Jenkins example on Azure</a> or the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/google_cloud/ReadMe.md">SeleniumBase Jenkins example on Google Cloud</a>.

* You can use [the Selenium Grid](https://selenium.dev/documentation/en/grid/) to scale your testing by distributing tests on several machines with parallel execution. To do this, check out the [SeleniumBase selenium_grid folder](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid), which should have everything you need, including the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md">Selenium Grid ReadMe</a>, which will help you get started.

* If you're using the <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/mysql_installation.md">SeleniumBase MySQL feature</a> to save results from tests running on a server machine, you can install [MySQL Workbench](https://dev.mysql.com/downloads/tools/workbench/) to help you read & write from your DB more easily.

* If you use [Slack](https://slack.com), you can easily have your Jenkins jobs display results there by using the [Jenkins Slack Plugin](https://github.com/jenkinsci/slack-plugin). Another way to send messages from your tests to Slack is by using [Slack's Incoming Webhooks API](https://api.slack.com/incoming-webhooks).

* If you're using AWS, you can set up an [Amazon S3](https://aws.amazon.com/s3/) account for saving log files and screenshots from your tests. To activate this feature, modify [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) with connection details in the S3 section, and add "``--with-s3-logging``" on the command-line when running your tests.

Here's an example of running tests with additional features enabled:

```bash
pytest [YOUR_TEST_FILE.py] --with-db-reporting --with-s3-logging
```

<a id="detailed_method_specifications"></a>
<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Detailed Method Specifications and Examples:</h3>

🔵 Navigating to a web page: (and related commands)

```python
self.open("https://xkcd.com/378/")  # This method opens the specified page.

self.go_back()  # This method navigates the browser to the previous page.

self.go_forward()  # This method navigates the browser forward in history.

self.refresh_page()  # This method reloads the current page.

self.get_current_url()  # This method returns the current page URL.

self.get_page_source()  # This method returns the current page source.
```

<b>ProTip™:</b> You may need to use the <code>self.get_page_source()</code> method along with Python's <code>find()</code> command to parse through the source to find something that Selenium wouldn't be able to. (You may want to brush up on your Python programming skills for that.)

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

You can also use <code>self.add_text()</code> or the WebDriver <code>.send_keys()</code> command, but those won't clear the text box first if there's already text inside.
If you want to type in special keys, that's easy too. Here's an example:

```python
from selenium.webdriver.common.keys import Keys
self.find_element("textarea").send_keys(Keys.SPACE + Keys.BACK_SPACE + '\n')  # The backspace should cancel out the space, leaving you with the newline
```

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

(NOTE: The short versions of this are ``self.find_element(ELEMENT)`` and ``self.assert_element(ELEMENT)``. The find_element() version returns the element)

Since the line above returns the element, you can combine that with .click() as shown below:

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
self.assert_true(myvar1 == something)

self.assert_equal(var1, var2)
```

🔵 Useful Conditional Statements: (with creative examples in action)

is_element_visible(selector)  # is an element visible on a page

```python
if self.is_element_visible('div#warning'):
    print("Red Alert: Something bad might be happening!")
```

is_element_present(selector)  # is an element present on a page

```python
if self.is_element_present('div#top_secret img.tracking_cookie'):
    self.contact_cookie_monster()  # Not a real SeleniumBase method
else:
    current_url = self.get_current_url()
    self.contact_the_nsa(url=current_url, message="Dark Zone Found")  # Not a real SeleniumBase method
```

Another example:

```python
def is_there_a_cloaked_klingon_ship_on_this_page():
    if self.is_element_present("div.ships div.klingon"):
        return not self.is_element_visible("div.ships div.klingon")
    return False
```

is_text_visible(text, selector)  # is text visible on a page

```python
def get_mirror_universe_captain_picard_superbowl_ad(superbowl_year):
    selector = "div.superbowl_%s div.commercials div.transcript div.picard" % superbowl_year
    if self.is_text_visible("For the Love of Marketing and Earl Grey Tea!", selector):
        return "Picard HubSpot Superbowl Ad 2015"
    elif self.is_text_visible("Delivery Drones... Engage", selector):
        return "Picard Amazon Superbowl Ad 2015"
    elif self.is_text_visible("Bing it on Screen!", selector):
        return "Picard Microsoft Superbowl Ad 2015"
    elif self.is_text_visible("OK Glass, Make it So!", selector):
        return "Picard Google Superbowl Ad 2015"
    elif self.is_text_visible("Number One, I've Never Seen Anything Like It.", selector):
        return "Picard Tesla Superbowl Ad 2015"
    elif self.is_text_visible("""With the first link, the chain is forged.
                              The first speech censored, the first thought forbidden,
                              the first freedom denied, chains us all irrevocably.""", selector):
        return "Picard Wikimedia Superbowl Ad 2015"
    elif self.is_text_visible("Let us make sure history never forgets the name ... Facebook", selector):
        return "Picard Facebook Superbowl Ad 2015"
    else:
        raise Exception("Reports of my assimilation are greatly exaggerated.")
```

🔵 Switching Tabs:

<p>What if your test opens up a new tab/window and now you have more than one page? No problem. You need to specify which one you currently want Selenium to use. Switching between tabs/windows is easy:</p>

```python
self.switch_to_window(1)  # This switches to the new tab (0 is the first one)
```

🔵 <b>ProTip™:</b> iFrames follow the same principle as new windows - you need to specify the iFrame if you want to take action on something in there

```python
self.switch_to_frame('ContentManagerTextBody_ifr')
# Now you can act inside the iFrame
# .... Do something cool (here)
self.switch_to_default_content()  # Exit the iFrame when you're done
```

🔵 Handling Pop-Up Alerts:

<p>What if your test makes an alert pop up in your browser? No problem. You need to switch to it and either accept it or dismiss it:</p>

```python
self.wait_for_and_accept_alert()

self.wait_for_and_dismiss_alert()
```

If you're not sure whether there's an alert before trying to accept or dismiss it, one way to handle that is to wrap your alert-handling code in a try/except block. Other methods such as .text and .send_keys() will also work with alerts.

🔵 Executing Custom jQuery Scripts:

<p>jQuery is a powerful JavaScript library that allows you to perform advanced actions in a web browser.
If the web page you're on already has jQuery loaded, you can start executing jQuery scripts immediately.
You'd know this because the web page would contain something like the following in the HTML:</p>

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
```

🔵 It's OK if you want to use jQuery on a page that doesn't have it loaded yet. To do so, run the following command first:

```python
self.activate_jquery()
```

🔵 Some websites have a restrictive [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) to prevent users from loading jQuery and other external libraries onto their websites. If you need to use jQuery or another JS library on such a website, add ``--disable-csp`` on the command-line.

🔵 Here are some examples of using jQuery in your scripts:

```python
self.execute_script('jQuery, window.scrollTo(0, 600)')  # Scrolling the page

self.execute_script("jQuery('#annoying-widget').hide()")  # Hiding elements on a page

self.execute_script("jQuery('#hidden-widget').show(0)")  # Showing hidden elements on a page

self.execute_script("jQuery('#annoying-button a').remove()")  # Removing elements on a page

self.execute_script("jQuery('%s').mouseover()" % (mouse_over_item))  # Mouse-over elements on a page

self.execute_script("jQuery('input#the_id').val('my_text')")  # Fast text input on a page

self.execute_script("jQuery('div#dropdown a.link').click()")  # Click elements on a page

self.execute_script("return jQuery('div#amazing')[0].text")  # Returns the css "text" of the element given

self.execute_script("return jQuery('textarea')[2].value")  # Returns the css "value" of the 3rd textarea element on the page
```

🔵 In the next example, JavaScript creates a referral button on a page, which is then clicked:

```python
start_page = "https://xkcd.com/465/"
destination_page = "https://github.com/seleniumbase/SeleniumBase"
self.open(start_page)
referral_link = '''<a class='analytics test' href='%s'>Free-Referral Button!</a>''' % destination_page
self.execute_script('''document.body.innerHTML = \"%s\"''' % referral_link)
self.click("a.analytics")  # Clicks the generated button
```

(Due to popular demand, this traffic generation example has been baked into SeleniumBase with the ``self.generate_referral(start_page, end_page)`` and the ``self.generate_traffic(start_page, end_page, loops)`` methods.)

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

🔵 Accessing Raw WebDriver

<p>If you need access to any commands that come with standard WebDriver, you can call them directly like this:</p>

```python
self.driver.delete_all_cookies()
capabilities = self.driver.capabilities
self.driver.find_elements_by_partial_link_text("GitHub")
```

(In general, you'll want to use the SeleniumBase versions of methods when available.)

🔵 Retrying failing tests automatically:

<p>You can use <code>--reruns NUM</code> to retry failing tests that many times. Use <code>--reruns-delay SECONDS</code> to wait that many seconds between retries. Example:</p>

```bash
pytest --reruns 5 --reruns-delay 1
```

<p>Additionally, you can use the <code>@retry_on_exception()</code> decorator to specifically retry failing methods. (First import: <code>from seleniumbase import decorators</code>) To learn more about SeleniumBase decorators, [click here](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/common).</p>


<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Wrap-Up</h3>

<b>Congratulations on getting started with SeleniumBase!</b>

<p>
<div><b>If you see something, say something!</b></div>
<div><a href="https://github.com/seleniumbase/SeleniumBase/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/seleniumbase/SeleniumBase.svg?color=22BB88" title="Closed Issues" /></a>   <a href="https://github.com/seleniumbase/SeleniumBase/pulls?q=is%3Apr+is%3Aclosed"><img src="https://img.shields.io/github/issues-pr-closed/seleniumbase/SeleniumBase.svg?logo=github&logoColor=white&color=22BB99" title="Closed Pull Requests" /></a></div>
</p>

<p>
<div><b>If you like us, give us a star!</b></div>
<div><a href="https://github.com/seleniumbase/SeleniumBase/stargazers"><img src="https://img.shields.io/github/stars/seleniumbase/seleniumbase.svg?color=888CFA" title="Stargazers" /></a></div>
</p>
<p><div><a href="https://github.com/mdmintz">https://github.com/mdmintz</a></div></p>

<div><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="290" /></a></div>

<div><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" title="SeleniumBase" /></a> <a href="https://github.com/seleniumbase/SeleniumBase/releases"><img src="https://img.shields.io/github/repo-size/seleniumbase/seleniumbase.svg" title="SeleniumBase" alt="Repo Size" /></a> <a href="https://gitter.im/seleniumbase/SeleniumBase"><img src="https://badges.gitter.im/seleniumbase/SeleniumBase.svg" title="SeleniumBase" alt="Join the chat!" /></a></div>

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://img.shields.io/badge/tested%20with-SeleniumBase-04C38E.svg" alt="Tested with SeleniumBase" /></a> <a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a></div>

<div><a href="https://pepy.tech/count/seleniumbase"> <img src="https://pepy.tech/badge/seleniumbase" alt="SeleniumBase PyPI downloads" /></a> <a href="https://twitter.com/SeleniumBase">
<img src="https://img.shields.io/twitter/follow/seleniumbase.svg?style=flat-rounded&logo=twitter&label=followers" alt="SeleniumBase Twitter followers" /></a></div>

<p><div><span><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.io/img/social/share_github.svg" title="SeleniumBase on GitHub" alt="SeleniumBase on GitHub" width="56" /></a></span>
<span><a href="https://gitter.im/seleniumbase/SeleniumBase"><img src="https://seleniumbase.io/img/social/share_gitter.svg" title="SeleniumBase on Gitter" alt="SeleniumBase on Gitter" width="44" /></a></span>
<span><a href="https://twitter.com/seleniumbase"><img src="https://seleniumbase.io/img/social/share_twitter.svg" title="SeleniumBase on Twitter" alt="SeleniumBase on Twitter" width="60" /></a></span>
<span><a href="https://instagram.com/seleniumbase"><img src="https://seleniumbase.io/img/social/share_instagram.svg" title="SeleniumBase on Instagram" alt="SeleniumBase on Instagram" width="52" /></a></span>
<span><a href="https://www.facebook.com/SeleniumBase"><img src="https://seleniumbase.io/img/social/share_facebook.svg" title="SeleniumBase on Facebook" alt="SeleniumBase on Facebook" width="56" /></a></span></div></p>
