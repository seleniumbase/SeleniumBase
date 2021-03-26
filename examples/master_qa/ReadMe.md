![](https://seleniumbase.io/cdn/img/masterqa_logo.png "MasterQA")

<h3><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> MasterQA combines automation with manual verification steps.</h3>

![](https://seleniumbase.io/cdn/gif/masterqa6.gif "MasterQA")

Here's example code from [basic_masterqa_test_0.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/master_qa/basic_masterqa_test_0.py):

```python
self.open("https://xkcd.com/1700/")
self.verify("Do you see a webcomic?")
self.highlight_click('link=Blag')
self.verify('Do you see a blog archive?')
self.highlight_update_text("input#s", "Dragons\n")
self.verify('Do you see "dragons" in the search results?')
```

After each automation checkpoint, a pop-up window will ask the user questions for each verification command.

When the test run completes, as seen from [this longer example](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/master_qa/masterqa_test_1.py), you'll reach the results page that appears after answering all the verification questions. (Failed verifications generate links to screenshots and log files.)

![](https://seleniumbase.io/cdn/img/mqa_hybrid.png "MasterQA")

You may have noticed the ``Incomplete Test Runs`` row on the results page. If the value for that is not zero, it means that one of the automated steps failed. This could happen if you tell your script to perform an action on an element that doesn't exist. Now that we're mixing automation with manual QA, it's good to tell apart the failures from each. The results_table CSV file contains a spreadsheet with the details of each failure (if any) for both manual and automated steps.

#### How to run the example tests from scratch:

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase
pip install .
cd examples/master_qa
pytest basic_masterqa_test_0.py
pytest masterqa_test_1.py
```

At the end of your test run, you'll receive a report with results, screenshots, and log files. Close the Results Page window when you're done.

### Check out [masterqa_test_1.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/master_qa/masterqa_test_1.py) to learn how to write your own MasterQA tests:

You'll notice that tests are written the same way as regular [SeleniumBase](https://seleniumbase.com) tests, with the key difference being a different import: ``from seleniumbase import MasterQA`` rather than ``from seleniumbase import BaseCase``. Now your Python test class will import ``MasterQA`` instead of ``BaseCase``.

To add a manual verification step, use ``self.verify()`` in the code after each part of your test that needs a manual verification step. If you want to include a custom question, add text inside that call (in quotes). Example:

```python
self.verify()

self.verify("Can you find the moon?")
```

--------

MasterQA is powered by [SeleniumBase](https://seleniumbase.com), the most advanced open-source automation framework on the [Planet](https://en.wikipedia.org/wiki/Earth).
