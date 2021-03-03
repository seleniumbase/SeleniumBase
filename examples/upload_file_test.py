""" Testing the self.choose_file() method. """

import os
from seleniumbase import BaseCase


class FileUploadButtonTests(BaseCase):

    def test_file_upload_button(self):
        self.open("https://www.w3schools.com/jsref/tryit.asp"
                  "?filename=tryjsref_fileupload_get")
        self.ad_block()
        self.switch_to_frame('iframeResult')
        zoom_in = 'input[type="file"]{zoom: 1.5;-moz-transform: scale(1.5);}'
        self.add_css_style(zoom_in)
        self.highlight('input[type="file"]')
        dir_name = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_name, "example_logs/screenshot.png")
        self.choose_file('input[type="file"]', file_path)
        self.demo_mode = True  # Adds highlighting to the assert statement
        self.assert_element('input[type="file"]')
