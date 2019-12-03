[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_m.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Customizing test runs

In addition to [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) (which lets you customize SeleniumBase global properties) you can customize test runs from the command line with pytest (or nosetests):

* Choose the browser for tests to use (Default: Chrome)
* Choose betweeen pytest & nose unittest runners
* Choose whether to enter Debug Mode on failures
* Choose additional variables to pass into tests
* Choose the User-Agent for the browser to use
* Choose the automation speed (with Demo Mode)
* Choose whether to run tests multi-threaded
* Choose whether to rerun failing tests
* Choose whether to reuse the browser session
* Choose a Chrome Extension to load
* Choose a Chrome User Data Directory to use
* Choose a BrowserStack server to run on
* Choose a Sauce Labs server to run on
* Choose a TestingBot server to run on
* Choose a CrossBrowserTesting server
* Choose a Selenium Grid to connect to
* Choose a database to save results to
* Choose a proxy server to connect to

...and more!

#### **Examples:**

These are run from the **[examples](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)** folder.
(Chrome is the default browser if not specified.)

```bash
pytest my_first_test.py

pytest my_first_test.py --demo

pytest my_first_test.py --browser=firefox

pytest test_suite.py --html=report.html

nosetests test_suite.py --report --show-report

pytest test_suite.py --headless -n=4

pytest test_suite.py --reruns=1 --reruns-delay=1

pytest test_suite.py --server=IP_ADDRESS --port=4444

pytest test_suite.py --reuse-session

pytest test_fail.py --pdb -s

pytest proxy_test.py --proxy=IP_ADDRESS:PORT

pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT

pytest user_agent_test.py --agent="USER-AGENT-STRING"

pytest my_first_test.py --settings-file=custom_settings.py
```

You can interchange **pytest** with **nosetests**, but using pytest is strongly recommended because developers stopped supporting nosetests. Chrome is the default browser if not specified.

(NOTE: If you're using **pytest** for running tests outside of the SeleniumBase repo, **you'll want a copy of [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini) at the base of the new folder structure**. If using **nosetests**, the same applies for [setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg).)

An easy way to override seleniumbase/config/settings.py is by using a custom settings file.
Here's the command-line option to add to tests: (See [examples/custom_settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/custom_settings.py))
``--settings-file=custom_settings.py``
(Settings include default timeout values, a two-factor auth key, DB credentials, S3 credentials, and other important settings used by tests.)

#### **Running tests on [BrowserStack](https://www.browserstack.com/automate#)'s Selenium Grid, the [Sauce Labs](https://saucelabs.com/products/open-source-frameworks/selenium) Selenium Grid, the [TestingBot](https://testingbot.com/features) Selenium Grid, (or your own):**

Here's how to connect to a BrowserStack Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.browserstack.com --port=80
```

Here's how to connect to a Sauce Labs Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@ondemand.saucelabs.com --port=80
```

Here's how to connect to a TestingBot Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.testingbot.com --port=80
```

Here's how to connect to a CrossBrowserTesting Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.crossbrowsertesting.com --port=80
```

Here's how to connect to a LambdaTest Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.lambdatest.com --port=80
```

Or you can create your own Selenium Grid for test distribution. ([See this ReadMe for details](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md))

#### **Example tests using Logging:**

```bash
pytest test_suite.py --browser=chrome
```
(During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), otherwise log files with be cleaned up at the start of the next test run.)

#### **Demo Mode:**

If any test is moving too fast for your eyes to see what's going on, you can run it in **Demo Mode** by adding ``--demo`` on the command line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real time:

```bash
pytest my_first_test.py --demo
```

You can override the default wait time by either updating [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) or by using ``--demo-sleep={NUM}`` when using Demo Mode. (NOTE: If you use ``--demo-sleep={NUM}`` without using ``--demo``, nothing will happen.)

```bash
pytest my_first_test.py --demo --demo-sleep=1.2
```

#### **Passing additional data to tests:**

If you want to pass additional data from the command line to your tests, you can use ``--data=STRING``. Now inside your tests, you can use ``self.data`` to access that.

#### **Running tests multithreaded:**

To run Pytest multithreaded on multiple CPUs at the same time, add ``-n=NUM`` or ``-n NUM`` on the command line, where NUM is the number of CPUs you want to use.

#### **Retrying failing tests automatically:**

You can use ``--reruns=NUM`` to retry failing tests that many times. Use ``--reruns-delay=SECONDS`` to wait that many seconds between retries. Example:
```
pytest --reruns=2 --reruns-delay=1
```

#### **Debugging tests:**

**You can use the following code snippets in your scripts to help you debug issues:**
```python
import time; time.sleep(5)  # Makes the test wait and do nothing for 5 seconds.
import ipdb; ipdb.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
import pytest; pytest.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
```

**To pause an active test that throws an exception or error, add ``--pdb -s``:**

```bash
pytest my_first_test.py --pdb -s
```

The code above will leave your browser window open in case there's a failure. (ipdb commands: 'c', 's', 'n' => continue, step, next).

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```
![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes.

```bash
nosetests test_suite.py --report
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" title="Example Nosetest Report" height="420">

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)

Here are some other useful command-line options that come with Pytest:
```bash
-v  # Prints the full test name for each test.
-q  # Prints fewer details in the console output when running tests.
-x  # Stop running the tests after the first failure is reached.
--html=report.html  # Creates a detailed test report after tests complete. (Using the pytest-html plugin)
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

#### **Using a Proxy Server:**

If you wish to use a proxy server for your browser tests (Chrome and Firefox only), you can add ``--proxy=IP_ADDRESS:PORT`` as an argument on the command line.

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

#### **Changing the User-Agent:**

If you wish to change the User-Agent for your browser tests (Chrome and Firefox only), you can add ``--agent="USER-AGENT-STRING"`` as an argument on the command line.

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```
