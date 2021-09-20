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
