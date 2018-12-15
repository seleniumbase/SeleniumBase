@ECHO OFF
python -m pip install --upgrade pip
pip install -e . --upgrade --no-cache-dir --progress-bar off
seleniumbase install geckodriver
seleniumbase install chromedriver
