<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) Installing webdrivers

To run web automation, you'll need webdrivers for each browser you plan on using.  With SeleniumBase, drivers are downloaded automatically as needed into the SeleniumBase ``drivers`` folder.

You can also download drivers manually with these commands:

```bash
seleniumbase get chromedriver
seleniumbase get geckodriver
seleniumbase get edgedriver
```

After running the commands above, web drivers will get downloaded into the ``seleniumbase/drivers/`` folder. SeleniumBase uses those drivers during tests. (The drivers don't come with SeleniumBase by default.)

If the necessary driver is not found in this location while running tests, SeleniumBase will instead look for the driver on the System PATH. If the necessary driver is not on the System PATH either, SeleniumBase will automatically attempt to download the required driver.

* You can also download specific versions of drivers. Examples:

```bash
sbase get chromedriver 107
sbase get chromedriver 107.0.5304.62
sbase get chromedriver latest
sbase get chromedriver latest-1
sbase get edgedriver 106.0.1370.42
```

(NOTE: ``sbase`` is a shortcut for ``seleniumbase``)

--------

If you plan on using the [Selenium Grid integration](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md) (which allows for ``remote`` webdriver), you'll need to put the drivers on your System PATH. On macOS and Linux, ``/usr/local/bin`` is a good PATH spot. On Windows, you may need to set the System PATH under Environment Variables to include the location where you placed the driver files. As a shortcut, you could place the driver files into your Python ``Scripts/`` folder in the location where you have Python installed, which should already be on your System PATH.

Here's where you can go to manually get web drivers from the source:

* For Chrome, get [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) on your System PATH.

* For Edge, get [Edge Driver (Microsoft WebDriver)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) on your System PATH.

* For Firefox, get [Geckodriver](https://github.com/mozilla/geckodriver/releases) on your System PATH.

* For Safari, get [Safari Driver](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/using_safari_driver.md) on your System PATH.

**macOS shortcuts**:

* You can also install drivers by using ``brew`` (aka ``homebrew``):

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

If you still need the web drivers, here are some scripts to help you get ``chromedriver`` and ``geckodriver`` on a Linux machine:

```bash
wget https://chromedriver.storage.googleapis.com/72.0.3626.69/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
```

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz
tar xvfz geckodriver-v0.32.0-linux64.tar.gz
mv geckodriver /usr/local/bin/
chmod +x /usr/local/bin/geckodriver
```

To verify that web drivers are working, **[follow these instructions](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/verify_webdriver.md)**.

[<img src="https://seleniumbase.github.io/cdn/img/sb_logo_b.png" title="SeleniumBase" width="280">](https://github.com/seleniumbase/SeleniumBase)
