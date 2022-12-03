"""
The setup package to install SeleniumBase dependencies and plugins.
(Uses selenium 4.x and is compatible with Python 2.7+ and Python 3.6+)
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
        os.system("python -m pip install 'flake8==5.0.4'")
        flake8_status = os.system("flake8 --exclude=recordings,temp")
        if flake8_status != 0:
            print("\nWARNING! Fix flake8 issues before publishing to PyPI!\n")
            sys.exit()
        else:
            print("*** No flake8 issues detected. Continuing...")
        print("\n*** Removing existing distribution packages: ***\n")
        os.system("rm -f dist/*.egg; rm -f dist/*.tar.gz; rm -f dist/*.whl")
        os.system("rm -rf build/bdist.*; rm -rf build/lib")
        print("\n*** Installing build: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'build>=0.9.0'")
        print("\n*** Installing twine: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'twine>=4.0.2'")
        print("\n*** Installing tqdm: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade tqdm")
        print("\n*** Rebuilding distribution packages: ***\n")
        os.system("python -m build")  # Create new tar/wheel
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
    keywords="pytest automation selenium browser testing webdriver sbase",
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: Utilities",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",  # noqa: E501
    install_requires=[
        'pip>=20.3.4;python_version<"3.6"',
        'pip>=21.3.1;python_version>="3.6" and python_version<"3.7"',
        'pip>=22.3.1;python_version>="3.7"',
        'packaging>=20.9;python_version<"3.6"',
        'packaging>=21.3;python_version>="3.6"',
        'setuptools>=44.1.1;python_version<"3.6"',
        'setuptools>=59.6.0;python_version>="3.6" and python_version<"3.7"',
        'setuptools>=65.6.3;python_version>="3.7"',
        'tomli>=1.2.3;python_version>="3.6" and python_version<"3.7"',
        'tomli>=2.0.1;python_version>="3.7"',
        "tqdm>=4.64.1",
        'wheel>=0.37.1;python_version<"3.7"',
        'wheel>=0.38.4;python_version>="3.7"',
        'attrs>=21.4.0;python_version<"3.6"',
        'attrs>=22.1.0;python_version>="3.6"',
        'PyYAML>=6.0;python_version>="3.6"',
        'certifi>=2021.10.8;python_version<"3.6"',
        'certifi>=2022.9.24;python_version>="3.6"',
        'filelock>=3.2.1;python_version<"3.6"',
        'filelock>=3.4.1;python_version>="3.6" and python_version<"3.7"',
        'filelock>=3.8.0;python_version>="3.7"',
        'platformdirs>=2.0.2;python_version<"3.6"',
        'platformdirs>=2.4.0;python_version>="3.6" and python_version<"3.7"',
        'platformdirs>=2.5.4;python_version>="3.7"',
        'pyparsing>=2.4.7;python_version<"3.6"',
        'pyparsing>=3.0.7;python_version>="3.6" and python_version<"3.7"',
        'pyparsing>=3.0.9;python_version>="3.7"',
        "six==1.16.0",
        'idna==2.10;python_version<"3.6"',  # Must stay in sync with "requests"
        'idna==3.4;python_version>="3.6"',  # Must stay in sync with "requests"
        'chardet==3.0.4;python_version<"3.6"',  # Stay in sync with "requests"
        'chardet==4.0.0;python_version>="3.6" and python_version<"3.7"',
        'chardet==5.1.0;python_version>="3.7"',  # Stay in sync with "requests"
        'charset-normalizer==2.0.12;python_version>="3.6" and python_version<"3.7"',  # noqa: E501
        'charset-normalizer==2.1.1;python_version>="3.7"',  # Sync "requests"
        'urllib3==1.26.12;python_version<"3.7"',
        'urllib3==1.26.13;python_version>="3.7"',
        'requests==2.27.1;python_version<"3.7"',
        'requests==2.28.1;python_version>="3.7"',
        'requests-toolbelt==0.10.1',
        "nose==1.3.7",
        'sniffio==1.3.0;python_version>="3.7"',
        'h11==0.14.0;python_version>="3.7"',
        'outcome==1.2.0;python_version>="3.7"',
        'trio==0.22.0;python_version>="3.7"',
        'trio-websocket==0.9.2;python_version>="3.7"',
        'websockets==10.4;python_version>="3.7"',
        'pyopenssl==22.1.0;python_version>="3.7"',
        'wsproto==1.2.0;python_version>="3.7"',
        'selenium==3.141.0;python_version<"3.7"',
        'selenium==4.7.2;python_version>="3.7"',
        'msedge-selenium-tools==3.141.3;python_version<"3.7"',
        'more-itertools==5.0.0;python_version<"3.6"',
        'more-itertools==8.14.0;python_version>="3.6" and python_version<"3.7"',  # noqa: E501
        'more-itertools==9.0.0;python_version>="3.7"',
        'cssselect==1.1.0;python_version<"3.7"',
        'cssselect==1.2.0;python_version>="3.7"',
        "sortedcontainers==2.4.0",
        'fasteners==0.16;python_version<"3.6"',
        'fasteners==0.17.3;python_version>="3.6" and python_version<"3.7"',
        'fasteners==0.18;python_version>="3.7"',
        "execnet==1.9.0",
        'pluggy==0.13.1;python_version<"3.6"',
        'pluggy==1.0.0;python_version>="3.6"',
        'py==1.8.1;python_version<"3.6"',
        'py==1.11.0;python_version>="3.6"',
        'pytest==4.6.11;python_version<"3.6"',
        'pytest==7.0.1;python_version>="3.6" and python_version<"3.7"',
        'pytest==7.2.0;python_version>="3.7"',
        'pytest-forked==1.3.0;python_version<"3.6"',
        'pytest-forked==1.4.0;python_version>="3.6"',
        'pytest-html==1.22.1;python_version<"3.6"',
        'pytest-html==2.0.1;python_version>="3.6"',  # Newer ones had issues
        'pytest-metadata==1.8.0;python_version<"3.6"',
        'pytest-metadata==1.11.0;python_version>="3.6" and python_version<"3.7"',  # noqa: E501
        'pytest-metadata==2.0.4;python_version>="3.7"',
        "pytest-ordering==0.6",
        'pytest-rerunfailures==8.0;python_version<"3.6"',
        'pytest-rerunfailures==10.3;python_version>="3.6"',
        'pytest-xdist==1.34.0;python_version<"3.6"',
        'pytest-xdist==2.5.0;python_version>="3.6" and python_version<"3.7"',
        'pytest-xdist==3.0.2;python_version>="3.7"',
        "parameterized==0.8.1",
        "sbvirtualdisplay==1.1.1",
        "behave==1.2.6",
        "parse==1.19.0",
        "parse-type==0.6.0",
        'soupsieve==1.9.6;python_version<"3.6"',
        'soupsieve==2.3.2.post1;python_version>="3.6"',
        'beautifulsoup4==4.9.3;python_version<"3.6"',
        'beautifulsoup4==4.11.1;python_version>="3.6"',
        'cryptography==2.9.2;python_version<"3.6"',
        'cryptography==36.0.2;python_version>="3.6" and python_version<"3.7"',
        'cryptography==38.0.4;python_version>="3.7"',
        'pygments==2.5.2;python_version<"3.6"',
        'pygments==2.13.0;python_version>="3.6"',
        'pyreadline==2.1;platform_system=="Windows" and python_version<"3.6"',
        'pyreadline3==3.4.1;platform_system=="Windows" and python_version>="3.6"',  # noqa: E501
        "pyrepl==0.9.0",
        "tabcompleter==1.0.0",
        "pdbp==1.2.3",
        'colorama==0.4.6;python_version<"3.6"',
        'colorama==0.4.5;python_version>="3.6" and python_version<"3.7"',
        'colorama==0.4.6;python_version>="3.7"',
        'exceptiongroup==1.0.4;python_version>="3.7"',
        'importlib-metadata==2.1.3;python_version<"3.6"',
        'importlib-metadata==4.2.0;python_version>="3.6" and python_version<"3.8"',  # noqa: E501
        "pycparser==2.21",
        'pyotp==2.3.0;python_version<"3.6"',
        'pyotp==2.7.0;python_version>="3.6"',
        "cffi==1.15.1",
        'typing-extensions==3.10.0.2;python_version<"3.6"',  # <3.9 for "rich"
        'typing-extensions==4.1.1;python_version>="3.6" and python_version<"3.7"',  # noqa: E501
        'typing-extensions==4.2.0;python_version>="3.7" and python_version<"3.9"',  # noqa: E501
        'rich==12.6.0;python_version>="3.6" and python_version<"4.0"',
    ],
    extras_require={
        # pip install -e .[coverage]
        # Usage: coverage run -m pytest; coverage html; coverage report
        "coverage": [
            'coverage==5.5;python_version<"3.6"',
            'coverage==6.2;python_version>="3.6" and python_version<"3.7"',
            'coverage==6.5.0;python_version>="3.7"',
            'pytest-cov==2.12.1;python_version<"3.6"',
            'pytest-cov==4.0.0;python_version>="3.6"',
        ],
        # pip install -e .[flake8]
        # Usage: flake8
        "flake8": [
            'flake8==3.7.9;python_version<"3.6"',
            'flake8==5.0.4;python_version>="3.6"',
            'mccabe==0.6.1;python_version<"3.6"',
            'mccabe==0.7.0;python_version>="3.6"',
            'pyflakes==2.1.1;python_version<"3.6"',
            'pyflakes==2.5.0;python_version>="3.6"',
            'pycodestyle==2.5.0;python_version<"3.6"',
            'pycodestyle==2.9.1;python_version>="3.6"',
        ],
        # pip install -e .[ipdb]
        "ipdb": [
            "ipdb==0.13.9",
            "ipython==7.34.0",
            "jedi==0.18.2",
            "parso==0.8.3",
        ],
        # pip install -e .[pdfminer]
        "pdfminer": [
            'pdfminer.six==20191110;python_version<"3.6"',
            'pdfminer.six==20211012;python_version>="3.6" and python_version<"3.7"',  # noqa: E501
            'pdfminer.six==20221105;python_version>="3.7"',
        ],
        # pip install -e .[pillow]
        "pillow": [
            'Pillow==6.2.2;python_version<"3.6"',
            'Pillow==8.4.0;python_version>="3.6" and python_version<"3.7"',
            'Pillow==9.3.0;python_version>="3.7"',
        ],
        # pip install -e .[psutil]
        "psutil": [
            "psutil==5.9.3",
        ],
        # pip install -e .[selenium-wire]
        "selenium-wire": [
            'selenium-wire==5.1.0;python_version>="3.7"',
            'Brotli==1.0.9;python_version>="3.7"',
            'blinker==1.5;python_version>="3.7"',
            'h2==4.1.0;python_version>="3.7"',
            'hpack==4.0.0;python_version>="3.7"',
            'hyperframe==6.0.1;python_version>="3.7"',
            'kaitaistruct==0.10;python_version>="3.7"',
            'pyasn1==0.4.8;python_version>="3.7"',
            'zstandard==0.19.0;python_version>="3.7"',
        ],
    },
    packages=[
        "seleniumbase",
        "sbase",
        "seleniumbase.behave",
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
        "seleniumbase.resources",
        "seleniumbase.translate",
        "seleniumbase.undetected",
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
