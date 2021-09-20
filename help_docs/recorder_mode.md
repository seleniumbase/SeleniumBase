[<img src="https://seleniumbase.io/cdn/img/super_logo_sb.png" title="SeleniumBase" width="296">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Recorder Mode</h2>

SeleniumBase <b>Recorder Mode</b> gives you the power to create automation scripts from manual browser actions.<br>(<i>Only Chromium browsers such as Chrome and Edge are supported.</i>)

<img src="https://seleniumbase.io/cdn/img/sb_recorder_notification.png" title="SeleniumBase" width="380">

To activate Recorder Mode, add ``--recorder`` to your ``pytest`` run command when running an existing test:

```bash
pytest TEST_NAME.py --recorder
```

In order to add actions to the test being run, you'll need to create a breakpoint somewhere inside your test:

```python
import ipdb; ipdb.set_trace()
```

Once you've reached the breakpoint, you can take control of the browser and add in any actions that you want recorded. When you are finished recording, type "``c``" on the command-line and press ``[Enter]`` to let the test continue from the breakpoint. After the test completes, a file called ``TEST_NAME_rec.py`` will be automatically created in the ``./recordings`` folder, which will include the actions performed by the test, and the manual actions that you added in. Below is a command-line notification:

```bash
>>> RECORDING saved to: recordings/my_first_test_rec.py
*******************************************************
```

While a recording is in progress, you can hit the ``[ESC]`` key to pause the recording. To resume the recording, you can hit the ``[~`]`` key, which is located directly below the ``[ESC]`` key on most keyboards.

<p>If you want to create a recording from scratch, just run:<br><code>pytest --recorder</code> on a Python file such as this one:

```python
from seleniumbase import BaseCase

class RecorderTest(BaseCase):
    def test_recorder(self):
        import ipdb; ipdb.set_trace()
```

The above file gives you a basic SeleniumBase file with a breakpoint in it so that you can immediately start recording after you've opened a new web page in the browser.

Recorder Mode works by saving your recorded actions into the browser's ``sessionStorage``. SeleniumBase then reads from the browser's ``sessionStorage`` to take the raw data and generate a full test from it. Keep in mind that ``sessionStorage`` is only present for a website while the browser tab remains on a web page of the same domain/origin. If you leave that domain/origin, the ``sessionStorage`` of that tab will no longer have the raw data that SeleniumBase needs to create a full recording. To compensate for this, all links to web pages of a different domain/origin will automatically open a new tab for you while in Recorder Mode. Additionally, the SeleniumBase ``self.open(URL)`` method will also open a new tab for you in Recorder Mode if the domain/origin is different from the current URL. When the recorded test completes, SeleniumBase will scan the ``sessionStorage`` of all open browser tabs for the data it needs to generate the complete SeleniumBase automation script.

If you just want to record actions on a single URL of a multi-URL test, you can call ``self.activate_recorder()`` from the test instead of using ``pytest --recorder`` from the command-line. When doing so, make sure that the browser tab is still on the same domain/origin at the end of the test, or else SeleniumBase will not have access to the ``sessionStorage`` data that it needs for generating a complete test.

(Note that **same domain/origin** is not the same as **same URL**. Example: ``https://xkcd.com/353/`` and ``https://xkcd.com/1537/`` are two different URLs with the **same domain/origin**. That means that both URLs will share the same ``sessionStorage`` data, and that any changes to ``sessionStorage`` from one URL will carry on to the ``sessionStorage`` of a different URL when the domain/origin is the same. If you want to find out a website's origin during a test, just call: ``self.get_origin()``, which returns the value of ``window.location.origin`` from the browser's console.)

The launch of Recorder Mode has brought a new SeleniumBase method along with it: ``self.open_if_not_url(URL)``. This method will open the URL given if the browser is not currently on that page. This is used as a method in recorded scripts when SeleniumBase detects that a click action has already brought the test to the given page. This method not only prevents an extra page load if not needed, but it also lets people know the current page of the browser at that point in the test.

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
