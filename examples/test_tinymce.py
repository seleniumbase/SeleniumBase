from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class TinyMceTests(BaseCase):
    def test_tinymce(self):
        if self.headless:
            self.open_if_not_url("about:blank")
            self.skip("Skip this test in headless mode!")
        self.open("https://seleniumbase.io/tinymce/")
        self.wait_for_element("div.mce-container-body")
        self.click('span:contains("File")')
        self.click('span:contains("New document")')
        self.click('span:contains("Paragraph")')
        self.click('span:contains("Heading 2")')
        self.switch_to_frame("iframe")
        self.add_text("#tinymce", "Automate anything with SeleniumBase!\n")
        self.switch_to_parent_frame()
        self.click("button i.mce-i-image")
        self.type('input[aria-label="Width"].mce-textbox', "300")
        image_url = "https://seleniumbase.github.io/img/sb_logo_10.png"
        self.type("input.mce-textbox", image_url + "\n")
        with self.frame_switch("iframe"):
            self.click("h2")
            self.post_message("Automate anything with SeleniumBase!")
        self.click('span:contains("File")')
        self.click('span:contains("Preview")')
        self.switch_to_frame('iframe[sandbox="allow-scripts"]')
        self.post_message("Learn SeleniumBase Today!")
