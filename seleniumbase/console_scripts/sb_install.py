"""
Installs the specified web driver.

Usage:
        seleniumbase install {chromedriver|geckodriver|edgedriver|
                              iedriver|operadriver}
Output:
        Installs the specified webdriver.
        (chromedriver is required for Chrome automation)
        (geckodriver is required for Firefox automation)
        (edgedriver is required for MS Edge automation)
        (iedriver is required for Internet Explorer automation)
        (operadriver is required for Opera Browser automation)
"""

import os
import platform
import requests
import shutil
import sys
import tarfile
import zipfile
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))


def invalid_run_command():
    exp = ("  ** install **\n\n")
    exp += "  Usage:\n"
    exp += "          seleniumbase install [DRIVER_NAME]\n"
    exp += "              (Drivers: chromedriver, geckodriver, edgedriver,\n"
    exp += "                        iedriver, operadriver)\n"
    exp += "  Example:\n"
    exp += "          seleniumbase install chromedriver\n"
    exp += "  Output:\n"
    exp += "          Installs the specified webdriver.\n"
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


def main():
    num_args = len(sys.argv)
    if sys.argv[0].split('/')[-1].lower() == "seleniumbase" or (
            sys.argv[0].split('\\')[-1].lower() == "seleniumbase"):
        if num_args < 3 or num_args > 3:
            invalid_run_command()
    else:
        invalid_run_command()
    name = sys.argv[num_args - 1].lower()

    file_name = None
    download_url = None
    downloads_folder = DRIVER_DIR
    sys_plat = sys.platform
    expected_contents = None
    platform_code = None
    inner_folder = None

    if name == "chromedriver":
        latest_version = "2.46"
        if "darwin" in sys_plat:
            file_name = "chromedriver_mac64.zip"
        elif "linux" in sys_plat:
            latest_version = "2.40"  # Linux machines may need the old driver
            file_name = "chromedriver_linux64.zip"
        elif "win32" in sys_plat or "win64" in sys_plat or "x64" in sys_plat:
            file_name = "chromedriver_win32.zip"  # Works for win32 / win_x64
        else:
            raise Exception("Cannot determine which version of Chromedriver "
                            "to download!")
        download_url = ("http://chromedriver.storage.googleapis.com/"
                        "%s/%s" % (latest_version, file_name))
        # Forcing Chromedriver v2.40 for now, even though it's not the latest.
        get_latest = False
        if get_latest:
            last = "http://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            print('\nLocating the latest version of Chromedriver...')
            latest_version = requests.get(last).text
            if not requests.get(download_url).ok:
                fallback_version = "2.40"
                download_url = ("http://chromedriver.storage.googleapis.com/"
                                "%s/%s" % (fallback_version, file_name))
            else:
                download_url = ("http://chromedriver.storage.googleapis.com/"
                                "%s/%s" % (latest_version, file_name))
            print("Found %s" % download_url)
    elif name == "geckodriver" or name == "firefoxdriver":
        latest_version = "v0.24.0"
        if "darwin" in sys_plat:
            file_name = "geckodriver-%s-macos.tar.gz" % latest_version
        elif "linux" in sys_plat:
            arch = platform.architecture()[0]
            if "64" in arch:
                file_name = "geckodriver-%s-linux64.tar.gz" % latest_version
            else:
                file_name = "geckodriver-%s-linux32.tar.gz" % latest_version
        elif "win32" in sys_plat or "win64" in sys_plat or "x64" in sys_plat:
            file_name = "geckodriver-%s-win64.zip" % latest_version
        else:
            raise Exception("Cannot determine which version of Geckodriver "
                            "(Firefox Driver) to download!")

        download_url = ("https://github.com/mozilla/geckodriver/"
                        "releases/download/"
                        "%s/%s" % (latest_version, file_name))
    elif name == "edgedriver" or name == "microsoftwebdriver":
        name = "edgedriver"
        version_code = "F/8/A/F8AF50AB-3C3A-4BC4-8773-DC27B32988DD"
        if "win32" in sys_plat or "win64" in sys_plat or "x64" in sys_plat:
            file_name = "MicrosoftWebDriver.exe"
        else:
            raise Exception("Sorry! Microsoft WebDriver / EdgeDriver is "
                            "only for Windows-based operating systems!")
        download_url = ("https://download.microsoft.com/download/"
                        "%s/%s" % (version_code, file_name))
    elif name == "iedriver":
        major_version = "3.14"
        full_version = "3.14.0"
        if "win32" in sys_plat:
            file_name = "IEDriverServer_Win32_%s.zip" % full_version
        elif "win64" in sys_plat or "x64" in sys_plat:
            file_name = "IEDriverServer_x64_%s.zip" % full_version
        else:
            raise Exception("Sorry! IEDriver is only for "
                            "Windows-based operating systems!")
        download_url = ("http://selenium-release.storage.googleapis.com/"
                        "%s/%s" % (major_version, file_name))
    elif name == "operadriver" or name == "operachromiumdriver":
        name = "operadriver"
        latest_version = "v.2.40"
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
                        "%s/%s" % (latest_version, file_name))
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
                # remove existing version if exists
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
                print("%s saved!\n" % new_file)
                print("Making %s executable ..." % new_file)
                make_executable(new_file)
                print("%s is now ready for use!" % new_file)
            print("")
        elif name == "operadriver":
            if len(contents) != 3:
                raise Exception("Unexpected content in OperaDriver Zip file!")
            elif sorted(contents) != sorted(expected_contents):
                raise Exception("Unexpected content in OperaDriver Zip file!")
            # Zip file is valid. Proceed.
            driver_path = None
            driver_file = None
            for f_name in contents:
                # remove existing version if exists
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
            print("%s saved!\n" % driver_path)
            print("Making %s executable ..." % driver_path)
            make_executable(driver_path)
            print("%s is now ready for use!" % driver_path)
            # clean up extra files
            if os.path.exists(inner_driver):
                os.remove(inner_driver)
            if os.path.exists(inner_sha):
                os.remove(inner_sha)
            if os.path.exists(downloads_folder + '/' + inner_folder):
                # only works if the directory is empty
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
                # remove existing version if exists
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
                print("%s saved!\n" % new_file)
                print("Making %s executable ..." % new_file)
                make_executable(new_file)
                print("%s is now ready for use!" % new_file)
            print("")
        elif len(contents) == 0:
            raise Exception("Tar file %s is empty!" % tar_file_path)
        else:
            raise Exception("Expecting only one file in %s!" % tar_file_path)
    else:
        # Not a .zip file or a .tar.gz file. Just a direct download.
        if "Driver" in file_name or "driver" in file_name:
            print("Making %s executable ..." % file_path)
            make_executable(file_path)
            print("%s is now ready for use!\n" % file_path)


if __name__ == "__main__":
    main()
