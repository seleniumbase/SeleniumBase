<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) Recorder Mode 🔴/⏺️

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=eKN5nq7YbdM"><img src="http://img.youtube.com/vi/eKN5nq7YbdM/0.jpg" title="SeleniumBase on YouTube" width="285" /></a>
<!-- GitHub Only --><p>(<b><a href="https://www.youtube.com/watch?v=eKN5nq7YbdM">Watch the tutorial on YouTube</a></b>)</p>

🔴 <b>SeleniumBase Recorder Mode</b> lets you record & export browser actions into test automation scripts.<br>

<img src="https://seleniumbase.github.io/cdn/img/sb_recorder_notification.png" title="SeleniumBase" width="380">

⏺️ To make a new recording with Recorder Mode, use ``sbase mkrec``, ``sbase codegen``, or ``sbase record``):

```bash
sbase mkrec TEST_NAME.py --url=URL
```

If the file already exists, you'll get an error. If no URL is provided, you'll start on a blank page and will need to navigate somewhere for the Recorder to activate. (The Recorder captures events on URLs that start with ``https``, ``http``, or ``file``.) The command above runs an empty test that stops at a breakpoint so that you can perform manual browser actions for the Recorder. When you have finished recording, type "``c``" on the command-line and press ``[ENTER]`` to continue from the breakpoint. The test will complete and a file called ``TEST_NAME_rec.py`` will be automatically created in the ``./recordings`` folder. That file will get copied back to the original folder with the name you gave it. (You can run with Edge instead of Chrome by adding ``--edge`` to the command above. For headed Linux machines, add ``--gui`` to prevent the default headless mode on Linux.)

Example:

```bash
sbase mkrec new_test.py --url=wikipedia.org

* RECORDING initialized: new_test.py

pytest new_test.py --rec -q -s --url=wikipedia.org

>>>>>>>>>>>>>>>>>> PDB set_trace >>>>>>>>>>>>>>>>>

> PATH_TO_YOUR_CURRENT_DIRECTORY/new_test.py(9)
   .
   5         def test_recording(self):
   6             if self.recorder_ext:
   7                 # When done recording actions,
   8                 # type "c", and press [Enter].
   9  ->             import pdb; pdb.set_trace()
 return None
(Pdb+) c

>>>>>>>>>>>>>>>>>> PDB continue >>>>>>>>>>>>>>>>>>

>>> RECORDING SAVED as: recordings/new_test_rec.py
**************************************************

*** RECORDING COPIED to: new_test.py
```

🔴 You can also activate Recorder Mode from the Desktop App:

```bash
sbase recorder
* Starting the SeleniumBase Recorder Desktop App...
```

<img src="https://seleniumbase.github.io/cdn/img/recorder_desktop.png" title="SeleniumBase" width="340">

