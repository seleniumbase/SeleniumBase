""" Download and run the selenium server jar file """

import subprocess
import os
import socket
import urllib
import sys
import time

SELENIUM_JAR = ("http://selenium-release.storage.googleapis.com"
                "/2.53/selenium-server-standalone-2.53.0.jar")
JAR_FILE = "selenium-server-standalone-2.53.0.jar"
try:
    import selenium
    if selenium.__version__[0] == '3':
        SELENIUM_JAR = ("http://selenium-release.storage.googleapis.com"
                        "/3.3/selenium-server-standalone-3.3.1.jar")
        JAR_FILE = "selenium-server-standalone-3.3.1.jar"
except Exception:
    pass


def download_selenium():
    """
    Downloads the selenium server jar file from its
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
        raise Exception("Error while downloading Selenium Server. Details: %s"
                        % sys.exc_info()[1])


def is_running_locally(host, port):
    socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_s.connect((host, port))
        socket_s.close()
        return True
    except:
        return False


def is_available_locally():
    return os.path.isfile(JAR_FILE)


def start_selenium_server(selenium_jar_location, port, file_path):

    """
    Starts selenium on the specified port
    and configures the output and error files.
    Throws an exeption if the server does not start.
    """

    process_args = None
    process_args = ["java", "-jar", selenium_jar_location, "-port", port]
    selenium_exec = subprocess.Popen(
        process_args,
        stdout=open("%s/log_seleniumOutput.txt" % (file_path), "w"),
        stderr=open("%s/log_seleniumError.txt" % (file_path), "w"))
    time.sleep(2)
    if selenium_exec.poll() == 1:
        raise StartSeleniumException("The selenium server did not start."
                                     "Do you already have one runing?")
    return selenium_exec


def stop_selenium_server(selenium_server_process):
    """Kills the selenium server.  We are expecting an error 143"""

    try:
        selenium_server_process.terminate()
        return selenium_server_process.poll() == 143
    except Exception:
        raise Exception(
            "Cannot kill selenium process. Details: " + sys.exc_info()[1])


class StartSeleniumException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def execute_selenium(host, port, file_path):
    if is_running_locally(host, port):
        return
    if not is_available_locally():
        download_selenium()
    try:
        return start_selenium_server(JAR_FILE, port, file_path)
    except StartSeleniumException:
        print("Selenium Server might already be running. Continuing... ")
