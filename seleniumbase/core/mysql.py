"""Wrapper for MySQL DB functions."""


class DatabaseManager:
    """This class wraps MySQL database methods for easy use."""

    def __init__(self, database_env="test", conf_creds=None):
        """Create a connection to the MySQL DB."""
        import fasteners
        import sys
        import time
        from seleniumbase import config as sb_config
        from seleniumbase.config import settings
        from seleniumbase.core import settings_parser
        from seleniumbase.fixtures import constants
        from seleniumbase.fixtures import shared_utils

        pip_find_lock = fasteners.InterProcessLock(
            constants.PipInstall.FINDLOCK
        )
        with pip_find_lock:
            try:
                import pymysql
            except Exception:
                if sys.version_info >= (3, 6):
                    shared_utils.pip_install("pymysql", version="1.0.2")
                else:
                    shared_utils.pip_install("pymysql", version="0.10.1")
                import pymysql
        db_server = settings.DB_HOST
        db_port = settings.DB_PORT
        db_user = settings.DB_USERNAME
        db_pass = settings.DB_PASSWORD
        db_schema = settings.DB_SCHEMA
        if hasattr(sb_config, "settings_file") and sb_config.settings_file:
            override = settings_parser.set_settings(sb_config.settings_file)
            if "DB_HOST" in override.keys():
                db_server = override["DB_HOST"]
            if "DB_PORT" in override.keys():
                db_port = override["DB_PORT"]
            if "DB_USERNAME" in override.keys():
                db_user = override["DB_USERNAME"]
            if "DB_PASSWORD" in override.keys():
                db_pass = override["DB_PASSWORD"]
            if "DB_SCHEMA" in override.keys():
                db_schema = override["DB_SCHEMA"]
        retry_count = 3
        backoff = 1.2  # Time to wait (in seconds) between retries.
        count = 0
        while count < retry_count:
            try:
                if sys.version_info >= (3, 6):
                    # PyMySQL 1.0.0 or above renamed the variables.
                    self.conn = pymysql.connect(
                        host=db_server,
                        port=db_port,
                        user=db_user,
                        password=db_pass,
                        database=db_schema,
                    )
                else:
                    # PyMySQL 0.10.1 for Python 2.7 and Python 3.5
                    self.conn = pymysql.connect(
                        host=db_server,
                        port=db_port,
                        user=db_user,
                        passwd=db_pass,
                        db=db_schema,
                    )
                self.conn.autocommit(True)
                self.cursor = self.conn.cursor()
                return
            except Exception:
                time.sleep(backoff)
                count = count + 1
        if retry_count == 3:
            raise Exception("Unable to connect to Database after 3 retries.")

    def query_fetch_all(self, query, values):
        """Execute db query, get all the values, and close the connection."""
        self.cursor.execute(query, values)
        retval = self.cursor.fetchall()
        self.__close_db()
        return retval

    def query_fetch_one(self, query, values):
        """Execute db query, get the first value, and close the connection."""
        self.cursor.execute(query, values)
        retval = self.cursor.fetchone()
        self.__close_db()
        return retval

    def execute_query(self, query, values):
        """Execute db query, close the connection, and return the results."""
        retval = self.cursor.execute(query, values)
        self.__close_db()
        return retval

    def __close_db(self):
        self.cursor.close()
        self.conn.close()
