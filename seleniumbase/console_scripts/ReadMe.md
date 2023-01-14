<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) Console Scripts 🌠

🌟 SeleniumBase console scripts can do many things, such as downloading web drivers, creating test directories with config files, activating the SeleniumBase Recorder, launching the SeleniumBase Commander, translating tests into other languages, running a Selenium Grid, and more.

* Usage: ``seleniumbase [COMMAND] [PARAMETERS]``

* (simplified): ``sbase [COMMAND] [PARAMETERS]``

* To list all commands: ``seleniumbase --help``

(<i>For running tests, [use <b>pytest</b> with SeleniumBase](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md).</i>)

```bash
COMMANDS:
      get / install    [DRIVER] [OPTIONS]
      methods          (List common Python methods)
      options          (List common pytest options)
      behave-options   (List common behave options)
      gui / commander  [OPTIONAL PATH or TEST FILE]
      behave-gui       (SBase Commander for Behave)
      caseplans        [OPTIONAL PATH or TEST FILE]
      mkdir            [DIRECTORY] [OPTIONS]
      mkfile           [FILE.py] [OPTIONS]
      mkrec / codegen  [FILE.py] [OPTIONS]
      recorder         (Open Recorder Desktop App.)
      record           (If args: mkrec. Else: App.)
      mkpres           [FILE.py] [LANG]
      mkchart          [FILE.py] [LANG]
      print            [FILE] [OPTIONS]
      translate        [SB_FILE.py] [LANG] [ACTION]
      convert          [WEBDRIVER_UNITTEST_FILE.py]
      extract-objects  [SB_FILE.py]
      inject-objects   [SB_FILE.py] [OPTIONS]
      objectify        [SB_FILE.py] [OPTIONS]
      revert-objects   [SB_FILE.py] [OPTIONS]
      encrypt / obfuscate
      decrypt / unobfuscate
      download server  (Get Selenium Grid JAR file)
      grid-hub         [start|stop] [OPTIONS]
      grid-node        [start|stop] --hub=[HOST/IP]
 * (EXAMPLE: "sbase get chromedriver latest") *

    Type "sbase help [COMMAND]" for specific command info.
    For info on all commands, type: "seleniumbase --help".
    Use "pytest" for running tests.
```

<h3>get / install</h3>

* Usage:

```bash
sbase get [DRIVER] [OPTIONS]
sbase install [DRIVER] [OPTIONS]
```

* Examples:

```bash
sbase get chromedriver
sbase get geckodriver
sbase get edgedriver
sbase get chromedriver 109
sbase get chromedriver 109.0.5414.74
sbase get chromedriver latest
sbase get chromedriver latest-1  # (Latest minus one)
sbase get chromedriver -p
sbase get chromedriver latest -p
```

(Drivers:  ``chromedriver``, ``geckodriver``, ``edgedriver``,
           ``iedriver``, ``operadriver``, ``uc_driver``)

(Options:  ``latest`` or a specific driver version.
           For chromedriver, you can also specify the major
           version int, or ``latest-1`` for latest minus 1.
           If none specified, installs the default version.
           ``-p`` / ``--path``: Also copy to "/usr/local/bin".)

* Output:

Downloads the webdriver to ``seleniumbase/drivers/``
(``chromedriver`` is required for Chrome automation)
(``geckodriver`` is required for Firefox automation)
(``edgedriver`` is required for MS__Edge automation)

<h3>methods</h3>

* Usage:

```bash
sbase methods
```

* Output:

Displays common SeleniumBase Python methods.

<h3>options</h3>

* Usage:

```bash
sbase options
```

* Output:

Displays common pytest command-line options
that are available when using SeleniumBase.

