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


class Presentations:
    SAVED_FOLDER = "saved_presentations"


class Charts:
    SAVED_FOLDER = "saved_charts"


class Dashboard:
    TITLE = "SeleniumBase Test Results Dashboard"
    STYLE_CSS = 'https://seleniumbase.io/cdn/css/pytest_style.css'
    META_REFRESH_HTML = '<meta http-equiv="refresh" content="10">'
    # LIVE_JS = 'https://livejs.com/live.js#html'
    LIVE_JS = 'https://seleniumbase.io/cdn/js/live.js#html'


class SavedCookies:
    STORAGE_FOLDER = "saved_cookies"


class Tours:
    EXPORTED_TOURS_FOLDER = "tours_exported"


class VisualBaseline:
    STORAGE_FOLDER = "visual_baseline"


class Values:
    # Demo Mode has slow scrolling to see where you are on the page better.
    # However, a regular slow scroll takes too long to cover big distances.
    # If the scroll distance is greater than SSMD, a slow scroll speeds up.
    SSMD = 900  # Smooth Scroll Minimum Distance (for advanced slow scroll)


class JQuery:
    VER = "3.5.1"
    MIN_JS = (
        "https://cdnjs.cloudflare.com/ajax/libs/jquery/%s/jquery.min.js" % VER)
    # MIN_JS = (
    #    "https://ajax.aspnetcdn.com/ajax/jQuery/jquery-%s.min.js" % VER)
    # MIN_JS = (
    #    "https://ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js" % VER)


class Messenger:
    VER = "1.5.0"
    MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
               "messenger/%s/css/messenger.min.css" % VER)
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "messenger/%s/js/messenger.min.js" % VER)
    THEME_FLAT_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/js/messenger-theme-flat.js" % VER)
    THEME_FUTURE_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                       "messenger/%s/js/messenger-theme-future.js" % VER)
    THEME_FLAT_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                      "messenger/%s/css/messenger-theme-flat.min.css" % VER)
    THEME_FUTURE_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                        "messenger/%s/css/"
                        "messenger-theme-future.min.css" % VER)
    THEME_BLOCK_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                       "messenger/%s/css/messenger-theme-block.min.css" % VER)
    THEME_AIR_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/css/messenger-theme-air.min.css" % VER)
    THEME_ICE_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "messenger/%s/css/messenger-theme-ice.min.css" % VER)
    SPINNER_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                   "messenger/%s/css/messenger-spinner.min.css" % VER)


class Underscore:
    VER = "1.12.0"
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "underscore.js/%s/underscore-min.js" % VER)


class Backbone:
    VER = "1.4.0"
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "backbone.js/%s/backbone-min.js" % VER)


class HtmlInspector:
    VER = "0.8.2"
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "html-inspector/%s/html-inspector.min.js" % VER)


class PrettifyJS:
    RUN_PRETTIFY_JS = ("https://cdn.jsdelivr.net/gh/google/"
                       "code-prettify@master/loader/run_prettify.js")


class Reveal:
    VER = "3.8.0"
    MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
               "reveal.js/%s/css/reveal.min.css" % VER)
    SERIF_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "reveal.js/%s/css/theme/serif.min.css" % VER)
    WHITE_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "reveal.js/%s/css/theme/white.min.css" % VER)
    BLACK_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "reveal.js/%s/css/theme/black.min.css" % VER)
    SKY_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                   "reveal.js/%s/css/theme/sky.min.css" % VER)
    MOON_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                    "reveal.js/%s/css/theme/moon.min.css" % VER)
    NIGHT_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "reveal.js/%s/css/theme/night.min.css" % VER)
    LEAGUE_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                      "reveal.js/%s/css/theme/league.min.css" % VER)
    BEIGE_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "reveal.js/%s/css/theme/beige.min.css" % VER)
    BLOOD_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                     "reveal.js/%s/css/theme/blood.min.css" % VER)
    SIMPLE_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                      "reveal.js/%s/css/theme/simple.min.css" % VER)
    SOLARIZED_MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                         "reveal.js/%s/css/theme/solarized.min.css" % VER)
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "reveal.js/%s/js/reveal.min.js" % VER)


class HighCharts:
    VER = "8.2.2"
    HC_CSS = ("https://code.highcharts.com/%s/css/highcharts.css" % VER)
    HC_JS = ("https://code.highcharts.com/%s/highcharts.js" % VER)
    EXPORTING_JS = ("https://code.highcharts.com/"
                    "%s/modules/exporting.js" % VER)
    EXPORT_DATA_JS = ("https://code.highcharts.com/"
                      "%s/modules/export-data.js" % VER)
    ACCESSIBILITY_JS = ("https://code.highcharts.com/"
                        "%s/modules/accessibility.js" % VER)


class BootstrapTour:
    VER = "0.11.0"
    MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
               "bootstrap-tour/%s/css/bootstrap-tour-standalone.min.css" % VER)
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "bootstrap-tour/%s/js/bootstrap-tour-standalone.min.js" % VER)


class DriverJS:
    VER = "0.9.8"
    MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
               "driver.js/%s/driver.min.css" % VER)
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "driver.js/%s/driver.min.js" % VER)


class Hopscotch:
    VER = "0.3.1"
    MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
               "hopscotch/%s/css/hopscotch.min.css" % VER)
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "hopscotch/%s/js/hopscotch.min.js" % VER)


class IntroJS:
    VER = "2.9.3"
    MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
               "intro.js/%s/introjs.css" % VER)
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "intro.js/%s/intro.min.js" % VER)


class JqueryConfirm:
    VER = "3.3.4"
    MIN_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
               "jquery-confirm/%s/jquery-confirm.min.css" % VER)
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "jquery-confirm/%s/jquery-confirm.min.js" % VER)


class Shepherd:
    VER = "1.8.1"
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
              "shepherd/%s/js/shepherd.min.js" % VER)
    THEME_ARROWS_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                        "shepherd/%s/css/shepherd-theme-arrows.css" % VER)
    THEME_ARR_FIX_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                         "shepherd/%s/css/shepherd-theme-arrows-fix.css" % VER)
    THEME_DEFAULT_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                         "shepherd/%s/css/shepherd-theme-default.css" % VER)
    THEME_DARK_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                      "shepherd/%s/css/shepherd-theme-dark.css" % VER)
    THEME_SQ_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                    "shepherd/%s/css/shepherd-theme-square.css" % VER)
    THEME_SQ_DK_CSS = ("https://cdnjs.cloudflare.com/ajax/libs/"
                       "shepherd/%s/css/shepherd-theme-square-dark.css" % VER)


class Tether:
    VER = "1.4.7"
    MIN_JS = ("https://cdnjs.cloudflare.com/ajax/libs/"
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
    PASSED = "Passed"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    UNTESTED = "Untested"
    ERROR = "Error"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"
