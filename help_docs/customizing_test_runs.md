[<img src="https://seleniumbase.io/cdn/img/sb_logo_10t.png" title="SeleniumBase" width="240">](https://github.com/seleniumbase/SeleniumBase/)

## pytest options for SeleniumBase

SeleniumBase's [pytest plugin](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py) lets you customize test runs from the CLI (Command-Line Interface), which adds options for setting/enabling the browser type, Dashboard Mode, Demo Mode, Headless Mode, Mobile Mode, Multi-threading Mode, Recorder Mode, reuse-session mode, proxy config, user agent config, browser extensions, html-report mode, and more.

Here are some examples of configuring tests, which can be run from the [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder:

```bash
# Run a test in Chrome (default browser)
pytest my_first_test.py

# Run a test in Firefox
pytest test_swag_labs.py --browser=firefox

# Run a test in Demo Mode (highlight assertions)
pytest test_demo_site.py --demo

# Run a test in Headless Mode (invisible browser)
pytest test_demo_site.py --headless

# Run tests multi-threaded using [n] threads
pytest test_suite.py -n=4

# Reuse the browser session for all tests being run
pytest test_suite.py --reuse-session

# Reuse the browser session, but empty cookies between tests
pytest test_suite.py --reuse-session --crumbs

# Create a real-time dashboard for test results
pytest test_suite.py --dashboard

# Create a pytest html report after tests are done
pytest test_suite.py --html=report.html

# Activate Debug Mode on failures ("c" to continue)
pytest test_fail.py --pdb -s

# Rerun failing tests more times
pytest test_suite.py --reruns=1

# Activate Debug Mode as the test begins ("n": next. "c": continue)
pytest test_null.py --trace -s

# Activate Recorder/Debug Mode as the test begins ("c" to continue)
pytest test_null.py --recorder --trace -s

# Pass extra data into tests (retrieve by calling self.data)
pytest my_first_test.py --data="ABC,DEF"

# Run tests on a local Selenium Grid
pytest test_suite.py --server="127.0.0.1"

# Run tests on a remote Selenium Grid
pytest test_suite.py --server=IP_ADDRESS --port=4444

# Run tests on a remote Selenium Grid with authentication
pytest test_suite.py --server=USERNAME:KEY@IP_ADDRESS --port=80

# Run tests through a proxy server
pytest proxy_test.py --proxy=IP_ADDRESS:PORT

# Run tests through a proxy server with authentication
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT

# Run tests while setting the web browser's User Agent
pytest user_agent_test.py --agent="USER-AGENT-STRING"

# Run tests using Chrome's mobile device emulator (default settings)
pytest test_swag_labs.py --mobile

# Run mobile tests specifying CSS Width, CSS Height, and Pixel-Ratio
pytest test_swag_labs.py --mobile --metrics="411,731,3"

# Run tests while changing SeleniumBase default settings
pytest my_first_test.py --settings-file=custom_settings.py
```

You can interchange ``pytest`` with ``nosetests`` for most tests, but using ``pytest`` is recommended. (``chrome`` is the default browser if not specified.)

If you're using ``pytest`` for running tests outside of the SeleniumBase repo, you'll want a copy of [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini) at the base of the new folder structure. If using ``nosetests``, the same applies for [setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg).

Here are some useful command-line options that come with ``pytest``:

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

SeleniumBase provides additional ``pytest`` command-line options for tests:

```bash
--browser=BROWSER  # (The web browser to use. Default: "chrome".)
--chrome  # (Shortcut for "--browser=chrome". On by default.)
--edge  # (Shortcut for "--browser=edge".)
--firefox  # (Shortcut for "--browser=firefox".)
--ie  # (Shortcut for "--browser=ie".)
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
--protocol=PROTOCOL  # (The Selenium Grid protocol: http|https.)
--server=SERVER  # (The Selenium Grid server/IP used for tests.)
--port=PORT  # (The Selenium Grid port used by the test server.)
--proxy=SERVER:PORT  # (Connect to a proxy server:port for tests.)
--proxy=USERNAME:PASSWORD@SERVER:PORT  # (Use authenticated proxy server.)
--agent=STRING  # (Modify the web browser's User-Agent string.)
--mobile  # (Use the mobile device emulator while running tests.)
--metrics=STRING  # (Set mobile metrics: "CSSWidth,CSSHeight,PixelRatio".)
--chromium-arg=ARG  # (Add a Chromium arg for Chrome/Edge, comma-separated.)
--firefox-arg=ARG  # (Add a Firefox arg for Firefox, comma-separated.)
--firefox-pref=SET  # (Set a Firefox preference:value set, comma-separated.)
--extension-zip=ZIP  # (Load a Chrome Extension .zip|.crx, comma-separated.)
--extension-dir=DIR  # (Load a Chrome Extension directory, comma-separated.)
--headless  # (Run tests in headless mode. The default arg on Linux OS.)
--headed  # (Run tests in headed/GUI mode on Linux OS.)
--xvfb  # (Run tests using the Xvfb virtual display server on Linux OS.)
--locale=LOCALE_CODE  # (Set the Language Locale Code for the web browser.)
--interval=SECONDS  # (The autoplay interval for presentations & tour steps)
--start-page=URL  # (The starting URL for the web browser when tests begin.)
--archive-logs  #  (Archive existing log files instead of deleting them.)
--archive-downloads  #  (Archive old downloads instead of deleting them.)
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
--recorder  # (Enables the Recorder for turning browser actions into code.)
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
--reuse-session | --rs  # (Reuse the browser session between tests.)
--crumbs  # (Delete all cookies between tests reusing a session.)
--maximize-window  # (Start tests with the web browser window maximized.)
--save-screenshot  # (Save a screenshot at the end of each test.)
--visual-baseline  # (Set the visual baseline for Visual/Layout tests.)
--timeout-multiplier=MULTIPLIER  # (Multiplies the default timeout values.)
```

(For more details, see the full list of command-line options **[here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py)**.)

You can also view a list of popular ``pytest`` options for SeleniumBase by typing:

```bash
seleniumbase options
```

Or the short form:

```bash
sbase options
```

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Example tests using Logging:</h3>

To see logging abilities, you can run a test suite that includes tests that fail on purpose:

```bash
pytest test_suite.py
```

🔵 During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. If ``--archive-logs`` is specified (or if ARCHIVE_EXISTING_LOGS is set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)), test logs will also get archived to the ``archived_logs/`` folder. Otherwise, the log files will be cleaned out when the next test run begins (by default).

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Demo Mode:</h3>

If any test is moving too fast for your eyes to see what's going on, you can run it in **Demo Mode** by adding ``--demo`` on the command line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real time:

```bash
pytest my_first_test.py --demo
```

You can override the default wait time by either updating [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) or by using ``--demo-sleep={NUM}`` when using Demo Mode. (NOTE: If you use ``--demo-sleep={NUM}`` without using ``--demo``, nothing will happen.)

```bash
pytest my_first_test.py --demo --demo-sleep=1.2
```

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Passing additional data to tests:</h3>

If you want to pass additional data from the command line to your tests, you can use ``--data=STRING``. Now inside your tests, you can use ``self.data`` to access that.

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Running tests multithreaded:</h3>

To run pytest tests using multiple processes, add ``-n=NUM`` or ``-n NUM`` on the command line, where NUM is the number of CPUs you want to use.

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Retrying failing tests automatically:</h3>

You can use ``--reruns=NUM`` to retry failing tests that many times. Use ``--reruns-delay=SECONDS`` to wait that many seconds between retries. Example:

```bash
pytest --reruns=1 --reruns-delay=1
```

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Debugging tests:</h3>

You can use the following calls in your scripts to help you debug issues:

```python
import time; time.sleep(5)  # Makes the test wait and do nothing for 5 seconds.
import ipdb; ipdb.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
import pytest; pytest.set_trace()  # Enter debugging mode. n = next, c = continue, s = step.
```

To pause an active test that throws an exception or error, add ``--pdb -s``:

```bash
pytest my_first_test.py --pdb -s
```

The code above will leave your browser window open in case there's a failure. (ipdb commands: 'c', 's', 'n' => continue, step, next).

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Combinations of options:</h3>

There are times when you'll want to combine various command-line options for added effect.
For instance, the multi-process option, ``-n=4``, can be customized by adding:
``--dist=loadscope`` or ``--dist=loadfile`` to it.
Here's more info on that, as taken from [pytest-xdist](https://pypi.org/project/pytest-xdist/):

* ``-n=4 --dist=loadscope``: Tests are grouped by module for test functions and by class for test methods. Groups are distributed to available workers as whole units. This guarantees that all tests in a group run in the same process. This can be useful if you have expensive module-level or class-level fixtures. Grouping by class takes priority over grouping by module.

* ``-n=4 --dist=loadfile``: Tests are grouped by their containing file. Groups are distributed to available workers as whole units. This guarantees that all tests in a file run in the same worker.

You might also want to combine multiple options at once. For example:

```bash
pytest -n=4 --reuse-session --headless -v --dashboard --html=report.html
```

The above not only runs tests in parallel processes, but it also tells tests in the same process to share the same browser session, runs the tests in headless mode, displays the full name of each test on a separate line, creates a realtime dashboard of the test results, and creates a full report after all tests complete.

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

🔵 Now you can navigate to ``http://localhost:1948/dashboard.html`` in order to view the dashboard as a web app. This requires two different terminal windows: one for running the server, and another for running the tests, which should be run from the same directory. (Use ``CTRL+C`` to stop the http server.)

🔵 Here's a full example of what the SeleniumBase Dashboard may look like:

```bash
pytest test_suite.py --dashboard --rs --headless
```

<img src="https://seleniumbase.io/cdn/img/dashboard_2.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="480" />

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Pytest Reports:</h3>

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

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Nosetest Reports:</h3>

The ``--report`` option gives you a fancy report after your test suite completes.

```bash
nosetests test_suite.py --report
```

<img src="https://seleniumbase.io/cdn/img/nose_report.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Customizing default settings:</h3>

An easy way to override [seleniumbase/config/settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) is by using a custom settings file.
Here's the command-line option to add to tests: (See [examples/custom_settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/custom_settings.py))
``--settings-file=custom_settings.py``
(Settings include default timeout values, a two-factor auth key, DB credentials, S3 credentials, and other important settings used by tests.)

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Running tests on a remote Selenium Grid:</h3>

SeleniumBase lets you run tests on remote Selenium Grids such as [BrowserStack](https://www.browserstack.com/automate#)'s Selenium Grid, [Sauce Labs](https://saucelabs.com/products/open-source-frameworks/selenium)'s Selenium Grid, [TestingBot](https://testingbot.com/features)'s Selenium Grid, other Grids, and even your own Grid:

(For setting browser desired capabilities while running Selenium remotely, see the ReadMe located here: https://github.com/seleniumbase/SeleniumBase/tree/master/examples/capabilities)

Here's how to connect to a BrowserStack Selenium Grid server for running tests:

```bash
pytest test_demo_site.py --server=USERNAME:KEY@hub.browserstack.com --port=80
```

Here's how to connect to a Sauce Labs Selenium Grid server for running tests:

```bash
pytest test_demo_site.py --server=USERNAME:KEY@ondemand.us-east-1.saucelabs.com --port=443 --protocol=https
```

Here's how to connect to a TestingBot Selenium Grid server for running tests:

```bash
pytest test_demo_site.py --server=USERNAME:KEY@hub.testingbot.com --port=80
```

Here's how to connect to a CrossBrowserTesting Selenium Grid server for running tests:

```bash
pytest test_demo_site.py --server=USERNAME:KEY@hub.crossbrowsertesting.com --port=80
```

Here's how to connect to a LambdaTest Selenium Grid server for running tests:

```bash
pytest test_demo_site.py --server=USERNAME:KEY@hub.lambdatest.com --port=80
```

Or you can create your own Selenium Grid for test distribution. ([See this ReadMe for details](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md))

To use a server on the ``https`` protocol, add ``--protocol=https``:

```bash
pytest test_demo_site.py --protocol=https --server=IP_ADDRESS --port=PORT
```

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Using a Proxy Server:</h3>

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

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Changing the User-Agent:</h3>

If you wish to change the User-Agent for your browser tests (Chrome and Firefox only), you can add ``--agent="USER-AGENT-STRING"`` as an argument on the command line.

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="28" /> Mobile Device Testing:</h3>

Use ``--mobile`` to quickly run your tests using Chrome's mobile device emulator with default values for device metrics (CSS Width, CSS Height, Pixel-Ratio) and a default value set for the user agent. To configure the mobile device metrics, use ``--metrics="CSS_Width,CSS_Height,Pixel_Ratio"`` to set those values. You'll also be able to set the user agent with ``--agent="USER-AGENT-STRING"`` (a default user agent will be used if not specified). To find real values for device metrics, [see this GitHub Gist](https://gist.github.com/sidferreira/3f5fad525e99b395d8bd882ee0fd9d00). For a list of available user agent strings, [check out this page](https://developers.whatismybrowser.com/useragents/explore/).

```bash
# Run tests using Chrome's mobile device emulator (default settings)
pytest test_swag_labs.py --mobile

# Run mobile tests specifying CSS Width, CSS Height, and Pixel-Ratio
pytest test_swag_labs.py --mobile --metrics="411,731,3"

# Run mobile tests specifying the user agent
pytest test_swag_labs.py --mobile --agent="Mozilla/5.0 (Linux; Android 9; Pixel 3 XL)"
```

[<img src="https://seleniumbase.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
