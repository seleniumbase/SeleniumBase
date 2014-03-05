from functools import wraps
import logging


def retry_if_unsuccessful(max_tries=2):
    """Decorator for a test method to make it automatically re-run on errors and failures.

    @max_tries: The maximum number of times the test will run before failing (default 2)

    This decorator will also run the test class's setUp/tearDown methods before/after
    each attempt at running the decorated test method.

    Please only add this decorator to a test if you have already made a best effort
    to fix flapping within the test, and have a good reason why more effort
    won't fix the flapping.
    """
    def _retry_if_unsuccessful(func):
        @wraps(func)
        def test_wrapper(self):
            for x in range(0, max_tries):
                # setUp is called automatically before the first run, and tearDown
                # is called automatically after the last, so we need to skip calling
                # setUp on the first iteration and tearDown on the last.
                setup_successful = x == 0
                try:
                    if x > 0:
                        self.setUp()
                        setup_successful = True
                    func(self)
                except Exception, e:
                    logging.exception('Exception running test: %s, retrying' % e)
                    if x < max_tries-1 and setup_successful:
                        self.tearDown()
                    if x + 1 >= max_tries:
                        raise
                else:
                    return
        return test_wrapper

    return _retry_if_unsuccessful
