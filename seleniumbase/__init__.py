import collections
import pdb
import shutil
import sys
from selenium import webdriver
from seleniumbase.__version__ import __version__
from seleniumbase.common import decorators  # noqa
from seleniumbase.common import encryption  # noqa
from seleniumbase.core.browser_launcher import get_driver  # noqa
from seleniumbase.fixtures import js_utils  # noqa
from seleniumbase.fixtures import page_actions  # noqa
from seleniumbase.fixtures import page_utils  # noqa
from seleniumbase.fixtures.base_case import BaseCase  # noqa
from seleniumbase.masterqa.master_qa import MasterQA  # noqa
from seleniumbase.plugins.sb_manager import SB  # noqa
from seleniumbase.plugins.driver_manager import Driver  # noqa
from seleniumbase.plugins.driver_manager import DriverContext  # noqa

if hasattr(pdb, "DefaultConfig"):
    # Only load pdbpp configuration if pdbpp is installed
    pdb.DefaultConfig.filename_color = pdb.Color.blue
    pdb.DefaultConfig.line_number_color = pdb.Color.turquoise
    pdb.DefaultConfig.show_hidden_frames_count = False
    pdb.DefaultConfig.disable_pytest_capturing = True
    pdb.DefaultConfig.enable_hidden_frames = False
    pdb.DefaultConfig.truncate_long_lines = True
    pdb.DefaultConfig.sticky_by_default = True
    # Fix spacing for line numbers > 9999
    pdb.Pdb.get_terminal_size = lambda x: (
        shutil.get_terminal_size()[0] - 1,
        shutil.get_terminal_size()[1],
    )
if sys.version_info[0] >= 3:
    from seleniumbase import translate  # noqa
if sys.version_info >= (3, 7):
    webdriver.TouchActions = None  # Lifeline for past selenium-wire versions
if sys.version_info >= (3, 10):
    collections.Callable = collections.abc.Callable  # Lifeline for nosetests
del collections  # Undo "import collections" / Simplify "dir(seleniumbase)"
del sys  # Undo "import sys" / Simplify "dir(seleniumbase)"
del webdriver  # Undo "import webdriver" / Simplify "dir(seleniumbase)"

version_list = [int(i) for i in __version__.split(".") if i.isdigit()]
version_tuple = tuple(version_list)
version_info = version_tuple  # noqa
