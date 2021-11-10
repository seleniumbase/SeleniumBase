<h3 align="center"><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.io/cdn/img/sb_logo_10t.png" alt="SeleniumBase" title="SeleniumBase" width="240"></a></h3>

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Recorder Mode</h2>

🔴 <b>SeleniumBase Recorder Mode</b> lets you record & export browser actions into test automation scripts.<br>

<img src="https://seleniumbase.io/cdn/img/sb_recorder_notification.png" title="SeleniumBase" width="380">

(This tutorial assumes that you are using SeleniumBase version ``2.1.6`` or newer.)

🔴 To make a new recording with Recorder Mode, you can use ``sbase mkrec`` or ``sbase codegen``):

```bash
sbase mkrec TEST_NAME.py --url=URL
```

If the file already exists, you'll get an error. If no URL is provided, you'll start on a blank page and will need to navigate somewhere for the Recorder to activate. (The Recorder captures events on URLs that start with ``https``, ``http``, or ``file``.) The command above runs an empty test that stops at a breakpoint so that you can perform manual browser actions for the Recorder. When you have finished recording, type "``c``" on the command-line and press ``[ENTER]`` to let the test continue from the breakpoint. The test will then complete and a file called ``TEST_NAME_rec.py`` will be automatically created in the ``./recordings`` folder. That file will get copied back to the original folder with the name you gave it. (You can run with Edge instead of Chrome by adding ``--edge`` to the command above. For headed Linux machines, add ``--gui`` to prevent the default headless mode on Linux.)

Example:

```bash
sbase mkrec new_test.py --url=wikipedia.org

* RECORDING initialized: new_test.py

pytest new_test.py --rec -q -s --url=wikipedia.org

> .../SeleniumBase/examples/new_test.py(7)test_recording()
      5     def test_recording(self):
      6         if self.recorder_ext and not self.xvfb:
----> 7             import ipdb; ipdb.set_trace()

ipdb> c

>>> RECORDING SAVED as: recordings/new_test_rec.py
**************************************************

*** RECORDING COPIED to: new_test.py
```

