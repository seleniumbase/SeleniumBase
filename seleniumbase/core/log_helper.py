# -*- coding: utf-8 -*-
import codecs
import os
import shutil
import sys
import time
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.fixtures import constants


def log_screenshot(test_logpath, driver, screenshot=None, get=False):
    screenshot_name = settings.SCREENSHOT_NAME
    screenshot_path = os.path.join(test_logpath, screenshot_name)
    screenshot_warning = constants.Warnings.SCREENSHOT_UNDEFINED
    try:
        if not screenshot:
            element = driver.find_element_by_tag_name("body")
            screenshot = element.screenshot_as_base64
        if screenshot != screenshot_warning:
            with open(screenshot_path, "wb") as file:
                file.write(screenshot)
        else:
            print("WARNING: %s" % screenshot_warning)
        if get:
            return screenshot
    except Exception:
        try:
            driver.get_screenshot_as_file(screenshot_path)
        except Exception:
            print("WARNING: %s" % screenshot_warning)


def get_master_time():
    """Returns (timestamp, the_date, the_time)"""
    import datetime

    timestamp = str(int(time.time())) + "  (Unix Timestamp)"
    now = datetime.datetime.now()
    utc_offset = -time.timezone / 3600.0
    utc_str = "UTC+0"
    if utc_offset > 0:
        if utc_offset < 10:
            utc_str = "UTC+0%s" % utc_offset
        else:
            utc_str = "UTC+%s" % utc_offset
    elif utc_offset < 0:
        if utc_offset > -10:
            utc_str = "UTC-0%s" % abs(utc_offset)
        else:
            utc_str = "UTC-%s" % abs(utc_offset)
    utc_str = utc_str.replace(".5", ".3").replace(".", ":") + "0"
    time_zone = ""
    try:
        time_zone = "(" + time.tzname[time.daylight] + ", " + utc_str + ")"
    except Exception:
        time_zone = "(" + utc_str + ")"
    # Use [Day-of-Week, Month Day, Year] format when time zone < GMT/UTC-3
    the_date = now.strftime("%A, %B %d, %Y").replace(" 0", " ")
    if utc_offset >= -3:
        # Use [Day-of-Week, Day Month Year] format when time zone >= GMT/UTC-3
        the_date = now.strftime("%A, %d %B %Y").replace(" 0", " ")
    the_time = now.strftime("%I:%M:%S %p  ") + time_zone
    if the_time.startswith("0"):
        the_time = the_time[1:]
    return timestamp, the_date, the_time


def get_browser_version(driver):
    driver_capabilities = driver.capabilities
    if "version" in driver_capabilities:
        browser_version = driver_capabilities["version"]
    else:
        browser_version = driver_capabilities["browserVersion"]
    return browser_version


def get_driver_name_and_version(driver, browser):
    if driver.capabilities["browserName"].lower() == "chrome":
        cap_dict = driver.capabilities["chrome"]
        return ("chromedriver", cap_dict["chromedriverVersion"].split(" ")[0])
    elif driver.capabilities["browserName"].lower() == "msedge":
        cap_dict = driver.capabilities["msedge"]
        return ("msedgedriver", cap_dict["msedgedriverVersion"].split(" ")[0])
    elif driver.capabilities["browserName"].lower() == "opera":
        cap_dict = driver.capabilities["opera"]
        return ("operadriver", cap_dict["operadriverVersion"].split(" ")[0])
    elif driver.capabilities["browserName"].lower() == "firefox":
        return ("geckodriver", driver.capabilities["moz:geckodriverVersion"])
    elif browser == "safari":
        return ("safaridriver", get_browser_version(driver))
    elif browser == "ie":
        return ("iedriver", get_browser_version(driver))
    else:
        return None


