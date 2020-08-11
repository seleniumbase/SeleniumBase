from seleniumbase import BaseCase


class VisualLayoutFailureTest(BaseCase):

    def test_applitools_change(self):
        self.open('https://applitools.com/helloworld?diff1')
        print('\nCreating baseline in "visual_baseline" folder.')
        self.check_window(name="helloworld", baseline=True)
        # Click a button that changes the text of an element
        self.click('a[href="?diff1"]')
        # Click a button that makes a hidden element visible
        self.click("button")
        self.check_window(name="helloworld", level=3)

    def test_python_home_change(self):
        self.open('https://python.org/')
        print('\nCreating baseline in "visual_baseline" folder.')
        self.check_window(name="python_home", baseline=True)
        # Remove the "Donate" button
        self.remove_element('a.donate-button')
        self.check_window(name="python_home", level=3)

    def test_xkcd_logo_change(self):
        self.open('https://xkcd.com/554/')
        print('\nCreating baseline in "visual_baseline" folder.')
        self.check_window(name="xkcd_554", baseline=True)
        # Change height: (83 -> 110) , Change width: (185 -> 120)
        self.set_attribute('[alt="xkcd.com logo"]', "height", "110")
        self.set_attribute('[alt="xkcd.com logo"]', "width", "120")
        self.check_window(name="xkcd_554", level=3)
