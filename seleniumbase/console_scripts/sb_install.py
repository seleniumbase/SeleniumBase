"""
Downloads the specified webdriver to "seleniumbase/drivers/"

Usage:
         sbase get {chromedriver|geckodriver|edgedriver|
                    iedriver|operadriver} [OPTIONS]
Options:
         VERSION         Specify the version.
                         Default chromedriver = 72.0.3626.69.
                         Tries to detect the needed version.
                         Use "latest" for the latest version.
                         Use "latest-1" for one less than that.
         -p OR --path    Also copy the driver to /usr/local/bin
Examples:
         sbase get chromedriver
         sbase get geckodriver
         sbase get edgedriver
         sbase get chromedriver 102.0.5005.61
         sbase get chromedriver 102
         sbase get chromedriver latest
         sbase get chromedriver latest-1  # (Latest minus one)
         sbase get chromedriver -p
         sbase get chromedriver latest -p
         sbase get edgedriver 102.0.1245.44
Output:
         Downloads the chosen webdriver to seleniumbase/drivers
         (chromedriver is required for Chrome automation)
         (geckodriver is required for Firefox automation)
         (edgedriver is required for MS Edge automation)
         (operadriver is required for Opera Browser automation)
         (iedriver is required for InternetExplorer automation)
"""

import colorama
import os
import platform
import requests
import shutil
import sys
import tarfile
import urllib3
import zipfile
from seleniumbase.fixtures import constants
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase

urllib3.disable_warnings()
selenium4_or_newer = False
if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
    selenium4_or_newer = True
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
LOCAL_PATH = "/usr/local/bin/"  # On Mac and Linux systems
DEFAULT_CHROMEDRIVER_VERSION = "72.0.3626.69"  # (Specify "latest" for latest)
DEFAULT_GECKODRIVER_VERSION = "v0.31.0"
DEFAULT_EDGEDRIVER_VERSION = "102.0.1245.44"  # (Looks for LATEST_STABLE first)
DEFAULT_OPERADRIVER_VERSION = "v.96.0.4664.45"


def invalid_run_command():
    exp = "  ** get / install **\n\n"
    exp += "  Usage:\n"
    exp += "           seleniumbase install [DRIVER] [OPTIONS]\n"
    exp += "           OR     sbase install [DRIVER] [OPTIONS]\n"
    exp += "           OR  seleniumbase get [DRIVER] [OPTIONS]\n"
    exp += "           OR         sbase get [DRIVER] [OPTIONS]\n"
    exp += "                (Drivers: chromedriver, geckodriver, edgedriver,\n"
    exp += "                          iedriver, operadriver)\n"
    exp += "  Options:\n"
    exp += "           VERSION        Specify the version.\n"
    exp += "                           (Default chromedriver = 72.0.3626.69.\n"
    exp += "                            Tries to detect the needed version.\n"
    exp += '                            Use "latest" for the latest version.\n'
    exp += "                            For chromedriver, you can also use\n"
    exp += "                            the major version integer\n"
    exp += '                            or "latest-1" for 1 less than that.)\n'
    exp += "           -p OR --path   Also copy the driver to /usr/local/bin\n"
    exp += "  Examples:\n"
    exp += "           sbase get chromedriver\n"
    exp += "           sbase get geckodriver\n"
    exp += "           sbase get edgedriver\n"
    exp += "           sbase get chromedriver 102\n"
    exp += "           sbase get chromedriver 102.0.5005.61\n"
    exp += "           sbase get chromedriver latest\n"
    exp += "           sbase get chromedriver latest-1\n"
    exp += "           sbase get chromedriver -p\n"
    exp += "           sbase get chromedriver latest -p\n"
    exp += "           sbase get edgedriver 102.0.1245.44\n"
    exp += "  Output:\n"
    exp += "          Downloads the chosen webdriver to seleniumbase/drivers\n"
    exp += "          (chromedriver is required for Chrome automation)\n"
    exp += "          (geckodriver is required for Firefox automation)\n"
    exp += "          (edgedriver is required for Microsoft Edge automation)\n"
    exp += "          (iedriver is required for InternetExplorer automation)\n"
    exp += "          (operadriver is required for Opera Browser automation)\n"
    print("")
    raise Exception("%s\n\n%s" % (constants.Warnings.INVALID_RUN_COMMAND, exp))


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def requests_get(url):
    response = None
    try:
        response = requests.get(url)
    except Exception:
        # Prevent SSLCertVerificationError / CERTIFICATE_VERIFY_FAILED
        url = url.replace("https://", "http://")
        response = requests.get(url)
    return response


