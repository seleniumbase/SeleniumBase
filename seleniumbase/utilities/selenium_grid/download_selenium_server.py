""" Downloads the Selenium Server JAR file and renames it. """

import os
import sys
if sys.version_info[0] == 2:
    from urllib import urlopen
else:
    from urllib.request import urlopen

SELENIUM_JAR = ("http://selenium-release.storage.googleapis.com"
                "/3.14/selenium-server-standalone-3.14.0.jar")
JAR_FILE = "selenium-server-standalone-3.14.0.jar"
RENAMED_JAR_FILE = "selenium-server-standalone.jar"

dir_path = os.path.dirname(os.path.realpath(__file__))
FULL_EXPECTED_PATH = dir_path + "/" + RENAMED_JAR_FILE
FULL_DOWNLOAD_PATH = os.getcwd() + '/' + RENAMED_JAR_FILE


def download_selenium_server():
    """
    Downloads the Selenium Server JAR file from its
    online location and stores it locally.
    """
    try:
        local_file = open(JAR_FILE, 'wb')
        remote_file = urlopen(SELENIUM_JAR)
        print('Downloading the Selenium Server JAR file...\n')
        local_file.write(remote_file.read())
        local_file.close()
        remote_file.close()
        print('Download Complete!')
    except Exception:
        raise Exception("Error downloading the Selenium Server JAR file.\n"
                        "Details: %s" % sys.exc_info()[1])


def is_available_locally():
    return os.path.isfile(FULL_EXPECTED_PATH)


def main():
    if not is_available_locally():
        download_selenium_server()
        for filename in os.listdir("."):
            # If multiple copies exist, keep only the latest and rename it.
            if filename.startswith("selenium-server-standalone-"):
                os.rename(filename, RENAMED_JAR_FILE)
                if FULL_DOWNLOAD_PATH != FULL_EXPECTED_PATH:
                    os.rename(RENAMED_JAR_FILE, FULL_EXPECTED_PATH)
        print("%s\n" % FULL_EXPECTED_PATH)


if __name__ == "__main__":
    main()
