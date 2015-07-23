"""
You'll probably want to customize this to your enviroment and needs.
"""

# Default time to wait for page elements to appear before performing actions
SMALL_TIMEOUT = 7
LARGE_TIMEOUT = 14

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
