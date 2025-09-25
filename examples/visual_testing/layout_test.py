from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class VisualLayoutTests(BaseCase):
    def test_xkcd_layout_change(self):
        self.demo_mode = False  # (It would interfere with html comparisons)
        self.open("https://xkcd.com/1424/")
        print('\nCreating baseline in "visual_baseline" folder.')
        self.sleep(0.08)
        self.check_window(name="xkcd", baseline=True)
        # Go to a different comic
        self.open("https://xkcd.com/1425/")
        # Verify html tags match the baseline
        self.check_window(name="xkcd", level=1)
        # Verify html tags and attribute names match the baseline
        self.check_window(name="xkcd", level=2)
        # Verify html tags and attribute values don't match the baseline
        with self.assert_raises(Exception):
            self.check_window(name="xkcd", level=3)
        # Now that we know the Exception was raised as expected,
        # let's print out the comparison results by running a Level-0 check.
        # (NOTE: Running with level-0 will print but NOT raise an Exception.)
        self.check_window(name="xkcd", level=0)
