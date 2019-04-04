### Automated Visual/Layout Testing

The purpose of automated visual/layout testing is to help you determine when something has changed the layout of a web page. Rather than comparing screenshots, a more effective way is to compare HTML tags at different points in time on the same web page. If a change is detected, it could mean that something broke on the webpage, or it might be something harmless like a website redesign or dynamic content loading on the web page. To handle automated visual/layout testing, SeleniumBase uses the ``self.check_window()`` method, which can set visual baselines for comparison and then compare the latest versions of web pages to the existing baseline.

The first time a test calls ``self.check_window()`` for a unique "name" parameter provided, it will set a visual baseline, meaning that it creates a folder, saves the URL to a file, saves the current window screenshot to a file, and creates the following three files with the listed data saved:
* tags_level1.txt  ->  HTML tags from the window
* tags_level2.txt  ->  HTML tags + attributes from the window
* tags_level3.txt  ->  HTML tags + attributes/values from the window

Baseline folders are named based on the test name and the name parameter passed to ``self.check_window()``. The same test can store multiple baseline folders.

If the baseline is being set/reset, the "level" doesn't matter.

After the first run of ``self.check_window()``, it will compare the HTML tags of the latest window to the one from the initial run.
Here's how the level system works:
* level=0 ->
    DRY RUN ONLY - Will perform a comparison to the baseline, and
                   print out any differences that are found, but
                   won't fail the test even if differences exist.
* level=1 ->
    HTML tags are compared to tags_level1.txt
* level=2 ->
    HTML tags are compared to tags_level1.txt and
    HTML tags/attributes are compared to tags_level2.txt
* level=3 ->
    HTML tags are compared to tags_level1.txt and
    HTML tags + attributes are compared to tags_level2.txt and
    HTML tags + attributes/values are compared to tags_level3.txt

As shown, Level-3 is the most strict, Level-1 is the least strict. If the comparisons from the latest window to the existing baseline don't match, the current test will fail, except for Level-0 tests.

You can reset the visual baseline on the command line by using:
    ``--visual_baseline``
As long as ``--visual_baseline`` is used on the command line while running tests, the ``self.check_window()`` method cannot fail because it will rebuild the visual baseline rather than comparing the html tags of the latest run to the existing baseline. If there are any expected layout changes to a website that you're testing, you'll need to reset the baseline to prevent unnecessary failures.

``self.check_window()`` will fail with "Page Domain Mismatch Failure" if the page domain doesn't match the domain of the baseline.

If you want to use ``self.check_window()`` to compare a web page to a later version of itself from within the same test run, you can add the parameter ``baseline=True`` to the first time you call ``self.check_window()`` in a test to use that as the baseline. This only makes sense if you're calling ``self.check_window()`` more than once with the same name parameter in the same test.

Automated Visual/Layout Testing with ``self.check_window()`` is not very effective for websites that have dynamic content that changes the layout and structure of web pages. For those, you're much better off using regular SeleniumBase functional testing.

Example usage:
```
    self.check_window(name="testing", level=0)
    self.check_window(name="xkcd_home", level=1)
    self.check_window(name="github_page", level=2)
    self.check_window(name="wikipedia_page", level=3)
```
