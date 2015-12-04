"""
Method for generating application strings used in the Testcase Database.
"""

import time


class ApplicationManager:
    """
    This class contains methods to generate application strings.
    """

    @classmethod
    def generate_application_string(cls, test):
        """ Generate an application string based on some of the given information
            that can be pulled from the test object: app_env, start_time. """

        app_env = 'test'
        if hasattr(test, 'env'):
            app_env = test.env
        elif hasattr(test, 'environment'):
            app_env = test.environment

        start_time = int(time.time() * 1000)

        return "%s.%s" % (app_env, start_time)
