from seleniumbase import BaseCase


class VisualLayoutTest(BaseCase):

    def test_python_home_layout_change(self):
        self.open('https://python.org/')
        print('\nCreating baseline in "visual_baseline" folder.')
        self.check_window(name="python_home", baseline=True)
        # Remove the "Donate" button
        self.remove_element('a.donate-button')
        self.check_window(name="python_home", level=0)
