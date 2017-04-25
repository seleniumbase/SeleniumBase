## Converting Selenium IDE recordings into SeleniumBase test scripts

[Selenium IDE](http://docs.seleniumhq.org/projects/ide/) is a tool that allows you to record and playback actions performed inside a web browser. It's available as a [downloadable Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/). Selenium IDE comes with an option to export recordings as various WebDriver test scripts, one of which is ``Python2/unittest/WebDriver``. Unfortunately, these natively-exported scripts tend to be very messy and don't run reliably. The purpose of this converter is to clean up and improve the scripts so that they can be used in production-level environments.

#### Step 1: Make a recording with Selenium IDE

![](https://cdn2.hubspot.net/hubfs/100006/selenium_ide_example_b.png "Selenium IDE example")

#### Step 2: Export your recording as a Python 2 Webdriver script

* ``File`` => ``Export Test Case As`` => ``Python 2 / unittest / WebDriver``

#### Step 3: Drop your exported file into the ``selenium_ide`` folder

* Just copy & paste!

(The full path of the folder is ``SeleniumBase/integrations/selenium_ide``)

#### Step 4: Run ``convert_ide.py`` on the exported Python script

```bash
python convert_ide.py [MY_TEST.py]
```

You should see a [MY_TEST_SB.py] file appear in the folder. (``_SB`` is added to the file name so that the original file stays intact in case you still need it.)

#### Step 5: Enjoy your new clean & reliable SeleniumBase test script

* You can now copy your new SeleniumBase test script into your test suite. It's ready to be run!
