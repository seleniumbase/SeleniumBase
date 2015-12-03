"""
Testcase database related methods
"""

from seleniumbase.core.mysql import DatabaseManager


class TestcaseManager:
    """
    Helper for Testcase related DB stuff
    """

    def __init__(self, database_env):
        self.database_env = database_env

    def insert_execution_data(self, execution_query_payload):
        """ Inserts an execution into the database.
            Returns the execution guid. """

        query = """INSERT INTO execution
                   (guid, executionStart, totalExecutionTime, username)
                   VALUES (%(guid)s,%(execution_start_time)s,
                           %(total_execution_time)s,%(username)s)"""
        DatabaseManager(self.database_env).execute_query_and_close(
            query,
            execution_query_payload.get_params())
        return execution_query_payload.guid

    def update_execution_data(self, execution_guid, execution_time):
        """updates an existing execution in the database"""

        query = """UPDATE execution
                   SET totalExecutionTime=%(execution_time)s
                   WHERE guid=%(execution_guid)s """
        DatabaseManager(self.database_env).execute_query_and_close(
            query,
            {"execution_guid": execution_guid,
             "execution_time": execution_time})

    def insert_testcase_data(self, testcase_run_payload):
        """inserts all data for the test case, returns the new row guid"""

        query = """INSERT INTO testcaseRunData
                   (guid, browser, state, execution_guid, env, start_time,
                    testcaseAddress, runtime, retryCount, message, stackTrace)
                          VALUES (
                              %(guid)s,
                              %(browser)s,
                              %(state)s,
                              %(execution_guid)s,
                              %(env)s,
                              %(start_time)s,
                              %(testcaseAddress)s,
                              %(runtime)s,
                              %(retryCount)s,
                              %(message)s,
                              %(stackTrace)s) """
        DatabaseManager(self.database_env).execute_query_and_close(
            query, testcase_run_payload.get_params())

    def update_testcase_data(self, testcase_payload):
        """updates an existing testcase run in the database"""

        query = """UPDATE testcaseRunData SET
                          runtime=%(runtime)s,
                          state=%(state)s,
                          retryCount=%(retryCount)s,
                          stackTrace=%(stackTrace)s,
                          message=%(message)s
                          WHERE guid=%(guid)s """
        DatabaseManager(self.database_env).execute_query_and_close(
            query, testcase_payload.get_params())

    def update_testcase_log_url(self, testcase_payload):
        """updates an existing testcase run's logging URL in the database"""

        query = """UPDATE testcaseRunData
                   SET logURL=%(logURL)s
                   WHERE guid=%(guid)s """
        DatabaseManager(self.database_env).execute_query_and_close(
            query, testcase_payload.get_params())


class ExecutionQueryPayload:
    """ Helper class for containing the execution query data """
    def __init__(self):
        self.execution_start_time = None
        self.total_execution_time = -1
        self.username = "Default"
        self.guid = None

    def get_params(self):
        """ Returns a params object for use with the pool """
        return {
            "execution_start_time": self.execution_start_time,
            "total_execution_time": self.total_execution_time,
            "username": self.username,
            "guid": self.guid
            }


class TestcaseDataPayload:
    """ Helper class for containing all the testcase query data """
    def __init__(self):
        self.guid = None
        self.testcaseAddress = None
        self.browser = None
        self.state = None
        self.execution_guid = None
        self.env = None
        self.start_time = None
        self.runtime = None
        self.retry_count = 0
        self.stack_trace = None
        self.message = None
        self.logURL = None

    def get_params(self):
        """ Returns a params object for use with the pool """
        return {
            "guid": self.guid,
            "testcaseAddress": self.testcaseAddress,
            "browser": self.browser,
            "state": self.state,
            "execution_guid": self.execution_guid,
            "env": self.env,
            "start_time": self.start_time,
            "runtime": self.runtime,
            "retryCount": self.retry_count,
            "stackTrace": self.stack_trace,
            "message": self.message,
            "logURL": self.logURL
        }
