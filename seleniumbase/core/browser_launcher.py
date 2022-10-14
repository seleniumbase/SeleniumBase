import fasteners
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import urllib3
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from seleniumbase.config import settings
from seleniumbase.core import download_helper
from seleniumbase.core import proxy_helper
from seleniumbase.fixtures import constants
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
from seleniumbase import extensions  # browser extensions storage folder

urllib3.disable_warnings()
selenium4_or_newer = False
if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
    selenium4_or_newer = True
    from selenium.webdriver.common.options import ArgOptions

DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
# Make sure that the SeleniumBase DRIVER_DIR is at the top of the System PATH
# (Changes to the System PATH with os.environ only last during the test run)
if not os.environ["PATH"].startswith(DRIVER_DIR):
    # Remove existing SeleniumBase DRIVER_DIR from System PATH if present
    os.environ["PATH"] = os.environ["PATH"].replace(DRIVER_DIR, "")
    # If two path separators are next to each other, replace with just one
    os.environ["PATH"] = os.environ["PATH"].replace(
        os.pathsep + os.pathsep, os.pathsep
    )
    # Put the SeleniumBase DRIVER_DIR at the beginning of the System PATH
    os.environ["PATH"] = DRIVER_DIR + os.pathsep + os.environ["PATH"]
EXTENSIONS_DIR = os.path.dirname(os.path.realpath(extensions.__file__))
DISABLE_CSP_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "disable_csp.zip")
AD_BLOCK_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "ad_block.zip")
RECORDER_ZIP_PATH = os.path.join(EXTENSIONS_DIR, "recorder.zip")
DOWNLOADS_FOLDER = download_helper.get_downloads_folder()
PROXY_ZIP_PATH = proxy_helper.PROXY_ZIP_PATH
PROXY_ZIP_LOCK = proxy_helper.PROXY_ZIP_LOCK
PROXY_DIR_PATH = proxy_helper.PROXY_DIR_PATH
PROXY_DIR_LOCK = proxy_helper.PROXY_DIR_LOCK
PLATFORM = sys.platform
IS_WINDOWS = False
LOCAL_CHROMEDRIVER = None
LOCAL_GECKODRIVER = None
LOCAL_EDGEDRIVER = None
LOCAL_IEDRIVER = None
LOCAL_HEADLESS_IEDRIVER = None
LOCAL_OPERADRIVER = None
LOCAL_UC_DRIVER = None
if "darwin" in PLATFORM or "linux" in PLATFORM:
    LOCAL_CHROMEDRIVER = DRIVER_DIR + "/chromedriver"
    LOCAL_GECKODRIVER = DRIVER_DIR + "/geckodriver"
    LOCAL_EDGEDRIVER = DRIVER_DIR + "/msedgedriver"
    LOCAL_OPERADRIVER = DRIVER_DIR + "/operadriver"
    LOCAL_UC_DRIVER = DRIVER_DIR + "/uc_driver"
elif "win32" in PLATFORM or "win64" in PLATFORM or "x64" in PLATFORM:
    IS_WINDOWS = True
    LOCAL_EDGEDRIVER = DRIVER_DIR + "/msedgedriver.exe"
    LOCAL_IEDRIVER = DRIVER_DIR + "/IEDriverServer.exe"
    LOCAL_HEADLESS_IEDRIVER = DRIVER_DIR + "/headless_ie_selenium.exe"
    LOCAL_CHROMEDRIVER = DRIVER_DIR + "/chromedriver.exe"
    LOCAL_GECKODRIVER = DRIVER_DIR + "/geckodriver.exe"
    LOCAL_OPERADRIVER = DRIVER_DIR + "/operadriver.exe"
    LOCAL_UC_DRIVER = DRIVER_DIR + "/uc_driver.exe"
else:
    # Cannot determine system
    pass  # SeleniumBase will use web drivers from the System PATH by default


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def make_driver_executable_if_not(driver_path):
    # Verify driver has executable permissions. If not, add them.
    permissions = oct(os.stat(driver_path)[0])[-3:]
    if "4" in permissions or "6" in permissions:
        # We want at least a '5' or '7' to make sure it's executable
        make_executable(driver_path)


def requests_get(url):
    import requests

    response = None
    try:
        response = requests.get(url)
    except Exception:
        # Prevent SSLCertVerificationError / CERTIFICATE_VERIFY_FAILED
        url = url.replace("https://", "http://")
        response = requests.get(url)
    return response


def get_latest_chromedriver_version():
    last = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    url_request = requests_get(last)
    if url_request.ok:
        return url_request.text
    else:
        return None


def chromedriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if (
            not IS_WINDOWS
            and os.path.exists(os.path.join(path, "chromedriver"))
        ):
            return os.path.join(path, "chromedriver")
        elif (
            IS_WINDOWS
            and os.path.exists(os.path.join(path, "chromedriver.exe"))
        ):
            return os.path.join(path, "chromedriver.exe")
    return None


def edgedriver_on_path():
    return os.path.exists(LOCAL_EDGEDRIVER)


def geckodriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if (not IS_WINDOWS) and os.path.exists(path + "/geckodriver"):
            return True
        elif IS_WINDOWS and os.path.exists(path + "/geckodriver.exe"):
            return True
    return False


def iedriver_on_path():
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        if os.path.exists(path + "/IEDriverServer.exe"):
            return True
    return False


def headless_iedriver_on_path():
    return os.path.exists(LOCAL_HEADLESS_IEDRIVER)


def _repair_chromedriver(chrome_options, headless_options, mcv=None):
    if mcv:
        subprocess.check_call(
            "sbase install chromedriver %s" % mcv, shell=True
        )
        return
    driver = None
    subprocess.check_call(
        "sbase install chromedriver 72.0.3626.69", shell=True
    )
    try:
        if selenium4_or_newer:
            service = ChromeService(executable_path=LOCAL_CHROMEDRIVER)
            driver = webdriver.Chrome(
                service=service,
                options=headless_options,
            )
        else:
            driver = webdriver.Chrome(
                executable_path=LOCAL_CHROMEDRIVER,
                options=headless_options,
            )
    except Exception:
        subprocess.check_call(
            "sbase install chromedriver latest-1", shell=True
        )
        return
    chrome_version = None
    if "version" in driver.capabilities:
        chrome_version = driver.capabilities["version"]
    else:
        chrome_version = driver.capabilities["browserVersion"]
    major_chrome_ver = chrome_version.split(".")[0]
    chrome_dict = driver.capabilities["chrome"]
    driver.quit()
    chromedriver_ver = chrome_dict["chromedriverVersion"]
    chromedriver_ver = chromedriver_ver.split(" ")[0]
    major_chromedriver_ver = chromedriver_ver.split(".")[0]
    if (
        major_chromedriver_ver != major_chrome_ver
        and int(major_chrome_ver) >= 73
    ):
        subprocess.check_call(
            "sbase install chromedriver %s" % major_chrome_ver, shell=True
        )
    return


def _repair_edgedriver(edge_version):
    print(
        "\nWarning: msedgedriver version doesn't match Edge version!"
        "\nAttempting to install a matching version of msedgedriver:"
    )
    subprocess.check_call(
        "sbase install edgedriver %s" % edge_version, shell=True
    )
    return


def _mark_driver_repaired():
    import codecs

    abs_path = os.path.abspath(".")
    driver_repaired_lock = constants.MultiBrowser.DRIVER_REPAIRED
    file_path = os.path.join(abs_path, driver_repaired_lock)
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)
    out_file = codecs.open(file_path, "w+", encoding="utf-8")
    out_file.writelines("")
    out_file.close()


def _was_driver_repaired():
    abs_path = os.path.abspath(".")
    driver_repaired_lock = constants.MultiBrowser.DRIVER_REPAIRED
    file_path = os.path.join(abs_path, driver_repaired_lock)
    return os.path.exists(file_path)


def _add_chrome_proxy_extension(
    chrome_options, proxy_string, proxy_user, proxy_pass, zip_it=True
):
    """Implementation of https://stackoverflow.com/a/35293284 for
    https://stackoverflow.com/questions/12848327/
    (Run Selenium on a proxy server that requires authentication.)"""
    arg_join = " ".join(sys.argv)
    if not ("-n" in sys.argv or " -n=" in arg_join or arg_join == "-c"):
        # Single-threaded
        if zip_it:
            proxy_helper.create_proxy_ext(proxy_string, proxy_user, proxy_pass)
            proxy_zip = PROXY_ZIP_PATH
            chrome_options.add_extension(proxy_zip)
        else:
            proxy_helper.create_proxy_ext(
                proxy_string, proxy_user, proxy_pass, zip_it=False
            )
            chrome_options = add_chrome_ext_dir(chrome_options, PROXY_DIR_PATH)

    else:
        # Pytest multithreaded test
        if zip_it:
            proxy_zip_lock = fasteners.InterProcessLock(PROXY_ZIP_LOCK)
            with proxy_zip_lock:
                if not os.path.exists(PROXY_ZIP_PATH):
                    proxy_helper.create_proxy_ext(
                        proxy_string, proxy_user, proxy_pass
                    )
                proxy_zip = PROXY_ZIP_PATH
                chrome_options.add_extension(proxy_zip)
        else:
            proxy_dir_lock = fasteners.InterProcessLock(PROXY_DIR_LOCK)
            with proxy_dir_lock:
                if not os.path.exists(PROXY_DIR_PATH):
                    proxy_helper.create_proxy_ext(
                        proxy_string, proxy_user, proxy_pass, False
                    )
                chrome_options = add_chrome_ext_dir(
                    chrome_options, PROXY_DIR_PATH
                )
    return chrome_options


def is_using_uc(undetectable, browser_name):
    if (
        selenium4_or_newer
        and undetectable
        and browser_name == constants.Browser.GOOGLE_CHROME
    ):
        return True
    return False


def _unzip_to_new_folder(zip_file, folder):
    proxy_dir_lock = fasteners.InterProcessLock(PROXY_DIR_LOCK)
    with proxy_dir_lock:
        if not os.path.exists(folder):
            import zipfile

            zip_ref = zipfile.ZipFile(zip_file, "r")
            os.makedirs(folder)
            zip_ref.extractall(folder)
            zip_ref.close()


def add_chrome_ext_dir(chrome_options, dir_path):
    option_exists = False
    for arg in chrome_options.arguments:
        if arg.startswith("--load-extension="):
            option_exists = True
            chrome_options.arguments.remove(arg)
            chrome_options.add_argument(
                "%s,%s" % (arg, os.path.realpath(dir_path))
            )
    if not option_exists:
        chrome_options.add_argument(
            "--load-extension=%s" % os.path.realpath(dir_path)
        )
    return chrome_options


def _add_chrome_disable_csp_extension(chrome_options):
    """Disable Chrome's Content-Security-Policy with a browser extension.
    See https://github.com/PhilGrayson/chrome-csp-disable for details."""
    chrome_options.add_extension(DISABLE_CSP_ZIP_PATH)
    return chrome_options


