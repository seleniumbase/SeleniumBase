[<img src="https://cdn2.hubspot.net/hubfs/100006/images/SeleniumBaseText_F.png" title="SeleniumBase" align="center" height="38">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)
### Automated Visual Testing (Layout Change Detection)

Automated visual testing helps you detect when the layout of a web page has changed. Rather than comparing screenshots, layout differences are detected by comparing HTML tags and properties with a baseline. If a change is detected, it could mean that something broke, the web page was redesigned, or dynamic content changed.

To handle automated visual testing, SeleniumBase uses the ``self.check_window()`` method, which can set visual baselines for comparison and then compare the latest versions of web pages to the existing baseline.

The first time a test calls ``self.check_window()`` with a unique "name" parameter, the visual baseline is set, which means a folder is created with the following files:
* page_url.txt  ->  The URL of the current window
* screenshot.png  -> A screenshot of the current window
* tags_level1.txt  ->  HTML tags from the window
* tags_level2.txt  ->  HTML tags + attributes from the window
* tags_level3.txt  ->  HTML tags + attributes/values from the window

After the first time ``self.check_window()`` is called, later calls will compare the HTML tags and properties of the latest window to the ones from the first call (<i>or to the ones from the call when the baseline was last reset</i>).

Here's an example call:
```
self.check_window(name="first_test)", level=3)
```
On the first run (<i>or if the baseline is being set/reset</i>) the "level" doesn't matter because that's only used for comparing the current layout to the existing baseline.

Here's how the level system works:
* level=0 ->
    DRY RUN ONLY - Will perform a comparison to the baseline, and print out any differences that are found, but won't fail the test even if differences exist.
* level=1 ->
    HTML tags are compared to tags_level1.txt
* level=2 ->
    HTML tags and attribute names are compared to tags_level2.txt
* level=3 ->
    HTML tags and attribute values are compared to tags_level3.txt

As shown, Level-3 is the most strict, Level-1 is the least strict. If the comparisons from the latest window to the existing baseline don't match, the current test will fail, except for Level-0 tests.

You can reset the visual baseline on the command line by adding the following parameter at runtime:
``--visual_baseline``

As long as ``--visual_baseline`` is used on the command line while running tests, the ``self.check_window()`` method cannot fail because it will rebuild the visual baseline rather than comparing the html tags of the latest run to the existing baseline. If there are any expected layout changes to a website that you're testing, you'll need to reset the baseline to prevent unnecessary failures.

``self.check_window()`` will fail with "Page Domain Mismatch Failure" if the domain of the current URL doesn't match the domain of the baseline URL.

If you want to use ``self.check_window()`` to compare a web page to a later version of itself from within the same test run, you can add the parameter ``baseline=True`` to the first time you call ``self.check_window()`` in a test to use that as the baseline. This only makes sense if you're calling ``self.check_window()`` more than once with the same "name" parameter in the same test.

Automated Visual Testing with ``self.check_window()`` is not very effective for websites that have dynamic content because that changes the layout and structure of web pages. For those pages, you're much better off using regular SeleniumBase functional testing, unless you can remove the dynamic content before performing the comparison, (such as by using ``self.ad_block()`` to remove dynamic ad content on a web page).

Example usage of ``self.check_window()``:
```python
    self.check_window(name="testing", level=0)
    self.check_window(name="xkcd_home", level=1)
    self.check_window(name="github_page", level=2)
    self.check_window(name="wikipedia_page", level=3)

    self.check_window(name="helloworld", baseline=True)
    ### Do something that may change the web page
    self.check_window(name="helloworld", level=3)
```

Full example test:
```python
from seleniumbase import BaseCase


class VisualLayoutTest(BaseCase):

    def test_applitools_layout_change(self):
        self.open('https://applitools.com/helloworld?diff1')
        print('\nCreating baseline in "visual_baseline" folder...')
        self.check_window(name="helloworld", baseline=True)
        self.click('a[href="?diff1"]')
        # Verify html tags match previous version
        self.check_window(name="helloworld", level=1)
        # Verify html tags and attribute names match previous version
        self.check_window(name="helloworld", level=2)
        # Verify html tags and attribute values match previous version
        self.check_window(name="helloworld", level=3)
        # Change the page enough for a Level-3 comparison to fail
        self.click("button")
        self.check_window(name="helloworld", level=1)
        self.check_window(name="helloworld", level=2)
        with self.assertRaises(Exception):
            self.check_window(name="helloworld", level=3)
        # Now that we know the Exception was raised as expected,
        # let's print out the comparison results by running in Level-0.
        # (NOTE: Running with level-0 will print but NOT raise an Exception.)
        self.check_window(name="helloworld", level=0)
```

Here's the output of that:
```
AssertionError:
First differing element 39:
['div', [['class', ['section', 'hidden-section', 'image-section']]]]
['div', [['class', ['section', 'image-section']]]]

-  ['div', [['class', ['section', 'hidden-section', 'image-section']]]],
?                                ------------------
+  ['div', [['class', ['section', 'image-section']]]],
*
*** Exception: <Level 3> Visual Diff Failure:
* HTML tag attribute values don't match the baseline!
```

Here's another example:
```python
from seleniumbase import BaseCase


class VisualLayoutTest(BaseCase):

    def test_xkcd_layout_change(self):
        self.open('https://xkcd.com/554/')
        print('\nCreating baseline in "visual_baseline" folder.')
        self.check_window(name="xkcd_554", baseline=True)
        # Change height: (83 -> 130) , Change width: (185 -> 120)
        self.set_attribute('[alt="xkcd.com logo"]', "height", "130")
        self.set_attribute('[alt="xkcd.com logo"]', "width", "120")
        self.check_window(name="xkcd_554", level=0)
```

Here's the output of that:
```
AssertionError:
First differing element 22:
['img[30 chars]['height', '83'], ['src', '/s/0b7742.png'], ['width', '185']]]
['img[30 chars]['height', '130'], ['src', '/s/0b7742.png'], ['width', '120']]]

-    ['height', '83'],
?                ^
+    ['height', '130'],
?                ^ +
-    ['width', '185']]],
?                ^^
+    ['width', '120']]],
?                ^^
*
*** Exception: <Level 3> Visual Diff Failure:
* HTML tag attribute values don't match the baseline!
```
