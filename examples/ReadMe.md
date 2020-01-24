[<img src="https://cdn2.hubspot.net/hubfs/100006/images/sb_logo_dh.png" title="SeleniumBase" align="center" height="155">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

## Running Example Tests

SeleniumBase tests can be run with either **``pytest``** or **``nosetests``**, but using pytest is strongly recommended. Chrome is the default browser if not specified.

During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)

(NOTE: Many tests in this folder fail on purpose to demonstrate the built-in logging, screenshots, and reporting features.)

**Here are some example run commands to help get you started:**

Run an example test in Chrome: (Default: ``--browser=chrome``)
```bash
pytest my_first_test.py
```

Run an example test in Firefox:
```bash
pytest my_first_test.py --browser=firefox
```

Run an example test in Demo Mode: (highlight assertions)
```bash
pytest my_first_test.py --demo
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/my_first_test_gif.gif" title="SeleniumBase"><br />

Run an example test in Headless Mode: (invisible browser)
```bash
pytest my_first_test.py --headless
```

Run tests with verbose output: (includes more details)
```bash
pytest test_suite.py -v
```

Run tests multi-threaded using [n] threads:
```bash
pytest test_suite.py -v -n=4
```

Run a parameterized test: (Generates multiple tests from one)
```bash
pytest parameterized_test.py -v
```

Run a test suite and generate a pytest report: (pytest-only)
```bash
pytest test_suite.py -v --html=report.html
```

Run a failing test: (See the ``latest_logs/`` folder for logs and screenshots)
```bash
pytest test_fail.py
```

Run an example test using Chrome's mobile device emulator: (default settings)
```bash
pytest test_swag_labs.py --mobile
```

Run a failing test with Debug-mode enabled: (``pdb`` activates on failures)
```bash
pytest test_fail.py --pdb -s
```

Run an example test suite that demonstrates the use of pytest markers:
```bash
pytest -m marker_test_suite -v
```

Run an example test suite that reuses the browser session between tests:
```bash
pytest test_suite.py --reuse-session -v
```

Run an example test demonstrating the ``rate_limited`` Python decorator:
```bash
pytest rate_limiting_test.py
```

Run an example test that demonstrates how to upload a file to a website:
```bash
pytest upload_file_test.py
```

Run an example test suite and generate a nosetest report: (nosetests-only)
```bash
nosetests test_suite.py --report --show-report
```

Run an example test using a nosetest configuration file: (nosetests-only)
```bash
nosetests my_first_test.py --config=example_config.cfg
```

For more advanced run commands, such as using a proxy server, see [../help_docs/customizing_test_runs.md](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md)

--------

To make things easier, here's a simple GUI program that allows you to run a few example tests by pressing a button:

```bash
python gui_test_runner.py
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/gui_test_runner_py.png" title="GUI Test Runner" height="260">

--------

[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_e.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
