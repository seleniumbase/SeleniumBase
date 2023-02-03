import os
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ScreenshotTests(BaseCase):
    def test_save_screenshot(self):
        self.open("https://seleniumbase.io/demo_page")
        # "./downloaded_files" is a special SeleniumBase folder for downloads
        self.save_screenshot("demo_page.png", folder="./downloaded_files")
        self.assert_downloaded_file("demo_page.png")
        print('\n"%s/%s" was saved!' % ("downloaded_files", "demo_page.png"))

    def test_save_screenshot_to_logs(self):
        self.open("https://seleniumbase.io/demo_page")
        self.save_screenshot_to_logs()
        # "self.log_path" is the absolute path to the "./latest_logs" folder.
        # Each test that generates log files will create a subfolder in there
        test_logpath = os.path.join(self.log_path, self.test_id)
        expected_screenshot = os.path.join(test_logpath, "_1_screenshot.png")
        self.assert_true(os.path.exists(expected_screenshot))
        print('\n"%s" was saved!' % (expected_screenshot))

        self.open("https://seleniumbase.io/tinymce/")
        self.save_screenshot_to_logs()
        expected_screenshot = os.path.join(test_logpath, "_2_screenshot.png")
        self.assert_true(os.path.exists(expected_screenshot))
        print('"%s" was saved!' % (expected_screenshot))

        self.open("https://seleniumbase.io/error_page/")
        self.save_screenshot_to_logs("error_page")
        expected_screenshot = os.path.join(test_logpath, "_3_error_page.png")
        self.assert_true(os.path.exists(expected_screenshot))
        print('"%s" was saved!' % (expected_screenshot))

        self.open("https://seleniumbase.io/devices/")
        self.save_screenshot_to_logs("devices")
        expected_screenshot = os.path.join(test_logpath, "_4_devices.png")
        self.assert_true(os.path.exists(expected_screenshot))
        print('"%s" was saved!' % (expected_screenshot))
