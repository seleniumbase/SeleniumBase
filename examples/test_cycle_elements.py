from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CycleTests(BaseCase):
    def test_cycle_elements_with_tab_and_press_enter(self):
        """
        Test pressing the tab key to cycle through elements.
        Then click on the active element and verify actions.
        This can all be performed by using a single command.
        The "\t" is the tab key. The "\n" is the RETURN key.
        """
        self.open("seleniumbase.io/demo_page")
        self.assert_text("This Text is Green", "#pText")
        self.send_keys("html", "\t\t\t\t\n")
        self.assert_text("This Text is Purple", "#pText")
