""" * Asserting that multiple elements are present or visible:
HTML Presence: assert_elements_present()
HTML Visibility: assert_elements() <> assert_elements_visible()"""
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTestClass(BaseCase):
    def test_assert_list_of_elements(self):
        self.open("https://seleniumbase.io/demo_page")
        self.assert_elements_present("head", "style", "script")
        self.assert_elements("h1", "h2", "h3")
        my_list = ["#myDropdown", "#myButton", "#svgRect"]
        self.assert_elements(my_list)
