""" This is the pytest configuration file """

import os
import shutil
import time
from seleniumbase.config import settings
from seleniumbase.fixtures import constants


def pytest_addoption(parser):
    parser.addoption('--browser', action="store",
                     dest='browser',
                     choices=constants.Browser.VERSION.keys(),
                     default=constants.Browser.FIREFOX,
                     help="""Specifies the web browser to use. Default=FireFox.
                          If you want to use Chrome, explicitly indicate that.
                          Example: (--browser=chrome)""")
    parser.addoption('--is_pytest', action="store_true",
                     dest='is_pytest',
                     default=True,
                     help="""This is used by the BaseCase class to tell apart
                          pytest runs from nosetest runs.""")
    parser.addoption('--data', dest='data',
                     default=None,
                     help='Extra data to pass from the command line.')
    parser.addoption('--with-selenium', action="store_true",
                     dest='with_selenium',
                     default=False,
                     help="Use if tests need to be run with a web browser.")
    parser.addoption('--with-testing_base', action="store_true",
                     dest='with_testing_base',
                     default=False,
                     help="Use to save logs (screenshots) when tests fail.")
    parser.addoption('--log_path', dest='log_path',
                     default='logs/',
                     help='Where the log files are saved.')
    parser.addoption('--headless', action="store_true",
                     dest='headless',
                     default=False,
                     help="""Using this makes Webdriver run headlessly,
                          which is useful inside a Linux Docker.""")
    parser.addoption('--demo_mode', action="store_true",
                     dest='demo_mode',
                     default=False,
                     help="""Using this slows down the automation so that
                          you can see what it's actually doing.""")
    parser.addoption('--demo_sleep', action='store', dest='demo_sleep',
                     default=None,
                     help="""Setting this overrides the Demo Mode sleep
                          time that happens after browser actions.""")


def pytest_configure(config):
    with_selenium = config.getoption('with_selenium')
    with_testing_base = config.getoption('with_testing_base')
    browser = config.getoption('browser')
    log_path = config.getoption('log_path')
    headless = config.getoption('headless')
    demo_mode = config.getoption('demo_mode')
    demo_sleep = ''
    data = ''
    if config.getoption('demo_sleep') is not None:
        demo_sleep = config.getoption('demo_sleep')
    if config.getoption('data') is not None:
        data = config.getoption('data')
    # Create a temporary config file while tests are running
    pytest_config = '.pytest_config'
    config_file = open(pytest_config, 'w+')
    config_file.write("with_selenium:::%s\n" % with_selenium)
    config_file.write("browser:::%s\n" % browser)
    config_file.write("data:::%s\n" % data)
    config_file.write("with_testing_base:::%s\n" % with_testing_base)
    config_file.write("log_path:::%s\n" % log_path)
    config_file.write("headless:::%s\n" % headless)
    config_file.write("demo_mode:::%s\n" % demo_mode)
    config_file.write("demo_sleep:::%s\n" % demo_sleep)
    config_file.close()
    log_folder_setup(config)


def pytest_unconfigure():
    pytest_config = '.pytest_config'
    if os.path.isfile(pytest_config):
        os.remove(pytest_config)


def log_folder_setup(config):
    # Handle Logging
    with_testing_base = config.getoption('with_testing_base')
    if with_testing_base:
        log_path = config.getoption('log_path')
        if log_path.endswith("/"):
            log_path = log_path[:-1]
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        else:
            archived_folder = "%s/../archived_logs/" % log_path
            if not os.path.exists(archived_folder):
                os.makedirs(archived_folder)
            archived_logs = "%slogs_%s" % (archived_folder, int(time.time()))
            shutil.move(log_path, archived_logs)
            os.makedirs(log_path)
            if not settings.ARCHIVE_EXISTING_LOGS:
                shutil.rmtree(archived_logs)


def pytest_runtest_setup():
    # A placeholder for a method that runs before every test with pytest
    pass


def pytest_runtest_teardown():
    # A placeholder for a method that runs after every test with pytest
    pass