def log_test_failure_data(test, test_logpath, driver, browser, url=None):
    import traceback

    browser_displayed = browser
    driver_displayed = None
    browser_version = None
    driver_version = None
    driver_name = None
    duration = None
    exc_message = None
    try:
        browser_version = get_browser_version(driver)
    except Exception:
        pass
    try:
        driver_name, driver_version = get_driver_name_and_version(
            driver, browser
        )
    except Exception:
        pass
    try:
        duration = "%.2fs" % (time.time() - (sb_config.start_time_ms / 1000.0))
    except Exception:
        duration = "(Unknown Duration)"
    if browser_version:
        headless = ""
        if test.headless and browser in ["chrome", "edge", "firefox"]:
            headless = " / headless"
        if test.headless2 and browser in ["chrome", "edge"]:
            headless = " / headless2"
        if browser and len(browser) > 1:
            # Capitalize the first letter
            browser = "%s%s" % (browser[0].upper(), browser[1:])
        browser_displayed = "%s %s%s" % (browser, browser_version, headless)
        if driver_name and driver_version:
            driver_displayed = "%s %s" % (driver_name, driver_version)
    else:
        browser_displayed = browser
        driver_displayed = "(Unknown Driver)"
    if not driver_displayed:
        driver_displayed = "(Unknown Driver)"
    basic_info_name = settings.BASIC_INFO_NAME
    basic_file_path = os.path.join(test_logpath, basic_info_name)
    if url:
        last_page = url
    else:
        last_page = get_last_page(driver)
    sb_config._fail_page = last_page
    timestamp, the_date, the_time = get_master_time()
    test_id = get_test_id(test)  # pytest runnable display_id (with the "::")
    data_to_save = []
    data_to_save.append("%s" % test_id)
    data_to_save.append(
        "--------------------------------------------------------------------"
    )
    data_to_save.append("Last Page: %s" % last_page)
    data_to_save.append(" Duration: %s" % duration)
    data_to_save.append("  Browser: %s" % browser_displayed)
    data_to_save.append("   Driver: %s" % driver_displayed)
    data_to_save.append("Timestamp: %s" % timestamp)
    data_to_save.append("     Date: %s" % the_date)
    data_to_save.append("     Time: %s" % the_time)
    data_to_save.append(
        "--------------------------------------------------------------------"
    )
    if (
        sys.version_info[0] >= 3
        and hasattr(test, "_outcome")
        and (hasattr(test._outcome, "errors") and test._outcome.errors)
    ):
        try:
            exc_message = test._outcome.errors[0][1][1]
            traceback_address = test._outcome.errors[0][1][2]
            traceback_list = traceback.format_list(
                traceback.extract_tb(traceback_address)[1:]
            )
            traceback_message = "".join(traceback_list).strip()
        except Exception:
            exc_message = "(Unknown Exception)"
            traceback_message = "(Unknown Traceback)"
        data_to_save.append("Traceback: " + traceback_message)
        data_to_save.append("Exception: " + str(exc_message))
    else:
        traceback_message = None
        if hasattr(test, "is_behave") and test.is_behave:
            if sb_config.behave_scenario.status.name == "failed":
                if sb_config.behave_step.error_message:
                    traceback_message = sb_config.behave_step.error_message
        else:
            traceback_message = "".join(
                traceback.format_exception(
                    sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2],
                )
            )
        if (
            not traceback_message
            or len(str(traceback_message)) < 30
            or traceback_message.endswith("StopIteration\n")
        ):
            good_stack = []
            the_stacks = []
            if hasattr(sys, "last_traceback"):
                the_stacks = traceback.format_list(
                    traceback.extract_tb(sys.last_traceback)
                )
            else:
                message = None
                if hasattr(test, "is_behave") and test.is_behave:
                    message = "Behave step was not implemented or skipped!"
                else:
                    message = "Traceback not found!"
                the_stacks = [message]
            for stack in the_stacks:
                if "/site-packages/pluggy/" not in stack:
                    if "/site-packages/_pytest/" not in stack:
                        good_stack.append(stack)
            traceback_message = "".join(good_stack)
            data_to_save.append("Traceback: " + traceback_message)
            if hasattr(sys, "last_value"):
                last_value = sys.last_value
                if last_value:
                    data_to_save.append("Exception: " + str(last_value))
        else:
            data_to_save.append("Traceback: " + traceback_message)
    if hasattr(test, "is_nosetest") and test.is_nosetest:
        # Also save the data for the report
        sb_config._report_test_id = test_id
        sb_config._report_fail_page = last_page
        sb_config._report_duration = duration
        sb_config._report_browser = browser_displayed
        sb_config._report_driver = driver_displayed
        sb_config._report_timestamp = timestamp
        sb_config._report_date = the_date
        sb_config._report_time = the_time
        sb_config._report_traceback = traceback_message
        sb_config._report_exception = exc_message
    log_file = codecs.open(basic_file_path, "w+", "utf-8")
    log_file.writelines("\r\n".join(data_to_save))
    log_file.close()


