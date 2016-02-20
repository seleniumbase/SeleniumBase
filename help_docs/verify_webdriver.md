### Verify that web drivers were successfully installed

*You can do this by checking inside a Python command prompt. (NOTE: xkcd is a webcomic)*

#### Verifying FirefoxDriver (comes with Selenium by default)
```bash
python
>>> from selenium import webdriver
>>> browser = webdriver.Firefox()
>>> browser.get("http://xkcd.com/1337/")
>>> browser.close()
>>> exit()
```

#### Verifying ChromeDriver (you had to install this separately)
```bash
python
>>> from selenium import webdriver
>>> browser = webdriver.Chrome()
>>> browser.get("http://xkcd.com/1337/")
>>> browser.close()
>>> exit()
```
