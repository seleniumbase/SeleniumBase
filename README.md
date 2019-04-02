[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_3.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

[<img src="https://img.shields.io/github/release/seleniumbase/SeleniumBase.svg" />](https://github.com/seleniumbase/SeleniumBase/releases) [<img src="https://dev.azure.com/seleniumbase/seleniumbase/_apis/build/status/seleniumbase.SeleniumBase?branchName=master" />](https://dev.azure.com/seleniumbase/seleniumbase/_build/latest?definitionId=1&branchName=master) [<img src="https://travis-ci.org/seleniumbase/SeleniumBase.svg?branch=master" alt="Build Status" />](https://travis-ci.org/seleniumbase/SeleniumBase) [<img src="https://badges.gitter.im/seleniumbase/SeleniumBase.svg" alt="Join the Gitter Chat" />](https://gitter.im/seleniumbase/SeleniumBase) [<img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" alt="MIT License" />](https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE) [<img src="https://img.shields.io/github/stars/seleniumbase/seleniumbase.svg" alt="GitHub Stars" />](https://github.com/seleniumbase/SeleniumBase/stargazers)<br />

Reliable Browser Automation & Testing with [Selenium-WebDriver](https://www.seleniumhq.org/) and [Pytest](https://docs.pytest.org/en/latest/).

<img src="https://cdn2.hubspot.net/hubfs/100006/sb_demo_mode.gif" title="SeleniumBase" height="236"><br />
(<i>Above: [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) from [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) running in demo mode, which adds JavaScript for highlighting page actions.</i>)<br />
```
pytest my_first_test.py --demo_mode
```

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Quick Start:

(<i>Requires [Git](https://git-scm.com/) and [Python](https://www.python.org/downloads/) [<img src="https://img.shields.io/badge/python-2.7,_3.x-22AADD.svg" alt="Python versions" />](https://www.python.org/downloads/). Optionally, you may want to use a [Python virtual environment](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md) to isolate Python dependencies between projects.</i>)

#### Clone SeleniumBase from GitHub:
```
git clone https://github.com/seleniumbase/SeleniumBase.git
```

#### Upgrade [pip](https://pypi.org/project/pip/) and [setuptools](https://pypi.org/project/setuptools/) to the latest versions:
```
python -m pip install -U pip setuptools
```
* (Depending on your user permissions, you may need to add ``--user`` to the command if you're not inside a [Python virtual environment](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md), or use "[sudo](https://en.wikipedia.org/wiki/Sudo)" on a UNIX-based OS if you're getting errors during installation.)

#### Install SeleniumBase:
```
cd SeleniumBase
pip install -U -r requirements.txt
python setup.py install
```
* (Use ``python setup.py develop`` if configuring seleniumbase inside a virtual environment.)
* (You can also get seleniumbase from the Python Package Index, [<img src="https://img.shields.io/pypi/v/seleniumbase.svg" alt="Version" />](https://pypi.python.org/pypi/seleniumbase))

#### Install a web driver to the [seleniumbase/drivers](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/drivers) folder:
```
seleniumbase install chromedriver
```

* (You need a different web driver for each web browser you want to run automation on: ``chromedriver`` for Chrome, ``edgedriver`` for Edge, ``geckodriver`` for Firefox, ``operadriver`` for Opera, and ``iedriver`` for Internet Explorer.)

#### Run a test on Chrome:
```
cd examples
pytest my_first_test.py --browser=chrome
```

* (Chrome is the default browser if not specified with ``--browser``)

<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32">

Check out [SeleniumBase Website Tours](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/tour_examples) (in the ``examples/tour_examples`` folder). It's great for prototyping a website onboarding experience. See the [Tours ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/ReadMe.md) for more details.

```
cd tour_examples
pytest google_tour.py
```

<img src="https://cdn2.hubspot.net/hubfs/100006/google_tour_3.gif" title="SeleniumBase Tour of Google" height="260"><br>
(Above: Actual demo of [google_tour.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/tour_examples/google_tour.py) running on [google.com](https://google.com))

<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32">

For more detailed steps on getting started, see the [**Detailed Instructions**](#seleniumbase_installation) section.

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Learn More:

#### **No more repetitive WebDriver code:**<br />
SeleniumBase automatically handles common WebDriver actions such as spinning up web browsers, waiting for page objects to load, saving screenshots during test failures, using a proxy server, and more. (<i>[Read about customizing test runs](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md).</i>)

#### **Simple Python syntax makes coding easy:**<br />

<img src="https://cdn2.hubspot.net/hubfs/100006/images/my_first_test_image.png" title="SeleniumBase Python Code" height="280">

(<i>By default, [CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp) are used for finding page elements.</i>)

#### **Run tests with Pytest or Nose in any browser:**<br />
(<i>Using **Pytest** is strongly recommended</i>)

```
pytest my_first_test.py --browser=chrome

nosetests test_suite.py --browser=firefox
```

Python methods that start with ``test_`` will automatically be run when using ``pytest`` or ``nosetests`` on a Python file, (<i>or on folders containing Python files</i>).

#### **No more messy code:**<br />
This long line of standard WebDriver code,
```python
self.driver.find_element_by_css_selector("textarea").send_keys("text")
```
...becomes the following in SeleniumBase:
```python
self.update_text("textarea", "text")
```
(<i>You can still use ``self.driver`` in your code.</i>)

#### **No more flaky tests:**<br />
SeleniumBase methods automatically wait for page elements to finish loading before interacting with them (*up to a timeout limit*). This means you no longer need random ``time.sleep()`` statements in your code.

#### **Assist manual QA with automation:**<br />
SeleniumBase includes an automated/manual hybrid solution called **[MasterQA](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/masterqa/ReadMe.md)**, which speeds up manual testing by having automation perform all the web browser actions while the manual tester only validates what is seen.

#### **Integrate with your favorite tools:**<br />
SeleniumBase is compatible with [Selenium Grid](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid), [MySQL](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/testcase_manager.py), [Docker](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/docker/ReadMe.md), [NodeJS](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/node_js), [Google Cloud](https://github.com/seleniumbase/SeleniumBase/tree/master/integrations/google_cloud/ReadMe.md), and [AWS](#amazon_section).

#### **Automate tedious business tasks:**<br />
Beyond test automation, SeleniumBase is perfect for automating tedious business tasks that you would perform in a web browser.

#### **Lots of happy users & customers:**<br />
To learn about businesses using SeleniumBase, [Click Here](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/happy_customers.md).

#### **Feature-Rich:**<br />
To see a full list of SeleniumBase features, [Click Here](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/features_list.md).

<a id="seleniumbase_installation"></a>
<img src="https://cdn2.hubspot.net/hubfs/100006/images/logo_base_4b.png" title="SeleniumBase" height="100">

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Detailed Instructions:

Before installation, **[install Python and Git](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/install_python_pip_git.md)**.

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Step 1:** Clone SeleniumBase

```
git clone https://github.com/seleniumbase/SeleniumBase.git
```

(<i>A [Git](https://git-scm.com/) GUI tool like [SourceTree](https://www.sourcetreeapp.com/) may help.</i>)

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Step 2:** Create a Virtual Environment

(OPTIONAL) To learn how to create a Python virtual environment, [see this ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md).

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Step 3:** Install SeleniumBase

If you're installing SeleniumBase from a cloned copy on your machine, use:
```
cd SeleniumBase

pip install -r requirements.txt --upgrade
python setup.py install
```

If you're installing SeleniumBase from the [Python Package Index](https://pypi.python.org/pypi/seleniumbase) [<img src="https://img.shields.io/badge/pypi-seleniumbase-22AAEE.svg" alt="pypi" />](https://pypi.python.org/pypi/seleniumbase), use:
```
pip install -U seleniumbase --no-cache-dir
```

If you're installing SeleniumBase directly from GitHub, use:
```
pip install -e git+https://github.com/seleniumbase/SeleniumBase.git@master#egg=seleniumbase
```

(If you encounter permission errors during installation while not using a virtual environment, you may need to add ``--user`` to your pip command. If you already have an older version of SeleniumBase installed, you may want to add ``--upgrade`` or ``-U`` to your pip command.)

<a id="seleniumbase_install_a_web_driver"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Step 4:** Install a Web Driver

SeleniumBase requires a web driver to run automation on web browers. For that, you'll need to either download a web driver to your path, or **[install a web driver](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/webdriver_installation.md)** with the SeleniumBase ``install`` command.

```
seleniumbase install chromedriver
seleniumbase install geckodriver
seleniumbase install edgedriver
```

(``geckodriver`` is the offical name of the Firefox driver)

<a id="seleniumbase_basic_usage"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Step 5:** Run the Example Script

**Here's what the example script, [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py), looks like:**

```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_basic(self):
        self.open("https://xkcd.com/353/")
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text("free to copy", "div center")
        self.open("https://xkcd.com/1481/")
        title = self.get_attribute("#comic img", "title")
        self.assert_true("86,400 seconds per day" in title)
        self.click("link=Blag")
        self.assert_text("The blag of the webcomic", "h2")
        self.update_text("input#s", "Robots!\n")
        self.assert_text("Hooray robots!", "#content")
        self.open("https://xkcd.com/1319/")
        self.assert_exact_text("Automation", "#ctitle")
```
(<i>By default, [CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp) are used for finding page elements.</i>)

**Here's how to run the example script on various web browsers:**

(NOTE: You can interchange **pytest** with **nosetests** at anytime.)

```
cd examples/

pytest my_first_test.py --browser=chrome

nosetests my_first_test.py --browser=firefox
```
(<i>If no browser is specified, Chrome is used by default.</i>)

<a id="seleniumbase_demo_mode"></a>
If the example test is moving too fast for your eyes to see what's going on, you can run it in **Demo Mode** by adding ``--demo_mode`` on the command line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real time:

```
pytest my_first_test.py --demo_mode
```

You can use the following in your scripts to help you debug issues:

```python
import time; time.sleep(5)  # sleep for 5 seconds (add this after the line you want to pause on)
import ipdb; ipdb.set_trace()  # waits for your command. n = next line of current method, c = continue, s = step / next executed line (will jump)
import pytest; pytest.set_trace()  # similar to ipdb, but specific to pytest
```

**To pause an active test that throws an exception or error, add ``--pdb -s``:**

```
pytest my_first_test.py --browser=chrome --pdb -s
```

The code above will leave your browser window open in case there's a failure. (ipdb commands: 'c', 's', 'n' => continue, step, next).

Here are some other useful **nosetest**-specific arguments:

```
--logging-level=INFO  # Hide DEBUG messages, which can be overwhelming.
-x  # Stop running the tests after the first failure is reached.
-v  # Prints the full test name rather than a dot for each test.
--with-id  # If -v is also used, will number the tests for easy counting.
```

During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), otherwise log files with be cleaned up at the start of the next test run. The ``test_suite.py`` collection contains tests that fail on purpose so that you can see how logging works.

```
cd examples/

pytest test_suite.py --browser=chrome

pytest test_suite.py --browser=firefox
```

If you want to run tests headlessly, use ``--headless``, which you'll need to do if your system lacks a GUI interface. Even if your system does have a GUI interface, it may still support headless browser automation.

To run Pytest multithreaded on multiple CPUs at the same time, add ``-n=NUM`` or ``-n NUM`` on the command line, where NUM is the number of CPUs you want to use.

If you want to pass additional data from the command line to your tests, you can use ``--data=STRING``. Now inside your tests, you can use ``self.data`` to access that.

<img src="https://cdn2.hubspot.net/hubfs/100006/images/logo_base_4b.png" title="SeleniumBase" height="100">

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Using SeleniumBase from a [PyPI](https://pypi.org/) installation:**

You can install SeleniumBase without cloning the repo by doing this:

```
python -m pip install -U pip
pip install -U seleniumbase --no-cache-dir
```

You can then install webdrivers by doing this:

```
seleniumbase install chromedriver
seleniumbase install geckodriver
seleniumbase install edgedriver
seleniumbase install iedriver
seleniumbase install operadriver
```

(You'll need chromedriver if you want to run automation on Chrome, geckodriver if you want to run automation on Firefox, edgedriver for Microsoft Edge, etc.)

When creating your own test directories, keep these two things in mind:

For running tests outside of the SeleniumBase repo with **Pytest**, you'll want a copy of **[pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini)** on the root folder. For running tests outside of the SeleniumBase repo with **Nosetests**, you'll want a copy of **[setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg)** on the root folder. (Subfolders should include a blank ``__init__.py`` file.)

As a shortcut, you'll be able to run ``seleniumbase mkdir [DIRECTORY_NAME]`` to create a new folder that already contains necessary files and some example tests that you can run. Example:

```
seleniumbase mkdir browser_tests
cd browser_tests
pytest my_first_test.py --browser=chrome
```

<img src="https://cdn2.hubspot.net/hubfs/100006/images/logo_base_4b.png" title="SeleniumBase" height="100">

<a id="creating_visual_reports"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Creating Visual Test Suite Reports:**

(NOTE: Several command line args are different for Pytest vs Nosetests)

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.

```
pytest test_suite.py --html=report.html
```

![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

You can also use ``--junitxml=report.xml`` to get an xml report instead. Jenkins can use this file to display better reporting for your tests.

```
pytest test_suite.py --junitxml=report.xml
```

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes.

```
nosetests test_suite.py --report
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" title="Example Nosetest Report" height="420">

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Using a Proxy Server:**

If you wish to use a proxy server for your browser tests (Chrome and Firefox only), you can add ``--proxy=IP_ADDRESS:PORT`` as an argument on the command line.

```
pytest proxy_test.py --proxy=IP_ADDRESS:PORT
```

If the proxy server that you wish to use requires authentication, you can do the following (Chrome only):

```
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT
```

To make things easier, you can add your frequently-used proxies to PROXY_LIST in [proxy_list.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/proxy_list.py), and then use ``--proxy=KEY_FROM_PROXY_LIST`` to use the IP_ADDRESS:PORT of that key.

```
pytest proxy_test.py --proxy=proxy1
```


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Changing the User-Agent:**

If you wish to change the User-Agent for your browser tests (Chrome and Firefox only), you can add ``--agent="USER AGENT STRING"`` as an argument on the command line.

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```


<a id="utilizing_advanced_features"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Production Environments & Integrations:**

Here are some things you can do to setup a production environment for your testing:

* You can setup a [Jenkins](https://jenkins.io/) build server for running tests at regular intervals. Jenkins has many plugins available, such as [the Xvfb headless browser plugin](https://wiki.jenkins-ci.org/display/JENKINS/Xvfb+Plugin) for running tests on a machine with no GUI. If you have Xvfb running in the background, you can add ``--headless`` to your run command in order to utilize it. For more info about the Xvfb plugin, [read this](https://qxf2.com/blog/xvfb-plugin-for-jenkins-selenium/). For a real-world Jenkins example of headless browser automation in action, check out [the SeleniumBase Google Cloud ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/google_cloud/ReadMe.md).

* You can use [the Selenium Grid](https://github.com/SeleniumHQ/selenium/wiki/Grid2) to scale your testing by distributing tests on several machines with parallel execution. To do this, check out the SeleniumBase [selenium_grid folder](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/utilities/selenium_grid), which should have everything you need. The [Selenium Grid ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md) will help you get started.

* If you're using the [SeleniumBase MySQL feature](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/mysql_installation.md) to save results from tests running on a server machine, you can install [MySQL Workbench](https://dev.mysql.com/downloads/tools/workbench/) to help you read & write from your DB more easily. You'll also need to install the MySQL Python client. Depending on your system, you may need to install additional requirements for this (such as on Windows). See [Stackoverflow](https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python) for more info.

```
pip install mysqlclient==1.3.14
```

* If you use [Slack](https://slack.com), you can easily have your Jenkins jobs display results there by using the [Jenkins Slack Plugin](https://github.com/jenkinsci/slack-plugin). Another way to send messages from your tests to Slack is by using [Slack's Incoming Webhooks API](https://api.slack.com/incoming-webhooks).

<a id="amazon_section"></a>
* If you're using AWS, you can setup an [Amazon S3](https://aws.amazon.com/s3/) account for saving your log files and screenshots for future viewing. SeleniumBase already has [all the code you need to connect to S3](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/s3_logging_plugin.py). You'll need to modify [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) with connection details to your instance and the location in S3 where you want log files to be saved. You'll also need to add "``--with-s3_logging``" on the command line when you run your tests.

Here's an example of running tests with additional features enabled:
```
pytest [YOUR_TEST_FILE].py --browser=chrome --with-db_reporting --with-s3_logging -s
```
(NOTE: If you haven't configured your MySQL or S3 connections in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), don't use ``--with-db_reporting`` or ``--with-s3_logging``.)

When the testing_base plugin is used, if there's a test failure, the basic_test_info plugin records test logs, the page_source plugin records the page source of the last web page seen by the test, and the screen_shots plugin records the image of the last page seen by the test where the failure occurred. Make sure you always include testing_base whenever you include a plugin that logs test data. The db_reporting plugin records the status of all tests run into your MySQL DB. The s3_logging plugin uploads basic test info, screenshots, and page source into your S3 storage folder.

To simplify that long run command, you can create a ``*.cfg`` file, such as the one provided in the example, and enter your plugins there so that you can run everything by typing:

```
nosetests [YOUR_TEST_FILE].py --config=[MY_CONFIG_FILE].cfg
```

You can simplify that even more by using a setup.cfg file, such as the one provided for you in the examples folder. If you kick off a test run from within the folder that setup.cfg is location in, that file will automatically be used as your configuration, meaning that you wouldn't have to type out all the plugins that you want to use (or include a config file) everytime you run tests.

If you tell pytest/nosetests to run an entire file, it will run every method in that python file that starts with "test". You can be more specific on what to run by doing something like the following: (<i>Note that the syntax is different for pytest vs nosetests.</i>)

```
pytest [YOUR_TEST_FILE].py::[SOME_CLASS_NAME]::test_[SOME_TEST_NAME]
nosetests [YOUR_TEST_FILE].py:[SOME_CLASS_NAME].test_[SOME_TEST_NAME]
```

Let's try an example of a test that fails:
```python
""" test_fail.py """
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_find_army_of_robots_on_xkcd_desert_island(self):
        self.open("https://xkcd.com/731/")
        self.assert_element("div#ARMY_OF_ROBOTS", timeout=1)  # This should fail
```

You can run it from the ``examples`` folder like this:

```
pytest test_fail.py
```

You'll notice that a logs folder, "latest_logs", was created to hold information about the failing test, and screenshots. Take a look at what you get. Remember, this data can be saved in your MySQL DB and in S3 if you include the necessary plugins in your run command (and if you set up the neccessary connections properly). For future test runs, past test results will get stored in the archived_logs folder if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py).


<img src="https://cdn2.hubspot.net/hubfs/100006/images/logo_base_4b.png" title="SeleniumBase" height="100">

<a id="detailed_method_specifications"></a>
### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **Detailed Method Specifications and Examples:**

#### Navigating to a web page (and related commands)

```python
self.open("https://xkcd.com/378/")  # This method opens the specified page.

self.go_back()  # This method navigates the browser to the previous page.

self.go_forward()  # This method navigates the browser forward in history.

self.refresh_page()  # This method reloads the current page.

self.get_current_url()  # This method returns the current page URL.

self.get_page_source()  # This method returns the current page source.
```

**ProTip™:** You may need to use the get_page_source() method along with Python's find() command to parse through the source to find something that Selenium wouldn't be able to. (You may want to brush up on your Python programming skills for that.)
Ex:
```python
source = self.get_page_source()
head_open_tag = source.find('<head>')
head_close_tag = source.find('</head>', head_open_tag)
everything_inside_head = source[head_open_tag+len('<head>'):head_close_tag]
```

#### Clicking

To click an element on the page:

```python
self.click("div#my_id")
```

**ProTip™:** In most web browsers, you can right-click on a page and select ``Inspect Element`` to see the CSS selector details that you'll need to create your own scripts.

#### Typing Text

self.update_text(selector, text)  # updates the text from the specified element with the specified value. An exception is raised if the element is missing or if the text field is not editable. Example:

```python
self.update_text("input#id_value", "2012")
```

You can also use self.add_text() or the WebDriver .send_keys() command, but those won't clear the text box first if there's already text inside.
If you want to type in special keys, that's easy too. Here's an example:

```python
from selenium.webdriver.common.keys import Keys
self.find_element("textarea").send_keys(Keys.SPACE + Keys.BACK_SPACE + '\n')  # the backspace should cancel out the space, leaving you with the newline
```

#### Getting the text from an element on a page

```python
text = self.get_text("header h2")
```

#### Getting the attribute value from an element on a page

```python
attribute = self.get_attribute("#comic img", "title")
```

#### Asserting existance of an element on a page within some number of seconds:

```python
self.wait_for_element_present("div.my_class", timeout=10)
```
(NOTE: You can also use: ``self.assert_element_present(ELEMENT)``)

#### Asserting visibility of an element on a page within some number of seconds:

```python
self.wait_for_element_visible("a.my_class", timeout=5)
```
(NOTE: The short versions of this are ``self.find_element(ELEMENT)`` and ``self.assert_element(ELEMENT)``. The find_element() version returns the element)

Since the line above returns the element, you can combine that with .click() as shown below:

```python
self.find_element("a.my_class", timeout=5).click()

# But you're better off using the following statement, which does the same thing:

self.click("a.my_class")  # DO IT THIS WAY!
```

**ProTip™:** You can use dots to signify class names (Ex: ``div.class_name``) as a simplified version of ``div[class="class_name"]`` within a CSS selector. 

You can also use ``*=`` to search for any partial value in a CSS selector as shown below:

```python
self.click('a[name*="partial_name"]')
```

#### Asserting visibility of text inside an element on a page within some number of seconds:

```python
self.assert_text("Make it so!", "div#trek div.picard div.quotes")
self.assert_text("Tea. Earl Grey. Hot.", "div#trek div.picard div.quotes", timeout=3)
```
(NOTE: ``self.find_text(TEXT, ELEMENT)`` and ``self.wait_for_text(TEXT, ELEMENT)`` also do this. For backwords compatibility, older method names were kept, but the default timeout may be different.)

#### Asserting Anything

```python
self.assert_true(myvar1 == something)

self.assert_equal(var1, var2)
```

#### Useful Conditional Statements (with creative examples in action)

is_element_visible(selector)  # is an element visible on a page
```python
import logging
if self.is_element_visible('div#warning'):
    logging.debug("Red Alert: Something bad might be happening!")
```

is_element_present(selector)  # is an element present on a page
```python
if self.is_element_present('div#top_secret img.tracking_cookie'):
    self.contact_cookie_monster()  # Not a real method unless you define it somewhere
else:
    current_url = self.get_current_url()
    self.contact_the_nsa(url=current_url, message="Dark Zone Found")  # Not a real method unless you define it somewhere
```
Another example:
```python
def is_there_a_cloaked_klingon_ship_on_this_page():
    if self.is_element_present("div.ships div.klingon"):
        return not self.is_element_visible("div.ships div.klingon")
    return False
```

is_text_visible(text, selector)  # is text visible on a page
```python
def get_mirror_universe_captain_picard_superbowl_ad(superbowl_year):
    selector = "div.superbowl_%s div.commercials div.transcript div.picard" % superbowl_year
    if self.is_text_visible("For the Love of Marketing and Earl Grey Tea!", selector):
        return "Picard HubSpot Superbowl Ad 2015"
    elif self.is_text_visible("Delivery Drones... Engage", selector):
        return "Picard Amazon Superbowl Ad 2015"
    elif self.is_text_visible("Bing it on Screen!", selector):
        return "Picard Microsoft Superbowl Ad 2015"
    elif self.is_text_visible("OK Glass, Make it So!", selector):
        return "Picard Google Superbowl Ad 2015"
    elif self.is_text_visible("Number One, I've Never Seen Anything Like It.", selector):
        return "Picard Tesla Superbowl Ad 2015"
    elif self.is_text_visible("""With the first link, the chain is forged.
                              The first speech censored, the first thought forbidden,
                              the first freedom denied, chains us all irrevocably.""", selector):
        return "Picard Wikimedia Superbowl Ad 2015"
    elif self.is_text_visible("Let us make sure history never forgets the name ... Facebook", selector):
        return "Picard Facebook Superbowl Ad 2015"
    else:
        raise Exception("Reports of my assimilation are greatly exaggerated.")
```

#### Switching Tabs

What if your test opens up a new tab/window and now you have more than one page? No problem. You need to specify which one you currently want Selenium to use. Switching between tabs/windows is easy:
Ex:

```python
self.switch_to_window(1)  # this switches to the new tab (0 is the first one)
```

**ProTip™:** iFrames follow the same principle as new windows - you need to specify the iFrame if you want to take action on something in there
Ex:

```python
self.switch_to_frame('ContentManagerTextBody_ifr')
# Now you can act inside the iFrame
# .... Do something cool (here)
self.switch_to_default_content()  # exit the iFrame when you're done
```

#### Handle Pop-Up Alerts

What if your test makes an alert pop up in your browser? No problem. You need to switch to it and either accept it or dismiss it:
Ex:

```python
self.wait_for_and_accept_alert()

self.wait_for_and_dismiss_alert()
```

If you're not sure whether there's an alert before trying to accept or dismiss it, one way to handle that is to wrap your alert-handling code in a try/except block. Other methods such as .text and .send_keys() will also work with alerts.

#### Executing Custom jQuery Scripts:

jQuery is a powerful JavaScript library that allows you to perform advanced actions in a web browser.
If the web page you're on already has jQuery loaded, you can start executing jQuery scripts immediately.
You'd know this because the web page would contain something like the following in the HTML:

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
```

It's OK if you want to use jQuery on a page that doesn't have it loaded yet. To do so, run the following command first:

```python
self.activate_jquery()
```

Some websites have a restrictive [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) to prevent users from loading jQuery and other external libraries onto their websites. If you need to use jQuery or another JS library on such a website, use Firefox with SeleniumBase, which overrides the CSP to allow loading of any JS library.

Here are some examples of using jQuery in your scripts:
```python
self.execute_script('jQuery, window.scrollTo(0, 600)')  # Scrolling the page

self.execute_script("jQuery('#annoying-widget').hide()")  # Hiding elements on a page

self.execute_script("jQuery('#hidden-widget').show(0)")  # Showing hidden elements on a page

self.execute_script("jQuery('#annoying-button a').remove()")  # Removing elements on a page

self.execute_script("jQuery('%s').mouseover()" % (mouse_over_item))  # Mouse-over elements on a page

self.execute_script("jQuery('input#the_id').val('my_text')")  # Fast text input on a page

self.execute_script("jQuery('div#dropdown a.link').click()")  # Click elements on a page

self.execute_script("return jQuery('div#amazing')[0].text")  # Returns the css "text" of the element given

self.execute_script("return jQuery('textarea')[2].value")  # Returns the css "value" of the 3rd textarea element on the page
```

In the following example, JavaScript is used to plant code on a page that Selenium can then touch after that:
```python
start_page = "https://xkcd.com/465/"
destination_page = "https://github.com/seleniumbase/SeleniumBase"
self.open(start_page)
referral_link = '''<a class='analytics test' href='%s'>Free-Referral Button!</a>''' % destination_page
self.execute_script('''document.body.innerHTML = \"%s\"''' % referral_link)
self.click("a.analytics")  # Clicks the generated button
```
(Due to popular demand, this traffic generation example has been baked into SeleniumBase with the ``self.generate_referral(start_page, end_page)`` and the ``self.generate_traffic(start_page, end_page, loops)`` methods.)

#### Using delayed asserts:

Let's say you want to verify multiple different elements on a web page in a single test, but you don't want the test to fail until you verified several elements at once so that you don't have to rerun the test to find more missing elements on the same page. That's where delayed asserts come in. Here's the example:

```python
from seleniumbase import BaseCase

class MyTestClass(BaseCase):

    def test_delayed_asserts(self):
        self.open('https://xkcd.com/993/')
        self.wait_for_element('#comic')
        self.delayed_assert_element('img[alt="Brand Identity"]')
        self.delayed_assert_element('img[alt="Rocket Ship"]')  # Will Fail
        self.delayed_assert_element('#comicmap')
        self.delayed_assert_text('Fake Item', '#middleContainer')  # Will Fail
        self.delayed_assert_text('Random', '#middleContainer')
        self.delayed_assert_element('a[name="Super Fake !!!"]')  # Will Fail
        self.process_delayed_asserts()
```

``delayed_assert_element()`` and ``delayed_assert_text()`` will save any exceptions that would be raised.
To flush out all the failed delayed asserts into a single exception, make sure to call ``self.process_delayed_asserts()`` at the end of your test method. If your test hits multiple pages, you can call ``self.process_delayed_asserts()`` at the end of all your delayed asserts for a single page. This way, the screenshot from your log file will have the location where the delayed asserts were made.

#### Accessing raw WebDriver

If you need access to any commands that come with standard WebDriver, you can call them directly like this:
```python
self.driver.delete_all_cookies()
capabilities = self.driver.capabilities
self.driver.find_elements_by_partial_link_text("GitHub")
```
(In general, you'll want to use the SeleniumBase versions of methods when available.)

#### Retrying failing tests automatically

You can use ``--reruns NUM`` to retry failing tests that many times. Use ``--reruns-delay SECONDS`` to wait that many seconds between retries. Example:
```
pytest --reruns 5 --reruns-delay 1
```

Additionally, you can use the ``@retry_on_exception()`` decorator to specifically retry failing methods. (First import: ``from seleniumbase import decorators``) To learn more about SeleniumBase decorators, [click here](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/common).

####  Checking Email: 
Let's say you have a test that sends an email, and now you want to check that the email was received:

```python
from seleniumbase.fixtures.email_manager import EmailManager, EmailException
num_email_results = 0
email_subject = "This is the subject to search for (maybe include a timestamp)"
email_manager = EmailManager("{YOUR SELENIUM GMAIL ACCOUNT EMAIL ADDRESS}")  # the password for this would be stored in seleniumbase/config/settings.py
try:
    html_text = email_manager.search(SUBJECT="%s" % email_subject, timeout=300)
    num_email_results = len(html_text)
except EmailException:
    num_email_results = 0
self.assert_true(num_email_results)  # true if not zero
```

Now you can parse through the email if you're looking for specific text or want to navigate to a link listed there.


### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Wrap-Up

#### Congratulations on getting started with SeleniumBase!

<i>**Questions or Comments?**</i><br />
[![Join the chat at https://gitter.im/seleniumbase/SeleniumBase](https://badges.gitter.im/seleniumbase/SeleniumBase.svg)](https://gitter.im/seleniumbase/SeleniumBase?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)<br />

If you see something, say something! We are very active in resolving issues. [<img src="https://img.shields.io/github/issues-closed-raw/seleniumbase/SeleniumBase.svg" alt="Closed Issues" />](https://github.com/seleniumbase/SeleniumBase/issues?q=is%3Aissue+is%3Aclosed)

[https://github.com/mdmintz](https://github.com/mdmintz)<br />

[<img src="https://cdn2.hubspot.net/hubfs/100006/images/SB_Logo3g4.png" title="SeleniumBase" height="45">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md) <br /> <img src="https://cdn2.hubspot.net/hubfs/100006/images/logo_base_4b.png" title="SeleniumBase" height="150"> <br /> [<img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" alt="MIT License" />](https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE)
