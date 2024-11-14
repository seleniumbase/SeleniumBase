"""Setup steps for installing SeleniumBase dependencies and plugins.
(Uses selenium 4.x and is compatible with Python 3.8+)"""
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
        os.system("python -m pip install 'flake8==7.1.1'")
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
        os.system("python -m pip install 'pkginfo'")
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
        "Homepage": "https://github.com/seleniumbase/SeleniumBase",
        "Changelog": "https://github.com/seleniumbase/SeleniumBase/releases",
        "Download": "https://pypi.org/project/seleniumbase/#files",
        "Blog": "https://seleniumbase.com/",
        "Discord": "https://discord.gg/EdhQTn3EyE",
        "PyPI": "https://pypi.org/project/seleniumbase/",
        "Source": "https://github.com/seleniumbase/SeleniumBase",
        "Repository": "https://github.com/seleniumbase/SeleniumBase",
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
    python_requires=">=3.8",
    install_requires=[
        'pip>=24.2',
        'packaging>=24.2',
        'setuptools~=70.2;python_version<"3.10"',  # Newer ones had issues
        'setuptools>=75.5.0;python_version>="3.10"',
        'wheel>=0.45.0',
        'attrs>=24.2.0',
        "certifi>=2024.8.30",
        "exceptiongroup>=1.2.2",
        'websockets~=13.1;python_version<"3.9"',
        'websockets>=14.1;python_version>="3.9"',
        'filelock>=3.16.1',
        'fasteners>=0.19',
        "mycdp>=1.1.0",
        "pynose>=1.5.3",
        'platformdirs>=4.3.6',
        'typing-extensions>=4.12.2',
        "sbvirtualdisplay>=1.3.0",
        "six>=1.16.0",
        'parse>=1.20.2',
        'parse-type>=0.6.4',
        'colorama>=0.4.6',
        'pyyaml>=6.0.2',
        'pygments>=2.18.0',
        'pyreadline3>=3.5.3;platform_system=="Windows"',
        "tabcompleter>=1.4.0",
        "pdbp>=1.6.1",
        "idna==3.10",
        'chardet==5.2.0',
        'charset-normalizer==3.4.0',
        'urllib3>=1.26.20,<2;python_version<"3.10"',
        'urllib3>=1.26.20,<2.3.0;python_version>="3.10"',
        'requests==2.32.3',
        'sniffio==1.3.1',
        'h11==0.14.0',
        'outcome==1.3.0.post0',
        'trio==0.27.0',
        'trio-websocket==0.11.1',
        'wsproto==1.2.0',
        'websocket-client==1.8.0',
        'selenium==4.26.1',
        'cssselect==1.2.0',
        "sortedcontainers==2.4.0",
        'execnet==2.1.1',
        'iniconfig==2.0.0',
        'pluggy==1.5.0',
        "py==1.11.0",  # Needed by pytest-html
        'pytest==8.3.3',
        "pytest-html==2.0.1",  # Newer ones had issues
        'pytest-metadata==3.1.1',
        "pytest-ordering==0.6",
        'pytest-rerunfailures==14.0',
        'pytest-xdist==3.6.1',
        'parameterized==0.9.0',
        "behave==1.2.6",
        'soupsieve==2.6',
        "beautifulsoup4==4.12.3",
        'pyotp==2.9.0',
        'python-xlib==0.33;platform_system=="Linux"',
        'markdown-it-py==3.0.0',
        'mdurl==0.1.2',
        'rich==13.9.4',
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
            'coverage>=7.6.1;python_version<"3.9"',
            'coverage>=7.6.5;python_version>="3.9"',
            'pytest-cov>=5.0.0;python_version<"3.9"',
            'pytest-cov>=6.0.0;python_version>="3.9"',
        ],
        # pip install -e .[flake8]
        # Usage: flake8
        "flake8": [
            'flake8==5.0.4;python_version<"3.9"',
            'flake8==7.1.1;python_version>="3.9"',
            "mccabe==0.7.0",
            'pyflakes==2.5.0;python_version<"3.9"',
            'pyflakes==3.2.0;python_version>="3.9"',
            'pycodestyle==2.9.1;python_version<"3.9"',
            'pycodestyle==2.12.1;python_version>="3.9"',
        ],
        # pip install -e .[ipdb]
        # (Not needed for debugging anymore. SeleniumBase now includes "pdbp".)
        "ipdb": [
            "ipdb==0.13.13",
            'ipython==7.34.0',
        ],
        # pip install -e .[mss]
        # (An optional library for tile_windows() in CDP Mode.)
        "mss": [
            "mss==9.0.2",  # Next one drops Python 3.8/3.9
        ],
        # pip install -e .[pdfminer]
        # (An optional library for parsing PDF files.)
        "pdfminer": [
            'pdfminer.six==20240706',
            'cryptography==39.0.2;python_version<"3.9"',
            'cryptography==43.0.3;python_version>="3.9"',
            'cffi==1.17.1',
            "pycparser==2.22",
        ],
        # pip install -e .[pillow]
        # (An optional library for image-processing.)
        "pillow": [
            'Pillow>=10.4.0;python_version<"3.9"',
            'Pillow>=11.0.0;python_version>="3.9"',
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
            "proxy.py==2.4.3",  # 2.4.4 did not have "Listening on ..."
        ],
        # pip install -e .[psutil]
        "psutil": [
            "psutil==6.0.0",
        ],
        # pip install -e .[pyautogui]
        "pyautogui": [
            "PyAutoGUI==0.9.54",
        ],
        # pip install -e .[selenium-stealth]
        "selenium-stealth": [
            'selenium-stealth==1.0.6',
        ],
        # pip install -e .[selenium-wire]
        "selenium-wire": [
            'selenium-wire==5.1.0',
            'pyOpenSSL==24.2.1',
            'pyparsing>=3.1.4',
            'Brotli==1.1.0',
            'blinker==1.7.0',  # Newer ones had issues
            'h2==4.1.0',
            'hpack==4.0.0',
            'hyperframe==6.0.1',
            'kaitaistruct==0.10',
            'pyasn1==0.6.1',
            'zstandard==0.23.0',
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
        "seleniumbase.undetected.cdp_driver",
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
