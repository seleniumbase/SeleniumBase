<!-- SeleniumBase Docs -->

<a id="customizing_test_runs"></a>

<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="40"> Options / Customization</h2>

<h3>🎛️ SeleniumBase has different ways of setting options, depending on which format you're using. Options can be set via the command-line or method call.</h3>

<blockquote>
<p dir="auto"></p>
<ul dir="auto">
<li><a href="#pytest_options"><strong>01. <code>pytest</code> command-line options</strong></a></li>
<li><a href="#sb_options"><strong>02. <code>SB()</code> method options</strong></a></li>
<li><a href="#driver_options"><strong>03. <code>Driver()</code> method options</strong></a></li>
<li><a href="#sb_cdp_chrome_options"><strong>04. <code>sb_cdp.Chrome()</code> method options</strong></a></li>
<li><a href="#activate_cdp_mode_options"><strong>05. <code>activate_cdp_mode()</code> method options</strong></a></li>
</ul>
</blockquote>

--------

<a id="pytest_options"></a>
<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> 01. <code>pytest</code> command-line options</h2>

🎛️ SeleniumBase's [pytest plugin](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py) lets you customize test runs from the CLI (Command-Line Interface), which adds options for setting/enabling the browser type, Dashboard Mode, Demo Mode, Headless Mode, Mobile Mode, Multi-threading Mode, Recorder Mode, UC Mode (stealth), reuse-session mode, Proxy Mode, and more.

