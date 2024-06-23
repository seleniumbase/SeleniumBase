"""SeleniumBase constants"""
from seleniumbase.core import encoded_images


class Environment:
    # Usage Example => "--env=qa" => Then access value in tests with "self.env"
    QA = "qa"
    RC = "rc"
    STAGING = "staging"
    DEVELOP = "develop"
    PRODUCTION = "production"
    PERFORMANCE = "performance"
    REPLICA = "replica"
    FEDRAMP = "fedramp"
    OFFLINE = "offline"
    ONLINE = "online"
    MASTER = "master"
    REMOTE = "remote"
    LEGACY = "legacy"
    LOCAL = "local"
    ALPHA = "alpha"
    BETA = "beta"
    DEMO = "demo"
    GDPR = "gdpr"
    MAIN = "main"
    TEST = "test"
    GOV = "gov"
    NEW = "new"
    OLD = "old"
    UAT = "uat"


class ValidEnvs:
    valid_envs = [
        "qa",
        "rc",
        "staging",
        "develop",
        "production",
        "performance",
        "replica",
        "fedramp",
        "offline",
        "online",
        "master",
        "remote",
        "legacy",
        "local",
        "alpha",
        "beta",
        "demo",
        "gdpr",
        "main",
        "test",
        "gov",
        "new",
        "old",
        "uat",
    ]


class PatchPy311:
    # Now that unittest is "patched/fixed" in Python 3.11 and up,
    # this second patch might not be needed to fix error-handling.
    # Enabling this might slow things slightly to fix some things.
    PATCH = False


class PageLoadStrategy:
    # Usage Example => "--pls=none"
    NORMAL = "normal"
    EAGER = "eager"
    NONE = "none"


class Files:
    # This is a special downloads folder for files downloaded by tests.
    # The "downloaded_files" folder is DELETED when starting new tests.
    # Add "--archive-downloads" to save a copy in "archived_files".
    # (These folder names should NOT be changed.)
    DOWNLOADS_FOLDER = "downloaded_files"
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"


class Logs:
    # This is where log files from the latest run get saved.
    # The "latest_logs" folder is DELETED when starting new tests.
    # Add "--archive-logs" to save a copy of logs in "archived_logs".
    # (These folder names should NOT be changed.)
    LATEST = "latest_logs"
    SAVED = "archived_logs"


class Presentations:
    SAVED_FOLDER = "saved_presentations"


class Charts:
    SAVED_FOLDER = "saved_charts"


class Recordings:
    SAVED_FOLDER = "recordings"


class Dashboard:
    TITLE = "SeleniumBase Dashboard ⚪"
    # STYLE_CSS = "https://seleniumbase.io/cdn/css/pytest_style.css"
    STYLE_CSS = "assets/pytest_style.css"  # Generated before tests
    META_REFRESH_HTML = '<meta http-equiv="refresh" content="12">'
    # LIVE_JS = "https://livejs.com/live.js#html"
    # LIVE_JS = "https://seleniumbase.io/cdn/js/live.js#html"
    LIVE_JS = "assets/live.js#html"  # Generated before tests
    LOCKFILE = Files.DOWNLOADS_FOLDER + "/dashboard.lock"
    DASH_JSON = Files.DOWNLOADS_FOLDER + "/dashboard.json"
    DASH_PIE = Files.DOWNLOADS_FOLDER + "/dash_pie.json"

    def get_dash_pie_1():
        if not hasattr(encoded_images, "DASH_PIE_PNG_1"):
            encoded_images.DASH_PIE_PNG_1 = encoded_images.get_dash_pie_png1()
        return encoded_images.DASH_PIE_PNG_1

    def get_dash_pie_2():
        if not hasattr(encoded_images, "DASH_PIE_PNG_2"):
            encoded_images.DASH_PIE_PNG_2 = encoded_images.get_dash_pie_png2()
        return encoded_images.DASH_PIE_PNG_2

    def get_dash_pie_3():
        if not hasattr(encoded_images, "DASH_PIE_PNG_3"):
            encoded_images.DASH_PIE_PNG_3 = encoded_images.get_dash_pie_png3()
        return encoded_images.DASH_PIE_PNG_3


