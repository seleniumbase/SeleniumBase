from seleniumbase import BaseCase


class DataPage():

    def go_to_data_url(self, sb):
        sb.open("data:text/html,<p>Hello!</p>")


class MyTests(BaseCase):

    def test_go_to_data_url(self):
        DataPage().go_to_data_url(self)
        self.assert_text("Hello!", "p")
