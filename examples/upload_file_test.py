""" Testing the self.choose_file() and self.assert_attribute() methods. """

import os
from seleniumbase import BaseCase


class FileUploadButtonTests(BaseCase):
    def test_file_upload_button(self):
        self.open(
            "https://www.w3schools.com/jsref/tryit.asp"
            "?filename=tryjsref_fileupload_get"
        )
        self.ad_block()
        self.switch_to_frame("iframeResult")
        zoom_in = 'input[type="file"]{zoom: 1.6;-moz-transform: scale(1.6);}'
        self.add_css_style(zoom_in)
        self.highlight('input[type="file"]')
        dir_name = os.path.dirname(os.path.abspath(__file__))
        my_file = "screenshot.png"
        file_path = os.path.join(dir_name, "example_logs/%s" % my_file)
        self.assert_attribute("#myFile", "value", "")
        self.choose_file('input[type="file"]', file_path)
        self.assert_attribute("#myFile", "value", "C:\\fakepath\\%s" % my_file)
        self.highlight('input[type="file"]')
