import codecs
import os
import shutil
import sys
import time
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.core.style_sheet import get_report_style

LATEST_REPORT_DIR = settings.LATEST_REPORT_DIR
ARCHIVE_DIR = settings.REPORT_ARCHIVE_DIR
HTML_REPORT = settings.HTML_REPORT
RESULTS_TABLE = settings.RESULTS_TABLE


def get_timestamp():
    return str(int(time.time() * 1000))


def process_successes(test, test_count, duration):
    return '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"' % (
        test_count,
        "Passed!",
        "*",
        "*",
        "*",
        test.browser,
        get_timestamp()[:-3],
        duration,
        test.id(),
        "*",
    )


def save_test_failure_data(test, name, folder=None):
    """
    Saves failure data to the current directory, or to a subfolder if provided.
    If {name} does not end in ".txt", it will get added to it.
    If the folder provided doesn't exist, it will get created.
    """
    if not name.endswith(".txt"):
        name = name + ".txt"
    if folder:
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        failure_data_file_path = os.path.join(file_path, name)
    else:
        failure_data_file_path = name
    failure_data_file = codecs.open(failure_data_file_path, "w+", "utf-8")
    data_to_save = []
    if not hasattr(sb_config, "_report_test_id"):
        exc_message = "(Unknown Exception)"
        traceback_message = ""
        if hasattr(sb_config, "_report_traceback"):
            traceback_message = str(sb_config._report_traceback)
        if hasattr(sb_config, "_report_exception"):
            if type(sb_config._report_exception) is tuple:
                exc_message = str(sb_config._report_exception[1].message)
            else:
                exc_message = str(sb_config._report_exception)
        data_to_save.append(test.id())
        data_to_save.append(
            "----------------------------------------------------------------"
        )
        data_to_save.append("Last Page: %s" % test._last_page_url)
        data_to_save.append("  Browser: %s" % test.browser)
        data_to_save.append("Timestamp: %s" % get_timestamp()[:-3])
        data_to_save.append(
            "----------------------------------------------------------------"
        )
        data_to_save.append("Traceback: %s" % traceback_message)
        data_to_save.append("Exception: %s" % exc_message)
        failure_data_file.writelines("\r\n".join(data_to_save))
        failure_data_file.close()
        return
    data_to_save.append(sb_config._report_test_id)
    data_to_save.append(
        "--------------------------------------------------------------------"
    )
    data_to_save.append("Last Page: %s" % sb_config._report_fail_page)
    data_to_save.append(" Duration: %s" % sb_config._report_duration)
    data_to_save.append("  Browser: %s" % sb_config._report_browser)
    data_to_save.append("   Driver: %s" % sb_config._report_driver)
    data_to_save.append("Timestamp: %s" % sb_config._report_timestamp)
    data_to_save.append("     Date: %s" % sb_config._report_date)
    data_to_save.append("     Time: %s" % sb_config._report_time)
    data_to_save.append(
        "--------------------------------------------------------------------"
    )
    data_to_save.append("Traceback: %s" % sb_config._report_traceback)
    data_to_save.append("Exception: %s" % sb_config._report_exception)
    failure_data_file.writelines("\r\n".join(data_to_save))
    failure_data_file.close()


def process_failures(test, test_count, duration):
    bad_page_image = "failure_%s.png" % test_count
    bad_page_data = "failure_%s.txt" % test_count
    screenshot_path = os.path.join(LATEST_REPORT_DIR, bad_page_image)
    if hasattr(test, "_last_page_screenshot") and test._last_page_screenshot:
        with open(screenshot_path, "wb") as file:
            file.write(test._last_page_screenshot)
    save_test_failure_data(test, bad_page_data, folder=LATEST_REPORT_DIR)
    exc_message = None
    if (
        hasattr(test, "_outcome")
        and hasattr(test._outcome, "errors")
        and test._outcome.errors
    ):
        try:
            exc_message = test._outcome.errors[0][1][1]
        except Exception:
            exc_message = "(Unknown Exception)"
    else:
        try:
            exc_message = sys.last_value
        except Exception:
            exc_message = "(Unknown Exception)"
    if not hasattr(test, "_last_page_url"):
        test._last_page_url = "about:blank"
    return '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"' % (
        test_count,
        "FAILED!",
        bad_page_data,
        bad_page_image,
        test._last_page_url,
        test.browser,
        get_timestamp()[:-3],
        duration,
        test.id(),
        exc_message,
    )


