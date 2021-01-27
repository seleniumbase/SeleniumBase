[<img src="https://seleniumbase.io/cdn/img/sb_logo_b.png" title="SeleniumBase" width="360">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Installing webdrivers</h2>

To run web automation, you'll need webdrivers for each browser you plan on using. Here are some commands that'll automatically download the driver you need into the SeleniumBase ``drivers`` folder once you've installed SeleniumBase:

```bash
sbase install chromedriver
sbase install geckodriver
sbase install edgedriver
sbase install iedriver
sbase install operadriver
```

* If you have the latest version of Chrome installed, get the latest chromedriver (<i>otherwise it defaults to chromedriver 2.44 for compatibility reasons</i>):

```bash
sbase install chromedriver latest
```

* You can also install a specific version of chromedriver for a specific version of Chrome:

```bash
sbase install chromedriver 88.0.4324.96

sbase install chromedriver 88
```

If you plan on using the [Selenium Grid integration](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md) (which allows for remote webdriver), you'll need to put the drivers on your System PATH. On macOS and Linux, ``/usr/local/bin`` is a good PATH spot. On Windows, you may need to set the System PATH under Environment Variables to include the location where you placed the driver files. As a shortcut, you could place the driver files into your Python ``Scripts/`` folder in the location where you have Python installed, which should already be on your System PATH.

Here's where you can go to manually install web drivers from the source:

* For Chrome, get [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) on your System PATH.

* For Firefox, get [Geckodriver](https://github.com/mozilla/geckodriver/releases) on your System PATH.

* For Microsoft Edge, get [Edge Driver (Microsoft WebDriver)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) on your System PATH.

* For Safari, get [Safari Driver](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/using_safari_driver.md) on your System PATH.

* For Opera, get [Opera Chromium Driver](https://github.com/operasoftware/operachromiumdriver/releases) on your System PATH..

* For PhantomJS headless browser automation, get [PhantomJS](http://phantomjs.org/download.html) on your System PATH. (NOTE: <i>PhantomJS is no longer officially supported by SeleniumHQ</i>)

**macOS shortcuts**:

* You can also install drivers by using ``brew`` (aka ``homebrew``), but you'll need to install that first. [Brew installation instructions are here](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/install_python_pip_git.md).

```bash
brew cask install chromedriver

brew install geckodriver
```

You can also upgrade existing webdrivers:

```bash
brew cask upgrade chromedriver

brew upgrade geckodriver
```

**Linux shortcuts**:

If you still need the web drivers, here are some scripts to help you install chromedriver and geckodriver on a Linux machine:

```bash
wget http://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
```

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar xvfz geckodriver-v0.26.0-linux64.tar.gz
mv geckodriver /usr/local/bin/
chmod +x /usr/local/bin/geckodriver
```

* If you wish to verify that web drivers are working, **[follow these instructions](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/verify_webdriver.md)**.
