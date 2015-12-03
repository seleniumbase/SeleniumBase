"""
Manager for dealing with uploading/managing files on S3
"""
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from seleniumbase.config import settings

already_uploaded_files = []


class S3LoggingBucket(object):
    """
    A class to upload our log files from tests to S3, from
    whence we can share them.
    """

    def __init__(self,
                 log_bucket=settings.S3_LOG_BUCKET,
                 bucket_url=settings.S3_BUCKET_URL,
                 selenium_access_key=settings.S3_SELENIUM_ACCESS_KEY,
                 selenium_secret_key=settings.S3_SELENIUM_SECRET_KEY):

        self.conn = S3Connection(selenium_access_key,
                                 selenium_secret_key)
        self.bucket = self.conn.get_bucket(log_bucket)
        self.bucket_url = bucket_url

    def get_key(self, _name):
        """create a new Key instance with the given name"""
        return Key(bucket=self.bucket, name=_name)

    def get_bucket(self):
        """return the bucket we're using"""
        return self.bucket

    def upload_file(self, file_name, file_path):
        """upload a given file from the file_path to the bucket
        with the new name/path file_name"""
        upload_key = Key(bucket=self.bucket, name=file_name)
        content_type = "text/plain"
        if file_name.endswith(".html"):
            content_type = "text/html"
        if file_name.endswith(".jpg"):
            content_type = "image/jpg"
        upload_key.set_contents_from_filename(
            file_path,
            headers={"Content-Type": content_type})
        upload_key.url = \
            upload_key.generate_url(expires_in=3600).split("?")[0]
        try:
            upload_key.make_public()
        except:
            pass
        return file_name

    def upload_index_file(self, test_address, timestamp):
        """create an index.html file with links to all the log files we
        just uploaded"""
        global already_uploaded_files
        already_uploaded_files = list(set(already_uploaded_files))
        already_uploaded_files.sort()
        file_name = "%s/%s/index.html" % (test_address, timestamp)
        index = self.get_key(file_name)
        index_str = []
        for completed_file in already_uploaded_files:
            index_str.append("<a href='" + self.bucket_url +
                             "%s'>%s</a>" % (completed_file, completed_file))
        index.set_contents_from_string(
            "<br>".join(index_str),
            headers={"Content-Type": "text/html"})
        index.make_public()
        return "%s%s" % (self.bucket_url, file_name)

    def save_uploaded_file_names(self, files):
        """We keep record of file names that have been uploaded. We upload log
        files related to each test after its execution. Once we're done, we
        use already_uploaded_files to create an index file"""
        global already_uploaded_files
        already_uploaded_files.extend(files)
