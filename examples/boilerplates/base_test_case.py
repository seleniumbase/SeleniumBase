'''
You can use this as a boilerplate for your test framework.
Define your customized library methods in a master class like this.
Then have all your test classes inherit it.
BaseTestCase will inherit SeleniumBase methods from BaseCase.
With Python 3, simplify "super(...)" to super().setUp() and super().tearDown()
'''

from seleniumbase import BaseCase


class BaseTestCase(BaseCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        # <<< Run custom setUp() code for tests AFTER the super().setUp() >>>

    def tearDown(self):
        self.save_teardown_screenshot()
        if self.has_exception():
            # <<< Run custom code if the test failed. >>>
            pass
        else:
            # <<< Run custom code if the test passed. >>>
            pass
        # (Wrap unreliable tearDown() code in a try/except block.)
        # <<< Run custom tearDown() code BEFORE the super().tearDown() >>>
        super(BaseTestCase, self).tearDown()

    def login(self):
        # <<< Placeholder. Add your code here. >>>
        # Reduce duplicate code in tests by having reusable methods like this.
        # If the UI changes, the fix can be applied in one place.
        pass

    def example_method(self):
        # <<< Placeholder. Add your code here. >>>
        pass


'''
# Now you can do something like this in your test files:

from base_test_case import BaseTestCase

class MyTests(BaseTestCase):

    def test_example(self):
        self.login()
        self.example_method()
        self.type("input", "Name")
        self.click("form button")
        ...
'''