def log_skipped_test_data(test, test_logpath, driver, browser, reason):
    browser_displayed = browser
    driver_displayed = None
    browser_version = None
    driver_version = None
    driver_name = None
    try:
        browser_version = get_browser_version(driver)
    except Exception:
        pass
    try:
        driver_name, driver_version = get_driver_name_and_version(
            driver, browser
        )
    except Exception:
        pass
    if browser_version:
        headless = ""
        if test.headless and browser in ["chrome", "edge", "firefox"]:
            headless = " / headless"
        if test.headless2 and browser in ["chrome", "edge"]:
            headless = " / headless2"
        if browser and len(browser) > 1:
            # Capitalize the first letter
            browser = "%s%s" % (browser[0].upper(), browser[1:])
        browser_displayed = "%s %s%s" % (browser, browser_version, headless)
        if driver_name and driver_version:
            driver_displayed = "%s %s" % (driver_name, driver_version)
    else:
        browser_displayed = browser
        driver_displayed = "(Unknown Driver)"
    if not driver_displayed:
        driver_displayed = "(Unknown Driver)"
    timestamp, the_date, the_time = get_master_time()
    test_id = get_test_id(test)  # pytest runnable display_id (with the "::")
    data_to_save = []
    data_to_save.append("%s" % test_id)
    data_to_save.append(
        "--------------------------------------------------------------------"
    )
    data_to_save.append("       Outcome: SKIPPED")
    data_to_save.append("       Browser: %s" % browser_displayed)
    data_to_save.append("        Driver: %s" % driver_displayed)
    data_to_save.append("     Timestamp: %s" % timestamp)
    data_to_save.append("          Date: %s" % the_date)
    data_to_save.append("          Time: %s" % the_time)
    data_to_save.append(
        "--------------------------------------------------------------------"
    )
    data_to_save.append(" * Skip Reason: %s" % reason)
    data_to_save.append("")
    file_path = os.path.join(test_logpath, "skip_reason.txt")
    log_file = codecs.open(file_path, "w+", encoding="utf-8")
    log_file.writelines("\r\n".join(data_to_save))
    log_file.close()


def log_page_source(test_logpath, driver, source=None):
    html_file_name = settings.PAGE_SOURCE_NAME
    if source:
        page_source = source
    else:
        try:
            page_source = driver.page_source
            page_source = get_html_source_with_base_href(driver, page_source)
        except Exception:
            source = constants.Warnings.PAGE_SOURCE_UNDEFINED
            page_source = constants.Warnings.PAGE_SOURCE_UNDEFINED
    if source == constants.Warnings.PAGE_SOURCE_UNDEFINED:
        page_source = (
            "<h3>Warning: "
            + source
            + (
                "</h3>\n<h4>The browser window was either unreachable, "
                "unresponsive, or closed prematurely!</h4>"
            )
        )
    html_file_path = os.path.join(test_logpath, html_file_name)
    html_file = codecs.open(html_file_path, "w+", "utf-8")
    html_file.write(page_source)
    html_file.close()


def get_test_id(test):
    if hasattr(test, "is_behave") and test.is_behave:
        file_name = sb_config.behave_scenario.filename
        line_num = sb_config.behave_line_num
        scenario_name = sb_config.behave_scenario.name
        if " -- @" in scenario_name:
            scenario_name = scenario_name.split(" -- @")[0]
        test_id = "%s:%s => %s" % (file_name, line_num, scenario_name)
        return test_id
    elif hasattr(test, "is_context_manager") and test.is_context_manager:
        filename = test.__class__.__module__.split(".")[-1] + ".py"
        classname = test.__class__.__name__
        methodname = test._testMethodName
        context_id = None
        if filename == "base_case.py" or methodname == "runTest":
            import traceback

            stack_base = traceback.format_stack()[0].split(", in ")[0]
            test_base = stack_base.split(", in ")[0].split(os.sep)[-1]
            if hasattr(test, "cm_filename") and test.cm_filename:
                filename = test.cm_filename
            else:
                filename = test_base.split('"')[0]
            classname = "SB"
            methodname = ".py:" + test_base.split(", line ")[-1]
            context_id = filename.split(".")[0] + methodname + ":" + classname
            return context_id
    test_id = None
    try:
        test_id = get_test_name(test)
    except Exception:
        test_id = "%s.%s.%s" % (
            test.__class__.__module__,
            test.__class__.__name__,
            test._testMethodName,
        )
        if test._sb_test_identifier and len(str(test._sb_test_identifier)) > 6:
            test_id = test._sb_test_identifier
    return test_id