class PipInstall:
    # FINDLOCK - Checking to see if a package is installed
    # (Make sure a package isn't installed multiple times)
    FINDLOCK = Files.DOWNLOADS_FOLDER + "/pipfinding.lock"
    # LOCKFILE - Locking before performing any pip install
    # (Make sure that only one package installs at a time)
    LOCKFILE = Files.DOWNLOADS_FOLDER + "/pipinstall.lock"


class Report:
    def get_favicon():
        if not hasattr(encoded_images, "REPORT_FAVICON"):
            encoded_images.REPORT_FAVICON = encoded_images.get_report_favicon()
        return encoded_images.REPORT_FAVICON


class SideBySide:
    HTML_FILE = "side_by_side.html"

    def get_favicon():
        if not hasattr(encoded_images, "SIDE_BY_SIDE_PNG"):
            encoded_images.SIDE_BY_SIDE_PNG = (
                encoded_images.get_side_by_side_png()
            )
        return encoded_images.SIDE_BY_SIDE_PNG


class MultiBrowser:
    DRIVER_FIXING_LOCK = Files.DOWNLOADS_FOLDER + "/driver_fixing.lock"
    DRIVER_REPAIRED = Files.DOWNLOADS_FOLDER + "/driver_fixed.lock"
    CERT_FIXING_LOCK = Files.DOWNLOADS_FOLDER + "/cert_fixing.lock"
    DOWNLOAD_FILE_LOCK = Files.DOWNLOADS_FOLDER + "/downloading.lock"
    FILE_IO_LOCK = Files.DOWNLOADS_FOLDER + "/file_io.lock"
    PYAUTOGUILOCK = Files.DOWNLOADS_FOLDER + "/pyautogui.lock"


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
    SSMD = 500  # Smooth Scroll Minimum Distance (for advanced slow scroll)


class Scroll:
    Y_OFFSET = 182


class Warnings:
    SCREENSHOT_SKIPPED = "Skipping screenshot!"
    SCREENSHOT_UNDEFINED = "Unable to get screenshot!"
    PAGE_SOURCE_UNDEFINED = "Unable to get page source!"
    INVALID_RUN_COMMAND = "INVALID RUN COMMAND!"


class JQuery:
    VER = "3.7.1"
    MIN_JS = "https://cdn.jsdelivr.net/npm/jquery@%s/dist/jquery.min.js" % VER


class Messenger:
    LIB = "https://cdn.jsdelivr.net/npm/messenger-hubspot"
    VER = "1.5.0"
    THEME = "messenger-theme"
    MIN_CSS = "%s@%s/build/css/messenger.min.css" % (LIB, VER)
    MIN_JS = "%s@%s/build/js/messenger.min.js" % (LIB, VER)
    THEME_FLAT_JS = "%s@%s/build/js/%s-flat.min.js" % (LIB, VER, THEME)
    THEME_FUTURE_JS = "%s@%s/build/js/%s-future.min.js" % (LIB, VER, THEME)
    THEME_FLAT_CSS = "%s@%s/build/css/%s-flat.min.css" % (LIB, VER, THEME)
    THEME_FUTURE_CSS = "%s@%s/build/css/%s-future.min.css" % (LIB, VER, THEME)
    THEME_BLOCK_CSS = "%s@%s/build/css/%s-block.min.css" % (LIB, VER, THEME)
    THEME_AIR_CSS = "%s@%s/build/css/%s-air.min.css" % (LIB, VER, THEME)
    THEME_ICE_CSS = "%s@%s/build/css/%s-ice.min.css" % (LIB, VER, THEME)
    SPINNER_CSS = "%s@%s/build/css/messenger-spinner.min.css" % (LIB, VER)


class Underscore:
    VER = "1.13.6"
    MIN_JS = (
        "https://cdn.jsdelivr.net/npm/underscore@%s/underscore.min.js" % VER
    )


class Backbone:
    VER = "1.6.0"
    MIN_JS = "https://cdn.jsdelivr.net/npm/backbone@%s/backbone.min.js" % VER


class HtmlInspector:
    VER = "0.8.2"
    MIN_JS = (
        "https://cdnjs.cloudflare.com/ajax/libs/"
        "html-inspector/%s/html-inspector.min.js" % VER
    )


