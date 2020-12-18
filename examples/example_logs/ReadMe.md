<a align="center" href="https://github.com/seleniumbase/SeleniumBase/"><img align="center" src="https://seleniumbase.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="320" /></a>

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Logging, Dashboards, and Reports:</h3>

Log files in [SeleniumBase/examples/example_logs](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/example_logs) were generated when [test_fail.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_fail.py) ran and failed. During test failures, logs and screenshots from the latest run will get saved to the ``latest_logs/`` folder. If ``--archive-logs`` is set, test logs will get archived to the ``archived_logs/`` folder (otherwise they will be cleaned out when the next test run begins).

```bash
pytest test_fail.py --browser=chrome

nosetests test_fail.py --browser=firefox
```

<b>Examples of expected log files generated during failures:</b>
<ul>
<li><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/basic_test_info.txt">basic_test_info.txt</a></li>
<li><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/page_source.html">page_source.html</a></li>
<li><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/screenshot.png">screenshot.png</a></li>
</ul>

<b>In addition to log files, you can also generate a dashboard and test reports.</b>

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> The SeleniumBase Dashboard:</h3>

The ``--dashboard`` option for pytest generates a SeleniumBase Dashboard located at ``dashboard.html``, which updates automatically as tests run and produce results.

<img src="https://seleniumbase.io/cdn/img/dashboard_1.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="360" />

Additionally, you can host your own SeleniumBase Dashboard Server on a port of your choice. Here's an example of that using Python 3's ``http.server``:

```bash
python -m http.server 1948
```

Now you can navigate to ``http://localhost:1948/dashboard.html`` in order to view the served dashboard from a web browser. (Be sure to run that command in the same directory where you ran your tests.)

Here's a full example of what the SeleniumBase Dashboard may look like:

```bash
pytest test_suite.py --dashboard --rs --headless
```

<img src="https://seleniumbase.io/cdn/img/dashboard_2.png" alt="The SeleniumBase Dashboard" title="The SeleniumBase Dashboard" width="480" />

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Pytest Reports:</h3>

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```

<img src="https://seleniumbase.io/cdn/img/html_report.png" alt="Example Pytest Report" title="Example Pytest Report" width="520" />

If viewing pytest html reports in [Jenkins](https://www.jenkins.io/), you may need to [configure Jenkins settings](https://stackoverflow.com/a/46197356) for the html to render correctly. This is due to [Jenkins CSP changes](https://www.jenkins.io/doc/book/system-administration/security/configuring-content-security-policy/).

--------

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Nosetest Reports:</h3>

The ``--report`` option gives you a fancy report after your test suite completes.

```bash
nosetests test_suite.py --report --browser=chrome
```

<img src="https://seleniumbase.io/cdn/img/nose_report.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(NOTE: You can add ``--show-report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show-report`` when running tests locally because it pauses the test run.)

--------

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.io/img/sb_logo_7.png" alt="SeleniumBase" width="240" /></a></div>
