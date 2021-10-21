## Verifying that web drivers are installed

On newer versions of SeleniumBase, the driver is automatically downloaded to the ``seleniumbase/drivers`` folder, and does not need to be on the System Path when running tests.

Drivers can be manually downloaded with commands such as:

```bash
sbase install chromedriver
sbase install chromedriver latest
sbase install geckodriver
sbase install edgedriver
```

--------

If you want to check that you have the correct driver installed on your System PATH (which is no longer necessary unless using the Selenium Grid), then continue reading below:

*This assumes you've already downloaded a driver to your **System PATH** with a command such as:*

```bash
sbase install chromedriver --path
```

(The above ``--path`` addition is for Linux/Mac only, which uses ``/usr/local/bin/``. The "Path" is different on Windows, and you'll need to manually copy the driver to your System Path, which is defined in the Control Panel's System Environment Variables.)

*You can verify that the correct drivers exist on your System Path by checking inside a Python command prompt.*

#### Verifying ChromeDriver

```bash
python
```

```python
>>> from selenium import webdriver
>>> driver = webdriver.Chrome()
>>> driver.get("https://www.google.com/chrome")
>>> driver.quit()
>>> exit()
```

#### Verifying Geckodriver (Firefox WebDriver)

```bash
python
```

```python
>>> from selenium import webdriver
>>> driver = webdriver.Firefox()
>>> driver.get("https://www.mozilla.org/firefox")
>>> driver.quit()
>>> exit()
```

#### Verifying WebDriver for Safari

```bash
python
```

```python
>>> from selenium import webdriver
>>> driver = webdriver.Safari()
>>> driver.get("https://www.apple.com/safari")
>>> driver.quit()
>>> exit()
```
