## Console Scripts

SeleniumBase console scripts help you get things done more easily, such as installing web drivers, creating a test directory with necessary configuration files, converting old Webdriver unittest scripts into SeleniumBase code, and using the Selenium Grid.

For running tests from the command line, [use **pytest** with SeleniumBase](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md).

### install

* Usage:
``seleniumbase install [DRIVER_NAME]``
        (Drivers: chromedriver, geckodriver, edgedriver,
                  iedriver, operadriver)

* Example:
``seleniumbase install chromedriver``

* Output:
Installs the specified webdriver.
(chromedriver is required for Google Chrome automation)
(geckodriver is required for Mozilla Firefox automation)
(edgedriver is required for Microsoft Edge automation)
(iedriver is required for Internet Explorer automation)
(operadriver is required for Opera Browser automation)

### mkdir

* Usage:
``seleniumbase mkdir [DIRECTORY_NAME]``

* Example:
``seleniumbase mkdir browser_tests``

* Output:
Creates a new folder for running SeleniumBase scripts.
The new folder contains default config files,
sample tests for helping new users get started, and
Python boilerplates for setting up customized
test frameworks.

### convert

* Usage:
``seleniumbase convert [PYTHON_WEBDRIVER_UNITTEST_FILE]``

* Output:
Converts a Selenium IDE exported WebDriver unittest
file into a SeleniumBase file. Adds _SB to the new
file name while keeping the original file intact.
Works with Katalon Recorder scripts.
See: http://www.katalon.com/automation-recorder

### grid-hub

* Usage:
``seleniumbase grid-hub {start|stop|restart}``

* Options:
``-v``, ``--verbose``  (Increases verbosity of logging output.)

* Output:
Controls the Selenium Grid Hub server, which allows
for running tests on multiple machines in parallel
to speed up test runs and reduce the total time
of test suite execution.
You can start, restart, or stop the Grid Hub server.

### grid-node

* Usage:
``seleniumbase grid-node {start|stop|restart} [OPTIONS]``

* Options:
``--hub=HUB_IP`` (The Grid Hub IP Address to connect to.) (Default: ``127.0.0.1``)
``-v``, ``--verbose``  (Increases verbosity of logging output.)

* Output:
Controls the Selenium Grid node, which serves as a
worker machine for your Selenium Grid Hub server.
You can start, restart, or stop the Grid node.
