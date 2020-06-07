"""
Installs the specified web driver.

Usage:
        seleniumbase install {chromedriver|geckodriver|edgedriver|
                              iedriver|operadriver} [OPTIONS]
Options:
        VERSION         Specify the version.
                        (Default chromedriver version = 2.44)
                        Use "latest" for the latest version.
        -p OR --path    Also copy the driver to /usr/local/bin
Example:
        seleniumbase install chromedriver
        seleniumbase install geckodriver
        seleniumbase install edgedriver
        seleniumbase install chromedriver 83.0.4103.39
        seleniumbase install chromedriver latest
        seleniumbase install chromedriver -p
        seleniumbase install chromedriver latest -p
        seleniumbase install edgedriver 79.0.309.65
Output:
        Installs the chosen webdriver to seleniumbase/drivers/
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
import urllib3
import zipfile
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
urllib3.disable_warnings()
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
LOCAL_PATH = "/usr/local/bin/"  # On Mac and Linux systems
DEFAULT_CHROMEDRIVER_VERSION = "2.44"
DEFAULT_GECKODRIVER_VERSION = "v0.26.0"
DEFAULT_EDGEDRIVER_VERSION = "79.0.309.65"
DEFAULT_OPERADRIVER_VERSION = "v.81.0.4044.113"


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
    use_version = ""
    new_file = ""
    f_name = ""

    if name == "chromedriver":
        use_version = DEFAULT_CHROMEDRIVER_VERSION
        get_latest = False
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                if use_version.lower() == "latest":
                    get_latest = True
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
            last = "http://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            url_request = requests.get(last)
            if url_request.ok:
                found_chromedriver = True
                use_version = url_request.text
        download_url = ("http://chromedriver.storage.googleapis.com/"
                        "%s/%s" % (use_version, file_name))
        url_request = None
        if not found_chromedriver:
            url_request = requests.get(download_url)
        if found_chromedriver or url_request.ok:
            print("\n* chromedriver version for download = %s" % use_version)
        else:
            raise Exception("Could not find chromedriver to download!\n")
    elif name == "geckodriver" or name == "firefoxdriver":
        use_version = DEFAULT_GECKODRIVER_VERSION
        if "win32" in sys_plat or "win64" in sys_plat or "x64" in sys_plat:
            use_version = "v0.24.0"
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
            print("\n* geckodriver version for download = %s" % use_version)
        else:
            raise Exception("\nCould not find the specified geckodriver "
                            "version to download!\n")
    elif name == "edgedriver" or name == "msedgedriver":
        name = "edgedriver"
        use_version = DEFAULT_EDGEDRIVER_VERSION
        if num_args == 4 or num_args == 5:
            if "-p" not in sys.argv[3].lower():
                use_version = sys.argv[3]
                if use_version.lower() == "latest":
                    use_version = DEFAULT_EDGEDRIVER_VERSION
            else:
                copy_to_path = True
        if num_args == 5:
            if "-p" in sys.argv[4].lower():
                copy_to_path = True
            else:
                invalid_run_command()
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
        download_url = ("http://selenium-release.storage.googleapis.com/"
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
                print("The file [%s] was saved to:\n%s\n" % (f_name, new_file))
                print("Making [%s %s] executable ..." % (f_name, use_version))
                make_executable(new_file)
                print("[%s] is now ready for use!" % f_name)
                if copy_to_path and os.path.exists(LOCAL_PATH):
                    path_file = LOCAL_PATH + f_name
                    shutil.copyfile(new_file, path_file)
                    make_executable(path_file)
                    print("Also copied to: %s" % path_file)
            print("")
        elif name == "edgedriver" or name == "msedgedriver":
            if "darwin" in sys_plat or "linux" in sys_plat:
                # Was expecting to be on a Windows OS at this point
                raise Exception("Unexpected file format for msedgedriver!")
            expected_contents = (['Driver_Notes/',
                                  'Driver_Notes/credits.html',
                                  'Driver_Notes/LICENSE',
                                  'msedgedriver.exe'])
            if len(contents) > 4:
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
                if str_name == "msedgedriver.exe":
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
            print("[%s] is now ready for use!" % driver_file)
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
            print("The file [%s] was saved to:\n%s\n" % (
                driver_file, driver_path))
            print("Making [%s %s] executable ..." % (driver_file, use_version))
            make_executable(driver_path)
            print("[%s] is now ready for use!" % driver_file)
            if copy_to_path and os.path.exists(LOCAL_PATH):
                path_file = LOCAL_PATH + driver_file
                shutil.copyfile(driver_path, path_file)
                make_executable(path_file)
                print("Also copied to: %s" % path_file)
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
                print("The file [%s] was saved to:\n%s\n" % (f_name, new_file))
                print("Making [%s %s] executable ..." % (f_name, use_version))
                make_executable(new_file)
                print("[%s] is now ready for use!" % f_name)
                if copy_to_path and os.path.exists(LOCAL_PATH):
                    path_file = LOCAL_PATH + f_name
                    shutil.copyfile(new_file, path_file)
                    make_executable(path_file)
                    print("Also copied to: %s" % path_file)
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
            print("[%s] is now ready for use!" % file_name)
            print("Location of [%s]:\n%s\n" % (file_name, file_path))


if __name__ == "__main__":
    main()