```bash
--browser=BROWSER  (The web browser to use. Default is "chrome")
--headless  (Run tests headlessly. Default mode on Linux OS.)
--demo  (Slow down and visually see test actions as they occur.)
--slow  (Slow down the automation. Faster than using Demo Mode.)
--reuse-session / --rs  (Reuse browser session between tests.)
--crumbs  (Clear all cookies between tests reusing a session.)
--maximize  (Start tests with the web browser window maximized.)
--dashboard  (Enable SeleniumBase\'s Dashboard at dashboard.html)
--uc  (Enable undetected-chromedriver to evade bot-detection.)
--incognito  (Enable Chromium\'s Incognito mode.)
--guest  (Enable Chromium\'s Guest mode.)
-m=MARKER  (Run tests with the specified pytest marker.)
-n=NUM  (Multithread the tests using that many threads.)
-v  (Verbose mode. Print the full names of each test run.)
--html=report.html  (Create a detailed pytest-html report.)
--collect-only / --co  (Only show discovered tests. No run.)
--co -q  (Only show full names of discovered tests. No run.)
-x  (Stop running tests after the first failure is reached.)
--pdb  (Enter the Post Mortem Debug Mode after any test fails.)
--trace  (Enter Debug Mode immediately after starting any test.)
      | Debug Mode Commands  >>>   help / h: List all commands. |
      |   n: Next line of method. s: Step through. c: Continue. |
      |  return / r: Run until method returns. j: Jump to line. |
      | where / w: Show stack spot. u: Up stack. d: Down stack. |
      | longlist / ll: See code. dir(): List namespace objects. |
--final-debug  (Enter Final Debug Mode after each test ends.)
--recorder  (Record browser actions to generate test scripts.)
--save-screenshot  (Save a screenshot at the end of each test.)
--archive-logs  (Archive old log files instead of deleting them.)
--check-js  (Check for JavaScript errors after page loads.)
--start-page=URL  (The browser start page when tests begin.)
--agent=STRING  (Modify the web browser\'s User-Agent string.)
--mobile  (Use Chromium\'s mobile device emulator during tests.)
--metrics=STRING  (Set mobile "CSSWidth,CSSHeight,PixelRatio".)
--ad-block  (Block some types of display ads after page loads.)
--settings-file=FILE  (Override default SeleniumBase settings.)
--env=ENV  (Set the test env. Access with "self.env" in tests.)
--data=DATA  (Extra test data. Access with "self.data" in tests.)
--disable-csp  (Disable the Content Security Policy of websites.)
--remote-debug  (Sync to Ch-R-Debugger chrome://inspect/#devices)
--server=SERVER  (The Selenium Grid server/IP used for tests.)
--port=PORT  (The Selenium Grid port used by the test server.)
--proxy=SERVER:PORT  (Connect to a proxy server:port for tests.)
--proxy=USER:PASS@SERVER:PORT  (Use authenticated proxy server.)

For the full list of command-line options, type: "pytest --help".
```

<h3>behave-options</h3>

* Usage:

```bash
sbase behave-options
```

* Output:

Displays common Behave command-line options
that are available when using SeleniumBase.

```bash
-D browser=BROWSER  (The web browser to use. Default is "chrome")
-D headless  (Run tests headlessly. Default mode on Linux OS.)
-D demo  (Slow down and visually see test actions as they occur.)
-D slow  (Slow down the automation. Faster than using Demo Mode.)
-D reuse-session / -D rs  (Reuse browser session between tests.)
-D crumbs  (Clear all cookies between tests reusing a session.)
-D maximize  (Start tests with the web browser window maximized.)
-D dashboard  (Enable SeleniumBase\'s Dashboard at dashboard.html)
-D uc  (Enable undetected-chromedriver to evade bot-detection.)
-D incognito  (Enable Chromium\'s Incognito mode.)
-D guest  (Enable Chromium\'s Guest mode.)
--no-snippets / -q  (Quiet mode. Don\'t print snippets.)
--dry-run / -d  (Dry run. Only show discovered tests.)
--stop  (Stop running tests after the first failure is reached.)
-D pdb  (Enter the Post Mortem Debug Mode after any test fails.)
      | Debug Mode Commands  >>>   help / h: List all commands. |
      |   n: Next line of method. s: Step through. c: Continue. |
      |  return / r: Run until method returns. j: Jump to line. |
      | where / w: Show stack spot. u: Up stack. d: Down stack. |
      | longlist / ll: See code. dir(): List namespace objects. |
-D recorder  (Record browser actions to generate test scripts.)
-D save-screenshot  (Save a screenshot at the end of each test.)
-D archive-logs  (Archive old log files instead of deleting them.)
-D check-js  (Check for JavaScript errors after page loads.)
-D start-page=URL  (The browser start page when tests begin.)
-D agent=STRING  (Modify the web browser\'s User-Agent string.)
-D mobile  (Use Chromium\'s mobile device emulator during tests.)
-D metrics=STRING  (Set mobile "CSSWidth,CSSHeight,PixelRatio".)
-D ad-block  (Block some types of display ads after page loads.)
-D settings-file=FILE  (Override default SeleniumBase settings.)
-D env=ENV  (Set the test env. Access with "self.env" in tests.)
-D data=DATA  (Extra test data. Access with "self.data" in tests.)
-D disable-csp  (Disable the Content Security Policy of websites.)
-D remote-debug  (Sync to Ch-R-Debugger chrome://inspect/#devices)
-D server=SERVER  (The Selenium Grid server/IP used for tests.)
-D port=PORT  (The Selenium Grid port used by the test server.)
-D proxy=SERVER:PORT  (Connect to a proxy server:port for tests.)
-D proxy=USER:PASS@SERVER:PORT  (Use authenticated proxy server.)

For the full list of command-line options, type: "behave --help".
```

