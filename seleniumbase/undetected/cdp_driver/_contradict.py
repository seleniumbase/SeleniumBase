import warnings as _warnings
from collections.abc import Mapping as _Mapping, Sequence as _Sequence
import logging

__logger__ = logging.getLogger(__name__)
__all__ = ["cdict", "ContraDict"]


def cdict(*args, **kwargs):
    """Factory function"""
    return ContraDict(*args, **kwargs)


class ContraDict(dict):
    """
    Directly inherited from dict.
    Accessible by attribute. o.x == o['x']
    This works also for all corner cases.
    Native json.dumps and json.loads work with it.

    Names like "keys", "update", "values" etc won't overwrite the methods,
    but will just be available using dict lookup notation obj['items']
    instead of obj.items.

    All key names are converted to snake_case.
    Hyphen's (-), dot's (.) or whitespaces are replaced by underscore (_).
    Autocomplete works even if the objects comes from a list.
    Recursive action. Dict assignments will be converted too.
    """
    __module__ = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        silent = kwargs.pop("silent", False)
        _ = dict(*args, **kwargs)

        super().__setattr__("__dict__", self)
        for k, v in _.items():
            _check_key(k, self, False, silent)
            super().__setitem__(k, _wrap(self.__class__, v))

    def __setitem__(self, key, value):
        super().__setitem__(key, _wrap(self.__class__, value))

    def __setattr__(self, key, value):
        super().__setitem__(key, _wrap(self.__class__, value))

    def __getattribute__(self, attribute):
        if attribute in self:
            return self[attribute]
        if not _check_key(attribute, self, True, silent=True):
            return getattr(super(), attribute)
        return object.__getattribute__(self, attribute)


def _wrap(cls, v):
    if isinstance(v, _Mapping):
        v = cls(v)
    elif isinstance(v, _Sequence) and not isinstance(
        v, (str, bytes, bytearray, set, tuple)
    ):
        v = list([_wrap(cls, x) for x in v])
    return v


_warning_names = (
    "items",
    "keys",
    "values",
    "update",
    "clear",
    "copy",
    "fromkeys",
    "get",
    "items",
    "keys",
    "pop",
    "popitem",
    "setdefault",
    "update",
    "values",
    "class",
)

_warning_names_message = """\n\
    While creating a ContraDict object, a key offending key name '{0}'
    has been found, which might behave unexpected.
    You will only be able to look it up using key,
    eg. myobject['{0}']. myobject.{0} will not work with that name."""


def _check_key(
    key: str, mapping: _Mapping, boolean: bool = False, silent=False
):
    """Checks `key` and warns if needed.
    :param key:
    :param boolean: return True or False instead of passthrough
    """
    e = None
    if not isinstance(key, (str,)):
        if boolean:
            return True
        return key
    if key.lower() in _warning_names or any(_ in key for _ in ("-", ".")):
        if not silent:
            _warnings.warn(_warning_names_message.format(key))
        e = True
    if not boolean:
        return key
    return not e
