from seleniumbase import BaseCase


class VisualLayoutTest(BaseCase):

    def test_applitools_helloworld(self):
        self.open('https://applitools.com/helloworld?diff1')
        print('Creating baseline in "visual_baseline" folder...')
        self.check_window(name="helloworld", baseline=True)
        self.click('a[href="?diff1"]')
        # Verify html tags match previous version
        self.check_window(name="helloworld", level=1)
        # Verify html tags + attributes match previous version
        self.check_window(name="helloworld", level=2)
        # Verify html tags + attributes + values match previous version
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
