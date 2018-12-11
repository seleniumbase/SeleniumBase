#### Logging, Screenshots, and Reports examples

Log files in [example_logs/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/example_logs) were generated when [test_fail.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_fail.py) ran and failed. By default, logs are saved to ``latest_logs/``. If ARCHIVE_EXISTING_LOGS is set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), past logs get saved to ``archived_logs/``.

```bash
pytest test_fail.py --browser=chrome

nosetests test_fail.py --browser=firefox
```

**Expected log files generated during failures:**
* [basic_test_info.txt](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/basic_test_info.txt)
* [page_source.html](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/page_source.html)
* [screenshot.png](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/screenshot.png)

---
**In addition to logging, you can also generate test reports:**

Reports are most useful when running large test suites. Pytest and Nosetest reports are handled differently.

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest test_suite.py --html=report.html
```
![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes. (Requires ``--with-testing_base`` to also be set when ``--report`` is used because it's part of that plugin.)

```bash
nosetests test_suite.py --report --browser=chrome
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" title="Example Nosetest Report" height="420">

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)