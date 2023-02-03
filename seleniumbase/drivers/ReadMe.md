### <img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> SeleniumBase webdriver storage

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
