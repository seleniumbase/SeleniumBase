"""
Testing Drag & Drop
"""

from seleniumbase import BaseCase


class DragAndDropTests(BaseCase):

    def test_drag_and_drop(self):
        self.open('https://www.w3schools.com/html/html5_draganddrop.asp')
        self.remove_elements("script")  # Ad content slows down the page
        self.remove_elements("iframe")  # Ad content slows down the page
        self.scroll_to("#div1")
        self.sleep(0.5)
        self.assert_false(self.is_element_visible("#div2 img#drag1"))
        self.drag_and_drop("#div1 img#drag1", '#div2')
        self.assert_true(self.is_element_visible("#div2 img#drag1"))
        self.sleep(1)
