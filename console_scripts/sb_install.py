"""
Installs the specified web driver.

Usage:
        seleniumbase install {chromedriver|geckodriver|edgedriver}
Output:
        Installs the specified webdriver.
        (chromedriver is required for Chrome automation)
        (geckodriver is required for Firefox automation)
        (edgedriver is required for MS Edge automation)
"""

import os
import platform
import requests
import sys
import tarfile
import zipfile
import drivers  # webdriver storage folder for SeleniumBase
if sys.version_info[0] == 2:
    from urllib import urlopen
else:
    from urllib.request import urlopen
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))


def invalid_run_command():
    exp = ("  ** install **\n\n")
    exp += "  Usage:\n"
    exp += "          seleniumbase install [DRIVER_NAME]\n"
    exp += "              (Drivers: chromedriver, geckodriver, edgedriver)\n"
    exp += "  Example:\n"
    exp += "          seleniumbase install chromedriver\n"
    exp += "  Output:\n"
    exp += "          Installs the specified webdriver.\n"
    exp += "          (chromedriver is required for Chrome automation)\n"
    exp += "          (geckodriver is required for Firefox automation)\n"
    exp += "          (edgedriver is required for MS Edge automation)\n"
    print("")
    raise Exception('INVALID RUN COMMAND!\n\n%s' % exp)


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def main():
    num_args = len(sys.argv)
    if sys.argv[0].split('/')[-1] == "seleniumbase" or (
            sys.argv[0].split('\\')[-1] == "seleniumbase"):
        if num_args < 3 or num_args > 3:
            invalid_run_command()
    else:
        invalid_run_command()
    name = sys.argv[num_args-1]

    file_name = None
    download_url = None
    downloads_folder = DRIVER_DIR

    if name == "chromedriver":
        if "darwin" in sys.platform:
            file_name = "chromedriver_mac64.zip"
        elif "linux" in sys.platform:
            file_name = "chromedriver_linux64.zip"
        elif "win32" in sys.platform or "win64" in sys.platform:
            file_name = "chromedriver_win32.zip"  # Works for win32 and win64
        else:
            raise Exception("Cannon determine which version of Chromedriver "
                            "to download!")

        latest_version = requests.get(
            "http://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
        download_url = ("http://chromedriver.storage.googleapis.com/"
                        "%s/%s" % (latest_version, file_name))
        print('\nLocating the latest version of Chromedriver...')
        if not requests.get(download_url).ok:
            # If there's a problem with the latest Chromedriver, fall back
            fallback_version = "2.41"
            download_url = ("http://chromedriver.storage.googleapis.com/"
                            "%s/%s" % (fallback_version, file_name))
        print("Found %s" % download_url)
    elif name == "geckodriver" or name == "firefoxdriver":
        latest_version = "v0.21.0"
        if "darwin" in sys.platform:
            file_name = "geckodriver-%s-macos.tar.gz" % latest_version
        elif "linux" in sys.platform:
            arch = platform.architecture()[0]
            if "64" in arch:
                file_name = "geckodriver-%s-linux64.tar.gz" % latest_version
            else:
                file_name = "geckodriver-%s-linux32.tar.gz" % latest_version
        elif "win32" in sys.platform:
            file_name = "geckodriver-%s-win32.zip" % latest_version
        elif "win64" in sys.platform:
            file_name = "geckodriver-%s-win64.zip" % latest_version
        else:
            raise Exception("Cannon determine which version of Geckodriver "
                            "(Firefox Driver) to download!")

        download_url = ("http://github.com/mozilla/geckodriver/"
                        "releases/download/"
                        "%s/%s" % (latest_version, file_name))
    elif name == "edgedriver" or name == "microsoftwebdriver":
        if "win32" in sys.platform or "win64" in sys.platform:
            version_code = "F/8/A/F8AF50AB-3C3A-4BC4-8773-DC27B32988DD"
            file_name = "MicrosoftWebDriver.exe"
            download_url = ("https://download.microsoft.com/download/"
                            "%s/%s" % (version_code, file_name))
        else:
            raise Exception("Sorry! Microsoft WebDriver / EdgeDriver is "
                            "only for Windows-based operating systems!")
    else:
        invalid_run_command()

    if file_name is None or download_url is None:
        invalid_run_command()

    file_path = downloads_folder + '/' + file_name
    if not os.path.exists(downloads_folder):
        os.mkdir(downloads_folder)
    local_file = open(file_path, 'wb')
    remote_file = urlopen(download_url)
    print('\nDownloading %s from:\n%s ...' % (file_name, download_url))
    local_file.write(remote_file.read())
    local_file.close()
    remote_file.close()
    print('Download Complete!\n')

    if file_name.endswith(".zip"):
        zip_file_path = file_path
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        contents = zip_ref.namelist()
        if len(contents) == 1:
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
            print('Untar Complete!\n')
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
