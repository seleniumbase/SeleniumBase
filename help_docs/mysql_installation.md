<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="25" /> MySQL Installation Instructions</h3>


#### [MySQL](http://www.mysql.com/) (OPTIONAL)

(NOTE: If you're using this test framework from a local development machine and don't plan on writing to a MySQL DB from your local test runs, you can skip this step.)

##### Linux (Ubuntu):
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql -e 'CREATE DATABASE IF NOT EXISTS test_db;'
sudo mysql -h 127.0.0.1 -u root test_db < seleniumbase/core/create_db_tables.sql
sudo service mysql restart
```

To change the password:
```bash
mysqladmin -u root -p'OLD_PASSWORD' password NEW_PASSWORD
sudo service mysql restart
```

##### MacOS:
```bash
brew install mysql
```

Then you'll need to start the MySQL service:
```bash
brew services start mysql
```

Continue with additional steps below to setup your DB.

##### Windows:
[Download MySQL here](http://dev.mysql.com/downloads/windows/)
Follow the steps from the MySQL Downloads page.

Continue with additional steps below to setup your DB.

#### Access your MySQL DB

If you want a visual tool to help make your MySQL life easier, [try MySQL Workbench](http://dev.mysql.com/downloads/workbench/).

#### Prepare your MySQL DB

You can use the [create_db_tables.sql](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/create_db_tables.sql) file to create the necessary tables for storing test data.

#### Configure your MySQL DB for SeleniumBase

You'll want to update your [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) file with your MySQL DB credentials so that tests can write to the database when they run.

#### Allow tests to write to your MySQL database

Add the ``--with-db_reporting`` argument on the command line when you want tests to write to your MySQL database.
Example:
```bash
pytest my_first_test.py --with-db_reporting
```
