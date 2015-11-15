"""
The setup package to install the SeleniumBase Test Framework plugins
on a server machine (or a development machine that intends to write to
a MySQL DB during test runs).
"""

from setuptools import setup, find_packages

setup(
    name = 'seleniumbase',
    version = '1.1.7',
    author = 'Michael Mintz',
    author_email = '@mintzworld',
    maintainer = 'Michael Mintz',
    description = 'The SeleniumBase Test Framework. (Powered by Python, WebDriver, and more...)',
    license = 'The MIT License',
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
            'db_reporting = seleniumbase.plugins.db_reporting_plugin:DBReporting',
            's3_logging = seleniumbase.plugins.s3_logging_plugin:S3Logging',
            'hipchat_reporting = seleniumbase.plugins.hipchat_reporting_plugin:HipchatReporting',
            ]
        }
    )
