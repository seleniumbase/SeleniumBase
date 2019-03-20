import os
import shutil
import sys
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.errorhandler import NoAlertPresentException
from seleniumbase import BaseCase
from seleniumbase.core.style_sheet import style
from seleniumbase.config import settings
from seleniumbase.fixtures import js_utils

LATEST_REPORT_DIR = settings.LATEST_REPORT_DIR
ARCHIVE_DIR = settings.REPORT_ARCHIVE_DIR
RESULTS_PAGE = settings.HTML_REPORT
BAD_PAGE_LOG = settings.RESULTS_TABLE
DEFAULT_VALIDATION_MESSAGE = settings.MASTERQA_DEFAULT_VALIDATION_MESSAGE
WAIT_TIME_BEFORE_VERIFY = settings.MASTERQA_WAIT_TIME_BEFORE_VERIFY
START_IN_FULL_SCREEN_MODE = settings.MASTERQA_START_IN_FULL_SCREEN_MODE
MAX_IDLE_TIME_BEFORE_QUIT = settings.MASTERQA_MAX_IDLE_TIME_BEFORE_QUIT

# This tool allows testers to quickly verify pages while assisted by automation


class __MasterQATestCase__(BaseCase):

    def get_timestamp(self):
        return str(int(time.time() * 1000))

    def manual_check_setup(self):
        self.manual_check_count = 0
        self.manual_check_successes = 0
        self.incomplete_runs = 0
        self.page_results_list = []
        self.clear_out_old_logs(archive_past_runs=False)

    def clear_out_old_logs(self, archive_past_runs=True, get_log_folder=False):
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % LATEST_REPORT_DIR
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        if archive_past_runs:
            archive_timestamp = int(time.time())
            if not os.path.exists("%s/../%s/" % (file_path, ARCHIVE_DIR)):
                os.makedirs("%s/../%s/" % (file_path, ARCHIVE_DIR))
            archive_dir = "%s/../%s/log_%s" % (
                file_path, ARCHIVE_DIR, archive_timestamp)
            shutil.move(file_path, archive_dir)
            os.makedirs(file_path)
            if get_log_folder:
                return archive_dir
        else:
            # Just delete bad pages to make room for the latest run.
            filelist = [f for f in os.listdir(
                "./%s" % LATEST_REPORT_DIR) if f.startswith("failed_") or (
                f == RESULTS_PAGE) or (f.startswith("automation_failure")) or (
                f == BAD_PAGE_LOG)]
            for f in filelist:
                os.remove("%s/%s" % (file_path, f))

    def jq_confirm_dialog(self, question):
        count = self.manual_check_count + 1
        title_content = ('<center><font color="#7700bb">Manual Check #%s:'
                         '</font></center><hr><font color="#0066ff">%s</font>'
                         '' % (count, question))
        title_content = js_utils.escape_quotes_if_needed(title_content)
        jqcd = ("""jconfirm({
                    boxWidth: '32.5%%',
                    useBootstrap: false,
                    containerFluid: false,
                    animationBounce: 1,
                    type: 'default',
                    theme: 'bootstrap',
                    typeAnimated: true,
                    animation: 'scale',
                    draggable: true,
                    dragWindowGap: 1,
                    container: 'body',
                    title: '%s',
                    content: '',
                    buttons: {
                        fail_button: {
                            btnClass: 'btn-red',
                            text: 'NO / FAIL',
                            action: function(){
                                $jqc_status = "Failure!"
                            }
                        },
                        pass_button: {
                            btnClass: 'btn-green',
                            text: 'YES / PASS',
                            action: function(){
                                $jqc_status = "Success!"
                            }
                        }
                    }
                });""" % title_content)
        self.execute_script(jqcd)

    def manual_page_check(self, *args):
        if not args:
            instructions = DEFAULT_VALIDATION_MESSAGE  # self.verify()
        else:
            instructions = str(args[0])
            if len(args) > 1:
                pass

        question = "Approve?"  # self.verify("")
        if instructions and "?" not in instructions:
            question = instructions + " <> Approve?"
        elif instructions and "?" in instructions:
            question = instructions

        use_jqc = False
        self.wait_for_ready_state_complete()
        if js_utils.is_jquery_confirm_activated(self.driver):
            use_jqc = True
        else:
            js_utils.activate_jquery_confirm(self.driver)
            get_jqc = None
            try:
                get_jqc = self.execute_script("return jconfirm")
                get_jqc = get_jqc["instances"]
                use_jqc = True
            except Exception:
                use_jqc = False

        if use_jqc:
            wait_time_before_verify = WAIT_TIME_BEFORE_VERIFY
            if self.verify_delay:
                wait_time_before_verify = float(self.verify_delay)
            # Allow a moment to see the full page before the dialog box pops up
            time.sleep(wait_time_before_verify)

            # Use the jquery_confirm library for manual page checks
            self.jq_confirm_dialog(question)
            time.sleep(0.02)
            waiting_for_response = True
            while waiting_for_response:
                time.sleep(0.05)
                jqc_open = self.execute_script(
                    "return jconfirm.instances.length")
                if str(jqc_open) == "0":
                    break
            time.sleep(0.1)
            status = None
            try:
                status = self.execute_script("return $jqc_status")
            except Exception:
                status = "Failure!"
                pre_status = self.execute_script(
                    "return jconfirm.lastClicked.hasClass('btn-green')")
                if pre_status:
                    status = "Success!"
        else:
            # Fallback to plain js confirm dialogs if can't load jquery_confirm
            if self.browser == 'ie':
                text = self.execute_script(
                    '''if(confirm("%s")){return "Success!"}
                    else{return "Failure!"}''' % question)
            elif self.browser == 'chrome':
                self.execute_script('''if(confirm("%s"))
                    {window.master_qa_result="Success!"}
                    else{window.master_qa_result="Failure!"}''' % question)
                time.sleep(0.05)
                self.wait_for_special_alert_absent()
                text = self.execute_script('return window.master_qa_result')
            else:
                try:
                    self.execute_script(
                        '''if(confirm("%s"))
                        {window.master_qa_result="Success!"}
                        else{window.master_qa_result="Failure!"}''' % question)
                except WebDriverException:
                    # Fix for https://github.com/mozilla/geckodriver/issues/431
                    pass
                time.sleep(0.05)
                self.wait_for_special_alert_absent()
                text = self.execute_script('return window.master_qa_result')
            status = text

        self.manual_check_count += 1
        try:
            current_url = self.driver.current_url
        except Exception:
            current_url = self.execute_script("return document.URL")
        if "Success!" in str(status):
            self.manual_check_successes += 1
            self.page_results_list.append(
                '"%s","%s","%s","%s","%s","%s","%s","%s"' % (
                    self.manual_check_count,
                    "Success",
                    "-",
                    current_url,
                    self.browser,
                    self.get_timestamp()[:-3],
                    instructions,
                    "*"))
            return 1
        else:
            bad_page_name = "failed_check_%s.png" % self.manual_check_count
            self.save_screenshot(bad_page_name, folder=LATEST_REPORT_DIR)
            self.page_results_list.append(
                '"%s","%s","%s","%s","%s","%s","%s","%s"' % (
                    self.manual_check_count,
                    "FAILED!",
                    bad_page_name,
                    current_url,
                    self.browser,
                    self.get_timestamp()[:-3],
                    instructions,
                    "*"))
            return 0

    def wait_for_special_alert_absent(self, timeout=MAX_IDLE_TIME_BEFORE_QUIT):
        for x in range(int(timeout * 20)):
            try:
                alert = self.driver.switch_to.alert
                dummy_variable = alert.text  # Raises exception if no alert
                if "?" not in dummy_variable:
                    return
                time.sleep(0.05)
            except NoAlertPresentException:
                return
        self.driver.quit()
        raise Exception(
            "%s seconds passed without human action! Stopping..." % timeout)

    def add_failure(self, exception=None):
        exc_info = None
        if exception:
            if hasattr(exception, 'msg'):
                exc_info = exception.msg
            elif hasattr(exception, 'message'):
                exc_info = exception.message
            else:
                exc_info = '(Unknown Exception)'

        self.incomplete_runs += 1
        error_page = "automation_failure_%s.png" % self.incomplete_runs
        self.save_screenshot(error_page, folder=LATEST_REPORT_DIR)
        self.page_results_list.append(
            '"%s","%s","%s","%s","%s","%s","%s","%s"' % (
                "ERR",
                "ERROR!",
                error_page,
                self.driver.current_url,
                self.browser,
                self.get_timestamp()[:-3],
                "-",
                exc_info))
        try:
            # Return to the original window if another was opened
            self.driver.switch_to_window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
        except Exception:
            pass

    def add_bad_page_log_file(self):
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % LATEST_REPORT_DIR
        log_file = "%s/%s" % (file_path, BAD_PAGE_LOG)
        f = open(log_file, 'w')
        h_p1 = '''"Num","Result","Screenshot","URL","Browser","Epoch Time",'''
        h_p2 = '''"Verification Instructions","Additional Info"\n'''
        page_header = h_p1 + h_p2
        f.write(page_header)
        for line in self.page_results_list:
            f.write("%s\n" % line)
        f.close()

    def add_results_page(self, html):
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % LATEST_REPORT_DIR
        results_file_name = RESULTS_PAGE
        results_file = "%s/%s" % (file_path, results_file_name)
        f = open(results_file, 'w')
        f.write(html)
        f.close()
        return results_file

    def process_manual_check_results(self, auto_close_results_page=False):
        perfection = True
        failures_count = self.manual_check_count - self.manual_check_successes
        print("\n\n*** Test Result: ***")
        if self.manual_check_successes == self.manual_check_count:
            pass
        else:
            print("WARNING: There were page issues detected!")
            perfection = False

        if self.incomplete_runs > 0:
            print("WARNING: Not all tests finished running!")
            perfection = False

        if perfection:
            if self.manual_check_count > 0:
                print("SUCCESS: Everything checks out OKAY!")
            else:
                print("WARNING: No manual checks were performed!")
        else:
            pass
        self.add_bad_page_log_file()  # Includes successful results

        log_string = self.clear_out_old_logs(get_log_folder=True)
        log_folder = log_string.split('/')[-1]
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % ARCHIVE_DIR
        log_path = "%s/%s" % (file_path, log_folder)
        web_log_path = "file://%s" % log_path

        tf_color = "#11BB11"
        if failures_count > 0:
            tf_color = "#EE3A3A"

        ir_color = "#11BB11"
        if self.incomplete_runs > 0:
            ir_color = "#EE3A3A"

        summary_table = '''<div><table><thead><tr>
              <th>TESTING SUMMARY</th>
              <th>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
              </tr></thead><tbody>
              <tr style="color:#00BB00"><td>CHECKS PASSED: <td>%s</tr>
              <tr style="color:%s"     ><td>CHECKS FAILED: <td>%s</tr>
              <tr style="color:#4D4DDD"><td>TOTAL VERIFICATIONS: <td>%s</tr>
              <tr style="color:%s"     ><td>INCOMPLETE TEST RUNS: <td>%s</tr>
              </tbody></table>''' % (self.manual_check_successes,
                                     tf_color,
                                     failures_count,
                                     self.manual_check_count,
                                     ir_color,
                                     self.incomplete_runs)

        summary_table = '''<h1 id="ContextHeader" class="sectionHeader" title="">
                     %s</h1>''' % summary_table

        log_link_shown = '../%s%s/' % (
            ARCHIVE_DIR, web_log_path.split(ARCHIVE_DIR)[1])
        csv_link = '%s/%s' % (web_log_path, BAD_PAGE_LOG)
        csv_link_shown = '%s' % BAD_PAGE_LOG
        log_table = '''<p><p><p><p><h2><table><tbody>
            <tr><td>LOG FILES LINK:&nbsp;&nbsp;<td><a href="%s">%s</a></tr>
            <tr><td>RESULTS TABLE:&nbsp;&nbsp;<td><a href="%s">%s</a></tr>
            </tbody></table></h2><p><p><p><p>''' % (
            web_log_path, log_link_shown, csv_link, csv_link_shown)

        failure_table = '<h2><table><tbody></div>'
        any_screenshots = False
        for line in self.page_results_list:
            line = line.split(',')
            if line[1] == '"FAILED!"' or line[1] == '"ERROR!"':
                if not any_screenshots:
                    any_screenshots = True
                    failure_table += '''<thead><tr>
                        <th>SCREENSHOT FILE&nbsp;&nbsp;&nbsp;&nbsp;</th>
                        <th>LOCATION OF FAILURE</th>
                        </tr></thead>'''
                display_url = line[3]
                if len(display_url) > 60:
                    display_url = display_url[0:58] + '...'
                line = '<a href="%s">%s</a>' % (
                    "file://" + log_path + '/' + line[2], line[2]) + '''
                    &nbsp;&nbsp;&nbsp;&nbsp;<td>
                    ''' + '<a href="%s">%s</a>' % (line[3], display_url)
                line = line.replace('"', '')
                failure_table += '<tr><td>%s</tr>\n' % line
        failure_table += '</tbody></table>'
        table_view = '%s%s%s' % (
            summary_table, log_table, failure_table)
        report_html = '<html><head>%s</head><body>%s</body></html>' % (
            style, table_view)
        results_file = self.add_results_page(report_html)
        archived_results_file = log_path + '/' + RESULTS_PAGE
        shutil.copyfile(results_file, archived_results_file)
        print(
            "\n*** The results html page is located at: ***\n" + results_file)
        self.open("file://%s" % archived_results_file)
        if auto_close_results_page:
            # Long enough to notice the results before closing the page
            time.sleep(1.0)
        else:
            # The user can decide when to close the results page
            print("\n*** Close the html report window to continue ***")
            while len(self.driver.window_handles):
                time.sleep(0.1)


class MasterQA(__MasterQATestCase__):

    def setUp(self):
        self.check_count = 0
        self.auto_close_results_page = False
        super(__MasterQATestCase__, self).setUp(masterqa_mode=True)
        self.manual_check_setup()
        if self.headless:
            self.auto_close_results_page = True
        if START_IN_FULL_SCREEN_MODE:
            self.maximize_window()

    def verify(self, *args):
        warn_msg = "\nWARNING: MasterQA skips manual checks in headless mode!"
        self.check_count += 1
        if self.headless:
            if self.check_count == 1:
                print(warn_msg)
            return
        # This is where the magic happens
        self.manual_page_check(*args)

    def auto_close_results(self):
        ''' If this method is called, the results page will automatically close
        at the end of the test run, rather than waiting on the user to close
        the results page manually.
        '''
        self.auto_close_results_page = True

    def tearDown(self):
        if self.headless and self.check_count > 0:
            print("WARNING: %s manual checks were skipped!" % self.check_count)
        if sys.exc_info()[1]:
            self.add_failure(sys.exc_info()[1])
        self.process_manual_check_results(self.auto_close_results_page)
        super(__MasterQATestCase__, self).tearDown()
