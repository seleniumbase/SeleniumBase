from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_double_click(self):
        self.open("https://www.w3schools.com/jsref"
                  "/tryit.asp?filename=tryjsref_ondblclick")
        self.switch_to_frame("iframeResult")
        self.double_click('[ondblclick="myFunction()"]')
        self.assert_text("Hello World", "#demo")
