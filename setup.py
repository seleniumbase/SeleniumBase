"""
The setup package to install SeleniumBase dependencies and plugins.
(Uses selenium 3.x and is compatible with Python 2.7+ and Python 3.5+)
"""

from setuptools import setup, find_packages  # noqa: F401
import os
import sys


this_dir = os.path.abspath(os.path.dirname(__file__))
long_description = None
total_description = None
try:
    with open(os.path.join(this_dir, "README.md"), "rb") as f:
        total_description = f.read().decode("utf-8")
    description_lines = total_description.split("\n")
    long_description_lines = []
    for line in description_lines:
        if not line.startswith("<meta ") and not line.startswith("<link "):
            long_description_lines.append(line)
    long_description = "\n".join(long_description_lines)
except IOError:
    long_description = "A complete library for building end-to-end tests."
about = {}
# Get the package version from the seleniumbase/__version__.py file
with open(os.path.join(this_dir, "seleniumbase", "__version__.py"), "rb") as f:
    exec(f.read().decode("utf-8"), about)

if sys.argv[-1] == "publish":
    reply = None
    input_method = input
    if not sys.version_info[0] >= 3:
        input_method = raw_input  # noqa: F821
    confirm_text = ">>> Confirm release PUBLISH to PyPI? (yes/no): "
    reply = str(input_method(confirm_text)).lower().strip()
    if reply == "yes":
        print("\n*** Checking code health with flake8:\n")
        os.system("python -m pip install 'flake8==4.0.1'")
        flake8_status = os.system("flake8 --exclude=recordings,temp")
        if flake8_status != 0:
            print("\nWARNING! Fix flake8 issues before publishing to PyPI!\n")
            sys.exit()
        else:
            print("*** No flake8 issues detected. Continuing...")
        print("\n*** Rebuilding distribution packages: ***\n")
        os.system("rm -f dist/*.egg; rm -f dist/*.tar.gz; rm -f dist/*.whl")
        os.system("rm -rf build/bdist.*; rm -rf build/lib")
        os.system("python setup.py sdist bdist_wheel")  # Create new tar/wheel
        print("\n*** Installing twine: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'twine>=1.15.0'")
        print("\n*** Installing tqdm: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'tqdm>=4.62.3'")
        print("\n*** Publishing The Release to PyPI: ***\n")
        os.system("python -m twine upload dist/*")  # Requires ~/.pypirc Keys
        print("\n*** The Release was PUBLISHED SUCCESSFULLY to PyPI! :) ***\n")
    else:
        print("\n>>> The Release was NOT PUBLISHED to PyPI! <<<\n")
    sys.exit()

