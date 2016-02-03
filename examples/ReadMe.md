The python tests here are in nosetest format, which means that you CANNOT run them by using “python [NAME OF .PY FILE]” in the command prompt. To make running these files easy, .sh files have been created. Those contain the run commands to properly execute the python tests.

On a MAC or Unix-based system, you can execute .sh files by using ./[NAME OF .SH FILE] in a command prompt from the folder that the .sh files are located in. On a Windows-based system .bat files work the same way. You can switch the file extensions from .sh to .bat if you need to. One .bat file has been included in this folder.

You may have trouble opening .cfg files if you want to try viewing/editing them because the file extension may be unrecognized on your system. If so, use the Right-Click “Open With” option, or just drag & drop the file into a text-editing program.

If you run scripts with logging enabled, you’ll see two folders appear: “logs” and “archived logs”. The “logs” folder will contain log files from the most recent test run, but logs will only be created if the test run is failing. Afterwards, logs from the “logs” folder will get pushed to the “archived_logs” folder.

You may also see .pyc files appear as you run tests. That’s compiled bytecode, which is a natural result of running Python code.

Here are some example run commands for the files in this folder and what they do:
(Note: You can replace ``nosetests`` with ``py.test`` for any of these.)

Run the example test in Firefox
```bash
nosetests my_first_test.py --browser=firefox --with-selenium
```

Run the example test in Chrome
```bash
nosetests my_first_test.py --browser=chrome --with-selenium
```

Run the example test in PhantomJS
```bash
nosetests my_first_test.py --browser=phantomjs --with-selenium
```

Run a test with all the configuration specifed by a config file
```bash
nosetests my_first_test.py --config=example_config.cfg
```

Example test with the use of python decorators
```bash
nosetests rate_limiting_test.py
```

Run a failing test with pdb mode enabled (If a test failure occurs, test enters pdb mode)
```bash
nosetests test_fail.py --browser=firefox --with-selenium --pdb --pdb-failures
```

Run a failing test with logging
```bash
nosetests test_fail.py --browser=firefox --with-selenium --with-testing_base --with-basic_test_info --with-page_source --with-screen_shots
```