import json
import logging
import time
import uuid
from seleniumbase.core.mysql import DatabaseManager

DEFAULT_WAIT_TIME = 1000 * 60 * 60 * 24  # A day later (in milliseconds)


class DividedTestStorage:
    """
    When you need a large time delay between two parts of a test, you can break
    the test up into two tests, and use the divided_test_data table of the
    MySQL DB to hold onto important information until the second part of the
    divided test is ready to complete the remainder of the test.

    *** Example ***:
    You've created an email-marketing tool that sends out a follow-up email in
    exactly 24 hours. The first part of the test can schedule the follow-up
    email while the second part of the test verifies that the follow-up email
    was sent and received successfully after enough time has passed.
    """

    @classmethod
    def get_divided_test_data(self, test_address, is_done=0):
        """ This method queries the divided_test_data table in the test_db and
            then returns a list of rows with the matching parameters.
            :param test_address: The ID (address) of the test case.
            :param is_done: (0 for test not done or 1 for test done)
            :returns: A list of rows found with the matching test_address.
        """
        db = DatabaseManager()
        query = """SELECT guid,test_address,inserted_at,test_data,is_done
                   FROM divided_test_data
                   WHERE test_address=%(test_address)s
                   AND is_done=%(is_done)s"""
        data = db.query_fetch_all(
            query, {"test_address": test_address,
                    "is_done": is_done})
        if data:
            return data
        else:
            logging.debug("Could not find any rows in divided_test_data.")
            logging.debug("DB Query = " + query %
                          {"test_address": test_address, "is_done": is_done})
            return []

    @classmethod
    def insert_divided_test_data(self, guid_, test_address,
                                 test_data, is_done=0,
                                 wait_time=DEFAULT_WAIT_TIME):
        """ This method inserts rows into the divided_test_data table
            in the DB based on the given parameters where
            inserted_at (Date format) is automatically set in this method.
            :param guid_: The guid that is provided by the test case.
            (Format: str(uuid.uuid4()))
            :param test_address: The ID (address) of the test case.
            :param test_data: Additional data to store for the test.
            :param is_done: (0 for test not done or 1 for test done)
            :returns: True (when no exceptions or errors occur)
        """
        inserted_at = int(time.time() * 1000)

        db = DatabaseManager()
        query = """INSERT INTO divided_test_data(
                   guid,test_address,inserted_at,
                   test_data,is_done,wait_time)
                   VALUES (%(guid)s,%(test_address)s,%(inserted_at)s,
                           %(test_data)s,%(is_done)s,%(wait_time)s)"""

        db.execute_query(
            query, {"guid": guid_,
                    "test_address": test_address,
                    "inserted_at": inserted_at,
                    "test_data": test_data,
                    "is_done": is_done,
                    "wait_time": inserted_at + wait_time})
        return True

    @classmethod
    def set_divided_test_to_done(self, guid_):
        """ This method updates the divided_test_data table in the DB
            to set the test with the selected guid to done.
            :param guid_: The guid that is provided by the test case.
            (Format: str(uuid.uuid4()))
            :returns: True (when no exceptions or errors occur)
        """
        db = DatabaseManager()
        query = """UPDATE divided_test_data
                   SET is_done=TRUE
                   WHERE guid=%(guid)s
                   AND is_done=FALSE"""
        db.execute_query(query, {"guid": guid_})
        return True


class DividedTestAssistant:
    """ Some methods for assisting tests (that don't call the DB directly) """

    @classmethod
    def get_divided_test_results(self, test_id, seconds, set_done=True):
        """
        This method gets the divided_test data and sets the applicable rows
        in the DB to done.
        The results is a list of dicts where each list item contains
        item[0] = guid
        item[1] = test_address
        item[2] = time (in seconds from Epoch)
        item[3] = test data dict encoded in json
        :param test_id: the self.id() of the test
        :param seconds: the wait period until the data can be checked
        :returns: the results for a specific test where enough time has passed
        """
        divided_test_data = DividedTestStorage.get_divided_test_data(
            test_address=test_id)
        now = int(time.time() * 1000)
        results_to_check = []
        if divided_test_data is None:
            return results_to_check
        for item in divided_test_data:
            if item[2] < now - (seconds * 1000):
                results_to_check.append(item)
                if set_done:
                    DividedTestStorage.set_divided_test_to_done(item[0])
        return results_to_check

    @classmethod
    def store_divided_test_data(self, test_id, test_data_dict,
                                wait_time=DEFAULT_WAIT_TIME):
        """
        Loads the dictionary of information into the divided_test_data table
        :param test_id: the self.id() of the test
        :param test_data_dict: a dictionary of data to store for later
        """
        test_data_json = json.JSONEncoder().encode(test_data_dict)
        DividedTestStorage.insert_divided_test_data(str(uuid.uuid4()),
                                                    test_id,
                                                    test_data_json,
                                                    0,
                                                    wait_time)

    @classmethod
    def set_test_done(self, test_guid):
        """ This method calls set_divided_test_to_done to set a
            row in the db to done.
            :param test_guid: The guid that is provided by the test.
            (Format: str(uuid.uuid4()))
            :returns: True (when no exceptions or errors occur)
        """
        DividedTestStorage.set_divided_test_to_done(test_guid)
        return True