def requests_get_with_retry(url):
    response = None
    try:
        response = requests.get(url)
    except Exception:
        import time

        time.sleep(0.75)
        response = requests.get(url)
    return response


def main(override=None):
    if override:
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

    file_name = None
    download_url = None
    headless_ie_url = None
    headless_ie_exists = False
    headless_ie_file_name = None
    downloads_folder = DRIVER_DIR
    sys_plat = sys.platform
    expected_contents = None
    platform_code = None
    inner_folder = None
    copy_to_path = False
    latest_version = ""
    use_version = ""
    new_file = ""
    f_name = ""
    colorama.init(autoreset=True)
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c4 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTWHITE_EX
    c5 = colorama.Fore.RED + colorama.Back.LIGHTWHITE_EX
    c6 = colorama.Fore.LIGHTYELLOW_EX + colorama.Back.BLUE
    cr = colorama.Style.RESET_ALL
    if "linux" in sys_plat:
        c1 = ""
        c2 = ""
        c3 = ""
        cr = ""

    if name == "chromedriver":
        last = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        use_version = DEFAULT_CHROMEDRIVER_VERSION

        if (
            selenium4_or_newer
            and not override
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
        get_latest_minus_one = False
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                uv_low = use_version.lower()
                if uv_low == "latest":
                    get_latest = True
                elif uv_low == "latest-1":
                    get_latest_minus_one = True
                elif len(uv_low) < 4 and uv_low.isdigit() and int(uv_low) > 69:
                    get_v_latest = True
            else:
                copy_to_path = True
        if num_args == 5:
            if "-p" in sys.argv[4].lower():
                copy_to_path = True
            else:
                invalid_run_command()
        if "darwin" in sys_plat:
            file_name = "chromedriver_mac64.zip"
        elif "linux" in sys_plat:
            file_name = "chromedriver_linux64.zip"
        elif "win32" in sys_plat or "win64" in sys_plat or "x64" in sys_plat:
            file_name = "chromedriver_win32.zip"  # Works for win32 / win_x64
            if not get_latest and not get_v_latest and num_args < 4:
                get_latest = True
        else:
            raise Exception(
                "Cannot determine which version of chromedriver to download!"
            )
        found_chromedriver = False
        if get_latest or get_latest_minus_one:
            url_request = requests_get(last)
            if url_request.ok:
                found_chromedriver = True
                use_version = url_request.text
                if get_latest_minus_one:
                    get_v_latest = True
                    use_version = str(int(use_version.split(".")[0]) - 1)
        if get_v_latest:
            url_req = requests_get(last)
            if url_req.ok:
                latest_version = url_req.text
            last = last + "_" + use_version
            url_request = requests_get(last)
            if url_request.ok:
                found_chromedriver = True
                use_version = url_request.text
                if use_version == latest_version:
                    get_latest = True
        download_url = (
            "https://chromedriver.storage.googleapis.com/"
            "%s/%s" % (use_version, file_name)
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
            if get_latest:
                p_version = p_version + " " + c2 + "(Latest)" + cr
            else:
                n_l_s = "NOT Latest"
                try:
                    int_use_version = int(use_version.split(".")[0])
                    int_latest_version = int(latest_version.split(".")[0])
                    if int_use_version > int_latest_version:
                        n_l_s = "NOT Latest Stable"
                except Exception:
                    pass
                not_latest = c5 + "(" + c4 + n_l_s + c5 + ")" + cr
                p_version = p_version + " " + not_latest
            msg = c2 + "chromedriver version for download" + cr
            print("\n*** %s = %s" % (msg, p_version))
        else:
            raise Exception("Could not find chromedriver to download!\n")
        if not get_latest:
            to_upgrade = " " + c3 + "To upgrade" + cr
            run_this = c3 + "run this" + cr
            install_sb = c6 + "sbase get chromedriver latest" + cr
            print("\n %s to the latest version of chromedriver," % to_upgrade)
            print("   %s: >>> %s" % (run_this, install_sb))
            print("  (Requires the latest version of Chrome installed)")
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
        if "darwin" in sys_plat:
            file_name = "geckodriver-%s-macos.tar.gz" % use_version
        elif "linux" in sys_plat:
            arch = platform.architecture()[0]
            if "64" in arch:
                file_name = "geckodriver-%s-linux64.tar.gz" % use_version
            else:
                file_name = "geckodriver-%s-linux32.tar.gz" % use_version
        elif "win32" in sys_plat or "win64" in sys_plat or "x64" in sys_plat:
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
            msg = c2 + "geckodriver version for download" + cr
            p_version = c3 + use_version + cr
            print("\n*** %s = %s" % (msg, p_version))
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
        if "win64" in sys_plat or "x64" in sys_plat:
            file_name = "edgedriver_win64.zip"
            suffix = "WINDOWS"
        elif "win32" in sys_plat or "x86" in sys_plat:
            file_name = "edgedriver_win32.zip"
            suffix = "WINDOWS"
        elif "darwin" in sys_plat:
            file_name = "edgedriver_mac64.zip"
            suffix = "MACOS"
        elif "linux" in sys_plat:
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
        msg = c2 + "edgedriver version for download" + cr
        p_version = c3 + use_version + cr
        print("\n*** %s = %s" % (msg, p_version))
    elif name == "iedriver":
        major_version = "3.14"
        full_version = "3.14.0"
        use_version = full_version
        if "win32" in sys_plat:
            file_name = "IEDriverServer_Win32_%s.zip" % full_version
        elif "win64" in sys_plat or "x64" in sys_plat:
            file_name = "IEDriverServer_x64_%s.zip" % full_version
        else:
            raise Exception(
                "Sorry! IEDriver is only for "
                "Windows-based operating systems!"
            )
        download_url = (
            "https://selenium-release.storage.googleapis.com/"
            "%s/%s" % (major_version, file_name)
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
            msg = c2 + "HeadlessIEDriver version for download" + cr
            p_version = c3 + headless_ie_version + cr
            print("\n*** %s = %s" % (msg, p_version))
    elif name == "operadriver" or name == "operachromiumdriver":
        name = "operadriver"
        use_version = DEFAULT_OPERADRIVER_VERSION
        get_latest = False
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                if use_version.lower() == "latest":
                    use_version = DEFAULT_OPERADRIVER_VERSION
            else:
                copy_to_path = True
        if num_args == 5:
            if "-p" in sys.argv[4].lower():
                copy_to_path = True
            else:
                invalid_run_command()
        if "darwin" in sys_plat:
            file_name = "operadriver_mac64.zip"
            platform_code = "mac64"
            inner_folder = "operadriver_%s/" % platform_code
            expected_contents = [
                "operadriver_mac64/",
                "operadriver_mac64/operadriver",
                "operadriver_mac64/sha512_sum",
            ]
        elif "linux" in sys_plat:
            file_name = "operadriver_linux64.zip"
            platform_code = "linux64"
            inner_folder = "operadriver_%s/" % platform_code
            expected_contents = [
                "operadriver_linux64/",
                "operadriver_linux64/operadriver",
                "operadriver_linux64/sha512_sum",
            ]
        elif "win32" in sys_plat:
            file_name = "operadriver_win32.zip"
            platform_code = "win32"
            inner_folder = "operadriver_%s/" % platform_code
            expected_contents = [
                "operadriver_win32/",
                "operadriver_win32/operadriver.exe",
                "operadriver_win32/sha512_sum",
            ]
        elif "win64" in sys_plat or "x64" in sys_plat:
            file_name = "operadriver_win64.zip"
            platform_code = "win64"
            inner_folder = "operadriver_%s/" % platform_code
            expected_contents = [
                "operadriver_win64/",
                "operadriver_win64/operadriver.exe",
                "operadriver_win64/sha512_sum",
            ]
        else:
            raise Exception(
                "Cannot determine which version of Operadriver to download!"
            )

        download_url = (
            "https://github.com/operasoftware/operachromiumdriver/"
            "releases/download/"
            "%s/%s" % (use_version, file_name)
        )
        msg = c2 + "operadriver version for download" + cr
        p_version = c3 + use_version + cr
        print("\n*** %s = %s" % (msg, p_version))
    else:
        invalid_run_command()

    if file_name is None or download_url is None:
        invalid_run_command()

    file_path = os.path.join(downloads_folder, file_name)
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)

    if headless_ie_exists:
        headless_ie_file_path = os.path.join(
            downloads_folder, headless_ie_file_name
        )
        print(
            "\nDownloading %s from:\n%s ..."
            % (headless_ie_file_name, headless_ie_url)
        )
        remote_file = requests_get_with_retry(headless_ie_url)
        with open(headless_ie_file_path, "wb") as file:
            file.write(remote_file.content)
        print("Download Complete!\n")
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
        print("Extracting %s from %s ..." % (filename, headless_ie_file_name))
        zip_ref.extractall(downloads_folder)
        zip_ref.close()
        os.remove(zip_file_path)
        shutil.copyfile(driver_path, os.path.join(downloads_folder, filename))
        print("Unzip Complete!\n")
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
        print(
            "The file [%s] was saved to:\n%s%s%s\n"
            % (filename, c3, driver_path, cr)
        )
        print("Making [%s %s] executable ..." % (driver_file, use_version))
        make_executable(driver_path)
        print("%s[%s] is now ready for use!%s" % (c1, driver_file, cr))

    print("\nDownloading %s from:\n%s ..." % (file_name, download_url))
    remote_file = requests_get_with_retry(download_url)
    with open(file_path, "wb") as file:
        file.write(remote_file.content)
    print("Download Complete!\n")

    if file_name.endswith(".zip"):
        zip_file_path = file_path
        zip_ref = zipfile.ZipFile(zip_file_path, "r")
        contents = zip_ref.namelist()
        if len(contents) == 1:
            if name == "operadriver":
                raise Exception("Zip file for OperaDriver is missing content!")
            for f_name in contents:
                # Remove existing version if exists
                new_file = os.path.join(downloads_folder, str(f_name))
                if "Driver" in new_file or "driver" in new_file:
                    if os.path.exists(new_file):
                        os.remove(new_file)  # Technically the old file now
            print("Extracting %s from %s ..." % (contents, file_name))
            zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            print("Unzip Complete!\n")
            for f_name in contents:
                new_file = os.path.join(downloads_folder, str(f_name))
                pr_file = c3 + new_file + cr
                print("The file [%s] was saved to:\n%s\n" % (f_name, pr_file))
                print("Making [%s %s] executable ..." % (f_name, use_version))
                make_executable(new_file)
                print("%s[%s] is now ready for use!%s" % (c1, f_name, cr))
                if copy_to_path and os.path.exists(LOCAL_PATH):
                    path_file = LOCAL_PATH + f_name
                    shutil.copyfile(new_file, path_file)
                    make_executable(path_file)
                    print("Also copied to: %s%s%s" % (c3, path_file, cr))
            print("")
        elif name == "edgedriver" or name == "msedgedriver":
            if "darwin" in sys_plat or "linux" in sys_plat:
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
                print(f_name)
                # Remove existing version if exists
                str_name = str(f_name)
                new_file = os.path.join(downloads_folder, str_name)
                if "darwin" in sys_plat or "linux" in sys_plat:
                    # Mac / Linux
                    if str_name == "msedgedriver":
                        driver_file = str_name
                        driver_path = new_file
                        if os.path.exists(new_file):
                            os.remove(new_file)
                else:
                    # Windows
                    if str_name == "msedgedriver.exe":
                        driver_file = str_name
                        driver_path = new_file
                        if os.path.exists(new_file):
                            os.remove(new_file)
            if not driver_file or not driver_path:
                raise Exception("msedgedriver missing from Zip file!")
            print("Extracting %s from %s ..." % (contents, file_name))
            zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            print("Unzip Complete!\n")
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
            print(
                "The file [%s] was saved to:\n%s\n"
                % (driver_file, driver_path)
            )
            print("Making [%s %s] executable ..." % (driver_file, use_version))
            make_executable(driver_path)
            print("%s[%s] is now ready for use!%s" % (c1, driver_file, cr))
            if copy_to_path and os.path.exists(LOCAL_PATH):
                path_file = LOCAL_PATH + f_name
                shutil.copyfile(new_file, path_file)
                make_executable(path_file)
                print("Also copied to: %s%s%s" % (c3, path_file, cr))
            print("")
        elif name == "operadriver":
            if len(contents) > 3:
                raise Exception("Unexpected content in OperaDriver Zip file!")
            # Zip file is valid. Proceed.
            driver_path = None
            driver_file = None
            for f_name in contents:
                # Remove existing version if exists
                str_name = str(f_name).split(inner_folder)[1]
                new_file = os.path.join(downloads_folder, str_name)
                if str_name == "operadriver" or str_name == "operadriver.exe":
                    driver_file = str_name
                    driver_path = new_file
                    if os.path.exists(new_file):
                        os.remove(new_file)
            if not driver_file or not driver_path:
                raise Exception("Operadriver missing from Zip file!")
            print("Extracting %s from %s ..." % (contents, file_name))
            zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            print("Unzip Complete!\n")
            inner_driver = os.path.join(
                downloads_folder, inner_folder, driver_file
            )
            inner_sha = os.path.join(
                downloads_folder, inner_folder, "sha512_sum"
            )
            shutil.copyfile(inner_driver, driver_path)
            pr_driver_path = c3 + driver_path + cr
            print(
                "The file [%s] was saved to:\n%s\n"
                % (driver_file, pr_driver_path)
            )
            print("Making [%s %s] executable ..." % (driver_file, use_version))
            make_executable(driver_path)
            print("%s[%s] is now ready for use!%s" % (c1, driver_file, cr))
            if copy_to_path and os.path.exists(LOCAL_PATH):
                path_file = LOCAL_PATH + driver_file
                shutil.copyfile(driver_path, path_file)
                make_executable(path_file)
                print("Also copied to: %s%s%s" % (c3, path_file, cr))
            # Clean up extra files
            if os.path.exists(inner_driver):
                os.remove(inner_driver)
            if os.path.exists(inner_sha):
                os.remove(inner_sha)
            if os.path.exists(os.path.join(downloads_folder, inner_folder)):
                # Only works if the directory is empty
                os.rmdir(os.path.join(downloads_folder, inner_folder))
            print("")
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
            print("Extracting %s from %s ..." % (contents, file_name))
            tar.extractall(downloads_folder)
            tar.close()
            os.remove(tar_file_path)
            print("Unzip Complete!\n")
            for f_name in contents:
                new_file = os.path.join(downloads_folder, str(f_name))
                pr_file = c3 + new_file + cr
                print("The file [%s] was saved to:\n%s\n" % (f_name, pr_file))
                print("Making [%s %s] executable ..." % (f_name, use_version))
                make_executable(new_file)
                print("%s[%s] is now ready for use!%s" % (c1, f_name, cr))
                if copy_to_path and os.path.exists(LOCAL_PATH):
                    path_file = LOCAL_PATH + f_name
                    shutil.copyfile(new_file, path_file)
                    make_executable(path_file)
                    print("Also copied to: %s%s%s" % (c3, path_file, cr))
            print("")
        elif len(contents) == 0:
            raise Exception("Tar file %s is empty!" % tar_file_path)
        else:
            raise Exception("Expecting only one file in %s!" % tar_file_path)
    else:
        # Not a .zip file or a .tar.gz file. Just a direct download.
        if "Driver" in file_name or "driver" in file_name:
            print("Making [%s] executable ..." % file_name)
            make_executable(file_path)
            print("%s[%s] is now ready for use!%s" % (c1, file_name, cr))
            print("Location of [%s]:\n%s\n" % (file_name, file_path))


if __name__ == "__main__":
    main()
