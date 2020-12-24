"""
The S3 Logging Plugin to upload all logs to the S3 bucket specified.
"""

import uuid
import logging
import os
from seleniumbase.core.s3_manager import S3LoggingBucket
from nose.plugins import Plugin


class S3Logging(Plugin):
    """
    The plugin for uploading test logs to the S3 bucket specified.
    """
    name = 's3_logging'  # Usage: --with-s3_logging

    def configure(self, options, conf):
        """ Get the options. """
        super(S3Logging, self).configure(options, conf)
        self.options = options

    def afterTest(self, test):
        """ After each testcase, upload logs to the S3 bucket. """
        s3_bucket = S3LoggingBucket()
        guid = str(uuid.uuid4().hex)
        path = "%s/%s" % (self.options.log_path,
                          test.test.id())
        uploaded_files = []
        for logfile in os.listdir(path):
            logfile_name = "%s/%s/%s" % (guid,
                                         test.test.id(),
                                         logfile.split(path)[-1])
            s3_bucket.upload_file(logfile_name,
                                  "%s/%s" % (path, logfile))
            uploaded_files.append(logfile_name)
        s3_bucket.save_uploaded_file_names(uploaded_files)
        index_file = s3_bucket.upload_index_file(test.id(), guid)
        print("\n\n*** Log files uploaded: ***\n%s\n" % index_file)
        logging.error("\n\n*** Log files uploaded: ***\n%s\n" % index_file)

        # If the database plugin is running, attach a link
        # to the logs index database row
        if hasattr(test.test, "testcase_guid"):
            from seleniumbase.core.testcase_manager \
                import TestcaseDataPayload, TestcaseManager
            self.testcase_manager = TestcaseManager(self.options.database_env)
            data_payload = TestcaseDataPayload()
            data_payload.guid = test.test.testcase_guid
            data_payload.log_url = index_file
            self.testcase_manager.update_testcase_log_url(data_payload)
