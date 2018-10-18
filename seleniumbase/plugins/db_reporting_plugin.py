"""
This plugin is for recording test results in the Testcase Database.
"""

import getpass
import time
import uuid
from optparse import SUPPRESS_HELP
from nose.plugins import Plugin
from nose.exc import SkipTest
from seleniumbase.core.application_manager import ApplicationManager
from seleniumbase.core.testcase_manager import ExecutionQueryPayload
from seleniumbase.core.testcase_manager import TestcaseDataPayload
from seleniumbase.core.testcase_manager import TestcaseManager
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import errors


class DBReporting(Plugin):
    """
    This plugin records test results in the Testcase Database.
    """
    name = 'db_reporting'  # Usage: --with-db_reporting

    def __init__(self):
        Plugin.__init__(self)
        self.execution_guid = str(uuid.uuid4())
        self.testcase_guid = None
        self.execution_start_time = 0
        self.case_start_time = 0
        self.application = None
        self.testcase_manager = None
        self.error_handled = False

    def options(self, parser, env):
        super(DBReporting, self).options(parser, env=env)
        parser.add_option('--database_environment', action='store',
                          dest='database_env',
                          choices=('production', 'qa', 'staging', 'develop',
                                   'test', 'local', 'master'),
                          default='test',
                          help=SUPPRESS_HELP)

    def configure(self, options, conf):
        super(DBReporting, self).configure(options, conf)
        self.options = options
        self.testcase_manager = TestcaseManager(self.options.database_env)

    def begin(self):
        """ At the start of the run, we want to record the test
            execution information in the database. """
        exec_payload = ExecutionQueryPayload()
        exec_payload.execution_start_time = int(time.time() * 1000)
        self.execution_start_time = exec_payload.execution_start_time
        exec_payload.guid = self.execution_guid
        exec_payload.username = getpass.getuser()
        self.testcase_manager.insert_execution_data(exec_payload)

    def startTest(self, test):
        """ At the start of the test, set the testcase details. """
        data_payload = TestcaseDataPayload()
        self.testcase_guid = str(uuid.uuid4())
        data_payload.guid = self.testcase_guid
        data_payload.execution_guid = self.execution_guid
        if hasattr(test, "browser"):
            data_payload.browser = test.browser
        else:
            data_payload.browser = "N/A"
        data_payload.test_address = test.id()
        application = ApplicationManager.generate_application_string(test)
        data_payload.env = application.split('.')[0]
        data_payload.start_time = application.split('.')[1]
        data_payload.state = constants.State.NOTRUN
        self.testcase_manager.insert_testcase_data(data_payload)
        self.case_start_time = int(time.time() * 1000)
        # Make the testcase guid available to other plugins
        test.testcase_guid = self.testcase_guid

    def finalize(self, result):
        """ At the end of the run, we want to
        update the DB row with the execution time. """
        runtime = int(time.time() * 1000) - self.execution_start_time
        self.testcase_manager.update_execution_data(self.execution_guid,
                                                    runtime)

    def addSuccess(self, test, capt):
        """
        After test completion, we want to record testcase run information.
        """
        self.__insert_test_result(constants.State.PASS, test)

    def addError(self, test, err, capt=None):
        """
        After a test error, we want to record testcase run information.
        """
        self.__insert_test_result(constants.State.ERROR, test, err)

    def handleError(self, test, err, capt=None):
        """
        After a test error, we want to record testcase run information.
        "Error" also encompasses any states other than Pass or Fail, so we
        check for those first.
        """
        if err[0] == errors.BlockedTest:
            self.__insert_test_result(constants.State.BLOCKED, test, err)
            self.error_handled = True
            raise SkipTest(err[1])
            return True

        elif err[0] == errors.DeprecatedTest:
            self.__insert_test_result(constants.State.DEPRECATED, test, err)
            self.error_handled = True
            raise SkipTest(err[1])
            return True

        elif err[0] == errors.SkipTest:
            self.__insert_test_result(constants.State.SKIP, test, err)
            self.error_handled = True
            raise SkipTest(err[1])
            return True

    def addFailure(self, test, err, capt=None, tbinfo=None):
        """
        After a test failure, we want to record testcase run information.
        """
        self.__insert_test_result(constants.State.FAILURE, test, err)

    def __insert_test_result(self, state, test, err=None):
        data_payload = TestcaseDataPayload()
        data_payload.runtime = int(time.time() * 1000) - self.case_start_time
        data_payload.guid = self.testcase_guid
        data_payload.execution_guid = self.execution_guid
        data_payload.state = state
        if err is not None:
            data_payload.message = err[1].__str__().split(
                '''-------------------- >> '''
                '''begin captured logging'''
                ''' << --------------------''', 1)[0]
        self.testcase_manager.update_testcase_data(data_payload)
