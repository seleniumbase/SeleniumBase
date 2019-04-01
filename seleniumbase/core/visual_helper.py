import os
from seleniumbase.fixtures import constants

VISUAL_BASELINE_DIR = constants.VisualBaseline.STORAGE_FOLDER
abs_path = os.path.abspath('.')
visual_baseline_path = os.path.join(abs_path, VISUAL_BASELINE_DIR)


def get_visual_baseline_folder():
    return visual_baseline_path


def visual_baseline_folder_setup():
    """ Handle Logging """
    if not os.path.exists(visual_baseline_path):
        try:
            os.makedirs(visual_baseline_path)
        except Exception:
            pass  # Should only be reachable during multi-threaded runs
