"""
The setup package to install SeleniumBase dependencies and plugins
"""

import os
from setuptools import setup, find_packages  # noqa

setup(
    name='seleniumbase',
    version='1.3.9',
    description='Test Automation Framework - seleniumbase.com',
    long_description='Automation Framework for Simple & Reliable Web Testing',
    platforms='Mac * Windows * Linux * Docker',
    url='http://seleniumbase.com',
    author='Michael Mintz',
    author_email='@mintzworld',
    maintainer='Michael Mintz',
    license='The MIT License',
    install_requires=[
        'pip>=9.0.1',
        'setuptools>=34.3.3',
        'selenium==3.3.1',
        'nose>=1.3.7',
        'pytest>=3.0.7',
        'six>=1.10.0',
        'flake8>=3.3.0',
        'requests>=2.13.0',
        'urllib3>=1.20',
        'BeautifulSoup>=3.2.1',
        'unittest2>=1.1.0',
        'chardet>=2.3.0',
        'boto>=2.46.1',
        'ipdb>=0.10.2',
        'pyvirtualdisplay>=0.2.1',
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
            ]
        }
    )

print(os.system("cat seleniumbase.egg-info/PKG-INFO"))
print("\n*** SeleniumBase Installation Complete! ***\n")