<h3>gui / commander</h3>

* Usage:

```bash
sbase gui [OPTIONAL PATH or TEST FILE]
sbase commander [OPTIONAL PATH or TEST FILE]
```

<h3>behave-gui</h3>

* Usage:

```bash
sbase behave-gui [OPTIONAL PATH or TEST FILE]
sbase gui-behave [OPTIONAL PATH or TEST FILE]
```

* Examples:

```bash
sbase behave-gui
sbase behave-gui -i=calculator
sbase behave-gui features/
sbase behave-gui features/calculator.feature
```

* Output:

Launches SeleniumBase Commander / GUI for Behave.

<h3>caseplans</h3>

* Usage:

```bash
sbase caseplans [OPTIONAL PATH or TEST FILE]
```

* Examples:

```bash
sbase caseplans
sbase caseplans -k agent
sbase caseplans -m marker2
sbase caseplans test_suite.py
sbase caseplans offline_examples/
```

* Output:

Launches the SeleniumBase Case Plans Generator.

<h3>mkdir</h3>

* Usage:

```bash
sbase mkdir [DIRECTORY] [OPTIONS]
```

* Example:

```bash
sbase mkdir ui_tests
```

* Options:

``-b`` / ``--basic``  (Only config files. No tests added.)

* Output:

Creates a new folder for running SBase scripts.
The new folder contains default config files,
sample tests for helping new users get started,
and Python boilerplates for setting up customized
test frameworks.

```bash
ui_tests/
├── __init__.py
├── my_first_test.py
├── parameterized_test.py
├── pytest.ini
├── requirements.txt
├── setup.cfg
├── test_demo_site.py
└── boilerplates/
    ├── __init__.py
    ├── base_test_case.py
    ├── boilerplate_test.py
    ├── classic_obj_test.py
    ├── page_objects.py
    ├── sb_fixture_test.py
    └── samples/
        ├── __init__.py
        ├── google_objects.py
        ├── google_test.py
        ├── sb_swag_test.py
        └── swag_labs_test.py
```

If running with the ``-b`` or ``--basic`` option:

```bash
ui_tests/
├── __init__.py
├── pytest.ini
├── requirements.txt
└── setup.cfg
```

<h3>mkfile</h3>

* Usage:

```bash
sbase mkfile [FILE.py] [OPTIONS]
```

* Example:

```bash
sbase mkfile new_test.py
```

* Options:

``-b`` / ``--basic``  (Basic boilerplate / single-line test)
``-r`` / ``--rec``  (adds Pdb+ breakpoint for Recorder Mode)

* Language Options:

``--en`` / ``--English``    |    ``--zh`` / ``--Chinese``
``--nl`` / ``--Dutch``      |    ``--fr`` / ``--French``
``--it`` / ``--Italian``    |    ``--ja`` / ``--Japanese``
``--ko`` / ``--Korean``     |    ``--pt`` / ``--Portuguese``
``--ru`` / ``--Russian``    |    ``--es`` / ``--Spanish``

