import os
import shutil
import time
from seleniumbase.config import settings
from seleniumbase.fixtures import constants

# Folder for saving downloaded files.
# If initiated by WebDriver clicks, works ONLY for Chrome and Firefox.
# Browser used doesn't matter if done with self.download_file(file_url)
# or self.save_file_as(file_url, new_file_name)
DOWNLOADS_DIR = constants.Files.DOWNLOADS_FOLDER
ARCHIVE_DIR = constants.Files.ARCHIVED_DOWNLOADS_FOLDER

abs_path = os.path.abspath('.')
downloads_path = abs_path + "/" + DOWNLOADS_DIR


def get_downloads_folder():
    return downloads_path


def reset_downloads_folder():
    ''' Clears the downloads folder.
        If settings.ARCHIVE_EXISTING_DOWNLOADS is set to True, archives it. '''
    if os.path.exists(downloads_path):
        archived_downloads_folder = "%s/../%s/" % (downloads_path, ARCHIVE_DIR)
        if not os.path.exists(archived_downloads_folder):
            os.makedirs(archived_downloads_folder)
        archived_downloads_folder = "%sdownloads_%s" % (
            archived_downloads_folder, int(time.time()))
        shutil.move(downloads_path, archived_downloads_folder)
        os.makedirs(downloads_path)
        if not settings.ARCHIVE_EXISTING_DOWNLOADS:
            shutil.rmtree(archived_downloads_folder)
