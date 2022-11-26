<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) Verifying that web drivers are installed

On newer versions of SeleniumBase, the driver is automatically downloaded to the ``seleniumbase/drivers`` folder as needed, and does not need to be on the System Path when running tests.

Drivers can be manually downloaded to the ``seleniumbase/drivers`` folder with commands such as:

```bash
sbase get chromedriver
sbase get chromedriver latest
sbase get geckodriver
sbase get edgedriver
```

--------

If you want to check that you have the correct driver installed on your System PATH (which is no longer necessary unless using the Selenium Grid), then continue reading below:

*This assumes you've already downloaded a driver to your **System PATH** with a command such as:*

```bash
sbase get chromedriver --path
```

(The above ``--path`` addition is for Linux/Mac only, which uses ``/usr/local/bin/``. The "Path" is different on Windows, and you'll need to manually copy the driver to your System Path, which is defined in the Control Panel's System Environment Variables.)

*You can verify that the correct drivers exist on your System Path by checking inside a Python command prompt.*

#### Verifying ChromeDriver

```bash
python
```

```python
>>> from seleniumbase import get_driver
>>> driver = get_driver("chrome", headless=False)
>>> driver.get("https://www.google.com/chrome")
>>> driver.quit()
>>> exit()
```

#### Verifying Geckodriver (Firefox WebDriver)

```bash
python
```

```python
>>> from seleniumbase import get_driver
>>> driver = get_driver("firefox", headless=False)
>>> driver.get("https://www.mozilla.org/firefox")
>>> driver.quit()
>>> exit()
```

#### Verifying WebDriver for Safari

```bash
python
```

```python
>>> from seleniumbase import get_driver
>>> driver = get_driver("safari", headless=False)
>>> driver.get("https://www.apple.com/safari")
>>> driver.quit()
>>> exit()
```
