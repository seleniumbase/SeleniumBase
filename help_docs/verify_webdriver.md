### Verify that web drivers were successfully installed

*You can do this by checking inside a Python command prompt. (NOTE: xkcd is a webcomic)*

#### Verifying ChromeDriver
```bash
python
>>> from selenium import webdriver
>>> browser = webdriver.Chrome()
>>> browser.get("http://xkcd.com/1337/")
>>> browser.close()
>>> exit()
```

#### Verifying FirefoxDriver (Geckodriver)
```bash
python
>>> from selenium import webdriver
>>> browser = webdriver.Firefox()
>>> browser.get("http://xkcd.com/1337/")
>>> browser.close()
>>> exit()
```
