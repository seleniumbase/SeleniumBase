## [<img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) Installing webdrivers

To run web automation, you'll need webdrivers for each browser you plan on using.  With SeleniumBase, drivers are downloaded automatically as needed into the SeleniumBase ``drivers`` folder.

You can also download drivers manually with these commands:

```bash
sbase get chromedriver
sbase get geckodriver
sbase get edgedriver
```

* ``sbase get chromedriver`` automatically tries to detect the version you need. If it can't, it defaults to ``chromedriver 72.0.3626.69`` for compatibility reasons. To force getting the latest version, use:

```bash
sbase get chromedriver latest
```

* You can also get a specific version of chromedriver for a specific version of Chrome:

```bash
sbase get chromedriver 102.0.5005.61

sbase get chromedriver 102
```

* On Linux, you can run the following two commands (once you've installed SeleniumBase) to automatically upgrade your Chromedriver to match your version of Chrome: (``wget`` downloads the file, and ``pytest`` runs it.)

```bash
wget https://raw.githubusercontent.com/seleniumbase/SeleniumBase/master/examples/upgrade_chromedriver.py
pytest upgrade_chromedriver.py -s
```

* If you run a test without the correct webdriver available, the driver will be downloaded automatically.

If you plan on using the [Selenium Grid integration](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md) (which allows for remote webdriver), you'll need to put the drivers on your System PATH. On macOS and Linux, ``/usr/local/bin`` is a good PATH spot. On Windows, you may need to set the System PATH under Environment Variables to include the location where you placed the driver files. As a shortcut, you could place the driver files into your Python ``Scripts/`` folder in the location where you have Python installed, which should already be on your System PATH.

Here's where you can go to manually get web drivers from the source:

* For Chrome, get [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) on your System PATH.

* For Firefox, get [Geckodriver](https://github.com/mozilla/geckodriver/releases) on your System PATH.

* For Microsoft Edge, get [Edge Driver (Microsoft WebDriver)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) on your System PATH.

* For Safari, get [Safari Driver](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/using_safari_driver.md) on your System PATH.

* For Opera, get [Opera Chromium Driver](https://github.com/operasoftware/operachromiumdriver/releases) on your System PATH..

* For PhantomJS headless browser automation, get [PhantomJS](http://phantomjs.org/download.html) on your System PATH. (NOTE: <i>PhantomJS is no longer officially supported by SeleniumHQ</i>)

**macOS shortcuts**:

* You can also install drivers by using ``brew`` (aka ``homebrew``), but you'll need to install that first. [Brew installation instructions are here](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/install_python_pip_git.md).

```bash
brew install --cask chromedriver

brew install geckodriver
```

You can also upgrade existing webdrivers:

```bash
brew upgrade --cask chromedriver

brew upgrade geckodriver
```

**Linux shortcuts**:

If you still need the web drivers, here are some scripts to help you get chromedriver and geckodriver on a Linux machine:

```bash
wget https://chromedriver.storage.googleapis.com/72.0.3626.69/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
```

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
tar xvfz geckodriver-v0.31.0-linux64.tar.gz
mv geckodriver /usr/local/bin/
chmod +x /usr/local/bin/geckodriver
```

* If you wish to verify that web drivers are working, **[follow these instructions](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/verify_webdriver.md)**.

[<img src="https://seleniumbase.io/cdn/img/sb_logo_b.png" title="SeleniumBase" width="280">](https://github.com/seleniumbase/SeleniumBase)
