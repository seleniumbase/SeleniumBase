'''
You can use this as a boilerplate for your test framework.
Define your customized library methods in a master class like this.
Then have all your test classes inherit it.
BaseTestCase will inherit SeleniumBase methods from BaseCase.
'''

from seleniumbase import BaseCase


class BaseTestCase(BaseCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        # Add custom setUp code for your tests AFTER the super().setUp()

    def tearDown(self):
        # Add custom tearDown code for your tests BEFORE the super().tearDown()
        super(BaseTestCase, self).tearDown()

    def login_to_site(self):
        # <<< Placeholder for actual code. Add your code here. >>>
        # Add frequently used methods like this in your base test case class.
        # This reduces the amount of duplicated code in your tests.
        # If the UI changes, the fix only needs to be applied in one place.
        pass

    def example_method(self):
        # <<< Placeholder for actual code. Add your code here. >>>
        pass


'''
# Now you can do something like this in your test files:

from base_test_case import BaseTestCase

class MyTests(BaseTestCase):

    def test_example(self):
        self.login_to_site()
        self.example_method()
'''
