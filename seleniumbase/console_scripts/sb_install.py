"""
Downloads the specified webdriver to "seleniumbase/drivers/"

Usage:
         sbase get {chromedriver|geckodriver|edgedriver|
                    iedriver|uc_driver} [OPTIONS]
Options:
         VERSION         Specify the version.
                         Tries to detect the needed version.
                         If using chromedriver or edgedriver,
                         you can use the major version integer.
         -p OR --path    Also copy the driver to /usr/local/bin
Examples:
         sbase get chromedriver
         sbase get geckodriver
         sbase get edgedriver
         sbase get chromedriver 114
         sbase get chromedriver 114.0.5735.90
         sbase get chromedriver stable
         sbase get chromedriver beta
         sbase get chromedriver -p
Output:
         Downloads the webdriver to seleniumbase/drivers/
         (chromedriver is required for Chrome automation)
         (geckodriver is required for Firefox automation)
         (edgedriver is required for MS__Edge automation)
"""
import colorama
import logging
import os
import platform
import requests
import shutil
import sys
import time
import tarfile
import urllib3
import zipfile
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import shared_utils
from seleniumbase import config as sb_config
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase

urllib3.disable_warnings()
ARCH = platform.architecture()[0]
IS_ARM_MAC = shared_utils.is_arm_mac()
IS_MAC = shared_utils.is_mac()
IS_LINUX = shared_utils.is_linux()
IS_WINDOWS = shared_utils.is_windows()
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
LOCAL_PATH = "/usr/local/bin/"  # On Mac and Linux systems
DEFAULT_CHROMEDRIVER_VERSION = "114.0.5735.90"  # (If can't find LATEST_STABLE)
DEFAULT_GECKODRIVER_VERSION = "v0.35.0"
DEFAULT_EDGEDRIVER_VERSION = "115.0.1901.183"  # (If can't find LATEST_STABLE)


def invalid_run_command():
    exp = "  ** get / install **\n\n"
    exp += "  Usage:\n"
    exp += "           seleniumbase install [DRIVER] [OPTIONS]\n"
    exp += "           OR     sbase install [DRIVER] [OPTIONS]\n"
    exp += "           OR  seleniumbase get [DRIVER] [OPTIONS]\n"
    exp += "           OR         sbase get [DRIVER] [OPTIONS]\n"
    exp += "                (Drivers: chromedriver, geckodriver, edgedriver,\n"
    exp += "                          iedriver, uc_driver)\n"
    exp += "  Options:\n"
    exp += "           VERSION        Specify the version.\n"
    exp += "                          Tries to detect the needed version.\n"
    exp += "                          If using chromedriver or edgedriver,\n"
    exp += "                          you can use the major version integer.\n"
    exp += "           -p OR --path   Also copy the driver to /usr/local/bin\n"
    exp += "  Examples:\n"
    exp += "           sbase get chromedriver\n"
    exp += "           sbase get geckodriver\n"
    exp += "           sbase get edgedriver\n"
    exp += "           sbase get chromedriver 114\n"
    exp += "           sbase get chromedriver 114.0.5735.90\n"
    exp += "           sbase get chromedriver stable\n"
    exp += "           sbase get chromedriver beta\n"
    exp += "           sbase get chromedriver -p\n"
    exp += "  Output:\n"
    exp += "          Downloads the webdriver to seleniumbase/drivers/\n"
    exp += "          (chromedriver is required for Chrome automation)\n"
    exp += "          (geckodriver is required for Firefox automation)\n"
    exp += "          (edgedriver is required for MS__Edge automation)\n"
    print("")
    raise Exception("%s\n\n%s" % (constants.Warnings.INVALID_RUN_COMMAND, exp))


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def get_proxy_info():
    use_proxy = None
    protocol = "http"
    proxy_string = None
    user_and_pass = None
    if " --proxy=" in " ".join(sys.argv):
        from seleniumbase.core import proxy_helper
        for arg in sys.argv:
            if arg.startswith("--proxy="):
                proxy_string = arg.split("--proxy=")[1]
                if "@" in proxy_string:
                    # Format => username:password@hostname:port
                    try:
                        user_and_pass = proxy_string.split("@")[0]
                        proxy_string = proxy_string.split("@")[1]
                    except Exception:
                        raise Exception(
                            "The format for using a proxy server with auth "
                            'is: "username:password@hostname:port". If not '
                            'using auth, the format is: "hostname:port".'
                        )
                if proxy_string.endswith(":443"):
                    protocol = "https"
                elif "socks4" in proxy_string:
                    protocol = "socks4"
                elif "socks5" in proxy_string:
                    protocol = "socks5"
                proxy_string = proxy_helper.validate_proxy_string(proxy_string)
                if user_and_pass:
                    proxy_string = "%s@%s" % (user_and_pass, proxy_string)
                use_proxy = True
                break
    return (use_proxy, protocol, proxy_string)


