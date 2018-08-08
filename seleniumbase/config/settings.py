"""
You'll probably want to customize this to your own environment and needs.

If you used ``python setup.py install`` instead of ``python setup.py develop``,
you may need to rerun ``python setup.py install`` in order for your changes
to take effect (unless you switch to using ``develop``).
"""


# #####>>>>>----- REQUIRED/IMPORTANT SETTINGS -----<<<<<#####

# Default maximum time (in seconds) to wait for page elements to appear.
# Different methods/actions in base_case.py use different timeouts.
# If the element to be acted on does not appear in time, the test fails.
MINI_TIMEOUT = 2
SMALL_TIMEOUT = 6
LARGE_TIMEOUT = 10
EXTREME_TIMEOUT = 30

# If True, existing logs from past test runs will be saved and take up space.
# If False, only the logs from the most recent test run will be saved locally.
ARCHIVE_EXISTING_LOGS = False

# If True, existing downloads from past runs will be saved and take up space.
# If False, only the downloads from the most recent run will be saved locally.
ARCHIVE_EXISTING_DOWNLOADS = False

# Default names for files saved during test failures when logging is turned on.
# (These files will get saved to the "latest_logs/" folder)
# Usage: "--with-testing_base"
SCREENSHOT_NAME = "screenshot.png"
BASIC_INFO_NAME = "basic_test_info.txt"
PAGE_SOURCE_NAME = "page_source.html"

# Default names for folders and files saved when reports are turned on.
# Usage: "--report" and "--with-testing_base" together. (NOSETESTS only)
LATEST_REPORT_DIR = "latest_report"
REPORT_ARCHIVE_DIR = "archived_reports"
HTML_REPORT = "report.html"
RESULTS_TABLE = "results_table.csv"

'''
This adds wait_for_ready_state_complete() after various browser actions.
Setting this to True may improve reliability at the cost of speed.
'''
# Called after self.open(url) or self.open_url(url), NOT self.driver.open(url)
WAIT_FOR_RSC_ON_PAGE_LOADS = True
# Called after self.click(selector), NOT element.click()
WAIT_FOR_RSC_ON_CLICKS = True

'''
This adds wait_for_angularjs() after various browser actions.
(Requires WAIT_FOR_RSC_ON_PAGE_LOADS and WAIT_FOR_RSC_ON_CLICKS to also be on.)
'''
WAIT_FOR_ANGULARJS = True

# Option to start Chrome in full screen mode by default
START_CHROME_IN_FULL_SCREEN_MODE = False

# Default time to wait after each browser action performed during Demo Mode.
# Use Demo Mode when you want others to see what your automation is doing.
# Usage: "--demo_mode". (Can be overwritten by using "--demo_sleep=TIME".)
DEFAULT_DEMO_MODE_TIMEOUT = 0.5

# Number of times to repeat the demo_mode highlight animation.
# Each loop is about 0.18 seconds. (Override by using "--highlights=TIMES".)
HIGHLIGHTS = 4

# Default time to keep messenger notifications visible (in seconds).
# Messenger notifications appear when reaching assert statements in Demo Mode.
DEFAULT_MESSAGE_DURATION = 2.55

# #####>>>>>----- MasterQA SETTINGS -----<<<<<#####
# ##### (Used when importing MasterQA as the parent class)

# The default message that appears when you don't specify a custom message
MASTERQA_DEFAULT_VALIDATION_MESSAGE = "Does the page look good?"

# The time delay (in seconds) before the validation pop-up appears
# This value can be overwritten on the command line. Ex: --verify_delay=0.5
MASTERQA_WAIT_TIME_BEFORE_VERIFY = 1.0

# If True, the automation will start in full-screen mode
MASTERQA_START_IN_FULL_SCREEN_MODE = False

# The maximimum idle time allowed (in seconds) before timing out and exiting
MASTERQA_MAX_IDLE_TIME_BEFORE_QUIT = 600


# #####>>>>>----- RECOMMENDED SETTINGS -----<<<<<#####
# ##### (For database reporting, saving test logs, and password encryption)

# MySQL DB Credentials
# (For saving data from tests)
DB_HOST = "127.0.0.1"
DB_USERNAME = "root"
DB_PASSWORD = "test"
DB_SCHEMA = "test_db"


# Amazon S3 Bucket Credentials
# (For saving screenshots and other log files from tests)
# (Bucket names are unique across all existing bucket names in Amazon S3)
S3_LOG_BUCKET = "[S3 BUCKET NAME]"
S3_BUCKET_URL = "https://s3.amazonaws.com/[S3 BUCKET NAME]/"
S3_SELENIUM_ACCESS_KEY = "[S3 ACCESS KEY]"
S3_SELENIUM_SECRET_KEY = "[S3 SECRET KEY]"


# ENCRYPTION SETTINGS
# (Used for string/password obfuscation)
# (You should reset the Encryption Key for every clone of SeleniumBase)
ENCRYPTION_KEY = "Pg^.l!8UdJ+Y7dMIe&fl*%!p9@ej]/#tL~3E4%6?"
# These tokens are added to the beginning and end of obfuscated passwords.
# Helps identify which strings/passwords have been obfuscated.
OBFUSCATION_START_TOKEN = "$^*ENCRYPT="
OBFUSCATION_END_TOKEN = "?&#$"


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
