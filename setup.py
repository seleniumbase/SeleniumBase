"""
The setup package to install SeleniumBase dependencies and plugins
(Uses selenium 3.x and is compatible with Python 2.7+ and Python 3.5+)
"""

from setuptools import setup, find_packages  # noqa
import os
import sys


this_directory = os.path.abspath(os.path.dirname(__file__))
long_description = None
try:
    with open(os.path.join(this_directory, 'README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
except IOError:
    long_description = 'Reliable Browser Automation & Testing Framework'

if sys.argv[-1] == 'publish':
    reply = None
    input_method = input
    if not sys.version_info[0] >= 3:
        input_method = raw_input  # noqa
    reply = str(input_method(
        '>>> Confirm release PUBLISH to PyPI? (yes/no): ')).lower().strip()
    if reply == 'yes':
        print("\n*** Checking code health with flake8:\n")
        flake8_status = os.system("flake8 --exclude=temp")
        if flake8_status != 0:
            print("\nWARNING! Fix flake8 issues before publishing to PyPI!\n")
            sys.exit()
        else:
            print("*** No flake8 issues detected. Continuing...")
        print("\n*** Rebuilding distribution packages: ***\n")
        os.system('rm -f dist/*.egg; rm -f dist/*.tar.gz; rm -f dist/*.whl')
        os.system('python setup.py sdist bdist_wheel')  # Create new tar/wheel
        print("\n*** Installing twine: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install 'twine>=1.15.0'")
        print("\n*** Publishing The Release to PyPI: ***\n")
        os.system('python -m twine upload dist/*')  # Requires ~/.pypirc Keys
        print("\n*** The Release was PUBLISHED SUCCESSFULLY to PyPI! :) ***\n")
    else:
        print("\n>>> The Release was NOT PUBLISHED to PyPI! <<<\n")
    sys.exit()

setup(
    name='seleniumbase',
    version='1.34.7',
    description='Fast, Easy, and Reliable Browser Automation & Testing.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seleniumbase/SeleniumBase',
    platforms=["Windows", "Linux", "Unix", "Mac OS-X"],
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Framework :: Pytest",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        'pip>=19.3.1',  # >= 19.3.1 required for Python 3.8+
        'setuptools',
        'setuptools-scm',
        'wheel',
        'six',
        'nose',
        'ipdb',
        'idna==2.8',  # Must stay in sync with "requests"
        'chardet==3.0.4',  # Must stay in sync with "requests"
        'urllib3==1.25.7',  # Must stay in sync with "requests"
        'requests==2.22.0',
        'selenium==3.141.0',
        'pluggy>=0.13.1',
        'attrs>=19.3.0',
        'pytest>=4.6.8;python_version<"3"',  # For Python 2 compatibility
        'pytest>=5.3.2;python_version>="3"',
        'pytest-cov>=2.8.1',
        'pytest-forked>=1.1.3',
        'pytest-html==1.22.1;python_version<"3.6"',
        'pytest-html==2.0.1;python_version>="3.6"',
        'pytest-metadata>=1.8.0',
        'pytest-ordering>=0.6',
        'pytest-rerunfailures>=8.0',
        'pytest-timeout>=1.3.3',
        'pytest-xdist>=1.31.0',
        'parameterized>=0.7.1',
        'soupsieve==1.9.5',
        'beautifulsoup4==4.8.2',
        'atomicwrites==1.3.0',
        'portalocker==1.5.2',
        'cryptography==2.8',
        'asn1crypto==1.2.0',
        'pyopenssl==19.1.0',
        'pygments>=2.5.2',
        'colorama==0.4.3',
        'coverage>=5.0.1',
        'pymysql==0.9.3',
        'pyotp==2.3.0',
        'boto==2.49.0',
        'cffi>=1.13.2',
        'tqdm>=4.41.0',
        'flake8==3.7.9',
        'certifi>=2019.11.28',
        'pdfminer.six==20191110',
    ],
    packages=[
        'seleniumbase',
        'seleniumbase.common',
        'seleniumbase.config',
        'seleniumbase.console_scripts',
        'seleniumbase.core',
        'seleniumbase.drivers',
        'seleniumbase.extensions',
        'seleniumbase.fixtures',
        'seleniumbase.masterqa',
        'seleniumbase.plugins',
        'seleniumbase.utilities',
        'seleniumbase.utilities.selenium_grid',
        'seleniumbase.utilities.selenium_ide',
        'seleniumbase.virtual_display',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'seleniumbase = seleniumbase.console_scripts.run:main',
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
