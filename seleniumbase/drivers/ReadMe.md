### SeleniumBase web driver storage

#### Usage:

```
seleniumbase install chromedriver
seleniumbase install geckodriver
seleniumbase install edgedriver
seleniumbase install iedriver
seleniumbase install operadriver
```

After running the commands above, web drivers will get downloaded into this folder. SeleniumBase will then use those drivers during test runs if present. (The drivers don't come with SeleniumBase by default.)

If the necessary driver is not found in this location while running tests, SeleniumBase will instead look for the driver on the System PATH. If the necessary driver is not on the System PATH either, you'll get errors.

#### Notes:
* chromedriver allows you to run browser tests on Chrome
* geckodriver allows you to run browser tests on Firefox
* edgedriver allows you to run browser tests on MS Edge
* iedriver allows you to run browser tests on MS IE
* operadriver allows you to run browser tests on Opera
