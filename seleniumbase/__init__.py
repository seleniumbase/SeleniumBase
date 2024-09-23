import collections
import os
import pdb
try:
    import pdbp  # (Pdb+) --- Python Debugger Plus
except Exception:
    pass
import sys
from selenium import webdriver
from seleniumbase.__version__ import __version__
from seleniumbase.common import decorators  # noqa
from seleniumbase.common import encryption  # noqa
from seleniumbase.core import colored_traceback  # noqa
from seleniumbase.core.browser_launcher import get_driver  # noqa
from seleniumbase.fixtures import js_utils  # noqa
from seleniumbase.fixtures import page_actions  # noqa
from seleniumbase.fixtures import page_utils  # noqa
from seleniumbase.fixtures import shared_utils  # noqa
from seleniumbase.fixtures.base_case import BaseCase  # noqa
from seleniumbase.masterqa.master_qa import MasterQA  # noqa
from seleniumbase.plugins.sb_manager import SB  # noqa
from seleniumbase.plugins.driver_manager import Driver  # noqa
from seleniumbase.plugins.driver_manager import DriverContext  # noqa
from seleniumbase import translate  # noqa

if sys.version_info[0] < 3 and "pdbp" in locals():
    # With Python3, "import pdbp" is all you need
    for key in pdbp.__dict__.keys():
        # Replace pdb with pdbp
        pdb.__dict__[key] = pdbp.__dict__[key]
    if hasattr(pdb, "DefaultConfig"):
        # Here's how to customize Pdb+ options
        pdb.DefaultConfig.filename_color = pdb.Color.fuchsia
        pdb.DefaultConfig.line_number_color = pdb.Color.turquoise
        pdb.DefaultConfig.truncate_long_lines = False
        pdb.DefaultConfig.sticky_by_default = True
colored_traceback.add_hook()
os.environ["SE_AVOID_STATS"] = "true"  # Disable Selenium Manager stats
webdriver.TouchActions = None  # Lifeline for past selenium-wire versions
if sys.version_info >= (3, 10):
    collections.Callable = collections.abc.Callable  # Lifeline for nosetests
del collections  # Undo "import collections" / Simplify "dir(seleniumbase)"
del os  # Undo "import os" / Simplify "dir(seleniumbase)"
del sys  # Undo "import sys" / Simplify "dir(seleniumbase)"
del webdriver  # Undo "import webdriver" / Simplify "dir(seleniumbase)"

version_list = [int(i) for i in __version__.split(".") if i.isdigit()]
version_tuple = tuple(version_list)
version_info = version_tuple  # noqa
