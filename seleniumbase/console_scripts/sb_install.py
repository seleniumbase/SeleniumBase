"""
Installs the specified web driver.

Usage:
        sbase install {chromedriver|geckodriver|edgedriver|
                       iedriver|operadriver} [OPTIONS]
Options:
        VERSION         Specify the version.
                        (Default chromedriver version = 2.44)
                        Use "latest" for the latest version.
        -p OR --path    Also copy the driver to /usr/local/bin
Example:
        sbase install chromedriver
        sbase install geckodriver
        sbase install edgedriver
        sbase install chromedriver 87.0.4280.88
        sbase install chromedriver 87
        sbase install chromedriver latest
        sbase install chromedriver -p
        sbase install chromedriver latest -p
        sbase install edgedriver 87.0.664.66
Output:
        Installs the chosen webdriver to seleniumbase/drivers/
        (chromedriver is required for Chrome automation)
        (geckodriver is required for Firefox automation)
        (edgedriver is required for MS Edge automation)
        (operadriver is required for Opera Browser automation)
        (iedriver is required for Internet Explorer automation)
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
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
urllib3.disable_warnings()
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
LOCAL_PATH = "/usr/local/bin/"  # On Mac and Linux systems
DEFAULT_CHROMEDRIVER_VERSION = "2.44"  # (Specify "latest" to get the latest)
DEFAULT_GECKODRIVER_VERSION = "v0.28.0"
DEFAULT_EDGEDRIVER_VERSION = "87.0.664.66"  # (Looks for LATEST_STABLE first)
DEFAULT_OPERADRIVER_VERSION = "v.84.0.4147.89"


def invalid_run_command():
    exp = ("  ** install **\n\n")
    exp += "  Usage:\n"
    exp += "          seleniumbase install [DRIVER_NAME] [OPTIONS]\n"
    exp += "              (Drivers: chromedriver, geckodriver, edgedriver,\n"
    exp += "                        iedriver, operadriver)\n"
    exp += "  Options:\n"
    exp += "          VERSION         Specify the version.\n"
    exp += "                          (Default chromedriver version = 2.44)\n"
    exp += '                          Use "latest" for the latest version.\n'
    exp += "          -p OR --path    Also copy the driver to /usr/local/bin\n"
    exp += "  Example:\n"
    exp += "          seleniumbase install chromedriver\n"
    exp += "          seleniumbase install geckodriver\n"
    exp += "          seleniumbase install chromedriver 76.0.3809.126\n"
    exp += "          seleniumbase install chromedriver latest\n"
    exp += "          seleniumbase install chromedriver -p\n"
    exp += "          seleniumbase install chromedriver latest -p\n"
    exp += "  Output:\n"
    exp += "          Installs the chosen webdriver to seleniumbase/drivers/\n"
    exp += "          (chromedriver is required for Chrome automation)\n"
    exp += "          (geckodriver is required for Firefox automation)\n"
    exp += "          (edgedriver is required for Microsoft Edge automation)\n"
    exp += "          (iedriver is required for InternetExplorer automation)\n"
    exp += "          (operadriver is required for Opera Browser automation)\n"
    print("")
    raise Exception('INVALID RUN COMMAND!\n\n%s' % exp)


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def main(override=None):
    if override == "chromedriver":
        sys.argv = ["seleniumbase", "install", "chromedriver"]
    elif override == "edgedriver":
        sys.argv = ["seleniumbase", "install", "edgedriver"]
    elif override == "geckodriver":
        sys.argv = ["seleniumbase", "install", "geckodriver"]

    num_args = len(sys.argv)
    if sys.argv[0].split('/')[-1].lower() == "seleniumbase" or (
            sys.argv[0].split('\\')[-1].lower() == "seleniumbase") or (
            sys.argv[0].split('/')[-1].lower() == "sbase") or (
            sys.argv[0].split('\\')[-1].lower() == "sbase"):
        if num_args < 3 or num_args > 5:
            invalid_run_command()
    else:
        invalid_run_command()
    name = sys.argv[2].lower()

    file_name = None
    download_url = None
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
        c1 = ''
        c2 = ''
        c3 = ''
        cr = ''

    if name == "chromedriver":
        last = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        use_version = DEFAULT_CHROMEDRIVER_VERSION
        get_latest = False
        get_v_latest = False
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                uv_low = use_version.lower()
                if uv_low == "latest":
                    get_latest = True
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
        else:
            raise Exception("Cannot determine which version of chromedriver "
                            "to download!")
        found_chromedriver = False
        if get_latest:
            url_request = requests.get(last)
            if url_request.ok:
                found_chromedriver = True
                use_version = url_request.text
        elif get_v_latest:
            url_req = requests.get(last)
            if url_req.ok:
                latest_version = url_req.text
            last = last + "_" + use_version
            url_request = requests.get(last)
            if url_request.ok:
                found_chromedriver = True
                use_version = url_request.text
                if use_version == latest_version:
                    get_latest = True
        download_url = ("https://chromedriver.storage.googleapis.com/"
                        "%s/%s" % (use_version, file_name))
        url_request = None
        if not found_chromedriver:
            url_req = requests.get(last)
            if url_req.ok:
                latest_version = url_req.text
                if use_version == latest_version:
                    get_latest = True
            url_request = requests.get(download_url)
        if found_chromedriver or url_request.ok:
            p_version = use_version
            p_version = c3 + use_version + cr
            if get_latest:
                p_version = p_version + " " + c2 + "(Latest)" + cr
            else:
                not_latest = c5 + "(" + c4 + "NOT Latest" + c5 + ")" + cr
                p_version = p_version + " " + not_latest
            msg = c2 + "chromedriver version for download" + cr
            print("\n*** %s = %s" % (msg, p_version))
        else:
            raise Exception("Could not find chromedriver to download!\n")
        if not get_latest:
            to_upgrade = " " + c3 + "To upgrade" + cr
            run_this = c3 + "run this" + cr
            install_sb = c6 + "sbase install chromedriver latest" + cr
            print("\n %s to the latest version of chromedriver," % to_upgrade)
            print('   %s: >>> %s' % (run_this, install_sb))
            print('  (Requires the latest version of Chrome installed)')
    elif name == "geckodriver" or name == "firefoxdriver":
        use_version = DEFAULT_GECKODRIVER_VERSION
        found_geckodriver = False
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                if use_version.lower() == "latest":
                    last = ("https://api.github.com/repos/"
                            "mozilla/geckodriver/releases/latest")
                    url_request = requests.get(last)
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
            raise Exception("Cannot determine which version of geckodriver "
                            "(Firefox Driver) to download!")
        download_url = ("https://github.com/mozilla/geckodriver/"
                        "releases/download/"
                        "%s/%s" % (use_version, file_name))
        url_request = None
        if not found_geckodriver:
            url_request = requests.get(download_url)
        if found_geckodriver or url_request.ok:
            msg = c2 + "geckodriver version for download" + cr
            p_version = c3 + use_version + cr
            print("\n*** %s = %s" % (msg, p_version))
        else:
            raise Exception("\nCould not find the specified geckodriver "
                            "version to download!\n")
    elif name == "edgedriver" or name == "msedgedriver":
        name = "edgedriver"
        last = (
            "https://msedgewebdriverstorage.blob.core.windows.net"
            "/edgewebdriver/LATEST_STABLE")
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
            url_request = requests.get(last)
            if url_request.ok:
                use_version = url_request.text.split('\r')[0].split('\n')[0]
            else:
                use_version = DEFAULT_EDGEDRIVER_VERSION
        if "win64" in sys_plat or "x64" in sys_plat:
            file_name = "edgedriver_win64.zip"
        elif "win32" in sys_plat or "x86" in sys_plat:
            file_name = "edgedriver_win32.zip"
        elif "darwin" in sys_plat:
            file_name = "edgedriver_mac64.zip"
        else:
            raise Exception("Sorry! Microsoft WebDriver / EdgeDriver is "
                            "only for Windows or Mac operating systems!")
        download_url = ("https://msedgedriver.azureedge.net/"
                        "%s/%s" % (use_version, file_name))
        if not get_latest and not use_version == DEFAULT_EDGEDRIVER_VERSION:
            url_request = requests.get(download_url)
            if not url_request.ok:
                raise Exception(
                    "Could not find version [%s] of EdgeDriver!" % use_version)
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
            raise Exception("Sorry! IEDriver is only for "
                            "Windows-based operating systems!")
        download_url = ("https://selenium-release.storage.googleapis.com/"
                        "%s/%s" % (major_version, file_name))
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
            expected_contents = (['operadriver_mac64/',
                                  'operadriver_mac64/operadriver',
                                  'operadriver_mac64/sha512_sum'])
        elif "linux" in sys_plat:
            file_name = "operadriver_linux64.zip"
            platform_code = "linux64"
            inner_folder = "operadriver_%s/" % platform_code
            expected_contents = (['operadriver_linux64/',
                                  'operadriver_linux64/operadriver',
                                  'operadriver_linux64/sha512_sum'])
        elif "win32" in sys_plat:
            file_name = "operadriver_win32.zip"
            platform_code = "win32"
            inner_folder = "operadriver_%s/" % platform_code
            expected_contents = (['operadriver_win32/',
                                  'operadriver_win32/operadriver.exe',
                                  'operadriver_win32/sha512_sum'])
        elif "win64" in sys_plat or "x64" in sys_plat:
            file_name = "operadriver_win64.zip"
            platform_code = "win64"
            inner_folder = "operadriver_%s/" % platform_code
            expected_contents = (['operadriver_win64/',
                                  'operadriver_win64/operadriver.exe',
                                  'operadriver_win64/sha512_sum'])
        else:
            raise Exception("Cannot determine which version of Operadriver "
                            "to download!")

        download_url = ("https://github.com/operasoftware/operachromiumdriver/"
                        "releases/download/"
                        "%s/%s" % (use_version, file_name))
        msg = c2 + "operadriver version for download" + cr
        p_version = c3 + use_version + cr
        print("\n*** %s = %s" % (msg, p_version))
    else:
        invalid_run_command()

    if file_name is None or download_url is None:
        invalid_run_command()

    file_path = downloads_folder + '/' + file_name
    if not os.path.exists(downloads_folder):
        os.mkdir(downloads_folder)

    print('\nDownloading %s from:\n%s ...' % (file_name, download_url))
    remote_file = requests.get(download_url)
    with open(file_path, 'wb') as file:
        file.write(remote_file.content)
    print('Download Complete!\n')

    if file_name.endswith(".zip"):
        zip_file_path = file_path
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        contents = zip_ref.namelist()
        if len(contents) == 1:
            if name == "operadriver":
                raise Exception("Zip file for OperaDriver is missing content!")
            for f_name in contents:
                # Remove existing version if exists
                new_file = downloads_folder + '/' + str(f_name)
                if "Driver" in new_file or "driver" in new_file:
                    if os.path.exists(new_file):
                        os.remove(new_file)  # Technically the old file now
            print('Extracting %s from %s ...' % (contents, file_name))
            zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            print('Unzip Complete!\n')
            for f_name in contents:
                new_file = downloads_folder + '/' + str(f_name)
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
                expected_contents = (['Driver_Notes/',
                                      'Driver_Notes/LICENSE',
                                      'Driver_Notes/credits.html',
                                      'msedgedriver',
                                      'libc++.dylib'])
            else:
                # Windows
                expected_contents = (['Driver_Notes/',
                                      'Driver_Notes/credits.html',
                                      'Driver_Notes/LICENSE',
                                      'msedgedriver.exe'])
            if len(contents) > 5:
                raise Exception("Unexpected content in EdgeDriver Zip file!")
            for content in contents:
                if content not in expected_contents:
                    raise Exception("Expected file [%s] missing from [%s]" % (
                        content, expected_contents))
            # Zip file is valid. Proceed.
            driver_path = None
            driver_file = None
            for f_name in contents:
                print(f_name)
                # Remove existing version if exists
                str_name = str(f_name)
                new_file = downloads_folder + '/' + str_name
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
            print('Extracting %s from %s ...' % (contents, file_name))
            zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            print('Unzip Complete!\n')
            to_remove = (['%s/Driver_Notes/credits.html' % downloads_folder,
                          '%s/Driver_Notes/LICENSE' % downloads_folder])
            for file_to_remove in to_remove:
                if os.path.exists(file_to_remove):
                    os.remove(file_to_remove)
            if os.path.exists(downloads_folder + '/' + "Driver_Notes/"):
                # Only works if the directory is empty
                os.rmdir(downloads_folder + '/' + "Driver_Notes/")
            print("The file [%s] was saved to:\n%s\n" % (
                driver_file, driver_path))
            print("Making [%s %s] executable ..." % (driver_file, use_version))
            make_executable(driver_path)
            print("%s[%s] is now ready for use!%s" % (c1, driver_file, cr))
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
                new_file = downloads_folder + '/' + str_name
                if str_name == "operadriver" or str_name == "operadriver.exe":
                    driver_file = str_name
                    driver_path = new_file
                    if os.path.exists(new_file):
                        os.remove(new_file)
            if not driver_file or not driver_path:
                raise Exception("Operadriver missing from Zip file!")
            print('Extracting %s from %s ...' % (contents, file_name))
            zip_ref.extractall(downloads_folder)
            zip_ref.close()
            os.remove(zip_file_path)
            print('Unzip Complete!\n')
            inner_driver = downloads_folder + '/' + inner_folder + driver_file
            inner_sha = downloads_folder + '/' + inner_folder + "sha512_sum"
            shutil.copyfile(inner_driver, driver_path)
            pr_driver_path = c3 + driver_path + cr
            print("The file [%s] was saved to:\n%s\n" % (
                driver_file, pr_driver_path))
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
            if os.path.exists(downloads_folder + '/' + inner_folder):
                # Only works if the directory is empty
                os.rmdir(downloads_folder + '/' + inner_folder)
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
                new_file = downloads_folder + '/' + str(f_name)
                if "Driver" in new_file or "driver" in new_file:
                    if os.path.exists(new_file):
                        os.remove(new_file)  # Technically the old file now
            print('Extracting %s from %s ...' % (contents, file_name))
            tar.extractall(downloads_folder)
            tar.close()
            os.remove(tar_file_path)
            print('Unzip Complete!\n')
            for f_name in contents:
                new_file = downloads_folder + '/' + str(f_name)
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
