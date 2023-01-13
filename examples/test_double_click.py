"""Test double_click() after switching into iframes."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class DoubleClickTests(BaseCase):
    def test_switch_to_frame_and_double_click(self):
        self.open("https://seleniumbase.io/w3schools/double_click")
        self.click("button#runbtn")
        self.switch_to_frame("iframe#iframeResult")
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")

    def test_switch_to_frame_of_element_and_double_click(self):
        self.open("https://seleniumbase.io/w3schools/double_click")
        self.click("button#runbtn")
        self.switch_to_frame_of_element('[ondblclick="myFunction()"]')
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")
