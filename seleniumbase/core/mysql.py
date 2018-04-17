"""
Wrapper for MySQL DB functions to make life easier.
"""

import time
from seleniumbase.core import mysql_conf as conf


class DatabaseManager():
    """
    This class wraps MySQL database methods for easy use.
    """

    def __init__(self, database_env='test', conf_creds=None):
        """
        Gets database information from mysql_conf.py and creates a connection.
        """
        import MySQLdb
        db_server, db_user, db_pass, db_schema = \
            conf.APP_CREDS[conf.Apps.TESTCASE_REPOSITORY][database_env]
        retry_count = 3
        backoff = 1.2  # Time to wait (in seconds) between retries.
        count = 0
        while count < retry_count:
            try:
                self.conn = MySQLdb.connect(host=db_server,
                                            user=db_user,
                                            passwd=db_pass,
                                            db=db_schema)
                self.conn.autocommit(True)
                self.cursor = self.conn.cursor()
                return
            except Exception:
                time.sleep(backoff)
                count = count + 1
        if retry_count == 3:
            raise Exception("Unable to connect to Database after 3 retries.")

    def query_fetch_all(self, query, values):
        """
        Executes a db query, gets all the values, and closes the connection.
        """
        self.cursor.execute(query, values)
        retval = self.cursor.fetchall()
        self.__close_db()
        return retval

    def query_fetch_one(self, query, values):
        """
        Executes a db query, gets the first value, and closes the connection.
        """
        self.cursor.execute(query, values)
        retval = self.cursor.fetchone()
        self.__close_db()
        return retval

    def execute_query(self, query, values):
        """
        Executes a query to the test_db and closes the connection afterwards.
        """
        retval = self.cursor.execute(query, values)
        self.__close_db()
        return retval

    def __close_db(self):
        self.cursor.close()
        self.conn.close()