def get_test_name(test):
    if "PYTEST_CURRENT_TEST" in os.environ:
        test_name = os.environ["PYTEST_CURRENT_TEST"].split(" ")[0]
    elif test.is_pytest:
        test_name = "%s.py::%s::%s" % (
            test.__class__.__module__.split(".")[-1],
            test.__class__.__name__,
            test._testMethodName,
        )
    else:
        test_name = "%s.py:%s.%s" % (
            test.__class__.__module__.split(".")[-1],
            test.__class__.__name__,
            test._testMethodName,
        )
    if test._sb_test_identifier and len(str(test._sb_test_identifier)) > 6:
        test_name = test._sb_test_identifier
        if hasattr(test, "_using_sb_fixture_class"):
            if test_name.count(".") >= 2:
                parts = test_name.split(".")
                full = parts[-3] + ".py::" + parts[-2] + "::" + parts[-1]
                test_name = full
        elif hasattr(test, "_using_sb_fixture_no_class"):
            if test_name.count(".") >= 1:
                parts = test_name.split(".")
                full = parts[-2] + ".py::" + parts[-1]
                test_name = full
    return test_name


def get_last_page(driver):
    try:
        last_page = driver.current_url
    except Exception:
        last_page = "[WARNING! Browser Not Open!]"
    if len(last_page) < 5:
        last_page = "[WARNING! Browser Not Open!]"
    return last_page


def get_base_url(full_url):
    protocol = full_url.split("://")[0]
    simple_url = full_url.split("://")[1]
    base_url = simple_url.split("/")[0]
    full_base_url = "%s://%s" % (protocol, base_url)
    return full_base_url


def get_base_href_html(full_url):
    """The base href line tells the html what the base page really is.
    This is important when trying to open the page outside it's home."""
    base_url = get_base_url(full_url)
    return '<base href="%s">' % base_url


def get_html_source_with_base_href(driver, page_source):
    """Combines the domain base href with the html source.
    Also adds on the meta charset, which may get dropped.
    This is needed for the page html to render correctly."""
    last_page = get_last_page(driver)
    meta_charset = '<meta charset="utf-8">'
    if "://" in last_page:
        base_href_html = get_base_href_html(last_page)
        if ' charset="' not in page_source:
            return "%s\n%s\n%s" % (base_href_html, meta_charset, page_source)
        else:
            return "%s\n%s" % (base_href_html, page_source)
    return ""


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
                os.stat(s).st_mtime - os.stat(d).st_mtime > 1
            ):
                shutil.copy2(s, d)


def archive_logs_if_set(log_path, archive_logs=False):
    """Handle Logging"""
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
                archived_folder = os.path.realpath(archived_folder) + "/"
                log_path = os.path.realpath(log_path) + "/"
                if not os.path.exists(archived_folder):
                    try:
                        os.makedirs(archived_folder)
                    except Exception:
                        pass  # Only reachable during multi-threaded runs
                time_id = str(int(time.time()))
                archived_logs = "%slogs_%s" % (archived_folder, time_id)
                copytree(log_path, archived_logs)


def log_folder_setup(log_path, archive_logs=False):
    """Handle Logging"""
    if log_path.endswith("/"):
        log_path = log_path[:-1]
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            pass  # Should only be reachable during multi-threaded runs
    else:
        archived_folder = "%s/../archived_logs/" % log_path
        archived_folder = os.path.realpath(archived_folder) + "/"
        if not os.path.exists(archived_folder):
            try:
                os.makedirs(archived_folder)
            except Exception:
                pass  # Should only be reachable during multi-threaded runs
        archived_logs = "%slogs_%s" % (archived_folder, int(time.time()))
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
