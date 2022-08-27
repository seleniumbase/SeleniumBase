"""
Testing Drag & Drop on different pages.
"""
from seleniumbase import BaseCase


class DragAndDropTests(BaseCase):
    def test_drag_and_drop(self):
        self.open("https://seleniumbase.io/other/drag_and_drop")
        self.assert_element_not_visible("#div1 img#drag1")
        self.drag_and_drop("#drag1", "#div1")
        self.assert_element("#div1 img#drag1")
        self.sleep(0.8)

    def test_w3schools_drag_and_drop(self):
        self.open("https://seleniumbase.io/w3schools/drag_drop")
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")
        self.assert_element_not_visible("#div1 img#drag1")
        self.drag_and_drop("#drag1", "#div1")
        self.assert_element("#div1 img#drag1")
        self.sleep(0.8)
