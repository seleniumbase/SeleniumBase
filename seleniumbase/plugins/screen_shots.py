"""
Contains the screenshot plugin for the selenium tests.
"""

import os
from nose.plugins import Plugin
from seleniumbase.config import settings


class ScreenShots(Plugin):
    """
    This plugin will take a screenshot when either a test fails
    or raises an error. It will store that screenshot either in
    the default logs file or in another file of the user's specification.
    """

    name = "screen_shots"
    logfile_name = settings.SCREENSHOT_NAME

    def options(self, parser, env):
        super(ScreenShots, self).options(parser, env=env)

    def configure(self, options, conf):
        super(ScreenShots, self).configure(options, conf)
        if not self.enabled:
            return
        self.options = options

    def add_screenshot(self, test, err, capt=None, tbinfo=None):
        test_logpath = self.options.log_path + "/" + test.id()
        if not os.path.exists(test_logpath):
            os.makedirs(test_logpath)
        screenshot_file = "%s/%s" % (test_logpath, self.logfile_name)
        test.driver.get_screenshot_as_file(screenshot_file)

    def addError(self, test, err, capt=None):
        self.add_screenshot(test, err, capt=capt)

    def addFailure(self, test, err, capt=None, tbinfo=None):
        self.add_screenshot(test, err, capt=capt, tbinfo=tbinfo)
