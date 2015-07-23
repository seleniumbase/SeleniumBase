"""
You'll probably want to customize this to your own environment and needs.
"""


##### REQUIRED SETTINGS #####

# Default times to wait for page elements to appear before performing actions
SMALL_TIMEOUT = 7
LARGE_TIMEOUT = 14


##### RECOMMENDED SETTINGS #####

# Amazon S3 Bucket Credentials (where screenshots and other log files get saved)
S3_LOG_BUCKET = "[ENTER LOG BUCKET FOLDER NAME HERE]"
S3_BUCKET_URL = "http://[ENTER SUBDOMAIN OF AMAZON BUCKET URL HERE].s3-[ENTER S3 REGION HERE].amazonaws.com/"
S3_SELENIUM_ACCESS_KEY = "[ENTER YOUR S3 ACCESS KEY FOR SELENIUM HERE]"
S3_SELENIUM_SECRET_KEY = "[ENTER YOUR S3 SECRET KEY FOR SELENIUM HERE]"

# MySQL DB Credentials (where data from tests gets saved)
DB_HOST = "[TEST DB HOST]"
DB_USERNAME = "[TEST DB USERNAME]"
DB_PASSWORD = "[TEST DB PASSWORD]"
DB_SCHEMA = "[TEST DB SCHEMA]"


##### OPTIONAL SETTINGS #####

# Default Email Credentials (if tests send out emails, you can scan through and verify them by using IMAP)
EMAIL_USERNAME = "[TEST ACCOUNT GMAIL USERNAME]@gmail.com"
EMAIL_PASSWORD = "[TEST ACCOUNT GMAIL PASSWORD]"
EMAIL_IMAP_STRING = "imap.gmail.com"
EMAIL_IMAP_PORT = 993

# HipChat Reporting Credentials (for HipChat notifications if your team uses HipChat)
# Other info such as room id and owner to mention get entered during nosetest options
HIPCHAT_AUTH_TOKEN = "[ENTER YOUR HIPCHAT AUTH TOKEN HERE]"
