[<img src="https://seleniumbase.io/cdn/img/sb_logo_10t.png" title="SeleniumBase" width="240">](https://github.com/seleniumbase/SeleniumBase/)

## Console Scripts

SeleniumBase console scripts help you get things done more easily, such as installing web drivers, creating a test directory with necessary configuration files, converting old WebDriver unittest scripts into SeleniumBase code, translating tests into multiple languages, and using the Selenium Grid.

* Usage: ``seleniumbase [COMMAND] [PARAMETERS]``

* (simplified): ``sbase [COMMAND] [PARAMETERS]``

* To list all commands: ``seleniumbase --help``

(<i>For running tests, [use <b>pytest</b> with SeleniumBase](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/customizing_test_runs.md).</i>)

### install

* Usage:
``sbase install [DRIVER] [OPTIONS]``

* Examples:

```bash
sbase install chromedriver
sbase install geckodriver
sbase install edgedriver
sbase install chromedriver 94
sbase install chromedriver 94.0.4606.61
sbase install chromedriver latest
sbase install chromedriver latest-1  # (Latest minus one)
sbase install chromedriver -p
sbase install chromedriver latest -p
sbase install edgedriver 94.0.992.38
```

(Drivers:  ``chromedriver``, ``geckodriver``, ``edgedriver``,
           ``iedriver``, ``operadriver``)

(Options:  ``latest`` or a specific driver version.
           For chromedriver, you can also specify the major
           version int, or ``latest-1`` for latest minus 1.
           If none specified, installs the default version.
           ``-p`` / ``--path``: Also copy to "/usr/local/bin".)

* Output:
Installs the specified webdriver.
(``chromedriver`` is required for Google Chrome automation)
(``geckodriver`` is required for Mozilla Firefox automation)
(``edgedriver`` is required for Microsoft Edge automation)
(``iedriver`` is required for Internet Explorer automation)
(``operadriver`` is required for Opera Browser automation)

### methods

* Usage:
``sbase methods``

* Output:
Displays common SeleniumBase Python methods.

### options

* Usage:
``sbase options``

* Output:
Displays common pytest command-line options
that are available when using SeleniumBase.

### mkdir

* Usage:
``sbase mkdir [DIRECTORY] [OPTIONS]``

* Example:
``sbase mkdir ui_tests``

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

### mkfile

* Usage:
``sbase mkfile [FILE.py] [OPTIONS]``

* Example:
``sbase mkfile new_test.py``

* Options:
``-b`` / ``--basic``  (Basic boilerplate / single-line test)
``-r`` / ``--recorder``  (Recorder Mode has ipdb breakpoint)

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

### mkpres

* Usage:
``sbase mkpres [FILE.py] [LANG]``

* Example:
``sbase mkpres new_presentation.py --en``

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

### mkchart

* Usage:
``sbase mkchart [FILE.py] [LANG]``

* Example:
``sbase mkchart new_chart.py --en``

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

### print

* Usage:
``sbase print [FILE] [OPTIONS]``

* Options:
``-n`` (Add line Numbers to the rows)

* Output:
Prints the code/text of any file
with syntax-highlighting.

### translate

* Usage:
``sbase translate [SB_FILE.py] [LANGUAGE] [ACTION]``

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

### extract-objects

* Usage:
``sbase extract-objects [SB_FILE.py]``

* Output:
Creates page objects based on selectors found in a
seleniumbase Python file and saves those objects to the
"page_objects.py" file in the same folder as the tests.

### inject-objects

* Usage:
``sbase inject-objects [SB_FILE.py] [OPTIONS]``

* Options:
``-c``, ``--comments``  (Add object selectors to the comments.)

* Output:
Takes the page objects found in the "page_objects.py"
file and uses those to replace matching selectors in
the selected seleniumbase Python file.

### objectify

* Usage:
``sbase objectify [SB_FILE.py] [OPTIONS]``

* Options:
``-c``, ``--comments``  (Add object selectors to the comments.)

* Output:
A modified version of the file where the selectors
have been replaced with variable names defined in
"page_objects.py", supporting the Page Object Pattern.
(This has the same outcome as combining
``extract-objects`` with ``inject-objects``)

### revert-objects

* Usage:
``sbase revert-objects [SB_FILE.py] [OPTIONS]``

* Options:
``-c``, ``--comments``  (Keep existing comments for the lines.)

* Output:
Reverts the changes made by ``seleniumbase objectify ...`` or
``seleniumbase inject-objects ...`` when run against a
seleniumbase Python file. Objects will get replaced by
selectors stored in the "page_objects.py" file.

### convert

* Usage:
``sbase convert [WEBDRIVER_UNITTEST_FILE.py]``

* Output:
Converts a Selenium IDE exported WebDriver unittest file
into a SeleniumBase file. Adds ``_SB`` to the new
file name while keeping the original file intact.
Works with Katalon Recorder scripts.
See [This ReadMe](https://seleniumbase.io/seleniumbase/utilities/selenium_ide/ReadMe/) for details.

### encrypt / obfuscate

* Usage:
``sbase encrypt``  OR  ``sbase obfuscate``

* Output:
Runs the password encryption/obfuscation tool.
(Where you can enter a password to encrypt/obfuscate.)

### decrypt / unobfuscate

* Usage:
``sbase decrypt``  OR  ``sbase unobfuscate``

* Output:
Runs the password decryption/unobfuscation tool.
(Where you can enter an encrypted password to decrypt.)

### download

* Usage:
``sbase download server``

* Output:
Downloads the Selenium Server JAR file for Grid usage.
(That JAR file is required when using a Selenium Grid)

### grid-hub

* Usage:
``sbase grid-hub {start|stop|restart} [OPTIONS]``

* Options:
``-v``, ``--verbose``  (Increases verbosity of logging output.)
``--timeout=TIMEOUT``  (Close idle browser windows after TIMEOUT seconds.)

* Output:
Controls the Selenium Grid Hub server, which allows
for running tests on multiple machines in parallel
to speed up test runs and reduce the total time
of test suite execution.
You can start, restart, or stop the Grid Hub server.

### grid-node

* Usage:
``sbase grid-node {start|stop|restart} [OPTIONS]``

* Options:
``--hub=HUB_IP`` (The Grid Hub IP Address to connect to.) (Default: ``127.0.0.1``)
``-v``, ``--verbose``  (Increases verbosity of logging output.)

* Output:
Controls the Selenium Grid node, which serves as a
worker machine for your Selenium Grid Hub server.
You can start, restart, or stop the Grid node.

--------

[<img src="https://seleniumbase.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="290">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
