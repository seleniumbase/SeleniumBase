## Verifying that web drivers are installed

*You can do this by checking inside a Python command prompt.*

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
