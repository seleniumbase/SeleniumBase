### Converting Katalon recordings into SeleniumBase test scripts

### (NOTE: **[SeleniumBase now has Recorder Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/recorder_mode.md)**, which is recommended over other record & playback tools.)

--------

Katalon Recorder (Selenium IDE) is a tool that allows you to record and playback actions performed inside a web browser. It's available as a [downloadable Chrome extension](https://chrome.google.com/webstore/detail/katalon-recorder-selenium/ljdobmomdgdljniojadhoplhkpialdid) and a [downloadable Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/katalon-automation-record/). The Katalon Recorder comes with an option to export recordings as various WebDriver test scripts, one of which is ``Python 2 (WebDriver + unittest)``. Unfortunately, these natively-exported scripts can be very messy and don't always run reliably. The purpose of this converter is to clean up and improve the scripts so that they can be used in production-level environments.

#### Step 1: Make a recording with the Katalon Recorder

![](https://seleniumbase.io/cdn/img/katalon_recorder_2.png "Katalon Recorder example")

#### Step 2: Export your recording as a Python 2 Webdriver script

* ``{} Export`` => ``Python 2 (WebDriver + unittest)`` => ``Save As File``

#### Step 3: Run ``seleniumbase convert`` on your exported Python file

```bash
seleniumbase convert MY_TEST.py
```

* You should see a [MY_TEST_SB.py] file appear in the folder. (``_SB`` is added to the file name so that the original file stays intact in case you still need it.) This new clean & reliable SeleniumBase test script is ready to be added into your test suite for running.

--------

--------

The following is an example of a Katalon Recorder exported file (**WebDriver + unittest format**).
It is **messy** and has **unnecessary lines of code** to do the task that was recorded:

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Swag(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_swag(self):
        driver = self.driver
        driver.get("https://www.saucedemo.com/")
        driver.find_element_by_id("user-name").click()
        driver.find_element_by_id("user-name").clear()
        driver.find_element_by_id("user-name").send_keys("standard_user")
        driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("secret_sauce")
        driver.find_element_by_id("login-button").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
```

<div><b>This can be improved on...</b></div>

<b>After running <code>seleniumbase convert [FILE.py]</code> on it, here is the new result:</b>

```python
# -*- coding: utf-8 -*-
from seleniumbase import BaseCase


class Swag(BaseCase):

    def test_swag(self):
        self.open('https://www.saucedemo.com/')
        self.type('#user-name', 'standard_user')
        self.type('#password', 'secret_sauce')
        self.click('#login-button')
```

<b>This is much cleaner than the original version.
It also uses the more reliable SeleniumBase methods.</b>
