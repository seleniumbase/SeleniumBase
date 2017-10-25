### Logging & Reports Tutorial

The log files you see in this folder were generated when [test_fail.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_fail.py) ran and failed with logging turned on. (Include ``--with-testing_base`` on the command line in your test runs.) By default, a folder named ``latest_logs/`` will appear in the location where you ran the tests. If you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), past logs will get moved to the ``archived_logs/`` folder instead of getting deleted.

**Usage examples:**
```bash
pytest test_fail.py --with-testing_base --browser=chrome

nosetests test_fail.py --with-selenium --with-testing_base --browser=firefox
```

**Expected log files generated during failures:**
[basic_test_info.txt](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/basic_test_info.txt)
[page_source.html](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/page_source.html)
[screenshot.png](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/screenshot.png)

---
**In addition to logging, you can also generate test reports:**

Reports are most useful when running large test suites. Pytest and Nosetest reports are handled differently.

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```bash
pytest my_test_suite.py --with-selenium --html=report.html
```
![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes. (Requires ``--with-testing_base`` to also be set when ``--report`` is used because it's part of that plugin.)

```bash
nosetests my_test_suite.py --with-selenium --with-testing_base --report --browser=chrome
```
![](http://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png "Example Nosetest Report")

(NOTE: You can add ``--show_report`` to immediately display the report after the test suite completes. You don't want to use this when running tests remotely because otherwise the test run will hang indefinitely until someone manually exits the report.)