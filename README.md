[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_sb4.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

[<img src="https://img.shields.io/github/release/seleniumbase/SeleniumBase.svg" alt=" " />](https://github.com/seleniumbase/SeleniumBase/releases) [<img src="https://img.shields.io/pypi/v/seleniumbase.svg" alt=" " />](https://pypi.python.org/pypi/seleniumbase) [<img src="https://badges.gitter.im/seleniumbase/SeleniumBase.svg" alt=" " />](https://gitter.im/seleniumbase/SeleniumBase) [<img src="https://img.shields.io/travis/seleniumbase/SeleniumBase/master.svg?logo=travis" alt=" " />](https://travis-ci.org/seleniumbase/SeleniumBase) [<img src="https://dev.azure.com/seleniumbase/seleniumbase/_apis/build/status/seleniumbase.SeleniumBase?branchName=master" alt=" " />](https://dev.azure.com/seleniumbase/seleniumbase/_build/latest?definitionId=1&branchName=master) [<img src="https://github.com/seleniumbase/SeleniumBase/workflows/CI%20build/badge.svg">](https://github.com/seleniumbase/SeleniumBase/actions) [<img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" alt=" " />](https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE) [<img src="https://img.shields.io/github/stars/seleniumbase/seleniumbase.svg" alt=" " />](https://github.com/seleniumbase/SeleniumBase/stargazers)

Python Framework for End-to-End UI Testing with [Selenium WebDriver](https://selenium.dev) and [pytest](https://pytest.org).

#### Features include:
* [Python methods](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md) to enhance WebDriver.
* Can run tests on web & mobile browsers.
* [Command-line options](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md) for test flexibility.
* Can do parallel testing on [Selenium Grid](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md).
* Includes tools for debugging tests easily.
* Supports [Azure](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/azure_pipelines/ReadMe.md), [GCP](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/google_cloud/ReadMe.md), [TravisCI](https://github.com/seleniumbase/SeleniumBase/blob/master/.travis.yml), & [Docker](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/docker/ReadMe.md).
* A logging system that takes screenshots.
* Includes a tool for [building website tours](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md).
* Lots of [examples](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/ReadMe.md) to help you get started.
* [Click here](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/features_list.md) to see a longer list of features.

<img src="https://cdn2.hubspot.net/hubfs/100006/images/my_first_test_gif.gif" title="SeleniumBase"><br />
(<i>Above: [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) from [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) in Demo Mode.</i>)<br />
```
pytest my_first_test.py --demo
```
---
[<img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_logo_dh.png" title="SeleniumBase" align="center" height="155">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Get Started:

You'll need **[Python](https://www.python.org/downloads/)** on your System PATH. [<img src="https://img.shields.io/pypi/pyversions/seleniumbase.svg?logo=python&logoColor=lightblue" alt="Python versions" alt="Python versions" />](https://www.python.org/downloads/)

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Install/upgrade ``pip``:
```bash
python -m easy_install -U pip
```

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Setup a Virtual Environment: (Optional)
To isolate **python** dependencies between projects, use a Virtual Environment. See the **[ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md)** for instructions. (<i>You can also read the official tutorial on virtual environments from **[python.org](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)**</i>)

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Install ``seleniumbase``: [<img src="https://img.shields.io/badge/pypi-seleniumbase-22AAEE.svg" alt=" " />](https://pypi.python.org/pypi/seleniumbase)
```bash
pip install seleniumbase
```
* Add ``--upgrade`` OR ``-U`` to upgrade an installation.
* Add ``--force-reinstall`` for a clean install.

You can also install seleniumbase from a ``git clone``:
```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase
pip install -r requirements.txt
python setup.py install
```
If multiple versions of Python are installed, be specific (E.g. use ``python3`` instead of ``python``).

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Download a webdriver:

SeleniumBase can download a webdriver to the [seleniumbase/drivers](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/drivers) folder with the ``install`` command:
```bash
seleniumbase install chromedriver
```
* You need a different webdriver for each web browser you want to run automation on: ``chromedriver`` for Chrome, ``edgedriver`` for Edge, ``geckodriver`` for Firefox, ``operadriver`` for Opera, and ``iedriver`` for Internet Explorer.
* If you have the latest version of Chrome installed, get the latest chromedriver (<i>otherwise it defaults to chromedriver 2.44 for compatibility reasons</i>):
```bash
seleniumbase install chromedriver latest
```

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Run a test on Chrome:
```bash
cd examples
pytest my_first_test.py
```
* Chrome is the default browser if not specified with ``--browser=BROWSER``.
* On Linux ``--headless`` is the default behavior (running with no GUI). You can also run in headless mode on any OS. If your Linux machine has a GUI and you want to see the web browser as tests run, add ``--headed`` or ``--gui``.

**Check out [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) to see what a simple test looks like:**
* <i>By default, [CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp) are used for finding page elements.</i>
* Here are some common SeleniumBase methods you might find in tests:
```python
self.open(URL)  # Navigate to the web page
self.click(SELECTOR)  # Click a page element
self.update_text(SELECTOR, TEXT)  # Type text (Add "\n" to text for pressing enter/return.)
self.assert_element(SELECTOR)  # Assert element is visible
self.assert_text(TEXT)  # Assert text is visible (has optional SELECTOR arg)
self.assert_title(PAGE_TITLE)  # Assert page title
self.assert_no_404_errors()  # Assert no 404 errors from files on the page
self.assert_no_js_errors()  # Assert no JavaScript errors on the page (Chrome-ONLY)
self.execute_script(JAVASCRIPT)  # Execute javascript code
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
For the complete list of SeleniumBase methods, see: **[help_docs/method_summary.md](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md)**

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Learn More:

#### **Automatic WebDriver abilities:**<br />
SeleniumBase automatically handles common WebDriver actions such as spinning up web browsers and saving screenshots during test failures. (<i>[Read more about customizing test runs](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md).</i>)

#### **Simplified code:**<br />
SeleniumBase uses simple syntax for commands, such as:
```python
self.update_text("input", "dogs\n")
```
The same command with regular WebDriver is very messy:
(<i>And it doesn't include SeleniumBase smart-waiting.</i>)
```python
self.driver.find_element_by_css_selector("input").clear()  # Not always needed
self.driver.find_element_by_css_selector("input").send_keys("dogs")
self.driver.find_element_by_css_selector("input").submit()
```
(<i>You can still use ``self.driver`` in your code.</i>)

#### **Run tests with ``pytest`` or ``nosetests`` in any browser:**<br />
(<i>Using **pytest** is recommended. **Chrome** is the default browser.</i>)
```bash
pytest my_first_test.py --browser=chrome

nosetests test_suite.py --browser=firefox
```
All Python methods that start with ``test_`` will automatically be run when using ``pytest`` or ``nosetests`` on a Python file, (<i>or on folders containing Python files</i>). You can also be more specific on what to run within a file by using the following: (<i>Note that the syntax is different for pytest vs nosetests.</i>)
```bash
pytest [FILE_NAME].py::[CLASS_NAME]::[METHOD_NAME]
nosetests [FILE_NAME].py:[CLASS_NAME].[METHOD_NAME]
```

#### **No more flaky tests:**<br />
SeleniumBase methods automatically wait for page elements to finish loading before interacting with them (*up to a timeout limit*). This means you no longer need random ``time.sleep()`` statements in your scripts.

#### **Automated/manual hybrid mode:**<br />
SeleniumBase includes a solution called **[MasterQA](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/masterqa/ReadMe.md)**, which speeds up manual testing by having automation perform all the browser actions while the manual tester handles validatation.

#### **Feature-Rich:**<br />
For a full list of SeleniumBase features, [Click Here](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/features_list.md).


<a id="seleniumbase_installation"></a>
<img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_media_logo_c.png" title="SeleniumBase" height="100">

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Detailed Instructions:

**Here's how to run the example script on various web browsers:**

First install a webdriver for each browser you intend to use:
```bash
seleniumbase install chromedriver
seleniumbase install geckodriver
seleniumbase install edgedriver
seleniumbase install iedriver
seleniumbase install operadriver
```

Next, choose between **pytest** and **nosetests** test runners. (<i>Mostly interchangeable.</i>)
```bash
cd examples/

pytest my_first_test.py --browser=chrome

nosetests my_first_test.py --browser=firefox
```
(<i>If no browser is specified, Chrome is used by default.</i>)
With Pytest, a green dot means a test passed. An "F" means a test failed.

<a id="seleniumbase_demo_mode"></a> **Use Demo Mode to help you see what tests are asserting.**

If the example test is moving too fast for your eyes, you can run it in **Demo Mode** by adding ``--demo`` on the command-line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real time:
```bash
pytest my_first_test.py --demo
```

**Pytest** includes test discovery. If you don't specify a specific file or folder to run from, ``pytest`` will search all subdirectories automatically for tests to run based on the following matching criteria:
Python filenames that start with ``test_`` or end with ``_test.py``.
Python methods that start with ``test_``.
The Python class name can be anything since SeleniumBase's ``BaseCase`` class inherits from the ``unittest.TestCase`` class.
You can see which tests are getting discovered by ``pytest`` by using:
```bash
pytest --collect-only -q
```

You can use the following in your scripts to help you debug issues:
(<i>If using ipdb, make sure you add "-s" to command-line options unless already in pytest.ini</i>)
```python
import time; time.sleep(5)  # Makes the test wait and do nothing for 5 seconds.
import ipdb; ipdb.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
import pytest; pytest.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
```

**To pause an active test that throws an exception or error, add ``--pdb -s``:**
```bash
pytest my_first_test.py --pdb -s
```
The code above will leave your browser window open in case there's a failure. (ipdb commands: 'n', 'c', 's' => next, continue, step).

Here are some other useful command-line options that come with Pytest:
```bash
-v  # Prints the full test name for each test.
-q  # Prints fewer details in the console output when running tests.
-x  # Stop running the tests after the first failure is reached.
--html=report.html  # Creates a detailed pytest-html report after tests finish.
--collect-only  # Show what tests would get run without actually running them.
-s  # See print statements. (Should be on by default with pytest.ini present.)
-n=NUM  # Multithread the tests using that many threads. (Speed up test runs!)
```

SeleniumBase provides additional Pytest command-line options for tests:
```bash
--browser=BROWSER  # (The web browser to use.)
--cap-file=FILE  # (The web browser's desired capabilities to use.)
--settings-file=FILE  # (Overrides SeleniumBase settings.py values.)
--env=ENV  # (Set a test environment. Use "self.env" to use this in tests.)
--data=DATA  # (Extra data to pass to tests. Use "self.data" in tests.)
--user-data-dir=DIR  # (Set the Chrome user data directory to use.)
--server=SERVER  # (The server / IP address used by the tests.)
--port=PORT  # (The port that's used by the test server.)
--proxy=SERVER:PORT  # (This is the proxy server:port combo used by tests.)
--agent=STRING  # (This designates the web browser's User Agent to use.)
--mobile  # (The option to use the mobile emulator while running tests.)
--metrics=STRING  # ("CSSWidth,Height,PixelRatio" for mobile emulator tests.)
--extension-zip=ZIP  # (Load a Chrome Extension .zip file, comma-separated.)
--extension-dir=DIR  # (Load a Chrome Extension directory, comma-separated.)
--headless  # (The option to run tests headlessly. The default on Linux OS.)
--headed  # (The option to run tests with a GUI on Linux OS.)
--start-page=URL  # (The starting URL for the web browser when tests begin.)
--log-path=LOG_PATH  # (The directory where log files get saved to.)
--archive-logs  # (Archive old log files instead of deleting them.)
--slow  # (The option to slow down the automation.)
--demo  # (The option to visually see test actions as they occur.)
--demo-sleep=SECONDS  # (The option to wait longer after Demo Mode actions.)
--highlights=NUM  # (Number of highlight animations for Demo Mode actions.)
--message-duration=SECONDS  # (The time length for Messenger alerts.)
--check-js  # (The option to check for JavaScript errors after page loads.)
--ad-block  # (The option to block some display ads after page loads.)
--verify-delay=SECONDS  # (The delay before MasterQA verification checks.)
--disable-csp  # (This disables the Content Security Policy of websites.)
--enable-sync  # (The option to enable "Chrome Sync".)
--reuse-session  # (The option to reuse the browser session between tests.)
--maximize-window  # (The option to start with the web browser maximized.)
--save-screenshot  # (The option to save a screenshot after each test.)
--visual-baseline  # (Set the visual baseline for Visual/Layout tests.)
--timeout-multiplier=MULTIPLIER  # (Multiplies the default timeout values.)
```
(For more details, see the full list of command-line options **[here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py)**.)

During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you add --archive_logs to command-line options, or have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), otherwise log files with be cleaned up at the start of the next test run. The ``test_suite.py`` collection contains tests that fail on purpose so that you can see how logging works.
```bash
cd examples/

pytest test_suite.py --browser=chrome

pytest test_suite.py --browser=firefox
```

An easy way to override seleniumbase/config/settings.py is by using a custom settings file.
Here's the command-line option to add to tests: (See [examples/custom_settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/custom_settings.py))
``--settings_file=custom_settings.py``
(Settings include default timeout values, a two-factor auth key, DB credentials, S3 credentials, and other important settings used by tests.)

To pass additional data from the command-line to tests, add ``--data="ANY STRING"``.
Now inside your tests, you can use ``self.data`` to access that.


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Test Directory Customization:**

For running tests outside of the SeleniumBase repo with **Pytest**, you'll want a copy of **[pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini)** on the root folder. For running tests outside of the SeleniumBase repo with **Nosetests**, you'll want a copy of **[setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg)** on the root folder. (Subfolders should include a blank ``__init__.py`` file.) These files specify default configuration details for tests. (For nosetest runs, you can also specify a .cfg file by using ``--config``. Example ``nosetests [MY_TEST].py --config=[MY_CONFIG].cfg``)

As a shortcut, you'll be able to run ``seleniumbase mkdir [DIRECTORY_NAME]`` to create a new folder that already contains necessary files and some example tests that you can run. Example:
```bash
seleniumbase mkdir ui_tests
cd ui_tests
pytest my_first_test.py
```


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Logging / Results from Failing Tests:**

Let's try an example of a test that fails:
```python
""" test_fail.py """
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_find_army_of_robots_on_xkcd_desert_island(self):
        self.open("https://xkcd.com/731/")
        self.assert_element("div#ARMY_OF_ROBOTS", timeout=1)  # This should fail
```

You can run it from the ``examples`` folder like this:
```bash
pytest test_fail.py
```

You'll notice that a logs folder, "latest_logs", was created to hold information about the failing test, and screenshots. During test runs, past results get moved to the archived_logs folder if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), or if your run tests with ``--archive-logs``. If you choose not to archive existing logs, they will be deleted and replaced by the logs of the latest test run.


<a id="creating_visual_reports"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Creating Visual Test Suite Reports:**

(NOTE: Several command-line args are different for Pytest vs Nosetests)

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.
```bash
pytest test_suite.py --html=report.html
```

![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

You can also use ``--junit-xml=report.xml`` to get an xml report instead. Jenkins can use this file to display better reporting for your tests.
```bash
pytest test_suite.py --junit-xml=report.xml
```

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes.
```bash
nosetests test_suite.py --report
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" title="Example Nosetest Report" height="420">

(NOTE: You can add ``--show-report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show-report`` when running tests locally because it pauses the test run.)


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Using a Proxy Server:**

If you wish to use a proxy server for your browser tests (Chrome and Firefox only), you can add ``--proxy=IP_ADDRESS:PORT`` as an argument on the command-line.
```bash
pytest proxy_test.py --proxy=IP_ADDRESS:PORT
```

If the proxy server that you wish to use requires authentication, you can do the following (Chrome only):
```bash
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT
```

To make things easier, you can add your frequently-used proxies to PROXY_LIST in [proxy_list.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/proxy_list.py), and then use ``--proxy=KEY_FROM_PROXY_LIST`` to use the IP_ADDRESS:PORT of that key.
```bash
pytest proxy_test.py --proxy=proxy1
```


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Changing the User-Agent:**

If you wish to change the User-Agent for your browser tests (Chrome and Firefox only), you can add ``--agent="USER AGENT STRING"`` as an argument on the command-line.
```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32">  **Building Guided Tours for Websites:**

Learn about [SeleniumBase Interactive Walkthroughs](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/tour_examples/ReadMe.md) (in the ``examples/tour_examples`` folder). It's great for prototyping a website onboarding experience.

<img src="https://cdn2.hubspot.net/hubfs/100006/google_tour_3.gif" title="SeleniumBase Tour of Google">

<a id="utilizing_advanced_features"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Production Environments & Integrations:**

Here are some things you can do to setup a production environment for your testing:

* You can setup a [Jenkins](https://jenkins.io/) build server for running tests at regular intervals. For a real-world Jenkins example of headless browser automation in action, check out the [SeleniumBase Jenkins example on Azure](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/azure/jenkins/ReadMe.md) or the [SeleniumBase Jenkins example on Google Cloud](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/google_cloud/ReadMe.md).

* You can use [the Selenium Grid](https://selenium.dev/documentation/en/grid/) to scale your testing by distributing tests on several machines with parallel execution. To do this, check out the [SeleniumBase selenium_grid folder](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid), which should have everything you need, including the [Selenium Grid ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md), which will help you get started.

* If you're using the [SeleniumBase MySQL feature](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/mysql_installation.md) to save results from tests running on a server machine, you can install [MySQL Workbench](https://dev.mysql.com/downloads/tools/workbench/) to help you read & write from your DB more easily.

* If you use [Slack](https://slack.com), you can easily have your Jenkins jobs display results there by using the [Jenkins Slack Plugin](https://github.com/jenkinsci/slack-plugin). Another way to send messages from your tests to Slack is by using [Slack's Incoming Webhooks API](https://api.slack.com/incoming-webhooks).

* If you're using AWS, you can setup an [Amazon S3](https://aws.amazon.com/s3/) account for saving log files and screenshots from your tests. To activate this feature, modify [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) with connection details in the S3 section, and add "``--with-s3-logging``" on the command-line when running your tests.

Here's an example of running tests with additional features enabled:
```bash
pytest [YOUR_TEST_FILE].py --with-db-reporting --with-s3-logging
```

<img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_media_logo_c.png" title="SeleniumBase" height="100">

<a id="detailed_method_specifications"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Detailed Method Specifications and Examples:**

#### Navigating to a web page (and related commands)

```python
self.open("https://xkcd.com/378/")  # This method opens the specified page.

self.go_back()  # This method navigates the browser to the previous page.

self.go_forward()  # This method navigates the browser forward in history.

self.refresh_page()  # This method reloads the current page.

self.get_current_url()  # This method returns the current page URL.

self.get_page_source()  # This method returns the current page source.
```

**ProTip™:** You may need to use the get_page_source() method along with Python's find() command to parse through the source to find something that Selenium wouldn't be able to. (You may want to brush up on your Python programming skills for that.)
```python
source = self.get_page_source()
head_open_tag = source.find('<head>')
head_close_tag = source.find('</head>', head_open_tag)
everything_inside_head = source[head_open_tag+len('<head>'):head_close_tag]
```

#### Clicking

To click an element on the page:
```python
self.click("div#my_id")
```

**ProTip™:** In most web browsers, you can right-click on a page and select ``Inspect Element`` to see the CSS selector details that you'll need to create your own scripts.

#### Typing Text

self.update_text(selector, text)  # updates the text from the specified element with the specified value. An exception is raised if the element is missing or if the text field is not editable. Example:
```python
self.update_text("input#id_value", "2012")
```

You can also use self.add_text() or the WebDriver .send_keys() command, but those won't clear the text box first if there's already text inside.
If you want to type in special keys, that's easy too. Here's an example:
```python
from selenium.webdriver.common.keys import Keys
self.find_element("textarea").send_keys(Keys.SPACE + Keys.BACK_SPACE + '\n')  # The backspace should cancel out the space, leaving you with the newline
```

#### Getting the text from an element on a page
```python
text = self.get_text("header h2")
```

#### Getting the attribute value from an element on a page
```python
attribute = self.get_attribute("#comic img", "title")
```

#### Asserting existance of an element on a page within some number of seconds:
```python
self.wait_for_element_present("div.my_class", timeout=10)
```
(NOTE: You can also use: ``self.assert_element_present(ELEMENT)``)

#### Asserting visibility of an element on a page within some number of seconds:
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

#### Asserting visibility of text inside an element on a page within some number of seconds:
```python
self.assert_text("Make it so!", "div#trek div.picard div.quotes")
self.assert_text("Tea. Earl Grey. Hot.", "div#trek div.picard div.quotes", timeout=3)
```
(NOTE: ``self.find_text(TEXT, ELEMENT)`` and ``self.wait_for_text(TEXT, ELEMENT)`` also do this. For backwords compatibility, older method names were kept, but the default timeout may be different.)

#### Asserting Anything
```python
self.assert_true(myvar1 == something)

self.assert_equal(var1, var2)
```

#### Useful Conditional Statements (with creative examples in action)

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

#### Switching Tabs

What if your test opens up a new tab/window and now you have more than one page? No problem. You need to specify which one you currently want Selenium to use. Switching between tabs/windows is easy:
```python
self.switch_to_window(1)  # This switches to the new tab (0 is the first one)
```

**ProTip™:** iFrames follow the same principle as new windows - you need to specify the iFrame if you want to take action on something in there
```python
self.switch_to_frame('ContentManagerTextBody_ifr')
# Now you can act inside the iFrame
# .... Do something cool (here)
self.switch_to_default_content()  # Exit the iFrame when you're done
```

#### Handle Pop-Up Alerts

What if your test makes an alert pop up in your browser? No problem. You need to switch to it and either accept it or dismiss it:
```python
self.wait_for_and_accept_alert()

self.wait_for_and_dismiss_alert()
```

If you're not sure whether there's an alert before trying to accept or dismiss it, one way to handle that is to wrap your alert-handling code in a try/except block. Other methods such as .text and .send_keys() will also work with alerts.

#### Executing Custom jQuery Scripts:

jQuery is a powerful JavaScript library that allows you to perform advanced actions in a web browser.
If the web page you're on already has jQuery loaded, you can start executing jQuery scripts immediately.
You'd know this because the web page would contain something like the following in the HTML:
```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
```

It's OK if you want to use jQuery on a page that doesn't have it loaded yet. To do so, run the following command first:
```python
self.activate_jquery()
```

Some websites have a restrictive [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) to prevent users from loading jQuery and other external libraries onto their websites. If you need to use jQuery or another JS library on such a website, add ``--disable_csp`` on the command-line.

Here are some examples of using jQuery in your scripts:
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

In the following example, JavaScript is used to plant code on a page that Selenium can then touch after that:
```python
start_page = "https://xkcd.com/465/"
destination_page = "https://github.com/seleniumbase/SeleniumBase"
self.open(start_page)
referral_link = '''<a class='analytics test' href='%s'>Free-Referral Button!</a>''' % destination_page
self.execute_script('''document.body.innerHTML = \"%s\"''' % referral_link)
self.click("a.analytics")  # Clicks the generated button
```
(Due to popular demand, this traffic generation example has been baked into SeleniumBase with the ``self.generate_referral(start_page, end_page)`` and the ``self.generate_traffic(start_page, end_page, loops)`` methods.)

#### Using delayed asserts:

Let's say you want to verify multiple different elements on a web page in a single test, but you don't want the test to fail until you verified several elements at once so that you don't have to rerun the test to find more missing elements on the same page. That's where delayed asserts come in. Here's the example:
```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_delayed_asserts(self):
        self.open('https://xkcd.com/993/')
        self.wait_for_element('#comic')
        self.delayed_assert_element('img[alt="Brand Identity"]')
        self.delayed_assert_element('img[alt="Rocket Ship"]')  # Will Fail
        self.delayed_assert_element('#comicmap')
        self.delayed_assert_text('Fake Item', '#middleContainer')  # Will Fail
        self.delayed_assert_text('Random', '#middleContainer')
        self.delayed_assert_element('a[name="Super Fake !!!"]')  # Will Fail
        self.process_delayed_asserts()
```

``delayed_assert_element()`` and ``delayed_assert_text()`` will save any exceptions that would be raised.
To flush out all the failed delayed asserts into a single exception, make sure to call ``self.process_delayed_asserts()`` at the end of your test method. If your test hits multiple pages, you can call ``self.process_delayed_asserts()`` at the end of all your delayed asserts for a single page. This way, the screenshot from your log file will have the location where the delayed asserts were made.

#### Accessing raw WebDriver

If you need access to any commands that come with standard WebDriver, you can call them directly like this:
```python
self.driver.delete_all_cookies()
capabilities = self.driver.capabilities
self.driver.find_elements_by_partial_link_text("GitHub")
```
(In general, you'll want to use the SeleniumBase versions of methods when available.)

#### Retrying failing tests automatically

You can use ``--reruns NUM`` to retry failing tests that many times. Use ``--reruns-delay SECONDS`` to wait that many seconds between retries. Example:
```
pytest --reruns 5 --reruns-delay 1
```

Additionally, you can use the ``@retry_on_exception()`` decorator to specifically retry failing methods. (First import: ``from seleniumbase import decorators``) To learn more about SeleniumBase decorators, [click here](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/common).


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Wrap-Up

#### Congratulations on getting started with SeleniumBase!

<i>**Questions or Comments?**</i><br />
[![Join the chat at https://gitter.im/seleniumbase/SeleniumBase](https://badges.gitter.im/seleniumbase/SeleniumBase.svg)](https://gitter.im/seleniumbase/SeleniumBase?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)<br />

If you see something, say something! We are very active in resolving issues. [<img src="https://img.shields.io/github/issues-closed-raw/seleniumbase/SeleniumBase.svg" alt=" " />](https://github.com/seleniumbase/SeleniumBase/issues?q=is%3Aissue+is%3Aclosed)

[https://github.com/mdmintz](https://github.com/mdmintz)<br />

[<img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_media_logo_c.png" title="SeleniumBase" height="100">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md) <br /> [<img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" alt=" " />](https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE)