⏺️ While a recording is in progress, you can press the ``[ESC]`` key to pause the Recorder. To resume the recording, you can hit the ``[~`]`` key, which is located directly below the ``[ESC]`` key on most keyboards.

⏺️ From within Recorder Mode there are two additional modes: "Assert Element Mode" and "Assert Text Mode". To switch into "Assert Element Mode", press the ``[^]-key (SHIFT+6)``: The border will become purple, and you'll be able to click on elements to assert from your test. To switch into "Assert Text Mode", press the ``[&]-key (SHIFT+7)``: The border will become teal, and you'll be able to click on elements for asserting text from your test.

While using either of the two special Assertion Modes, certain actions such as clicking on links won't have any effect. This lets you make assertions on elements without navigating away from the page, etc. To add an assertion for buttons without triggering default "click" behavior, mouse-down on the button and then mouse-up somewhere else. (This prevents a detected click while still recording the assert.) To return back to the original Recorder Mode, press any key other than ``[SHIFT]`` or ``[BACKSPACE]`` (Eg: Press ``[CONTROL]``, etc.). Press ``[ESC]`` once to leave the Assertion Modes, but it'll stop the Recorder if you press it again.

⏺️ For extra flexibility, the ``sbase mkrec`` command can be split into four separate commands:

```bash
sbase mkfile TEST_NAME.py --rec

pytest TEST_NAME.py --rec -q -s

sbase print ./recordings/TEST_NAME_rec.py -n

cp ./recordings/TEST_NAME_rec.py ./TEST_NAME.py
```

The first command creates a boilerplate test with a breakpoint; the second command runs the test with the Recorder activated; the third command prints the completed test to the console; and the fourth command replaces the initial boilerplate with the completed test. If you're just experimenting with the Recorder, you can run the second command as many times as you want, and it'll override previous recordings saved to ``./recordings/TEST_NAME_rec.py``. (Note that ``-s`` is needed to allow breakpoints, unless you already have a ``pytest.ini`` file present with ``addopts = --capture=no`` in it. The ``-q`` is optional, which shortens ``pytest`` console output.)

⏺️ You can also use the Recorder to add code to an existing test. To do that, you'll first need to create a breakpoint in your code to insert manual browser actions:

```python
import pdb; pdb.set_trace()
```

Now you'll be able to run your test with ``pytest``, and it will stop at the breakpoint for you to add in actions: (Press ``c`` and ``ENTER`` on the command-line to continue from the breakpoint.)

```bash
pytest TEST_NAME.py --rec -s
```

⏺️ You can also set a breakpoint at the start of your test by adding ``--trace`` as a ``pytest`` command-line option: (This is useful when running Recorder Mode without any ``pdb`` breakpoints.)

```bash
pytest TEST_NAME.py --trace --rec -s
```

⏺️ After the test completes, a file called ``TEST_NAME_rec.py`` will be automatically created in the ``./recordings`` folder, which will include the actions performed by the test, and the manual actions that you added in.

⏺️ Here's a command-line notification for a completed recording:

```bash
>>> RECORDING SAVED as: recordings/TEST_NAME_rec.py
***************************************************
```

⏺️ When running additional tests from the same Python module, Recordings will get added to the file that was created from the first test:

```bash
>>> RECORDING ADDED to: recordings/TEST_NAME_rec.py
***************************************************
```

⏺️ Recorder Mode works by saving your recorded actions into the browser's sessionStorage. SeleniumBase then reads from the browser's sessionStorage to take the raw data and generate a full test from it. Keep in mind that sessionStorage is only present while the browser tab remains in the same domain/origin. (The sessionStorage of that tab goes away if you leave that domain/origin.) To compensate, links to web pages of different domain/origin will automatically open a new tab for you in Recorder Mode.

⏺️ Additionally, the SeleniumBase <code>self.open(URL)</code> method will also open a new tab for you in Recorder Mode if the domain/origin is different from the current URL. If you need to navigate to a different domain/origin from within the same tab, call <code>self.save_recorded_actions()</code> first, which saves the recorded data for later. When a recorded test completes, SeleniumBase scans the sessionStorage data of all open browser tabs for generating the completed script.

⏺️ As an alternative to activating Recorder Mode with the <code>--rec</code> command-line arg, you can also call <code>self.activate_recorder()</code> from your tests. Using the Recorder this way is only useful for tests that stay on the same URL. This is because the standard Recorder Mode functions as a Chrome extension and persists wherever the browser goes. (This version only stays on the page where called.)

⏺️ (Note that <b>same domain/origin</b> is not the same as <b>same URL</b>. Example: <a href="https://xkcd.com/353/" target="_blank">https://xkcd.com/353</a> and <a href="https://xkcd.com/1537/" target="_blank">https://xkcd.com/1537</a> are two different URLs with the <b>same domain/origin</b>. That means both URLs share the same sessionStorage, and that changes persist to different URLs of the same domain/origin. If you want to find out a website's origin during a test, just call: <code>self.get_origin()</code>, which returns the value of <code>window.location.origin</code> from the browser's console.)

⏺️ Inside recorded tests, you might find the <code>self.open_if_not_url(URL)</code> method, which opens the URL given if the browser is not currently on that page. SeleniumBase uses this method in recorded scripts when the Recorder detects that a browser action changed the current URL. This method prevents an unnecessary page load and shows what page the test visited after a browser action.

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
