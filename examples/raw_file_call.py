"""Call a file with "python" instead of using "pytest" directly.
To run, use: "python raw_file_call.py".
Works by using pytest.main([__file__])."""
from seleniumbase import BaseCase

if __name__ == "__main__":
    from pytest import main

    main([__file__])


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
        self.switch_to_default_content()
        self.post_message("SeleniumBase is the best!")
