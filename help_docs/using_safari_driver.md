### Info about using Safari Driver for running automated tests on macOS

(NOTE: SafariDriver requires Safari 10 running on OS X 10.11 El Capitan or greater)

You can find info on Safari Driver if you scroll down to that section on the [SeleniumHQ downloads page](https://www.seleniumhq.org/download/).

That page will tell you to [download the required Safari Driver browser extension (SafariDriver.safariextz) here at this link](http://selenium-release.storage.googleapis.com/index.html?path=2.48/).

For that to work, you'll need to [download the Standalone Selenium Server from here](http://docs.seleniumhq.org/download/) and put that JAR file in ``/usr/local/bin/``. To make the next step easier, rename the downloaded JAR file to ``selenium-server-standalone.jar`` (if it's not already called that).

Next, configure the Selenium Server JAR file into your PATH like this:

```bash
export SELENIUM_SERVER_JAR=/usr/local/bin/selenium-server-standalone.jar
export PATH=$PATH:/usr/local/bin/selenium-server-standalone.jar
```

Now you're ready to run automated tests on Safari if you use ``--browser=safari`` on the command line when running your tests/scripts with SeleniumBase.
