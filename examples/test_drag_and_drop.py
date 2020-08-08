"""
Testing Drag & Drop
"""

from seleniumbase import BaseCase


class DragAndDropTests(BaseCase):

    def test_drag_and_drop(self):
        url = '://w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop'
        self.open(url)
        self.remove_elements("#tryitLeaderboard")
        self.switch_to_frame("iframeResult")
        self.assert_element_not_visible("#div1 img#drag1")
        self.drag_and_drop("#drag1", "#div1")
        self.assert_element("#div1 img#drag1")
        self.sleep(1)
