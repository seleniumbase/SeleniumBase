## Running SeleniumBase Scripts

To run tests, make sure you've already installed SeleniumBase using ``pip install seleniumbase`` OR ``pip install -r requirements.txt`` + ``python setup.py develop`` from the top-level directory.

You can interchange **pytest** with **nosetests**, but using pytest is strongly recommended because developers stopped supporting nosetests. Chrome is the default browser if not specified.

During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)

(NOTE: Many tests in this folder fail on purpose to demonstrate the built-in logging, screenshots, and reporting features.)

**Here are some example run commands to help get you started:**

Run the example test in Chrome:
```bash
pytest my_first_test.py --browser=chrome
```

Run the example test in Firefox:
```bash
pytest my_first_test.py --browser=firefox
```

Run the example test in Demo Mode (highlights page objects being acted on):
```bash
pytest my_first_test.py --browser=chrome --demo_mode
```

Run the example test suite and generate an pytest report: (pytest-only)
```bash
pytest basic_script.py --html=report.html
```

Run the example test suite and generate a nosetest report: (nosetests-only)
```bash
nosetests my_test_suite.py --report --show_report
```

Run a test using a nosetest configuration file: (nosetests-only)
```bash
nosetests my_first_test.py --config=example_config.cfg
```

Run a test demonstrating the use of SeleniumBase Python decorators available:
```bash
pytest rate_limiting_test.py
```

Run a failing test: (See the ``latest_logs/`` folder afterwards for logs and screenshots)
```bash
pytest test_fail.py --browser=chrome
```

Run a failing test with Debugging-mode enabled: (If a test failure occurs, pdb activates)
```bash
pytest test_fail.py --browser=chrome --pdb --pdb-failures -s
```

For more advanced run commands, such as using a proxy server,  see [../help_docs/customizing_test_runs.md](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md)

--------

To makes things easier, here's a simple GUI program that allows you to kick off a few example scripts by pressing a button:

```bash
python gui_test_runner.py
```

<img src="https://cdn2.hubspot.net/hubfs/100006/images/The_GUI_Runner.png" title="GUI Test Runner" height="400">

(NOTE: If you see any ``*.pyc`` files appear as you run tests, that's perfectly normal. Compiled bytecode is a natural result of running Python code.)
