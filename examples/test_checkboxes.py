from seleniumbase import BaseCase


class CheckboxTests(BaseCase):
    def test_checkboxes_and_radio_buttons(self):
        self.open(
            "https://www.w3schools.com/tags/tryit.asp"
            "?filename=tryhtml5_input_type_checkbox"
        )
        self.ad_block()
        self.switch_to_frame("iframeResult")
        checkbox = "input#vehicle2"
        self.assert_false(self.is_selected(checkbox))
        self.click(checkbox)
        self.assert_true(self.is_selected(checkbox))
        self.open(
            "https://www.w3schools.com/tags/tryit.asp"
            "?filename=tryhtml5_input_type_radio"
        )
        self.switch_to_frame("iframeResult")
        option_button = "input#css"
        self.assert_false(self.is_selected(option_button))
        self.click(option_button)
        self.assert_true(self.is_selected(option_button))
