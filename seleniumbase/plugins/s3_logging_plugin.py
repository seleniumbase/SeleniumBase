"""S3 Logging Plugin for SeleniumBase tests that run with pynose / nosetests"""
import uuid
import os
from nose.plugins import Plugin


class S3Logging(Plugin):
    """The plugin for uploading test logs to the S3 bucket specified."""
    name = "s3_logging"  # Usage: --with-s3-logging

    def configure(self, options, conf):
        """Get the options."""
        super().configure(options, conf)
        self.options = options
        self.test_id = None

    def save_data_to_logs(self, data, file_name):
        from seleniumbase.fixtures import page_utils

        test_logpath = os.path.join(self.options.log_path, self.test_id)
        file_name = str(file_name)
        destination_folder = test_logpath
        page_utils._save_data_as(data, destination_folder, file_name)

    def afterTest(self, test):
        """Upload logs to the S3 bucket after tests complete."""
        from seleniumbase.core.s3_manager import S3LoggingBucket

        self.test_id = test.test.id()
        s3_bucket = S3LoggingBucket()
        guid = str(uuid.uuid4().hex)
        path = os.path.join(self.options.log_path, self.test_id)
        uploaded_files = []
        for logfile in os.listdir(path):
            logfile_name = "%s/%s/%s" % (
                guid,
                self.test_id,
                logfile.split(path)[-1],
            )
            s3_bucket.upload_file(logfile_name, os.path.join(path, logfile))
            uploaded_files.append(logfile_name)
        s3_bucket.save_uploaded_file_names(uploaded_files)
        index_file = s3_bucket.upload_index_file(
            test.id(), guid, path, self.save_data_to_logs
        )
        print("\n*** Log files uploaded: ***\n%s\n" % index_file)

        # If the SB database plugin is also being used,
        # attach a link to the logs index database row.
        if hasattr(test.test, "testcase_guid"):
            from seleniumbase.core.testcase_manager import (
                TestcaseDataPayload,
                TestcaseManager,
            )

            self.testcase_manager = TestcaseManager(self.options.database_env)
            data_payload = TestcaseDataPayload()
            data_payload.guid = test.test.testcase_guid
            data_payload.log_url = index_file
            self.testcase_manager.update_testcase_log_url(data_payload)
