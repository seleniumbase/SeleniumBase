### <img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> SeleniumBase webdriver storage

* You need a different webdriver for each web browser you want to run automation on: ``chromedriver`` for Chrome, ``edgedriver`` for Edge, ``geckodriver`` for Firefox, ``operadriver`` for Opera, and ``iedriver`` for Internet Explorer.

```
seleniumbase install chromedriver
seleniumbase install geckodriver
seleniumbase install edgedriver
seleniumbase install iedriver
seleniumbase install operadriver
```
After running the commands above, web drivers will get downloaded into this folder. SeleniumBase will then use those drivers during test runs if present. (The drivers don't come with SeleniumBase by default.)

* If you have the latest version of Chrome installed, get the latest chromedriver (<i>otherwise it defaults to chromedriver 2.44 for compatibility reasons</i>):
```bash
seleniumbase install chromedriver latest
```

If the necessary driver is not found in this location while running tests, SeleniumBase will instead look for the driver on the System PATH. If the necessary driver is not on the System PATH either, SeleniumBase will automatically attempt to download the required driver.
