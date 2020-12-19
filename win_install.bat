@ECHO OFF
py -m pip install --upgrade pip
pip install -e . --upgrade --no-cache-dir --progress-bar=off
seleniumbase install chromedriver
seleniumbase install geckodriver
seleniumbase install edgedriver
