## Support for migrating from Protractor to SeleniumBase

🔵 The Protractor/Angular tests from [github.com/angular/protractor/tree/master/example](https://github.com/angular/protractor/tree/master/example) have been migrated to SeleniumBase and placed in this directory.

🔵 Protractor tests that end in ``.spec.js`` will now end in ``_test.py`` for the conversion to SeleniumBase/Python format with pytest auto-discovery.

✅ Here's a test run with ``pytest`` using ``--reuse-session`` mode and Chromium ``--guest`` mode:

```zsh
$ pytest --rs -v --guest
=========================== test session starts ============================
platform darwin -- Python 3.11.9, pytest-8.3.3, pluggy-1.5.0 -- /Users/michael/.virtualenvs/sbase11/bin/python
metadata: {'Python': '3.11.9', 'Platform': 'macOS-13.2.1-arm64-arm-64bit', 'Packages': {'pytest': '8.3.3', 'pluggy': '1.5.0'}, 'Plugins': {'cov': '6.0.0', 'html': '2.0.1', 'metadata': '3.1.1', 'seleniumbase': '4.33.2', 'ordering': '0.6', 'rerunfailures': '15.0', 'xdist': '3.6.1'}}
rootdir: /Users/michael/github/SeleniumBase/examples
configfile: pytest.ini
plugins: html-2.0.1, metadata-3.1.1, seleniumbase-4.33.2, ordering-0.6, rerunfailures-15.0, xdist-3.6.1
collected 4 items

example_test.py::AngularJSHomePageTests::test_greet_user PASSED
example_test.py::AngularJSHomePageTests::test_todo_list PASSED
input_test.py::AngularMaterialInputTests::test_invalid_input PASSED
mat_paginator_test.py::AngularMaterialPaginatorTests::test_pagination PASSED

============================ 4 passed in 4.24s =============================
```
