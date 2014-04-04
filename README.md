# SeleniumSpot Test Framework

The purpose of this open-sourced Selenium Webdriver-based test framework is to have a complete and fully automated testing system for performing browser-based integration testing. You may be wondering why you'd want to use this as opposed to raw WebDriver scripts. Here are the added benefits:
* MySQL DB integration for storing test data and results
* Amazon S3 manager (to upload logs and screenshots from tests when they fail to see what went wrong)
* Easy to use and integrate with the Jenkins build-server
* An advanced logging system (to organize and store all your test data in Jenkins + S3 + MySQL)
* A system for easily utilizing data generated from previous tests (the delayed-data manager)
* An error-handling system (so that we can process useful data for the log files, eg: the page_source plugin)
* An email manager (so that we can automatically read and parse through emails sent to gmail addresses)
* Libraries for code simplification and reusable code
* Nosetest support (a fast and easy way to run all your tests)
* A plugin to send test failure notifications directly through HipChat (in the event of a test failure)
* Advanced commands that will save you significant time

To utilize some of the more advanced integrations, you'll need to setup instances and make connections to the following:
MySQL, Jenkins, Amazon S3, Gmail, HipChat, and a Selenium Grid. (More on this later)
We've provided placeholders in the code where you can specify your connection details. You can also use this framework as a bare-bones Selenium WebDriver command executer to automate tasks in a browser without doing any data reporting (and that's also the fastest way to make sure your base setup is working properly).
If you plan on running tests from a build server across multiple cloud machines, connecting to BrowserStack's Selenium cloud may be the least expensive alternative to having your own Selenium Grid. (If you're looking elsewhere, be wary of any Selenium cloud service that charges you by the test minute, as opposed to a flat monthly fee, because it may be a trap - those automated test minutes add up fast, and you don't want to limit the amount of automation you have.)

Check out HubSpot's blog article on [Automated Testing with Selenium](http://dev.hubspot.com/blog/bid/88880/Automated-Integration-Testing-with-Selenium-at-HubSpot). This is an excellent example of all the pieces coming together.

In short, developers aren't perfect. Bugs can slip by undetected during deploys even if there are existing unit tests to watch for problems. A fully-capable integration testing solution can provide an added layer of security.

A working system would be something like this: You have a QA build and a Prod build. After a QA deploy, run all the associated Selenium tests on QA. If everything passes, it's considered safe to deploy to Prod. As an added safety measure, run all those Selenium tests again on Prod after a deploy. If those pass, you should be able to feel safe. For more protection, also run Selenium tests at regular intervals in case something other than deploys breaks the system.


## Part I: MAC SETUP INSTRUCTIONS
####(Windows users: Try Powershell. You may need to make some adjustments during installation. This framework works on Windows machines if setup correctly.)

**Step 0:** Get the requirements:

