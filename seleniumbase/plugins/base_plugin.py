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
            default='logs/',
            help='Where the log files are saved.')

    def configure(self, options, conf):
        super(Base, self).configure(options, conf)
        if not self.enabled:
            return
        self.options = options
        log_path = options.log_path
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

    def beforeTest(self, test):
        test_logpath = self.options.log_path + "/" + test.id()
        if not os.path.exists(test_logpath):
            os.makedirs(test_logpath)
        test.test.environment = self.options.environment
        test.test.data = self.options.data
        test.test.args = self.options

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

    def addFailure(self, test, err, capt=None):
        self.__log_all_options_if_none_specified(test)

    def addError(self, test, err, capt=None):
        """
        Since Skip, Blocked, and Deprecated are all technically errors, but not
        error states, we want to make sure that they don't show up in
        the nose output as errors.
        """
        if (err[0] == errors.BlockedTest or
                err[0] == errors.SkipTest or
                err[0] == errors.DeprecatedTest):
            print err[1].__str__().split('''-------------------- >> '''
                                         '''begin captured logging'''
                                         ''' << --------------------''', 1)[0]
        else:
            self.__log_all_options_if_none_specified(test)

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
