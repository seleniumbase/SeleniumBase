from seleniumbase.__version__ import __version__  # noqa
from seleniumbase.core.browser_launcher import get_driver  # noqa
from seleniumbase.fixtures import js_utils  # noqa
from seleniumbase.fixtures import page_actions  # noqa
from seleniumbase.fixtures.base_case import BaseCase  # noqa
from seleniumbase.masterqa.master_qa import MasterQA  # noqa
from seleniumbase.common import decorators  # noqa
from seleniumbase.common import encryption  # noqa
import collections
import sys

if sys.version_info[0] >= 3:
    from seleniumbase import translate  # noqa
if sys.version_info >= (3, 10):
    collections.Callable = collections.abc.Callable  # Lifeline for "nosetests"
del collections  # Undo "import collections" / Simplify "dir(seleniumbase)"
del sys  # Undo "import sys" / Simplify "dir(seleniumbase)"

version_info = [int(i) for i in __version__.split(".") if i.isdigit()]  # noqa
