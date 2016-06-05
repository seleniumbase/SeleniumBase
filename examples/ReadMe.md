## Running SeleniumBase Scripts

Here are some example run commands for the files in this folder and what they do:
(Note: You can replace ``nosetests`` with ``py.test`` for any of these.)

Run the example test in Firefox
```bash
nosetests my_first_test.py --with-selenium --browser=firefox
```

Run the example test in Chrome
```bash
nosetests my_first_test.py --with-selenium --browser=chrome
```

Run the example test in PhantomJS
```bash
nosetests my_first_test.py --with-selenium --browser=phantomjs
```

Run the example test suite in Firefox and generate an html report (nosetests-only)
```bash
nosetests my_test_suite.py --with-selenium --browser=firefox --with-testing_base --report
```

Run the example test suite in Chrome and generate an html report (nosetests-only)
```bash
nosetests my_test_suite.py --with-selenium --browser=chrome --with-testing_base --report
```

Run the example test suite in PhantomJS and generate an html report (nosetests-only)
```bash
nosetests my_test_suite.py --with-selenium --browser=phantomjs --with-testing_base --report
```

Run a test with all the configuration specifed by a config file
```bash
nosetests my_first_test.py --config=example_config.cfg
```

Example test with the use of python decorators
```bash
nosetests rate_limiting_test.py
```

Run the example test slowly
```bash
nosetests my_first_test.py --browser=firefox --with-selenium --demo_mode
```

Run a failing test with pdb mode enabled (If a test failure occurs, test enters pdb mode)
```bash
nosetests test_fail.py --browser=firefox --with-selenium --pdb --pdb-failures
```

Run a failing test with logging
```bash
nosetests test_fail.py --browser=firefox --with-selenium --with-testing_base --with-basic_test_info --with-page_source --with-screen_shots
```

If you run scripts with logging enabled, you’ll see two folders appear: “logs” and “archived logs”. The “logs” folder will contain log files from the most recent test run, but logs will only be created if the test run is failing. Afterwards, logs from the “logs” folder will get pushed to the “archived_logs” folder.

You may also see .pyc files appear as you run tests. That’s compiled bytecode, which is a natural result of running Python code.
