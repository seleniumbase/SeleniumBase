'''
You can use this as a boilerplate for your test framework.
Define your customized library methods here.
Then have all your test classes inherit it.
The master class will inherit SeleniumBase methods from BaseCase.
'''

from seleniumbase import BaseCase


class MasterTestCase(BaseCase):

    def setUp(self):
        super(MasterTestCase, self).setUp()

    def example_method(self):
        pass


'''
# Now you can do something like this in your test files:

from master_class import MasterTestCase

class MyTests(MasterTestCase):

    def test_example(self):
        self.example_method()
'''
