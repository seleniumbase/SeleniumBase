import sys
import traceback


def log_test_failure_data(log_file, driver, browser):
    try:
        last_page = driver.current_url
    except Exception:
        last_page = '[WARNING! Browser Not Open!]'
    if len(last_page) < 5:
        last_page = '[WARNING! Browser Not Open!]'
    data_to_save = []
    data_to_save.append("Last_Page: %s" % last_page)
    data_to_save.append("Browser: %s " % browser)
    data_to_save.append("Traceback: " + ''.join(
        traceback.format_exception(sys.exc_info()[0],
                                   sys.exc_info()[1],
                                   sys.exc_info()[2])))
    log_file.writelines("\r\n".join(data_to_save))
