from seleniumbase import BaseCase


class DoubleClickTests(BaseCase):

    def test_switch_to_frame_and_double_click(self):
        self.open("https://www.w3schools.com/jsref"
                  "/tryit.asp?filename=tryjsref_ondblclick")
        self.ad_block()
        self.switch_to_frame("iframe#iframeResult")
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")

    def test_switch_to_frame_of_element_and_double_click(self):
        self.open("https://www.w3schools.com/jsref"
                  "/tryit.asp?filename=tryjsref_ondblclick")
        self.ad_block()
        self.switch_to_frame_of_element('[ondblclick="myFunction()"]')
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")
