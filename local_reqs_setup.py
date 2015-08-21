"""
The setup package to install the SeleniumBase Test Framework plugins
on a development machine that DOES NOT intend to write to
a MySQL DB during test runs.
(Includes requirements installation without pip.)
"""

from setuptools import setup, find_packages

setup(
    name = 'seleniumbase',
    version = '1.1.5',
    author = 'Michael Mintz',
    author_email = '@mintzworld',
    maintainer = 'Michael Mintz',
    description = 'The SeleniumBase Test Framework. (Powered by Python, WebDriver, and more...)',
    license = 'The MIT License',
    install_requires = ['selenium==2.47.1',
                        'nose==1.3.7',
                        'requests==2.7.0',
                        'urllib3==1.10.4',
                        'BeautifulSoup==3.2.1',
                        'unittest2==1.1.0',
                        'chardet==2.3.0',
                        'simplejson==3.7.3',
                        'boto==2.38.0'],
    packages = ['seleniumbase',
                'seleniumbase.core',
                'seleniumbase.plugins',
                'seleniumbase.fixtures',
                'seleniumbase.common',
                'seleniumbase.config'],
    entry_points = {
        'nose.plugins': [
            'base_plugin = seleniumbase.plugins.base_plugin:Base',
            'selenium = seleniumbase.plugins.selenium_plugin:SeleniumBrowser',
            'page_source = seleniumbase.plugins.page_source:PageSource',
            'screen_shots = seleniumbase.plugins.screen_shots:ScreenShots',
            'test_info = seleniumbase.plugins.basic_test_info:BasicTestInfo',
            's3_logging = seleniumbase.plugins.s3_logging_plugin:S3Logging',
            'hipchat_reporting = seleniumbase.plugins.hipchat_reporting_plugin:HipchatReporting',
            ]
        }
    )
