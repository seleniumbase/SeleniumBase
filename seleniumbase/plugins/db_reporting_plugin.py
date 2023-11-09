"""DB Reporting Plugin for SeleniumBase tests that use pynose / nosetests"""
import time
import uuid
from nose.plugins import Plugin
from seleniumbase.fixtures import constants


class DBReporting(Plugin):
    """This plugin records test results in the Testcase Database."""
    name = "db_reporting"  # Usage: --with-db_reporting

    def __init__(self):
        Plugin.__init__(self)
        self.execution_guid = str(uuid.uuid4())
        self.testcase_guid = None
        self.execution_start_time = 0
        self.case_start_time = 0
        self.testcase_manager = None
        self._result_set = False
        self._test = None

    def options(self, parser, env):
        super().options(parser, env=env)
        parser.add_option(
            "--database_env",
            "--database-env",
            action="store",
            dest="database_env",
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
            help="The database environment to run the tests in.",
        )

    def configure(self, options, conf):
        from seleniumbase.core.testcase_manager import TestcaseManager

        super().configure(options, conf)
        self.options = options
        self.testcase_manager = TestcaseManager(self.options.database_env)

    def begin(self):
        """At the start of the run, we want to record the test
        execution information in the database."""
        import getpass
        from seleniumbase.core.testcase_manager import ExecutionQueryPayload

        exec_payload = ExecutionQueryPayload()
        exec_payload.execution_start_time = int(time.time() * 1000)
        self.execution_start_time = exec_payload.execution_start_time
        exec_payload.guid = self.execution_guid
        exec_payload.username = getpass.getuser()
        self.testcase_manager.insert_execution_data(exec_payload)

    def startTest(self, test):
        """At the start of the test, set testcase details."""
        from seleniumbase.core.application_manager import ApplicationManager
        from seleniumbase.core.testcase_manager import TestcaseDataPayload

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
        data_payload.env = application.split(".")[0]
        data_payload.start_time = application.split(".")[1]
        data_payload.state = constants.State.UNTESTED
        self.testcase_manager.insert_testcase_data(data_payload)
        self.case_start_time = int(time.time() * 1000)
        # Make the testcase guid available to other plugins
        test.testcase_guid = self.testcase_guid
        self._test = test
        self._test._nose_skip_reason = None

    def finalize(self, result):
        """At the end of the test run, we want to
        update the DB row with the total execution time."""
        runtime = int(time.time() * 1000) - self.execution_start_time
        self.testcase_manager.update_execution_data(
            self.execution_guid, runtime
        )

    def afterTest(self, test):
        if not self._result_set:
            err = None
            try:
                err = self._test._nose_skip_reason
                if err:
                    err = "Skipped:   " + str(err)
                    err = (err, err)
            except Exception:
                pass
            if not err:
                err = "Skipped:   (no reason given)"
                err = (err, err)
            self.__insert_test_result(constants.State.SKIPPED, self._test, err)

    def addSuccess(self, test, capt):
        """After each test success, record testcase run information."""
        self.__insert_test_result(constants.State.PASSED, test)
        self._result_set = True

    def addFailure(self, test, err, capt=None, tbinfo=None):
        """After each test failure, record testcase run information."""
        self.__insert_test_result(constants.State.FAILED, test, err)
        self._result_set = True

    def addError(self, test, err, capt=None):
        """After each test error, record testcase run information.
        (Test errors should be treated the same as test failures.)"""
        self.__insert_test_result(constants.State.FAILED, test, err)
        self._result_set = True

    def handleError(self, test, err, capt=None):
        """After each test error, record testcase run information.
        "Error" also encompasses any states other than Pass or Fail."""
        from nose.exc import SkipTest
        from seleniumbase.fixtures import errors

        if err[0] == errors.BlockedTest:
            self.__insert_test_result(constants.State.BLOCKED, test, err)
            self._result_set = True
            raise SkipTest(err[1])
        elif err[0] == errors.DeprecatedTest:
            self.__insert_test_result(constants.State.DEPRECATED, test, err)
            self._result_set = True
            raise SkipTest(err[1])
        elif err[0] == errors.SkipTest:
            self.__insert_test_result(constants.State.SKIPPED, test, err)
            self._result_set = True
            raise SkipTest(err[1])

    def __insert_test_result(self, state, test, err=None):
        from seleniumbase.core.testcase_manager import TestcaseDataPayload

        data_payload = TestcaseDataPayload()
        data_payload.runtime = int(time.time() * 1000) - self.case_start_time
        data_payload.guid = self.testcase_guid
        data_payload.execution_guid = self.execution_guid
        data_payload.state = state
        if err is not None:
            data_payload.message = (
                err[1]
                .__str__()
                .split(
                    """-------------------- >> """
                    """begin captured logging"""
                    """ << --------------------""",
                    1,
                )[0]
            )
        self.testcase_manager.update_testcase_data(data_payload)