* Output:

Creates a new SeleniumBase test file with boilerplate code.
If the file already exists, an error is raised.
By default, uses English mode and creates a
boilerplate with the 5 most common SeleniumBase
methods, which are "open", "type", "click",
"assert_element", and "assert_text". If using the
basic boilerplate option, only the "open" method
is included.

<h3>mkrec / record / codegen</h3>

* Usage:

```bash
sbase mkrec [FILE.py] [OPTIONS]
sbase codegen [FILE.py] [OPTIONS]
```

* Examples:

```bash
sbase mkrec new_test.py
sbase mkrec new_test.py --url=seleniumbase.io
sbase codegen new_test.py
sbase codegen new_test.py --url=wikipedia.org
```

* Options:

``--url=URL``  (Sets the initial start page URL.)
``--edge``  (Use Edge browser instead of Chrome.)
``--gui`` / ``--headed``  (Use headed mode on Linux.)
``--uc`` / ``--undetected``  (Use undetectable mode.)
``--overwrite``  (Overwrite file when it exists.)
``--behave``  (Also output Behave/Gherkin files.)

* Output:

Creates a new SeleniumBase test using the Recorder.
If the filename already exists, an error is raised.

<h3>recorder</h3>

* Usage:

```bash
sbase recorder [OPTIONS]
```

* Options:

``--uc`` / ``--undetected``  (Use undetectable mode.)
``--behave``  (Also output Behave/Gherkin files.)

* Output:

Launches the SeleniumBase Recorder Desktop App.

<h3>mkpres</h3>

* Usage:

```bash
sbase mkpres [FILE.py] [LANG]
```

* Example:

```bash
sbase mkpres new_presentation.py --en
```

* Language Options:

``--en`` / ``--English``    |    ``--zh`` / ``--Chinese``
``--nl`` / ``--Dutch``      |    ``--fr`` / ``--French``
``--it`` / ``--Italian``    |    ``--ja`` / ``--Japanese``
``--ko`` / ``--Korean``     |    ``--pt`` / ``--Portuguese``
``--ru`` / ``--Russian``    |    ``--es`` / ``--Spanish``

* Output:

Creates a new presentation with 3 example slides.
If the file already exists, an error is raised.
By default, the slides are written in English,
and use "serif" theme with "slide" transition.
The slides can be used as a basic boilerplate.

<h3>mkchart</h3>

* Usage:

```bash
sbase mkchart [FILE.py] [LANG]
```

* Example:

```bash
sbase mkchart new_chart.py --en
```

* Language Options:

``--en`` / ``--English``    |    ``--zh`` / ``--Chinese``
``--nl`` / ``--Dutch``      |    ``--fr`` / ``--French``
``--it`` / ``--Italian``    |    ``--ja`` / ``--Japanese``
``--ko`` / ``--Korean``     |    ``--pt`` / ``--Portuguese``
``--ru`` / ``--Russian``    |    ``--es`` / ``--Spanish``

* Output:

Creates a new SeleniumBase chart presentation.
If the file already exists, an error is raised.
By default, the slides are written in English,
and use a "sky" theme with "slide" transition.
The chart can be used as a basic boilerplate.

<h3>print</h3>

* Usage:

```bash
sbase print [FILE] [OPTIONS]
```

* Options:

``-n`` (Add line Numbers to the rows)

* Output:

Prints the code/text of any file
with syntax-highlighting.

<h3>translate</h3>

* Usage:

```bash
sbase translate [SB_FILE.py] [LANGUAGE] [ACTION]
```

* Languages:

``--en`` / ``--English``    |    ``--zh`` / ``--Chinese``
``--nl`` / ``--Dutch``      |    ``--fr`` / ``--French``
``--it`` / ``--Italian``    |    ``--ja`` / ``--Japanese``
``--ko`` / ``--Korean``     |    ``--pt`` / ``--Portuguese``
``--ru`` / ``--Russian``    |    ``--es`` / ``--Spanish``

* Actions:

``-p`` / ``--print``  (Print translation output to the screen)
``-o`` / ``--overwrite``  (Overwrite the file being translated)
``-c`` / ``--copy``  (Copy the translation to a new ``.py`` file)

