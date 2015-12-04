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
    # Browser windows aren't always maximized. This may display more details.
    logfile_name_2 = "full_screenshot.jpg"

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
        '''try:
            # Let humans see any errors on screen before closing the window
            test.driver.maximize_window()
            import time
            time.sleep(0.2)  # Make sure the screen is ready
        except Exception:
            pass
        # Second screenshot at fullscreen might not be necessary
        # import base64
        screen_b64 = test.driver.get_screenshot_as_base64()
        screen = base64.decodestring(screen_b64)
        screenshot_file_2 = "%s/%s" % (test_logpath, self.logfile_name_2)
        f1 = open(screenshot_file_2, 'w+')
        f1.write(screen)
        f1.close()'''

    def addError(self, test, err, capt=None):
        self.add_screenshot(test, err, capt=capt)

    def addFailure(self, test, err, capt=None, tbinfo=None):
        self.add_screenshot(test, err, capt=capt, tbinfo=tbinfo)
