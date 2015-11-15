The python tests here are in nosetest format, which means that you CANNOT run them by using “python [NAME OF .PY FILE]” in the command prompt. To make running these files easy, .sh files have been created. Those contain the run commands to properly execute the python tests.

On a MAC or Unix-based system, you can execute .sh files by using ./[NAME OF .SH FILE] in a command prompt from the folder that the .sh files are located in. On a Windows-based system .bat files work the same way. You can switch the file extensions from .sh to .bat if you need to. One .bat file has been included in this folder.

You may have trouble opening .cfg files if you want to try viewing/editing them because the file extension may be unrecognized on your system. If so, use the Right-Click “Open With” option, or just drag & drop the file into a text-editing program.

If you run scripts with logging enabled, you’ll see two folders appear: “logs” and “archived logs”. The “logs” folder will contain log files from the most recent test run, but logs will only be created if the test run is failing. Afterwards, logs from the “logs” folder will get pushed to the “archived_logs” folder.

You may also see .pyc files appear as you run tests. That’s compiled bytecode, which is a natural result of running Python code.
