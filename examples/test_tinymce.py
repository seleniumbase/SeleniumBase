import re
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def click_menu_item(self, text):
        self.sleep(0.2)
        soup = self.get_beautiful_soup(self.get_page_source())
        pattern = re.compile('%s' % text)
        the_id = soup.find(text=pattern).parent.parent.attrs["id"]
        self.click("#%s" % the_id)

    def test_base(self):
        self.open("https://seleniumbase.io/other/tinymce")
        self.wait_for_element("div.mce-container-body")
        self.click_menu_item("File")
        self.click_menu_item("New document")
        self.click_menu_item("Paragraph")
        self.click_menu_item("Heading 2")
        self.switch_to_frame("iframe#mce_1_ifr")
        self.send_keys("#tinymce", "Automate anything with SeleniumBase!\n")
        self.switch_to_default_content()
        self.click('button i.mce-i-image')
        self.type('input[aria-label="Width"].mce-textbox', "300")
        image_url = "https://seleniumbase.io/img/sb_logo_10.png"
        self.type("input.mce-textbox", image_url + "\n")
        self.switch_to_frame("iframe#mce_1_ifr")
        self.click("h2")
        self.switch_to_default_content()
        self.post_message("Automate anything with SeleniumBase!")
        self.click_menu_item("File")
        self.click_menu_item("Preview")
        self.switch_to_frame('iframe[sandbox="allow-scripts"]')
        self.post_message("Learn SeleniumBase Today!")
