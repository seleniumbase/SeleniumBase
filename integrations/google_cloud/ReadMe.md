## Google Cloud setup instructions for SeleniumBase (using Jenkins)

#### 1. Go to the Google Cloud Launcher

Navigate to [https://console.cloud.google.com/launcher](https://console.cloud.google.com/launcher)
(If you already have an active Google Cloud project, Google Cloud Lanucher will probably default to using that)

#### 2. Launch a Jenkins Instance

Under "Featured Solutions", Click on "Jenkins"
Click on "Launch on Compute Engine"
Give the instance a name
Give the instance a zone
Click "Create"

#### 3. Connect with your new Jenkins instance

SSH into your new instance by selecting: "SSH" => "Open in browser window" from the instance page.

#### 4. Clone the SeleniumBase repository from the root ("/") directory.

```bash
cd /
sudo git clone https://github.com/mdmintz/SeleniumBase.git
```

#### 5. Enter the "google_cloud" folder

```bash
cd SeleniumBase/integrations/google_cloud/
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
sudo pip install -r requirements.txt
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

(The url, as well as username and password, should be accessible from your Google Cloud Platform VM instance page.)

#### 16. Create a Jenkins job

Click on "New Item"
Give your new Jenkins job a name (ex: "First_Test")
Select "Freestyle project"
Click "OK"

#### 17. Setup your new Jenkins job

Click on the dropdown "Add build step", then select "Execute shell".
For the "Command", put:
```bash
cd /SeleniumBase
nosetests examples/my_first_test.py --with-selenium --headless --browser=chrome
```
Click "Save" when you're done.

#### 18. Run your new Jenkins job

Click on "Build Now"
(If all the setup was done correctly, you should see a blue dot appear after a few seconds, indicating that the test job passed.)

#### 19. Future Work

If you have a web application that you want to test, you'll be able to create SeleniumBase tests and add them to Jenkins as you saw here. You may want to create a Deploy job, which downloads the latest version of your repository, and then kicks off all tests to run after that. You could tell that Deploy job to auto-run whenever a change is pushed to your repository by using: "Poll SCM". All your tests would then be able to run by using: "Build after other projects are built".

#### Congratulations! You're now well on your way to becoming a build & release / automation engineer!
