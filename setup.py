"""Setup steps for installing SeleniumBase dependencies and plugins.
(Uses selenium 4.x and is compatible with Python 3.7+)"""
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
    confirm_text = ">>> Confirm release PUBLISH to PyPI? (yes/no): "
    reply = str(input_method(confirm_text)).lower().strip()
    if reply == "yes":
        if sys.version_info < (3, 9):
            print("\nERROR! Publishing to PyPI requires Python>=3.9")
            sys.exit()
        print("\n*** Checking code health with flake8:\n")
        os.system("python -m pip install 'flake8==7.0.0'")
        flake8_status = os.system("flake8 --exclude=recordings,temp")
        if flake8_status != 0:
            print("\nERROR! Fix flake8 issues before publishing to PyPI!\n")
            sys.exit()
        else:
            print("*** No flake8 issues detected. Continuing...")
        print("\n*** Removing existing distribution packages: ***\n")
        os.system("rm -f dist/*.egg; rm -f dist/*.tar.gz; rm -f dist/*.whl")
        os.system("rm -rf build/bdist.*; rm -rf build/lib")
        print("\n*** Installing build: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'build'")
        print("\n*** Installing pkginfo: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'pkginfo'")
        print("\n*** Installing readme-renderer: *** (For PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'readme-renderer'")
        print("\n*** Installing jaraco.classes: *** (For PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'jaraco.classes'")
        print("\n*** Installing more-itertools: *** (For PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'more-itertools'")
        print("\n*** Installing zipp: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'zipp'")
        print("\n*** Installing importlib-metadata: *** (For PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'importlib-metadata'")
        print("\n*** Installing keyring, requests-toolbelt: *** (For PyPI)\n")
        os.system("python -m pip install --upgrade keyring requests-toolbelt")
        print("\n*** Installing twine: *** (Required for PyPI uploads)\n")
        os.system("python -m pip install --upgrade 'twine'")
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
    keywords=[
        "pytest",
        "selenium",
        "framework",
        "automation",
        "browser",
        "testing",
        "webdriver",
        "seleniumbase",
        "sbase",
        "crawling",
        "scraping",
    ],
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
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
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        'pip>=24.0',
        'packaging>=24.0',
        'setuptools>=68.0.0;python_version<"3.8"',
        'setuptools>=69.2.0;python_version>="3.8"',
        'wheel>=0.42.0;python_version<"3.8"',
        'wheel>=0.43.0;python_version>="3.8"',
        'attrs>=23.2.0',
        "certifi>=2024.2.2",
        'filelock>=3.12.2;python_version<"3.8"',
        'filelock>=3.13.3;python_version>="3.8"',
        'platformdirs>=4.0.0;python_version<"3.8"',
        'platformdirs>=4.2.0;python_version>="3.8"',
        'typing-extensions>=4.11.0;python_version>="3.8"',
        'parse>=1.20.1',
        'parse-type>=0.6.2',
        'pyyaml>=6.0.1',
        "six==1.16.0",
        "idna==3.6",
        'chardet==5.2.0',
        'charset-normalizer==3.3.2',
        'urllib3>=1.26.18,<2;python_version<"3.10"',
        'urllib3>=1.26.18,<2.3.0;python_version>="3.10"',
        'requests==2.31.0',
        "pynose==1.5.1",
        'sniffio==1.3.1',
        'h11==0.14.0',
        'outcome==1.3.0.post0',
        'trio==0.22.2;python_version<"3.8"',
        'trio==0.25.0;python_version>="3.8"',
        'trio-websocket==0.11.1',
        'wsproto==1.2.0',
        'selenium==4.11.2;python_version<"3.8"',
        'selenium==4.19.0;python_version>="3.8"',
        'cssselect==1.2.0',
        "sortedcontainers==2.4.0",
        'fasteners==0.19',
        'execnet==2.0.2;python_version<"3.8"',
        'execnet==2.1.0;python_version>="3.8"',
        'iniconfig==2.0.0',
        'pluggy==1.2.0;python_version<"3.8"',
        'pluggy==1.4.0;python_version>="3.8"',
        "py==1.11.0",
        'pytest==7.4.4;python_version<"3.8"',
        'pytest==8.1.1;python_version>="3.8"',
        "pytest-html==2.0.1",  # Newer ones had issues
        'pytest-metadata==3.0.0;python_version<"3.8"',
        'pytest-metadata==3.1.1;python_version>="3.8"',
        "pytest-ordering==0.6",
        'pytest-rerunfailures==13.0;python_version<"3.8"',
        'pytest-rerunfailures==14.0;python_version>="3.8"',
        'pytest-xdist==3.5.0',
        'parameterized==0.9.0',
        "sbvirtualdisplay==1.3.0",
        "behave==1.2.6",
        'soupsieve==2.4.1;python_version<"3.8"',
        'soupsieve==2.5;python_version>="3.8"',
        "beautifulsoup4==4.12.3",
        'pygments==2.17.2',
        'pyreadline3==3.4.1;platform_system=="Windows"',
        "tabcompleter==1.3.0",
        "pdbp==1.5.0",
        'colorama==0.4.6',
        'exceptiongroup==1.2.0',
        'pyotp==2.9.0',
        'markdown-it-py==2.2.0;python_version<"3.8"',
        'markdown-it-py==3.0.0;python_version>="3.8"',
        'mdurl==0.1.2',
        'rich==13.7.1',
    ],
    extras_require={
        # pip install -e .[allure]
        # Usage: pytest --alluredir=allure_results
        # Serve: allure serve allure_results
        "allure": [
            'allure-pytest>=2.13.5',
            'allure-python-commons>=2.13.5',
            'allure-behave>=2.13.5',
        ],
        # pip install -e .[coverage]
        # Usage: coverage run -m pytest; coverage html; coverage report
        "coverage": [
            'coverage==7.2.7;python_version<"3.8"',
            'coverage>=7.4.4;python_version>="3.8"',
            'pytest-cov==4.1.0;python_version<"3.8"',
            'pytest-cov>=5.0.0;python_version>="3.8"',
        ],
        # pip install -e .[flake8]
        # Usage: flake8
        "flake8": [
            'flake8==5.0.4;python_version<"3.9"',
            'flake8==7.0.0;python_version>="3.9"',
            "mccabe==0.7.0",
            'pyflakes==2.5.0;python_version<"3.9"',
            'pyflakes==3.2.0;python_version>="3.9"',
            'pycodestyle==2.9.1;python_version<"3.9"',
            'pycodestyle==2.11.1;python_version>="3.9"',
        ],
        # pip install -e .[ipdb]
        # (Not needed for debugging anymore. SeleniumBase now includes "pdbp".)
        "ipdb": [
            "ipdb==0.13.13",
            'ipython==7.34.0',
        ],
        # pip install -e .[pdfminer]
        # (An optional library for parsing PDF files.)
        "pdfminer": [
            'pdfminer.six==20221105;python_version<"3.8"',
            'pdfminer.six==20231228;python_version>="3.8"',
            'cryptography==39.0.2;python_version<"3.9"',
            'cryptography==42.0.5;python_version>="3.9"',
            'cffi==1.15.1;python_version<"3.8"',
            'cffi==1.16.0;python_version>="3.8"',
            "pycparser==2.22",
        ],
        # pip install -e .[pillow]
        # (An optional library for image-processing.)
        "pillow": [
            'Pillow==9.5.0;python_version<"3.8"',
            'Pillow>=10.3.0;python_version>="3.8"',
        ],
        # pip install -e .[pip-system-certs]
        # (If you see [SSL: CERTIFICATE_VERIFY_FAILED], then get this.)
        # (May help those with corporate self-signed certs on Windows.)
        "pip-system-certs": [
            'pip-system-certs==4.0;platform_system=="Windows"',
        ],
        # pip install -e .[proxy]
        # Usage: proxy
        # (That starts a proxy server on "127.0.0.1:8899".)
        "proxy": [
            "proxy.py==2.4.3",
        ],
        # pip install -e .[psutil]
        "psutil": [
            "psutil==5.9.8",
        ],
        # pip install -e .[selenium-stealth]
        "selenium-stealth": [
            'selenium-stealth==1.0.6',
        ],
        # pip install -e .[selenium-wire]
        "selenium-wire": [
            'selenium-wire==5.1.0',
            'Brotli==1.1.0',
            'blinker==1.7.0',
            'h2==4.1.0',
            'hpack==4.0.0',
            'hyperframe==6.0.1',
            'kaitaistruct==0.10',
            'pyasn1==0.5.1',
            'zstandard==0.22.0',
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
