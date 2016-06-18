import os
import shutil
import time
from seleniumbase.config import settings

# Folder for saving downloaded files (Chrome and Firefox ONLY)
DOWNLOADS_DIR = 'downloaded_files'
ARCHIVE_DIR = 'archived_files'

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
