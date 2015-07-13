"""
The setup package to install the SeleniumSpot Test Framework plugins.
"""

from setuptools import setup, find_packages

setup(
    name = 'test_framework',
    version = '1.1.0',
    author = 'Michael Mintz',
    author_email = '@mintzworld',
    maintainer = 'Michael Mintz',
    description = 'The SeleniumSpot Test Framework. (Powered by Python, WebDriver, and more...)',
    license = 'The MIT License',
    packages = ['test_framework',
                'test_framework.core',
                'test_framework.plugins',
                'test_framework.fixtures'],
    entry_points = {
        'nose.plugins': [
            'base_plugin = test_framework.plugins.base_plugin:Base',
            'selenium = test_framework.plugins.selenium_plugin:SeleniumBase',
            'page_source = test_framework.plugins.page_source:PageSource',
            'screen_shots = test_framework.plugins.screen_shots:ScreenShots',
            'test_info = test_framework.plugins.basic_test_info:BasicTestInfo',
            'db_reporting = test_framework.plugins.db_reporting_plugin:DBReporting',
            's3_logging = test_framework.plugins.s3_logging_plugin:S3Logging',
            'hipchat_reporting = test_framework.plugins.hipchat_reporting_plugin:HipchatReporting',
            ]
        }
    )