* Options:

``-n``  (include line Numbers when using the Print action)

* Output:

Translates a SeleniumBase Python file into the language
specified. Method calls and "import" lines get swapped.
Both a language and an action must be specified.
The ``-p`` action can be paired with one other action.
When running with ``-c`` (or ``--copy``), the new file name
will be the original name appended with an underscore
plus the 2-letter language code of the new language.
(Example: Translating "test_1.py" into Japanese with
``-c`` will create a new file called "test_1_ja.py".)

<h3>extract-objects</h3>

* Usage:

```bash
sbase extract-objects [SB_FILE.py]
```

* Output:

Creates page objects based on selectors found in a
seleniumbase Python file and saves those objects to the
"page_objects.py" file in the same folder as the tests.

<h3>inject-objects</h3>

* Usage:

```bash
sbase inject-objects [SB_FILE.py] [OPTIONS]
```

* Options:

``-c``, ``--comments``  (Add object selectors to the comments.)

* Output:

Takes the page objects found in the "page_objects.py"
file and uses those to replace matching selectors in
the selected seleniumbase Python file.

<h3>objectify</h3>

* Usage:

```bash
sbase objectify [SB_FILE.py] [OPTIONS]
```

* Options:

``-c``, ``--comments``  (Add object selectors to the comments.)

* Output:

A modified version of the file where the selectors
have been replaced with variable names defined in
"page_objects.py", supporting the Page Object Pattern.
(This has the same outcome as combining
``extract-objects`` with ``inject-objects``)

<h3>revert-objects</h3>

* Usage:

```bash
sbase revert-objects [SB_FILE.py] [OPTIONS]
```

* Options:

``-c``, ``--comments``  (Keep existing comments for the lines.)

* Output:

Reverts the changes made by ``seleniumbase objectify ...`` or
``seleniumbase inject-objects ...`` when run against a
seleniumbase Python file. Objects will get replaced by
selectors stored in the "page_objects.py" file.

<h3>convert</h3>

* Usage:

```bash
sbase convert [WEBDRIVER_UNITTEST_FILE.py]
```

* Output:

Converts a Selenium IDE exported WebDriver unittest file
into a SeleniumBase file. Adds ``_SB`` to the new
file name while keeping the original file intact.
Works with Katalon Recorder scripts.
See [This ReadMe](https://seleniumbase.io/seleniumbase/utilities/selenium_ide/ReadMe/) for details.

<h3>encrypt / obfuscate</h3>

* Usage:

``sbase encrypt``  OR  ``sbase obfuscate``

* Output:

Runs the password encryption/obfuscation tool.
(Where you can enter a password to encrypt/obfuscate.)

<h3>decrypt / unobfuscate</h3>

* Usage:

``sbase decrypt``  OR  ``sbase unobfuscate``

* Output:

Runs the password decryption/unobfuscation tool.
(Where you can enter an encrypted password to decrypt.)

<h3>download</h3>

* Usage:

```bash
sbase download server
```

* Output:

Downloads the Selenium Server JAR file for Grid usage.
(That JAR file is required when using a Selenium Grid)

<h3>grid-hub</h3>

* Usage:

```bash
sbase grid-hub {start|stop|restart} [OPTIONS]
```

* Options:

``-v``, ``--verbose``  (Increases verbosity of logging output.)
``--timeout=TIMEOUT``  (Close idle browser windows after TIMEOUT seconds.)

* Output:

Controls the Selenium Grid Hub server, which allows
for running tests on multiple machines in parallel
to speed up test runs and reduce the total time
of test suite execution.
You can start, restart, or stop the Grid Hub server.

<h3>grid-node</h3>

* Usage:

```bash
sbase grid-node {start|stop|restart} [OPTIONS]
```

* Options:

``--hub=HUB_IP`` (The Grid Hub IP Address to connect to.) (Default: ``127.0.0.1``)
``-v``, ``--verbose``  (Increases verbosity of logging output.)

* Output:

Controls the Selenium Grid node, which serves as a
worker machine for your Selenium Grid Hub server.
You can start, restart, or stop the Grid node.

--------

[<img src="https://seleniumbase.github.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
