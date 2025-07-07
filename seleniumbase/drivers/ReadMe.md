<!-- SeleniumBase Docs -->

## <img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> SeleniumBase driver storage

To run web automation, you'll need webdrivers for each browser you plan on using.  With SeleniumBase, drivers are downloaded automatically as needed into the SeleniumBase `drivers` folder.

🎛️ You can also download drivers manually with these commands:

```zsh
seleniumbase get chromedriver
seleniumbase get geckodriver
seleniumbase get edgedriver
```

After running the commands above, web drivers will get downloaded into the `seleniumbase/drivers/` folder. SeleniumBase uses those drivers during tests. (The drivers don't come with SeleniumBase by default.)

If the necessary driver is not found in this location while running tests, SeleniumBase will instead look for the driver on the System PATH. If the necessary driver is not on the System PATH either, SeleniumBase will automatically attempt to download the required driver.

🎛️ You can also download specific versions of drivers. Examples:

```zsh
sbase get chromedriver 114
sbase get chromedriver 114.0.5735.90
sbase get chromedriver stable
sbase get chromedriver beta
sbase get chromedriver dev
sbase get chromedriver canary
sbase get chromedriver previous  # One major version before the stable version
sbase get chromedriver mlatest  # Milestone latest version for detected browser
sbase get edgedriver 115.0.1901.183
```

(NOTE: `sbase` is a shortcut for `seleniumbase`)

--------

**Browser Binaries**:

🎛️ Use the `sbase get` command to download the `Chrome for Testing` and `Chrome-Headless-Shell` browser binaries. Example:

```zsh
sbase get cft  # (For `Chrome for Testing`)
sbase get chs  # (For `Chrome-Headless-Shell`)
```

Those commands download those binaries into the `seleniumbase/drivers` folder.
To use the binaries from there in SeleniumBase scripts, set the `binary_location` to `cft` or `chs`.

(Source: https://googlechromelabs.github.io/chrome-for-testing/)

--------

[<img src="https://seleniumbase.github.io/cdn/img/sb_logo_b.png" title="SeleniumBase" width="280">](https://github.com/seleniumbase/SeleniumBase)
