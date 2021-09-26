[<img src="https://seleniumbase.io/cdn/img/sb_logo_10t.png" title="SeleniumBase" width="220">](https://github.com/seleniumbase/SeleniumBase/)

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Recorder Mode</h2>

🔴 SeleniumBase <b>Recorder Mode</b> gives you the power to create automation scripts from manual browser actions.<br>(<i>Only Chromium browsers such as Chrome and Edge are supported.</i>)

<img src="https://seleniumbase.io/cdn/img/sb_recorder_notification.png" title="SeleniumBase" width="380">

🔴 To activate Recorder Mode, add ``--recorder`` to your ``pytest`` run command when running an existing test: (Also add ``-s`` to allow breakpoints, unless you already have a ``pytest.ini`` file present with ``--capture=no`` in it.)

```bash
pytest TEST_NAME.py --recorder -s
```

🔴 To add your own actions inside the test, you'll need to create a breakpoint somewhere inside of it:

```python
import ipdb; ipdb.set_trace()
```

🔴 Once you've reached the breakpoint, you can take control of the browser and add in any actions that you want recorded. When you are finished recording, type "``c``" on the command-line and press ``[Enter]`` to let the test continue from the breakpoint. After the test completes, a file called ``TEST_NAME_rec.py`` will be automatically created in the ``./recordings`` folder, which will include the actions performed by the test, and the manual actions that you added in. Below is a command-line notification:

```bash
>>> RECORDING SAVED as: recordings/my_first_test_rec.py
*******************************************************
```

If a Python file contains more tests, they'll be added:

```bash
>>> RECORDING ADDED to: recordings/my_first_test_rec.py
*******************************************************
```

🔴 While a recording is in progress, you can hit the ``[ESC]`` key to pause the recording. To resume the recording, you can hit the ``[~`]`` key, which is located directly below the ``[ESC]`` key on most keyboards.

<p>🔴 If you want to create a recording from scratch, just run:<br><code>pytest --recorder</code> on a Python file such as this one:</p>

```python
from seleniumbase import BaseCase

class RecorderTest(BaseCase):
    def test_recorder(self):
        import ipdb; ipdb.set_trace()
```

<p>🔴 The above file gives you a basic SeleniumBase file with a breakpoint in it so that you can immediately start recording after you've opened a new web page in the browser.</p>

<p>🔴 Recorder Mode works by saving your recorded actions into the browser's <code>sessionStorage</code>. SeleniumBase then reads from the browser's <code>sessionStorage</code> to take the raw data and generate a full test from it. Keep in mind that <code>sessionStorage</code> is only present for a website while the browser tab remains on a web page of the same domain/origin. If you leave that domain/origin, the <code>sessionStorage</code> of that tab will no longer have the raw data that SeleniumBase needs to create a full recording. To compensate for this, all links to web pages of a different domain/origin will automatically open a new tab for you while in Recorder Mode. Additionally, the SeleniumBase <code>self.open(URL)</code> method will also open a new tab for you in Recorder Mode if the domain/origin is different from the current URL. When the recorded test completes, SeleniumBase will scan the <code>sessionStorage</code> of all open browser tabs for the data it needs to generate the complete SeleniumBase automation script.</p>

<p>🔴 If you just want to record actions on a single URL of a multi-URL test, you can call <code>self.activate_recorder()</code> from the test instead of using <code>pytest --recorder</code> from the command-line. When doing so, make sure that the browser tab is still on the same domain/origin at the end of the test, or else SeleniumBase will not have access to the <code>sessionStorage</code> data that it needs for generating a complete test.</p>

<p>🔴 (Note that <b>same domain/origin</b> is not the same as <b>same URL</b>. Example: <code>https://xkcd.com/353/</code> and <code>https://xkcd.com/1537/</code> are two different URLs with the <b>same domain/origin</b>. That means that both URLs will share the same <code>sessionStorage</code> data, and that any changes to <code>sessionStorage</code> from one URL will carry on to the <code>sessionStorage</code> of a different URL when the domain/origin is the same. If you want to find out a website's origin during a test, just call: <code>self.get_origin()</code>, which returns the value of <code>window.location.origin</code> from the browser's console.)</p>

<p>🔴 The launch of Recorder Mode has brought a new SeleniumBase method along with it: <code>self.open_if_not_url(URL)</code>. This method will open the URL given if the browser is not currently on that page. This is used as a method in recorded scripts when SeleniumBase detects that a click action has already brought the test to the given page. This method not only prevents an extra page load if not needed, but it also lets people know the current page of the browser at that point in the test.</p>

<p>🔴 SeleniumBase <code>1.66.1</code> adds the ability to record changes to <i>"Choose File"</i> <code>input</code> fields. Sometimes the <i>"Choose File"</i> input field is hidden on websites, so <code>self.show_file_choosers()</code> was added to get around this edge case. Version <code>1.66.1</code> also adds <code>self.set_content_to_frame(frame)</code>, which lets you record actions inside of iframes.</p>

<p>🔴 SeleniumBase <code>1.66.2</code> adds the ability to save selectors using the <code>":contains(TEXT)"</code> selector. If a Python file being recorded has multiple tests being run, then all those tests will get saved to the generated <code>*_rec.py</code> file. The Recorder will now save common <code>self.assert_*</code> calls made during tests. In order to escape iframes when using <code>self.set_content_to_frame(frame)</code>, a new method was added: <code>self.set_content_to_default()</code>. The <code>self.set_content_to_*()</code> methods will be automatically used in place of <code>self.switch_to_*()</code> methods in Recorder Mode, unless a test explicitly calls <code>self._rec_overrides_switch = False</code> before the <code>self.switch_to_*()</code> methods are called. Additionally, if an iframe contains the <code>src</code> attribute, that page will get loaded in a new tab when switching to it in Recorder Mode.</p>

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
