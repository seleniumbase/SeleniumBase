from seleniumbase import BaseCase


class VisualLayoutTests(BaseCase):
    def test_xkcd_layout_change(self):
        self.open("https://xkcd.com/554/")
        print('\nCreating baseline in "visual_baseline" folder.')
        self.check_window(name="xkcd_554", baseline=True)
        # Change height: (83 -> 130) , Change width: (185 -> 120)
        self.set_attribute('[alt="xkcd.com logo"]', "height", "130")
        self.set_attribute('[alt="xkcd.com logo"]', "width", "120")
        self.check_window(name="xkcd_554", level=0)
