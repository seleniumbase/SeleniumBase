"""
This class containts some frequently-used constants
"""


class Environment:
    QA = "qa"
    STAGING = "staging"
    PRODUCTION = "production"
    MASTER = "master"
    LOCAL = "local"
    TEST = "test"


class Files:
    DOWNLOADS_FOLDER = "downloaded_files"
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"


class ValidBrowsers:
    valid_browsers = ["firefox", "ie", "edge", "safari", "chrome", "phantomjs"]


class Browser:
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "ie"
    EDGE = "edge"
    SAFARI = "safari"
    GOOGLE_CHROME = "chrome"
    PHANTOM_JS = "phantomjs"

    VERSION = {
        "firefox": None,
        "ie": None,
        "edge": None,
        "safari": None,
        "chrome": None,
        "phantomjs": None
    }

    LATEST = {
        "firefox": None,
        "ie": None,
        "edge": None,
        "safari": None,
        "chrome": None,
        "phantomjs": None
    }


class State:
    NOTRUN = "NotRun"
    ERROR = "Error"
    FAILURE = "Fail"
    PASS = "Pass"
    SKIP = "Skip"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"
