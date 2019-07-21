<a id="how_seleniumbase_works"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **How SeleniumBase Works:**

At the core, SeleniumBase works by extending [Pytest](https://docs.pytest.org/en/latest/) and [Nosetests](http://nose.readthedocs.io/en/latest/) as a direct plugin to each one. SeleniumBase automatically spins up web browsers for tests, and then gives those tests access to the SeleniumBase libraries through the BaseCase class, [found here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py). Now you can use "``--browser=chrome``" to specify the web browser to use (Default = "Chrome"). You can also include additional plugins for additional features such as "``--demo_mode``" (for highlighting elements & changing the speed of test runs) and "``--proxy=IP_ADDRESS:PORT``" (for using a proxy server during test runs). There are also other plugins available such as "``--with-db_reporting``", "``--with-s3_logging``", and more.

(NOTE: Pytest and Nosetests work by automatically running any Python method that starts with "``test``" from the file that you specified on the command line. You can also run all tests from a specific class in a file, or even pick out an individual test to run.)

To use SeleniumBase calls you need the following:
```python
from seleniumbase import BaseCase
```
And then have your test classes inherit BaseCase:
```python
class MyTestClass(BaseCase):
```
(*See the example test, [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py), for reference.*)
