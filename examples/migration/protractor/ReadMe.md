## Support for migrating from Protractor to SeleniumBase

🔵 The Protractor/Angular tests from [github.com/angular/protractor/tree/master/example](https://github.com/angular/protractor/tree/master/example) have been migrated to SeleniumBase and placed in this directory.

🔵 Protractor tests that end in ``.spec.js`` will now end in ``_test.py`` for the conversion to SeleniumBase/Python format with pytest auto-discovery.

✅ Here's a test run with ``pytest`` using ``--reuse-session`` mode and Chromium ``--guest`` mode:

```bash
$ pytest --rs -v --guest
========================== test session starts ==========================
platform darwin -- Python 3.9.2, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
metadata: {'Python': '3.9.2', 'Platform': 'macOS-10.14.6-x86_64-i386-64bit', 'Packages': {'pytest': '6.2.3', 'py': '1.10.0', 'pluggy': '0.13.1'}, 'Plugins': {'html': '2.0.1', 'rerunfailures': '9.1.1', 'xdist': '2.2.1', 'metadata': '1.11.0', 'ordering': '0.6', 'forked': '1.3.0', 'seleniumbase': '1.62.0'}}
rootdir: /Users/michael/github/SeleniumBase/examples, configfile: pytest.ini
plugins: html-2.0.1, rerunfailures-9.1.1, xdist-2.2.1, metadata-1.11.0, ordering-0.6, forked-1.3.0, seleniumbase-1.62.0
collected 4 items

example_test.py::AngularJSHomePageTests::test_greet_user PASSED
example_test.py::AngularJSHomePageTests::test_todo_list PASSED
input_test.py::AngularMaterialInputTests::test_invalid_input PASSED
mat_paginator_test.py::AngularMaterialPaginatorTests::test_pagination PASSED

========================== 4 passed in 10.34s ==========================
```
