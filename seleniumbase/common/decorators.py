import logging
import math
import sys
import time
import warnings
from functools import wraps


def retry_on_exception(tries=6, delay=1, backoff=2, max_delay=32):
    """
    Decorator for implementing exponential backoff for retrying on failures.

    tries: Max number of tries to execute the wrapped function before failing.
    delay: Delay time in seconds before the FIRST retry.
    backoff: Multiplier to extend the initial delay by for each retry.
    max_delay: Max time in seconds to wait between retries.
    """
    tries = math.floor(tries)
    if tries < 1:
        raise ValueError('"tries" must be greater than or equal to 1.')
    if delay < 0:
        raise ValueError('"delay" must be greater than or equal to 0.')
    if backoff < 1:
        raise ValueError('"backoff" must be greater than or equal to 1.')
    if max_delay < delay:
        raise ValueError('"max_delay" must be greater than or equal to delay.')

    def decorated_function_with_retry(func):
        @wraps(func)
        def function_to_retry(*args, **kwargs):
            local_tries, local_delay = tries, delay
            while local_tries > 1:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if local_delay > max_delay:
                        local_delay = max_delay
                    logging.exception(
                        "%s: Retrying in %d seconds..." % (str(e), local_delay)
                    )
                    time.sleep(local_delay)
                    local_tries -= 1
                    local_delay *= backoff
            return func(*args, **kwargs)

        return function_to_retry

    return decorated_function_with_retry


def rate_limited(max_per_second):
    """This decorator limits how often a method can get called in a second.
    If the limit is exceeded, the call will be held in a queue until
    enough time has passed.
    Useful when trying to avoid overloading a system with rapid calls."""
    import threading

    min_interval = 1.0 / float(max_per_second)

    def decorate(func):
        last_time_called = [0.0]
        rate_lock = threading.Lock()  # To support multi-threading

        def rate_limited_function(*args, **kargs):
            try:
                rate_lock.acquire(True)
                elapsed = None
                if sys.version_info[0] >= 3:
                    elapsed = time.process_time() - last_time_called[0]
                else:
                    elapsed = time.clock() - last_time_called[0]
                wait_time_remaining = min_interval - elapsed
                if wait_time_remaining > 0:
                    time.sleep(wait_time_remaining)
                if sys.version_info[0] >= 3:
                    last_time_called[0] = time.process_time()
                else:
                    last_time_called[0] = time.clock()
            finally:
                rate_lock.release()
            return func(*args, **kargs)

        return rate_limited_function

    return decorate


def deprecated(message=None):
    """This decorator marks methods as deprecated.
    A warning is displayed if the method is called."""
    import inspect

    def decorated_method_to_deprecate(func):
        if inspect.isclass(func):
            # Handle a deprecated class differently from a deprecated method
            msg = "Class {}() is DEPRECATED!".format(func.__name__)
            if message:
                msg += " *** %s ***" % message
            warnings.simplefilter("always", DeprecationWarning)  # See Warnings
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)  # Set Default
            return func

        @wraps(func)
        def new_func(*args, **kwargs):
            msg = "Method {}() is DEPRECATED!".format(func.__name__)
            if message:
                msg += " *** %s ***" % message
            warnings.simplefilter("always", DeprecationWarning)  # See Warnings
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)  # Set Default
            return func(*args, **kwargs)

        return new_func

    return decorated_method_to_deprecate
