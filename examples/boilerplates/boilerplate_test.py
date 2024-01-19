try:  # Run with "pytest" (relative imports are valid)
    from .base_test_case import BaseTestCase
    from .page_objects import Page
except (ImportError, ValueError):  # Run with "python"
    from base_test_case import BaseTestCase
    from page_objects import Page
    BaseTestCase.main(__name__, __file__)


class MyTestClass(BaseTestCase):
    def test_boilerplate(self):
        self.login()
        self.example_method()
        self.assert_element(Page.html)
