#### **Step 0a:** Setup your [![Python version](https://img.shields.io/badge/python-2.7,_3.*-22AADD.svg "Python version")](https://docs.python.org/2/) Python/pip environment:

* To install ``python``, ``pip``, ``git``, and either ``virtualenv`` or ``virtualenvwrapper``, **[follow these instructions](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/requirements_installation.md)**.


#### **Step 0b:** Install web browsers to run automation on:

* Download & install web browsers such as [Chrome](https://www.google.com/chrome/browser/desktop/index.html) and/or [Firefox](https://www.mozilla.org/firefox/new/).


#### **Step 0c:** Get web drivers for each browser you intend to run automation on:

To run automation on various web browsers, you'll need to download a driver file for each one and place it on your System **[PATH](http://java.com/en/download/help/path.xml)**. On a Mac, ``/usr/local/bin`` is a good spot. On Windows, make sure you set the System Path under Environment Variables to include the location where you placed the driver files:

* For Chrome, get [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) on your System Path. (**Version 2.32 or above is recommended!**)

* For Firefox, get [Geckodriver](https://github.com/mozilla/geckodriver/releases) on your System Path.

* For Microsoft Edge, get [Edge Driver (Microsoft WebDriver)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) on your System Path.

* For Safari, get [Safari Driver](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/using_safari_driver.md) on your System Path.

* For PhantomJS headless browser automation, get [PhantomJS](http://phantomjs.org/download.html) on your System Path.

Mac:

* On a Mac, you can install drivers more easily by using ``brew`` (aka ``homebrew``), but you have to install that first. [Brew installation instructions are here](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/requirements_installation.md).

```bash
brew install chromedriver phantomjs
```

(NOTE: If your existing version of chromedriver is less than 2.32, **upgrading is recommended!**)

```bash
brew upgrade chromedriver
```

* To verify that the web drivers are working, **[follow these instructions](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/verify_webdriver.md)**.
