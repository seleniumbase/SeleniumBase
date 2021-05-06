""" Classic Page Object Model with the "sb" fixture """


class DataPage:
    def go_to_data_url(self, sb):
        sb.open("data:text/html,<p>Hello!</p><input />")

    def add_input_text(self, sb, text):
        sb.type("input", text)


class ObjTests:
    def test_data_url_page(self, sb):
        DataPage().go_to_data_url(sb)
        sb.assert_text("Hello!", "p")
        DataPage().add_input_text(sb, "Goodbye!")
