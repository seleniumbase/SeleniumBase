from seleniumbase import BaseCase


class VisualLayoutTest(BaseCase):

    def test_applitools_layout_change(self):
        self.open('https://applitools.com/helloworld?diff1')
        print('\nCreating baseline in "visual_baseline" folder.')
        self.check_window(name="helloworld", baseline=True)
        # Click a button that changes the text of an element
        # (Text changes do not impact visual comparisons)
        self.click('a[href="?diff1"]')
        # Verify html tags match the baseline
        self.check_window(name="helloworld", level=1)
        # Verify html tags and attribute names match the baseline
        self.check_window(name="helloworld", level=2)
        # Verify html tags and attribute values match the baseline
        self.check_window(name="helloworld", level=3)
        # Click a button that makes a hidden element visible
        self.click("button")
        self.check_window(name="helloworld", level=1)
        self.check_window(name="helloworld", level=2)
        with self.assertRaises(Exception):
            self.check_window(name="helloworld", level=3)
        # Now that we know the Exception was raised as expected,
        # let's print out the comparison results by running a Level-0 check.
        # (NOTE: Running with level-0 will print but NOT raise an Exception.)
        self.check_window(name="helloworld", level=0)
