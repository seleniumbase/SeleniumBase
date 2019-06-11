@ECHO OFF
python -m easy_install --upgrade pip
pip install -e . --upgrade --no-cache-dir --progress-bar off
seleniumbase install chromedriver
seleniumbase install geckodriver
