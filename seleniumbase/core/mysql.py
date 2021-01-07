"""
Wrapper for MySQL DB functions to make life easier.
"""

import sys
import time
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.core import settings_parser


class DatabaseManager():
    """
    This class wraps MySQL database methods for easy use.
    """

    def __init__(self, database_env='test', conf_creds=None):
        """
        Create a connection to the MySQL DB.
        """
        import pymysql
        db_server = settings.DB_HOST
        db_port = settings.DB_PORT
        db_user = settings.DB_USERNAME
        db_pass = settings.DB_PASSWORD
        db_schema = settings.DB_SCHEMA
        if hasattr(sb_config, "settings_file") and sb_config.settings_file:
            override = settings_parser.set_settings(sb_config.settings_file)
            if "DB_HOST" in override.keys():
                db_server = override['DB_HOST']
            if "DB_PORT" in override.keys():
                db_port = override['DB_PORT']
            if "DB_USERNAME" in override.keys():
                db_user = override['DB_USERNAME']
            if "DB_PASSWORD" in override.keys():
                db_pass = override['DB_PASSWORD']
            if "DB_SCHEMA" in override.keys():
                db_schema = override['DB_SCHEMA']
        retry_count = 3
        backoff = 1.2  # Time to wait (in seconds) between retries.
        count = 0
        while count < retry_count:
            try:
                if sys.version_info[0] == 3 and sys.version_info[1] >= 6 or (
                        sys.version_info[0] > 3):
                    # PyMySQL 1.0.0 or above renamed the variables.
                    self.conn = pymysql.connect(host=db_server,
                                                port=db_port,
                                                user=db_user,
                                                password=db_pass,
                                                database=db_schema)
                else:
                    # PyMySQL 0.10.1 for Python 2.7 and Python 3.5
                    self.conn = pymysql.connect(host=db_server,
                                                port=db_port,
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
