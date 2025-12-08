"""Setup steps for installing SeleniumBase dependencies and plugins.
(Uses selenium 4.x and is compatible with Python 3.9+)"""
from setuptools import setup, find_packages  # noqa: F401
import os
import sys


this_dir = os.path.abspath(os.path.dirname(__file__))
long_description = None
total_description = None
try:
    with open(os.path.join(this_dir, "README.md"), mode="rb") as f:
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
with open(
    os.path.join(this_dir, "seleniumbase", "__version__.py"), mode="rb"
) as f:
    exec(f.read().decode("utf-8"), about)

if sys.argv[-1] == "publish":
    reply = None
    input_method = input
    confirm_text = ">>> Confirm release PUBLISH to PyPI? (yes/no): "
    reply = str(input_method(confirm_text)).lower().strip()
    if reply == "yes":
        if sys.version_info < (3, 10):
            current_ver = ".".join(str(ver) for ver in sys.version_info[:3])
            print("\nERROR! Publishing to PyPI requires Python>=3.10")
            print("You are currently using Python %s\n" % current_ver)
            sys.exit()
        print("\n*** Checking code health with flake8:\n")
        os.system("python -m pip install 'flake8==7.3.0'")
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
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
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
    python_requires=">=3.9",
    install_requires=[
        'pip>=25.3',
        'packaging>=25.0',
        'setuptools~=70.2;python_version<"3.10"',  # Newer ones had issues
        'setuptools>=80.9.0;python_version>="3.10"',
        'wheel>=0.45.1',
        'attrs>=25.4.0',
        'certifi>=2025.11.12',
        'exceptiongroup>=1.3.1',
        'websockets>=15.0.1',
        'filelock~=3.19.1;python_version<"3.10"',
        'filelock>=3.20.0;python_version>="3.10"',
        'fasteners>=0.20',
        'mycdp>=1.3.2',
        'pynose>=1.5.5',
        'platformdirs~=4.4.0;python_version<"3.10"',
        'platformdirs>=4.5.1;python_version>="3.10"',
        'typing-extensions>=4.15.0',
        'sbvirtualdisplay>=1.4.0',
        'MarkupSafe>=3.0.3',
        "Jinja2>=3.1.6",
        "six>=1.17.0",
        'parse>=1.20.2',
        'parse-type>=0.6.6',
        'colorama>=0.4.6',
        'pyyaml>=6.0.3',
        'pygments>=2.19.2',
        'pyreadline3>=3.5.4;platform_system=="Windows"',
        'tabcompleter>=1.4.0',
        'pdbp>=1.8.1',
        'idna>=3.11',
        'chardet==5.2.0',
        'charset-normalizer>=3.4.4,<4',
        'urllib3>=1.26.20,<2;python_version<"3.10"',
        'urllib3>=1.26.20,<3;python_version>="3.10"',
        'requests~=2.32.5',
        'sniffio==1.3.1',
        'h11==0.16.0',
        'outcome==1.3.0.post0',
        'trio>=0.31.0,<1;python_version<"3.10"',
        'trio>=0.32.0,<1;python_version>="3.10"',
        'trio-websocket~=0.12.2',
        'wsproto==1.2.0;python_version<"3.10"',
        'wsproto~=1.3.2;python_version>="3.10"',
        'websocket-client~=1.9.0',
        'selenium==4.32.0;python_version<"3.10"',
        'selenium==4.39.0;python_version>="3.10"',
        'cssselect==1.3.0',
        'nest-asyncio==1.6.0',
        'sortedcontainers==2.4.0',
        'execnet==2.1.1;python_version<"3.10"',
        'execnet==2.1.2;python_version>="3.10"',
        'iniconfig==2.1.0;python_version<"3.10"',
        'iniconfig==2.3.0;python_version>="3.10"',
        'pluggy==1.6.0',
        'pytest==8.4.2;python_version<"3.11"',
        'pytest==9.0.2;python_version>="3.11"',
        'pytest-html==4.0.2',  # Newer ones had issues
        'pytest-metadata==3.1.1',
        'pytest-ordering==0.6',
        'pytest-rerunfailures==16.0.1;python_version<"3.10"',
        'pytest-rerunfailures==16.1;python_version>="3.10"',
        'pytest-xdist==3.8.0',
        'parameterized==0.9.0',
        'behave==1.2.6',  # Newer ones had issues
        'soupsieve~=2.8',
        'beautifulsoup4~=4.14.3',
        'pyotp==2.9.0',
        'python-xlib==0.33;platform_system=="Linux"',
        'PyAutoGUI>=0.9.54;platform_system=="Linux"',
        'markdown-it-py==3.0.0;python_version<"3.10"',
        'markdown-it-py==4.0.0;python_version>="3.10"',
        'mdurl==0.1.2',
        'rich>=14.2.0,<15',
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
            'coverage>=7.10.7;python_version<"3.10"',
            'coverage>=7.12.0;python_version>="3.10"',
            'pytest-cov>=7.0.0',
        ],
        # pip install -e .[flake8]
        # Usage: flake8
        "flake8": [
            'flake8==7.3.0',
            "mccabe==0.7.0",
            'pyflakes==3.4.0',
            'pycodestyle==2.14.0',
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
            'mss==10.1.0',
        ],
        # pip install -e .[pdfminer]
        # (An optional library for parsing PDF files.)
        "pdfminer": [
            'pdfminer.six==20251107',
            'cryptography==46.0.3',
            'cffi==2.0.0',
            'pycparser==2.23',
        ],
        # pip install -e .[pillow]
        # (An optional library for image-processing.)
        "pillow": [
            'Pillow>=11.3.0;python_version<"3.10"',
            'Pillow>=12.0.0;python_version>="3.10"',
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
        # pip install -e .[playwright]
        # (For the Playwright integration.)
        "playwright": [
            "playwright>=1.56.0",
        ],
        # pip install -e .[psutil]
        "psutil": [
            "psutil>=7.1.3",
        ],
        # pip install -e .[pyautogui]
        # (Already a required dependency on Linux now.)
        "pyautogui": [
            'PyAutoGUI>=0.9.54;platform_system!="Linux"',
        ],
        # pip install -e .[selenium-stealth]
        "selenium-stealth": [
            'selenium-stealth==1.0.6',
        ],
        # pip install -e .[selenium-wire]
        "selenium-wire": [
            'selenium-wire==5.1.0',
            'pyOpenSSL>=24.2.1',
            'pyparsing>=3.1.4',
            'Brotli==1.1.0',
            'blinker==1.7.0',  # Newer ones had issues
            'h2==4.1.0',
            'hpack==4.0.0',
            'hyperframe==6.0.1',
            'kaitaistruct==0.10',
            'pyasn1==0.6.1',
            'zstandard>=0.23.0',
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
        "seleniumbase.drivers.cft_drivers",
        "seleniumbase.drivers.chs_drivers",
        "seleniumbase.drivers.opera_drivers",
        "seleniumbase.drivers.brave_drivers",
        "seleniumbase.drivers.comet_drivers",
        "seleniumbase.drivers.atlas_drivers",
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
