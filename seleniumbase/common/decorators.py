import logging
import math
import threading
import time
from functools import wraps


def retry_on_exception(tries=6, delay=1, backoff=2, max_delay=32):
    '''
    Decorator for implementing exponential backoff for retrying on failures.

    tries: Max number of tries to execute the wrapped function before failing.
    delay: Delay time in seconds before the FIRST retry.
    backoff: Multiplier to extend the initial delay by for each retry.
    max_delay: Max time in seconds to wait between retries.
    '''
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
                except Exception, e:
                    if local_delay > max_delay:
                        local_delay = max_delay
                    logging.exception('%s: Retrying in %d seconds...'
                                      % (str(e), local_delay))
                    time.sleep(local_delay)
                    local_tries -= 1
                    local_delay *= backoff
            return func(*args, **kwargs)
        return function_to_retry
    return decorated_function_with_retry


def rate_limited(max_per_second):
    min_interval = 1.0 / float(max_per_second)

    def decorate(func):
        last_time_called = [0.0]
        rate_lock = threading.Lock()  # To support multi-threading

        def rate_limited_function(*args, **kargs):
            try:
                rate_lock.acquire(True)
                elapsed = time.clock() - last_time_called[0]
                wait_time_remaining = min_interval - elapsed
                if wait_time_remaining > 0:
                    time.sleep(wait_time_remaining)
                last_time_called[0] = time.clock()
            finally:
                rate_lock.release()
            return func(*args, **kargs)
        return rate_limited_function
    return decorate
