"""
The setup package to install the SeleniumSpot Test Framework plugins.
"""

from setuptools import setup, find_packages

REQUIREMENTS = [
    'python==2.7.6',
    'selenium==2.46.1',
    'nose==1.3.7',
    'requests==2.7.0',
    'urllib3==1.10.4',
    'BeautifulSoup==3.2.1',
    'unittest2==1.1.0',
    'chardet==2.3.0',
    'simplejson==3.7.3',
    'boto==2.38.0',
    'MySQL-python==1.2.5',
    'pdb==0.1',
    'ipdb==0.8.1'
]

setup(
    name = 'seleniumspot',
    version = '1.1.1',
    author = 'Michael Mintz',
    author_email = '@mintzworld',
    install_requires=REQUIREMENTS,
    maintainer = 'Michael Mintz',
    description = 'The SeleniumSpot Test Framework. (Powered by Python, WebDriver, and more...)',
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
