"""Base Plugin for SeleniumBase tests that run with pynose / nosetests"""
import ast
import sys
import time
from nose.plugins import Plugin
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.core import download_helper
from seleniumbase.core import log_helper
from seleniumbase.core import report_helper
from seleniumbase.fixtures import constants

python3_11_or_newer = False
if sys.version_info >= (3, 11):
    python3_11_or_newer = True
py311_patch2 = constants.PatchPy311.PATCH = True


class Base(Plugin):
    """This plugin adds the following command-line options to pynose:
    --env=ENV  (Set the test env. Access with "self.env" in tests.)
    --account=STR  (Set account. Access with "self.account" in tests.)
    --data=STRING  (Extra test data. Access with "self.data" in tests.)
    --var1=STRING  (Extra test data. Access with "self.var1" in tests.)
    --var2=STRING  (Extra test data. Access with "self.var2" in tests.)
    --var3=STRING  (Extra test data. Access with "self.var3" in tests.)
    --variables=DICT  (Extra test data. Access with "self.variables".)
    --settings-file=FILE  (Override default SeleniumBase settings.)
    --ftrace | --final-trace  (Enter Debug Mode after any test ends.)
    --archive-logs  (Archive old log files instead of deleting them.)
    --archive-downloads  (Archive old downloads instead of deleting.)
    --report  (Create a fancy nosetests report after tests complete.)
    --show-report   If self.report is turned on, then the report will
                    display immediately after tests complete their run.
                    Only use this when running tests locally, as this will
                    pause the test run until the report window is closed.
    """
    name = "testing_base"  # Usage: --with-testing_base  (Enabled by default)

    def options(self, parser, env):
        super().options(parser, env=env)
        parser.addoption = parser.add_option  # Reuse name from pytest parser
        parser.addoption(
            "--env",
            action="store",
            dest="environment",
            choices=(
                constants.Environment.QA,
                constants.Environment.RC,
                constants.Environment.STAGING,
                constants.Environment.DEVELOP,
                constants.Environment.PRODUCTION,
                constants.Environment.PERFORMANCE,
                constants.Environment.REPLICA,
                constants.Environment.FEDRAMP,
                constants.Environment.OFFLINE,
                constants.Environment.ONLINE,
                constants.Environment.MASTER,
                constants.Environment.REMOTE,
                constants.Environment.LEGACY,
                constants.Environment.LOCAL,
                constants.Environment.ALPHA,
                constants.Environment.BETA,
                constants.Environment.DEMO,
                constants.Environment.GDPR,
                constants.Environment.MAIN,
                constants.Environment.TEST,
                constants.Environment.GOV,
                constants.Environment.NEW,
                constants.Environment.OLD,
                constants.Environment.UAT,
            ),
            default=constants.Environment.TEST,
            help="""This option sets a test env from a list of choices.
                    Access using "self.env" or "self.environment".""",
        )
        parser.addoption(
            "--account",
            dest="account",
            default=None,
            help="""This option sets a test account string.
                    In tests, use "self.account" to get the value.""",
        )
        parser.addoption(
            "--data",
            dest="data",
            default=None,
            help="Extra data to pass to tests from the command line.",
        )
        parser.addoption(
            "--var1",
            dest="var1",
            default=None,
            help="Extra data to pass to tests from the command line.",
        )
        parser.addoption(
            "--var2",
            dest="var2",
            default=None,
            help="Extra data to pass to tests from the command line.",
        )
        parser.addoption(
            "--var3",
            dest="var3",
            default=None,
            help="Extra data to pass to tests from the command line.",
        )
        parser.addoption(
            "--variables",
            dest="variables",
            default=None,
            help="""A var dict to pass to tests from the command line.
                    Example usage:
                    ----------------------------------------------
                    Option: --variables='{"special":123}'
                    Access: self.variables["special"]
                    ----------------------------------------------
                    Option: --variables='{"color":"red","num":42}'
                    Access: self.variables["color"]
                    Access: self.variables["num"]
                    ----------------------------------------------""",
        )
        parser.addoption(
            "--settings_file",
            "--settings-file",
            "--settings",
            action="store",
            dest="settings_file",
            default=None,
            help="""The file that stores key/value pairs for overriding
                    values in the SeleniumBase settings.py file.""",
        )
        parser.addoption(
            "--final-debug",
            "--final-trace",
            "--fdebug",
            "--ftrace",
            action="store_true",
            dest="final_debug",
            default=False,
            help="""Enter Debug Mode at the end of each test.
                    To enter Debug Mode only on failures, use "--pdb".
                    If using both "--final-debug" and "--pdb" together,
                    then Debug Mode will activate twice on failures.""",
        )
        parser.addoption(
            "--log_path",
            "--log-path",
            dest="log_path",
            default=constants.Logs.LATEST + "/",
            help="""(DEPRECATED) - This field is NOT EDITABLE anymore.
                    Log files are saved to the "latest_logs/" folder.""",
        )
        parser.addoption(
            "--archive_logs",
            "--archive-logs",
            action="store_true",
            dest="archive_logs",
            default=False,
            help="Archive old log files instead of deleting them.",
        )
        parser.addoption(
            "--archive_downloads",
            "--archive-downloads",
            action="store_true",
            dest="archive_downloads",
            default=False,
            help="Archive old downloads instead of deleting them.",
        )
        parser.addoption(
            "--report",
            action="store_true",
            dest="report",
            default=False,
            help="Create a fancy report at the end of the test suite.",
        )
        parser.addoption(
            "--show_report",
            "--show-report",
            action="store_true",
            dest="show_report",
            default=False,
            help="If true when using report, will display it after tests run.",
        )
        found_processes_arg = False
        for arg in sys.argv:
            if "--processes=" in arg or "--processes" in arg:
                found_processes_arg = True
        if found_processes_arg:
            print("* WARNING: Don't use multi-threading with nosetests! *")
            parser.addoption(
                "--processes",
                dest="processes",
                default=0,
                help="WARNING: Don't use multi-threading with nosetests!",
            )

    def configure(self, options, conf):
        super().configure(options, conf)
        self.enabled = True  # Used if test class inherits BaseCase
        self.options = options
        self.report_on = options.report
        self.show_report = options.show_report
        self.successes = []
        self.failures = []
        self.start_time = float(0)
        self.duration = float(0)
        self.page_results_list = []
        self.test_count = 0
        self.import_error = False
        log_path = constants.Logs.LATEST + "/"
        archive_logs = options.archive_logs
        log_helper.log_folder_setup(log_path, archive_logs)
        download_helper.reset_downloads_folder()
        sb_config.is_nosetest = True
        if self.report_on:
            report_helper.clear_out_old_report_logs(archive_past_runs=False)

    def beforeTest(self, test):
        sb_config._context_of_runner = False  # Context Manager Compatibility
        variables = self.options.variables
        if variables and isinstance(variables, str) and len(variables) > 0:
            bad_input = False
            if not variables.startswith("{") or not variables.endswith("}"):
                bad_input = True
            else:
                try:
                    variables = ast.literal_eval(variables)
                    if not isinstance(variables, dict):
                        bad_input = True
                except Exception:
                    bad_input = True
            if bad_input:
                raise Exception(
                    '\nExpecting a Python dictionary for "variables"!'
                    "\nEg. --variables=\"{'KEY1':'VALUE', 'KEY2':123}\""
                )
        else:
            variables = {}
        test.test.is_nosetest = True
        test.test.environment = self.options.environment
        test.test.env = self.options.environment  # Add a shortened version
        test.test.account = self.options.account
        test.test.data = self.options.data
        test.test.var1 = self.options.var1
        test.test.var2 = self.options.var2
        test.test.var3 = self.options.var3
        test.test.variables = variables  # Already verified is a dictionary
        test.test.settings_file = self.options.settings_file
        test.test._final_debug = self.options.final_debug
        test.test.log_path = self.options.log_path
        if self.options.archive_downloads:
            settings.ARCHIVE_EXISTING_DOWNLOADS = True
        test.test.args = self.options
        test.test.report_on = self.report_on
        self.test_count += 1
        self.start_time = float(time.time())

    def finalize(self, result):
        log_helper.archive_logs_if_set(
            self.options.log_path, self.options.archive_logs
        )
        log_helper.clear_empty_logs()
        if self.report_on:
            if not self.import_error:
                report_helper.add_bad_page_log_file(self.page_results_list)
                report_log_path = report_helper.archive_new_report_logs()
                report_helper.build_report(
                    report_log_path,
                    self.page_results_list,
                    self.successes,
                    self.failures,
                    self.options.browser,
                    self.show_report,
                )

    def addSuccess(self, test, capt):
        if self.report_on:
            self.duration = str(
                "%.2fs" % (float(time.time()) - float(self.start_time))
            )
            self.successes.append(test.id())
            self.page_results_list.append(
                report_helper.process_successes(
                    test, self.test_count, self.duration
                )
            )

    def add_fails_or_errors(self, test, err):
        if self.report_on:
            self.duration = str(
                "%.2fs" % (float(time.time()) - float(self.start_time))
            )
            if test.id() == "nose.failure.Failure.runTest":
                print(">>> ERROR: Could not locate tests to run!")
                print(">>> The Test Report WILL NOT be generated!")
                self.import_error = True
                return
            self.failures.append(test.id())
            self.page_results_list.append(
                report_helper.process_failures(
                    test, self.test_count, self.duration
                )
            )
        if python3_11_or_newer and py311_patch2:
            # Handle a bug on Python 3.11 where exceptions aren't seen
            sb_config._browser_version = None
            try:
                test._BaseCase__set_last_page_screenshot()
                test._BaseCase__set_last_page_url()
                test._BaseCase__set_last_page_source()
                sb_config._browser_version = test._get_browser_version()
                test._log_fail_data()
            except Exception:
                pass
            sb_config._excinfo_tb = err
            log_path = None
            if hasattr(sb_config, "_test_logpath"):
                log_path = sb_config._test_logpath
            if hasattr(sb_config, "_last_page_source"):
                source = sb_config._last_page_source
            if log_path and source:
                log_helper.log_page_source(log_path, None, source)
            last_page_screenshot_png = None
            if hasattr(sb_config, "_last_page_screenshot_png"):
                last_page_screenshot_png = sb_config._last_page_screenshot_png
            if log_path and last_page_screenshot_png:
                log_helper.log_screenshot(
                    log_path, None, last_page_screenshot_png
                )

    def addFailure(self, test, err, capt=None, tbinfo=None):
        self.add_fails_or_errors(test, err)

    def addError(self, test, err, capt=None):
        """Since Skip, Blocked, and Deprecated are all technically errors,
        but not error states, we want to make sure that they
        don't show up in the nose output as errors."""
        from seleniumbase.fixtures import errors

        if (
            err[0] == errors.BlockedTest
            or (err[0] == errors.SkipTest)
            or (err[0] == errors.DeprecatedTest)
        ):
            print(
                err[1]
                .__str__()
                .split(
                    """-------------------- >> """
                    """begin captured logging"""
                    """ << --------------------""",
                    1,
                )[0]
            )
        else:
            pass
        self.add_fails_or_errors(test, err)

    def handleError(self, test, err, capt=None):
        """After each test error, record testcase run information.
        "Error" also encompasses any states other than Pass or Fail."""
        from nose.exc import SkipTest
        from seleniumbase.fixtures import errors

        if not hasattr(test.test, "testcase_guid"):
            if err[0] == errors.BlockedTest:
                raise SkipTest(err[1])
            elif err[0] == errors.DeprecatedTest:
                raise SkipTest(err[1])
            elif err[0] == errors.SkipTest:
                raise SkipTest(err[1])
