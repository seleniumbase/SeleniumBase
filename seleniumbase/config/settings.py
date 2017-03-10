"""
You'll probably want to customize this to your own environment and needs.

NOSETESTS USERS: IF YOU MAKE CHANGES TO THIS FILE, YOU NEED TO RERUN
``python setup.py install`` IN ORDER FOR YOUR CHANGES TO TAKE EFFECT.
"""


# #####>>>>>----- REQUIRED/IMPORTANT SETTINGS -----<<<<<#####

# Default seconds to wait for page elements to appear before performing actions
TINY_TIMEOUT = 0.1
MINI_TIMEOUT = 2
SMALL_TIMEOUT = 5
LARGE_TIMEOUT = 10
EXTREME_TIMEOUT = 30

# Default time to wait after each browser action performed during Demo Mode
# Use Demo Mode when you want others to see what your automation is doing
# Usage: --demo_mode when run from the command line when using --with-selenium
# This value can be overwritten on the command line by using --demo_sleep=FLOAT
DEFAULT_DEMO_MODE_TIMEOUT = 1.0

# Number of times to repeat the highlight animation. (Seen during Demo Mode)
# Each loop is about 0.18 seconds.
# This value can be overwritten on the command line by using --highlights=TIMES
HIGHLIGHTS = 4

# If True, existing logs from past test runs will be saved and take up space.
# If False, only the logs from the most recent test run will be saved locally.
# This has no effect on Jenkins/S3/MySQL, which may still be saving test logs.
ARCHIVE_EXISTING_LOGS = False

# If True, existing downloads from past runs will be saved and take up space.
# If False, only the downloads from the most recent run will be saved locally.
ARCHIVE_EXISTING_DOWNLOADS = False

# Default names for files saved during test failures when logging is turned on.
# (These files will get saved to the "latest_logs/" folder)
# Usage: "--with-testing_base"
SCREENSHOT_NAME = "screenshot.jpg"
BASIC_INFO_NAME = "basic_test_info.txt"
PAGE_SOURCE_NAME = "page_source.html"

# Default names for folders and files saved when reports are turned on.
# Usage: "--report" (Also requires: "--with-testing_base")
LATEST_REPORT_DIR = "latest_report"
REPORT_ARCHIVE_DIR = "archived_reports"
HTML_REPORT = "report.html"
RESULTS_TABLE = "results_table.csv"

'''
This adds wait_for_ready_state_complete() after various browser actions.
By default, Selenium waits for the 'interactive' state before continuing.
Setting this to True may improve reliability at the cost of speed.
WARNING: Some websites are in a perpetual "interactive" state due to
dynamic content that never fully finishes loading (Use "False" there).
'''
# Called after self.open(url) or self.open_url(url), NOT self.driver.open(url)
WAIT_FOR_RSC_ON_PAGE_LOADS = True
# Called after self.click(selector), NOT element.click()
WAIT_FOR_RSC_ON_CLICKS = True


# #####>>>>>----- MasterQA SETTINGS -----<<<<<#####
# ##### (Used when importing MasterQA as the parent class)

# The default message that appears when you don't specify a custom message
MASTERQA_DEFAULT_VALIDATION_MESSAGE = "Does the page look good?"

# The time delay (in seconds) before the validation pop-up appears
# This value can be overwritten on the command line. Ex: --verify_delay=0.5
MASTERQA_WAIT_TIME_BEFORE_VERIFY = 1.0

# If True, the automation will start in full-screen mode
MASTERQA_START_IN_FULL_SCREEN_MODE = True

# The maximimum idle time allowed (in seconds) before timing out and exiting
MASTERQA_MAX_IDLE_TIME_BEFORE_QUIT = 600


# #####>>>>>----- RECOMMENDED SETTINGS -----<<<<<#####
# ##### (For database reporting and saving test logs)

# MySQL DB Credentials
# (For saving data from tests)
DB_HOST = "127.0.0.1"
DB_USERNAME = "root"
DB_PASSWORD = "test"
DB_SCHEMA = "test"


# Amazon S3 Bucket Credentials
# (For saving screenshots and other log files from tests)
S3_LOG_BUCKET = "[S3 BUCKET NAME]"
S3_BUCKET_URL = "https://[S3 BUCKET NAME].s3.amazonaws.com/"
S3_SELENIUM_ACCESS_KEY = "[S3 ACCESS KEY]"
S3_SELENIUM_SECRET_KEY = "[S3 SECRET KEY]"


# #####>>>>>----- OPTIONAL SETTINGS -----<<<<<#####
# ##### (For reading emails, notifying people via chat apps, etc.)

# Default Email Credentials
# (If tests send out emails, you can scan and verify them by using IMAP)
# Here's a list of imap strings for known email providers:
# - Gmail:         imap.gmail.com
# - Outlook/Live:  imap-mail.outlook.com
# - Yahoo Mail:    imap.mail.yahoo.com
# - AT&T:          imap.mail.att.net
# - Comcast:       imap.comcast.net
# - Verizon:       incoming.verizon.net
EMAIL_USERNAME = "[TEST ACCOUNT GMAIL USERNAME]@gmail.com"
EMAIL_PASSWORD = "[TEST ACCOUNT GMAIL PASSWORD]"
EMAIL_IMAP_STRING = "imap.gmail.com"
EMAIL_IMAP_PORT = 993

# HipChat Reporting Credentials
# (For HipChat notifications if your team uses HipChat)
# (room_id and owner_to_mention get entered during nosetest options)
HIPCHAT_AUTH_TOKEN = "[ENTER YOUR HIPCHAT AUTH TOKEN HERE]"
