<p align="center"><a align="center" href="https://github.com/seleniumbase/SeleniumBase/blob/master/README.md"><img align="center" src="https://cdn2.hubspot.net/hubfs/100006/images/SeleniumBaseText_F.png" alt="SeleniumBase" width="290" /></a></p>

<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Running Example Tests:</h2>

SeleniumBase tests are run with **``pytest``**. Chrome is the default browser if not specifed. During test failures, logs and screenshots from the latest run are saved to the ``latest_logs/`` folder.

Example tests are located in <b>[SeleniumBase/examples](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)</b>.

(NOTE: Some example tests fail on purpose to demonstrate [logging features](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md).)

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
<img src="https://cdn2.hubspot.net/hubfs/100006/images/my_first_test_gif.gif" title="SeleniumBase Demo Mode" /><br />

Run a different example in Demo Mode:
```bash
pytest test_swag_labs.py --demo
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/swag_labs_gif.gif" /><br />

Run an example test in Headless Mode: (invisible browser)
```bash
pytest my_first_test.py --headless
```

Run an example test using Chrome's mobile device emulator: (default settings)
```bash
pytest test_swag_labs.py --mobile
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/swag_mobile.gif" title="SeleniumBase Mobile Mode" /><br />

Run tests with verbose output: (includes more details)
```bash
pytest test_suite.py -v
```

Run a test on the Demo Site to try many SeleniumBase methods:
```bash
pytest test_demo_site.py
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/demo_page.gif" title="SeleniumBase Mobile Mode" /><br />

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

--------

#### SeleniumBase tests can also be run with ``nosetests``:

Run an example test with nosetests:
```bash
nosetests my_first_test.py
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
<img src="https://cdn2.hubspot.net/hubfs/100006/images/gui_test_runner_py.png" title="GUI Test Runner" width="320" />

--------

<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_sb8.png" title="SeleniumBase" width="290" />

<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/tested%20with-SeleniumBase-04C38E.svg" alt="Tested with SeleniumBase" /></a>
