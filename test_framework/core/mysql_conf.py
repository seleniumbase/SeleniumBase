"""
This file contains database credentials for the various databases the tests need to access
"""

# Environments
TEST = "test"

class Apps:
    TESTCASE_REPOSITORY = "testcase_repository"

APP_CREDS = {

    Apps.TESTCASE_REPOSITORY: {
        TEST: ("[TEST DB HOST]", 
             "[TEST DB USERNAME]", "[TEST DB PASSWORD]", "[TEST DB SCHEMA]")
    },

}
