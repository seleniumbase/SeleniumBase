"""
The setup package to install the SeleniumBase Test Framework plugins
on a development machine that DOES NOT intend to write to
a MySQL DB during test runs.
"""

from setuptools import setup, find_packages

setup(
    name = 'seleniumbase',
    version = '1.1.2',
    author = 'Michael Mintz',
    author_email = '@mintzworld',
    maintainer = 'Michael Mintz',
    description = 'The SeleniumBase Test Framework. (Powered by Python, WebDriver, and more...)',
    license = 'The MIT License',
    packages = ['test_framework',
                'test_framework.core',
                'test_framework.plugins',
                'test_framework.fixtures',
                'test_framework.common',
                'test_framework.config'],
    entry_points = {
        'nose.plugins': [
            'base_plugin = test_framework.plugins.base_plugin:Base',
            'selenium = test_framework.plugins.selenium_plugin:SeleniumBrowser',
            'page_source = test_framework.plugins.page_source:PageSource',
            'screen_shots = test_framework.plugins.screen_shots:ScreenShots',
            'test_info = test_framework.plugins.basic_test_info:BasicTestInfo',
            's3_logging = test_framework.plugins.s3_logging_plugin:S3Logging',
            'hipchat_reporting = test_framework.plugins.hipchat_reporting_plugin:HipchatReporting',
            ]
        }
    )
