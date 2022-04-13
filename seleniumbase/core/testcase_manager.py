from seleniumbase.core.mysql import DatabaseManager


class TestcaseManager:
    def __init__(self, database_env):
        self.database_env = database_env

    def insert_execution_data(self, execution_query_payload):
        """Inserts a test execution row into the database.
        Returns the execution guid.
        "execution_start_time" is defined by milliseconds since the Epoch.
        (See https://currentmillis.com to convert that to a real date.)"""

        query = """INSERT INTO test_execution
                   (guid, execution_start, total_execution_time, username)
                   VALUES (%(guid)s,%(execution_start_time)s,
                           %(total_execution_time)s,%(username)s)"""
        DatabaseManager(self.database_env).execute_query(
            query, execution_query_payload.get_params()
        )
        return execution_query_payload.guid

    def update_execution_data(self, execution_guid, execution_time):
        """Updates an existing test execution row in the database."""
        query = """UPDATE test_execution
                   SET total_execution_time=%(execution_time)s
                   WHERE guid=%(execution_guid)s """
        DatabaseManager(self.database_env).execute_query(
            query,
            {
                "execution_guid": execution_guid,
                "execution_time": execution_time,
            },
        )

    def insert_testcase_data(self, testcase_run_payload):
        """Inserts all data for the test in the DB. Returns new row guid."""
        query = """INSERT INTO test_run_data(
                   guid, browser, state, execution_guid, env, start_time,
                   test_address, runtime, retry_count, message, stack_trace)
                          VALUES (
                              %(guid)s,
                              %(browser)s,
                              %(state)s,
                              %(execution_guid)s,
                              %(env)s,
                              %(start_time)s,
                              %(test_address)s,
                              %(runtime)s,
                              %(retry_count)s,
                              %(message)s,
                              %(stack_trace)s) """
        DatabaseManager(self.database_env).execute_query(
            query, testcase_run_payload.get_params()
        )

    def update_testcase_data(self, testcase_payload):
        """Updates an existing test run in the database."""
        query = """UPDATE test_run_data SET
                            runtime=%(runtime)s,
                            state=%(state)s,
                            retry_count=%(retry_count)s,
                            stack_trace=%(stack_trace)s,
                            message=%(message)s
                            WHERE guid=%(guid)s """
        DatabaseManager(self.database_env).execute_query(
            query, testcase_payload.get_params()
        )

    def update_testcase_log_url(self, testcase_payload):
        query = """UPDATE test_run_data
                   SET log_url=%(log_url)s
                   WHERE guid=%(guid)s """
        DatabaseManager(self.database_env).execute_query(
            query, testcase_payload.get_params()
        )


class ExecutionQueryPayload:
    def __init__(self):
        self.execution_start_time = None
        self.total_execution_time = -1
        self.username = "Default"
        self.guid = None

    def get_params(self):
        return {
            "execution_start_time": self.execution_start_time,
            "total_execution_time": self.total_execution_time,
            "username": self.username,
            "guid": self.guid,
        }


class TestcaseDataPayload:
    def __init__(self):
        self.guid = None
        self.test_address = None
        self.browser = None
        self.state = None
        self.execution_guid = None
        self.env = None
        self.start_time = None
        self.runtime = None
        self.retry_count = 0
        self.stack_trace = None
        self.message = None
        self.log_url = None

    def get_params(self):
        return {
            "guid": self.guid,
            "test_address": self.test_address,
            "browser": self.browser,
            "state": self.state,
            "execution_guid": self.execution_guid,
            "env": self.env,
            "start_time": self.start_time,
            "runtime": self.runtime,
            "retry_count": self.retry_count,
            "stack_trace": self.stack_trace,
            "message": self.message,
            "log_url": self.log_url,
        }
