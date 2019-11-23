"""
SeleniumBase constants are stored in this file.
"""


class Environment:
    # Usage Example => "--env=qa" => Then access value in tests with "self.env"
    QA = "qa"
    STAGING = "staging"
    DEVELOP = "develop"
    PRODUCTION = "production"
    MASTER = "master"
    LOCAL = "local"
    TEST = "test"


class Files:
    DOWNLOADS_FOLDER = "downloaded_files"
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"


class SavedCookies:
    STORAGE_FOLDER = "saved_cookies"


class VisualBaseline:
    STORAGE_FOLDER = "visual_baseline"


class JQuery:
    VER = "3.4.1"
    MIN_JS = "//cdnjs.cloudflare.com/ajax/libs/jquery/%s/jquery.min.js" % VER
    # MIN_JS = "//ajax.aspnetcdn.com/ajax/jQuery/jquery-%s.min.js" % VER
    # MIN_JS = "//ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js" % VER


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
                      "messenger/%s/css/messenger-theme-flat.min.css" % VER)
    THEME_FUTURE_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                        "messenger/%s/css/"
                        "messenger-theme-future.min.css" % VER)
    THEME_BLOCK_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                       "messenger/%s/css/messenger-theme-block.min.css" % VER)
    THEME_AIR_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/css/messenger-theme-air.min.css" % VER)
    THEME_ICE_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/css/messenger-theme-ice.min.css" % VER)
    SPINNER_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
                   "messenger/%s/css/messenger-spinner.min.css" % VER)


class Underscore:
    VER = "1.9.1"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "underscore.js/%s/underscore-min.js" % VER)


class Backbone:
    VER = "1.4.0"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "backbone.js/%s/backbone-min.js" % VER)


class HtmlInspector:
    VER = "0.8.2"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "html-inspector/%s/html-inspector.min.js" % VER)


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


class JqueryConfirm:
    VER = "3.3.4"
    MIN_CSS = ("//cdnjs.cloudflare.com/ajax/libs/"
               "jquery-confirm/%s/jquery-confirm.min.css" % VER)
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "jquery-confirm/%s/jquery-confirm.min.js" % VER)


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
    VER = "1.4.7"
    MIN_JS = ("//cdnjs.cloudflare.com/ajax/libs/"
              "tether/%s/js/tether.min.js" % VER)


class ValidBrowsers:
    valid_browsers = (
        ["chrome", "edge", "firefox", "ie",
         "opera", "phantomjs", "safari",
         "android", "iphone", "ipad", "remote"])


class Browser:
    GOOGLE_CHROME = "chrome"
    EDGE = "edge"
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "ie"
    OPERA = "opera"
    PHANTOM_JS = "phantomjs"
    SAFARI = "safari"
    ANDROID = "android"
    IPHONE = "iphone"
    IPAD = "ipad"
    REMOTE = "remote"

    VERSION = {
        "chrome": None,
        "edge": None,
        "firefox": None,
        "ie": None,
        "opera": None,
        "phantomjs": None,
        "safari": None,
        "android": None,
        "iphone": None,
        "ipad": None,
        "remote": None
    }

    LATEST = {
        "chrome": None,
        "edge": None,
        "firefox": None,
        "ie": None,
        "opera": None,
        "phantomjs": None,
        "safari": None,
        "android": None,
        "iphone": None,
        "ipad": None,
        "remote": None
    }


class State:
    NOTRUN = "NotRun"
    ERROR = "Error"
    FAILURE = "Fail"
    PASS = "Pass"
    SKIP = "Skip"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"
