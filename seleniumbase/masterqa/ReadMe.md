![](http://cdn2.hubspot.net/hubfs/100006/images/masterqa_logo-11.png "MasterQA")
## Automation-Driven Manual QA

### MasterQA combines [SeleniumBase](http://seleniumbase.github.io/SeleniumBase/) automation with manual verification to greatly improve the productivity and sanity of QA teams.

When you can't fully automate your testing, use MasterQA to speed up your manual testing. [Here's an example of a basic MasterQA test script](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/basic_masterqa_test.py): (You'll notice that the Python syntax mostly uses natural language, with the addition of a CSS_selector used in the update_text method.)

```python
from seleniumbase import MasterQA

class MasterQATests(MasterQA):

    def test_masterqa(self):
        self.open("http://xkcd.com/1700/")
        self.verify("Do you see a webcomic?")
        self.click_link_text('Store')
        self.verify("Do you see items for sale?")
        self.update_text("input#top-search-input", "poster\n")
        self.verify("Do you see posters in the search results?")
```

When the browser reaches http://xkcd.com/1700/ after calling ``self.open("http://xkcd.com/1700/")`` (Step 1 in the screenshot below) and hits the first verification line, ``self.verify("Do you see a webcomic?")``, a pop-up appears asking the manual QA tester: "Do you see a webcomic?" (Step 2 in the screenshot below):

![](http://cdn2.hubspot.net/hubfs/100006/xkcd_new_bug_chrome3.png "MasterQA Example")

Here's another example, which demonstrates the results page that appears after responding to all the verification questions. (You'll notice that failed verifications will generate links to screenshots and log files.)

![](http://cdn2.hubspot.net/hubfs/100006/images/hybrid_screen.png "MasterQA Example")

(Above: Actual screens from [masterqa_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/masterqa_test.py) running against [xkcd.com](http://xkcd.com/1522/))

Here's how to install and run MasterQA from scratch:

### Install SeleniumBase and run the example tests:
```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase
pip install -r requirements.txt
python setup.py install
cd examples
nosetests basic_masterqa_test.py --with-selenium
nosetests masterqa_test.py --with-selenium
```

At the end of your test run, you'll receive a report with results, screenshots, and log files. (Add ``--browser=chrome`` to your run command in order to use Chrome instead of Firefox, which requires Chromedriver installed.)

### Follow the [longer example test](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/masterqa_test.py) to write your own tests:

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
