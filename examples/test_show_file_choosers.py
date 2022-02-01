"""
self.show_file_choosers() is used to show hidden file-upload fields.
Verify that one can choose a file after the hidden input is visible.
"""
import os
from seleniumbase import BaseCase


class FileUpload(BaseCase):
    def test_show_file_choosers(self):
        self.open("https://imgbb.com/upload")
        choose_file_selector = 'input[type="file"]'
        uploaded_image = "#anywhere-upload-queue li.queue-item"
        self.assert_element_not_visible(choose_file_selector)
        self.show_file_choosers()
        self.highlight(choose_file_selector)
        self.assert_element(choose_file_selector)
        self.assert_attribute(choose_file_selector, "value", "")
        self.assert_element_not_visible(uploaded_image)
        dir_name = os.path.dirname(os.path.abspath(__file__))
        my_file = "screenshot.png"
        file_path = os.path.join(dir_name, "example_logs/%s" % my_file)
        self.choose_file(choose_file_selector, file_path)
        if self.browser != "safari":
            seen_path = "%s\\%s" % ("C:\\fakepath", my_file)
            self.assert_attribute(choose_file_selector, "value", seen_path)
        self.demo_mode = True
        self.assert_element(uploaded_image)
