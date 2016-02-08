""" Download the selenium server jar file """

import os
from seleniumbase.core import selenium_launcher

if not selenium_launcher.is_available_locally():
    selenium_launcher.download_selenium()

for filename in os.listdir("."):
    if filename.startswith("selenium-server-standalone-"):
        os.rename(filename, "selenium-server-standalone.jar")