def clear_out_old_report_logs(archive_past_runs=True, get_log_folder=False):
    abs_path = os.path.abspath(".")
    file_path = os.path.join(abs_path, LATEST_REPORT_DIR)
    if not os.path.exists(file_path):
        try:
            os.makedirs(file_path)
        except Exception:
            pass  # Should only be reachable during multi-threaded runs

    if archive_past_runs:
        archive_timestamp = int(time.time())
        archive_dir_root = os.path.join(file_path, "..", ARCHIVE_DIR)
        if not os.path.exists(archive_dir_root):
            os.makedirs(archive_dir_root)
        archive_dir = os.path.join(
            archive_dir_root, "report_%s" % archive_timestamp
        )
        shutil.move(file_path, archive_dir)
        os.makedirs(file_path)
        if get_log_folder:
            return archive_dir
    else:
        # Just delete bad pages to make room for the latest run.
        filelist = [
            f
            for f in os.listdir(os.path.join(".", LATEST_REPORT_DIR))
            if f.startswith("failure_")
            or (f == HTML_REPORT)
            or (f.startswith("automation_failure"))
            or (f == RESULTS_TABLE)
        ]
        for f in filelist:
            os.remove(os.path.join(file_path, f))


def add_bad_page_log_file(page_results_list):
    abs_path = os.path.abspath(".")
    file_path = os.path.join(abs_path, LATEST_REPORT_DIR)
    log_file = os.path.join(file_path, RESULTS_TABLE)
    f = open(log_file, "w")
    h_p1 = '"Num","Result","Stacktrace","Screenshot",'
    h_p2 = '"URL","Browser","Epoch Time","Duration",'
    h_p3 = '"Test Case Address","Additional Info"\n'
    page_header = h_p1 + h_p2 + h_p3
    f.write(page_header)
    for line in page_results_list:
        f.write("%s\n" % line)
    f.close()


def archive_new_report_logs():
    log_string = clear_out_old_report_logs(get_log_folder=True)
    log_folder = log_string.split("/")[-1]
    abs_path = os.path.abspath(".")
    file_path = os.path.join(abs_path, ARCHIVE_DIR)
    report_log_path = os.path.join(file_path, log_folder)
    return report_log_path


def add_results_page(html):
    abs_path = os.path.abspath(".")
    file_path = os.path.join(abs_path, LATEST_REPORT_DIR)
    results_file_name = HTML_REPORT
    results_file = os.path.join(file_path, results_file_name)
    f = open(results_file, "w")
    f.write(html)
    f.close()
    return results_file


