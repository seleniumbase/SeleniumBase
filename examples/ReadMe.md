<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) Example Tests:

<p align="left"><a align="center" href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_demo_site.py"><img align="center" src="https://seleniumbase.github.io/cdn/img/sb_demo_page.png" alt="SeleniumBase Demo Page" width="420" /></a></p>

* <b>SeleniumBase</b> tests are run with <b>pytest</b>.
* Chrome is the default browser if not specified.
* Tests are structured using [20 unique syntax formats](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/syntax_formats.md).
* Logs from test failures are saved to ``./latest_logs/``.
* Tests can be run with [multiple command-line options](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md).
* Examples can be found in: **[SeleniumBase/examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)**.

(NOTE: Some example tests fail on purpose to demonstrate [logging features](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/ReadMe.md).)

--------

<h3><img src="https://seleniumbase.github.io/img/logo7.png" title="SeleniumBase" width="32" /> Example tests with run commands to help you get started:</h3>

--------

Run an [example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_demo_site.py): (Default option: ``--browser=chrome``)

```bash
pytest test_demo_site.py
```

<img src="https://seleniumbase.github.io/cdn/gif/demo_page_4.gif" title="SeleniumBase Demo Page" /><br />

--------

Run an example test in Firefox:

```bash
pytest my_first_test.py --browser=firefox
```

--------

Run an example test in Demo Mode: (highlight assertions)

```bash
pytest test_swag_labs.py --demo
```

<img src="https://seleniumbase.github.io/cdn/gif/swag_demo_3.gif" /><br />

--------

Run [test_coffee_cart.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_coffee_cart.py) to test the [Coffee Cart](https://seleniumbase.io/coffee/) app:

```bash
pytest test_coffee_cart.py --demo
```

<img src="https://seleniumbase.github.io/cdn/gif/coffee_cart.gif" title="SeleniumBase Coffee App Example" alt="SeleniumBase Example" title="SeleniumBase Coffee App Example" />

--------

Run a [Wordle-solver example](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/wordle_test.py):

```bash
pytest wordle_test.py
```

<img src="https://seleniumbase.github.io/cdn/gif/wordle.gif" title="Solving Wordle with SeleniumBase" /><br />

--------

Run an example test in Headless Mode: (invisible browser)

```bash
pytest my_first_test.py --headless
```

--------

Run an [example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_swag_labs.py) using Chrome's mobile device emulator: (default settings)

```bash
pytest test_swag_labs.py --mobile
```

<img src="https://seleniumbase.github.io/cdn/gif/swag_mobile_2.gif" title="SeleniumBase Mobile Mode" /><br />

--------

Run another [example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_xkcd.py) in Demo Mode: (highlight assertions)

```bash
pytest test_xkcd.py --demo
```

<img src="https://seleniumbase.github.io/cdn/gif/xkcd_vid.gif" title="SeleniumBase Demo Mode" /><br />

--------

Run a [test suite](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_suite.py) with verbose output: (see more details)

```bash
pytest test_suite.py -v
```

--------

Run a test suite multi-threaded using [n] threads:

```bash
pytest test_suite.py -n=4
```

--------

Run a [parameterized test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/parameterized_test.py): (Generates multiple tests from one)

```bash
pytest parameterized_test.py -v
```

--------

Run a test suite and generate a SeleniumBase Dashboard:

```bash
pytest test_suite.py --dashboard
```

--------

Run a test suite and generate a pytest report:

```bash
pytest test_suite.py --html=report.html
```

--------

Run a [failing test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_fail.py): (See the ``latest_logs/`` folder for logs and screenshots)

```bash
pytest test_fail.py
```

--------

Run a failing test with Debug-mode enabled: (``pdb`` activates on failures)

```bash
pytest test_fail.py --pdb -s
```

--------

Run a test suite that demonstrates the use of pytest markers:

```bash
pytest -m marker_test_suite -v
```

--------

Run a test suite that reuses the browser session between tests:

```bash
pytest test_suite.py --reuse-session
```

--------

Run an [example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/rate_limiting_test.py) demonstrating the ``rate_limited`` Python decorator:

```bash
pytest rate_limiting_test.py
```

--------

Run an [example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/upload_file_test.py) that demonstrates how to upload a file to a website:

```bash
pytest upload_file_test.py
```

--------

Try the new SeleniumBase Commander! A GUI for pytest:

```bash
sbase gui
```

<img src="https://seleniumbase.github.io/cdn/img/sbase_commander.png" title="SeleniumBase Commander / GUI for pytest" width="520" /><br />

--------

<b>SeleniumBase tests can also be run with ``nosetests``:</b>

Run an example test with nosetests:

```bash
nosetests my_first_test.py
```

--------

Run an example test suite and generate a nosetest report:

```bash
nosetests test_suite.py --report --show-report
```

--------

Run an example test using a nosetest configuration file:

```bash
nosetests my_first_test.py --config=example_config.cfg
```

--------

For more advanced run commands, such as using a proxy server, see [../help_docs/customizing_test_runs.md](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md)

--------

If you just need to perform some quick website verification on various devices, you can use the <a href="https://seleniumbase.io/devices/">SeleniumBase Device Farm</a>. Just plug in a website URL, and it will display how the website looks on four different devices:

<a href="https://seleniumbase.io/devices/?url=github.com"><img src="https://seleniumbase.github.io/cdn/img/github_demo2.png" width="540" title="SeleniumBase Mobile Mode" /></a><br />

--------

To make things easier, here's a simple GUI program that allows you to run a few example tests by pressing a button:

```bash
python gui_test_runner.py
```

<img src="https://seleniumbase.github.io/cdn/img/gui_test_runner.png" title="GUI Test Runner" width="320" />

(The newer [SeleniumBase Commander](https://seleniumbase.io/help_docs/commander/) improves on that.)

--------

🎖️ To launch the SeleniumBase Commander GUI for pytest:

```bash
sbase gui
```

<img src="https://seleniumbase.github.io/cdn/img/sbase_commander_wide.png" title="SeleniumBase Commander" width="600">

--------

<img src="https://seleniumbase.github.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="320" />

<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/tested%20with-SeleniumBase-04C38E.svg" alt="Tested with SeleniumBase" /></a>
