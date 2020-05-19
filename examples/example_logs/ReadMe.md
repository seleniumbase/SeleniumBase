<a align="center" href="https://github.com/seleniumbase/SeleniumBase/"><img align="center" src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_sb.png" title="SeleniumBase" width="290" /></a>

### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Logging, Screenshots, and Reports:

Log files in [SeleniumBase/examples/example_logs](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/example_logs) were generated when [test_fail.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_fail.py) ran and failed. During test failures, logs and screenshots get saved to the ``latest_logs/`` folder. If ``--archive-logs`` is set, test logs will get archived to the ``archived_logs/`` folder.

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

--------

<b>In addition to logging, you can also generate test reports:</b>

Reports are most useful when running large test suites. Pytest and Nosetest reports are handled differently.

### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Pytest Reports:

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/pytest_report_3c.png" alt="Example Pytest Report" title="Example Pytest Report" width="520" />

### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Nosetest Reports:

The ``--report`` option gives you a fancy report after your test suite completes. (Requires ``--with-testing_base`` to also be set when ``--report`` is used because it's part of that plugin.)

```bash
nosetests test_suite.py --report --browser=chrome
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" alt="Example Nosetest Report" title="Example Nosetest Report" width="320" />

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)
