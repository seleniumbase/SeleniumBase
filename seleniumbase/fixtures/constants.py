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


class Browser:
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "ie"
    SAFARI = "safari"
    GOOGLE_CHROME = "chrome"
    PHANTOM_JS = "phantomjs"
    HTML_UNIT = "htmlunit"

    VERSION = {
        "firefox": None,
        "ie": None,
        "chrome": None,
        "phantomjs": None,
        "htmlunit": None
    }

    LATEST = {
        "firefox": None,
        "ie": None,
        "chrome": None,
        "phantomjs": None,
        "htmlunit": None
    }


class State:
    NOTRUN = "NotRun"
    ERROR = "Error"
    FAILURE = "Fail"
    PASS = "Pass"
    SKIP = "Skip"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"
