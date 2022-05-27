### <img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> SeleniumBase webdriver storage

* You need a different webdriver for each web browser you want to run automation on: ``chromedriver`` for Chrome, ``edgedriver`` for Edge, ``geckodriver`` for Firefox, ``operadriver`` for Opera, and ``iedriver`` for Internet Explorer.

```bash
seleniumbase get chromedriver
seleniumbase get geckodriver
seleniumbase get edgedriver
seleniumbase get iedriver
seleniumbase get operadriver
```

After running the commands above, web drivers will get downloaded into this folder. SeleniumBase will then use those drivers during tests if present. (The drivers don't come with SeleniumBase by default.)

* If you have the latest version of Chrome installed, get the latest chromedriver (<i>otherwise it defaults to chromedriver 72.0.3626.69 for compatibility reasons</i>):

```bash
sbase get chromedriver latest
```

If the necessary driver is not found in this location while running tests, SeleniumBase will instead look for the driver on the System PATH. If the necessary driver is not on the System PATH either, SeleniumBase will automatically attempt to download the required driver.

* You can also download specific versions of drivers. Examples:

```bash
sbase get chromedriver 101
sbase get chromedriver 101.0.4951.41
sbase get chromedriver latest-1
sbase get edgedriver 101.0.1210.32
```