🎛️ Here are some examples of configuring tests, which can be run from the [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder:

```zsh
# Run a test in Chrome (default browser)
pytest my_first_test.py

# Run a test in Edge
pytest test_swag_labs.py --edge

# Run a test in Demo Mode (highlight assertions)
pytest test_demo_site.py --demo

# Run a test in Headless Mode (invisible browser)
pytest test_demo_site.py --headless

# Run tests multi-threaded using [n] threads
pytest test_suite.py -n4

# Reuse the browser session for all tests ("--reuse-session")
pytest test_suite.py --rs

# Reuse the browser session, but erase cookies between tests
pytest test_suite.py --rs --crumbs

# Create a real-time dashboard for test results
pytest test_suite.py --dashboard

# Create a pytest-html report after tests are done
pytest test_suite.py --html=report.html

# Rerun failing tests more times
pytest test_suite.py --reruns=1

# Activate Debug Mode at the start ("n": next. "c": continue)
pytest test_null.py --trace -s

# Activate Debug Mode on failures ("n": next. "c": continue)
pytest test_fail.py --pdb -s

# Activate Debug Mode at the end ("n": next. "c": continue)
pytest test_fail.py --ftrace -s

# Activate Recorder/Debug Mode as the test begins ("c" to continue)
pytest test_null.py --recorder --trace -s

# Pass extra data into tests (retrieve by calling self.data)
pytest my_first_test.py --data="ABC"

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
pytest test_swag_labs.py --mobile --metrics="360,640,2"

# Run tests using UC Mode to evade bot-detection services
pytest verify_undetected.py --uc

# Run tests while changing SeleniumBase default settings
pytest my_first_test.py --settings-file=custom_settings.py
```

🎛️ You can interchange ``pytest`` with ``nosetests`` for most tests, but using ``pytest`` is recommended. (``chrome`` is the default browser if not specified.)

🎛️ If you're using ``pytest`` for running tests outside of the SeleniumBase repo, you'll want a copy of [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini) at the base of the new folder structure. If using ``nosetests``, the same applies for [setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg).

🎛️ Here are some useful command-line options that come with ``pytest``:

```zsh
-v  # Verbose mode. Prints the full name of each test and shows more details.
-q  # Quiet mode. Print fewer details in the console output when running tests.
-x  # Stop running the tests after the first failure is reached.
--html=report.html  # Creates a detailed pytest-html report after tests finish.
--co | --collect-only  # Show what tests would get run. (Without running them)
--co -q  # (Both options together!) - Do a dry run with full test names shown.
-n=NUM  # Multithread the tests using that many threads. (Speed up test runs!)
-s  # See print statements. (Should be on by default with pytest.ini present.)
--junit-xml=report.xml  # Creates a junit-xml report after tests finish.
--pdb  # If a test fails, enter Post Mortem Debug Mode. (Don't use with CI!)
--trace  # Enter Debug Mode at the beginning of each test. (Don't use with CI!)
-m=MARKER  # Run tests with the specified pytest marker.
```

🎛️ SeleniumBase provides additional ``pytest`` command-line options for tests:

```zsh
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
--disable-features="F1,F2"  # (Disable features, comma-separated, no spaces.)
--binary-location=PATH  # (Set path of the Chromium browser binary to use.)
--driver-version=VER  # (Set the chromedriver or uc_driver version to use.)
--sjw  # (Skip JS Waits for readyState to be "complete" or Angular to load.)
--wfa  # (Wait for AngularJS to be done loading after specific web actions.)
--pls=PLS  # (Set pageLoadStrategy on Chrome: "normal", "eager", or "none".)
--headless  # (The default headless mode. Linux uses this mode by default.)
--headless1  # (Use Chrome's old headless mode. Fast, but has limitations.)
--headless2  # (Use Chrome's new headless mode, which supports extensions.)
--headed  # (Run tests in headed/GUI mode on Linux OS, where not default.)
--xvfb  # (Run tests using the Xvfb virtual display server on Linux OS.)
--xvfb-metrics=STRING  # (Set Xvfb display size on Linux: "Width,Height".)
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
--host-resolver-rules=RULES  # (Set host-resolver-rules, comma-separated.)
--block-images  # (Block images from loading during tests.)
--do-not-track  # (Indicate to websites that you don't want to be tracked.)
--verify-delay=SECONDS  # (The delay before MasterQA verification checks.)
--ee | --esc-end  # (Lets the user end the current test via the ESC key.)
--recorder  # (Enables the Recorder for turning browser actions into code.)
--rec-behave  # (Same as Recorder Mode, but also generates behave-gherkin.)
--rec-sleep  # (If the Recorder is enabled, also records self.sleep calls.)
--rec-print  # (If the Recorder is enabled, prints output after tests end.)
--disable-cookies  # (Disable Cookies on websites. Pages might break!)
--disable-js  # (Disable JavaScript on websites. Pages might break!)
--disable-csp  # (Disable the Content Security Policy of websites.)
--disable-ws  # (Disable Web Security on Chromium-based browsers.)
--enable-ws  # (Enable Web Security on Chromium-based browsers.)
--enable-sync  # (Enable "Chrome Sync" on websites.)
--uc | --undetected  # (Use undetected-chromedriver to evade bot-detection.)
--uc-cdp-events  # (Capture CDP events when running in "--undetected" mode.)
--log-cdp  # ("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
--remote-debug  # (Sync to Chrome Remote Debugger chrome://inspect/#devices)
--ftrace | --final-trace  # (Debug Mode after each test. Don't use with CI!)
--dashboard  # (Enable the SeleniumBase Dashboard. Saved at: dashboard.html)
--dash-title=STRING  # (Set the title shown for the generated dashboard.)
--enable-3d-apis  # (Enables WebGL and 3D APIs.)
--swiftshader  # (Chrome "--use-gl=angle" / "--use-angle=swiftshader-webgl")
--incognito  # (Enable Chrome's Incognito mode.)
--guest  # (Enable Chrome's Guest mode.)
--dark  # (Enable Chrome's Dark mode.)
--devtools  # (Open Chrome's DevTools when the browser opens.)
--rs | --reuse-session  # (Reuse browser session for all tests.)
--rcs | --reuse-class-session  # (Reuse session for tests in class.)
--crumbs  # (Delete all cookies between tests reusing a session.)
--disable-beforeunload  # (Disable the "beforeunload" event on Chrome.)
--window-position=X,Y  # (Set the browser's starting window position.)
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

(For more details, see the full list of command-line options **[here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py)**.)

🎛️ You can also view a list of popular ``pytest`` options for SeleniumBase by typing:

```zsh
seleniumbase options
```

Or the short form:

```zsh
sbase options
```

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Example tests using Logging:</h3>

To see logging abilities, you can run a test suite that includes tests that fail on purpose:

```zsh
pytest test_suite.py
```

🔵 During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. If ``--archive-logs`` is specified (or if ARCHIVE_EXISTING_LOGS is set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)), test logs will also get archived to the ``archived_logs/`` folder. Otherwise, the log files will be cleaned out when the next test run begins (by default).

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Demo Mode:</h3>

🔵 If any test is moving too fast for your eyes to see what's going on, you can run it in **Demo Mode** by adding ``--demo`` on the command line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real-time:

```zsh
pytest my_first_test.py --demo
```

🔵 You can override the default wait time by either updating [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) or by using ``--demo-sleep=NUM`` when using Demo Mode. (NOTE: If you use ``--demo-sleep=NUM`` without using ``--demo``, nothing will happen.)

```zsh
pytest my_first_test.py --demo --demo-sleep=1.2
```

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Passing additional data to tests:</h3>

If you want to pass additional data from the command line to your tests, you can use ``--data=STRING``. Now inside your tests, you can use ``self.data`` to access that.

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Running tests multithreaded:</h3>

To run ``pytest`` with multiple processes, add ``-n=NUM``, ``-n NUM``, or ``-nNUM`` on the command line, where ``NUM`` is the number of CPUs you want to use.

```zsh
pytest -n=8
pytest -n 8
pytest -n8
```

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> How to retry failing tests automatically:</h3>

<p>You can use <code translate="no">pytest --reruns=NUM</code> to retry failing tests that many times. Add <code translate="no">--reruns-delay=SECONDS</code> to wait that many seconds between retries. Example:</p>

```zsh
pytest --reruns=1 --reruns-delay=1
```

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Debugging tests:</h3>

🔵 You can use the following calls in your scripts to help you debug issues:

```python
import time; time.sleep(5)  # Makes the test wait and do nothing for 5 seconds.
import pdb; pdb.set_trace()  # Debug Mode. n: next, c: continue, s: step, u: up, d: down.
import pytest; pytest.set_trace()  # Debug Mode. n: next, c: continue, s: step, u: up, d: down.
```

🔵 To pause an active test that throws an exception or error, (*and keep the browser window open while **Debug Mode** begins in the console*), add **``--pdb``** as a ``pytest`` option:

```zsh
pytest test_fail.py --pdb
```

🔵 To start tests in Debug Mode, add **``--trace``** as a ``pytest`` option:

```zsh
pytest test_coffee_cart.py --trace
```

(**``pdb``** commands: ``n``, ``c``, ``s``, ``u``, ``d`` => ``next``, ``continue``, ``step``, ``up``, ``down``).

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Combinations of options:</h3>

🎛️ There are times when you'll want to combine various command-line options for added effect.
For instance, the multi-process option, ``-n8``, can be customized by adding:
``--dist=loadscope`` or ``--dist=loadfile`` to it.
There's more info on that here: [pytest-xdist](https://pypi.org/project/pytest-xdist/2.5.0/):

* ``-n8 --dist=loadscope``: Tests are grouped by module for test functions and by class for test methods. Groups are distributed to available workers as whole units. This guarantees that all tests in a group run in the same process. This can be useful if you have expensive module-level or class-level fixtures. Grouping by class takes priority over grouping by module.

* ``-n8 --dist=loadfile``: Tests are grouped by their containing file. Groups are distributed to available workers as whole units. This guarantees that all tests in a file run in the same worker.

<details>
<summary> ▶️ <code translate="no">-n8 --dist=loadgroup</code> (<b>click to expand</b>)</summary>
<div>

<ul><li>Tests are grouped by the <code translate="no">xdist_group</code> mark. Groups are distributed to available workers as whole units. This guarantees that all tests with the same <code translate="no">xdist_group</code> name run in the same worker.</li></ul>

```python
@pytest.mark.xdist_group(name="group1")
def test_1():
    pass

class Test:
    @pytest.mark.xdist_group("group1")
    def test_2():
        pass
```

<blockquote><p>This makes <code translate="no">test_1</code> and <code translate="no">Test::test_2</code> run in the same worker. Tests without the <code translate="no">xdist_group</code> mark are distributed normally.</p></blockquote>

</div>
</details>

🎛️ You might also want to combine multiple options at once. For example:

```zsh
pytest --headless -n8 --dashboard --html=report.html -v --rs --crumbs
```

The above not only runs tests in parallel processes, but it also tells tests in the same process to share the same browser session, runs the tests in headless mode, displays the full name of each test on a separate line, creates a real-time dashboard of the test results, and creates a full report after all tests complete.

--------

🎛️ For extra speed, run your tests using `chrome-headless-shell`:

First, get `chrome-headless-shell` if you don't already have it:

```zsh
sbase get chs
```

Then, run scripts with `--chs` / `chs=True`:

```zsh
pytest --chs -n8 --dashboard --html=report.html -v --rs
```

That makes your tests run very quickly in headless mode.

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> The SeleniumBase Dashboard:</h3>

🔵 The ``--dashboard`` option for pytest generates a SeleniumBase Dashboard located at ``dashboard.html``, which updates automatically as tests run and produce results. Example:

```zsh
pytest --dashboard --rs --headless
```

<img src="https://seleniumbase.github.io/cdn/img/dashboard_1.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="360" />

🔵 Additionally, you can host your own SeleniumBase Dashboard Server on a port of your choice. Here's an example of that using Python 3's ``http.server``:

```zsh
python -m http.server 1948
```

🔵 Now you can navigate to ``http://localhost:1948/dashboard.html`` in order to view the dashboard as a web app. This requires two different terminal windows: one for running the server, and another for running the tests, which should be run from the same directory. (Use <kbd>Ctrl+C</kbd> to stop the http server.)

🔵 Here's a full example of what the SeleniumBase Dashboard may look like:

```zsh
pytest test_suite.py --dashboard --rs --headless
```

<img src="https://seleniumbase.github.io/cdn/img/dashboard_2.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="480" />

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Pytest Reports:</h3>

🔵 Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```zsh
pytest test_suite.py --html=report.html
```

<img src="https://seleniumbase.github.io/cdn/img/html_report.png" alt="Example Pytest Report" title="Example Pytest Report" width="520" />

🔵 When combining pytest html reports with SeleniumBase Dashboard usage, the pie chart from the Dashboard will get added to the html report. Additionally, if you set the html report URL to be the same as the Dashboard URL when also using the dashboard, (example: ``--dashboard --html=dashboard.html``), then the Dashboard will become an advanced html report when all the tests complete.

🔵 Here's an example of an upgraded html report:

```zsh
pytest test_suite.py --dashboard --html=report.html
```

<img src="https://seleniumbase.github.io/cdn/img/dash_report.jpg" alt="Dashboard Pytest HTML Report" title="Dashboard Pytest HTML Report" width="520" />

If viewing pytest html reports in [Jenkins](https://www.jenkins.io/), you may need to [configure Jenkins settings](https://stackoverflow.com/a/46197356/7058266) for the html to render correctly. This is due to [Jenkins CSP changes](https://www.jenkins.io/doc/book/system-administration/security/configuring-content-security-policy/).

You can also use ``--junit-xml=report.xml`` to get an xml report instead. Jenkins can use this file to display better reporting for your tests.

```zsh
pytest test_suite.py --junit-xml=report.xml
```

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Nosetest Reports:</h3>

The ``--report`` option gives you a fancy report after your test suite completes.

```zsh
nosetests test_suite.py --report
```

<img src="https://seleniumbase.github.io/cdn/img/nose_report.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Language Locale Codes</h3>

You can specify a Language Locale Code to customize web pages on supported websites. With SeleniumBase, you can change the web browser's Locale on the command line by doing this:

```zsh
pytest --locale=CODE  # Example: --locale=ru
```

Visit <a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/locale_codes.md"><b>🗾 Locales</b></a> for a full list of codes.

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Changing the default driver version:</h3>

🔵 By default, SeleniumBase will make sure that the major driver version matches the major browser version for Chromium tests. (Eg. If Chrome `117.X` is installed and you have chromedriver `117.X`, then nothing happens, but if you had chromedriver `116.X` instead, then SeleniumBase would download chromedriver `117.X` to match the browser version.)

🎛️ To change this default behavior, you can use:

```zsh
pytest --driver-version=VER
```

The `VER` in `--driver-version=VER` can be:
* A major driver version. Eg. `117`. (milestone)
* An exact driver version. Eg. `117.0.5938.92`.
* ``"browser"`` (exact match on browser version)
* ``"keep"`` (keep using the driver you already have)
* ``"latest"`` / ``"stable"`` (latest stable version)
* ``"previous"`` / ``"latest-1"`` (latest minus one)
* ``"beta"`` (latest beta version)
* ``"dev"`` (latest dev version)
* ``"canary"`` (latest canary version)
* ``"mlatest"`` (latest version for the milestone)

Note that different options could lead to the same result. (Eg. If you have the latest version of a browser for a milestone, then ``"browser"`` and ``"mlatest"`` should give you the same driver if the latest driver version for that milestone matches the browser version.)

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Setting the binary location:</h3>

🔵 By default, SeleniumBase uses the browser binary detected on the System PATH.

🎛️ To change this default behavior, you can use:

```zsh
pytest --binary-location=PATH
```

The `PATH` in `--binary-location=PATH` / `--bl=PATH` can be:
* A relative or exact path to the browser binary.
* `"cft"` as a special option for `Chrome for Testing`.
* `"chs"` as a special option for `Chrome-Headless-Shell`.

Before using the `"cft"` / `"chs"` options, call `sbase get cft` / `sbase get chs` in order to download the specified binaries into the `seleniumbase/drivers` folder. The default version is the latest stable version on https://googlechromelabs.github.io/chrome-for-testing/. You can change that by specifying the arg as a parameter. (Eg. `sbase get cft 131`, `sbase get chs 132`, etc.)

With the `SB()` and `Driver()` formats, the binary location is set via the `binary_location` parameter.

--------

🎛️ To use the special `Chrome for Testing` binary:

```zsh
sbase get cft
```

Then, run scripts with `--cft` / `cft=True`:

```zsh
pytest --cft -n8 --dashboard --html=report.html -v --rs --headless
```

--------

(Note that `--chs` / `chs=True` activates `Chrome-Headless-Shell`)

`Chrome-Headless-Shell` is the fastest version of Chrome, designed specifically for headless automation. (This mode is NOT compatible with UC Mode!)

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Customizing default settings:</h3>

🎛️ An easy way to override [seleniumbase/config/settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) is by using a custom settings file.
Here's the command-line option to add to tests: (See [examples/custom_settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/custom_settings.py))

```zsh
pytest --settings-file=custom_settings.py
```

(Settings include default timeout values, a two-factor auth key, DB credentials, S3 credentials, and other important settings used by tests.)

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Running tests on a remote Selenium Grid:</h3>

🌐 SeleniumBase lets you run tests on remote Selenium Grids such as [BrowserStack](https://www.browserstack.com/automate#)'s Selenium Grid, [Sauce Labs](https://saucelabs.com/products/platform-configurator)'s Selenium Grid, other Grids, and even your own Grid:

🌐 For setting browser desired capabilities while running Selenium remotely, see the ReadMe located here: https://github.com/seleniumbase/SeleniumBase/tree/master/examples/capabilities

Here's how to connect to a BrowserStack Selenium Grid server for running tests:

```zsh
pytest test_demo_site.py --server=USERNAME:KEY@hub.browserstack.com --port=80
```

Here's how to connect to a Sauce Labs Selenium Grid server for running tests:

```zsh
pytest test_demo_site.py --server=USERNAME:KEY@ondemand.us-east-1.saucelabs.com --port=443 --protocol=https
```

🌐 Or you can create your own Selenium Grid for test distribution. ([See this ReadMe for details](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md))

🌐 To use a server on the ``https`` protocol, add ``--protocol=https``: (*Now automatic if the port is 443.*)

```zsh
pytest test_demo_site.py --protocol=https --server=IP_ADDRESS --port=PORT
```

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Using a Proxy Server:</h3>

🌐 If you wish to use a proxy server for your browser tests (Chromium or Firefox), you can add ``--proxy=IP_ADDRESS:PORT`` as an argument on the command line.

```zsh
pytest proxy_test.py --proxy=IP_ADDRESS:PORT
```

🌐 If the proxy server that you wish to use requires authentication, you can do the following (Chromium only):

```zsh
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT
```

🌐 SeleniumBase also supports SOCKS4 and SOCKS5 proxies:

```zsh
pytest proxy_test.py --proxy="socks4://IP_ADDRESS:PORT"

pytest proxy_test.py --proxy="socks5://IP_ADDRESS:PORT"
```

To make things easier, you can add your frequently-used proxies to PROXY_LIST in [proxy_list.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/proxy_list.py), and then use ``--proxy=KEY_FROM_PROXY_LIST`` to use the IP_ADDRESS:PORT of that key.

```zsh
pytest proxy_test.py --proxy=proxy1
```

--------

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Changing the User-Agent:</h3>

🔤 If you wish to change the User-Agent for your browser tests (Chrome and Firefox only), you can add ``--agent="USER-AGENT-STRING"`` as an argument on the command line.

```zsh
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```

<h3><img src="https://seleniumbase.github.io/img/green_logo.png" title="SeleniumBase" width="32" /> Mobile Device Testing:</h3>

📱 Use ``--mobile`` to quickly run your tests using Chrome's mobile device emulator with default values for device metrics (CSS Width, CSS Height, Pixel-Ratio) and a default value set for the user agent. To configure the mobile device metrics, use ``--metrics="CSS_Width,CSS_Height,Pixel_Ratio"`` to set those values. You'll also be able to set the user agent with ``--agent="USER-AGENT-STRING"`` (a default user agent will be used if not specified). To find real values for device metrics, [see this GitHub Gist](https://gist.github.com/sidferreira/3f5fad525e99b395d8bd882ee0fd9d00). For a list of available user agent strings, [check out this page](https://developers.whatismybrowser.com/useragents/explore/).

```zsh
# Run tests using Chrome's mobile device emulator (default settings)
pytest test_swag_labs.py --mobile

# Run mobile tests specifying CSS Width, CSS Height, and Pixel-Ratio
pytest test_swag_labs.py --mobile --metrics="411,731,3"

# Run mobile tests specifying the user agent
pytest test_swag_labs.py --mobile --agent="Mozilla/5.0 (Linux; Android 9; Pixel 3 XL)"
```

--------

<a id="sb_options"></a>
<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> 02. <code>SB()</code> method options</h2>

```python
test=None  # Test Mode: Output, Logging, Continue on failure unless "rtf".
rtf=None  # Shortcut / Duplicate of "raise_test_failure".
raise_test_failure=None  # If "test" mode, raise Exception on 1st failure.
browser=None  # Choose from "chrome", "edge", "firefox", or "safari".
headless=None  # Use the default headless mode for Chromium and Firefox.
headless1=None  # Use Chromium's old headless mode. (Fast, but limited)
headless2=None  # Use Chromium's new headless mode. (Has more features)
locale_code=None  # Set the Language Locale Code for the web browser.
protocol=None  # The Selenium Grid protocol: "http" or "https".
servername=None  # The Selenium Grid server/IP used for tests.
port=None  # The Selenium Grid port used by the test server.
proxy=None  # Use proxy. Format: "SERVER:PORT" or "USER:PASS@SERVER:PORT".
proxy_bypass_list=None  # Skip proxy when using the listed domains.
proxy_pac_url=None  # Use PAC file. (Format: URL or USERNAME:PASSWORD@URL)
multi_proxy=None  # Allow multiple proxies with auth when multi-threaded.
agent=None  # Modify the web browser's User-Agent string.
cap_file=None  # The desired capabilities to use with a Selenium Grid.
cap_string=None  # The desired capabilities to use with a Selenium Grid.
recorder_ext=None  # Enables the SeleniumBase Recorder Chromium extension.
disable_cookies=None  # Disable Cookies on websites. (Pages might break!)
disable_js=None  # Disable JavaScript on websites. (Pages might break!)
disable_csp=None  # Disable the Content Security Policy of websites.
enable_ws=None  # Enable Web Security on Chromium-based browsers.
enable_sync=None  # Enable "Chrome Sync" on websites.
use_auto_ext=None  # Use Chrome's automation extension.
undetectable=None  # Use undetected-chromedriver to evade bot-detection.
uc_cdp_events=None  # Capture CDP events in undetected-chromedriver mode.
uc_subprocess=None  # Use undetected-chromedriver as a subprocess.
log_cdp_events=None  # Capture {"performance": "ALL", "browser": "ALL"}
incognito=None  # Enable Chromium's Incognito mode.
guest_mode=None  # Enable Chromium's Guest mode.
dark_mode=None  # Enable Chromium's Dark mode.
devtools=None  # Open Chromium's DevTools when the browser opens.
remote_debug=None  # Enable Chrome's Debugger on "http://localhost:9222".
enable_3d_apis=None  # Enable WebGL and 3D APIs.
swiftshader=None  # Chrome: --use-gl=angle / --use-angle=swiftshader-webgl
ad_block_on=None  # Block some types of display ads from loading.
host_resolver_rules=None  # Set host-resolver-rules, comma-separated.
block_images=None  # Block images from loading during tests.
do_not_track=None  # Tell websites that you don't want to be tracked.
chromium_arg=None  # "ARG=N,ARG2" (Set Chromium args, ","-separated.)
firefox_arg=None  # "ARG=N,ARG2" (Set Firefox args, comma-separated.)
firefox_pref=None  # SET (Set Firefox PREFERENCE:VALUE set, ","-separated)
user_data_dir=None  # Set the Chrome user data directory to use.
extension_zip=None  # Load a Chrome Extension .zip|.crx, comma-separated.
extension_dir=None  # Load a Chrome Extension directory, comma-separated.
disable_features=None  # "F1,F2" (Disable Chrome features, ","-separated.)
binary_location=None  # Set path of the Chromium browser binary to use.
driver_version=None  # Set the chromedriver or uc_driver version to use.
skip_js_waits=None  # Skip JS Waits (readyState=="complete" and Angular).
wait_for_angularjs=None  # Wait for AngularJS to load after some actions.
use_wire=None  # Use selenium-wire's webdriver over selenium webdriver.
external_pdf=None  # Set Chrome "plugins.always_open_pdf_externally":True.
window_position=None  # Set the browser's starting window position: "X,Y"
window_size=None  # Set the browser's starting window size: "Width,Height"
is_mobile=None  # Use the mobile device emulator while running tests.
mobile=None  # Shortcut / Duplicate of "is_mobile".
device_metrics=None  # Set mobile metrics: "CSSWidth,CSSHeight,PixelRatio"
xvfb=None  # Run tests using the Xvfb virtual display server on Linux OS.
xvfb_metrics=None  # Set Xvfb display size on Linux: "Width,Height".
start_page=None  # The starting URL for the web browser when tests begin.
rec_print=None  # If Recorder is enabled, prints output after tests end.
rec_behave=None  # Like Recorder Mode, but also generates behave-gherkin.
record_sleep=None  # If Recorder enabled, also records self.sleep calls.
data=None  # Extra test data. Access with "self.data" in tests.
var1=None  # Extra test data. Access with "self.var1" in tests.
var2=None  # Extra test data. Access with "self.var2" in tests.
var3=None  # Extra test data. Access with "self.var3" in tests.
variables=None  # DICT (Extra test data. Access with "self.variables")
account=None  # Set account. Access with "self.account" in tests.
environment=None  # Set the test env. Access with "self.env" in tests.
headed=None  # Run tests in headed/GUI mode on Linux, where not default.
maximize=None  # Start tests with the browser window maximized.
disable_ws=None  # Reverse of "enable_ws". (None and False are different)
disable_beforeunload=None  # Disable the "beforeunload" event on Chromium.
settings_file=None  # A file for overriding default SeleniumBase settings.
position=None  # Shortcut / Duplicate of "window_position".
size=None  # Shortcut / Duplicate of "window_size".
uc=None  # Shortcut / Duplicate of "undetectable".
undetected=None  # Shortcut / Duplicate of "undetectable".
uc_cdp=None  # Shortcut / Duplicate of "uc_cdp_events".
uc_sub=None  # Shortcut / Duplicate of "uc_subprocess".
locale=None  # Shortcut / Duplicate of "locale_code".
log_cdp=None  # Shortcut / Duplicate of "log_cdp_events".
ad_block=None  # Shortcut / Duplicate of "ad_block_on".
server=None  # Shortcut / Duplicate of "servername".
guest=None  # Shortcut / Duplicate of "guest_mode".
wire=None  # Shortcut / Duplicate of "use_wire".
pls=None  # Shortcut / Duplicate of "page_load_strategy".
sjw=None  # Shortcut / Duplicate of "skip_js_waits".
wfa=None  # Shortcut / Duplicate of "wait_for_angularjs".
cft=None  # Use "Chrome for Testing"
chs=None  # Use "Chrome-Headless-Shell"
save_screenshot=None  # Save a screenshot at the end of each test.
no_screenshot=None  # No screenshots saved unless tests directly ask it.
page_load_strategy=None  # Set Chrome PLS to "normal", "eager", or "none".
timeout_multiplier=None  # Multiplies the default timeout values.
js_checking_on=None  # Check for JavaScript errors after page loads.
slow=None  # Slow down the automation. Faster than using Demo Mode.
demo=None  # Slow down and visually see test actions as they occur.
demo_sleep=None  # SECONDS (Set wait time after Slow & Demo Mode actions.)
message_duration=None  # SECONDS (The time length for Messenger alerts.)
highlights=None  # Number of highlight animations for Demo Mode actions.
interval=None  # SECONDS (Autoplay interval for SB Slides & Tour steps.)
time_limit=None  # SECONDS (Safely fail tests that exceed the time limit.)
```

Example: [SeleniumBase/examples/raw_robot.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_robot.py)

--------

<a id="driver_options"></a>
<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> 03. <code>Driver()</code> method options</h2>

```python
browser=None  # Choose from "chrome", "edge", "firefox", or "safari".
headless=None  # Use the default headless mode for Chromium and Firefox.
headless1=None  # Use Chromium's old headless mode. (Fast, but limited)
headless2=None  # Use Chromium's new headless mode. (Has more features)
headed=None  # Run tests in headed/GUI mode on Linux, where not default.
locale_code=None  # Set the Language Locale Code for the web browser.
protocol=None  # The Selenium Grid protocol: "http" or "https".
servername=None  # The Selenium Grid server/IP used for tests.
port=None  # The Selenium Grid port used by the test server.
proxy=None  # Use proxy. Format: "SERVER:PORT" or "USER:PASS@SERVER:PORT".
proxy_bypass_list=None  # Skip proxy when using the listed domains.
proxy_pac_url=None  # Use PAC file. (Format: URL or USERNAME:PASSWORD@URL)
multi_proxy=None  # Allow multiple proxies with auth when multi-threaded.
agent=None  # Modify the web browser's User-Agent string.
cap_file=None  # The desired capabilities to use with a Selenium Grid.
cap_string=None  # The desired capabilities to use with a Selenium Grid.
recorder_ext=None  # Enables the SeleniumBase Recorder Chromium extension.
disable_cookies=None  # Disable Cookies on websites. (Pages might break!)
disable_js=None  # Disable JavaScript on websites. (Pages might break!)
disable_csp=None  # Disable the Content Security Policy of websites.
enable_ws=None  # Enable Web Security on Chromium-based browsers.
disable_ws=None  # Reverse of "enable_ws". (None and False are different)
enable_sync=None  # Enable "Chrome Sync" on websites.
use_auto_ext=None  # Use Chrome's automation extension.
undetectable=None  # Use undetected-chromedriver to evade bot-detection.
uc_cdp_events=None  # Capture CDP events in undetected-chromedriver mode.
uc_subprocess=None  # Use undetected-chromedriver as a subprocess.
log_cdp_events=None  # Capture {"performance": "ALL", "browser": "ALL"}
no_sandbox=None  # (DEPRECATED) - "--no-sandbox" is always used now.
disable_gpu=None  # (DEPRECATED) - GPU is disabled if not "swiftshader".
incognito=None  # Enable Chromium's Incognito mode.
guest_mode=None  # Enable Chromium's Guest mode.
dark_mode=None  # Enable Chromium's Dark mode.
devtools=None  # Open Chromium's DevTools when the browser opens.
remote_debug=None  # Enable Chrome's Debugger on "http://localhost:9222".
enable_3d_apis=None  # Enable WebGL and 3D APIs.
swiftshader=None  # Chrome: --use-gl=angle / --use-angle=swiftshader-webgl
ad_block_on=None  # Block some types of display ads from loading.
host_resolver_rules=None  # Set host-resolver-rules, comma-separated.
block_images=None  # Block images from loading during tests.
do_not_track=None  # Tell websites that you don't want to be tracked.
chromium_arg=None  # "ARG=N,ARG2" (Set Chromium args, ","-separated.)
firefox_arg=None  # "ARG=N,ARG2" (Set Firefox args, comma-separated.)
firefox_pref=None  # SET (Set Firefox PREFERENCE:VALUE set, ","-separated)
user_data_dir=None  # Set the Chrome user data directory to use.
extension_zip=None  # Load a Chrome Extension .zip|.crx, comma-separated.
extension_dir=None  # Load a Chrome Extension directory, comma-separated.
disable_features=None  # "F1,F2" (Disable Chrome features, ","-separated.)
binary_location=None  # Set path of the Chromium browser binary to use.
driver_version=None  # Set the chromedriver or uc_driver version to use.
page_load_strategy=None  # Set Chrome PLS to "normal", "eager", or "none".
use_wire=None  # Use selenium-wire's webdriver over selenium webdriver.
external_pdf=None  # Set Chrome "plugins.always_open_pdf_externally":True.
window_position=None  # Set the browser's starting window position: "X,Y"
window_size=None  # Set the browser's starting window size: "Width,Height"
is_mobile=None  # Use the mobile device emulator while running tests.
mobile=None  # Shortcut / Duplicate of "is_mobile".
d_width=None  # Set device width
d_height=None  # Set device height
d_p_r=None  # Set device pixel ratio
position=None  # Shortcut / Duplicate of "window_position".
size=None  # Shortcut / Duplicate of "window_size".
uc=None  # Shortcut / Duplicate of "undetectable".
undetected=None  # Shortcut / Duplicate of "undetectable".
uc_cdp=None  # Shortcut / Duplicate of "uc_cdp_events".
uc_sub=None  # Shortcut / Duplicate of "uc_subprocess".
locale=None  # Shortcut / Duplicate of "locale_code".
log_cdp=None  # Shortcut / Duplicate of "log_cdp_events".
ad_block=None  # Shortcut / Duplicate of "ad_block_on".
server=None  # Shortcut / Duplicate of "servername".
guest=None  # Shortcut / Duplicate of "guest_mode".
wire=None  # Shortcut / Duplicate of "use_wire".
pls=None  # Shortcut / Duplicate of "page_load_strategy".
cft=None  # Use "Chrome for Testing"
chs=None  # Use "Chrome-Headless-Shell"
```

Example: [SeleniumBase/examples/raw_driver_manager.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/raw_driver_manager.py)

--------

<a id="sb_cdp_chrome_options"></a>
<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> 04. <code>sb_cdp.Chrome()</code> method options</h2>

```python
url: Optional[str] = None
user_data_dir: Optional[PathLike] = None
headless: Optional[bool] = False
incognito: Optional[bool] = False
guest: Optional[bool] = False
browser_executable_path: Optional[PathLike] = None
browser_args: Optional[List[str]] = None
xvfb_metrics: Optional[List[str]] = None  # "Width,Height" for Linux
ad_block: Optional[bool] = False
sandbox: Optional[bool] = True
lang: Optional[str] = None  # Set the Language Locale Code
host: Optional[str] = None  # Chrome remote-debugging-host
port: Optional[int] = None  # Chrome remote-debugging-port
xvfb: Optional[int] = None  # Use a special virtual display on Linux
headed: Optional[bool] = None  # Override default Xvfb mode on Linux
expert: Optional[bool] = None  # Open up closed Shadow-root elements
agent: Optional[str] = None  # Set the user-agent string
proxy: Optional[str] = None  # "host:port" or "user:pass@host:port"
tzone: Optional[str] = None  # Eg "America/New_York", "Asia/Kolkata"
geoloc: Optional[list | tuple] = None  # Eg (48.87645, 2.26340)
extension_dir: Optional[str] = None  # Chrome extension directory
platform: Optional[str] = None  # Set the Platform. Eg: "MacIntel"
```

Example: [SeleniumBase/examples/cdp_mode/raw_geolocation.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_geolocation.py)

--------

<a id="activate_cdp_mode_options"></a>
<h2><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> 05. <code>activate_cdp_mode()</code> method options</h2>

```python
url: Optional[str] = None  # The URL to navigate to
lang: Optional[str] = None  # Set the Language Locale Code
agent: Optional[str] = None  # Set the user-agent string
tzone: Optional[str] = None  # Eg "America/New_York", "Asia/Kolkata"
geoloc: Optional[list | tuple] = None  # Eg (48.87645, 2.26340)
platform: Optional[str] = None  # Set the Platform. Eg: "MacIntel"
```

Example: [SeleniumBase/examples/cdp_mode/raw_geolocation_sb.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_geolocation_sb.py)

Note that if CDP Mode is already active, the options above can also be used when calling `sb.cdp.open()`. (The `url` arg is required in this case.)

--------

[<img src="https://seleniumbase.github.io/cdn/img/fancy_logo_14.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase)
