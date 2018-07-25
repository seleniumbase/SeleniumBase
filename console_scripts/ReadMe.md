## Console Scripts

### mkdir

* Usage:
``seleniumbase mkdir [DIRECTORY_NAME]``

* Output:
Creates a new folder for running SeleniumBase scripts.
The new folder contains default config files,
sample tests for helping new users get started, and
Python boilerplates for setting up customized
test frameworks.

### convert

* Usage:
``seleniumbase convert [MY_TEST.py]``

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