setup(
    name="seleniumbase",
    version=about["__version__"],
    description="A complete web automation framework for end-to-end testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seleniumbase/SeleniumBase",
    project_urls={
        "Changelog": "https://github.com/seleniumbase/SeleniumBase/releases",
        "Download": "https://pypi.org/project/seleniumbase/#files",
        "Gitter": "https://gitter.im/seleniumbase/SeleniumBase",
        "Slack": "https://app.slack.com/client/T0ABCRTNX/C01SM888REZ",
        "Blog": "https://seleniumbase.com/",
        "PyPI": "https://pypi.org/project/seleniumbase/",
        "Source": "https://github.com/seleniumbase/SeleniumBase",
        "Documentation": "https://seleniumbase.io/",
    },
    platforms=["Windows", "Linux", "Mac OS-X"],
    author="Michael Mintz",
    author_email="mdmintz@gmail.com",
    maintainer="Michael Mintz",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: Web Environment",
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
        "Programming Language :: Python :: 3.10",
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
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[
        'pip>=20.3.4;python_version<"3.6"',
        'pip>=21.3;python_version>="3.6"',
        'packaging>=20.9;python_version<"3.6"',
        'packaging>=21.0;python_version>="3.6"',
        "typing-extensions>=3.10.0.2",
        'setuptools>=44.1.1;python_version<"3.5"',
        'setuptools>=50.3.2;python_version>="3.5" and python_version<"3.6"',
        'setuptools>=58.2.0;python_version>="3.6"',
        'setuptools-scm==5.0.2;python_version<"3.6"',
        'setuptools-scm>=6.3.2;python_version>="3.6"',
        'tomli>=1.2.1;python_version>="3.6"',
        "wheel>=0.37.0",
        "attrs>=21.2.0",
        'PyYAML>=6.0;python_version>="3.6"',
        "sortedcontainers==2.4.0",
        "certifi>=2021.10.8",
        "six==1.16.0",
        "nose==1.3.7",
        'ipdb==0.13.4;python_version<"3.5"',
        'ipdb==0.13.9;python_version>="3.5"',
        'parso==0.7.1;python_version<"3.6"',
        'parso==0.8.2;python_version>="3.6"',
        'jedi==0.17.2;python_version<"3.6"',
        'jedi==0.18.0;python_version>="3.6"',
        'idna==2.10;python_version<"3.6"',  # Must stay in sync with "requests"
        'idna==3.3;python_version>="3.6"',  # Must stay in sync with "requests"
        'chardet==3.0.4;python_version<"3.5"',  # Stay in sync with "requests"
        'chardet==4.0.0;python_version>="3.5"',  # Stay in sync with "requests"
        'charset-normalizer==2.0.7;python_version>="3.5"',  # Sync "requests"
        "urllib3==1.26.7",  # Must stay in sync with "requests"
        'requests==2.26.0;python_version<"3.5"',
        'requests==2.25.1;python_version>="3.5" and python_version<"3.6"',
        'requests==2.26.0;python_version>="3.6"',
        "selenium==3.141.0",
        'msedge-selenium-tools==3.141.3;python_version<"3.7"',
        'more-itertools==5.0.0;python_version<"3.5"',
        'more-itertools==8.10.0;python_version>="3.5"',
        "cssselect==1.1.0",
        'filelock==3.2.1;python_version<"3.6"',
        'filelock==3.3.1;python_version>="3.6"',
        'fasteners==0.16;python_version<"3.5"',
        'fasteners==0.16.3;python_version>="3.5"',
        "execnet==1.9.0",
        'pluggy==0.13.1;python_version<"3.6"',
        'pluggy==1.0.0;python_version>="3.6"',
        'py==1.8.1;python_version<"3.5"',
        'py==1.10.0;python_version>="3.5"',
        'pytest==4.6.11;python_version<"3.5"',
        'pytest==6.1.2;python_version>="3.5" and python_version<"3.6"',
        'pytest==6.2.5;python_version>="3.6"',
        "pytest-forked==1.3.0",
        'pytest-html==1.22.1;python_version<"3.6"',
        'pytest-html==2.0.1;python_version>="3.6"',  # Newer ones had issues
        'pytest-metadata==1.8.0;python_version<"3.6"',
        'pytest-metadata==1.11.0;python_version>="3.6"',
        "pytest-ordering==0.6",
        'pytest-rerunfailures==8.0;python_version<"3.5"',
        'pytest-rerunfailures==9.1.1;python_version>="3.5" and python_version<"3.6"',  # noqa: E501
        'pytest-rerunfailures==10.2;python_version>="3.6"',
        'pytest-xdist==1.34.0;python_version<"3.5"',
        'pytest-xdist==2.2.1;python_version>="3.5" and python_version<"3.6"',
        'pytest-xdist==2.4.0;python_version>="3.6"',
        "parameterized==0.8.1",
        "sbvirtualdisplay==1.0.0",
        'soupsieve==1.9.6;python_version<"3.5"',
        'soupsieve==2.1;python_version>="3.5" and python_version<"3.6"',
        'soupsieve==2.2.1;python_version>="3.6"',
        'beautifulsoup4==4.9.3;python_version<"3.5"',
        'beautifulsoup4==4.10.0;python_version>="3.5"',
        'cryptography==2.9.2;python_version<"3.5"',
        'cryptography==3.2.1;python_version>="3.5" and python_version<"3.6"',
        'cryptography==3.4.8;python_version>="3.6" and python_version<"3.7"',
        'cryptography==35.0.0;python_version>="3.7"',
        'pygments==2.5.2;python_version<"3.5"',
        'pygments==2.10.0;python_version>="3.5"',
        'traitlets==4.3.3;python_version<"3.7"',
        'traitlets==5.1.0;python_version>="3.7"',
        'prompt-toolkit==1.0.18;python_version<"3.5"',
        'prompt-toolkit==2.0.10;python_version>="3.5" and python_version<"3.6.2"',  # noqa: E501
        'prompt-toolkit==3.0.20;python_version>="3.6.2"',
        'decorator==4.4.2;python_version<"3.5"',
        'decorator==5.1.0;python_version>="3.5"',
        'ipython==5.10.0;python_version<"3.5"',
        'ipython==7.9.0;python_version>="3.5" and python_version<"3.6"',
        'ipython==7.16.1;python_version>="3.6" and python_version<"3.7"',
        'ipython==7.28.0;python_version>="3.7"',  # Requires matplotlib-inline
        'matplotlib-inline==0.1.3;python_version>="3.7"',  # ipython needs this
        "colorama==0.4.4",
        'platformdirs==2.0.2;python_version<"3.6"',
        'platformdirs==2.4.0;python_version>="3.6"',
        'pathlib2==2.3.5;python_version<"3.5"',  # Sync with "virtualenv"
        'importlib-metadata==2.0.0;python_version<"3.5"',
        'importlib-metadata==2.1.1;python_version>="3.5" and python_version<"3.6"',  # noqa: E501
        "virtualenv>=20.8.1",  # Sync with importlib-metadata and pathlib2
        'pymysql==0.10.1;python_version<"3.6"',
        'pymysql==1.0.2;python_version>="3.6"',
        "pyotp==2.6.0",
        "boto==2.49.0",
        "cffi==1.15.0",
        "toml==0.10.2",
        'Pillow==6.2.2;python_version<"3.5"',
        'Pillow==7.2.0;python_version>="3.5" and python_version<"3.6"',
        'Pillow==8.4.0;python_version>="3.6"',
        'rich==10.12.0;python_version>="3.6" and python_version<"4.0"',
        'tornado==5.1.1;python_version<"3.5"',
        'tornado==6.1;python_version>="3.5"',
        'pdfminer.six==20191110;python_version<"3.5"',
        'pdfminer.six==20201018;python_version>="3.5" and python_version<"3.6"',  # noqa: E501
        'pdfminer.six==20211012;python_version>="3.6"',
    ],
    extras_require={
        # pip install -e .[coverage]
        "coverage": [
            'coverage==5.5;python_version<"3.6"',
            'coverage==6.0.2;python_version>="3.6"',
            'pytest-cov==2.12.1;python_version<"3.6"',
            'pytest-cov==3.0.0;python_version>="3.6"',
        ],
        # pip install -e .[flake]
        "flake": [
            'flake8==3.7.9;python_version<"3.5"',
            'flake8==3.9.2;python_version>="3.5" and python_version<"3.6"',
            'flake8==4.0.1;python_version>="3.6"',
            'pyflakes==2.1.1;python_version<"3.5"',
            'pyflakes==2.3.1;python_version>="3.5" and python_version<"3.6"',
            'pyflakes==2.4.0;python_version>="3.6"',
            'pycodestyle==2.5.0;python_version<"3.5"',
            'pycodestyle==2.7.0;python_version>="3.5" and python_version<"3.6"',  # noqa: E501
            'pycodestyle==2.8.0;python_version>="3.6"',
        ],
    },
    packages=[
        "seleniumbase",
        "sbase",
        "seleniumbase.common",
        "seleniumbase.config",
        "seleniumbase.console_scripts",
        "seleniumbase.core",
        "seleniumbase.drivers",
        "seleniumbase.extensions",
        "seleniumbase.fixtures",
        "seleniumbase.js_code",
        "seleniumbase.masterqa",
        "seleniumbase.plugins",
        "seleniumbase.translate",
        "seleniumbase.utilities",
        "seleniumbase.utilities.selenium_grid",
        "seleniumbase.utilities.selenium_ide",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "seleniumbase = seleniumbase.console_scripts.run:main",
            "sbase = seleniumbase.console_scripts.run:main",  # Simplified name
        ],
        "nose.plugins": [
            "base_plugin = seleniumbase.plugins.base_plugin:Base",
            "selenium = seleniumbase.plugins.selenium_plugin:SeleniumBrowser",
            "page_source = seleniumbase.plugins.page_source:PageSource",
            "screen_shots = seleniumbase.plugins.screen_shots:ScreenShots",
            "test_info = seleniumbase.plugins.basic_test_info:BasicTestInfo",
            (
                "db_reporting = "
                "seleniumbase.plugins.db_reporting_plugin:DBReporting"
            ),
            "s3_logging = seleniumbase.plugins.s3_logging_plugin:S3Logging",
        ],
        "pytest11": ["seleniumbase = seleniumbase.plugins.pytest_plugin"],
    },
)

# print(os.system("cat seleniumbase.egg-info/PKG-INFO"))
print("\n*** SeleniumBase Installation Complete! ***\n")
