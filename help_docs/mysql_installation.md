### MySQL Installation Instructions


#### [MySQL](http://www.mysql.com/) (OPTIONAL)

(NOTE: If you're using this test framework from a local development machine and don't plan on writing to a MySQL DB from your local test runs, you can skip this step.)

Mac:
```bash
brew install MySQL
```

Windows:
[Download MySQL here](http://dev.mysql.com/downloads/windows/)

That installs the MySQL library so that you can use database commands in your code. To make that useful, you'll want to have a MySQL DB that you can connect to.

#### Access your MySQL DB

If you want a visual tool to help make your MySQL life easier, [try MySQL Workbench](http://dev.mysql.com/downloads/workbench/).

#### Prepare your MySQL DB

You can use the [testcaserepository.sql](https://github.com/mdmintz/SeleniumBase/blob/master/seleniumbase/core/testcaserepository.sql) file to create the necessary tables for storing test data.

If you were able to successfully install MySQL, you can now install the remaining MySQL requirements:
```bash
pip install -r server_requirements.txt
```

#### Configure your MySQL DB for SeleniumBase

You'll want to update your [settings.py](https://github.com/mdmintz/SeleniumBase/blob/master/seleniumbase/config/settings.py) file with your MySQL DB credentials so that tests can write to the database when they run.

#### Allow tests to write to your MySQL database

Add the ``--with-db_reporting`` argument on the command line when you want tests to write to your MySQL database.
Example:
```bash
nosetests my_first_test.py --with-selenium --with-db_reporting
```
