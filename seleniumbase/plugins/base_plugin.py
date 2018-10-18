"""
This is the Nose plugin for saving logs and setting a test environment.
Vars include "env" and "log_path".
You can have tests behave differently based on the environment.
You can access the values of these variables from the tests.
"""

import os
import sys
import time
from nose.plugins import Plugin
from nose.exc import SkipTest
from seleniumbase.core import log_helper
from seleniumbase.core import report_helper
from seleniumbase.fixtures import constants, errors


class Base(Plugin):
    """
    The base_plugin includes the following variables for nosetest runs:
    self.env -- The environment for the tests to use (Usage: --env=ENV)
    self.data -- Any extra data to pass to the tests (Usage: --data=DATA)
    self.log_path -- The directory where log files get saved to
                     (Usage: --log_path=LOG_PATH)
    self.report -- The option to create a fancy report after tests complete
                   (Usage: --report)
    self.show_report -- If self.report is turned on, then the report will
                        display immediately after tests complete their run.
                        Only use this when running tests locally, as this will
                        pause the test run until the report window is closed.
                        (Usage: --show_report)
    """
    name = 'testing_base'  # Usage: --with-testing_base

    def options(self, parser, env):
        super(Base, self).options(parser, env=env)
        parser.add_option(
            '--env', action='store',
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
            '--data', dest='data',
            default=None,
            help='Extra data to pass from the command line.')
        parser.add_option(
            '--log_path', dest='log_path',
            default='latest_logs/',
            help='Where the log files are saved.')
        parser.add_option(
            '--report', action="store_true", dest='report',
            default=False,
            help='Create a fancy report at the end of the test suite.')
        parser.add_option(
            '--show_report', action="store_true",
            dest='show_report',
            default=False,
            help="If true when using report, will display it after tests run.")
        found_processes_arg = False
        for arg in sys.argv:
            if "--processes=" in arg:
                found_processes_arg = True
        if found_processes_arg:
            print("* WARNING: Don't use multi-threading with nosetests! *")
            parser.add_option(
                '--processes', dest='processes',
                default=0,
                help="WARNING: Don't use multi-threading with nosetests!")

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
        log_path = options.log_path
        log_helper.log_folder_setup(log_path)
        if self.report_on:
            report_helper.clear_out_old_report_logs(archive_past_runs=False)

    def beforeTest(self, test):
        test_logpath = self.options.log_path + "/" + test.id()
        if not os.path.exists(test_logpath):
            os.makedirs(test_logpath)
        test.test.environment = self.options.environment
        test.test.env = self.options.environment  # Add a shortened version
        test.test.data = self.options.data
        test.test.args = self.options
        self.test_count += 1
        self.start_time = float(time.time())

    def finalize(self, result):
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
        if ((not self.options.enable_plugin_basic_test_info) and
                (not self.options.enable_plugin_screen_shots) and
                (not self.options.enable_plugin_page_source)):
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
        if (err[0] == errors.BlockedTest or
                err[0] == errors.SkipTest or
                err[0] == errors.DeprecatedTest):
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