def _add_chrome_ad_block_extension(chrome_options):
    """Block Ads on Chromium Browsers with a browser extension.
    See https://github.com/slingamn/simpleblock for details."""
    chrome_options.add_extension(AD_BLOCK_ZIP_PATH)
    return chrome_options


def _add_chrome_recorder_extension(chrome_options):
    """The SeleniumBase Recorder Chrome/Edge extension.
    https://seleniumbase.io/help_docs/recorder_mode/"""
    chrome_options.add_extension(RECORDER_ZIP_PATH)
    return chrome_options


def _set_chrome_options(
    browser_name,
    downloads_path,
    headless,
    locale_code,
    proxy_string,
    proxy_auth,
    proxy_user,
    proxy_pass,
    proxy_bypass_list,
    proxy_pac_url,
    user_agent,
    recorder_ext,
    disable_js,
    disable_csp,
    enable_ws,
    enable_sync,
    use_auto_ext,
    undetectable,
    uc_subprocess,
    no_sandbox,
    disable_gpu,
    headless2,
    incognito,
    guest_mode,
    devtools,
    remote_debug,
    swiftshader,
    ad_block_on,
    block_images,
    do_not_track,
    chromium_arg,
    user_data_dir,
    extension_zip,
    extension_dir,
    page_load_strategy,
    external_pdf,
    servername,
    mobile_emulator,
    device_width,
    device_height,
    device_pixel_ratio,
):
    chrome_options = webdriver.ChromeOptions()
    if is_using_uc(undetectable, browser_name):
        from seleniumbase import undetected

        chrome_options = undetected.ChromeOptions()
    elif browser_name == constants.Browser.OPERA:
        chrome_options = webdriver.opera.options.Options()

    prefs = {}
    prefs["download.default_directory"] = downloads_path
    prefs["local_discovery.notifications_enabled"] = False
    prefs["credentials_enable_service"] = False
    prefs["download.prompt_for_download"] = False
    prefs["download.directory_upgrade"] = True
    prefs["safebrowsing.enabled"] = False
    prefs["default_content_setting_values.notifications"] = 0
    prefs["content_settings.exceptions.automatic_downloads.*.setting"] = 1
    prefs["safebrowsing.disable_download_protection"] = True
    prefs["default_content_settings.popups"] = 0
    prefs["managed_default_content_settings.popups"] = 0
    prefs["profile.password_manager_enabled"] = False
    prefs["profile.default_content_setting_values.notifications"] = 2
    prefs["profile.default_content_settings.popups"] = 0
    prefs["profile.managed_default_content_settings.popups"] = 0
    prefs["profile.default_content_setting_values.automatic_downloads"] = 1
    if locale_code:
        prefs["intl.accept_languages"] = locale_code
    if block_images:
        prefs["profile.managed_default_content_settings.images"] = 2
    if disable_js:
        prefs["profile.managed_default_content_settings.javascript"] = 2
    if do_not_track:
        prefs["enable_do_not_track"] = True
    if external_pdf:
        prefs["plugins.always_open_pdf_externally"] = True
    chrome_options.add_experimental_option("prefs", prefs)
    if not selenium4_or_newer:
        chrome_options.add_experimental_option("w3c", True)
    if enable_sync:
        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation", "enable-logging", "disable-sync"],
        )
        chrome_options.add_argument("--enable-sync")
    else:
        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation", "enable-logging", "enable-blink-features"],
        )
    if browser_name == constants.Browser.OPERA:
        # Disable the Blink features
        if enable_sync:
            chrome_options.add_experimental_option(
                "excludeSwitches",
                (
                    [
                        "enable-automation",
                        "enable-logging",
                        "disable-sync",
                        "enable-blink-features",
                    ]
                ),
            )
            chrome_options.add_argument("--enable-sync")
        else:
            chrome_options.add_experimental_option(
                "excludeSwitches",
                (
                    [
                        "enable-automation",
                        "enable-logging",
                        "enable-blink-features",
                    ]
                ),
            )
    if mobile_emulator:
        emulator_settings = {}
        device_metrics = {}
        if (
            type(device_width) is int
            and type(device_height) is int
            and type(device_pixel_ratio) is int
        ):
            device_metrics["width"] = device_width
            device_metrics["height"] = device_height
            device_metrics["pixelRatio"] = device_pixel_ratio
        else:
            device_metrics["width"] = 360
            device_metrics["height"] = 640
            device_metrics["pixelRatio"] = 2
        emulator_settings["deviceMetrics"] = device_metrics
        if user_agent:
            emulator_settings["userAgent"] = user_agent
        chrome_options.add_experimental_option(
            "mobileEmulation", emulator_settings
        )
    if (
        not proxy_auth
        and not disable_csp
        and not ad_block_on
        and not recorder_ext
        and (not extension_zip and not extension_dir)
    ):
        if incognito:
            # Use Chrome's Incognito Mode
            # Incognito Mode prevents Chrome extensions from loading,
            # so if using extensions or a feature that uses extensions,
            # then Chrome's Incognito mode will be disabled instead.
            chrome_options.add_argument("--incognito")
        elif guest_mode:
            # Use Chrome's Guest Mode
            # Guest mode prevents Chrome extensions from loading,
            # so if using extensions or a feature that uses extensions,
            # then Chrome's Guest Mode will be disabled instead.
            chrome_options.add_argument("--guest")
        else:
            pass
    if user_data_dir:
        abs_path = os.path.abspath(user_data_dir)
        chrome_options.add_argument("user-data-dir=%s" % abs_path)
    if extension_zip:
        # Can be a comma-separated list of .ZIP or .CRX files
        extension_zip_list = extension_zip.split(",")
        for extension_zip_item in extension_zip_list:
            abs_path = os.path.abspath(extension_zip_item)
            chrome_options.add_extension(abs_path)
    if extension_dir:
        # load-extension input can be a comma-separated list
        abs_path = os.path.abspath(extension_dir)
        chrome_options = add_chrome_ext_dir(chrome_options, abs_path)
    if (
        selenium4_or_newer
        and page_load_strategy
        and page_load_strategy.lower() in ["eager", "none"]
    ):
        # Only change it if not "normal", which is the default.
        chrome_options.page_load_strategy = page_load_strategy.lower()
    elif (
        selenium4_or_newer
        and not page_load_strategy
        and hasattr(settings, "PAGE_LOAD_STRATEGY")
        and settings.PAGE_LOAD_STRATEGY
        and settings.PAGE_LOAD_STRATEGY.lower() in ["eager", "none"]
    ):
        # Only change it if not "normal", which is the default.
        chrome_options.page_load_strategy = settings.PAGE_LOAD_STRATEGY.lower()
    if servername != "localhost":
        use_auto_ext = True  # Use Automation Extension
    if not use_auto_ext:  # Disable Automation Extension. (Default)
        if browser_name != constants.Browser.OPERA:
            chrome_options.add_argument(
                "--disable-blink-features=AutomationControlled"
            )
        chrome_options.add_experimental_option("useAutomationExtension", False)
    if headless2:
        chrome_options.add_argument("--headless=chrome")
    elif headless:
        chrome_options.add_argument("--headless")
    if (settings.DISABLE_CSP_ON_CHROME or disable_csp) and not headless:
        # Headless Chrome does not support extensions, which are required
        # for disabling the Content Security Policy on Chrome.
        if is_using_uc(undetectable, browser_name):
            disable_csp_zip = DISABLE_CSP_ZIP_PATH
            disable_csp_dir = os.path.join(DOWNLOADS_FOLDER, "disable_csp")
            _unzip_to_new_folder(disable_csp_zip, disable_csp_dir)
            chrome_options = add_chrome_ext_dir(
                chrome_options, disable_csp_dir
            )
        else:
            chrome_options = _add_chrome_disable_csp_extension(chrome_options)
    if ad_block_on and not headless:
        # Headless Chrome does not support extensions.
        if is_using_uc(undetectable, browser_name):
            ad_block_zip = AD_BLOCK_ZIP_PATH
            ad_block_dir = os.path.join(DOWNLOADS_FOLDER, "ad_block")
            _unzip_to_new_folder(ad_block_zip, ad_block_dir)
            chrome_options = add_chrome_ext_dir(chrome_options, ad_block_dir)
        else:
            chrome_options = _add_chrome_ad_block_extension(chrome_options)
    if recorder_ext and not headless:
        if is_using_uc(undetectable, browser_name):
            recorder_zip = RECORDER_ZIP_PATH
            recorder_dir = os.path.join(DOWNLOADS_FOLDER, "recorder")
            _unzip_to_new_folder(recorder_zip, recorder_dir)
            chrome_options = add_chrome_ext_dir(chrome_options, recorder_dir)
        else:
            chrome_options = _add_chrome_recorder_extension(chrome_options)
    if proxy_string:
        if proxy_auth:
            zip_it = True
            if is_using_uc(undetectable, browser_name):
                zip_it = False  # undetected-chromedriver needs a folder ext
            chrome_options = _add_chrome_proxy_extension(
                chrome_options, proxy_string, proxy_user, proxy_pass, zip_it
            )
        chrome_options.add_argument("--proxy-server=%s" % proxy_string)
        if proxy_bypass_list:
            chrome_options.add_argument(
                "--proxy-bypass-list=%s" % proxy_bypass_list
            )
    elif proxy_pac_url:
        if proxy_auth:
            zip_it = True  # undetected-chromedriver needs a folder ext
            if is_using_uc(undetectable, browser_name):
                zip_it = False
            chrome_options = _add_chrome_proxy_extension(
                chrome_options, None, proxy_user, proxy_pass, zip_it
            )
        chrome_options.add_argument("--proxy-pac-url=%s" % proxy_pac_url)
    if browser_name != constants.Browser.OPERA:
        # Opera Chromium doesn't support these switches
        chrome_options.add_argument("--ignore-certificate-errors")
        if not enable_ws:
            chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--no-sandbox")
    else:
        # Opera Chromium only!
        chrome_options.add_argument("--allow-elevated-browser")
    if remote_debug:
        # To access the Remote Debugger, go to: http://localhost:9222
        # while a Chromium driver is running.
        # Info: https://chromedevtools.github.io/devtools-protocol/
        chrome_options.add_argument("--remote-debugging-port=9222")
    if swiftshader:
        chrome_options.add_argument("--use-gl=swiftshader")
    else:
        chrome_options.add_argument("--disable-gpu")
    if "linux" in PLATFORM:
        chrome_options.add_argument("--disable-dev-shm-usage")
    if chromium_arg:
        # Can be a comma-separated list of Chromium args
        chromium_arg_list = chromium_arg.split(",")
        for chromium_arg_item in chromium_arg_list:
            chromium_arg_item = chromium_arg_item.strip()
            if not chromium_arg_item.startswith("--"):
                if chromium_arg_item.startswith("-"):
                    chromium_arg_item = "-" + chromium_arg_item
                else:
                    chromium_arg_item = "--" + chromium_arg_item
            if len(chromium_arg_item) >= 3:
                chrome_options.add_argument(chromium_arg_item)
    if devtools and not headless:
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
    if user_agent:
        chrome_options.add_argument("--user-agent=%s" % user_agent)
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-single-click-autofill")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--disable-prompt-on-repost")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-3d-apis")
    if (
        is_using_uc(undetectable, browser_name)
        and (
            not headless
            or "linux" in PLATFORM  # switches to Xvfb (non-headless)
        )
    ):
        # Skip remaining options that trigger anti-bot services
        return chrome_options
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument(
        "--disable-autofill-keyboard-accessory-view[8]"
    )
    chrome_options.add_argument("--homepage=about:blank")
    chrome_options.add_argument("--dom-automation")
    chrome_options.add_argument("--disable-hang-monitor")
    return chrome_options


