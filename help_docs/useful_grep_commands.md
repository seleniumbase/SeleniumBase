<!-- SeleniumBase Docs -->

## Useful grep commands

There are several useful **grep** commands for helping you find and/or replace text in multiple files. Examples:

#### List all files containing ``self.get_new_driver(``, ignoring ".pyc" files, from the current directory:

``grep -rl "self.get_new_driver(" * --exclude=\*.pyc``
OR
``grep -rl * -e "self.get_new_driver(" --exclude=\*.pyc``

To only search ``.py`` files, use ``--include=\*.py``:

``grep -rl "self.get_new_driver(" * --include=\*.py``

--------

#### Replace all occurrences of "foo_abc" with "bar_xyz" on Linux, for Python files from the current directory:

``sed -i 's/foo_abc/bar_xyz/g' *.py``

#### Replace all occurrences of "foo_abc" with "bar_xyz" on macOS, for Python files from the current directory:

``sed -i '' 's/foo_abc/bar_xyz/g' *.py``

--------

#### Find all chromedriver processes (this combines ``ps`` with ``grep``):

``ps -ef |grep chromedriver``

--------

#### References:
* https://stackoverflow.com/questions/16956810/how-do-i-find-all-files-containing-specific-text-on-linux
* https://stackoverflow.com/questions/11392478/how-to-replace-a-string-in-multiple-files-in-linux-command-line/20721292#20721292
