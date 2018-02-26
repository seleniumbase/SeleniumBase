from .base_test_case import BaseTestCase
from .page_objects import HomePage


class MyTestClass(BaseTestCase):

    def test_boilerplate(self):
        self.login_to_site()
        self.example_method()
        self.assert_element(HomePage.html)
