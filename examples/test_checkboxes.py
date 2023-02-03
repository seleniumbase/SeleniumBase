from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class CheckboxTests(BaseCase):
    def test_checkboxes_and_radio_buttons(self):
        self.open("https://seleniumbase.io/w3schools/checkboxes")
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")
        checkbox = "input#vehicle2"
        self.assert_false(self.is_selected(checkbox))
        self.click(checkbox)
        self.assert_true(self.is_selected(checkbox))
        self.open("https://seleniumbase.io/w3schools/radio_buttons")
        self.click("button#runbtn")
        self.switch_to_frame("iframeResult")
        option_button = "input#css"
        self.assert_false(self.is_selected(option_button))
        self.click(option_button)
        self.assert_true(self.is_selected(option_button))
