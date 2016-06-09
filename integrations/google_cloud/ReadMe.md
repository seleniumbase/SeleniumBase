## Google Cloud setup instructions for SeleniumBase (using Jenkins)

#### 1. Go to the Google Cloud Launcher

* Navigate to [https://console.cloud.google.com/launcher](https://console.cloud.google.com/launcher)
* (If you already have an active Google Cloud project, the Google Cloud Launcher will probably default to using that)

#### 2. Launch a Jenkins Instance

* Under "Featured Solutions", Click on "Jenkins"
* Click on "Launch on Compute Engine"
* Give the instance a name
* Give the instance a zone
* Click "Create"

#### 3. Connect with your new Jenkins instance

* SSH into your new instance by selecting: "SSH" => "Open in browser window" from the instance page.

#### 4. Clone the SeleniumBase repository from the root ("/") directory.

```bash
cd /
sudo git clone https://github.com/mdmintz/SeleniumBase.git
```

#### 5. Enter the "linux" folder

```bash
cd SeleniumBase/integrations/linux/
```

#### 6. Give Jenkins (aka "tomcat" user) sudo access

```bash
./jenkins_permissions.sh
```

#### 7. Become "tomcat" (the Jenkins user) and enter a "bash" shell

```bash
sudo su tomcat
bash
```

#### 8. Install dependencies

```bash
./Linuxfile.sh
```

#### 9. Start up the headless browser display mechanism (Xvfb)

```bash
./Xvfb_launcher.sh
```

#### 10. Go to the SeleniumBase directory

```bash
cd /SeleniumBase
```

#### 11. Install the requirements for SeleniumBase

```bash
sudo pip install -r server_requirements.txt
```

#### 12. Install SeleniumBase

```bash
sudo python setup.py install
```

#### 13. Run an example test in Chrome to make sure everything's working properly

```bash
nosetests examples/my_first_test.py --with-selenium --headless --browser=chrome
```

#### 14. You can also verify that Firefox works too

```bash
nosetests examples/my_first_test.py --with-selenium --headless --browser=firefox
```

#### 15. Login to Jenkins

* (The url, as well as username and password, should be accessible from your Google Cloud Platform VM instance page.)

#### 16. Create a new Jenkins job

* Click on "New Item"
* Give your new Jenkins job a name (ex: "First_Test")
* Select "Freestyle project"
* Click "OK"

#### 17. Setup your new Jenkins job

* Under "Source Code Management", select "Git".
* For the "Repository URL", put: ``https://github.com/mdmintz/SeleniumBase.git``. (You'll eventually be using your own clone of the repository here.)
* Under "Build", click the "Add build step" dropdown and then select "Execute shell".
* For the "Command", put:
```bash
nosetests examples/my_first_test.py --with-selenium --headless --browser=chrome
```
* Click "Save" when you're done.

#### 18. Run your new Jenkins job

* Click on "Build Now"
* (If all the setup was done correctly, you should see a blue dot appear after a few seconds, indicating that the test job passed.)

#### 19. Future Work

If you have a web application that you want to test, you'll be able to create SeleniumBase tests and add them to Jenkins as you saw here. You may want to create a Deploy job, which downloads the latest version of your repository, and then kicks off all tests to run after that. You could then tell that Deploy job to auto-run whenever a change is pushed to your repository by using: "Poll SCM". All your tests would then be able to run by using: "Build after other projects are built". You can also use MySQL to save test results in the DB so that you can query the data at any time.

#### Congratulations! You're now well on your way to becoming a build & release / automation engineer!

## MySQL DB setup instructions

#### 20. Return to the Google Cloud Launcher and launch a MySQL Instance

* Under "Featured Solutions", Click on "MySQL"
* Click on "Launch on Compute Engine"
* Give the instance a name
* Give the instance a zone
* Click "Create"

#### 21. Get the Connection credentials for your new MySQL DB

* Under the Google Cloud Platform menu, go to "Compute Engine"
* Find your new MySQL instance and then write down the value written in the "External IP" section.
* Under the Google Cloud Platform menu, go to "Deployment Manager"
* Find your new MySQL instance and then click on it.
* Write down the values for Admin username and password. (Username should be "root")

#### 22. Get a MySQL GUI tool so that you can connect to your MySQL DB

* You can download [MySQL Workbench](http://dev.mysql.com/downloads/tools/workbench/) for this.

#### 23. Create a new connection to your MySQL DB

* Use the MySQL DB credentials that you saved in Step 21 for this.

#### 24. Create a new schema in your MySQL DB

* You can name your schema ``test``.

#### 25. Create the necessary tables in your MySQL schema

* Run a SQL script in your MySQL schema using [testcaserepository.sql](https://raw.githubusercontent.com/mdmintz/SeleniumBase/master/seleniumbase/core/testcaserepository.sql)

#### 26. Have your local clone of SeleniumBase connect to your MySQL DB

* Update the MySQL connection details in your [settings.py](https://github.com/mdmintz/SeleniumBase/blob/master/seleniumbase/config/settings.py) file to use the credentials that you saved in Step 21.
* Run the following command again from the top-level SeleniumBase folder to make sure that SeleniumBase uses the updated credentials:

```bash
sudo python setup.py install
```

#### 27. Have your SeleniumBase Jenkins jobs use your MySQL DB

* For the "Execute shell", use the following as your updated "Command":

```bash
nosetests examples/my_test_suite.py --with-selenium --headless --browser=chrome --with-db_reporting --with-testing_base
```

* Click "Save" when you're done.

#### 28. Run your new Jenkins job

* Click on "Build Now"
* If all goes well, you should be seeing new rows appear in your MySQL DB.

#### 29. Congratulations! If you made it this far, you've become a SeleniumBase pro!
