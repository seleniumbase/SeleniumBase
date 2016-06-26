"""
This plugin is for saving logs and setting a test environment.
Vars include "env" and "log_path".
You can have tests behave differently based on the environment.
You can access the values of these variables from the tests.
"""

import os
import shutil
import time
from nose.plugins import Plugin
from nose.exc import SkipTest
from seleniumbase.config import settings
from seleniumbase.core import log_helper
from seleniumbase.core import report_helper
from seleniumbase.fixtures import constants, errors


class Base(Plugin):
    """
    The base_plugin includes the following variables:
    self.options.env -- the environment for the tests to use (--env=ENV)
    self.options.data -- any extra data to pass to the tests (--data=DATA)
    self.options.log_path -- the directory in which the log files
                            are saved (--log_path=LOG_PATH)
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
            '--hide_report', action="store_true",
            dest='hide_report',
            default=False,
            help="If true while using report, it won't pop up after tests run")

    def configure(self, options, conf):
        super(Base, self).configure(options, conf)
        if not self.enabled:
            return
        self.options = options
        log_path = options.log_path
        self.report_on = options.report
        self.hide_report = options.hide_report
        if log_path.endswith("/"):
            log_path = log_path[:-1]
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        else:
            archived_folder = "%s/../archived_logs/" % log_path
            if not os.path.exists(archived_folder):
                os.makedirs(archived_folder)
            archived_logs = "%slogs_%s" % (archived_folder, int(time.time()))
            shutil.move(log_path, archived_logs)
            os.makedirs(log_path)
            if not settings.ARCHIVE_EXISTING_LOGS:
                shutil.rmtree(archived_logs)
        self.successes = []
        self.failures = []
        self.duration = float(0)
        self.page_results_list = []
        self.test_count = 0
        self.import_error = False
        if self.report_on:
            report_helper.clear_out_old_report_logs(archive_past_runs=False)

    def beforeTest(self, test):
        test_logpath = self.options.log_path + "/" + test.id()
        if not os.path.exists(test_logpath):
            os.makedirs(test_logpath)
        test.test.environment = self.options.environment
        test.test.data = self.options.data
        test.test.args = self.options
        self.test_count += 1
        self.duration = float(time.time())

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
                    self.hide_report)

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
                test_logpath, test.driver, test.browser)
            log_helper.log_page_source(test_logpath, test.driver)

    def addSuccess(self, test, capt):
        if self.report_on:
            self.duration = str(
                "%0.3fs" % (float(time.time()) - float(self.duration)))
            self.successes.append(test.id())
            self.page_results_list.append(
                report_helper.process_successes(
                    test, self.test_count, self.duration))

    def add_fails_or_errors(self, test):
        if self.report_on:
            self.duration = str(
                "%0.3fs" % (float(time.time()) - float(self.duration)))
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
        self.__log_all_options_if_none_specified(test)
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
            self.__log_all_options_if_none_specified(test)
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