[Homebrew](http://brew.sh/) + [Git](http://git-scm.com/)

    ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
    brew install git
    brew update

[MySQL](http://www.mysql.com/)

    brew install MySQL

That installs the MySQL library so that you can use db commands in your code. To make that useful, you'll want to have a MySQL DB that you can connect to, and you'll want to put your credentials in the mysql_conf.py file in the test_framework/core folder to access your DB from your tests. You'll also want to add the necessary tables, so to get you started, use the testcaserepository.sql file from the test_framework/core folder.

[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

    cd ~/
    pip install virtualenvwrapper
    export WORKON_HOME=~/Envs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh

[Chromedriver](http://code.google.com/p/chromedriver/) and [PhantomJS](http://phantomjs.org/)

    brew install chromedriver phantomjs

(There are web drivers for other web browsers as well. These two will get you started.)


**Step 1:** Checkout the SeleniumSpot Test Framework with Git or a Git GUI tool:

First you'll want to fork the repository on GitHub to create your own copy. This is important because you'll want to add your own configurations, credentials, settings, etc. Now clone your forked SeleniumSpot repository to your development machine. You can use a tool such as [SourceTree](http://www.sourcetreeapp.com/) to make things easier by providing you with a simple-to-use user interface for viewing and managing your git commits and status.

```bash
git clone [LOCATION OF YOUR FORKED SELENIUMSPOT GITHUB FOLDER]/SeleniumSpot.git
cd SeleniumSpot
```


**Step 2:** Create a virtualenv for seleniumspot:

```bash
mkvirtualenv seleniumspot
```

(Virtual environments are important because they allow you to have separate configurations from the rest of your system. This will prevent conflicts if you use other tools that require other configurations and settings.)

If you ever need to leave your virtual environment, use the following command:

```bash
deactivate
```

To get back into your virtual environment, use the following command:

```bash
workon seleniumspot
```


**Step 3:** Install necessary packages from the SeleniumSpot folder and compile the test framework

```bash
sudo pip install -r requirements.pip
sudo python setup.py install
```

(If you already have root access on the machine you're using, you might not need to add "sudo" before those commands.)

(If the pip install gives you a "clang error: unknown argument: '-mno-fused-madd'", see: http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa)


**Step 4:** You can verify that Chromedriver and Selenium were successfully installed by checking inside a python command prompt:

```bash
python
>>> from selenium import webdriver
>>> browser = webdriver.Chrome()
>>> browser.get("http://dev.hubspot.com/blog/the-classic-qa-team-is-obsolete")
>>> browser.close()
>>> exit()
```


**Step 5:** Now to verify the test framework installation by writing a simple Selenium script that performs basic actions such as navigating to a web page, clicking, waiting for page elements to appear, typing in text, scraping text on a page, and verifying text. (copy/paste this into a new file called "my_first_test.py"). This may be a good time to read up on css selectors. If you use Chrome, you can right-click on a page and select "Inspect Element" to see the details you need to create such a script. At a quick glance, dots are for class names and pound signs are for IDs. You'll also see something like "timeout=5" in the script, which tells the script how long to wait before failing (you can skip that argument and have it default to 30 seconds, which can be modified from the test framework code).

```python
from test_framework.fixtures import base_case

class MyTestClass(base_case.BaseCase):

    def test_basic(self):
        self.driver.get("http://www.wikipedia.org/")
        self.wait_for_element_visible("a[href='//en.wikipedia.org/']", timeout=5).click()
        self.wait_for_element_visible("div#simpleSearch", timeout=5)
        self.wait_for_element_visible("input[name='search']", timeout=5)
        self.update_text_value("input[name='search']", "Boston\n")
        text = self.wait_for_element_visible("div#mw-content-text", timeout=5).text
        self.assertTrue("The Charles River separates Boston from " in text)
        self.wait_for_element_visible("a[title='Find out about Wikipedia']").click()
        self.wait_for_text_visible("Since its creation in 2001", "div#mw-content-text", timeout=5)

        self.driver.get("http://www.wikimedia.org/")
        self.wait_for_element_visible('img[alt="Wikivoyage"]', timeout=5).click()
        self.wait_for_element_visible("a[href='//en.wikivoyage.org/']", timeout=5).click()
        self.wait_for_element_visible('a[title="Visit the main page"]', timeout=5)
        self.wait_for_element_visible('input#searchInput', timeout=5)
        self.update_text_value("input#searchInput", "Israel\n")
        self.wait_for_element_visible("div#contentSub", timeout=5)
        text = self.wait_for_element_visible("div#mw-content-text", timeout=5).text
        self.assertTrue("The state of Israel" in text)
```

Now run the script:

```bash
nosetests my_first_test.py --browser=chrome --with-selenium -s
```

After the test completes, in the console output you'll see a dot on a new line, representing a passing test. (On test failures you'll see an F instead, and on test errors you'll see an E). It looks more like a moving progress bar when you're running a ton of unit tests side by side. This is part of nosetests. After all tests complete (in this case there is only one), you'll see the "Ran 1 test in ..." line, followed by an "OK" if all nosetests passed.
If the example is moving too fast for your eyes to see what's going on, there are 2 things you can do. Add either of the following:

```python
import time; time.sleep(5) # sleep for 5 seconds (add this after the line you want to pause on)
import pdb; pdb.set_trace() # waits for your command. n = next line of current method, c = continue, s = step / next executed line (will jump)
```

You may also want to have your test sleep in other situations where you need to have your test wait for something. If you know what you're waiting for, you should be specific by using a command that waits for something specific to happen.

If you need to debug things on the fly (in case of errors), use this line to run the code:

```bash
nosetests my_first_test.py --browser=chrome --with-selenium --pdb --pdb-failures -s
```

The above code will leave your browser window open in case there's a failure, which is possible if the web pages from the example change the data that's displayed on the page. (pdb commands: 'c', 's', 'n' => continue, step, next).


**Step 6:** Complete the setup

If you're planning on using the full power of this test framework, there are a few more things you'll want to do:

* Setup your [Jenkins](http://jenkins-ci.org/) build server for running your tests at regular intervals. (Or you can use any build server you want.)

* Setup an [Amazon S3](http://aws.amazon.com/s3/) account for saving your log files and screenshots for future viewing. This test framework already has the code you need to connect to it. (Modify the s3_manager.py file from the test_framework/core folder with connection details to your instance.)

* Install [MySQL Workbench](http://dev.mysql.com/downloads/tools/workbench/) to make life easier by giving you a nice GUI tool that you can use to read & write from your DB directly.

* Setup your Selenium Grid and update your *.cfg file to point there. An example config file called selenium_server_config_example.cfg has been provided for you in the grid folder. The start-selenium-node.bat and start-selenium-server.sh files are for running your grid. In an example situation, your Selenium Grid server might live on a unix box and your Selenium Grid nodes might live on EC2 Windows virtual machines. When your build server runs a Selenium test, it would connect to your Selenium Grid to find out which Grid browser nodes are available to run that test. To simplify things, you can just use [Browser Stack](https://www.browserstack.com/automate) as your entire Selenium Grid (and let them do all the fun work of maintaining the grid for you).

* If you use [HipChat](https://www.hipchat.com/), you can have test alerts go there when tests fail. If that sounds good to you, update the db_reporting_plugin.py file from the plugins folder with your credentials.

* Be sure to tell SeleniumSpot to use these added features when you set them up. That's easy to do. You would be running tests like this:

```bash
nosetests [YOUR_TEST_FILE].py --browser=chrome --with-selenium --with-testing_base --with-basic_test_info --with-page_source --with-screen_shots --with-db_reporting --with-s3_logging -s
```

(When the testing_base plugin is used, if there's a test failure, the basic_test_info plugin records test logs, the page_source plugin records the page source of the last web page seen by the test, and the screen_shots plugin records the image of the last page seen by the test where the failure occurred. Make sure you always include testing_base whenever you include a plugin that logs test data. The db_reporting plugin records the status of all tests as long as you've setup your MySQL DB properly and you've also updated your test_framework/core/mysql_conf.py file with your DB credentials.)
To simplify that long run command, you can create a *.cfg file, such as the one provided in the example, and enter your plugins there so that you can run everything just by typing:

```bash
nosetests [YOUR_TEST_FILE].py --config=[MY_CONFIG_FILE].cfg -s
```

So much easier on the eyes :)
Remember, nosetests will run every method in that python file that starts with "test" in the method name. You can be more specific on what to run by doing something like:

```bash
nosetests [YOUR_TEST_FILE].py:[SOME_CLASS_NAME].test_[SOME_TEST_NAME] --config=[MY_CONFIG_FILE].cfg -s
```

Let's try an example of a test that fails. Copy the following into a file called fail_test.py:
```python
""" test_fail.py """
from test_framework.fixtures import base_case

class MyTestClass(base_case.BaseCase):

    def test_find_google_on_bing(self):
        self.driver.get("http://bing.com")
        self.wait_for_element_visible("div#google_is_here", timeout=3)  # This should fail
```
Now run it:

```bash
nosetests test_fail.py --browser=chrome --with-selenium --with-testing_base --with-basic_test_info --with-page_source --with-screen_shots -s
```

You'll notice that a logs folder was created to hold information about the failing test, and screenshots. Take a look at what you get. Remember, this data can be saved in your MySQL DB and in S3 if you include the necessary plugins in your run command (and if you set up the neccessary connections properly). For future test runs, past test results will get stored in the archived_logs folder.

Have you made it this far? Congratulations!!! Now you're ready to dive in at full speed!


## Part II: Detailed Method Specifications, Examples

Important Note: Make sure you include the following import in your code to use the framework commands:

```python
from test_framework.fixtures import base_case
```

#### Navigating to a Page, Plus Some Other Useful Related Commands

```python
self.driver.get("https://xkcd.com/378/")  # Instant navigation to any web page - just specify the url.

self.driver.refresh()  # refresh/reload the current page.

where_am_i = self.driver.current_url  # this variable changes as the current page changes.

source = self.driver.page_source   # this variable changes as the page source changes.
```

**ProTip™:** You may need to use the page_source method along with Python's find() command to parse through the source to find something that Selenium wouldn't be able to. (You may want to brush up on your Python programming skills if you're confused.)
Ex:
```python
source = self.driver.page_source
first_image_open_tag = source.find('<img>')
first_image_close_tag = source.find'</img>', first_image_open_tag)
everything_inside_first_image_tags = source[first_image_open_tag+len('<img>'):first_image_close_tag]
```

#### Clicking

To click an element on the page:

```python
self.click("div#my_id")
```

#### Asserting existance of an element on a page within some number of seconds:

```python
self.wait_for_element_present("div.my_class", timeout=10)
```

#### Asserting visibility of an element on a page within some number of seconds:

```python
self.wait_for_element_visible("a.my_class", timeout=5)
```

You can even combine visibility checking and clicking into one statement like so:

```python
self.wait_for_element_visible("a.my_class", timeout=5).click()
```

#### Asserting visibility of text inside an element on a page within some number of seconds:

```python
self.wait_for_text_visible("Make it so!", "div#trek div.picard div.quotes", timeout=3)
self.wait_for_text_visible("Tea. Earl Grey. Hot.", "div#trek div.picard div.quotes", timeout=1)
```

#### Asserting Anything

```python
self.assertTrue(myvar1 == something)

self.assertEqual(var1, var2)
```

#### Useful Conditional Statements (with creative examples in action)

is_element_visible(selector)  # is an element visible on a page
```python
import logging
if self.is_element_visible('div#warning'):
    logging.debug("Red Alert: Something bad might be happening!")
```

is_element_present(selector)  # is an element present on a page
```python
if self.is_element_present('div#top_secret img.tracking_cookie'):
    self.contact_cookie_monster()  # Not a real method unless you define it somewhere
else:
    current_url = self.driver.current_url
    self.contact_the_nsa(url=current_url, message="Dark Zone Found")  # Not a real method unless you define it somewhere
```
Another example:
```python
def is_there_a_cloaked_klingon_ship_on_this_page():
    if self.is_element_present("div.ships div.klingon"):
        return not self.is_element_visible("div.ships div.klingon")
    return False
```

is_text_visible(text, selector)  # is text visible on a page
```python
def get_mirror_universe_captain_picard_superbowl_ad(superbowl_year):
    selector = "div.superbowl_%s div.commercials div.transcript div.picard" % superbowl_year
    if self.is_text_visible("For the Love of Marketing and Earl Grey Tea!", selector):
        return "Picard HubSpot Superbowl Ad 2015"
    elif self.is_text_visible("Delivery Drones... Engage", selector):
        return "Picard Amazon Superbowl Ad 2015"
    elif self.is_text_visible("Bing it on Screen!", selector):
        return "Picard Microsoft Superbowl Ad 2015"
    elif self.is_text_visible("OK Glass, Make it So!", selector):
        return "Picard Google Superbowl Ad 2015"
    elif self.is_text_visible("Number One, I've Never Seen Anything Like It.", selector):
        return "Picard Tesla Superbowl Ad 2015"
    elif self.is_text_visible("""With the first link, the chain is forged.
                              The first speech censored, the first thought forbidden,
                              the first freedom denied, chains us all irrevocably.""", selector):
        return "Picard Wikimedia Superbowl Ad 2015"
    elif self.is_text_visible("Let us make sure history never forgets the name ... Facebook", selector):
        return "Picard Facebook Superbowl Ad 2015"
    else:
        raise Exception("Reports of my assimilation are greatly exaggerated.")
```

#### Typing Text

update_text_value(selector, text)  # updates the text from the specified element with the specified value. Exception raised if element missing or field not editable. Example:

```python
self.update_text_value("input#id_value", "2012")
```

You can also use the WebDriver .send_keys() command, but it won't clear the text box first if there's already text inside.
If you want to type in special keys, that's easy too. Here's an example:

```python
from selenium.webdriver.common.keys import Keys
self.wait_for_element_visible("textarea").send_keys(Keys.SPACE + Keys.BACK_SPACE + '\n')  # the backspace should cancel out the space, leaving you with the newline
```

#### Switching Tabs

So what if your test opens up a new tab/window and now you have more than one page? No problem. You just need to specify which one you currently want Selenium to use. Switching between them is easy:
Ex:

```python
self.driver.switch_to_window(self.driver.window_handles[1])  # this switches to the new tab
```

driver.window_handles is a list that will continually get updated when new windows/tabs appear (index numbering is auto-incrementing from 0, which represents the main window)

**ProTip™:** iFrames follow the same principle as new windows - you need to specify the iFrame if you want to take action on something in there
Ex:

```python
self.driver.switch_to_frame('ContentManagerTextBody_ifr')
# Now you can act inside the iFrame
# Do something cool (here)
self.driver.switch_to_default_content()  # exit the iFrame when you're done
```

#### Executing Custom jQuery Scripts:

jQuery is a powerful JavaScript library that allows you to perform advanced actions in a web browser.
If the web page you're on already has jQuery loaded, you can start executing jQuery scripts immediately.
You'd know this because the web page would contain something like the following in the HTML:

```html
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
```

It's OK if you want to use jQuery on a page that doesn't have it loaded yet. To do so, you need to run the following command first:

```python
self.driver.execute_script('var script = document.createElement("script"); script.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"; document.getElementsByTagName("head")[0].appendChild(script);')
```

Here are some examples:
```python
self.driver.execute_script('jQuery, window.scrollTo(0, 600)')  # Scrolling the page

self.driver.execute_script("jQuery('#annoying-widget').hide()")  # Hiding elements on a page

self.driver.execute_script("jQuery('#annoying-button a').remove()")  # Removing elements on a page

self.driver.execute_script("jQuery('%s').mouseover()" % (mouse_over_item))  # Mouse-over elements on a page

self.driver.execute_script("jQuery('input#the_id').val('my_text')")  # Fast text input on a page

self.driver.execute_script("jQuery('div#dropdown a.link').click()")  # Click elements on a page

self.driver.execute_script("return jQuery('div#amazing')[0].text")  # Returns the css "text" of the element given

self.driver.execute_script("return jQuery('textarea')[2].value")  # Returns the css "value" of the 3rd textarea element on the page
```

In the following more-complex example, jQuery is used to plant code on a page that Selenium can then touch after that:
```python
self.driver.get(SOME_PAGE_TO_PLAY_WITH)
referral_link = '<a class="analytics test" href="%s">Free-Referral Button!</a>' % DESTINATION_URL
self.driver.execute_script("document.body.innerHTML = \"%s\"" % referral_link)
self.driver.find_element_by_css_selector("a.analytics").click()  # Clicks the generated button
```

## Part III: Explanations + Advanced Abilities 

So by now you may be wondering how the nosetests code works? Nosetests will automatically run any test that starts with "test" from the file you selected. You can also be more specific and run specific tests in a file or any test in a specific class. For example, the code in the early examples could've been run using "nosetests my_first_test.py:MyTestClass.test_basic ... ...". If you just wanted to run all tests in MyTestClass, you can use: "nosetests my_first_test.py:MyTestClass ... ...", which is useful when you have multiple tests in the same file. Don't forget the plugins. (In the beginning example, since there was only one test in that file, this won't change anything.) And if you want better logging in the console output, that's what the "-s" is for.

To use the test framework calls, don't forget to include the following import:

```python
from test_framework.fixtures import base_case
```

And you'll need to inherit the base case in your classes like so:

```python
class MyTestClass(base_case.BaseCase):
```

To understand the full scope of the test framework, we have to take a peek inside. From the top-level folder that contained the requirements.pip and setup.py files, there are two other major folders: "grid" and "test_framework". The Selenium "Grid" is what maintains the remote machines running selenium tests for "selenium.hubteam.com/jenkins". Machines can be spun up through Amazon EC2, and each one is capable of running 5 simultaneous browser tests. The other major folder, "test_framework", is what contains everything else. The "test_framework" folder contains all the major components such as "Core", "Fixtures", and "Plugins". For all intensive purposes, those sections are all equally important. They contain all the code and libraries that make our test framework useful (because otherwise we'd just be writing tests using raw selenium calls without any special add-ons or support).


####  Checking Email: 
So let's say you have a test that sends an email, and now you want to check that the email was received:

```python
from test_framework.fixtures.email_manager import EmailManager, EmailException
num_email_results = 0
email_subject = "This is the subject to search for (maybe include a timestamp)"
email_manager = EmailManager("[YOUR SELENIUM GMAIL EMAIL ADDRESS]")  # the password for this is elsewhere (in the library) because this is a default email account
try:
    html_text = email_manager.search(SUBJECT="%s" % email_subject, timeout=300)
    num_email_results = len(html_text)
except EmailException:
    num_email_results = 0
self.assertTrue(num_email_results)  # true if not zero
```

Now you can parse through the email if you're looking for specific text or want to navigate to a link listed there.


####  Database Powers: 
Let's say you have a test that needs to access the database. First make sure you already have a table ready. Then, Boom:
Ex:

```python
from test_framework.core.mysql import DatabaseManager
def write_data_to_db(self, theId, theValue, theUrl):
    db = DatabaseManager()
    query = """INSERT INTO myTable(theId,theValue,theUrl)
               VALUES (%(theId)s,%(theValue)s,%(theUrl)s)"""
    db.execute_query_and_close(query, {"theId":theId,
                               "theValue":theValue,
                               "theUrl":theUrl})
```

Access credentials are stored in your library file for your convenience (you have to add them first).

The following example below (taken from the Delayed Data Manager) shows how data can be pulled from the database.

```python
import logging
from test_framework.core.mysql import DatabaseManager

def get_delayed_test_data(self, testcase_address, done=0):
    """ Returns a list of rows """
    db = DatabaseManager()
    query = """SELECT guid,testcaseAddress,insertedAt,expectedResult,done
               FROM delayedTestData
               WHERE testcaseAddress=%(testcase_address)s
               AND done=%(done)s"""
    data = db.fetchall_query_and_close(query, {"testcase_address":testcase_address, "done":done})
    if data:
        return data
    else:
        logging.debug("Could not find any rows in delayedTestData.")
        logging.debug("DB Query = " + query % {"testcase_address":testcase_address, "done":done})
        return []
```

And now you know how to pull data from the DB.

You may also be wondering when you would use the Delayed Data Manager. Here's one example: If you scheduled an email to go out 12 hours from now and you wanted to check that the email gets received (but you don't want the Selenium test of a Jenkins job to sit idle for 12 hours) you can store the email credentials as a unique time-stamp for the email subject in the DB (along with a time for when it's safe for the email to be searched for) and then a later-running test can do the checking after the right amount of time has passed.


Congratulations! If you've made it this far, it means you have a pretty good idea about how to move forward!
Feel free to check out other exciting open source projects on GitHub:
[https://github.com/hubspot](https://github.com/hubspot)

Happy Automating!

~ Michael Mintz (AKA MintzWorld / DrSelenium / your friendly neighborhood automation wizard)


### Legal Disclaimer
Automation is a powerful tool. It allows you to take full control of web browsers and do just about anything that a human could do, but faster. It can be used for both good and evil. With great power comes great responsibility. You are fully responsible for how you use this framework and the automation that you create. You may also want to see an expert when it comes to setting up your automation environment if you require assistance.
