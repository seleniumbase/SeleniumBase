"""
This class containts some frequently-used constants
"""


class Environment:
    # Usage Example => "--env=qa" => Then access value in tests with "self.env"
    QA = "qa"
    STAGING = "staging"
    PRODUCTION = "production"
    MASTER = "master"
    LOCAL = "local"
    TEST = "test"


class Files:
    DOWNLOADS_FOLDER = "downloaded_files"
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"


class JQuery:
    VER = "3.3.1"
    # MIN_JS = "//cdnjs.cloudflare.com/ajax/libs/jquery/%s/jquery.min.js" % VER
    MIN_JS = "//ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js" % VER


class Messenger:
    VER = "1.5.0"
    MIN_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
               "messenger/%s/css/messenger.min.css" % VER)
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "messenger/%s/js/messenger.min.js" % VER)
    THEME_FLAT_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/js/messenger-theme-flat.js" % VER)
    THEME_FUTURE_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
                       "messenger/%s/js/messenger-theme-future.js" % VER)
    THEME_FLAT_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                      "messenger/%s/css/messenger-theme-flat.css" % VER)
    THEME_FUTURE_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                        "messenger/%s/css/messenger-theme-future.css" % VER)
    THEME_BLOCK_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                       "messenger/%s/css/messenger-theme-block.css" % VER)
    THEME_AIR_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/css/messenger-theme-air.css" % VER)
    THEME_ICE_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/css/messenger-theme-ice.css" % VER)
    SPINNER_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                   "messenger/%s/css/messenger-spinner.css" % VER)


class Underscore:
    VER = "1.9.1"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "underscore.js/%s/underscore-min.js" % VER)


class Backbone:
    VER = "1.3.3"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "backbone.js/%s/backbone-min.js" % VER)


class BootstrapTour:
    VER = "0.11.0"
    MIN_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
               "bootstrap-tour/%s/css/bootstrap-tour-standalone.min.css" % VER)
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "bootstrap-tour/%s/js/bootstrap-tour-standalone.min.js" % VER)


class Hopscotch:
    VER = "0.3.1"
    MIN_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
               "hopscotch/%s/css/hopscotch.min.css" % VER)
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "hopscotch/%s/js/hopscotch.min.js" % VER)


class IntroJS:
    VER = "2.9.3"
    MIN_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
               "intro.js/%s/introjs.css" % VER)
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "intro.js/%s/intro.min.js" % VER)


class Shepherd:
    VER = "1.8.1"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "shepherd/%s/js/shepherd.min.js" % VER)
    THEME_ARROWS_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                        "shepherd/%s/css/shepherd-theme-arrows.css" % VER)
    THEME_ARR_FIX_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                         "shepherd/%s/css/shepherd-theme-arrows-fix.css" % VER)
    THEME_DEFAULT_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                         "shepherd/%s/css/shepherd-theme-default.css" % VER)
    THEME_DARK_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                      "shepherd/%s/css/shepherd-theme-dark.css" % VER)
    THEME_SQ_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                    "shepherd/%s/css/shepherd-theme-square.css" % VER)
    THEME_SQ_DK_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                       "shepherd/%s/css/shepherd-theme-square-dark.css" % VER)


class Tether:
    VER = "1.4.4"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "tether/%s/js/tether.min.js" % VER)


class ValidBrowsers:
    valid_browsers = (
        ["chrome", "edge", "firefox", "ie", "opera", "phantomjs", "safari"])


class Browser:
    GOOGLE_CHROME = "chrome"
    EDGE = "edge"
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "ie"
    OPERA = "opera"
    PHANTOM_JS = "phantomjs"
    SAFARI = "safari"

    VERSION = {
        "chrome": None,
        "edge": None,
        "firefox": None,
        "ie": None,
        "opera": None,
        "phantomjs": None,
        "safari": None
    }

    LATEST = {
        "chrome": None,
        "edge": None,
        "firefox": None,
        "ie": None,
        "opera": None,
        "phantomjs": None,
        "safari": None
    }


class State:
    NOTRUN = "NotRun"
    ERROR = "Error"
    FAILURE = "Fail"
    PASS = "Pass"
    SKIP = "Skip"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"
