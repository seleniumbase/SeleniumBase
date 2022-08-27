"""
To override default settings stored in seleniumbase/config/settings.py,
change the values here and add "--settings=custom_settings.py" when running.
"""

# Default timeout values for waiting for page elements to appear.
MINI_TIMEOUT = 2
SMALL_TIMEOUT = 7
LARGE_TIMEOUT = 10
EXTREME_TIMEOUT = 30

# Default page load timeout.
# In global Selenium settings, this value is set to 300 seconds by default.
# When the timeout is exceeded: "Timed out receiving message from renderer"
PAGE_LOAD_TIMEOUT = 120

# Default page load strategy.
# ["normal", "eager", "none"]
# Selenium default = "normal"
PAGE_LOAD_STRATEGY = "normal"

# If False, only logs from the most recent test run will be saved.
ARCHIVE_EXISTING_LOGS = False
ARCHIVE_EXISTING_DOWNLOADS = False

# If True, switch to new tabs automatically if a click opens a new one.
# (Only happens if the initial tab is still on same URL as before.)
SWITCH_TO_NEW_TABS_ON_CLICK = True

"""
These methods add JS waits, such as self.wait_for_ready_state_complete(),
which waits for document.readyState to be "complete" after Selenium actions.
"""
# Called after self.open(URL), NOT driver.get(URL)
WAIT_FOR_RSC_ON_PAGE_LOADS = True
# Called after self.click(selector), NOT element.click()
WAIT_FOR_RSC_ON_CLICKS = False
# Wait for AngularJS calls to complete after various browser actions.
WAIT_FOR_ANGULARJS = True
# Skip ALL calls to wait_for_ready_state_complete() and wait_for_angularjs().
SKIP_JS_WAITS = False

# Changing the default behavior of Demo Mode. Activate with: --demo_mode
DEFAULT_DEMO_MODE_TIMEOUT = 0.5
HIGHLIGHTS = 4
DEFAULT_MESSAGE_DURATION = 2.55

# Disabling the Content Security Policy of the browser by default.
DISABLE_CSP_ON_FIREFOX = True
DISABLE_CSP_ON_CHROME = False

# If True and --proxy=IP_ADDRESS:PORT is invalid, then error immediately.
RAISE_INVALID_PROXY_STRING_EXCEPTION = True

# Default browser resolutions when opening new windows for tests.
# (Headless resolutions take priority, and include all browsers.)
# (Firefox starts maximized by default when running in GUI Mode.)
CHROME_START_WIDTH = 1250
CHROME_START_HEIGHT = 840
HEADLESS_START_WIDTH = 1440
HEADLESS_START_HEIGHT = 1880

# Changing the default behavior of MasterQA Mode.
MASTERQA_DEFAULT_VALIDATION_MESSAGE = "Does the page look good?"
MASTERQA_WAIT_TIME_BEFORE_VERIFY = 0.5
MASTERQA_START_IN_FULL_SCREEN_MODE = False
MASTERQA_MAX_IDLE_TIME_BEFORE_QUIT = 600

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

# Encryption Settings
# (Used for string/password obfuscation)
# (You should reset the Encryption Key for every clone of SeleniumBase)
ENCRYPTION_KEY = "Pg^.l!8UdJ+Y7dMIe&fl*%!p9@ej]/#tL~3E4%6?"
# These tokens are added to the beginning and end of obfuscated passwords.
# Helps identify which strings/passwords have been obfuscated.
OBFUSCATION_START_TOKEN = "$^*ENCRYPT="
OBFUSCATION_END_TOKEN = "?&#$"
