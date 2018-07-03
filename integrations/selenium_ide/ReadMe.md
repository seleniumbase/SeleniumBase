## Converting Katalon-based Selenium IDE recordings into SeleniumBase test scripts

[Katelon Recorder / Selenium IDE](https://www.katalon.com/resources-center/blog/katalon-automation-recorder/) (<i>the successor to the [old Selenium IDE](http://docs.seleniumhq.org/projects/ide/)</i>) is a tool that allows you to record and playback actions performed inside a web browser. It's available as a [downloadable Chrome extension](https://chrome.google.com/webstore/detail/katalon-recorder-selenium/ljdobmomdgdljniojadhoplhkpialdid) and a [downloadable Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/katalon-automation-record/). Katelon Recorder comes with an option to export recordings as various WebDriver test scripts, one of which is ``Python 2 (WebDriver + unittest)``. Unfortunately, these natively-exported scripts can be very messy and don't always run reliably. The purpose of this converter is to clean up and improve the scripts so that they can be used in production-level environments.

#### Step 1: Make a recording with Katelon Recorder

![](https://cdn2.hubspot.net/hubfs/100006/images/katalon_recorder_2.png "Katelon Recorder example")

#### Step 2: Export your recording as a Python 2 Webdriver script

* ``{} Export`` => ``Python 2 (WebDriver + unittest)`` => ``Save As File``

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
