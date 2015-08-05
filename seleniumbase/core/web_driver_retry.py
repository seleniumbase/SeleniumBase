from selenium.common.exceptions import WebDriverException
import time


def web_driver_retry(in_func, timeout=30):
    tic = time.time()
    end_time = tic + timeout
    timeout = 5
    while time.time() < end_time:
        try:
            return in_func()
        except (WebDriverException, AssertionError), e:
            if (time.time() - tic) < 5:
                sleep_for = 0.25
            else:
                sleep_for = 1
            time.sleep(sleep_for)
    raise e


def asserts_visible(in_func):
    def out_func():
        element = in_func()
        if len(element) and element[0].is_displayed():
            return element[0]
        raise WebDriverException
    return out_func

