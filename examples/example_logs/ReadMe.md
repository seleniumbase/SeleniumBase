<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) Logs, The Dashboard, and Reports:

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=XpuJCjJhJwQ"><img src="http://img.youtube.com/vi/XpuJCjJhJwQ/0.jpg" title="SeleniumBase on YouTube" width="285" /></a>
<!-- GitHub Only --><p>(<b><a href="https://www.youtube.com/watch?v=XpuJCjJhJwQ">The Dashboard Tutorial on YouTube</a></b>)</p>

🔵 During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. If ``--archive-logs`` is specified (or if ARCHIVE_EXISTING_LOGS is set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py)), test logs will also get archived to the ``archived_logs/`` folder. Otherwise, the log files will be cleaned out when the next test run begins (by default).

```bash
pytest test_fail.py
```

(Log files in [SeleniumBase/examples/example_logs](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/example_logs) were generated when [test_fail.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_fail.py) ran and failed.)

<b>Examples of expected log files generated during failures:</b>
<ul>
<li><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/basic_test_info.txt">basic_test_info.txt</a></li>
<li><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/page_source.html">page_source.html</a></li>
<li><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/screenshot.png">screenshot.png</a></li>
</ul>

<b>In addition to log files, you can also generate dashboards and test reports.</b>

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> The SeleniumBase Dashboard:</h3>

🔵 The ``--dashboard`` option for pytest generates a SeleniumBase Dashboard located at ``dashboard.html``, which updates automatically as tests run and produce results. Example:

```bash
pytest --dashboard --rs --headless
```

<img src="https://seleniumbase.github.io/cdn/img/dashboard_1.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="360" />

🔵 Additionally, you can host your own SeleniumBase Dashboard Server on a port of your choice. Here's an example of that using Python 3's ``http.server``:

```bash
python -m http.server 1948
```

🔵 Now you can navigate to ``http://localhost:1948/dashboard.html`` in order to view the dashboard as a web app. This requires two different terminal windows: one for running the server, and another for running the tests, which should be run from the same directory. (Use ``CTRL+C`` to stop the http server.)

🔵 Here's a full example of what the SeleniumBase Dashboard may look like:

```bash
pytest test_suite.py --dashboard --rs --headless
```

<img src="https://seleniumbase.github.io/cdn/img/dashboard_2.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="480" />

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Pytest Reports:</h3>

🔵 Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```

<img src="https://seleniumbase.github.io/cdn/img/html_report.png" alt="Example Pytest Report" title="Example Pytest Report" width="520" />

🔵 When combining pytest html reports with SeleniumBase Dashboard usage, the pie chart from the Dashboard will get added to the html report. Additionally, if you set the html report URL to be the same as the Dashboard URL when also using the dashboard, (example: ``--dashboard --html=dashboard.html``), then the Dashboard will become an advanced html report when all the tests complete.

🔵 Here's an example of an upgraded html report:

```bash
pytest test_suite.py --dashboard --html=report.html
```

<img src="https://seleniumbase.github.io/cdn/img/dash_report.png" alt="Dashboard Pytest HTML Report" title="Dashboard Pytest HTML Report" width="520" />

--------

If viewing ``pytest-html`` reports in [Jenkins](https://www.jenkins.io/), you may need to [configure Jenkins settings](https://stackoverflow.com/a/46197356) for the HTML to render correctly. This is due to [Jenkins CSP changes](https://www.jenkins.io/doc/book/security/configuring-content-security-policy/). That setting can be changed from ``Manage Jenkins`` > ``Script Console`` by running:

```
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")
```

--------

You can also use ``--junit-xml=report.xml`` to get an xml report instead. Jenkins can use this file to display better reporting for your tests.

```bash
pytest test_suite.py --junit-xml=report.xml
```

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Nosetest Reports:</h3>

The ``nosetests`` ``--report`` option gives you a fancy report after your tests complete.

```bash
nosetests test_suite.py --report
```

<img src="https://seleniumbase.github.io/cdn/img/nose_report.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(NOTE: You can add ``--show-report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show-report`` when running tests locally because it pauses the test run.)

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> 🐝⚪ Behave Dashboard & Reports:</h3>

(The [behave_bdd/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/behave_bdd) folder can be found in the [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) folder.)

```bash
behave behave_bdd/features/ -D dashboard -D headless
```

<img src="https://seleniumbase.github.io/cdn/img/sb_behave_dashboard.png" title="SeleniumBase" width="600">

You can also use ``--junit`` to get ``.xml`` reports for each Behave feature. Jenkins can use these files to display better reporting for your tests.

```bash
behave behave_bdd/features/ --junit -D rs -D headless
```

--------

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/img/sb_logo_10.png" alt="SeleniumBase" width="240" /></a></div>
