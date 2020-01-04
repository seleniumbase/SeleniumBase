from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_double_click_and_switch_to_frame(self):
        self.open("https://www.w3schools.com/jsref"
                  "/tryit.asp?filename=tryjsref_ondblclick")
        self.ad_block()
        self.switch_to_frame("#iframeResult")
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")

    def test_double_click_and_switch_to_frame_of_element(self):
        self.open("https://www.w3schools.com/jsref"
                  "/tryit.asp?filename=tryjsref_ondblclick")
        self.ad_block()
        self.switch_to_frame_of_element('[ondblclick="myFunction()"]')
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")
