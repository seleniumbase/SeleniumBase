'''
Demonstration of parsing data from files.
In this example, login information is pulled for tests.
'''

from seleniumbase import BaseCase


class ParseTestCase(BaseCase):

    def setUp(self):
        super(ParseTestCase, self).setUp()

    def get_login_credentials(self, user_type):
        # Example of parsing data from a file (Method 1)
        with open('qa_login_example.txt') as f:
            file_lines = [line.rstrip() for line in f]
        for line in file_lines:
            line_items = line.split(',')
            if line_items[0] == user_type:
                return line_items[1], line_items[2]

    def get_all_login_credentials(self):
        # Example of parsing data from a file (Method 2)
        keys = {}
        with open('staging_login_example.txt') as f:
            file_lines = [line.rstrip() for line in f]
        for line in file_lines:
            line_items = line.split(',')
            if line_items[0] == 'admin':
                keys['admin'] = (
                    {'username': line_items[1], 'password': line_items[2]})
            if line_items[0] == 'employee':
                keys['employee'] = (
                    {'username': line_items[1], 'password': line_items[2]})
            if line_items[0] == 'customer':
                keys['customer'] = (
                    {'username': line_items[1], 'password': line_items[2]})
        return keys


class ParseTests(ParseTestCase):

    def test_get_login_credentials(self):
        print("\nExample 1 of getting login info from parsing a config file:")
        print("")
        username, password = self.get_login_credentials("admin")
        print("Getting Admin User login data:")
        print("Username: %s" % username)
        print("Password: %s" % password)

        print("\nExample 2 of getting login info from parsing a config file:")
        print("")
        keys = self.get_all_login_credentials()
        print("Getting Customer login data:")
        print("Username: %s" % keys["customer"]["username"])
        print("Password: %s" % keys["customer"]["password"])
