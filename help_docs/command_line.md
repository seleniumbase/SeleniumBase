### The Command Line Interface

In addition to [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), which allows you to customize the test framework, SeleniumBase gives you the flexibility to customize & control test runs from the command line:

* Set your browser there (default = Chrome)
* Change the automation speed (with Demo Mode)
* Choose betweeen pytest & nose unittest runners
* Specify what to log and where to store logs
* Choose additional variables to pass into tests
* Choose whether to enter Debug Mode on failures
* Choose a database to save results to
* Choose a Selenium Grid to connect to

...and more!

**Examples:** (These are run from the **[examples](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)** folder.):

```bash
pytest my_first_test.py --browser=chrome

nosetests my_first_test.py --with-selenium --demo_mode --browser=firefox
```
(<i>The Selenium plugin, ``--with-selenium``, is enabled by default when using pytest to run test classes that inherit the [BaseCase](#seleniumbase_basic_usage) class, thanks to [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini). You can do the same for nosetests by adding ``with-selenium=1`` under ``[nosetests]`` in a [setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/setup.cfg) file located in the folder where you call nosetests.</i>)

**Here's how to run the example script on various web browsers by using nosetests:**

(NOTE: You can interchange **nosetests** with **pytest**.)

```bash
cd examples/

nosetests my_first_test.py --with-selenium --browser=chrome

nosetests my_first_test.py --with-selenium --browser=firefox

nosetests my_first_test.py --with-selenium --browser=phantomjs
```
After the test completes, in the console output you'll see a dot (``.``) on a new line, representing a passing test. (On test failures you'll see an ``F`` instead, and on test errors you'll see an ``E``). It looks more like a moving progress bar when you're running a ton of unit tests side by side. This is part of nosetests. After all tests complete (in this case there is only one), you'll see the "``Ran 1 test in ...``" line, followed by an "``OK``" if all nosetests passed. The ``--with-selenium`` option is required for running GUI tests with nosetests (not needed when using pytest). If no browser is specified, Chrome will become the default. The ``-s`` option is optional, and that makes sure that any standard output is printed immediately on the command line when tests have print statements in them, which makes debugging much easier.

**Here's how to run the example script using pytest**:

```bash
cd examples/

pytest my_first_test.py --browser=firefox

pytest my_first_test.py --browser=chrome

pytest my_first_test.py --browser=phantomjs
```
(NOTE: If you're using **pytest** instead of nosetests for running tests outside of the SeleniumBase repo, **you'll need a copy of [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini) at the base of the new folder structure**, already provided here.

**Example tests using Logging**:
```bash
pytest my_test_suite.py --with-testing_base --browser=chrome
```
(NOTE: The ``--with-testing_base`` plugin gives you full logging on test failures, which saves screenshots, page source, and basic test info into the logs folder.)

**Demo Mode:**

If any test is moving too fast for your eyes to see what's going on, you can run it in **Demo Mode** by adding ``--demo_mode`` on the command line, which pauses the browser briefly between actions, and highlights page elements being acted on:

```bash
nosetests my_first_test.py --with-selenium --browser=chrome --demo_mode
```

You can override the default wait time by either updating [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) or by using ``--demo_sleep={NUM}`` when using Demo Mode. (NOTE: If you use ``--demo_sleep={NUM}`` without using ``--demo_mode``, nothing will happen.)

If you ever make any changes to your local copy of ``settings.py``, you may need to run ``python setup.py install`` for those changes to take effect.

```bash
nosetests my_first_test.py --with-selenium --browser=chrome --demo_mode --demo_sleep=1.2
```

**You can also use the following in your scripts to slow down the tests:**
```python
import time; time.sleep(5)  # sleep for 5 seconds (add this after the line you want to pause on)
import ipdb; ipdb.set_trace()  # waits for your command. n = next line of current method, c = continue, s = step / next executed line (will jump)
```

(NOTE: If you're using pytest instead of nosetests and you want to use ipdb in your script for debugging purposes, you'll either need to add ``--capture=no`` on the command line, or use ``import pytest; pytest.set_trace()`` instead of using ipdb. More info on that [here](http://stackoverflow.com/questions/2678792/can-i-debug-with-python-debugger-when-using-py-test-somehow).)

You may also want to have your test sleep in other situations where you need to have your test wait for something. If you know what you're waiting for, you should be specific by using a command that waits for something specific to happen.

**If you need to debug things on the fly (in case of errors), use this:**

```bash
nosetests my_first_test.py --browser=chrome --with-selenium --pdb --pdb-failures -s
```

The above code (with --pdb) will leave your browser window open in case there's a failure, which is possible if the web pages from the example change the data that's displayed on the page. (ipdb commands: 'c', 's', 'n' => continue, step, next). You may need the ``-s`` in order to see all console output.

**Here are some other useful nosetest arguments for appending to your run commands:**

```bash
--logging-level=INFO  # Hide DEBUG messages, which can be overwhelming.
-x  # Stop running the tests after the first failure is reached.
-v  # Prints the full test name rather than a dot for each test.
--with-id  # If -v is also used, will number the tests for easy counting.
```

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest my_test_suite.py --with-selenium --html=report.html
```
![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes. (Requires ``--with-testing_base`` to also be set when ``--report`` is used because it's part of that plugin.)

```bash
nosetests my_test_suite.py --with-selenium --with-testing_base --report
```
![](http://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png "Example Nosetest Report")

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)