"""
Sometimes tests open new tabs/windows, and you'll need
to switch to them first in order to interact with them.
The starting window is window(0). Then increments by 1.
"""
from seleniumbase import BaseCase


class TabSwitchingTests(BaseCase):
    def test_switch_to_tabs(self):
        self.open("data:text/html,<h1>Page A</h1>")
        self.assert_text("Page A")
        self.open_new_window()
        self.open("data:text/html,<h1>Page B</h1>")
        self.assert_text("Page B")
        self.switch_to_window(0)
        self.assert_text("Page A")
        self.assert_text_not_visible("Page B")
        self.switch_to_window(1)
        self.assert_text("Page B")
        self.assert_text_not_visible("Page A")
