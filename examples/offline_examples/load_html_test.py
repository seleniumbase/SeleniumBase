import pytest
from seleniumbase import BaseCase


@pytest.mark.offline  # Can be run with: "pytest -m offline"
class OfflineTests(BaseCase):
    def test_load_html_string(self):
        html = "<h2>Hello</h2><p><input />&nbsp;&nbsp;<button>OK!</button></p>"
        self.load_html_string(html)  # Open "data:text/html," then replace html
        self.assert_text("Hello", "h2")
        self.assert_text("OK!", "button")
        self.type("input", "Goodbye")
        self.click("button")
        new_html = '<h3>Checkbox</h3><p><input type="checkbox" />Check Me!</p>'
        self.set_content(new_html)  # Same as load_html_string(), but keeps URL
        self.assert_text("Checkbox", "h3")
        self.assert_text("Check Me!", "p")
        self.assert_false(self.is_selected("input"))
        self.click("input")
        self.assert_true(self.is_selected("input"))
