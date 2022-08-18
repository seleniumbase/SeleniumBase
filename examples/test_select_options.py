from seleniumbase import BaseCase


class SelectTestClass(BaseCase):
    def test_base(self):
        self.open("https://seleniumbase.io/demo_page")

        expected_option_texts = [
            "Set to 25%", "Set to 50%", "Set to 75%", "Set to 100%"
        ]
        option_texts = self.get_select_options("select#mySelect")
        self.assert_equal(option_texts, expected_option_texts)

        expected_option_indexes = ["0", "1", "2", "3"]
        option_indexes = self.get_select_options(
            "select#mySelect", attribute="index"
        )
        self.assert_equal(option_indexes, expected_option_indexes)

        expected_option_values = ["25%", "50%", "75%", "100%"]
        option_values = self.get_select_options(
            "select#mySelect", attribute="value"
        )
        self.assert_equal(option_values, expected_option_values)

        for index, option_text in enumerate(option_texts):
            self.select_option_by_text("#mySelect", option_text)
            selected_value = self.get_attribute("#mySelect", "value")
            self.assert_equal(selected_value, option_values[index])

        for index, option_value in enumerate(option_values):
            self.select_option_by_value("#mySelect", option_value)
            selected_value = self.get_attribute("#mySelect", "value")
            self.assert_equal(selected_value, option_values[index])

        for index, option_index in enumerate(option_indexes):
            self.select_option_by_index("#mySelect", option_index)
            # assert_attribute() combines get_attribute() and assert_equal()
            # It also highlights the element when Demo Mode is enabled.
            self.assert_attribute("#mySelect", "value", option_values[index])
