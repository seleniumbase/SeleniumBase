"""
This file contains database credentials for the various databases
that the tests need to access
"""

from seleniumbase.config import settings

# Environments
TEST = "test"


class Apps:
    TESTCASE_REPOSITORY = "testcase_repository"


APP_CREDS = {

    Apps.TESTCASE_REPOSITORY: {
        TEST: (
            settings.DB_HOST,
            settings.DB_USERNAME,
            settings.DB_PASSWORD,
            settings.DB_SCHEMA)
    },

}