class PrettifyJS:
    RUN_PRETTIFY_JS = (
        "https://cdn.jsdelivr.net/gh/google/"
        "code-prettify@master/loader/run_prettify.js"
    )


class Reveal:
    LIB = "https://cdn.jsdelivr.net/npm/reveal.js"
    VER = "3.8.0"
    MIN_CSS = "%s@%s/css/reveal.min.css" % (LIB, VER)
    SERIF_MIN_CSS = "%s@%s/css/theme/serif.min.css" % (LIB, VER)
    WHITE_MIN_CSS = "%s@%s/css/theme/white.min.css" % (LIB, VER)
    BLACK_MIN_CSS = "%s@%s/css/theme/black.min.css" % (LIB, VER)
    SKY_MIN_CSS = "%s@%s/css/theme/sky.min.css" % (LIB, VER)
    MOON_MIN_CSS = "%s@%s/css/theme/moon.min.css" % (LIB, VER)
    NIGHT_MIN_CSS = "%s@%s/css/theme/night.min.css" % (LIB, VER)
    LEAGUE_MIN_CSS = "%s@%s/css/theme/league.min.css" % (LIB, VER)
    BEIGE_MIN_CSS = "%s@%s/css/theme/beige.min.css" % (LIB, VER)
    BLOOD_MIN_CSS = "%s@%s/css/theme/blood.min.css" % (LIB, VER)
    SIMPLE_MIN_CSS = "%s@%s/css/theme/simple.min.css" % (LIB, VER)
    SOLARIZED_MIN_CSS = "%s@%s/css/theme/solarized.min.css" % (LIB, VER)
    MIN_JS = "%s@%s/js/reveal.min.js" % (LIB, VER)


class HighCharts:
    VER = "10.3.3"
    HC_CSS = "https://code.highcharts.com/%s/css/highcharts.css" % VER
    HC_JS = "https://code.highcharts.com/%s/highcharts.js" % VER
    EXPORTING_JS = "https://code.highcharts.com/%s/modules/exporting.js" % VER
    EXPORT_DATA_JS = (
        "https://code.highcharts.com/%s/modules/export-data.js" % VER
    )
    ACCESSIBILITY_JS = (
        "https://code.highcharts.com/%s/modules/accessibility.js" % VER
    )


class BootstrapTour:
    LIB = "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tour"
    VER = "0.12.0"
    MIN_CSS = "%s/%s/css/bootstrap-tour-standalone.min.css" % (LIB, VER)
    # MIN_JS = "%s/%s/js/bootstrap-tour-standalone.min.js" % (LIB, VER)
    MIN_JS = "https://seleniumbase.github.io/cdn/js/bootstraptour.min.js"


class DriverJS:
    LIB = "https://cdn.jsdelivr.net/npm/driver.js"
    VER = "0.9.8"
    MIN_CSS = "%s@%s/dist/driver.min.css" % (LIB, VER)
    MIN_JS = "%s@%s/dist/driver.min.js" % (LIB, VER)


class Hopscotch:
    LIB = "https://cdn.jsdelivr.net/npm/hopscotch"
    VER = "0.3.1"
    MIN_CSS = "%s@%s/dist/css/hopscotch.min.css" % (LIB, VER)
    MIN_JS = "%s@%s/dist/js/hopscotch.min.js" % (LIB, VER)


class IntroJS:
    VER = "5.1.0"
    MIN_CSS = (
        "https://cdn.jsdelivr.net/npm/"
        "intro.js@%s/minified/introjs.min.css" % VER
    )
    MIN_JS = "https://cdn.jsdelivr.net/npm/intro.js@%s/intro.min.js" % VER


class TourColor:
    # Used for button colors in IntroJS Tours
    # theme_color = "#f26721"  # Orange
    # hover_color = "#db5409"  # Darker Orange
    theme_color = "#367be5"  # Blue
    hover_color = "#245ac0"  # Darker Blue


class JqueryConfirm:
    LIB = "https://cdn.jsdelivr.net/npm/jquery-confirm"
    VER = "3.3.4"
    MIN_CSS = "%s@%s/css/jquery-confirm.min.css" % (LIB, VER)
    MIN_JS = "%s@%s/js/jquery-confirm.min.js" % (LIB, VER)
    DEFAULT_THEME = "bootstrap"
    DEFAULT_COLOR = "blue"
    DEFAULT_WIDTH = "38%"