🔴 While a recording is in progress, you can press the ``[ESC]`` key to pause the recording. To resume the recording, you can hit the ``[~`]`` key, which is located directly below the ``[ESC]`` key on most keyboards.

🔴 From within Recorder Mode there are two additional modes: "Assert Element Mode" and "Assert Text Mode". To switch into "Assert Element Mode", press the <code>{^}-key (SHIFT+6)</code>: The border will become purple, and you'll be able to click on elements to assert from your test. To switch into "Assert Text Mode", press the <code>{&}-key (SHIFT+7)</code>: The border will become teal, and you'll be able to click on elements for asserting text from your test. While using either of the two special Assertion Modes, certain actions such as clicking on links won't have any effect. This lets you make assertions on elements without navigating away from the page, etc. To add an assertion for a button without triggering its default behavior via a "click" action, mouse-down on the button and then mouse-up somewhere else, which prevents a detected click while still recording the assert. To return back to the original Recorder Mode, press any key other than SHIFT or BACKSPACE (Eg: Press ``CONTROL``, etc.). You can also press ESC once to leave the Assertion Modes, but if you press it again, it'll stop the Recorder.

🔴 For extra flexibility, the ``sbase mkrec`` command can be split into four separate commands:

```bash
sbase mkfile TEST_NAME.py --rec

pytest TEST_NAME.py --rec -q -s

sbase print ./recordings/TEST_NAME_rec.py -n

cp ./recordings/TEST_NAME_rec.py ./TEST_NAME.py
```

The first command creates a boilerplate test with a breakpoint; the second command runs the test with the Recorder activated; the third command prints the completed test to the console; and the fourth command replaces the initial boilerplate with the completed test. If you're just experimenting with the Recorder, you can run the second command as many times as you want, and it'll override previous recordings saved to ``./recordings/TEST_NAME_rec.py``. (Note that ``-s`` is needed to allow breakpoints, unless you already have a ``pytest.ini`` file present with ``addopts = --capture=no`` in it. The ``-q`` is optional, which shortens ``pytest`` console output.)

🔴 You can also use the Recorder to add code to an existing test. To do that, you'll first need to create a breakpoint in your code where you want to insert manual browser actions:

```python
import ipdb; ipdb.set_trace()
```

Now you'll be able to run your test with ``pytest``, and it will stop at the breakpoint for you to add in actions: (Press ``c`` and ``ENTER`` on the command-line to continue from the breakpoint.)

```bash
pytest TEST_NAME.py --rec -s
```

🔴 You can also set a breakpoint at the start of your test by adding ``--trace`` as a ``pytest`` command-line option: (This is useful when running Recorder Mode without any ``ipdb`` breakpoints.)

```bash
pytest TEST_NAME.py --trace --rec -s
```

🔴 After the test completes, a file called ``TEST_NAME_rec.py`` will be automatically created in the ``./recordings`` folder, which will include the actions performed by the test, and the manual actions that you added in.

🔴 Here's a command-line notification for a completed recording:

```bash
>>> RECORDING SAVED as: recordings/TEST_NAME_rec.py
***************************************************
```

🔴 When running additional tests from the same Python module, Recordings will get added to the file that was created from the first test:

```bash
>>> RECORDING ADDED to: recordings/TEST_NAME_rec.py
***************************************************
```

🔴 Recorder Mode works by saving your recorded actions into the browser's <code>sessionStorage</code>. SeleniumBase then reads from the browser's <code>sessionStorage</code> to take the raw data and generate a full test from it. Keep in mind that <code>sessionStorage</code> is only present for a website while the browser tab remains on a web page of the same domain/origin. If you leave that domain/origin, the <code>sessionStorage</code> of that tab will no longer have the raw data that SeleniumBase needs to create a full recording. To compensate for this, all links to web pages of a different domain/origin will automatically open a new tab for you while in Recorder Mode. Additionally, the SeleniumBase <code>self.open(URL)</code> method will also open a new tab for you in Recorder Mode if the domain/origin is different from the current URL. If you need to navigate to a different domain/origin from within the same tab, call <code>self.save_recorded_actions()</code> first, which saves the recorded data for later. When the recorded test completes, SeleniumBase will scan the <code>sessionStorage</code> of all open browser tabs for the data it needs to generate the complete SeleniumBase automation script.

🔴 As an alternative to activating Recorder Mode with the <code>--rec</code> command-line arg, you can also call <code>self.activate_recorder()</code> from your tests. This is only useful for tests that stay on the same URL because the Recorder will turn off when leaving the page where you activated the Recorder. The reason for this is because the standard Recorder Mode functions as a Chrome extension (and persists wherever the browser goes), whereas the method call version of Recorder Mode only lives in the page where it was called.

🔴 (Note that <b>same domain/origin</b> is not the same as <b>same URL</b>. Example: <a href="https://xkcd.com/353/" target="_blank">https://xkcd.com/353</a> and <a href="https://xkcd.com/1537/" target="_blank">https://xkcd.com/1537</a> are two different URLs with the <b>same domain/origin</b>. That means that both URLs will share the same <code>sessionStorage</code> data, and that any changes to <code>sessionStorage</code> from one URL will carry on to the <code>sessionStorage</code> of a different URL when the domain/origin is the same. If you want to find out a website's origin during a test, just call: <code>self.get_origin()</code>, which returns the value of <code>window.location.origin</code> from the browser's console.)

🔴 Inside recorded tests, you might find the <code>self.open_if_not_url(URL)</code> method, which opens the URL given if the browser is not currently on that page. This is used as a method in recorded scripts when SeleniumBase detects that a browser action (such as a click) has brought the test to that page. This method not only prevents an extra page load if not needed, but it also lets people know what page the test went to after a browser action was performed.

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
