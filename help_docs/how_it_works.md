[<img src="https://seleniumbase.io/cdn/img/sb_logo_b.png" title="SeleniumBase" width="360">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

<a id="how_seleniumbase_works"></a>
<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> How it works:</h2>

At the core, SeleniumBase works by extending [pytest](https://docs.pytest.org/en/latest/) as a direct plugin. SeleniumBase automatically spins up web browsers for tests (using Selenium WebDriver), and then gives those tests access to the SeleniumBase libraries through the [BaseCase class](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py). Tests are also given access to [SeleniumBase command-line arguments](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md) and [SeleniumBase methods](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/method_summary.md), which provide additional functionality.

(NOTE: pytest uses a feature called test discovery to automatically find and run Python methods that start with "``test_``" from the file that you specified on the command line.)

The most common way of using SeleniumBase is by inheriting BaseCase:

```python
from seleniumbase import BaseCase
```

Then have your test classes inherit BaseCase:

```python
class MyTestClass(BaseCase):
```

(See the example test, [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py), for reference.)

--------

For more ways of using SeleniumBase, see: <a href="https://seleniumbase.io/help_docs/syntax_formats/">SyntaxFormats</a>.
