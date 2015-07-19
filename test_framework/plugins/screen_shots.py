"""
Contains the screenshot plugin for the selenium tests.
"""

import os
import time
import base64
from nose.plugins import Plugin

class ScreenShots(Plugin):
    """
    This plugin will take a screenshot when either a test fails
    or raises an error. It will store that screenshot either in
    the default logs file or in another file of the user's specification.
    """

    name = "screen_shots"
    logfile_name = "screenshot.jpg"
    # Browser windows aren't always maximized. This may display more details.
    logfile_name_2 = "screenshot_fullscreen.jpg"

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
        try:
            test.driver.maximize_window()
        except Exception:
            pass
        screen_b64 = test.driver.get_screenshot_as_base64()
        screen = base64.decodestring(screen_b64)
        time.sleep(0.3)
        screenshot_file_2 = "%s/%s" % (test_logpath, self.logfile_name_2)
        f1 = open(screenshot_file_2, 'w+')
        f1.write(screen)
        f1.close()


    def addError(self, test, err, capt=None):
        self.add_screenshot(test, err, capt=capt)


    def addFailure(self, test, err, capt=None, tbinfo=None):
        self.add_screenshot(test, err, capt=capt, tbinfo=tbinfo)
