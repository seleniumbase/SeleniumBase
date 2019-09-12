'''Utility functions for xauth.'''
import os
import hashlib
from seleniumbase.virtual_display import easyprocess


class NotFoundError(Exception):
    '''Error when xauth was not found.'''
    pass


def is_installed():
    '''
    Return whether or not xauth is installed.
    '''
    try:
        easyprocess.EasyProcess(['xauth', '-h']).check_installed()
    except easyprocess.EasyProcessCheckInstalledError:
        return False
    else:
        return True


def generate_mcookie():
    '''
    Generate a cookie string suitable for xauth.
    '''
    data = os.urandom(16)  # 16 bytes = 128 bit
    return hashlib.md5(data).hexdigest()


def call(*args):
    '''
    Call xauth with the given args.
    '''
    easyprocess.EasyProcess(['xauth'] + list(args)).call()
