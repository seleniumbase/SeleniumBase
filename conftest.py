""" This is the pytest configuration file """

from seleniumbase.fixtures import constants


def pytest_addoption(parser):
    parser.addoption('--browser', action="store",
                     dest='browser',
                     choices=constants.Browser.VERSION.keys(),
                     default=constants.Browser.FIREFOX,
                     help="""Specifies the web browser to use. Default = FireFox.
                          If you want to use Chrome, explicitly indicate that.
                          Example: (--browser=chrome)""")
    parse_args(parser)


def parse_args(config):
    browser = config._getparser().parse_known_args()[0].browser
    pytest_config = '.pytest_config'
    config_file = open(pytest_config, 'w+')
    config_file.write(browser)
    config_file.close()
