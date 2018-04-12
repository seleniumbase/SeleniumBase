"""
This file organizes connection details to the Testcase Database.
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
