"""
The setup package to install SeleniumBase dependencies and plugins
(Uses selenium 3.x and is compatible with Python 2.7+ and Python 3.5+)
"""

from setuptools import setup, find_packages  # noqa
import os
import sys


this_directory = os.path.abspath(os.path.dirname(__file__))
long_description = None
total_description = None
try:
    with open(os.path.join(this_directory, 'README.md'), 'rb') as f:
        total_description = f.read().decode('utf-8')
    description_lines = total_description.split('\n')
    long_description_lines = []
    for line in description_lines:
        if not line.startswith("<meta ") and not line.startswith("<link "):
            long_description_lines.append(line)
    long_description = "\n".join(long_description_lines)
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
        os.system("python -m pip install --upgrade 'twine>=1.15.0'")
        print("\n*** Installing tqdm: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'tqdm>=4.50.0'")
        print("\n*** Publishing The Release to PyPI: ***\n")
        os.system('python -m twine upload dist/*')  # Requires ~/.pypirc Keys
        print("\n*** The Release was PUBLISHED SUCCESSFULLY to PyPI! :) ***\n")
    else:
        print("\n>>> The Release was NOT PUBLISHED to PyPI! <<<\n")
    sys.exit()

setup(
    name='seleniumbase',
    version='1.49.25',
    description='A complete framework for Web-UI testing | seleniumbase.io',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seleniumbase/SeleniumBase',
    platforms=["Windows", "Linux", "Mac OS-X"],
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: Utilities",
    ],
    install_requires=[
        'pip>=20.2.3',
        'packaging>=20.4',
        'setuptools>=44.1.1;python_version<"3.5"',
        'setuptools>=50.3.0;python_version>="3.5"',
        'setuptools-scm',
        'wheel>=0.35.1',
        'six',
        'nose',
        'ipdb',
        'parso==0.7.1',  # The last version for Python 2 and 3.5
        'jedi==0.17.2',  # The last version for Python 2 and 3.5
        'idna==2.10',  # Must stay in sync with "requests"
        'chardet==3.0.4',  # Must stay in sync with "requests"
        'urllib3==1.25.10',  # Must stay in sync with "requests"
        'requests==2.24.0',
        'selenium==3.141.0',
        'msedge-selenium-tools==3.141.2',
        'more-itertools==5.0.0;python_version<"3.5"',
        'more-itertools==8.5.0;python_version>="3.5"',
        'cssselect==1.1.0',
        'pluggy==0.13.1',
        'attrs>=20.2.0',
        'py==1.8.1;python_version<"3.5"',
        'py==1.9.0;python_version>="3.5"',
        'pytest==4.6.11;python_version<"3.5"',
        'pytest==6.1.1;python_version>="3.5"',
        'pytest-cov==2.10.1',
        'pytest-forked==1.3.0',
        'pytest-html==1.22.1;python_version<"3.6"',
        'pytest-html==2.0.1;python_version>="3.6"',
        'pytest-metadata==1.8.0;python_version<"3.6"',
        'pytest-metadata==1.10.0;python_version>="3.6"',
        'pytest-ordering==0.6',
        'pytest-rerunfailures==8.0;python_version<"3.5"',
        'pytest-rerunfailures==9.1.1;python_version>="3.5"',
        'pytest-xdist==1.34.0;python_version<"3.5"',
        'pytest-xdist==2.1.0;python_version>="3.5"',
        'parameterized==0.7.4',
        'soupsieve==1.9.6;python_version<"3.5"',
        'soupsieve==2.0.1;python_version>="3.5"',
        'beautifulsoup4==4.9.3',
        'cryptography==3.0;python_version<"3.6"',
        'cryptography==3.1.1;python_version>="3.6"',
        'pyopenssl==19.1.0',
        'pygments==2.5.2;python_version<"3.5"',
        'pygments==2.7.1;python_version>="3.5"',
        'traitlets==4.3.3;python_version<"3.7"',
        'traitlets==5.0.4;python_version>="3.7"',
        'ipython==5.10.0;python_version<"3.5"',
        'prompt-toolkit==1.0.18;python_version<"3.6"',
        'prompt-toolkit==3.0.7;python_version>="3.6"',
        'ipython==6.5.0;python_version>="3.5" and python_version<"3.6"',
        'ipython==7.16.1;python_version>="3.6" and python_version<"3.7"',
        'ipython==7.18.1;python_version>="3.7"',
        'colorama==0.4.3',
        'pathlib2==2.3.5;python_version<"3.5"',  # Sync with "virtualenv"
        'importlib-metadata==2.0.0',  # Sync with "virtualenv"
        'virtualenv>=20.0.33',  # Sync with importlib-metadata and pathlib2
        'pymysql==0.10.1',
        'coverage==5.3',
        'brython==3.9.0',
        'pyotp==2.4.0',
        'boto==2.49.0',
        'cffi==1.14.3',
        'zipp==1.2.0;python_version<"3.6"',
        'zipp==3.3.0;python_version>="3.6"',
        'rich==8.0.0;python_version>="3.6" and python_version<"4.0"',
        'flake8==3.7.9;python_version<"3.5"',
        'flake8==3.8.4;python_version>="3.5"',
        'pyflakes==2.1.1;python_version<"3.5"',
        'pyflakes==2.2.0;python_version>="3.5"',
        'certifi>=2020.6.20',
        'allure-pytest==2.8.18',
        'pdfminer.six==20191110;python_version<"3.5"',
        'pdfminer.six==20200726;python_version>="3.5"',
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
        'seleniumbase.translate',
        'seleniumbase.utilities',
        'seleniumbase.utilities.selenium_grid',
        'seleniumbase.utilities.selenium_ide',
        'seleniumbase.virtual_display',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'seleniumbase = seleniumbase.console_scripts.run:main',
            'sbase = seleniumbase.console_scripts.run:main',  # Simplified name
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
