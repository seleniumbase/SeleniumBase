"""Methods for uploading/managing files on Amazon S3."""

already_uploaded_files = []


class S3LoggingBucket(object):
    """A class for uploading log files from tests to Amazon S3.
    Those files can then be shared easily."""
    from seleniumbase.config import settings

    def __init__(
        self,
        log_bucket=settings.S3_LOG_BUCKET,
        bucket_url=settings.S3_BUCKET_URL,
        selenium_access_key=settings.S3_SELENIUM_ACCESS_KEY,
        selenium_secret_key=settings.S3_SELENIUM_SECRET_KEY,
    ):
        import fasteners
        from seleniumbase.fixtures import constants
        from seleniumbase.fixtures import shared_utils

        pip_find_lock = fasteners.InterProcessLock(
            constants.PipInstall.FINDLOCK
        )
        with pip_find_lock:
            try:
                import boto3
            except Exception:
                shared_utils.pip_install("boto3")
                import boto3
        self.conn = boto3.Session(
            aws_access_key_id=selenium_access_key,
            aws_secret_access_key=selenium_secret_key,
        )
        self.bucket = log_bucket
        self.bucket_url = bucket_url

    def get_key(self, file_name):
        """Create a new S3 connection instance with the given name."""
        return self.conn.resource("s3").Object(self.bucket, file_name)

    def get_bucket(self):
        """Return the bucket being used."""
        return self.bucket

    def upload_file(self, file_name, file_path):
        """Upload a given file from the file_path to the bucket
        with the new name/path file_name."""
        upload_key = self.get_key(file_name)
        content_type = "text/plain"
        if file_name.endswith(".html"):
            content_type = "text/html"
        elif file_name.endswith(".jpg"):
            content_type = "image/jpeg"
        elif file_name.endswith(".png"):
            content_type = "image/png"
        upload_key.Bucket().upload_file(
            file_path,
            file_name,
            ExtraArgs={"ACL": "public-read", "ContentType": content_type},
        )

    def upload_index_file(
        self, test_address, timestamp, data_path, save_data_to_logs
    ):
        """Create an index.html file with links to all the log files
        that were just uploaded."""
        import os

        global already_uploaded_files
        already_uploaded_files = list(set(already_uploaded_files))
        already_uploaded_files.sort()
        file_name = "%s/%s/index.html" % (test_address, timestamp)
        index = self.get_key(file_name)
        index_str = []
        for completed_file in already_uploaded_files:
            index_str.append(
                "<a href='" + self.bucket_url + ""
                "%s'>%s</a>" % (completed_file, completed_file)
            )
        index_page = str("<br>".join(index_str))
        save_data_to_logs(index_page, "index.html")
        file_path = os.path.join(data_path, "index.html")
        index.Bucket().upload_file(
            file_path,
            file_name,
            ExtraArgs={"ACL": "public-read", "ContentType": "text/html"},
        )
        return "%s%s" % (self.bucket_url, file_name)

    def save_uploaded_file_names(self, files):
        """Keep a record of all file names that have been uploaded.
        Upload log files related to each test after its execution.
        Once done, use already_uploaded_files to create an index file."""
        global already_uploaded_files
        already_uploaded_files.extend(files)
