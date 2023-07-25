<!-- SeleniumBase Docs -->

## MySQL Installation Instructions


### [MySQL](http://www.mysql.com/) (OPTIONAL)

(NOTE: If you don't plan on using the SeleniumBase MySQL DB feature, then you can skip this section.)

--------

### GitHub Actions Ubuntu Linux MySQL Setup:

```bash
sudo /etc/init.d/mysql start
mysql -e 'CREATE DATABASE IF NOT EXISTS test_db;' -uroot -proot
wget https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/seleniumbase/core/create_db_tables.sql
sudo mysql -h 127.0.0.1 -uroot -proot test_db < create_db_tables.sql
sudo mysql -e 'ALTER USER "root"@"localhost" IDENTIFIED BY "test";' -uroot -proot
sudo service mysql restart
```

Have SeleniumBase tests write to the MySQL DB:

```bash
pytest --with-db_reporting
```

Query MySQL DB Results:

```bash
mysql -e 'select test_address,browser,state,start_time,runtime from test_db.test_run_data;' -uroot -ptest
```

--------

### Standard Ubuntu Linux MySQL Setup:

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql -e 'CREATE DATABASE IF NOT EXISTS test_db;'
sudo mysql -h 127.0.0.1 -u root test_db < seleniumbase/core/create_db_tables.sql
sudo service mysql restart
```

To change the password from `root` to `test`:

```bash
mysqladmin -u root -p'root' password 'test'
sudo service mysql restart
```

### MacOS MySQL Setup:

```bash
brew install mysql
```

Then start the MySQL service:

```bash
brew services start mysql
```

(Continue with additional steps below to set up your DB.)

### Windows MySQL Setup:

[Download MySQL here](http://dev.mysql.com/downloads/windows/)
Follow the steps from the MySQL Downloads page.

(Continue with additional steps below to set up your DB.)

### Access your MySQL DB:

If you want a visual tool to help make your MySQL life easier, [try MySQL Workbench](http://dev.mysql.com/downloads/workbench/).

### Prepare your MySQL DB:

Use the [create_db_tables.sql](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/core/create_db_tables.sql) file to create the necessary tables for storing test data.

### Configure your MySQL DB for SeleniumBase:

Update your [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) file with your MySQL DB credentials so that tests can write to the database when they run.

### Have SeleniumBase tests write to your MySQL DB:

Add the ``--with-db_reporting`` argument on the command line when you want tests to write to your MySQL database. Example:

```bash
pytest --with-db_reporting
```
