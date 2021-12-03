"""
You'll probably want to customize this to your own environment and needs.

For changes to take effect immediately, use Python's Develop Mode.
Develop Mode Install: "pip install -e ."  (from the top-level directory)
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
# You can also archive existing logs on the command line with: "--archive_logs"
ARCHIVE_EXISTING_LOGS = False

# If True, existing downloads from past runs will be saved and take up space.
# If False, only the downloads from the most recent run will be saved locally.
ARCHIVE_EXISTING_DOWNLOADS = False

# Default names for files saved during test failures.
# (These files will get saved to the "latest_logs/" folder.)
SCREENSHOT_NAME = "screenshot.png"
BASIC_INFO_NAME = "basic_test_info.txt"
PAGE_SOURCE_NAME = "page_source.html"

# Default names for files and folders saved when using nosetests reports.
# Usage: "--report". (NOSETESTS only)
LATEST_REPORT_DIR = "latest_report"
REPORT_ARCHIVE_DIR = "archived_reports"
HTML_REPORT = "report.html"
RESULTS_TABLE = "results_table.csv"

"""
If True, switch to new tabs/windows automatically if a click opens a new one.
(This switch only happens if the initial tab is still on same URL as before,
which prevents a situation where a click opens up a new URL in the same tab,
where a pop-up might open up a new tab on its own, leading to a double open.
If False, the browser will stay on the current tab where the click happened.
"""
SWITCH_TO_NEW_TABS_ON_CLICK = True

"""
This adds wait_for_ready_state_complete() after various browser actions.
Setting this to True may improve reliability at the cost of speed.
"""
# Called after self.open(url) or self.open_url(url), NOT self.driver.open(url)
WAIT_FOR_RSC_ON_PAGE_LOADS = True
# Called after self.click(selector), NOT element.click()
WAIT_FOR_RSC_ON_CLICKS = False

"""
This adds wait_for_angularjs() after various browser actions.
(Requires WAIT_FOR_RSC_ON_PAGE_LOADS and WAIT_FOR_RSC_ON_CLICKS to also be on.)
"""
WAIT_FOR_ANGULARJS = True

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

# If True, the Content Security Policy will be disabled on Firefox.
# If False, each website's default Content Security Policy will be used.
# (A website's CSP may prevent SeleniumBase from loading custom JavaScript.)
# If using demo_mode or MasterQA, this value will become True regardless.
# You can also disable the CSP on the command line by using "--disable_csp".
DISABLE_CSP_ON_FIREFOX = True

# If True, the Content Security Policy will be disabled on Chrome.
# If False, each website's default Content Security Policy will be used.
# (A website's CSP may prevent SeleniumBase from loading custom JavaScript.)
# You can also disable the CSP on the command line by using "--disable_csp".
DISABLE_CSP_ON_CHROME = False

# If True, an Exception is raised immediately for invalid proxy string syntax.
# If False, a Warning will appear after the test, with no proxy server used.
# (This applies when using --proxy=[PROXY_STRING] for using a proxy server.)
RAISE_INVALID_PROXY_STRING_EXCEPTION = True

# Default browser resolutions when opening new windows for tests.
# (Headless resolutions take priority, and include all browsers.)
# (Firefox starts maximized by default when running in GUI Mode.)
CHROME_START_WIDTH = 1250
CHROME_START_HEIGHT = 840
HEADLESS_START_WIDTH = 1440
HEADLESS_START_HEIGHT = 1880

# #####>>>>>----- MasterQA SETTINGS -----<<<<<#####
# ##### (Used when importing MasterQA as the parent class)

# The default message that appears when you don't specify a custom message
MASTERQA_DEFAULT_VALIDATION_MESSAGE = "Does the page look good?"

# The time delay (in seconds) before the MasterQA validation pop-up appears.
# This value can be overwritten on the command line. Ex: --verify_delay=1.0
MASTERQA_WAIT_TIME_BEFORE_VERIFY = 0.5

# If True, the automation will start in full-screen mode
MASTERQA_START_IN_FULL_SCREEN_MODE = False

# The maximum idle time allowed (in seconds) before timing out and exiting
MASTERQA_MAX_IDLE_TIME_BEFORE_QUIT = 600


# #####>>>>>----- RECOMMENDED SETTINGS -----<<<<<#####
# ##### (For multi-factor auth, DB/cloud logging, and password encryption)

# Google Authenticator
# (For 2-factor authentication using a time-based one-time password algorithm)
# (See https://github.com/pyotp/pyotp and https://pypi.org/project/pyotp/ )
# (Also works with Authy and other compatible apps.)
# Usage: "self.get_google_auth_password()"  (output based on timestamp)
# Usage with override: "self.get_google_auth_password(totp_key=TOTP_KEY)"
TOTP_KEY = "base32secretABCD"


# MySQL DB Credentials
# (For saving data from tests to a MySQL DB)
# Usage: "--with-db_reporting"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USERNAME = "root"
DB_PASSWORD = "test"
DB_SCHEMA = "test_db"


# Amazon S3 Bucket Credentials
# (For saving screenshots and other log files from tests)
# (Bucket names are unique across all existing bucket names in Amazon S3)
# Usage: "--with-s3_logging"
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
