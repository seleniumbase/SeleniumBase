import re
from seleniumbase.config import settings


def set_settings(settings_file):
    if not settings_file.endswith(".py"):
        raise Exception("\n\n`%s` is not a Python file!\n\n" % settings_file)

    f = open(settings_file, "r")
    all_code = f.read()
    f.close()

    override_settings = {}
    num_settings = 0

    code_lines = all_code.split("\n")
    for line in code_lines:

        # KEY = "VALUE"
        data = re.match(r'^\s*([\S]+)\s*=\s*"([\S\s]+)"\s*$', line)
        if data:
            key = data.group(1)
            value = '"' + data.group(2) + '"'
            override_settings[key] = value
            num_settings += 1
            continue

        # KEY = 'VALUE'
        data = re.match(r"^\s*([\S]+)\s*=\s*'([\S\s]+)'\s*$", line)
        if data:
            key = data.group(1)
            value = "'" + data.group(2) + "'"
            override_settings[key] = value
            num_settings += 1
            continue

        # KEY = VALUE
        data = re.match(r"^\s*([\S]+)\s*=\s*([\S]+)\s*$", line)
        if data:
            key = data.group(1)
            value = data.group(2)
            override_settings[key] = value
            num_settings += 1
            continue

    for key in override_settings.keys():
        value = override_settings[key]
        if value.replace(".", "1").isdigit():
            if value.count(".") == 1:
                override_settings[key] = float(value)
            elif value.count(".") == 0:
                override_settings[key] = int(value)
            else:
                continue
        elif value == "True":
            override_settings[key] = True
        elif value == "False":
            override_settings[key] = False
        elif len(value) > 1 and value.startswith('"') and value.endswith('"'):
            override_settings[key] = value[1:-1]
        elif len(value) > 1 and value.startswith("'") and value.endswith("'"):
            override_settings[key] = value[1:-1]
        else:
            continue

        if key == "MINI_TIMEOUT":
            settings.MINI_TIMEOUT = override_settings[key]
        elif key == "SMALL_TIMEOUT":
            settings.SMALL_TIMEOUT = override_settings[key]
        elif key == "LARGE_TIMEOUT":
            settings.LARGE_TIMEOUT = override_settings[key]
        elif key == "EXTREME_TIMEOUT":
            settings.EXTREME_TIMEOUT = override_settings[key]
        elif key == "ARCHIVE_EXISTING_LOGS":
            settings.ARCHIVE_EXISTING_LOGS = override_settings[key]
        elif key == "ARCHIVE_EXISTING_DOWNLOADS":
            settings.ARCHIVE_EXISTING_DOWNLOADS = override_settings[key]
        elif key == "SCREENSHOT_NAME":
            settings.SCREENSHOT_NAME = override_settings[key]
        elif key == "BASIC_INFO_NAME":
            settings.BASIC_INFO_NAME = override_settings[key]
        elif key == "PAGE_SOURCE_NAME":
            settings.PAGE_SOURCE_NAME = override_settings[key]
        elif key == "LATEST_REPORT_DIR":
            settings.LATEST_REPORT_DIR = override_settings[key]
        elif key == "REPORT_ARCHIVE_DIR":
            settings.REPORT_ARCHIVE_DIR = override_settings[key]
        elif key == "HTML_REPORT":
            settings.HTML_REPORT = override_settings[key]
        elif key == "RESULTS_TABLE":
            settings.RESULTS_TABLE = override_settings[key]
        elif key == "WAIT_FOR_RSC_ON_PAGE_LOADS":
            settings.WAIT_FOR_RSC_ON_PAGE_LOADS = override_settings[key]
        elif key == "WAIT_FOR_RSC_ON_CLICKS":
            settings.WAIT_FOR_RSC_ON_CLICKS = override_settings[key]
        elif key == "WAIT_FOR_ANGULARJS":
            settings.WAIT_FOR_ANGULARJS = override_settings[key]
        elif key == "DEFAULT_DEMO_MODE_TIMEOUT":
            settings.DEFAULT_DEMO_MODE_TIMEOUT = override_settings[key]
        elif key == "HIGHLIGHTS":
            settings.HIGHLIGHTS = override_settings[key]
        elif key == "DEFAULT_MESSAGE_DURATION":
            settings.DEFAULT_MESSAGE_DURATION = override_settings[key]
        elif key == "DISABLE_CSP_ON_FIREFOX":
            settings.DISABLE_CSP_ON_FIREFOX = override_settings[key]
        elif key == "DISABLE_CSP_ON_CHROME":
            settings.DISABLE_CSP_ON_CHROME = override_settings[key]
        elif key == "RAISE_INVALID_PROXY_STRING_EXCEPTION":
            settings.RAISE_INVALID_PROXY_STRING_EXCEPTION = override_settings[
                key
            ]
        elif key == "MASTERQA_DEFAULT_VALIDATION_MESSAGE":
            settings.MASTERQA_DEFAULT_VALIDATION_MESSAGE = override_settings[
                key
            ]
        elif key == "MASTERQA_WAIT_TIME_BEFORE_VERIFY":
            settings.MASTERQA_WAIT_TIME_BEFORE_VERIFY = override_settings[key]
        elif key == "MASTERQA_START_IN_FULL_SCREEN_MODE":
            settings.MASTERQA_START_IN_FULL_SCREEN_MODE = override_settings[
                key
            ]
        elif key == "MASTERQA_MAX_IDLE_TIME_BEFORE_QUIT":
            settings.MASTERQA_MAX_IDLE_TIME_BEFORE_QUIT = override_settings[
                key
            ]
        elif key == "TOTP_KEY":
            settings.TOTP_KEY = override_settings[key]
        elif key == "DB_HOST":
            settings.DB_HOST = override_settings[key]
        elif key == "DB_PORT":
            settings.DB_PORT = override_settings[key]
        elif key == "DB_USERNAME":
            settings.DB_USERNAME = override_settings[key]
        elif key == "DB_PASSWORD":
            settings.DB_PASSWORD = override_settings[key]
        elif key == "DB_SCHEMA":
            settings.DB_SCHEMA = override_settings[key]
        elif key == "S3_LOG_BUCKET":
            settings.S3_LOG_BUCKET = override_settings[key]
        elif key == "S3_BUCKET_URL":
            settings.S3_BUCKET_URL = override_settings[key]
        elif key == "S3_SELENIUM_ACCESS_KEY":
            settings.S3_SELENIUM_ACCESS_KEY = override_settings[key]
        elif key == "S3_SELENIUM_SECRET_KEY":
            settings.S3_SELENIUM_SECRET_KEY = override_settings[key]
        elif key == "ENCRYPTION_KEY":
            settings.ENCRYPTION_KEY = override_settings[key]
        elif key == "OBFUSCATION_START_TOKEN":
            settings.OBFUSCATION_START_TOKEN = override_settings[key]
        elif key == "OBFUSCATION_END_TOKEN":
            settings.OBFUSCATION_END_TOKEN = override_settings[key]
        else:
            continue

    if num_settings == 0:
        raise Exception("Unable to parse the settings file!")

    return override_settings
