import json
import logging
import time
import uuid
from seleniumbase.core.mysql import DatabaseManager

DEFAULT_EXPIRATION = 1000 * 60 * 60 * 48


class DelayedTestStorage:
    """ The database-calling methods of the Delayed Test Framework """

    @classmethod
    def get_delayed_test_data(self, testcase_address, done=0):
        """ This method queries the delayedTestData table in the DB and
            then returns a list of rows with the matching parameters.
            :param testcase_address: The ID (address) of the test case.
            :param done: (0 for test not done or 1 for test done)
            :returns: A list of rows found with the matching testcase_address.
        """
        db = DatabaseManager()
        query = """SELECT guid,testcaseAddress,insertedAt,expectedResult,done
                   FROM delayedTestData
                   WHERE testcaseAddress=%(testcase_address)s
                   AND done=%(done)s"""
        data = db.fetchall_query_and_close(
            query, {"testcase_address": testcase_address,
                    "done": done})
        if data:
            return data
        else:
            logging.debug("Could not find any rows in delayedTestData.")
            logging.debug("DB Query = " + query %
                          {"testcase_address": testcase_address, "done": done})
            return []

    @classmethod
    def insert_delayed_test_data(self, guid_, testcase_address,
                                 expected_result, done=0,
                                 expires_at=DEFAULT_EXPIRATION):
        """ This method inserts rows into the delayedTestData table
            in the DB based on the given parameters where
            inserted_at (Date format) is automatically set in this method.
            :param guid_: The guid that is provided by the test case.
            (Format: str(uuid.uuid4()))
            :param testcase_address: The ID (address) of the test case.
            :param expected_result: The result string of persistent data
            that will be stored in the DB.
            :param done: (0 for test not done or 1 for test done)
            :returns: True (when no exceptions or errors occur)
        """
        inserted_at = int(time.time() * 1000)

        db = DatabaseManager()
        query = """INSERT INTO delayedTestData(
                   guid,testcaseAddress,insertedAt,
                   expectedResult,done,expiresAt)
                   VALUES (%(guid)s,%(testcaseAddress)s,%(inserted_at)s,
                           %(expected_result)s,%(done)s,%(expires_at)s)"""

        db.execute_query_and_close(
            query, {"guid": guid_,
                    "testcaseAddress": testcase_address,
                    "inserted_at": inserted_at,
                    "expected_result": expected_result,
                    "done": done,
                    "expires_at": inserted_at + expires_at})
        return True

    @classmethod
    def set_delayed_test_to_done(self, guid_):
        """ This method updates the delayedTestData table in the DB
            to set the test with the selected guid to done.
            :param guid_: The guid that is provided by the test case.
            (Format: str(uuid.uuid4()))
            :returns: True (when no exceptions or errors occur)
        """
        db = DatabaseManager()
        query = """UPDATE delayedTestData
                   SET done=TRUE
                   WHERE guid=%(guid)s
                   AND done=FALSE"""
        db.execute_query_and_close(query, {"guid": guid_})
        return True


class DelayedTestAssistant:
    """ Some methods for assisting tests (that don't call the DB directly) """

    @classmethod
    def get_delayed_results(self, test_id, seconds, set_done=True):
        """
        This method gets the delayed_test_data and sets the applicable rows
        in the DB to done.
        The results is a list of dicts where each list item contains
        item[0] = guid
        item[1] = testcaseAddress
        item[2] = seconds from epoch
        item[3] = expected results dict encoded in json
        :param test_id: the self.id() of the test
        :param seconds: the wait period until the data can be checked
        :returns: the results for a specific test where enough time has passed
        """
        delayed_test_data = DelayedTestStorage.get_delayed_test_data(
            testcase_address=test_id)
        now = int(time.time() * 1000)
        results_to_check = []
        if delayed_test_data is None:
            return results_to_check
        for item in delayed_test_data:
            if item[2] < now - (seconds * 1000):
                results_to_check.append(item)
                if set_done:
                    DelayedTestStorage.set_delayed_test_to_done(item[0])
        return results_to_check

    @classmethod
    def store_delayed_data(self, test_id, expected_result_dict,
                           expires_at=DEFAULT_EXPIRATION):
        """
        Loads the dictionary of information into the delayed test database
        :param test_id: the self.id() of the test
        :param expected_result_dict: a dictionary of what's to be checked later
        """
        expected_result_json = json.JSONEncoder().encode(expected_result_dict)
        DelayedTestStorage.insert_delayed_test_data(str(uuid.uuid4()),
                                                    test_id,
                                                    expected_result_json,
                                                    0,
                                                    expires_at)

    @classmethod
    def set_test_done(self, test_guid):
        """ This method calls set_delayed_test_to_done to set a
            row in the db to done.
            :param test_guid: The guid that is provided by the test.
            (Format: str(uuid.uuid4()))
            :returns: True (when no exceptions or errors occur)
        """
        DelayedTestStorage.set_delayed_test_to_done(test_guid)
        return True
