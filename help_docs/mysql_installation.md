### MySQL Installation Instructions


#### [MySQL](http://www.mysql.com/) (OPTIONAL)

(NOTE: If you're using this test framework from a local development machine and don't plan on writing to a MySQL DB from your local test runs, you can skip this step.)

Mac:

```bash
brew install MySQL
```

Windows: [Download MySQL here](http://dev.mysql.com/downloads/windows/)

That installs the MySQL library so that you can use db commands in your code. To make that useful, you'll want to have a MySQL DB that you can connect to. You'll also want to use the testcaserepository.sql file from the seleniumbase/core folder to add the necessary tables.

If you want a visual tool to help make your MySQL life easier, [try MySQL Workbench](http://dev.mysql.com/downloads/workbench/).