def build_report(
    report_log_path,
    page_results_list,
    successes,
    failures,
    browser_type,
    show_report,
):

    web_log_path = "file://%s" % report_log_path
    successes_count = len(successes)
    failures_count = len(failures)
    total_test_count = successes_count + failures_count

    tf_color = "#11BB11"
    if failures_count > 0:
        tf_color = "#EE3A3A"

    summary_table = """<div><table><thead><tr>
        <th>TESTING SUMMARY</th>
        <th>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
        </tr></thead><tbody>
        <tr style="color:#00BB00"><td>TESTS PASSING: <td>%s</tr>
        <tr style="color:%s"     ><td>TESTS FAILING: <td>%s</tr>
        <tr style="color:#4D4DDD"><td>TOTAL TESTS: <td>%s</tr>
        </tbody></table>""" % (
        successes_count,
        tf_color,
        failures_count,
        total_test_count,
    )

    summary_table = (
        """<h1 id="ContextHeader" class="sectionHeader" title="">
        %s</h1>"""
        % summary_table
    )

    log_link_shown = os.path.join(
        "..", "%s%s" % (ARCHIVE_DIR, web_log_path.split(ARCHIVE_DIR)[1])
    )
    csv_link = os.path.join(web_log_path, RESULTS_TABLE)
    csv_link_shown = "%s" % RESULTS_TABLE
    log_table = """<p><p><p><p><h2><table><tbody>
        <tr><td>LOG FILES LINK:&nbsp;&nbsp;<td><a href="%s">%s</a></tr>
        <tr><td>RESULTS TABLE:&nbsp;&nbsp;<td><a href="%s">%s</a></tr>
        </tbody></table></h2><p><p><p><p>""" % (
        web_log_path,
        log_link_shown,
        csv_link,
        csv_link_shown,
    )

    failure_table = "<h2><table><tbody></div>"
    any_screenshots = False
    for line in page_results_list:
        line = line.split(",")
        if line[1] == '"FAILED!"':
            if not any_screenshots:
                any_screenshots = True
                failure_table += """<thead><tr>
                    <th>STACKTRACE&nbsp;&nbsp;</th>
                    <th>SCREENSHOT&nbsp;&nbsp;</th>
                    <th>LOCATION OF FAILURE</th>
                    </tr></thead>"""
            display_url = line[4]
            actual_url = line[4]
            if len(display_url) < 7:
                display_url = sb_config._report_fail_page
                actual_url = sb_config._report_fail_page
            if len(display_url) > 60:
                display_url = display_url[0:58] + "..."
            line = (
                '<a href="%s">%s</a>'
                % ("file://" + report_log_path + "/" + line[2], line[2])
                + """
                &nbsp;&nbsp;
                """
                + '<td><a href="%s">%s</a>'
                % ("file://" + report_log_path + "/" + line[3], line[3])
                + """
                &nbsp;&nbsp;
                """
                + '<td><a href="%s">%s</a>' % (actual_url, display_url)
            )
            line = line.replace('"', "")
            failure_table += "<tr><td>%s</tr>\n" % line
    failure_table += "</tbody></table></h2>"

    failing_list = ""
    if failures:
        failing_list = "<h2><table><tbody>"
        failing_list += """<thead><tr><th>LIST OF FAILING TESTS
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        </th></tr></thead>"""
        for failure in failures:
            failing_list += '<tr style="color:#EE3A3A"><td>%s</tr>\n' % failure
        failing_list += "</tbody></table></h2>"

    passing_list = ""
    if successes:
        passing_list = "<h2><table><tbody>"
        passing_list += """<thead><tr><th>LIST OF PASSING TESTS
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        </th></tr></thead>"""
        for success in successes:
            passing_list += '<tr style="color:#00BB00"><td>%s</tr>\n' % success
        passing_list += "</tbody></table></h2>"

    table_view = "%s%s%s%s%s" % (
        summary_table,
        log_table,
        failure_table,
        failing_list,
        passing_list,
    )
    report_html = "<html><head>%s</head><body>%s</body></html>" % (
        get_report_style(),
        table_view,
    )
    results_file = add_results_page(report_html)
    archived_results_file = report_log_path + "/" + HTML_REPORT
    shutil.copyfile(results_file, archived_results_file)
    print("\n* The latest html report page is located at:\n" + results_file)
    print(
        "\n* Files saved for this report are located at:\n" + report_log_path
    )
    print("")
    if show_report:
        from seleniumbase import get_driver

        driver = get_driver(browser_type, headless=False)
        driver.get("file://%s" % archived_results_file)
        print("\n*** Close the html report window to continue. ***")
        while len(driver.window_handles):
            time.sleep(0.1)
        driver.quit()
