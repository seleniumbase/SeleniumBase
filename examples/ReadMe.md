[<img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_logo_f2.png" title="SeleniumBase" align="center" height="120">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

## Running Tests

To run tests, make sure you've already installed SeleniumBase using ``pip install seleniumbase`` OR ``pip install -r requirements.txt`` + ``python setup.py install`` from the top-level directory.

You can interchange **pytest** with **nosetests**, but using pytest is strongly recommended because developers stopped supporting nosetests. Chrome is the default browser if not specified.

During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)

(NOTE: Many tests in this folder fail on purpose to demonstrate the built-in logging, screenshots, and reporting features.)

**Here are some example run commands to help get you started:**

Run an example test in Chrome (``--browser=chrome`` is the default):
```bash
pytest my_first_test.py
```

Run an example test in Firefox:
```bash
pytest my_first_test.py --browser=firefox
```

Run an example test in Demo Mode (highlights page objects being acted on):
```bash
pytest my_first_test.py --demo_mode
```

Run an example test demonstrating parameterization:
```bash
pytest parameterized_test.py
```

Run an example test suite and generate an pytest report: (pytest-only)
```bash
pytest test_suite.py --html=report.html
```

Run an example test suite and generate a nosetest report: (nosetests-only)
```bash
nosetests test_suite.py --report --show_report
```

Run an example test using a nosetest configuration file: (nosetests-only)
```bash
nosetests my_first_test.py --config=example_config.cfg
```

Run a test demonstrating the use of SeleniumBase Python decorators available:
```bash
pytest rate_limiting_test.py
```

Run a failing test: (See the ``latest_logs/`` folder afterwards for logs and screenshots)
```bash
pytest test_fail.py
```

Run a failing test with Debugging-mode enabled: (If a test failure occurs, pdb activates)
```bash
pytest test_fail.py --pdb -s
```

Run an example test suite that demonstrates the use of pytest markers:
```bash
pytest -v -m marker_test_suite
```

Run a test that demonstrates how to upload a file to a website:
```bash
pytest upload_file_test.py
```

For more advanced run commands, such as using a proxy server, see [../help_docs/customizing_test_runs.md](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md)

--------

To make things easier, here's a simple GUI program that allows you to run a few example tests by pressing a button:

```bash
python gui_test_runner.py
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/gui_test_runner_py.png" title="GUI Test Runner" height="260">
