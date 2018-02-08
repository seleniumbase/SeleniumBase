""" Downloads the Selenium Server JAR file and renames it. """

import os
import sys
import urllib

SELENIUM_JAR = ("http://selenium-release.storage.googleapis.com"
                "/2.53/selenium-server-standalone-2.53.0.jar")
JAR_FILE = "selenium-server-standalone-2.53.0.jar"
try:
    import selenium
    if selenium.__version__[0] == '3':
        SELENIUM_JAR = ("http://selenium-release.storage.googleapis.com"
                        "/3.8/selenium-server-standalone-3.8.1.jar")
        JAR_FILE = "selenium-server-standalone-3.8.1.jar"
except Exception:
    pass

RENAMED_JAR_FILE = "selenium-server-standalone.jar"


def download_selenium():
    """
    Downloads the Selenium Server JAR file from its
    online location and stores it locally.
    """
    try:
        local_file = open(JAR_FILE, 'wb')
        remote_file = urllib.urlopen(SELENIUM_JAR)
        print('Downloading Selenium Server JAR File...\n')
        local_file.write(remote_file.read())
        local_file.close()
        remote_file.close()
        print('Download Complete!\n')
    except Exception:
        raise Exception("Error downloading the Selenium Server JAR file.\n"
                        "Details: %s" % sys.exc_info()[1])


def is_available_locally():
    return os.path.isfile(RENAMED_JAR_FILE)


if not is_available_locally():
    download_selenium()
    for filename in os.listdir("."):
        if filename.startswith("selenium-server-standalone-"):
            os.rename(filename, RENAMED_JAR_FILE)
