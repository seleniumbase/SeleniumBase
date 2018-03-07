"""
The setup package to install SeleniumBase dependencies and plugins
(Uses the older Selenium 2.53.6 for compatibility reasons)
"""

import os
from setuptools import setup, find_packages  # noqa

setup(
    name='seleniumbase',
    version='1.7.2',
    description='Web Automation & Testing Framework - http://seleniumbase.com',
    long_description='Web Automation and Testing Framework - seleniumbase.com',
    platforms='Mac * Windows * Linux * Docker',
    url='http://seleniumbase.com',
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    license='The MIT License',
    install_requires=[
        'pip>=9.0.1',
        'setuptools>=38.5.1',
        'ipython==5.5.0',
        'selenium==2.53.6',
        'nose==1.3.7',
        'pytest==3.4.1',
        'pytest-html==1.16.1',
        'pytest-xdist==1.22.2',
        'six==1.10.0',
        'flake8==3.5.0',
        'requests==2.18.4',
        'BeautifulSoup4==4.6.0',
        'unittest2==1.1.0',
        'chardet==3.0.4',
        'boto==2.48.0',
        'ipdb==0.10.2',
        'pyvirtualdisplay==0.2.1',
        ],
    packages=['seleniumbase',
              'seleniumbase.core',
              'seleniumbase.plugins',
              'seleniumbase.fixtures',
              'seleniumbase.masterqa',
              'seleniumbase.common',
              'seleniumbase.config'],
    entry_points={
        'nose.plugins': [
            'base_plugin = seleniumbase.plugins.base_plugin:Base',
            'selenium = seleniumbase.plugins.selenium_plugin:SeleniumBrowser',
            'page_source = seleniumbase.plugins.page_source:PageSource',
            'screen_shots = seleniumbase.plugins.screen_shots:ScreenShots',
            'test_info = seleniumbase.plugins.basic_test_info:BasicTestInfo',
            ('db_reporting = '
             'seleniumbase.plugins.db_reporting_plugin:DBReporting'),
            's3_logging = seleniumbase.plugins.s3_logging_plugin:S3Logging',
            ('hipchat_reporting = seleniumbase.plugins'
             '.hipchat_reporting_plugin:HipchatReporting'),
            ],
        'pytest11': ['seleniumbase = seleniumbase.plugins.pytest_plugin']
        }
    )

print(os.system("cat seleniumbase.egg-info/PKG-INFO"))
print("\n*** SeleniumBase Installation Complete! ***\n")
