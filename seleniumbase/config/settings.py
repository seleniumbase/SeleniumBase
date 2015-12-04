"""
You'll probably want to customize this to your own environment and needs.
"""


# #####>>>>>----- REQUIRED/IMPORTANT SETTINGS -----<<<<<#####

# Default times to wait for page elements to appear before performing actions
SMALL_TIMEOUT = 5
LARGE_TIMEOUT = 10
EXTREME_TIMEOUT = 30

# If True, existing logs from past test runs will be saved and take up space.
# If False, only the logs from the most recent test run will be saved locally.
# This has no effect on Jenkins/S3/MySQL, which may still be saving test logs.
ARCHIVE_EXISTING_LOGS = False

# Default names for files saved during test failures when logging is turned on.
# (These files will get saved to the "logs/" folder)
SCREENSHOT_NAME = "screenshot.jpg"
BASIC_INFO_NAME = "basic_test_info.txt"
PAGE_SOURCE_NAME = "page_source.html"

''' This adds wait_for_ready_state_complete() after various browser actions.
    By default, Selenium waits for the 'interactive' state before continuing.
    Setting this to True may improve reliability at the cost of speed.
    WARNING: Some websites are in a perpetual "interactive" state due to
    dynamic content that never fully finishes loading (Use "False" there). '''
# Called after self.open(url) or self.open_url(url), NOT self.driver.open(url)
WAIT_FOR_RSC_ON_PAGE_LOADS = False
# Called after self.click(selector), NOT element.click()
WAIT_FOR_RSC_ON_CLICKS = False


# #####>>>>>----- RECOMMENDED SETTINGS -----<<<<<#####
# ##### (For test logging and database reporting)

# Amazon S3 Bucket Credentials
# (For saving screenshots and other log files from tests)
S3_LOG_BUCKET = "[ENTER LOG BUCKET FOLDER NAME HERE]"
S3_BUCKET_URL = ("http://[ENTER SUBDOMAIN OF AMAZON BUCKET URL HERE]"
                 ".s3-[ENTER S3 REGION HERE].amazonaws.com/")
S3_SELENIUM_ACCESS_KEY = "[ENTER YOUR S3 ACCESS KEY FOR SELENIUM HERE]"
S3_SELENIUM_SECRET_KEY = "[ENTER YOUR S3 SECRET KEY FOR SELENIUM HERE]"

# MySQL DB Credentials
# (For saving data from tests)
DB_HOST = "[TEST DB HOST]"  # Ex: "127.0.0.1"
DB_USERNAME = "[TEST DB USERNAME]"  # Ex: "root"
DB_PASSWORD = "[TEST DB PASSWORD]"  # Ex: "test"
DB_SCHEMA = "[TEST DB SCHEMA]"  # Ex: "test"


# #####>>>>>----- OPTIONAL SETTINGS -----<<<<<#####
# ##### (For reading emails, notifying people via chat apps, etc.)

# Default Email Credentials
# (If tests send out emails, you can scan and verify them by using IMAP)
EMAIL_USERNAME = "[TEST ACCOUNT GMAIL USERNAME]@gmail.com"
EMAIL_PASSWORD = "[TEST ACCOUNT GMAIL PASSWORD]"
EMAIL_IMAP_STRING = "imap.gmail.com"
EMAIL_IMAP_PORT = 993

# HipChat Reporting Credentials
# (For HipChat notifications if your team uses HipChat)
# (room_id and owner_to_mention get entered during nosetest options)
HIPCHAT_AUTH_TOKEN = "[ENTER YOUR HIPCHAT AUTH TOKEN HERE]"