class Shepherd:
    LIB = "https://cdnjs.cloudflare.com/ajax/libs/shepherd"
    VER = "1.8.1"
    MIN_JS = "%s/%s/js/shepherd.min.js" % (LIB, VER)
    THEME_ARROWS_CSS = "%s/%s/css/shepherd-theme-arrows.css" % (LIB, VER)
    THEME_ARR_FIX_CSS = "%s/%s/css/shepherd-theme-arrows-fix.css" % (LIB, VER)
    THEME_DEFAULT_CSS = "%s/%s/css/shepherd-theme-default.css" % (LIB, VER)
    THEME_DARK_CSS = "%s/%s/css/shepherd-theme-dark.css" % (LIB, VER)
    THEME_SQ_CSS = "%s/%s/css/shepherd-theme-square.css" % (LIB, VER)
    THEME_SQ_DK_CSS = "%s/%s/css/shepherd-theme-square-dark.css" % (LIB, VER)


class Tether:
    VER = "1.4.7"
    MIN_JS = (
        "https://cdn.jsdelivr.net/npm/tether@%s/dist/js/tether.min.js" % VER
    )


class ProxyPy:
    # The version installed if proxy.py is not installed
    VER = "2.4.3"


class SeleniumWire:
    # The version installed if selenium-wire is not installed
    VER = "5.1.0"
    BLINKER_VER = "1.7.0"  # The "blinker" dependency version


class PyAutoGUI:
    # The version installed if PyAutoGUI is not installed
    VER = "0.9.54"


class Mobile:
    # Default values for mobile settings
    WIDTH = 390
    HEIGHT = 715
    RATIO = 3
    AGENT = (
        "Mozilla/5.0 (Linux; Android 13; Pixel 7 XL "
        "Build/SP2A.220505.006.A1; wv) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
        "Chrome/110.0.5028.105 Mobile Safari/537.36"
    )


class UC:
    RECONNECT_TIME = 2.4  # Seconds


class ValidBrowsers:
    valid_browsers = [
        "chrome",
        "edge",
        "firefox",
        "ie",
        "safari",
        "remote",
    ]


class ValidBinaries:
    valid_chrome_binaries_on_linux = [
        "google-chrome",
        "google-chrome-stable",
        "chrome",
        "chromium",
        "chromium-browser",
        "google-chrome-beta",
        "google-chrome-dev",
        "google-chrome-unstable",
        "brave-browser",
        "brave-browser-stable",
        "brave",
        "opera",
        "opera-stable",
        "chrome.exe",  # WSL (Windows Subsystem for Linux)
    ]
    valid_edge_binaries_on_linux = [
        "microsoft-edge",
        "microsoft-edge-stable",
        "microsoft-edge-beta",
        "microsoft-edge-dev",
        "msedge.exe",  # WSL (Windows Subsystem for Linux)
    ]
    valid_chrome_binaries_on_macos = [
        "Google Chrome",
        "Chromium",
        "Google Chrome for Testing",
        "Google Chrome Beta",
        "Google Chrome Dev",
        "Brave Browser",
        "Opera",
    ]
    valid_edge_binaries_on_macos = [
        "Microsoft Edge",
    ]
    valid_chrome_binaries_on_windows = [
        "chrome.exe",
        "chromium.exe",
        "brave.exe",
        "opera.exe",
    ]
    valid_edge_binaries_on_windows = [
        "msedge.exe",
    ]


class Browser:
    GOOGLE_CHROME = "chrome"
    EDGE = "edge"
    FIREFOX = "firefox"
    INTERNET_EXPLORER = "ie"
    SAFARI = "safari"
    REMOTE = "remote"

    VERSION = {
        "chrome": None,
        "edge": None,
        "firefox": None,
        "ie": None,
        "safari": None,
        "remote": None,
    }

    LATEST = {
        "chrome": None,
        "edge": None,
        "firefox": None,
        "ie": None,
        "safari": None,
        "remote": None,
    }


class Protocol:
    HTTP = "http"
    HTTPS = "https"


class State:
    PASSED = "Passed"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    UNTESTED = "Untested"
    ERROR = "Error"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"
