'''
You can use this as a boilerplate for your test framework.
Define your customized library methods in a master class like this.
Then have all your test classes inherit it.
MasterTestCase will inherit SeleniumBase methods from BaseCase.
'''

from seleniumbase import BaseCase


class MasterTestCase(BaseCase):

    def setUp(self):
        super(MasterTestCase, self).setUp()

    def login_to_site(self):
        # Add frequently used methods like this in your master class.
        # This reduces the amount of duplicated code in your tests.
        # If the UI changes, the fix only needs to be applied in one place.
        pass

    def example_method(self):
        # Add your code here.
        pass


'''
# Now you can do something like this in your test files:

from master_test_case import MasterTestCase

class MyTests(MasterTestCase):

    def test_example(self):
        self.login_to_site()
        self.example_method()
'''
