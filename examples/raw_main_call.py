"""Can use "python" instead of using "pytest".
Added pytest args will be included in the run.
Example usage: "python raw_file_call.py"."""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class TinyMceTest(BaseCase):
    def test_tinymce(self):
        self.open("https://seleniumbase.io/tinymce/")
        self.wait_for_element("div.mce-container-body")
        self.click('span:contains("File")')
        self.click('span:contains("New document")')
        self.click('span:contains("Paragraph")')
        self.click('span:contains("Heading 1")')
        with self.frame_switch("iframe"):
            self.add_text("#tinymce", "SeleniumBase!")
            self.highlight("#tinymce")
            self.post_message("SeleniumBase is fast!", duration=1.5)
        self.post_message("And SeleniumBase is fun!", duration=1.5)
