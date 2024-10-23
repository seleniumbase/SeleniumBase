import logging
import math
import time
import warnings
from contextlib import contextmanager
from functools import wraps
from seleniumbase.common.exceptions import TimeoutException


@contextmanager
def print_runtime(description=None, limit=None):
    """Print the runtime duration of a method or "with"-block after completion.
    If limit, fail if the runtime duration exceeds the limit after completion.

    Method / Function example usage ->
        from seleniumbase import decorators

        @decorators.print_runtime("My Method")
        def my_method():
            # code ...
            # code ...

    "with"-block example usage ->
        from seleniumbase import decorators

        with decorators.print_runtime("My Code Block"):
            # code ...
            # code ... """
    if not description:
        description = "Code Block"
    description = str(description)
    if limit:
        limit = float("%.2f" % limit)
        if limit < 0.01:
            limit = 0.01  # Minimum runtime limit
    exception = None
    start_time = time.time()
    try:
        yield
    except Exception as e:
        exception = e
        raise
    finally:
        end_time = time.time()
        run_time = end_time - start_time
        name = description
        # Print times with a statistically significant number of decimal places
        if run_time < 0.0001:
            print("<info> - {%s} ran for %.7f seconds." % (name, run_time))
        elif run_time < 0.001:
            print("<info> - {%s} ran for %.6f seconds." % (name, run_time))
        elif run_time < 0.01:
            print("<info> - {%s} ran for %.5f seconds." % (name, run_time))
        elif run_time < 0.1:
            print("<info> - {%s} ran for %.4f seconds." % (name, run_time))
        elif run_time < 1:
            print("<info> - {%s} ran for %.3f seconds." % (name, run_time))
        else:
            print("<info> - {%s} ran for %.2f seconds." % (name, run_time))
        if limit and limit > 0 and run_time > limit:
            message = (
                "\n {%s} duration of %.2fs exceeded the time limit of %.2fs!"
                % (name, run_time, limit)
            )
            if exception:
                message = exception.msg + "\nAND " + message
            raise TimeoutException(message)


@contextmanager
def runtime_limit(limit, description=None):
    """Fail if the runtime duration of a method or "with"-block exceeds limit.
    (The failure won't occur until after the method or "with"-block completes.)

    Method / Function example usage ->
        from seleniumbase import decorators

        @decorators.runtime_limit(4.5)
        def my_method():
            # code ...
            # code ...

    "with"-block example usage ->
        from seleniumbase import decorators

        with decorators.runtime_limit(32):
            # code ...
            # code ... """
    limit = float("%.2f" % limit)
    if limit < 0.01:
        limit = 0.01  # Minimum runtime limit
    if not description:
        description = "Code Block"
    description = str(description)
    exception = None
    start_time = time.time()
    try:
        yield
    except Exception as e:
        exception = e
        raise
    finally:
        end_time = time.time()
        run_time = end_time - start_time
        # Fail if the runtime of the code block exceeds the limit
        if limit and limit > 0 and run_time > limit:
            message = (
                "\n {%s} duration of %.2fs exceeded the time limit of %.2fs!"
                % (description, run_time, limit)
            )
            if exception:
                message = exception.msg + "\nAND " + message
            raise TimeoutException(message)


def retry_on_exception(tries=6, delay=1, backoff=2, max_delay=32):
    """Decorator for implementing exponential backoff for retrying on failures.

    tries: Max number of tries to execute the wrapped function before failing.
    delay: Delay time in seconds before the FIRST retry.
    backoff: Multiplier to extend the initial delay by for each retry.
    max_delay: Max time in seconds to wait between retries."""
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
                elapsed = time.process_time() - last_time_called[0]
                wait_time_remaining = min_interval - elapsed
                if wait_time_remaining > 0:
                    time.sleep(wait_time_remaining)
                last_time_called[0] = time.process_time()
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
