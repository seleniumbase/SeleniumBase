"""The plugin for saving basic test info for Selenium tests."""
import os
import codecs
import time
import traceback
from nose.plugins import Plugin
from seleniumbase.config import settings


class BasicTestInfo(Plugin):
    """This plugin captures basic info when a test fails or raises an error."""
    name = "basic_test_info"  # Usage: --with-basic_test_info
    logfile_name = settings.BASIC_INFO_NAME

    def options(self, parser, env):
        super().options(parser, env=env)

    def configure(self, options, conf):
        super().configure(options, conf)
        if not self.enabled:
            return
        self.options = options

    def addError(self, test, err, capt=None):
        test_logpath = self.options.log_path + "/" + test.id()
        if not os.path.exists(test_logpath):
            os.makedirs(test_logpath)
        file_name = "%s/%s" % (test_logpath, self.logfile_name)
        basic_info_file = codecs.open(file_name, "w+", "utf-8")
        self.__log_test_error_data(basic_info_file, test, err, "Error")
        basic_info_file.close()

    def addFailure(self, test, err, capt=None, tbinfo=None):
        test_logpath = self.options.log_path + "/" + test.id()
        if not os.path.exists(test_logpath):
            os.makedirs(test_logpath)
        file_name = "%s/%s" % (test_logpath, self.logfile_name)
        basic_info_file = codecs.open(file_name, "w+", "utf-8")
        self.__log_test_error_data(basic_info_file, test, err, "Error")
        basic_info_file.close()

    def __log_test_error_data(self, log_file, test, err, type):
        data_to_save = []
        data_to_save.append("Last Page: %s" % test.driver.current_url)
        data_to_save.append("  Browser: %s" % self.options.browser)
        data_to_save.append("Timestamp: %s" % int(time.time()))
        data_to_save.append("Server: %s " % self.options.servername)
        data_to_save.append("%s: %s" % (type, err[0]))
        data_to_save.append(
            "Traceback: " + "".join(traceback.format_exception(*err))
        )
        log_file.writelines("\r\n".join(data_to_save))
