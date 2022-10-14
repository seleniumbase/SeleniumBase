import collections
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
