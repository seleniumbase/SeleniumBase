""" This is the pytest configuration file """

import os
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
                      help="Input if tests need to be run with a web browser.")


def pytest_configure(config):
    with_selenium = config.getoption('with_selenium')
    browser = config.getoption('browser')
    data = ''
    if config.getoption('data') is not None:
        data = config.getoption('data')
    # Create a temporary config file while tests are running
    pytest_config = '.pytest_config'
    config_file = open(pytest_config, 'w+')
    config_file.write("with_selenium:::%s\n" % with_selenium)
    config_file.write("browser:::%s\n" % browser)
    config_file.write("data:::%s\n" % data)
    config_file.close()


def pytest_unconfigure():
    pytest_config = '.pytest_config'
    if os.path.isfile(pytest_config):
        os.remove(pytest_config)


def pytest_runtest_setup():
    # A placeholder for a method that runs before every test with pytest
    pass


def pytest_runtest_teardown():
    # A placeholder for a method that runs after every test with pytest
    pass
