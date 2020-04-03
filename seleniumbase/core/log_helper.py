import codecs
import os
import shutil
import sys
import time
import traceback
from seleniumbase.config import settings


def log_screenshot(test_logpath, driver, screenshot=None, get=False):
    screenshot_name = settings.SCREENSHOT_NAME
    screenshot_path = "%s/%s" % (test_logpath, screenshot_name)
    try:
        if not screenshot:
            element = driver.find_element_by_tag_name('body')
            screenshot = element.screenshot_as_base64
        with open(screenshot_path, "wb") as file:
            file.write(screenshot)
        if get:
            return screenshot
    except Exception:
        try:
            driver.get_screenshot_as_file(screenshot_path)
        except Exception:
            print("WARNING: Unable to get screenshot for failure logs!")


def log_test_failure_data(test, test_logpath, driver, browser, url=None):
    basic_info_name = settings.BASIC_INFO_NAME
    basic_file_path = "%s/%s" % (test_logpath, basic_info_name)
    log_file = codecs.open(basic_file_path, "w+", "utf-8")
    if url:
        last_page = url
    else:
        last_page = get_last_page(driver)
    data_to_save = []
    data_to_save.append("Last Page: %s" % last_page)
    data_to_save.append("  Browser: %s" % browser)
    data_to_save.append("Timestamp: %s" % int(time.time()))
    if sys.version_info[0] >= 3 and hasattr(test, '_outcome'):
        if test._outcome.errors:
            try:
                exc_message = test._outcome.errors[0][1][1]
                traceback_address = test._outcome.errors[0][1][2]
                traceback_list = traceback.format_list(
                    traceback.extract_tb(traceback_address)[1:])
                traceback_message = ''.join(traceback_list).strip()
            except Exception:
                exc_message = "(Unknown Exception)"
                traceback_message = "(Unknown Traceback)"
            data_to_save.append("Traceback: " + traceback_message)
            data_to_save.append("Exception: " + str(exc_message))
    else:
        data_to_save.append("Traceback: " + ''.join(
            traceback.format_exception(sys.exc_info()[0],
                                       sys.exc_info()[1],
                                       sys.exc_info()[2])))
    log_file.writelines("\r\n".join(data_to_save))
    log_file.close()


def log_page_source(test_logpath, driver, source=None):
    html_file_name = settings.PAGE_SOURCE_NAME
    if source:
        page_source = source
    else:
        try:
            page_source = driver.page_source
        except Exception:
            # Since we can't get the page source from here, skip saving it
            return
    html_file_path = "%s/%s" % (test_logpath, html_file_name)
    html_file = codecs.open(html_file_path, "w+", "utf-8")
    rendered_source = get_html_source_with_base_href(driver, page_source)
    html_file.write(rendered_source)
    html_file.close()


def get_last_page(driver):
    try:
        last_page = driver.current_url
    except Exception:
        last_page = '[WARNING! Browser Not Open!]'
    if len(last_page) < 5:
        last_page = '[WARNING! Browser Not Open!]'
    return last_page


def get_base_url(full_url):
    protocol = full_url.split('://')[0]
    simple_url = full_url.split('://')[1]
    base_url = simple_url.split('/')[0]
    full_base_url = "%s://%s" % (protocol, base_url)
    return full_base_url


def get_base_href_html(full_url):
    ''' The base href line tells the html what the base page really is.
        This is important when trying to open the page outside it's home. '''
    base_url = get_base_url(full_url)
    return '<base href="%s">' % base_url


def get_html_source_with_base_href(driver, page_source):
    ''' Combines the domain base href with the html source.
        This is needed for the page html to render correctly. '''
    last_page = get_last_page(driver)
    if '://' in last_page:
        base_href_html = get_base_href_html(last_page)
        return '%s\n%s' % (base_href_html, page_source)
    return ''


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or (
                    os.stat(s).st_mtime - os.stat(d).st_mtime > 1):
                shutil.copy2(s, d)


def archive_logs_if_set(log_path, archive_logs=False):
    """ Handle Logging """
    arg_join = " ".join(sys.argv)
    if ("-n" in sys.argv) or ("-n=" in arg_join) or (arg_join == "-c"):
        return  # Skip if multithreaded
    if log_path.endswith("/"):
        log_path = log_path[:-1]
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            pass  # Only reachable during multi-threaded runs
    else:
        if settings.ARCHIVE_EXISTING_LOGS or archive_logs:
            if len(os.listdir(log_path)) > 0:
                archived_folder = "%s/../archived_logs/" % log_path
                archived_folder = os.path.realpath(archived_folder) + '/'
                log_path = os.path.realpath(log_path) + '/'
                if not os.path.exists(archived_folder):
                    try:
                        os.makedirs(archived_folder)
                    except Exception:
                        pass  # Only reachable during multi-threaded runs
                time_id = str(int(time.time()))
                archived_logs = "%slogs_%s" % (archived_folder, time_id)
                copytree(log_path, archived_logs)


def log_folder_setup(log_path, archive_logs=False):
    """ Handle Logging """
    if log_path.endswith("/"):
        log_path = log_path[:-1]
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            pass  # Should only be reachable during multi-threaded runs
    else:
        archived_folder = "%s/../archived_logs/" % log_path
        archived_folder = os.path.realpath(archived_folder) + '/'
        if not os.path.exists(archived_folder):
            try:
                os.makedirs(archived_folder)
            except Exception:
                pass  # Should only be reachable during multi-threaded runs
        archived_logs = "%slogs_%s" % (
            archived_folder, int(time.time()))

        if len(os.listdir(log_path)) > 0:
            try:
                shutil.move(log_path, archived_logs)
                os.makedirs(log_path)
            except Exception:
                pass  # A file was probably open at the time
            if not settings.ARCHIVE_EXISTING_LOGS and not archive_logs:
                shutil.rmtree(archived_logs)
            else:
                a_join = " ".join(sys.argv)
                if ("-n" in sys.argv) or ("-n=" in a_join) or (a_join == "-c"):
                    # Logs are saved/archived now if tests are multithreaded
                    pass
                else:
                    shutil.rmtree(archived_logs)  # (Archive test run later)
