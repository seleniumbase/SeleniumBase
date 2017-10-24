## Running SeleniumBase Scripts

(NOTE: If you didn't install SeleniumBase properly, these scripts won't work. Installation steps include "``pip install seleniumbase``" and/or "``python setup.py install``" from the top-level directory.)

To makes things easier, here's a simple GUI program that allows you to kick off a few example scripts by pressing a button:

```bash
python gui_test_runner.py
```

(NOTE: With the exception of [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py), which should pass, many other tests in this folder fail on purpose to demonstrate features such as screenshots on failure, exception logging, and test reports.)

(NOTE: You can interchange ``nosetests`` with ``pytest`` in most of these examples.)

![](http://cdn2.hubspot.net/hubfs/100006/images/GUI_Test_Runner_5.png "GUI Test Runner")

If you run scripts with logging enabled, (using ``--with-testing_base``), you’ll see two folders appear: “latest_logs” and “archived_logs”. The “latest_logs” folder will contain log files from the most recent test run, but logs will only be created if the test run is failing. Afterwards, logs from the “latest_logs” folder will get pushed to the “archived_logs” folder if you have have the ``ARCHIVE_EXISTING_LOGS`` feature enabled in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py). Make sure to run ``python setup.py install`` for your changes to take effect if you make any changes to that file.

**For running scripts the usual way, here are some of the example run commands:**

Run the example test in Chrome:
```bash
pytest my_first_test.py --browser=chrome
```

Run the example test in Firefox:
```bash
pytest my_first_test.py --browser=firefox
```

Run the example test in PhantomJS:
```bash
pytest my_first_test.py --browser=phantomjs
```

Run the example test in Demo Mode (runs slower and adds highlights):
```bash
pytest my_first_test.py --browser=chrome --demo_mode
```

Run the example test suite in Chrome and generate an html report: (nosetests-only)
```bash
nosetests my_test_suite.py --with-selenium --browser=chrome --with-testing_base --report
```

Run the example test suite in Firefox and generate an html report: (nosetests-only)
```bash
nosetests my_test_suite.py --with-selenium --browser=firefox --with-testing_base --report
```

Run the example test suite in PhantomJS and generate an html report: (nosetests-only)
```bash
nosetests my_test_suite.py --with-selenium --browser=phantomjs --with-testing_base --report
```

Run a test with configuration specifed by a config file:
```bash
nosetests my_first_test.py --config=example_config.cfg
```

Run a test demonstrating the use of Python decorators available:
```bash
nosetests rate_limiting_test.py
```

Run a failing test with pdb mode enabled: (If a test failure occurs, test enters pdb mode)
```bash
nosetests test_fail.py --browser=chrome --with-selenium --pdb --pdb-failures
```

Run a failing test with logging:
```bash
pytest test_fail.py --browser=chrome --with-testing_base --with-basic_test_info --with-page_source --with-screen_shots
```

(NOTE: If you see any ``*.pyc`` files appear as you run tests, that's perfectly normal. Compiled bytecode is a natural result of running Python code.)
