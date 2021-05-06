""" Classic Page Object Model with BaseCase inheritance """
from seleniumbase import BaseCase


class DataPage:
    def go_to_data_url(self, sb):
        sb.open("data:text/html,<p>Hello!</p><input />")

    def add_input_text(self, sb, text):
        sb.type("input", text)


class ObjTests(BaseCase):
    def test_data_url_page(self):
        DataPage().go_to_data_url(self)
        self.assert_text("Hello!", "p")
        DataPage().add_input_text(self, "Goodbye!")
