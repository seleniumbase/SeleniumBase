## Converting Katalon/Selenium IDE recordings into SeleniumBase test scripts

[Katelon Recorder / Selenium IDE](https://www.katalon.com/resources-center/blog/katalon-automation-recorder/) (<i>the successor to the [old Selenium IDE](http://docs.seleniumhq.org/projects/ide/)</i>) is a tool that allows you to record and playback actions performed inside a web browser. It's available as a [downloadable Chrome extension](https://chrome.google.com/webstore/detail/katalon-recorder-selenium/ljdobmomdgdljniojadhoplhkpialdid) and a [downloadable Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/katalon-automation-record/). Katelon Recorder comes with an option to export recordings as various WebDriver test scripts, one of which is ``Python 2 (WebDriver + unittest)``. Unfortunately, these natively-exported scripts can be very messy and don't always run reliably. The purpose of this converter is to clean up and improve the scripts so that they can be used in production-level environments.

#### Step 1: Make a recording with Katelon Recorder

![](https://cdn2.hubspot.net/hubfs/100006/images/katalon_recorder_2.png "Katelon Recorder example")

#### Step 2: Export your recording as a Python 2 Webdriver script

* ``{} Export`` => ``Python 2 (WebDriver + unittest)`` => ``Save As File``

#### Step 3: Run ``seleniumbase convert`` on your exported Python file

```
seleniumbase convert [MY_TEST.py]
```

* You should see a [MY_TEST_SB.py] file appear in the folder. (``_SB`` is added to the file name so that the original file stays intact in case you still need it.) This new clean & reliable SeleniumBase test script is ready to be added into your test suite for running.
