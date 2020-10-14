@ECHO OFF
py -m pip --upgrade pip
pip install -e . --upgrade --no-cache-dir --progress-bar off
seleniumbase install chromedriver
seleniumbase install geckodriver