def requests_get(url):
    use_proxy, protocol, proxy_string = get_proxy_info()
    proxies = None
    response = None
    if use_proxy:
        proxies = {protocol: proxy_string}
    try:
        response = requests.get(url, proxies=proxies, timeout=1.25)
    except Exception:
        # Prevent SSLCertVerificationError / CERTIFICATE_VERIFY_FAILED
        url = url.replace("https://", "http://")
        time.sleep(0.04)
        response = requests.get(url, proxies=proxies, timeout=2.75)
    return response


def requests_get_with_retry(url):
    use_proxy, protocol, proxy_string = get_proxy_info()
    proxies = None
    response = None
    if use_proxy:
        proxies = {protocol: proxy_string}
    try:
        response = requests.get(url, proxies=proxies, timeout=1.35)
    except Exception:
        time.sleep(1)
        try:
            response = requests.get(url, proxies=proxies, timeout=2.45)
        except Exception:
            time.sleep(1)
            response = requests.get(url, proxies=proxies, timeout=3.55)
    return response


def get_cft_known_good_versions():
    if hasattr(sb_config, "cft_kgv_json") and sb_config.cft_kgv_json:
        return sb_config.cft_kgv_json
    cft_ngv_url = (
        "https://googlechromelabs.github.io/"
        "chrome-for-testing/known-good-versions.json"
    )
    sb_config.cft_kgv_json = requests_get(cft_ngv_url)
    return sb_config.cft_kgv_json


def get_cft_latest_versions_per_milestone():
    if hasattr(sb_config, "cft_lvpm_json") and sb_config.cft_lvpm_json:
        return sb_config.cft_lvpm_json
    cft_lvpm_url = (
        "https://googlechromelabs.github.io/"
        "chrome-for-testing/latest-versions-per-milestone.json"
    )
    sb_config.cft_lvpm_json = requests_get(cft_lvpm_url)
    return sb_config.cft_lvpm_json


def get_cft_latest_version_from_milestone(milestone):
    url_request = get_cft_latest_versions_per_milestone()
    return url_request.json()["milestones"][milestone]["version"]


def get_latest_chromedriver_version(channel="Stable"):
    try:
        if hasattr(sb_config, "cft_lkgv_json") and sb_config.cft_lkgv_json:
            return sb_config.cft_lkgv_json["channels"][channel]["version"]
        req = requests_get(
            "https://googlechromelabs.github.io/"
            "chrome-for-testing/last-known-good-versions.json"
        )
        if req and req.ok:
            sb_config.cft_lkgv_json = req.json()
            return req.json()["channels"][channel]["version"]
    except Exception:
        pass
    # If a problem with Chrome-for-Testing JSON API: Fall back
    return DEFAULT_CHROMEDRIVER_VERSION


def get_latest_stable_chromedriver_version():
    return get_latest_chromedriver_version(channel="Stable")


def get_latest_beta_chromedriver_version():
    return get_latest_chromedriver_version(channel="Beta")


def get_latest_dev_chromedriver_version():
    return get_latest_chromedriver_version(channel="Dev")


def get_latest_canary_chromedriver_version():
    return get_latest_chromedriver_version(channel="Canary")


def log_d(message):
    """If setting sb_config.settings.HIDE_DRIVER_DOWNLOADS to True,
    output from driver downloads are logged instead of printed."""
    if (
        hasattr(sb_config.settings, "HIDE_DRIVER_DOWNLOADS")
        and sb_config.settings.HIDE_DRIVER_DOWNLOADS
    ):
        logging.debug(message)
    else:
        print(message)


