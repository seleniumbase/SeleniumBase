# -*- coding: utf-8 -*-
""" This is the Nosetest plugin for setting base configuration and logging. """

import sys
import time
from nose.plugins import Plugin
from nose.exc import SkipTest
from seleniumbase.core import log_helper
from seleniumbase.core import report_helper
from seleniumbase.fixtures import constants, errors


class Base(Plugin):
    """
    This plugin adds the following command-line options to nosetests:
    --env=ENV  (Set the test env. Access with "self.env" in tests.)
    --data=DATA  (Extra test data. Access with "self.data" in tests.)
    --var1=DATA  (Extra test data. Access with "self.var1" in tests.)
    --var2=DATA  (Extra test data. Access with "self.var2" in tests.)
    --var3=DATA  (Extra test data. Access with "self.var3" in tests.)
    --settings-file=FILE  (Override default SeleniumBase settings.)
    --archive-logs  (Archive old log files instead of deleting them.)
    --report  (Create a fancy nosetests report after tests complete.)
    --show-report   If self.report is turned on, then the report will
                    display immediately after tests complete their run.
                    Only use this when running tests locally, as this will
                    pause the test run until the report window is closed.
    """
    name = 'testing_base'  # Usage: --with-testing_base  (Enabled by default)

    def options(self, parser, env):
        super(Base, self).options(parser, env=env)
        parser.add_option(
            '--env',
            action='store',
            dest='environment',
            choices=(
                constants.Environment.QA,
                constants.Environment.STAGING,
                constants.Environment.DEVELOP,
                constants.Environment.PRODUCTION,
                constants.Environment.MASTER,
                constants.Environment.LOCAL,
                constants.Environment.TEST),
            default=constants.Environment.TEST,
            help="The environment to run the tests in.")
        parser.add_option(
            '--data',
            dest='data',
            default=None,
            help='Extra data to pass to tests from the command line.')
        parser.add_option(
            '--var1',
            dest='var1',
            default=None,
            help='Extra data to pass to tests from the command line.')
        parser.add_option(
            '--var2',
            dest='var2',
            default=None,
            help='Extra data to pass to tests from the command line.')
        parser.add_option(
            '--var3',
            dest='var3',
            default=None,
            help='Extra data to pass to tests from the command line.')
        parser.add_option(
            '--settings_file', '--settings-file', '--settings',
            action='store',
            dest='settings_file',
            default=None,
            help="""The file that stores key/value pairs for overriding
                    values in the SeleniumBase settings.py file.""")
        parser.add_option(
            '--log_path', '--log-path',
            dest='log_path',
            default='latest_logs/',
            help="""(DEPRECATED) - This field is NOT EDITABLE anymore.
                    Log files are saved to the "latest_logs/" folder.""")
        parser.add_option(
            '--archive_logs', '--archive-logs',
            action="store_true",
            dest='archive_logs',
            default=False,
            help="Archive old log files instead of deleting them.")
        parser.add_option(
            '--report',
            action="store_true",
            dest='report',
            default=False,
            help='Create a fancy report at the end of the test suite.')
        parser.add_option(
            '--show_report', '--show-report',
            action="store_true",
            dest='show_report',
            default=False,
            help="If true when using report, will display it after tests run.")
        found_processes_arg = False
        found_timeout_arg = False
        for arg in sys.argv:
            if "--processes=" in arg:
                found_processes_arg = True
            if "--timeout=" in arg:
                found_timeout_arg = True
        if found_processes_arg:
            print("* WARNING: Don't use multi-threading with nosetests! *")
            parser.add_option(
                '--processes',
                dest='processes',
                default=0,
                help="WARNING: Don't use multi-threading with nosetests!")
        if found_timeout_arg:
            print("\n  WARNING: Don't use --timeout=s from pytest-timeout!")
            print("  It's not thread-safe for WebDriver processes!")
            print("  Use --time-limit=s from SeleniumBase instead!\n")
            parser.add_option(
                '--timeout',
                dest='timeout',
                default=0,
                help="Don't use --timeout=s! Use --time-limit=s instead!")

    def configure(self, options, conf):
        super(Base, self).configure(options, conf)
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
        log_path = 'latest_logs/'
        archive_logs = options.archive_logs
        log_helper.log_folder_setup(log_path, archive_logs)
        if self.report_on:
            report_helper.clear_out_old_report_logs(archive_past_runs=False)

    def beforeTest(self, test):
        test.test.environment = self.options.environment
        test.test.env = self.options.environment  # Add a shortened version
        test.test.data = self.options.data
        test.test.var1 = self.options.var1
        test.test.var2 = self.options.var2
        test.test.var3 = self.options.var3
        test.test.settings_file = self.options.settings_file
        test.test.log_path = self.options.log_path
        test.test.args = self.options
        test.test.report_on = self.report_on
        self.test_count += 1
        self.start_time = float(time.time())

    def finalize(self, result):
        log_helper.archive_logs_if_set(
            self.options.log_path, self.options.archive_logs)
        if self.report_on:
            if not self.import_error:
                report_helper.add_bad_page_log_file(self.page_results_list)
                report_log_path = report_helper.archive_new_report_logs()
                report_helper.build_report(
                    report_log_path,
                    self.page_results_list,
                    self.successes, self.failures,
                    self.options.browser,
                    self.show_report)

    def __log_all_options_if_none_specified(self, test):
        """
        When testing_base is specified, but none of the log options to save are
        specified (basic_test_info, screen_shots, page_source), then save them
        all by default. Otherwise, save only selected ones from their plugins.
        """
        if ((not self.options.enable_plugin_basic_test_info) and (
                not self.options.enable_plugin_screen_shots) and (
                not self.options.enable_plugin_page_source)):
            test_logpath = self.options.log_path + "/" + test.id()
            log_helper.log_screenshot(test_logpath, test.driver)
            log_helper.log_test_failure_data(
                test, test_logpath, test.driver, test.browser)
            log_helper.log_page_source(test_logpath, test.driver)

    def addSuccess(self, test, capt):
        if self.report_on:
            self.duration = str(
                "%0.3fs" % (float(time.time()) - float(self.start_time)))
            self.successes.append(test.id())
            self.page_results_list.append(
                report_helper.process_successes(
                    test, self.test_count, self.duration))

    def add_fails_or_errors(self, test):
        if self.report_on:
            self.duration = str(
                "%0.3fs" % (float(time.time()) - float(self.start_time)))
            if test.id() == 'nose.failure.Failure.runTest':
                print(">>> ERROR: Could not locate tests to run!")
                print(">>> The Test Report WILL NOT be generated!")
                self.import_error = True
                return
            self.failures.append(test.id())
            br = self.options.browser
            self.page_results_list.append(
                report_helper.process_failures(
                    test, self.test_count, br, self.duration))

    def addFailure(self, test, err, capt=None, tbinfo=None):
        # self.__log_all_options_if_none_specified(test)
        self.add_fails_or_errors(test)

    def addError(self, test, err, capt=None):
        """
        Since Skip, Blocked, and Deprecated are all technically errors, but not
        error states, we want to make sure that they don't show up in
        the nose output as errors.
        """
        if (err[0] == errors.BlockedTest or (
                err[0] == errors.SkipTest) or (
                err[0] == errors.DeprecatedTest)):
            print(err[1].__str__().split('''-------------------- >> '''
                                         '''begin captured logging'''
                                         ''' << --------------------''', 1)[0])
        else:
            # self.__log_all_options_if_none_specified(test)
            pass
        self.add_fails_or_errors(test)

    def handleError(self, test, err, capt=None):
        """
        If the database plugin is not present, we have to handle capturing
        "errors" that shouldn't be reported as such in base.
        """
        if not hasattr(test.test, "testcase_guid"):
            if err[0] == errors.BlockedTest:
                raise SkipTest(err[1])
                return True

            elif err[0] == errors.DeprecatedTest:
                raise SkipTest(err[1])
                return True

            elif err[0] == errors.SkipTest:
                raise SkipTest(err[1])
                return True
