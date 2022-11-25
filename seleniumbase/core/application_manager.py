import time


class ApplicationManager:
    """Generating application strings for the Testcase Database."""

    @classmethod
    def generate_application_string(cls, test):
        """Generate a string based on some of the given information
        that's pulled from the test object: app_env, start_time."""

        app_env = "test"
        if hasattr(test, "env"):
            app_env = test.env
        elif hasattr(test, "environment"):
            app_env = test.environment

        start_time = int(time.time() * 1000)

        return "%s.%s" % (app_env, start_time)
