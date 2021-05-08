"""Utility functions for xauth."""
import os
import hashlib
from seleniumbase.virtual_display.easyprocess import EasyProcess


class NotFoundError(Exception):
    """Error when xauth was not found."""

    pass


def is_installed():
    """
    Return whether or not xauth is installed.
    """
    try:
        p = EasyProcess(["xauth", "-V"])
        p.enable_stdout_log = False
        p.enable_stderr_log = False
        p.call()
    except Exception:
        return False
    else:
        return True


def generate_mcookie():
    """
    Generate a cookie string suitable for xauth.
    """
    data = os.urandom(16)  # 16 bytes = 128 bit
    return hashlib.md5(data).hexdigest()


def call(*args):
    """
    Call xauth with the given args.
    """
    EasyProcess(["xauth"] + list(args)).call()
