"""
The setup package to install SeleniumBase dependencies and plugins
(Uses selenium 3.x and is compatible with Python 2.7+ and Python 3.6+)
"""

from setuptools import setup, find_packages  # noqa

setup(
    name='seleniumbase',
    version='1.13.3',
    description='Web Automation & Testing Framework - http://seleniumbase.com',
    long_description='Web Automation and Testing Framework - seleniumbase.com',
    platforms='Mac * Windows * Linux * Docker',
    url='http://seleniumbase.com',
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    license='The MIT License',
    install_requires=[
        'pip',
        'setuptools',
        'ipython==5.6.0',
        'selenium==3.11.0',
        'nose==1.3.7',
        'pytest==3.6.3',
        'pytest-html==1.19.0',
        'pytest-xdist==1.22.2',
        'six==1.11.0',
        'flake8==3.5.0',
        'requests==2.19.1',
        'beautifulsoup4==4.6.0',
        'unittest2==1.1.0',
        'chardet==3.0.4',
        'boto==2.48.0',
        'ipdb==0.11',
        'PyVirtualDisplay==0.2.1',
        ],
    packages=['seleniumbase',
              'seleniumbase.common',
              'seleniumbase.config',
              'seleniumbase.core',
              'seleniumbase.fixtures',
              'seleniumbase.masterqa',
              'seleniumbase.plugins',
              'console_scripts',
              'drivers',
              'integrations',
              'integrations.selenium_grid',
              'integrations.selenium_ide',
              ],
    entry_points={
        'console_scripts': [
            'seleniumbase = console_scripts.run:main',
        ],
        'nose.plugins': [
            'base_plugin = seleniumbase.plugins.base_plugin:Base',
            'selenium = seleniumbase.plugins.selenium_plugin:SeleniumBrowser',
            'page_source = seleniumbase.plugins.page_source:PageSource',
            'screen_shots = seleniumbase.plugins.screen_shots:ScreenShots',
            'test_info = seleniumbase.plugins.basic_test_info:BasicTestInfo',
            ('db_reporting = '
             'seleniumbase.plugins.db_reporting_plugin:DBReporting'),
            's3_logging = seleniumbase.plugins.s3_logging_plugin:S3Logging',
            ],
        'pytest11': ['seleniumbase = seleniumbase.plugins.pytest_plugin']
        }
    )

# print(os.system("cat seleniumbase.egg-info/PKG-INFO"))
print("\n*** SeleniumBase Installation Complete! ***\n")
