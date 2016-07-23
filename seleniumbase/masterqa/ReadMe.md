![](http://cdn2.hubspot.net/hubfs/100006/images/masterqa_logo-11.png "MasterQA")
## Automation-Driven Manual QA

MasterQA uses [SeleniumBase](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md) automation to speed up manual QA when total automation isn't possible (or desired).

Here's the main code of [basic_masterqa_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/basic_masterqa_test.py):

```python
self.open("http://xkcd.com/1700/")
self.verify("Do you see a webcomic?")
self.click_link_text('Store')
self.verify("Do you see items for sale?")
self.update_text("input#top-search-input", "poster\n")
self.verify("Do you see posters in the search results?")
```

After the web browser performs various automated actions, a pop-up window will ask the tester questions for each verification command. *(See the screenshot below)*

![](http://cdn2.hubspot.net/hubfs/100006/xkcd_new_bug_chrome3.png "MasterQA Example")

At the end of a full test run, as seen from [this other example]((https://github.com/seleniumbase/SeleniumBase/blob/master/examples/masterqa_test.py)), you'll see a results page that appears after responding to all the verification questions. (Failed verifications generate links to screenshots and log files.)

![](http://cdn2.hubspot.net/hubfs/100006/images/hybrid_screen.png "MasterQA Example")

You may have noticed the ``Incomplete Test Runs`` row on the results page. If the value for that is not zero, it means that one of the automated steps failed. This could happen if you tell your script to perform an action on an element that doesn't exist. Now that we're mixing automation with manual QA, it's good to tell apart the failures from each. The results_table CSV file contains a spreadsheet with the details of each failure (if any) for both manual and automated steps.

#### How to run the example tests from scratch:
```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase
pip install -r requirements.txt
python setup.py install
cd examples
nosetests basic_masterqa_test.py --with-selenium
nosetests masterqa_test.py --with-selenium
```

At the end of your test run, you'll receive a report with results, screenshots, and log files. (Add ``--browser=chrome`` to your run command in order to use Chrome instead of Firefox, which requires Chromedriver installed.) Close the Results Page window when you're done.

### Follow [masterqa_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/masterqa_test.py) to write your own tests:

```python
from seleniumbase import MasterQA

class MasterQATests(MasterQA):

    def test_xkcd(self):
        self.open("http://xkcd.com/1512/")
        for i in xrange(4):
            self.click('a[rel="next"]')
        for i in xrange(3):
            self.click('a[rel="prev"]')
        self.verify()
        self.open("http://xkcd.com/1520/")
        for i in xrange(2):
            self.click('a[rel="next"]')
        self.verify("Can you find the moon?")
        self.click('a[rel="next"]')
        self.verify("Do the drones look safe?")
        self.click_link_text('Blag')
        self.update_text("input#s", "Robots!\n")
        self.verify("Does it say 'Hooray robots' on the page?")
        self.open("http://xkcd.com/213/")
        for i in xrange(5):
            self.click('a[rel="prev"]')
        self.verify("Does the page say 'Abnormal Expressions'?")
```

You'll notice that tests are written based on [SeleniumBase](http://seleniumbase.com), with the key difference of using a different import: ``from seleniumbase import MasterQA`` rather than ``from seleniumbase import BaseCase``. Now the test class will import ``MasterQA`` instead of ``BaseCase``.

To add a manual verification step, use ``self.verify()`` in the code after each part of the script that needs manual verification. If you want to include a custom question, add text inside that call (in quotes). Example:

```python
self.verify()

self.verify("Can you find the moon?")
```

MasterQA is powered by [SeleniumBase](http://seleniumbase.com), the most advanced open-source automation platform on the [Planet](https://en.wikipedia.org/wiki/Earth).
