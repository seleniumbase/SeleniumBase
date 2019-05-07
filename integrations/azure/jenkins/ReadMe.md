### Building a browser-based test automation server with [Jenkins on Azure](https://azuremarketplace.microsoft.com/en-au/marketplace/apps/azure-oss.jenkins) by using [SeleniumBase](https://github.com/seleniumbase/SeleniumBase)

----------

### Step 0. Fork the [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) repo on GitHub to get started quickly.

* **(You'll be using your own repository eventually.)**


### Step 1. Find Jenkins in the Azure Marketplace

#### Search for ["Jenkins" in the Azure Marketplace](https://portal.azure.com/#blade/Microsoft_Azure_Marketplace/GalleryFeaturedMenuItemBlade/selectedMenuItemId/home/searchQuery/jenkins/resetMenuId/) and select the ``Jenkins (Publisher: Microsoft)`` result to get to the Jenkins Start page.

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_01.png "Jenkins on Azure")


### Step 2. Launch a Jenkins instance

#### Click "Create" and follow the steps...

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_02.png "Jenkins on Azure")

#### Continue to "Additional Settings" when you're done with "Basics".

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_03.png "Jenkins on Azure")

#### On the "Additional Settings" section, set the Size to "B2s":

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_04.png "Jenkins on Azure")

#### Once you've reached Step 5, click "Create" to complete the setup.

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_05.png "Jenkins on Azure")


### Step 3. Inspect your new Jenkins instance to SSH into the new machine

#### Once your new Jenkins instance has finished launching, you should be able to see the main page:

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_06.png "Jenkins on Azure")

#### On the main page, you should be able to find the Public IP Address.
* **Use that IP Address to SSH into the machine:**

```bash
ssh USERNAME@IP_ADDRESS
```

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_07.png "Jenkins on Azure")


### Step 4. Clone the SeleniumBase repository from the root ("/") directory.

```bash
cd /
sudo git clone https://github.com/seleniumbase/SeleniumBase.git
```


### Step 5. Enter the "linux" folder

```bash
cd SeleniumBase/integrations/linux/
```

### Step 6. Give the "jenkins" user sudo access (See [jenkins_permissions.sh](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/linux/jenkins_permissions.sh) for details)

```bash
./jenkins_permissions.sh
```

### Step 7. Become the "jenkins" user and enter a "bash" shell

```bash
sudo su jenkins
bash
```

### Step 8. Install dependencies (See [Linuxfile.sh](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/linux/Linuxfile.sh) for details)

```bash
./Linuxfile.sh
```

### Step 9. Start up the headless browser display mechanism: Xvfb (See [Xvfb_launcher.sh](https://github.com/seleniumbase/SeleniumBase/blob/master/integrations/linux/Xvfb_launcher.sh) for details)

```bash
./Xvfb_launcher.sh
```

### Step 10. Go to the SeleniumBase directory

```bash
cd /SeleniumBase
```

### Step 11. Install the [requirements](https://github.com/seleniumbase/SeleniumBase/blob/master/requirements.txt) for SeleniumBase

```bash
sudo pip install -r requirements.txt --upgrade
```

### Step 12. Install SeleniumBase (Make sure you already installed the requirements above)

```bash
sudo python setup.py develop
```

### Step 13. Install chromedriver

```bash
sudo seleniumbase install chromedriver
```

### Step 14. Run an [example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) in Chrome to verify installation (May take up to 10 seconds)

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_08.png "Jenkins on Azure")

```bash
pytest examples/my_first_test.py --headless --browser=chrome
```

### Step 15. Secure your Jenkins machine

#### Navigate to http://JENKINS_IP_ADDRESS/jenkins-on-azure/

(Depending on your version of Jenkins, you may see the following screen, or nothing at all.)

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_09.png "Jenkins on Azure")

#### Initially, Jenkins uses only ``http``, which makes it less secure.

#### You'll need to set up SSH Port Forwarding in order to secure it.

* **To do this, copy/paste the string and run it in a NEW command prompt on your local machine (NOT from an SSH terminal session), swapping out the username and DNS name with the ones you set up when creating the Jenkins instance in Azure.**

``ssh -L 127.0.0.1:8080:localhost:8080 USERNAME@DNS_NAME``


### Step 16. Login to Jenkins

#### If you've correctly set up SSH Port Forwarding, the url will be ``http://127.0.0.1:8080/``

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_10.png "Jenkins on Azure")

#### You'll need to get the password from the SSH terminal on the Linux machine to log in:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```


### Step 17. Customize Jenkins

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_11.png "Jenkins on Azure")


### Step 18. Create an Admin user

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_12.png "Jenkins on Azure")

#### Once Jenkins has finished loading, the top left of the page should look like this:

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_13.png "Jenkins on Azure")


### Step 19. Create a new Jenkins job

* **Click on "New Item"**
* **Give your new Jenkins job a name (ex: "Test1")**
* **Select "Freestyle project"**
* **Click "OK"**

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_14.png "Jenkins on Azure")


### Step 20. Setup your new Jenkins job

* **Under "Source Code Management", select "Git".**
* **For the "Repository URL", put: ``https://github.com/seleniumbase/SeleniumBase.git``. (You'll eventually be using your own clone of the repository here.)**

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_15.png "Jenkins on Azure")

* **Under "Build", click the "Add build step" dropdown.**
* **Select "Execute shell".**
* **For the "Command", paste:**
```bash
cd examples
pytest my_first_test.py --headless
```

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_16.png "Jenkins on Azure")

#### Click "Save" when you're done.

* **You'll see the following page after that:**

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_18.png "Jenkins on Azure")


### Step 21. Run your new Jenkins job

* **Click on "Build Now"**
* **(If everything was done correctly, you'll see a blue dot appear after a few seconds, indicating that the test job passed.)**

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_19.png "Jenkins on Azure")


### Step 22. See the top Jenkins page for an overview of all jobs

![](https://cdn2.hubspot.net/hubfs/100006/images/jenkins_on_azure_17.png "Jenkins on Azure")


### Step 23. Future Work

If you have a web application that you want to test, you'll be able to create SeleniumBase tests and add them to Jenkins as you saw here. You may want to create a Deploy job, which downloads the latest version of your repository, and then kicks off all tests to run after that. You could then tell that Deploy job to auto-run whenever a change is pushed to your repository by using: "Poll SCM". All your tests would then be able to run by using: "Build after other projects are built". 

#### Congratulations! You're now well on your way to becoming a build & release / automation engineer!
