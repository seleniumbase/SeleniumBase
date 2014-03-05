"""
Methods for generating and parsing application strings used 
in the Testcase Database
"""

import time

class ApplicationManager:
    """
    This class contains methods to generate application strings.  We build
    it from available test data
    """

    @classmethod
    def generate_application_string(cls, test):
        """generate an application string based on any of the given information
           that can be pulled from the test object: app_name, app_env,
           unique_id, user"""

        app_name = ''
        app_env = 'test'
        unique_id = ''
        user = ''

        if hasattr(test, 'app_name'):
            app_name = test.app_name

        if hasattr(test, 'unique_id'):
            unique_id = test.unique_id
        else:
            unique_id = int(time.time() * 1000)

        if hasattr(test, 'user'):
            user = test.user

        return "%s.%s.%s.%s" % (app_name, app_env, unique_id, user)


    @classmethod
    def parse_application_string(cls, string):
        """parse a generated application string into its parts:
            app_name, app_env, unique_id, user """

        pieces = string.split('.')
        return pieces[0], pieces[1], pieces[2], pieces[3]