def main(override=None, intel_for_uc=None, force_uc=None):
    if override:
        found_proxy = None
        if hasattr(sb_config, "proxy_driver") and sb_config.proxy_driver:
            if " --proxy=" in " ".join(sys.argv):
                for arg in sys.argv:
                    if arg.startswith("--proxy="):
                        found_proxy = arg
                        break
        if override == "chromedriver":
            sys.argv = ["seleniumbase", "get", "chromedriver"]
        elif override.startswith("chromedriver "):
            extra = override.split("chromedriver ")[1]
            sys.argv = ["seleniumbase", "get", "chromedriver", extra]
        elif override == "edgedriver":
            sys.argv = ["seleniumbase", "get", "edgedriver"]
        elif override.startswith("edgedriver "):
            extra = override.split("edgedriver ")[1]
            sys.argv = ["seleniumbase", "get", "edgedriver", extra]
        elif override == "geckodriver":
            sys.argv = ["seleniumbase", "get", "geckodriver"]
        elif override.startswith("geckodriver "):
            extra = override.split("geckodriver ")[1]
            sys.argv = ["seleniumbase", "get", "geckodriver", extra]
        elif override == "iedriver":
            sys.argv = ["seleniumbase", "get", "iedriver"]
        elif override.startswith("iedriver "):
            extra = override.split("iedriver ")[1]
            sys.argv = ["seleniumbase", "get", "iedriver", extra]
        if found_proxy:
            sys.argv.append(found_proxy)

    num_args = len(sys.argv)
    if (
        "sbase" in sys.argv[0].lower()
        or ("seleniumbase" in sys.argv[0].lower())
    ):
        if num_args < 3 or num_args > 5:
            invalid_run_command()
    else:
        invalid_run_command()
    name = sys.argv[2].lower()
    if force_uc:
        name = "uc_driver"

    file_name = None
    download_url = None
    headless_ie_url = None
    headless_ie_exists = False
    headless_ie_file_name = None
    downloads_folder = DRIVER_DIR
    expected_contents = None
    platform_code = None
    copy_to_path = False
    latest_version = ""
    use_version = ""
    new_file = ""
    f_name = ""
    if IS_WINDOWS and hasattr(colorama, "just_fix_windows_console"):
        colorama.just_fix_windows_console()
    else:
        colorama.init(autoreset=True)
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c4 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTWHITE_EX
    c5 = colorama.Fore.RED + colorama.Back.LIGHTWHITE_EX
    c6 = colorama.Fore.LIGHTYELLOW_EX + colorama.Back.CYAN
    cr = colorama.Style.RESET_ALL
    if IS_LINUX:
        c1 = ""
        c2 = ""
        c3 = ""
        c4 = ""
        c5 = ""
        c6 = ""
        cr = ""

    if name == "chromedriver" or name == "uc_driver":
        if name == "uc_driver" and IS_ARM_MAC:
            intel_for_uc = True  # uc_driver is generated from chromedriver
        last = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        use_version = DEFAULT_CHROMEDRIVER_VERSION  # Until get correct VER

        if (
            not override
            and (
                num_args == 3
                or (num_args == 4 and "-p" in sys.argv[3].lower())
            )
        ):
            major_chrome_version = None
            try:
                from seleniumbase.core import detect_b_ver

                br_app = "google-chrome"
                major_chrome_version = (
                    detect_b_ver.get_browser_version_from_os(br_app)
                ).split(".")[0]
                if int(major_chrome_version) < 72:
                    major_chrome_version = None
            except Exception:
                major_chrome_version = None
            if major_chrome_version and major_chrome_version.isnumeric():
                num_args += 1
                sys.argv.insert(3, major_chrome_version)

        get_latest = False
        get_v_latest = False
        get_previous = False
        get_beta = False
        get_canary = False
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                uv_low = use_version.lower()
                if uv_low == "latest" or uv_low == "stable":
                    uv_low = "latest"  # If "stable", rename
                    get_latest = True
                elif uv_low == "latest-1" or uv_low == "previous":
                    uv_low = "latest-1"  # If "previous", rename
                    get_previous = True
                elif uv_low == "beta":
                    get_beta = True
                elif uv_low == "dev":
                    use_version = get_latest_dev_chromedriver_version()
                    sys.argv[3] = use_version
                elif uv_low == "canary":
                    get_canary = True
                elif uv_low.isdigit() and int(uv_low) > 69:
                    get_v_latest = True
            else:
                copy_to_path = True
        if num_args == 5:
            if "-p" in sys.argv[4].lower():
                copy_to_path = True
            else:
                invalid_run_command()
        if IS_MAC:
            if IS_ARM_MAC and not intel_for_uc:
                use_version = use_version.lower()
                if (
                    use_version == "latest"
                    or use_version == "stable"
                    or use_version == "latest-1"
                    or use_version == "previous"
                    or use_version == "beta"
                    or use_version == "canary"
                ):
                    use_version = get_latest_stable_chromedriver_version()
                if use_version == "latest-1" or use_version == "previous":
                    use_version = str(int(use_version.split(".")[0]) - 1)
                elif use_version == "beta":
                    use_version = str(int(use_version.split(".")[0]) + 1)
                elif use_version == "canary":
                    use_version = str(int(use_version.split(".")[0]) + 2)
            if (
                IS_ARM_MAC
                and not intel_for_uc
                and int(use_version.split(".")[0]) > 105
            ):
                file_name = "chromedriver_mac_arm64.zip"
            else:
                file_name = "chromedriver_mac64.zip"
        elif IS_LINUX:
            file_name = "chromedriver_linux64.zip"
        elif IS_WINDOWS:
            file_name = "chromedriver_win32.zip"  # Works for win32 / win_x64
            if not get_latest and not get_v_latest and num_args < 4:
                get_latest = True
        else:
            raise Exception(
                "Cannot determine which version of chromedriver to download!"
            )
        found_chromedriver = False
        cft = False
        if get_latest or get_previous or get_beta or get_canary:
            use_version = get_latest_stable_chromedriver_version()
            found_chromedriver = True
            if get_previous and int(use_version.split(".")[0]) >= 115:
                get_v_latest = True
                use_version = str(int(use_version.split(".")[0]) - 1)
            elif get_beta and int(use_version.split(".")[0]) >= 115:
                get_v_latest = True
                use_version = get_latest_beta_chromedriver_version()
                use_version = use_version.split(".")[0]
            elif get_canary and int(use_version.split(".")[0]) >= 115:
                get_v_latest = True
                use_version = get_latest_canary_chromedriver_version()
                use_version = use_version.split(".")[0]
        force_cft = False
        if (
            use_version.split(".")[0].isnumeric()
            and int(use_version.split(".")[0]) >= 115
        ):
            force_cft = True
        if (get_v_latest or force_cft):
            if get_v_latest:
                if not force_cft:
                    url_req = requests_get(last)
                    if url_req.ok:
                        latest_version = url_req.text
                else:
                    latest_version = get_latest_stable_chromedriver_version()
                force_cft = False
            if not force_cft and int(use_version) < 115:
                last = last + "_" + use_version
                url_request = requests_get(last)
                if url_request.ok:
                    found_chromedriver = True
                    use_version = url_request.text
                    if use_version == latest_version:
                        get_latest = True
            else:
                url_request = None
                cft = True
                if force_cft:
                    url_request = get_cft_known_good_versions()
                    if (
                        url_request.ok
                        and '"version":"%s"' % use_version in url_request.text
                    ):
                        fver = use_version
                        found_chromedriver = True
                else:
                    url_request = get_cft_latest_versions_per_milestone()
                if not force_cft and url_request.ok:
                    fver = get_cft_latest_version_from_milestone(use_version)
                    found_chromedriver = True
                    use_version = str(fver)
                    if use_version == latest_version:
                        get_latest = True
        download_url = (
            "https://chromedriver.storage.googleapis.com/"
            "%s/%s" % (use_version, file_name)
        )
        plat_arch = ""
        if cft:
            if IS_MAC:
                if (
                    IS_ARM_MAC
                    and not intel_for_uc
                ):
                    platform_code = "mac-arm64"
                    file_name = "chromedriver-mac-arm64.zip"
                else:
                    platform_code = "mac-x64"
                    file_name = "chromedriver-mac-x64.zip"
            elif IS_LINUX:
                platform_code = "linux64"
                file_name = "chromedriver-linux64.zip"
            elif IS_WINDOWS:
                if "64" in ARCH:
                    platform_code = "win64"
                    file_name = "chromedriver-win64.zip"
                else:
                    platform_code = "win32"
                    file_name = "chromedriver-win32.zip"
            plat_arch = file_name.split(".zip")[0]
            download_url = (
                "https://storage.googleapis.com/chrome-for-testing-public/"
                "%s/%s/%s" % (use_version, platform_code, file_name)
            )
        url_request = None
        if not found_chromedriver:
            url_req = requests_get(last)
            if url_req.ok:
                latest_version = url_req.text
                if use_version == latest_version:
                    get_latest = True
            url_request = requests_get(download_url)
        if found_chromedriver or url_request.ok:
            p_version = use_version
            p_version = c3 + use_version + cr
            latest_stable = get_latest_stable_chromedriver_version()
            latest_beta = get_latest_beta_chromedriver_version()
            latest_dev = get_latest_dev_chromedriver_version()
            latest_canary = get_latest_canary_chromedriver_version()
            vint = True
            int_use_ver = None
            int_latest_ver = None
            try:
                int_use_ver = int(use_version.split(".")[0])
                int_latest_ver = int(latest_stable.split(".")[0])
            except Exception:
                vint = False
            on_cft = False
            if int_latest_ver > 115:
                on_cft = True
            if cft and on_cft and use_version == latest_stable:
                p_version = p_version + " " + c2 + "(Latest Stable)" + cr + " "
            elif cft and on_cft and use_version == latest_beta:
                p_version = p_version + " " + c2 + "(Latest Beta)" + cr + " "
            elif cft and on_cft and use_version == latest_dev:
                p_version = p_version + " " + c2 + "(Latest Dev)" + cr + " "
            elif cft and on_cft and use_version == latest_canary:
                p_version = p_version + " " + c2 + "(Latest Canary)" + cr + " "
            elif not vint:
                pass
            elif vint and cft and on_cft and int_use_ver == int_latest_ver:
                p_version = p_version + " " + c2 + "(Stable)" + cr
            elif vint and cft and on_cft and int_use_ver == int_latest_ver + 1:
                p_version = p_version + " " + c2 + "(Beta)" + cr
            elif vint and cft and on_cft and int_use_ver == int_latest_ver + 2:
                p_version = p_version + " " + c2 + "(Dev / Canary)" + cr
            elif vint and cft and on_cft and int_use_ver == int_latest_ver - 1:
                p_version = p_version + " " + c6 + "(Previous Version)" + cr
            elif cft and not on_cft:
                pass
            else:
                not_latest = c5 + "(" + c4 + "Legacy Version" + c5 + ")" + cr
                p_version = p_version + " " + not_latest
            msg = c2 + "chromedriver to download" + cr
            log_d("\n*** %s = %s" % (msg, p_version))
        else:
            raise Exception("Could not find chromedriver to download!\n")
        if not get_latest:
            pass
    elif name == "geckodriver" or name == "firefoxdriver":
        use_version = DEFAULT_GECKODRIVER_VERSION
        found_geckodriver = False
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                if use_version.lower() == "latest":
                    last = (
                        "https://api.github.com/repos/"
                        "mozilla/geckodriver/releases/latest"
                    )
                    url_request = requests_get(last)
                    if url_request.ok:
                        found_geckodriver = True
                        use_version = url_request.json()["tag_name"]
                    else:
                        use_version = DEFAULT_GECKODRIVER_VERSION
            else:
                copy_to_path = True
        if num_args == 5:
            if "-p" in sys.argv[4].lower():
                copy_to_path = True
            else:
                invalid_run_command()
        if IS_MAC:
            if IS_ARM_MAC:
                file_name = "geckodriver-%s-macos-aarch64.tar.gz" % use_version
            else:
                file_name = "geckodriver-%s-macos.tar.gz" % use_version
        elif IS_LINUX:
            if "64" in ARCH:
                if "aarch64" in platform.processor():
                    file_name = (
                        "geckodriver-%s-linux-aarch64.tar.gz" % use_version
                    )
                else:
                    file_name = "geckodriver-%s-linux64.tar.gz" % use_version
            else:
                file_name = "geckodriver-%s-linux32.tar.gz" % use_version
        elif IS_WINDOWS:
            file_name = "geckodriver-%s-win64.zip" % use_version
        else:
            raise Exception(
                "Cannot determine which version of geckodriver to download!"
            )
        download_url = (
            "https://github.com/mozilla/geckodriver/"
            "releases/download/"
            "%s/%s" % (use_version, file_name)
        )
        url_request = None
        if not found_geckodriver:
            url_request = requests_get(download_url)
        if found_geckodriver or url_request.ok:
            msg = c2 + "geckodriver to download" + cr
            p_version = c3 + use_version + cr
            log_d("\n*** %s = %s" % (msg, p_version))
        else:
            raise Exception(
                "\nCould not find the specified geckodriver "
                "version to download!\n"
            )
    elif name == "edgedriver" or name == "msedgedriver":
        name = "edgedriver"
        last = (
            "https://msedgewebdriverstorage.blob.core.windows.net"
            "/edgewebdriver/LATEST_STABLE"
        )

        if (
            not override
            and (
                num_args == 3
                or (num_args == 4 and "-p" in sys.argv[3].lower())
            )
        ):
            use_version = "latest"
            major_edge_version = None
            try:
                from seleniumbase.core import detect_b_ver

                br_app = "edge"
                major_edge_version = (
                    detect_b_ver.get_browser_version_from_os(br_app)
                ).split(".")[0]
                if int(major_edge_version) < 80:
                    major_edge_version = None
            except Exception:
                major_edge_version = None
            if major_edge_version and major_edge_version.isnumeric():
                num_args += 1
                sys.argv.insert(3, major_edge_version)
                use_version = major_edge_version

        get_latest = False
        if num_args == 3:
            get_latest = True
        if num_args == 4 and "-p" in sys.argv[3].lower():
            get_latest = True
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                if use_version.lower() == "latest":
                    use_version = DEFAULT_EDGEDRIVER_VERSION
                    get_latest = True
            else:
                copy_to_path = True
        if num_args == 5:
            if "-p" in sys.argv[4].lower():
                copy_to_path = True
            else:
                invalid_run_command()
        if get_latest:
            url_request = requests_get_with_retry(last)
            if url_request.ok:
                use_version = url_request.text.split("\r")[0].split("\n")[0]
                use_version = use_version.split(".")[0]
            else:
                use_version = DEFAULT_EDGEDRIVER_VERSION
        suffix = None
        if IS_WINDOWS and "64" in ARCH:
            file_name = "edgedriver_win64.zip"
            suffix = "WINDOWS"
        elif IS_WINDOWS:
            file_name = "edgedriver_win32.zip"
            suffix = "WINDOWS"
        elif IS_MAC:
            if IS_ARM_MAC and int(use_version.split(".")[0]) > 104:
                file_name = "edgedriver_mac64_m1.zip"
            else:
                file_name = "edgedriver_mac64.zip"
            suffix = "MACOS"
        elif IS_LINUX:
            file_name = "edgedriver_linux64.zip"
            suffix = "LINUX"
        else:
            raise Exception(
                "Cannot determine which version of EdgeDriver to download!"
            )
        if use_version.isdigit():
            edgedriver_st = "https://msedgedriver.azureedge.net/LATEST_RELEASE"
            use_version = "%s_%s_%s" % (edgedriver_st, use_version, suffix)
            url_request = requests_get_with_retry(use_version)
            if url_request.ok:
                use_version = url_request.text.split("\r")[0].split("\n")[0]
                if (
                    int(use_version.split(".")[0]) == 115
                    and use_version.startswith("115.0")
                    and use_version != "115.0.1901.183"
                ):
                    use_version = "115.0.1901.183"
        download_url = "https://msedgedriver.azureedge.net/%s/%s" % (
            use_version,
            file_name,
        )
        if not get_latest and not use_version == DEFAULT_EDGEDRIVER_VERSION:
            url_request = requests_get_with_retry(download_url)
            if not url_request.ok:
                raise Exception(
                    "Could not find version [%s] of EdgeDriver!" % use_version
                )
        msg = c2 + "edgedriver to download" + cr
        p_version = c3 + use_version + cr
        log_d("\n*** %s = %s" % (msg, p_version))
    elif name == "iedriver":
        full_version = "4.14.0"
        use_version = full_version
        if IS_WINDOWS and "64" in ARCH:
            file_name = "IEDriverServer_x64_%s.zip" % full_version
        elif IS_WINDOWS:
            file_name = "IEDriverServer_Win32_%s.zip" % full_version
        else:
            raise Exception(
                "Sorry! IEDriver is only for "
                "Windows-based systems!"
            )
        download_url = (
            "https://github.com/SeleniumHQ/selenium/"
            "releases/download/selenium-"
            "%s/%s" % (full_version, file_name)
        )
        headless_ie_version = "v1.4"
        headless_ie_file_name = "headless-selenium-for-win-v1-4.zip"
        headless_ie_url = (
            "https://github.com/kybu/headless-selenium-for-win/"
            "releases/download/"
            "%s/%s" % (headless_ie_version, headless_ie_file_name)
        )
        url_request = requests_get_with_retry(headless_ie_url)
        if url_request.ok:
            headless_ie_exists = True
            msg = c2 + "HeadlessIEDriver to download" + cr
            p_version = c3 + headless_ie_version + cr
            log_d("\n*** %s = %s" % (msg, p_version))
    else:
        invalid_run_command()

    if file_name is None or download_url is None:
        invalid_run_command()

    file_path = os.path.join(downloads_folder, file_name)
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)

    driver_name = None  # The name of the driver executable
    driver_contents = []  # The contents of the driver zip file

    if headless_ie_exists:
        headless_ie_file_path = os.path.join(
            downloads_folder, headless_ie_file_name
        )
        log_d(
            "\nDownloading %s from:\n%s ..."
            % (headless_ie_file_name, headless_ie_url)
        )
        remote_file = requests_get_with_retry(headless_ie_url)
        with open(headless_ie_file_path, "wb") as file:
            file.write(remote_file.content)
        log_d("%sDownload Complete!%s\n" % (c1, cr))
        zip_file_path = headless_ie_file_path
        zip_ref = zipfile.ZipFile(zip_file_path, "r")
        contents = zip_ref.namelist()
        h_ie_fn = headless_ie_file_name.split(".zip")[0]
        expected_contents = [
            "%s/" % h_ie_fn,
            "%s/ruby_example/" % h_ie_fn,
            "%s/ruby_example/Gemfile" % h_ie_fn,
            "%s/ruby_example/Gemfile.lock" % h_ie_fn,
            "%s/ruby_example/ruby_example.rb" % h_ie_fn,
            "%s/desktop_utils.exe" % h_ie_fn,
            "%s/headless_ie_selenium.exe" % h_ie_fn,
            "%s/README.md" % h_ie_fn,
        ]
        if len(contents) > 8:
            raise Exception("Unexpected content in HeadlessIEDriver Zip file!")
        for content in contents:
            if content not in expected_contents:
                raise Exception(
                    "Expected file [%s] missing from [%s]"
                    % (content, expected_contents)
                )
        # Zip file is valid. Proceed.
        driver_path = None
        driver_file = None
        filename = None
        for f_name in contents:
            # Remove existing version if exists
            str_name = str(f_name)
            new_file = os.path.join(downloads_folder, str_name)
            if str_name == "%s/headless_ie_selenium.exe" % h_ie_fn:
                driver_file = str_name
                driver_path = new_file
                filename = "headless_ie_selenium.exe"
                if os.path.exists(new_file):
                    os.remove(new_file)
        if not driver_file or not driver_path or not filename:
            raise Exception("headless_ie_selenium.exe missing from Zip file!")
        log_d("Extracting %s from %s ..." % (filename, headless_ie_file_name))
        zip_ref.extractall(downloads_folder)
        zip_ref.close()
        os.remove(zip_file_path)
        shutil.copyfile(driver_path, os.path.join(downloads_folder, filename))
        log_d("%sUnzip Complete!%s\n" % (c2, cr))
        to_remove = [
            "%s/%s/ruby_example/Gemfile" % (downloads_folder, h_ie_fn),
            "%s/%s/ruby_example/Gemfile.lock" % (downloads_folder, h_ie_fn),
            "%s/%s/ruby_example/ruby_example.rb" % (downloads_folder, h_ie_fn),
            "%s/%s/desktop_utils.exe" % (downloads_folder, h_ie_fn),
            "%s/%s/headless_ie_selenium.exe" % (downloads_folder, h_ie_fn),
            "%s/%s/README.md" % (downloads_folder, h_ie_fn),
        ]
        for file_to_remove in to_remove:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
        if os.path.exists("%s/%s/ruby_example/" % (downloads_folder, h_ie_fn)):
            # Only works if the directory is empty
            os.rmdir("%s/%s/ruby_example/" % (downloads_folder, h_ie_fn))
        if os.path.exists(os.path.join(downloads_folder, h_ie_fn)):
            # Only works if the directory is empty
            os.rmdir(os.path.join(downloads_folder, h_ie_fn))
        driver_path = os.path.join(downloads_folder, filename)
        log_d(
            "The file [%s] was saved to:\n%s%s%s\n"
            % (filename, c3, driver_path, cr)
        )
        log_d("Making [%s %s] executable ..." % (driver_file, use_version))
        make_executable(driver_path)
        log_d(
            "%s[%s %s] is now ready for use!%s"
            % (c1, driver_file, use_version, cr)
        )

    log_d("\nDownloading %s from:\n%s ..." % (file_name, download_url))
    remote_file = requests_get_with_retry(download_url)
    with open(file_path, "wb") as file:
        file.write(remote_file.content)
    log_d("%sDownload Complete!%s\n" % (c1, cr))

    if file_name.endswith(".zip"):
        zip_file_path = file_path
        zip_ref = zipfile.ZipFile(zip_file_path, "r")
        contents = zip_ref.namelist()
        if (
            len(contents) >= 1
            and name in ["chromedriver", "uc_driver", "geckodriver"]
        ):
            for f_name in contents:
                if (
                    (name == "chromedriver" or name == "uc_driver")
                    and (
                        f_name.split("/")[-1] == "chromedriver"
                        or f_name.split("/")[-1] == "chromedriver.exe"
                    )
                ):
                    driver_name = f_name.split("/")[-1]
                    driver_contents = [driver_name]
                # Remove existing version if exists
                new_file = os.path.join(downloads_folder, str(f_name))
                if name == "uc_driver":
                    if new_file.endswith("drivers/chromedriver"):
                        new_file = new_file.replace(
                            "drivers/chromedriver", "drivers/uc_driver"
                        )
                    elif new_file.endswith("drivers/chromedriver.exe"):
                        new_file = new_file.replace(
                            "drivers/chromedriver.exe", "drivers/uc_driver.exe"
                        )
                    elif "drivers/%s/chromedriver" % plat_arch in new_file:
                        new_file = new_file.replace(
                            "drivers/%s/chromedriver" % plat_arch,
                            "drivers/%s/uc_driver" % plat_arch
                        )
                    elif "drivers/%s/chromedriver.exe" % plat_arch in new_file:
                        new_file = new_file.replace(
                            "drivers/%s/chromedriver.exe" % plat_arch,
                            "drivers/%s/uc_driver.exe" % plat_arch
                        )
                if "Driver" in new_file or "driver" in new_file:
                    if os.path.exists(new_file):
                        os.remove(new_file)  # Technically the old file now
            if driver_contents:
                contents = driver_contents
            log_d("Extracting %s from %s ..." % (contents, file_name))
            if name == "uc_driver":
                f_name = "uc_driver"
                new_file = os.path.join(downloads_folder, f_name)
                if os.path.exists(new_file):
                    os.remove(new_file)
                zipinfos = zip_ref.infolist()
                for zipinfo in zipinfos:
                    if zipinfo.filename.split("/")[-1] == "chromedriver":
                        zipinfo.filename = "uc_driver"
                        zip_ref.extract(zipinfo, downloads_folder)
                    elif zipinfo.filename.split("/")[-1] == "chromedriver.exe":
                        zipinfo.filename = "uc_driver.exe"
                        zip_ref.extract(zipinfo, downloads_folder)
                contents = zip_ref.namelist()
                if driver_contents:
                    contents = driver_contents
            elif name == "chromedriver" or name == "uc_driver":
                zipinfos = zip_ref.infolist()
                for zipinfo in zipinfos:
                    if zipinfo.filename.split("/")[-1] == "chromedriver":
                        zipinfo.filename = "chromedriver"
                    elif zipinfo.filename.split("/")[-1] == (
                        "chromedriver.exe"
                    ):
                        zipinfo.filename = "chromedriver.exe"
                    if (
                        zipinfo.filename.split("/")[-1] == "chromedriver"
                        or zipinfo.filename.split("/")[-1] == (
                            "chromedriver.exe"
                        )
                    ):
                        zip_ref.extract(zipinfo, downloads_folder)
                contents = zip_ref.namelist()
                if driver_contents:
                    contents = driver_contents
            else:
                zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            log_d("%sUnzip Complete!%s\n" % (c2, cr))
            for f_name in contents:
                if name == "uc_driver":
                    if IS_WINDOWS:
                        f_name = "uc_driver.exe"
                    else:
                        f_name = "uc_driver"
                new_file = os.path.join(downloads_folder, str(f_name))
                pr_file = c3 + new_file + cr
                log_d("The file [%s] was saved to:\n%s\n" % (f_name, pr_file))
                log_d("Making [%s %s] executable ..." % (f_name, use_version))
                make_executable(new_file)
                log_d(
                    "%s[%s %s] is now ready for use!%s" %
                    (c1, f_name, use_version, cr)
                )
                if copy_to_path and os.path.exists(LOCAL_PATH):
                    path_file = LOCAL_PATH + f_name
                    shutil.copyfile(new_file, path_file)
                    make_executable(path_file)
                    log_d("Also copied to: %s%s%s" % (c3, path_file, cr))
            log_d("")
        elif (
            name == "edgedriver"
            or name == "msedgedriver"
            or name == "iedriver"
        ):
            if IS_MAC or IS_LINUX:
                # Mac / Linux
                expected_contents = [
                    "Driver_Notes/",
                    "Driver_Notes/EULA",
                    "Driver_Notes/LICENSE",
                    "Driver_Notes/credits.html",
                    "msedgedriver",
                    "libc++.dylib",
                ]
            else:
                # Windows
                expected_contents = [
                    "Driver_Notes/",
                    "Driver_Notes/credits.html",
                    "Driver_Notes/EULA",
                    "Driver_Notes/LICENSE",
                    "msedgedriver.exe",
                ]
            if name == "iedriver":
                expected_contents = ["IEDriverServer.exe"]
            if len(contents) > 5:
                raise Exception("Unexpected content in EdgeDriver Zip file!")
            for content in contents:
                if content not in expected_contents:
                    raise Exception(
                        "Expected file [%s] missing from [%s]"
                        % (content, expected_contents)
                    )
            # Zip file is valid. Proceed.
            driver_path = None
            driver_file = None
            for f_name in contents:
                # Remove existing version if exists
                str_name = str(f_name)
                new_file = os.path.join(downloads_folder, str_name)
                if (
                    ((IS_MAC or IS_LINUX) and str_name == "msedgedriver")
                    or (
                        str_name == "msedgedriver.exe"
                        or str_name == "IEDriverServer.exe"
                    )
                ):
                    driver_file = str_name
                    driver_path = new_file
                    if os.path.exists(new_file):
                        os.remove(new_file)
            if not driver_file or not driver_path:
                if str_name == "IEDriverServer.exe":
                    raise Exception("IEDriverServer missing from Zip file!")
                raise Exception("msedgedriver missing from Zip file!")
            log_d("Extracting %s from %s ..." % (contents, file_name))
            zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            log_d("%sUnzip Complete!%s\n" % (c2, cr))
            to_remove = [
                "%s/Driver_Notes/credits.html" % downloads_folder,
                "%s/Driver_Notes/EULA" % downloads_folder,
                "%s/Driver_Notes/LICENSE" % downloads_folder,
            ]
            for file_to_remove in to_remove:
                if os.path.exists(file_to_remove):
                    os.remove(file_to_remove)
            if os.path.exists(os.path.join(downloads_folder, "Driver_Notes/")):
                # Only works if the directory is empty
                os.rmdir(os.path.join(downloads_folder, "Driver_Notes/"))
            pr_driver_path = c3 + driver_path + cr
            log_d(
                "The file [%s] was saved to:\n%s\n"
                % (driver_file, pr_driver_path)
            )
            log_d("Making [%s %s] executable ..." % (driver_file, use_version))
            make_executable(driver_path)
            log_d(
                "%s[%s %s] is now ready for use!%s"
                % (c1, driver_file, use_version, cr)
            )
            if copy_to_path and os.path.exists(LOCAL_PATH):
                path_file = LOCAL_PATH + f_name
                shutil.copyfile(new_file, path_file)
                make_executable(path_file)
                log_d("Also copied to: %s%s%s" % (c3, path_file, cr))
            log_d("")
        elif len(contents) == 0:
            raise Exception("Zip file %s is empty!" % zip_file_path)
        else:
            raise Exception("Expecting only one file in %s!" % zip_file_path)
    elif file_name.endswith(".tar.gz"):
        tar_file_path = file_path
        tar = tarfile.open(file_path)
        contents = tar.getnames()
        if len(contents) == 1:
            for f_name in contents:
                # Remove existing version if exists
                new_file = os.path.join(downloads_folder, str(f_name))
                if "Driver" in new_file or "driver" in new_file:
                    if os.path.exists(new_file):
                        os.remove(new_file)  # Technically the old file now
            log_d("Extracting %s from %s ..." % (contents, file_name))
            tar.extractall(downloads_folder)
            tar.close()
            os.remove(tar_file_path)
            log_d("%sUnzip Complete!%s\n" % (c2, cr))
            for f_name in contents:
                new_file = os.path.join(downloads_folder, str(f_name))
                pr_file = c3 + new_file + cr
                log_d("The file [%s] was saved to:\n%s\n" % (f_name, pr_file))
                log_d("Making [%s %s] executable ..." % (f_name, use_version))
                make_executable(new_file)
                log_d(
                    "%s[%s %s] is now ready for use!%s"
                    % (c1, f_name, use_version, cr)
                )
                if copy_to_path and os.path.exists(LOCAL_PATH):
                    path_file = LOCAL_PATH + f_name
                    shutil.copyfile(new_file, path_file)
                    make_executable(path_file)
                    log_d("Also copied to: %s%s%s" % (c3, path_file, cr))
            log_d("")
        elif len(contents) == 0:
            raise Exception("Tar file %s is empty!" % tar_file_path)
        else:
            raise Exception("Expecting only one file in %s!" % tar_file_path)
    else:
        # Not a .zip file or a .tar.gz file. Just a direct download.
        if "Driver" in file_name or "driver" in file_name:
            log_d("Making [%s] executable ..." % file_name)
            make_executable(file_path)
            log_d("%s[%s] is now ready for use!%s" % (c1, file_name, cr))
            log_d("Location of [%s]:\n%s\n" % (file_name, file_path))


if __name__ == "__main__":
    main()
