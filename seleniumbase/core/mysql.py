"""
Wrapper for MySQL functions to make life easier
Due to compatibility issues, might only work for Python 2.7 right now
"""

import time


class DatabaseManager():
    """
    This class wraps database functions for easy use.
    It connects to the testcase database.
    """

    def __init__(self, database_env='test', conf_creds=None):
        """
        Gets database information from mysql_conf.py and creates a connection.
        """
        import mysql_conf as conf  # This had problems when using Python 3
        import MySQLdb
        db_server, db_user, db_pass, db_schema = \
            conf.APP_CREDS[conf.Apps.TESTCASE_REPOSITORY][database_env]
        retry_count = 3
        backoff = 1.2  # Time to wait (in seconds) between retries
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

    def fetchall_query_and_close(self, query, values):
        """
        Executes a query, gets all the values and then closes up the connection
        """
        self.cursor.execute(query, values)
        retval = self.cursor.fetchall()
        self.__close_db()
        return retval

    def fetchone_query_and_close(self, query, values):
        """
        Executes a query, gets the first value, and closes up the connection
        """
        self.cursor.execute(query, values)
        retval = self.cursor.fetchone()
        self.__close_db()
        return retval

    def execute_query_and_close(self, query, values):
        """
        Executes a query and closes the connection
        """
        retval = self.cursor.execute(query, values)
        self.__close_db()
        return retval

    def __close_db(self):
        self.cursor.close()
        self.conn.close()