def _set_firefox_options(
    downloads_path,
    headless,
    locale_code,
    proxy_string,
    proxy_bypass_list,
    proxy_pac_url,
    user_agent,
    disable_js,
    disable_csp,
    firefox_arg,
    firefox_pref,
):
    blank_p = "about:blank"
    options = webdriver.FirefoxOptions()
    options.accept_untrusted_certs = True
    options.set_preference("reader.parse-on-load.enabled", False)
    options.set_preference("browser.startup.homepage", blank_p)
    options.set_preference("startup.homepage_welcome_url", blank_p)
    options.set_preference("startup.homepage_welcome_url.additional", blank_p)
    options.set_preference("browser.newtab.url", blank_p)
    options.set_preference("trailhead.firstrun.branches", "nofirstrun-empty")
    options.set_preference("browser.aboutwelcome.enabled", False)
    options.set_preference("pdfjs.disabled", True)
    options.set_preference("app.update.auto", False)
    options.set_preference("app.update.enabled", False)
    options.set_preference("browser.formfill.enable", False)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("dom.disable_beforeunload", True)
    options.set_preference("browser.contentblocking.database.enabled", True)
    options.set_preference("extensions.allowPrivateBrowsingByDefault", True)
    options.set_preference("extensions.PrivateBrowsing.notification", False)
    options.set_preference("extensions.systemAddon.update.enabled", False)
    options.set_preference("extensions.update.autoUpdateDefault", False)
    options.set_preference("extensions.update.enabled", False)
    options.set_preference("datareporting.healthreport.service.enabled", False)
    options.set_preference("datareporting.healthreport.uploadEnabled", False)
    options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
    options.set_preference("browser.search.update", False)
    options.set_preference("privacy.trackingprotection.enabled", False)
    options.set_preference("toolkit.telemetry.enabled", False)
    options.set_preference("toolkit.telemetry.unified", False)
    options.set_preference("toolkit.telemetry.archive.enabled", False)
    if proxy_string:
        socks_proxy = False
        socks_ver = 0
        chunks = proxy_string.split(":")
        if len(chunks) == 3 and (
            chunks[0] == "socks4" or chunks[0] == "socks5"
        ):
            socks_proxy = True
            socks_ver = int(chunks[0][5])
            if chunks[1].startswith("//") and len(chunks[1]) > 2:
                chunks[1] = chunks[1][2:]
            proxy_server = chunks[1]
            proxy_port = chunks[2]
        else:
            proxy_server = proxy_string.split(":")[0]
            proxy_port = proxy_string.split(":")[1]
        options.set_preference("network.proxy.type", 1)
        if socks_proxy:
            options.set_preference("network.proxy.socks", proxy_server)
            options.set_preference("network.proxy.socks_port", int(proxy_port))
            options.set_preference("network.proxy.socks_version", socks_ver)
        else:
            options.set_preference("network.proxy.http", proxy_server)
            options.set_preference("network.proxy.http_port", int(proxy_port))
            options.set_preference("network.proxy.ssl", proxy_server)
            options.set_preference("network.proxy.ssl_port", int(proxy_port))
        if proxy_bypass_list:
            options.set_preference("no_proxies_on", proxy_bypass_list)
    elif proxy_pac_url:
        options.set_preference("network.proxy.type", 2)
        options.set_preference("network.proxy.autoconfig_url", proxy_pac_url)
    if user_agent:
        options.set_preference("general.useragent.override", user_agent)
    options.set_preference(
        "security.mixed_content.block_active_content", False
    )
    options.set_preference("security.warn_submit_insecure", False)
    if disable_js:
        options.set_preference("javascript.enabled", False)
    if settings.DISABLE_CSP_ON_FIREFOX or disable_csp:
        options.set_preference("security.csp.enable", False)
    options.set_preference(
        "browser.download.manager.showAlertOnComplete", False
    )
    if headless and "linux" not in PLATFORM:
        options.add_argument("--headless")
    if locale_code:
        options.set_preference("intl.accept_languages", locale_code)
    options.set_preference("browser.shell.checkDefaultBrowser", False)
    options.set_preference("browser.startup.page", 0)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.animateNotifications", False)
    options.set_preference("browser.download.dir", downloads_path)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        (
            "application/pdf, application/zip, application/octet-stream, "
            "text/csv, text/xml, application/xml, text/plain, "
            "text/octet-stream, application/x-gzip, application/x-tar "
            "application/"
            "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
    if firefox_arg:
        # Can be a comma-separated list of Firefox args
        firefox_arg_list = firefox_arg.split(",")
        for firefox_arg_item in firefox_arg_list:
            firefox_arg_item = firefox_arg_item.strip()
            if not firefox_arg_item.startswith("--"):
                if firefox_arg_item.startswith("-"):
                    firefox_arg_item = "-" + firefox_arg_item
                else:
                    firefox_arg_item = "--" + firefox_arg_item
            if len(firefox_arg_item) >= 3:
                options.add_argument(firefox_arg_item)
    if firefox_pref:
        # Can be a comma-separated list of Firefox preference:value pairs
        firefox_pref_list = firefox_pref.split(",")
        for firefox_pref_item in firefox_pref_list:
            f_pref = None
            f_pref_value = None
            needs_conversion = False
            if firefox_pref_item.count(":") == 0:
                f_pref = firefox_pref_item
                f_pref_value = True
            elif firefox_pref_item.count(":") == 1:
                f_pref = firefox_pref_item.split(":")[0]
                f_pref_value = firefox_pref_item.split(":")[1]
                needs_conversion = True
            else:  # More than one ":" in the set. (Too many!)
                raise Exception(
                    'Incorrect formatting for Firefox "pref:value" set!'
                )
            if needs_conversion:
                if f_pref_value.lower() == "true" or len(f_pref_value) == 0:
                    f_pref_value = True
                elif f_pref_value.lower() == "false":
                    f_pref_value = False
                elif f_pref_value.isdigit():
                    f_pref_value = int(f_pref_value)
                elif f_pref_value.isdecimal():
                    f_pref_value = float(f_pref_value)
                else:
                    pass  # keep as string
            if len(f_pref) >= 1:
                options.set_preference(f_pref, f_pref_value)
    return options


def display_proxy_warning(proxy_string):
    message = (
        '\n\nWARNING: Proxy String ["%s"] is NOT in the expected '
        '"ip_address:port" or "server:port" format, '
        "(OR the key does not exist in "
        "seleniumbase.config.proxy_list.PROXY_LIST)." % proxy_string
    )
    if settings.RAISE_INVALID_PROXY_STRING_EXCEPTION:
        raise Exception(message)
    else:
        message += " *** DEFAULTING to NOT USING a Proxy Server! ***"
        warnings.simplefilter("always", Warning)  # See Warnings
        warnings.warn(message, category=Warning, stacklevel=2)
        warnings.simplefilter("default", Warning)  # Set Default


def validate_proxy_string(proxy_string):
    from seleniumbase.config import proxy_list
    from seleniumbase.fixtures import page_utils

    if proxy_string in proxy_list.PROXY_LIST.keys():
        proxy_string = proxy_list.PROXY_LIST[proxy_string]
        if not proxy_string:
            return None
    valid = False
    val_ip = re.match(
        r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$", proxy_string
    )
    if not val_ip:
        if proxy_string.startswith("http://"):
            proxy_string = proxy_string.split("http://")[1]
        elif proxy_string.startswith("https://"):
            proxy_string = proxy_string.split("https://")[1]
        elif "://" in proxy_string:
            if not proxy_string.startswith("socks4://") and not (
                proxy_string.startswith("socks5://")
            ):
                proxy_string = proxy_string.split("://")[1]
        chunks = proxy_string.split(":")
        if len(chunks) == 2:
            if re.match(r"^\d+$", chunks[1]):
                if page_utils.is_valid_url("http://" + proxy_string):
                    valid = True
        elif len(chunks) == 3:
            if re.match(r"^\d+$", chunks[2]):
                if page_utils.is_valid_url("http:" + ":".join(chunks[1:])):
                    if chunks[0] == "http":
                        valid = True
                    elif chunks[0] == "https":
                        valid = True
                    elif chunks[0] == "socks4":
                        valid = True
                    elif chunks[0] == "socks5":
                        valid = True
    else:
        proxy_string = val_ip.group()
        valid = True
    if not valid:
        display_proxy_warning(proxy_string)
        proxy_string = None
    return proxy_string


def get_driver(
    browser_name=None,
    headless=False,
    locale_code=None,
    use_grid=False,
    protocol="http",
    servername="localhost",
    port=4444,
    proxy_string=None,
    proxy_bypass_list=None,
    proxy_pac_url=None,
    user_agent=None,
    cap_file=None,
    cap_string=None,
    recorder_ext=False,
    disable_js=False,
    disable_csp=False,
    enable_ws=False,
    enable_sync=False,
    use_auto_ext=False,
    undetectable=False,
    uc_subprocess=False,
    no_sandbox=False,
    disable_gpu=False,
    headless2=False,
    incognito=False,
    guest_mode=False,
    devtools=False,
    remote_debug=False,
    swiftshader=False,
    ad_block_on=False,
    block_images=False,
    do_not_track=False,
    chromium_arg=None,
    firefox_arg=None,
    firefox_pref=None,
    user_data_dir=None,
    extension_zip=None,
    extension_dir=None,
    page_load_strategy=None,
    external_pdf=False,
    test_id=None,
    mobile_emulator=False,
    device_width=None,
    device_height=None,
    device_pixel_ratio=None,
    browser=None,  # A duplicate of browser_name to avoid confusion
):
    if not browser_name:
        if browser:
            browser_name = browser
        else:
            browser_name = "chrome"  # The default if not specified
    browser_name = browser_name.lower()
    if headless2 and browser_name == constants.Browser.FIREFOX:
        headless2 = False  # Only for Chromium
        headless = True
    if uc_subprocess and not undetectable:
        undetectable = True
    proxy_auth = False
    proxy_user = None
    proxy_pass = None
    if proxy_string:
        username_and_password = None
        if "@" in proxy_string:
            # Format => username:password@hostname:port
            try:
                username_and_password = proxy_string.split("@")[0]
                proxy_string = proxy_string.split("@")[1]
                proxy_user = username_and_password.split(":")[0]
                proxy_pass = username_and_password.split(":")[1]
            except Exception:
                raise Exception(
                    "The format for using a proxy server with authentication "
                    'is: "username:password@hostname:port". If using a proxy '
                    'server without auth, the format is: "hostname:port".'
                )
            if browser_name != constants.Browser.GOOGLE_CHROME and (
                browser_name != constants.Browser.EDGE
            ):
                raise Exception(
                    "Chrome or Edge is required when using a proxy server "
                    "that has authentication! (If using a proxy server "
                    "without auth, Chrome, Edge, or Firefox may be used.)"
                )
        proxy_string = validate_proxy_string(proxy_string)
        if proxy_string and proxy_user and proxy_pass:
            proxy_auth = True
    elif proxy_pac_url:
        username_and_password = None
        if "@" in proxy_pac_url:
            # Format => username:password@PAC_URL.pac
            try:
                username_and_password = proxy_pac_url.split("@")[0]
                proxy_pac_url = proxy_pac_url.split("@")[1]
                proxy_user = username_and_password.split(":")[0]
                proxy_pass = username_and_password.split(":")[1]
            except Exception:
                raise Exception(
                    "The format for using a PAC URL with authentication "
                    'is: "username:password@PAC_URL.pac". If using a PAC '
                    'URL without auth, the format is: "PAC_URL.pac".'
                )
            if browser_name != constants.Browser.GOOGLE_CHROME and (
                browser_name != constants.Browser.EDGE
            ):
                raise Exception(
                    "Chrome or Edge is required when using a PAC URL "
                    "that has authentication! (If using a PAC URL "
                    "without auth, Chrome, Edge, or Firefox may be used.)"
                )
        if not proxy_pac_url.lower().endswith(".pac"):
            raise Exception('The proxy PAC URL must end with ".pac"!')
        if proxy_pac_url and proxy_user and proxy_pass:
            proxy_auth = True
    if (
        is_using_uc(undetectable, browser_name)
        and "linux" not in PLATFORM
        and headless
    ):
        headless = False
        headless2 = True
    if (
        headless
        and (
            proxy_auth
            or disable_js
            or ad_block_on
            or disable_csp
            or recorder_ext
            or extension_zip
            or extension_dir
        )
        and (
            browser_name == constants.Browser.GOOGLE_CHROME
            or browser_name == constants.Browser.EDGE
        )
    ):
        # Headless Chrome/Edge doesn't support extensions, which are
        # required when using a proxy server that has authentication,
        # or when using other SeleniumBase extensions (eg: Recorder).
        # Instead, base_case.py will use the SBVirtualDisplay when not
        # using Chrome's built-in headless mode. See link for details:
        # https://bugs.chromium.org/p/chromium/issues/detail?id=706008
        headless = False
        if "linux" not in PLATFORM:
            # Use the new headless mode on Chrome if not using Linux:
            # bugs.chromium.org/p/chromium/issues/detail?id=706008#c36
            # Although Linux is technically supported, there are a lot
            # of old versions of Chrome on Linux server machines, and
            # this mode requires a recent version of Chrome to work.
            # Specify "--headless2" as a pytest arg to use on Linux.
            headless2 = True
    if (
        browser_name == constants.Browser.GOOGLE_CHROME
        and user_data_dir
        and len(user_data_dir) < 3
    ):
        raise Exception(
            "Name length of Chrome's User Data Directory must be >= 3."
        )
    if use_grid:
        return get_remote_driver(
            browser_name,
            headless,
            locale_code,
            protocol,
            servername,
            port,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            cap_file,
            cap_string,
            recorder_ext,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_subprocess,
            no_sandbox,
            disable_gpu,
            headless2,
            incognito,
            guest_mode,
            devtools,
            remote_debug,
            swiftshader,
            ad_block_on,
            block_images,
            do_not_track,
            chromium_arg,
            firefox_arg,
            firefox_pref,
            user_data_dir,
            extension_zip,
            extension_dir,
            page_load_strategy,
            external_pdf,
            test_id,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )
    else:
        return get_local_driver(
            browser_name,
            headless,
            locale_code,
            servername,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            recorder_ext,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_subprocess,
            no_sandbox,
            disable_gpu,
            headless2,
            incognito,
            guest_mode,
            devtools,
            remote_debug,
            swiftshader,
            ad_block_on,
            block_images,
            do_not_track,
            chromium_arg,
            firefox_arg,
            firefox_pref,
            user_data_dir,
            extension_zip,
            extension_dir,
            page_load_strategy,
            external_pdf,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )


def get_remote_driver(
    browser_name,
    headless,
    locale_code,
    protocol,
    servername,
    port,
    proxy_string,
    proxy_auth,
    proxy_user,
    proxy_pass,
    proxy_bypass_list,
    proxy_pac_url,
    user_agent,
    cap_file,
    cap_string,
    recorder_ext,
    disable_js,
    disable_csp,
    enable_ws,
    enable_sync,
    use_auto_ext,
    undetectable,
    uc_subprocess,
    no_sandbox,
    disable_gpu,
    headless2,
    incognito,
    guest_mode,
    devtools,
    remote_debug,
    swiftshader,
    ad_block_on,
    block_images,
    do_not_track,
    chromium_arg,
    firefox_arg,
    firefox_pref,
    user_data_dir,
    extension_zip,
    extension_dir,
    page_load_strategy,
    external_pdf,
    test_id,
    mobile_emulator,
    device_width,
    device_height,
    device_pixel_ratio,
):
    # Construct the address for connecting to a Selenium Grid
    if servername.startswith("https://"):
        protocol = "https"
        servername = servername.split("https://")[1]
    elif "://" in servername:
        servername = servername.split("://")[1]
    server_with_port = ""
    if ":" not in servername:
        col_port = ":" + str(port)
        first_slash = servername.find("/")
        if first_slash != -1:
            server_with_port = (
                servername[:first_slash] + col_port + servername[first_slash:]
            )
        else:
            server_with_port = servername + col_port
    else:
        server_with_port = servername
    address = "%s://%s" % (protocol, server_with_port)
    if not address.endswith("/wd/hub"):
        if address.endswith("/"):
            address += "wd/hub"
        else:
            address += "/wd/hub"
    downloads_path = DOWNLOADS_FOLDER
    desired_caps = {}
    extra_caps = {}
    if cap_file:
        from seleniumbase.core import capabilities_parser

        desired_caps = capabilities_parser.get_desired_capabilities(cap_file)
    if cap_string:
        import json

        try:
            extra_caps = json.loads(str(cap_string))
        except Exception as e:
            p1 = "Invalid input format for --cap-string:\n  %s" % e
            p2 = "The --cap-string input was: %s" % cap_string
            p3 = (
                "Enclose cap-string in SINGLE quotes; "
                "keys and values in DOUBLE quotes."
            )
            p4 = (
                """Here's an example of correct cap-string usage:\n  """
                """--cap-string='{"browserName":"chrome","name":"test1"}'"""
            )
            raise Exception("%s\n%s\n%s\n%s" % (p1, p2, p3, p4))
        for cap_key in extra_caps.keys():
            desired_caps[cap_key] = extra_caps[cap_key]
    if cap_file or cap_string:
        if "name" in desired_caps.keys():
            if desired_caps["name"] == "*":
                desired_caps["name"] = test_id
    if browser_name == constants.Browser.GOOGLE_CHROME:
        chrome_options = _set_chrome_options(
            browser_name,
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            recorder_ext,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_subprocess,
            no_sandbox,
            disable_gpu,
            headless2,
            incognito,
            guest_mode,
            devtools,
            remote_debug,
            swiftshader,
            ad_block_on,
            block_images,
            do_not_track,
            chromium_arg,
            user_data_dir,
            extension_zip,
            extension_dir,
            page_load_strategy,
            external_pdf,
            servername,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )
        capabilities = None
        if selenium4_or_newer:
            capabilities = webdriver.ChromeOptions().to_capabilities()
        else:
            capabilities = chrome_options.to_capabilities()
        # Set custom desired capabilities
        selenoid = False
        selenoid_options = None
        screen_resolution = None
        browser_version = None
        platform_name = None
        extension_capabilities = {}
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
            if key == "selenoid:options":
                selenoid = True
                selenoid_options = desired_caps[key]
            elif key == "screenResolution":
                screen_resolution = desired_caps[key]
            elif key == "version" or key == "browserVersion":
                browser_version = desired_caps[key]
            elif key == "platform" or key == "platformName":
                platform_name = desired_caps[key]
            elif re.match("[a-zA-Z0-9]*:[a-zA-Z0-9]*", key):
                extension_capabilities[key] = desired_caps[key]
        if selenium4_or_newer:
            chrome_options.set_capability("cloud:options", capabilities)
            if selenoid:
                snops = selenoid_options
                chrome_options.set_capability("selenoid:options", snops)
            if screen_resolution:
                scres = screen_resolution
                chrome_options.set_capability("screenResolution", scres)
            if browser_version:
                br_vers = browser_version
                chrome_options.set_capability("browserVersion", br_vers)
            if platform_name:
                plat_name = platform_name
                chrome_options.set_capability("platformName", plat_name)
            if extension_capabilities:
                for key in extension_capabilities:
                    ext_caps = extension_capabilities
                    chrome_options.set_capability(key, ext_caps[key])
            return webdriver.Remote(
                command_executor=address,
                options=chrome_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.FIREFOX:
        firefox_options = _set_firefox_options(
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            disable_js,
            disable_csp,
            firefox_arg,
            firefox_pref,
        )
        capabilities = None
        if selenium4_or_newer:
            capabilities = webdriver.FirefoxOptions().to_capabilities()
        else:
            capabilities = firefox_options.to_capabilities()
        capabilities["marionette"] = True
        if "linux" in PLATFORM:
            if headless:
                capabilities["moz:firefoxOptions"] = {"args": ["-headless"]}
        # Set custom desired capabilities
        selenoid = False
        selenoid_options = None
        screen_resolution = None
        browser_version = None
        platform_name = None
        extension_capabilities = {}
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
            if key == "selenoid:options":
                selenoid = True
                selenoid_options = desired_caps[key]
            elif key == "screenResolution":
                screen_resolution = desired_caps[key]
            elif key == "version" or key == "browserVersion":
                browser_version = desired_caps[key]
            elif key == "platform" or key == "platformName":
                platform_name = desired_caps[key]
            elif re.match("[a-zA-Z0-9]*:[a-zA-Z0-9]*", key):
                extension_capabilities[key] = desired_caps[key]
        if selenium4_or_newer:
            firefox_options.set_capability("cloud:options", capabilities)
            if selenoid:
                snops = selenoid_options
                firefox_options.set_capability("selenoid:options", snops)
            if screen_resolution:
                scres = screen_resolution
                firefox_options.set_capability("screenResolution", scres)
            if browser_version:
                br_vers = browser_version
                firefox_options.set_capability("browserVersion", br_vers)
            if platform_name:
                plat_name = platform_name
                firefox_options.set_capability("platformName", plat_name)
            if extension_capabilities:
                for key in extension_capabilities:
                    ext_caps = extension_capabilities
                    firefox_options.set_capability(key, ext_caps[key])
            return webdriver.Remote(
                command_executor=address,
                options=firefox_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.INTERNET_EXPLORER:
        capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
        if selenium4_or_newer:
            remote_options = ArgOptions()
            remote_options.set_capability("cloud:options", desired_caps)
            return webdriver.Remote(
                command_executor=address,
                options=remote_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            for key in desired_caps.keys():
                capabilities[key] = desired_caps[key]
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.EDGE:
        capabilities = webdriver.DesiredCapabilities.EDGE
        if selenium4_or_newer:
            remote_options = ArgOptions()
            remote_options.set_capability("cloud:options", desired_caps)
            return webdriver.Remote(
                command_executor=address,
                options=remote_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            for key in desired_caps.keys():
                capabilities[key] = desired_caps[key]
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.SAFARI:
        capabilities = webdriver.DesiredCapabilities.SAFARI
        if selenium4_or_newer:
            remote_options = ArgOptions()
            remote_options.set_capability("cloud:options", desired_caps)
            return webdriver.Remote(
                command_executor=address,
                options=remote_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            for key in desired_caps.keys():
                capabilities[key] = desired_caps[key]
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.OPERA:
        opera_options = _set_chrome_options(
            browser_name,
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_auth,
            proxy_user,
            proxy_pass,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            recorder_ext,
            disable_js,
            disable_csp,
            enable_ws,
            enable_sync,
            use_auto_ext,
            undetectable,
            uc_subprocess,
            no_sandbox,
            disable_gpu,
            headless2,
            incognito,
            guest_mode,
            devtools,
            remote_debug,
            swiftshader,
            ad_block_on,
            block_images,
            do_not_track,
            chromium_arg,
            user_data_dir,
            extension_zip,
            extension_dir,
            page_load_strategy,
            external_pdf,
            servername,
            mobile_emulator,
            device_width,
            device_height,
            device_pixel_ratio,
        )
        capabilities = None
        if selenium4_or_newer:
            capabilities = webdriver.DesiredCapabilities.OPERA
        else:
            opera_options = webdriver.opera.options.Options()
            capabilities = opera_options.to_capabilities()
        # Set custom desired capabilities
        selenoid = False
        selenoid_options = None
        screen_resolution = None
        browser_version = None
        platform_name = None
        extension_capabilities = {}
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
            if key == "selenoid:options":
                selenoid = True
                selenoid_options = desired_caps[key]
            elif key == "screenResolution":
                screen_resolution = desired_caps[key]
            elif key == "version" or key == "browserVersion":
                browser_version = desired_caps[key]
            elif key == "platform" or key == "platformName":
                platform_name = desired_caps[key]
            elif re.match("[a-zA-Z0-9]*:[a-zA-Z0-9]*", key):
                extension_capabilities[key] = desired_caps[key]
        if selenium4_or_newer:
            opera_options.set_capability("cloud:options", capabilities)
            if selenoid:
                snops = selenoid_options
                opera_options.set_capability("selenoid:options", snops)
            if screen_resolution:
                scres = screen_resolution
                opera_options.set_capability("screenResolution", scres)
            if browser_version:
                br_vers = browser_version
                opera_options.set_capability("browserVersion", br_vers)
            if platform_name:
                plat_name = platform_name
                opera_options.set_capability("platformName", plat_name)
            if extension_capabilities:
                for key in extension_capabilities:
                    ext_caps = extension_capabilities
                    opera_options.set_capability(key, ext_caps[key])
            return webdriver.Remote(
                command_executor=address,
                options=opera_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.PHANTOM_JS:
        if selenium4_or_newer:
            message = (
                "\n"
                "PhantomJS is no longer available for Selenium 4!\n"
                'Try using "--headless" mode with Chrome instead!'
            )
            raise Exception(message)
        capabilities = webdriver.DesiredCapabilities.PHANTOMJS
        for key in desired_caps.keys():
            capabilities[key] = desired_caps[key]
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.ANDROID:
        capabilities = webdriver.DesiredCapabilities.ANDROID
        if selenium4_or_newer:
            remote_options = ArgOptions()
            remote_options.set_capability("cloud:options", desired_caps)
            return webdriver.Remote(
                command_executor=address,
                options=remote_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            for key in desired_caps.keys():
                capabilities[key] = desired_caps[key]
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.IPHONE:
        capabilities = webdriver.DesiredCapabilities.IPHONE
        if selenium4_or_newer:
            remote_options = ArgOptions()
            remote_options.set_capability("cloud:options", desired_caps)
            return webdriver.Remote(
                command_executor=address,
                options=remote_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            for key in desired_caps.keys():
                capabilities[key] = desired_caps[key]
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.IPAD:
        capabilities = webdriver.DesiredCapabilities.IPAD
        if selenium4_or_newer:
            remote_options = ArgOptions()
            remote_options.set_capability("cloud:options", desired_caps)
            return webdriver.Remote(
                command_executor=address,
                options=remote_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            for key in desired_caps.keys():
                capabilities[key] = desired_caps[key]
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=capabilities,
                keep_alive=True,
            )
    elif browser_name == constants.Browser.REMOTE:
        if selenium4_or_newer:
            remote_options = ArgOptions()
            # shovel caps into remote options.
            for cap_name, cap_value in desired_caps.items():
                remote_options.set_capability(cap_name, cap_value)
            return webdriver.Remote(
                command_executor=address,
                options=remote_options,
                keep_alive=True,
            )
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Remote(
                command_executor=address,
                desired_capabilities=desired_caps,
                keep_alive=True,
            )


def get_local_driver(
    browser_name,
    headless,
    locale_code,
    servername,
    proxy_string,
    proxy_auth,
    proxy_user,
    proxy_pass,
    proxy_bypass_list,
    proxy_pac_url,
    user_agent,
    recorder_ext,
    disable_js,
    disable_csp,
    enable_ws,
    enable_sync,
    use_auto_ext,
    undetectable,
    uc_subprocess,
    no_sandbox,
    disable_gpu,
    headless2,
    incognito,
    guest_mode,
    devtools,
    remote_debug,
    swiftshader,
    ad_block_on,
    block_images,
    do_not_track,
    chromium_arg,
    firefox_arg,
    firefox_pref,
    user_data_dir,
    extension_zip,
    extension_dir,
    page_load_strategy,
    external_pdf,
    mobile_emulator,
    device_width,
    device_height,
    device_pixel_ratio,
):
    """
    Spins up a new web browser and returns the driver.
    Can also be used to spin up additional browsers for the same test.
    """
    downloads_path = DOWNLOADS_FOLDER

    if browser_name == constants.Browser.FIREFOX:
        firefox_options = _set_firefox_options(
            downloads_path,
            headless,
            locale_code,
            proxy_string,
            proxy_bypass_list,
            proxy_pac_url,
            user_agent,
            disable_js,
            disable_csp,
            firefox_arg,
            firefox_pref,
        )
        if LOCAL_GECKODRIVER and os.path.exists(LOCAL_GECKODRIVER):
            try:
                make_driver_executable_if_not(LOCAL_GECKODRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make geckodriver"
                    " executable: %s" % e
                )
        elif not geckodriver_on_path():
            from seleniumbase.console_scripts import sb_install

            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                sys_args = sys.argv  # Save a copy of current sys args
                print("\nWarning: geckodriver not found. Getting it now:")
                try:
                    sb_install.main(override="geckodriver")
                except Exception as e:
                    print("\nWarning: Could not install geckodriver: %s" % e)
                sys.argv = sys_args  # Put back the original sys args
            else:
                geckodriver_fixing_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                )
                with geckodriver_fixing_lock:
                    if not geckodriver_on_path():
                        sys_args = sys.argv  # Save a copy of sys args
                        print(
                            "\nWarning: geckodriver not found. "
                            "Getting it now:"
                        )
                        sb_install.main(override="geckodriver")
                        sys.argv = sys_args  # Put back original sys args
        # Launch Firefox
        if os.path.exists(LOCAL_GECKODRIVER):
            if selenium4_or_newer:
                service = FirefoxService(
                    executable_path=LOCAL_GECKODRIVER,
                    log_path=os.devnull,
                )
                try:
                    return webdriver.Firefox(
                        service=service,
                        options=firefox_options,
                    )
                except BaseException as e:
                    if (
                        "geckodriver unexpectedly exited" in str(e)
                        or "Process unexpectedly closed" in str(e)
                        or "Failed to read marionette port" in str(e)
                        or "A connection attempt failed" in str(e)
                        or hasattr(e, "msg") and (
                            "geckodriver unexpectedly exited" in e.msg
                            or "Process unexpectedly closed" in e.msg
                            or "Failed to read marionette port" in e.msg
                            or "A connection attempt failed" in e.msg
                        )
                    ):
                        # Firefox probably just auto-updated itself,
                        # which causes intermittent issues to occur.
                        # Trying again right after that often works.
                        time.sleep(0.1)
                        return webdriver.Firefox(
                            service=service,
                            options=firefox_options,
                        )
                    else:
                        raise  # Not an obvious fix.
            else:
                return webdriver.Firefox(
                    executable_path=LOCAL_GECKODRIVER,
                    service_log_path=os.devnull,
                    options=firefox_options,
                )
        else:
            if selenium4_or_newer:
                service = FirefoxService(log_path=os.devnull)
                try:
                    return webdriver.Firefox(
                        service=service, options=firefox_options
                    )
                except BaseException as e:
                    if (
                        "geckodriver unexpectedly exited" in str(e)
                        or "Process unexpectedly closed" in str(e)
                        or "Failed to read marionette port" in str(e)
                        or "A connection attempt failed" in str(e)
                        or hasattr(e, "msg") and (
                            "geckodriver unexpectedly exited" in e.msg
                            or "Process unexpectedly closed" in e.msg
                            or "Failed to read marionette port" in e.msg
                            or "A connection attempt failed" in e.msg
                        )
                    ):
                        # Firefox probably just auto-updated itself,
                        # which causes intermittent issues to occur.
                        # Trying again right after that often works.
                        time.sleep(0.1)
                        return webdriver.Firefox(
                            service=service,
                            options=firefox_options,
                        )
                    else:
                        raise  # Not an obvious fix.
            else:
                return webdriver.Firefox(
                    service_log_path=os.devnull,
                    options=firefox_options,
                )
    elif browser_name == constants.Browser.INTERNET_EXPLORER:
        if not IS_WINDOWS:
            raise Exception(
                "IE Browser is for Windows-based operating systems only!"
            )
        from selenium.webdriver.ie.options import Options

        ie_options = Options()
        ie_options.ignore_protected_mode_settings = True
        ie_options.ignore_zoom_level = True
        ie_options.require_window_focus = False
        ie_options.native_events = True
        ie_options.full_page_screenshot = True
        ie_options.persistent_hover = True
        ie_capabilities = ie_options.to_capabilities()
        if LOCAL_IEDRIVER and os.path.exists(LOCAL_IEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_IEDRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make IEDriver executable: %s" % e
                )
        elif not iedriver_on_path():
            from seleniumbase.console_scripts import sb_install

            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                sys_args = sys.argv  # Save a copy of current sys args
                print("\nWarning: IEDriver not found. Getting it now:")
                sb_install.main(override="iedriver")
                sys.argv = sys_args  # Put back the original sys args
        if LOCAL_HEADLESS_IEDRIVER and os.path.exists(LOCAL_HEADLESS_IEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_HEADLESS_IEDRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make HeadlessIEDriver executable: %s"
                    % e
                )
        elif not headless_iedriver_on_path():
            from seleniumbase.console_scripts import sb_install

            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                sys_args = sys.argv  # Save a copy of current sys args
                print("\nWarning: HeadlessIEDriver not found. Getting it now:")
                sb_install.main(override="iedriver")
                sys.argv = sys_args  # Put back the original sys args
        if not headless:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Ie(capabilities=ie_capabilities)
        else:
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Ie(
                executable_path=LOCAL_HEADLESS_IEDRIVER,
                capabilities=ie_capabilities,
            )
    elif browser_name == constants.Browser.EDGE:
        prefs = {
            "download.default_directory": downloads_path,
            "local_discovery.notifications_enabled": False,
            "credentials_enable_service": False,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True,
            "default_content_setting_values.notifications": 0,
            "default_content_settings.popups": 0,
            "managed_default_content_settings.popups": 0,
            "content_settings.exceptions.automatic_downloads.*.setting": 1,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads": 1,
        }
        if LOCAL_EDGEDRIVER and os.path.exists(LOCAL_EDGEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_EDGEDRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make edgedriver"
                    " executable: %s" % e
                )
        elif not edgedriver_on_path():
            from seleniumbase.console_scripts import sb_install

            args = " ".join(sys.argv)
            if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                # (Not multithreaded)
                sys_args = sys.argv  # Save a copy of current sys args
                print("\nWarning: msedgedriver not found. Getting it now:")
                sb_install.main(override="edgedriver")
                sys.argv = sys_args  # Put back the original sys args
            else:
                edgedriver_fixing_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                )
                with edgedriver_fixing_lock:
                    if not edgedriver_on_path():
                        sys_args = sys.argv  # Save a copy of sys args
                        print(
                            "\nWarning: msedgedriver not found. "
                            "Getting it now:"
                        )
                        sb_install.main(override="edgedriver")
                        sys.argv = sys_args  # Put back original sys args

        # For Microsoft Edge (Chromium) version 80 or higher
        if selenium4_or_newer:
            Edge = webdriver.edge.webdriver.WebDriver
            EdgeOptions = webdriver.edge.webdriver.Options
        else:
            from msedge.selenium_tools import Edge, EdgeOptions

        if LOCAL_EDGEDRIVER and os.path.exists(LOCAL_EDGEDRIVER):
            try:
                make_driver_executable_if_not(LOCAL_EDGEDRIVER)
            except Exception as e:
                logging.debug(
                    "\nWarning: Could not make edgedriver"
                    " executable: %s" % e
                )
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        if locale_code:
            prefs["intl.accept_languages"] = locale_code
        if block_images:
            prefs["profile.managed_default_content_settings.images"] = 2
        if disable_js:
            prefs["profile.managed_default_content_settings.javascript"] = 2
        if do_not_track:
            prefs["enable_do_not_track"] = True
        if external_pdf:
            prefs["plugins.always_open_pdf_externally"] = True
        edge_options.add_experimental_option("prefs", prefs)
        if not selenium4_or_newer:
            edge_options.add_experimental_option("w3c", True)
        edge_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        edge_options.add_experimental_option("useAutomationExtension", False)
        edge_options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        if not enable_sync:
            edge_options.add_argument("--disable-sync")
        if guest_mode:
            edge_options.add_argument("--guest")
        if headless2:
            edge_options.add_argument("--headless=chrome")
        elif headless:
            edge_options.add_argument("--headless")
        if mobile_emulator:
            emulator_settings = {}
            device_metrics = {}
            if (
                type(device_width) is int
                and type(device_height) is int
                and type(device_pixel_ratio) is int
            ):
                device_metrics["width"] = device_width
                device_metrics["height"] = device_height
                device_metrics["pixelRatio"] = device_pixel_ratio
            else:
                device_metrics["width"] = 360
                device_metrics["height"] = 640
                device_metrics["pixelRatio"] = 2
            emulator_settings["deviceMetrics"] = device_metrics
            if user_agent:
                emulator_settings["userAgent"] = user_agent
            edge_options.add_experimental_option(
                "mobileEmulation", emulator_settings
            )
        if user_data_dir:
            abs_path = os.path.abspath(user_data_dir)
            edge_options.add_argument("user-data-dir=%s" % abs_path)
        if extension_zip:
            # Can be a comma-separated list of .ZIP or .CRX files
            extension_zip_list = extension_zip.split(",")
            for extension_zip_item in extension_zip_list:
                abs_path = os.path.abspath(extension_zip_item)
                edge_options.add_extension(abs_path)
        if extension_dir:
            # load-extension input can be a comma-separated list
            abs_path = os.path.abspath(extension_dir)
            edge_options = add_chrome_ext_dir(edge_options, abs_path)
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-save-password-bubble")
        edge_options.add_argument("--disable-single-click-autofill")
        edge_options.add_argument(
            "--disable-autofill-keyboard-accessory-view[8]"
        )
        edge_options.add_argument("--disable-browser-side-navigation")
        edge_options.add_argument("--disable-translate")
        if not enable_ws:
            edge_options.add_argument("--disable-web-security")
        edge_options.add_argument("--homepage=about:blank")
        edge_options.add_argument("--dns-prefetch-disable")
        edge_options.add_argument("--dom-automation")
        edge_options.add_argument("--disable-hang-monitor")
        edge_options.add_argument("--disable-prompt-on-repost")
        edge_options.add_argument("--disable-3d-apis")
        if (
            selenium4_or_newer
            and page_load_strategy
            and page_load_strategy.lower() in ["eager", "none"]
        ):
            # Only change it if not "normal", which is the default.
            edge_options.page_load_strategy = page_load_strategy.lower()
        elif (
            selenium4_or_newer
            and not page_load_strategy
            and hasattr(settings, "PAGE_LOAD_STRATEGY")
            and settings.PAGE_LOAD_STRATEGY
            and settings.PAGE_LOAD_STRATEGY.lower() in ["eager", "none"]
        ):
            # Only change it if not "normal", which is the default.
            edge_options.page_load_strategy = (
                settings.PAGE_LOAD_STRATEGY.lower()
            )
        if (settings.DISABLE_CSP_ON_CHROME or disable_csp) and not headless:
            # Headless Edge doesn't support extensions, which are required
            # for disabling the Content Security Policy on Edge
            edge_options = _add_chrome_disable_csp_extension(edge_options)
        if ad_block_on and not headless:
            edge_options = _add_chrome_ad_block_extension(edge_options)
        if recorder_ext and not headless:
            edge_options = _add_chrome_recorder_extension(edge_options)
        if proxy_string:
            if proxy_auth:
                edge_options = _add_chrome_proxy_extension(
                    edge_options, proxy_string, proxy_user, proxy_pass
                )
            edge_options.add_argument("--proxy-server=%s" % proxy_string)
            if proxy_bypass_list:
                edge_options.add_argument(
                    "--proxy-bypass-list=%s" % proxy_bypass_list
                )
        elif proxy_pac_url:
            if proxy_auth:
                edge_options = _add_chrome_proxy_extension(
                    edge_options, None, proxy_user, proxy_pass
                )
            edge_options.add_argument("--proxy-pac-url=%s" % proxy_pac_url)
        edge_options.add_argument("--test-type")
        edge_options.add_argument("--log-level=3")
        edge_options.add_argument("--no-first-run")
        edge_options.add_argument("--ignore-certificate-errors")
        if devtools and not headless:
            edge_options.add_argument("--auto-open-devtools-for-tabs")
        edge_options.add_argument("--allow-file-access-from-files")
        edge_options.add_argument("--allow-insecure-localhost")
        edge_options.add_argument("--allow-running-insecure-content")
        if user_agent:
            edge_options.add_argument("--user-agent=%s" % user_agent)
        edge_options.add_argument("--no-sandbox")
        if remote_debug:
            # To access the Remote Debugger, go to: http://localhost:9222
            # while a Chromium driver is running.
            # Info: https://chromedevtools.github.io/devtools-protocol/
            edge_options.add_argument("--remote-debugging-port=9222")
        if swiftshader:
            edge_options.add_argument("--use-gl=swiftshader")
        else:
            edge_options.add_argument("--disable-gpu")
        if "linux" in PLATFORM:
            edge_options.add_argument("--disable-dev-shm-usage")
        if chromium_arg:
            # Can be a comma-separated list of Chromium args
            chromium_arg_list = chromium_arg.split(",")
            for chromium_arg_item in chromium_arg_list:
                chromium_arg_item = chromium_arg_item.strip()
                if not chromium_arg_item.startswith("--"):
                    if chromium_arg_item.startswith("-"):
                        chromium_arg_item = "-" + chromium_arg_item
                    else:
                        chromium_arg_item = "--" + chromium_arg_item
                if len(chromium_arg_item) >= 3:
                    edge_options.add_argument(chromium_arg_item)
        if selenium4_or_newer:
            try:
                service = EdgeService(
                    executable_path=LOCAL_EDGEDRIVER, log_path=os.devnull
                )
                driver = Edge(service=service, options=edge_options)
            except Exception as e:
                if not hasattr(e, "msg"):
                    raise
                auto_upgrade_edgedriver = False
                edge_version = None
                if (
                    "This version of MSEdgeDriver only supports" in e.msg
                    or "This version of Microsoft Edge WebDriver" in e.msg
                ):
                    if "Current browser version is " in e.msg:
                        auto_upgrade_edgedriver = True
                        edge_version = e.msg.split(
                            "Current browser version is "
                        )[1].split(" ")[0]
                    elif "only supports MSEdge version " in e.msg:
                        auto_upgrade_edgedriver = True
                        edge_version = e.msg.split(
                            "only supports MSEdge version "
                        )[1].split(" ")[0]
                elif "DevToolsActivePort file doesn't exist" in e.msg:
                    service = EdgeService(
                        executable_path=LOCAL_EDGEDRIVER,
                        log_path=os.devnull,
                    )
                    # https://stackoverflow.com/a/56638103/7058266
                    edge_options.add_argument("--remote-debugging-port=9222")
                    return Edge(service=service, options=edge_options)
                if not auto_upgrade_edgedriver:
                    raise  # Not an obvious fix.
                else:
                    pass  # Try upgrading EdgeDriver to match Edge.
                args = " ".join(sys.argv)
                if "-n" in sys.argv or " -n=" in args or args == "-c":
                    edgedriver_fixing_lock = fasteners.InterProcessLock(
                        constants.MultiBrowser.DRIVER_FIXING_LOCK
                    )
                    with edgedriver_fixing_lock:
                        try:
                            if not _was_driver_repaired():
                                _repair_edgedriver(edge_version)
                                _mark_driver_repaired()
                        except Exception:
                            pass
                else:
                    try:
                        if not _was_driver_repaired():
                            _repair_edgedriver(edge_version)
                        _mark_driver_repaired()
                    except Exception:
                        pass
                service = EdgeService(
                    executable_path=LOCAL_EDGEDRIVER,
                    log_path=os.devnull,
                    service_args=["--disable-build-check"],
                )
                driver = Edge(service=service, options=edge_options)
            return driver
        else:
            capabilities = edge_options.to_capabilities()
            capabilities["platform"] = ""
            try:
                driver = Edge(
                    executable_path=LOCAL_EDGEDRIVER,
                    service_log_path=os.devnull,
                    capabilities=capabilities,
                )
            except Exception as e:
                if not hasattr(e, "msg"):
                    raise
                auto_upgrade_edgedriver = False
                edge_version = None
                if (
                    "This version of MSEdgeDriver only supports" in e.msg
                    or "This version of Microsoft Edge WebDriver" in e.msg
                ):
                    if "Current browser version is " in e.msg:
                        auto_upgrade_edgedriver = True
                        edge_version = e.msg.split(
                            "Current browser version is "
                        )[1].split(" ")[0]
                    elif "only supports MSEdge version " in e.msg:
                        auto_upgrade_edgedriver = True
                        edge_version = e.msg.split(
                            "only supports MSEdge version "
                        )[1].split(" ")[0]
                elif "DevToolsActivePort file doesn't exist" in e.msg:
                    service = EdgeService(
                        executable_path=LOCAL_EDGEDRIVER,
                        log_path=os.devnull,
                    )
                    # https://stackoverflow.com/a/56638103/7058266
                    edge_options.add_argument("--remote-debugging-port=9222")
                    return Edge(service=service, options=edge_options)
                if not auto_upgrade_edgedriver:
                    raise  # Not an obvious fix.
                else:
                    pass  # Try upgrading EdgeDriver to match Edge.
                args = " ".join(sys.argv)
                if "-n" in sys.argv or " -n=" in args or args == "-c":
                    edgedriver_fixing_lock = fasteners.InterProcessLock(
                        constants.MultiBrowser.DRIVER_FIXING_LOCK
                    )
                    with edgedriver_fixing_lock:
                        if not _was_driver_repaired():
                            _repair_edgedriver(edge_version)
                            _mark_driver_repaired()
                else:
                    if not _was_driver_repaired():
                        _repair_edgedriver(edge_version)
                    _mark_driver_repaired()
                driver = Edge(
                    executable_path=LOCAL_EDGEDRIVER,
                    service_log_path=os.devnull,
                    service_args=["--disable-build-check"],
                    capabilities=capabilities,
                )
            return driver
    elif browser_name == constants.Browser.SAFARI:
        arg_join = " ".join(sys.argv)
        if ("-n" in sys.argv) or (" -n=" in arg_join) or (arg_join == "-c"):
            # Skip if multithreaded
            raise Exception("Can't run Safari tests in multithreaded mode!")
        warnings.simplefilter("ignore", category=DeprecationWarning)
        return webdriver.safari.webdriver.WebDriver(quiet=False)
    elif browser_name == constants.Browser.OPERA:
        try:
            if LOCAL_OPERADRIVER and os.path.exists(LOCAL_OPERADRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_OPERADRIVER)
                except Exception as e:
                    logging.debug(
                        "\nWarning: Could not make operadriver"
                        " executable: %s" % e
                    )
            # Opera Chromium doesn't support headless mode.
            # https://github.com/operasoftware/operachromiumdriver/issues/62
            headless = False
            opera_options = _set_chrome_options(
                browser_name,
                downloads_path,
                headless,
                locale_code,
                proxy_string,
                proxy_auth,
                proxy_user,
                proxy_pass,
                proxy_bypass_list,
                proxy_pac_url,
                user_agent,
                recorder_ext,
                disable_js,
                disable_csp,
                enable_ws,
                enable_sync,
                use_auto_ext,
                undetectable,
                uc_subprocess,
                no_sandbox,
                disable_gpu,
                headless2,
                incognito,
                guest_mode,
                devtools,
                remote_debug,
                swiftshader,
                ad_block_on,
                block_images,
                do_not_track,
                chromium_arg,
                user_data_dir,
                extension_zip,
                extension_dir,
                page_load_strategy,
                external_pdf,
                servername,
                mobile_emulator,
                device_width,
                device_height,
                device_pixel_ratio,
            )
            opera_options.headless = False  # No support for headless Opera
            warnings.simplefilter("ignore", category=DeprecationWarning)
            return webdriver.Opera(options=opera_options)
        except Exception:
            # Opera support was dropped! Downgrade to Python 3.6 to use it!
            return webdriver.Opera()
    elif browser_name == constants.Browser.PHANTOM_JS:
        if selenium4_or_newer:
            message = (
                "\n"
                "PhantomJS is no longer available for Selenium 4!\n"
                'Try using "--headless" mode with Chrome instead!'
            )
            raise Exception(message)
        with warnings.catch_warnings():
            # Ignore "PhantomJS has been deprecated" UserWarning
            warnings.simplefilter("ignore", category=UserWarning)
            return webdriver.PhantomJS()
    elif browser_name == constants.Browser.GOOGLE_CHROME:
        try:
            chrome_options = _set_chrome_options(
                browser_name,
                downloads_path,
                headless,
                locale_code,
                proxy_string,
                proxy_auth,
                proxy_user,
                proxy_pass,
                proxy_bypass_list,
                proxy_pac_url,
                user_agent,
                recorder_ext,
                disable_js,
                disable_csp,
                enable_ws,
                enable_sync,
                use_auto_ext,
                undetectable,
                uc_subprocess,
                no_sandbox,
                disable_gpu,
                headless2,
                incognito,
                guest_mode,
                devtools,
                remote_debug,
                swiftshader,
                ad_block_on,
                block_images,
                do_not_track,
                chromium_arg,
                user_data_dir,
                extension_zip,
                extension_dir,
                page_load_strategy,
                external_pdf,
                servername,
                mobile_emulator,
                device_width,
                device_height,
                device_pixel_ratio,
            )
            use_version = "latest"
            major_chrome_version = None
            if selenium4_or_newer:
                try:
                    from seleniumbase.core import detect_b_ver

                    br_app = "google-chrome"
                    major_chrome_version = (
                        detect_b_ver.get_browser_version_from_os(br_app)
                    ).split(".")[0]
                    if int(major_chrome_version) < 67:
                        major_chrome_version = None
                    elif (
                        int(major_chrome_version) >= 67
                        and int(major_chrome_version) <= 72
                    ):
                        # chromedrivers 2.41 - 2.46 could be swapped with 72
                        major_chrome_version = "72"
                except Exception:
                    major_chrome_version = None
            if major_chrome_version:
                use_version = major_chrome_version
            driver_version = None
            path_chromedriver = chromedriver_on_path()
            if os.path.exists(LOCAL_CHROMEDRIVER):
                try:
                    output = subprocess.check_output(
                        "%s --version" % LOCAL_CHROMEDRIVER, shell=True
                    )
                    if IS_WINDOWS:
                        output = output.decode("latin1")
                    else:
                        output = output.decode("utf-8")
                    output = output.split(" ")[1].split(".")[0]
                    if int(output) >= 2:
                        driver_version = output
                except Exception:
                    pass
            elif path_chromedriver:
                try:
                    output = subprocess.check_output(
                        "%s --version" % path_chromedriver, shell=True
                    )
                    if IS_WINDOWS:
                        output = output.decode("latin1")
                    else:
                        output = output.decode("utf-8")
                    output = output.split(" ")[1].split(".")[0]
                    if int(output) >= 2:
                        driver_version = output
                except Exception:
                    pass
            disable_build_check = False
            if (
                LOCAL_CHROMEDRIVER
                and os.path.exists(LOCAL_CHROMEDRIVER)
                and (
                    use_version == driver_version
                    or use_version == "latest"
                )
            ):
                try:
                    make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                except Exception as e:
                    logging.debug(
                        "\nWarning: Could not make chromedriver"
                        " executable: %s" % e
                    )
            elif (
                not path_chromedriver
                or (
                    use_version != "latest"
                    and driver_version
                    and use_version != driver_version
                    and (
                        selenium4_or_newer
                        or driver_version != "72"
                    )
                )
            ):
                # chromedriver download needed in the seleniumbase/drivers dir
                from seleniumbase.console_scripts import sb_install

                args = " ".join(sys.argv)
                if not ("-n" in sys.argv or " -n=" in args or args == "-c"):
                    # (Not multithreaded)
                    sys_args = sys.argv  # Save a copy of current sys args
                    msg = "chromedriver update needed. Getting it now:"
                    if not path_chromedriver:
                        msg = "chromedriver not found. Getting it now:"

                    print("\nWarning: %s" % msg)
                    try:
                        sb_install.main(
                            override="chromedriver %s" % use_version
                        )
                    except Exception:
                        d_latest = get_latest_chromedriver_version()
                        if (
                            d_latest
                            and use_version != "latest"
                            and int(use_version) > int(d_latest.split(".")[0])
                        ):
                            disable_build_check = True
                            d_latest_major = d_latest.split(".")[0]
                            if (
                                not path_chromedriver
                                or (
                                    driver_version
                                    and (
                                        int(driver_version)
                                        < int(d_latest_major)
                                    )
                                )
                            ):
                                sb_install.main(
                                    override="chromedriver latest"
                                )
                    sys.argv = sys_args  # Put back the original sys args
                else:
                    chromedriver_fixing_lock = fasteners.InterProcessLock(
                        constants.MultiBrowser.DRIVER_FIXING_LOCK
                    )
                    with chromedriver_fixing_lock:
                        if not chromedriver_on_path():
                            sys_args = sys.argv  # Save a copy of sys args
                            msg = "chromedriver not found. Getting it now:"
                            print("\nWarning: %s" % msg)
                            try:
                                sb_install.main(
                                    override="chromedriver %s" % use_version
                                )
                            except Exception:
                                d_latest = get_latest_chromedriver_version()
                                if (
                                    d_latest
                                    and use_version != "latest"
                                    and (
                                        int(use_version)
                                        > int(d_latest.split(".")[0])
                                    )
                                ):
                                    disable_build_check = True
                                    d_latest_major = d_latest.split(".")[0]
                                    if (
                                        not path_chromedriver
                                        or (
                                            driver_version
                                            and (
                                                int(driver_version)
                                                < int(d_latest_major)
                                            )
                                        )
                                    ):
                                        sb_install.main(
                                            override="chromedriver latest"
                                        )
                            sys.argv = sys_args  # Put back original sys args
            service_args = []
            if disable_build_check:
                service_args = ["--disable-build-check"]
            if is_using_uc(undetectable, browser_name):
                uc_lock = fasteners.InterProcessLock(
                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                )
                with uc_lock:  # No UC multithreaded tests
                    uc_driver_version = None
                    if os.path.exists(LOCAL_UC_DRIVER):
                        try:
                            output = subprocess.check_output(
                                "%s --version" % LOCAL_UC_DRIVER, shell=True
                            )
                            if IS_WINDOWS:
                                output = output.decode("latin1")
                            else:
                                output = output.decode("utf-8")
                            output = output.split(" ")[1].split(".")[0]
                            if int(output) >= 72:
                                uc_driver_version = output
                        except Exception:
                            pass
                    if (
                        uc_driver_version != use_version
                        and use_version != "latest"
                    ):
                        if os.path.exists(LOCAL_CHROMEDRIVER):
                            shutil.copyfile(
                                LOCAL_CHROMEDRIVER, LOCAL_UC_DRIVER
                            )
                        elif os.path.exists(path_chromedriver):
                            shutil.copyfile(
                                path_chromedriver, LOCAL_UC_DRIVER
                            )
                        try:
                            make_driver_executable_if_not(LOCAL_UC_DRIVER)
                        except Exception as e:
                            logging.debug(
                                "\nWarning: Could not make uc_driver"
                                " executable: %s" % e
                            )
            if (
                not headless
                or "linux" not in PLATFORM
                or is_using_uc(undetectable, browser_name)
            ):
                try:
                    if (
                        os.path.exists(LOCAL_CHROMEDRIVER)
                        or is_using_uc(undetectable, browser_name)
                    ):
                        if selenium4_or_newer:
                            if headless and "linux" not in PLATFORM:
                                undetectable = False  # No support for headless
                            if undetectable:
                                from seleniumbase import undetected
                                from urllib.error import URLError

                                if "linux" in PLATFORM:
                                    chrome_options.headless = False  # Use Xvfb
                                    if "--headless" in (
                                        chrome_options.arguments
                                    ):
                                        chrome_options.arguments.remove(
                                            "--headless"
                                        )
                                cert = "unable to get local issuer certificate"
                                uc_chrome_version = None
                                if (
                                    use_version.isnumeric
                                    and int(use_version) >= 72
                                ):
                                    uc_chrome_version = int(use_version)
                                uc_lock = fasteners.InterProcessLock(
                                    constants.MultiBrowser.DRIVER_FIXING_LOCK
                                )
                                with uc_lock:
                                    try:
                                        uc_path = None
                                        if os.path.exists(LOCAL_UC_DRIVER):
                                            uc_path = LOCAL_UC_DRIVER
                                            uc_path = os.path.realpath(uc_path)
                                        driver = undetected.Chrome(
                                            options=chrome_options,
                                            user_data_dir=user_data_dir,
                                            driver_executable_path=uc_path,
                                            headless=False,  # Xvfb needed!
                                            version_main=uc_chrome_version,
                                            use_subprocess=uc_subprocess,
                                        )
                                    except URLError as e:
                                        if (
                                            cert in e.args[0]
                                            and "darwin" in PLATFORM
                                        ):
                                            os.system(
                                                r"bash /Applications/Python*/"
                                                r"Install\ "
                                                r"Certificates.command"
                                            )
                                            driver = undetected.Chrome(
                                                options=chrome_options,
                                                user_data_dir=user_data_dir,
                                                driver_executable_path=uc_path,
                                                headless=False,  # Xvfb needed!
                                                version_main=uc_chrome_version,
                                                use_subprocess=uc_subprocess,
                                            )
                                        else:
                                            raise
                            else:
                                service = ChromeService(
                                    executable_path=LOCAL_CHROMEDRIVER,
                                    log_path=os.devnull,
                                    service_args=service_args,
                                )
                                driver = webdriver.Chrome(
                                    service=service,
                                    options=chrome_options,
                                )
                        else:
                            driver = webdriver.Chrome(
                                executable_path=LOCAL_CHROMEDRIVER,
                                service_log_path=os.devnull,
                                service_args=service_args,
                                options=chrome_options,
                            )
                    else:
                        if selenium4_or_newer:
                            service = ChromeService(
                                log_path=os.devnull,
                                service_args=service_args,
                            )
                            driver = webdriver.Chrome(
                                service=service,
                                options=chrome_options,
                            )
                        else:
                            driver = webdriver.Chrome(
                                service_log_path=os.devnull,
                                service_args=service_args,
                                options=chrome_options,
                            )
                except Exception as e:
                    if not hasattr(e, "msg"):
                        raise
                    auto_upgrade_chromedriver = False
                    if "This version of ChromeDriver only supports" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Chrome version must be between" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Missing or invalid capabilities" in e.msg:
                        if selenium4_or_newer:
                            chrome_options.add_experimental_option("w3c", True)
                            service = ChromeService(log_path=os.devnull)
                            with warnings.catch_warnings():
                                warnings.simplefilter(
                                    "ignore", category=DeprecationWarning
                                )
                                return webdriver.Chrome(
                                    service=service, options=chrome_options
                                )
                        else:
                            raise
                    if not auto_upgrade_chromedriver:
                        raise  # Not an obvious fix.
                    else:
                        pass  # Try upgrading ChromeDriver to match Chrome.
                    mcv = None  # Major Chrome Version
                    if "Current browser version is " in e.msg:
                        line = e.msg.split("Current browser version is ")[1]
                        browser_version = line.split(" ")[0]
                        major_chrome_version = browser_version.split(".")[0]
                        if (
                            major_chrome_version.isnumeric()
                            and int(major_chrome_version) >= 86
                        ):
                            mcv = major_chrome_version
                    headless = True
                    headless_options = _set_chrome_options(
                        browser_name,
                        downloads_path,
                        headless,
                        locale_code,
                        proxy_string,
                        proxy_auth,
                        proxy_user,
                        proxy_pass,
                        proxy_bypass_list,
                        proxy_pac_url,
                        user_agent,
                        recorder_ext,
                        disable_js,
                        disable_csp,
                        enable_ws,
                        enable_sync,
                        use_auto_ext,
                        undetectable,
                        uc_subprocess,
                        no_sandbox,
                        disable_gpu,
                        headless2,
                        incognito,
                        guest_mode,
                        devtools,
                        remote_debug,
                        swiftshader,
                        ad_block_on,
                        block_images,
                        do_not_track,
                        chromium_arg,
                        user_data_dir,
                        extension_zip,
                        extension_dir,
                        page_load_strategy,
                        external_pdf,
                        servername,
                        mobile_emulator,
                        device_width,
                        device_height,
                        device_pixel_ratio,
                    )
                    args = " ".join(sys.argv)
                    if "-n" in sys.argv or " -n=" in args or args == "-c":
                        chromedriver_fixing_lock = fasteners.InterProcessLock(
                            constants.MultiBrowser.DRIVER_FIXING_LOCK
                        )
                        with chromedriver_fixing_lock:
                            if not _was_driver_repaired():
                                _repair_chromedriver(
                                    chrome_options, headless_options, mcv
                                )
                                _mark_driver_repaired()
                    else:
                        if not _was_driver_repaired():
                            _repair_chromedriver(
                                chrome_options, headless_options, mcv
                            )
                        _mark_driver_repaired()
                    if os.path.exists(LOCAL_CHROMEDRIVER):
                        if selenium4_or_newer:
                            service = ChromeService(
                                executable_path=LOCAL_CHROMEDRIVER,
                                service_args=["--disable-build-check"],
                            )
                            driver = webdriver.Chrome(
                                service=service,
                                options=chrome_options,
                            )
                        else:
                            driver = webdriver.Chrome(
                                executable_path=LOCAL_CHROMEDRIVER,
                                service_args=["--disable-build-check"],
                                options=chrome_options,
                            )
                    else:
                        if selenium4_or_newer:
                            service = ChromeService(
                                service_args=["--disable-build-check"],
                            )
                            driver = webdriver.Chrome(
                                service=service,
                                options=chrome_options,
                            )
                        else:
                            driver = webdriver.Chrome(
                                service_args=["--disable-build-check"],
                                options=chrome_options,
                            )
                return driver
            else:  # Running headless on Linux (and not using --uc)
                try:
                    return webdriver.Chrome(options=chrome_options)
                except Exception as e:
                    if not hasattr(e, "msg"):
                        raise
                    auto_upgrade_chromedriver = False
                    if "This version of ChromeDriver only supports" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Chrome version must be between" in e.msg:
                        auto_upgrade_chromedriver = True
                    elif "Missing or invalid capabilities" in e.msg:
                        if selenium4_or_newer:
                            chrome_options.add_experimental_option("w3c", True)
                            service = ChromeService(log_path=os.devnull)
                            with warnings.catch_warnings():
                                warnings.simplefilter(
                                    "ignore", category=DeprecationWarning
                                )
                                return webdriver.Chrome(
                                    service=service, options=chrome_options
                                )
                        else:
                            raise
                    mcv = None  # Major Chrome Version
                    if "Current browser version is " in e.msg:
                        line = e.msg.split("Current browser version is ")[1]
                        browser_version = line.split(" ")[0]
                        major_chrome_version = browser_version.split(".")[0]
                        if (
                            major_chrome_version.isnumeric()
                            and int(major_chrome_version) >= 86
                        ):
                            mcv = major_chrome_version
                    if auto_upgrade_chromedriver:
                        args = " ".join(sys.argv)
                        if "-n" in sys.argv or " -n=" in args or args == "-c":
                            chromedr_fixing_lock = fasteners.InterProcessLock(
                                constants.MultiBrowser.DRIVER_FIXING_LOCK
                            )
                            with chromedr_fixing_lock:
                                if not _was_driver_repaired():
                                    try:
                                        _repair_chromedriver(
                                            chrome_options, chrome_options, mcv
                                        )
                                        _mark_driver_repaired()
                                    except Exception:
                                        pass
                        else:
                            if not _was_driver_repaired():
                                try:
                                    _repair_chromedriver(
                                        chrome_options, chrome_options, mcv
                                    )
                                except Exception:
                                    pass
                            _mark_driver_repaired()
                        try:
                            if selenium4_or_newer:
                                service = ChromeService(
                                    service_args=["--disable-build-check"],
                                )
                                return webdriver.Chrome(
                                    service=service,
                                    options=chrome_options,
                                )
                            else:
                                return webdriver.Chrome(
                                    service_args=["--disable-build-check"],
                                    options=chrome_options,
                                )
                        except Exception:
                            pass
                    # Use the virtual display on Linux during headless errors
                    logging.debug(
                        "\nWarning: Chrome failed to launch in"
                        " headless mode. Attempting to use the"
                        " SeleniumBase virtual display on Linux..."
                    )
                    chrome_options.headless = False
                    return webdriver.Chrome(options=chrome_options)
        except Exception:
            try:
                # Try again if Chrome didn't launch
                return webdriver.Chrome(options=chrome_options)
            except Exception:
                pass
            if headless:
                raise
            if LOCAL_CHROMEDRIVER and os.path.exists(LOCAL_CHROMEDRIVER):
                try:
                    make_driver_executable_if_not(LOCAL_CHROMEDRIVER)
                except Exception as e:
                    logging.debug(
                        "\nWarning: Could not make chromedriver"
                        " executable: %s" % e
                    )
            return webdriver.Chrome()
    else:
        raise Exception(
            "%s is not a valid browser option for this system!" % browser_name
        )
