import logging
import os
import pathlib
import secrets
import sys
import tempfile
import zipfile
from seleniumbase.config import settings
from typing import Union, List, Optional

__all__ = [
    "Config",
    "find_chrome_executable",
    "temp_profile_dir",
    "is_root",
    "is_posix",
    "PathLike",
]

logger = logging.getLogger(__name__)
is_posix = sys.platform.startswith(("darwin", "cygwin", "linux", "linux2"))

PathLike = Union[str, pathlib.Path]
AUTO = None


class Config:
    """Config object"""

    def __init__(
        self,
        user_data_dir: Optional[PathLike] = AUTO,
        headless: Optional[bool] = False,
        incognito: Optional[bool] = False,
        guest: Optional[bool] = False,
        browser_executable_path: Optional[PathLike] = AUTO,
        browser_args: Optional[List[str]] = AUTO,
        sandbox: Optional[bool] = True,
        lang: Optional[str] = "en-US",
        host: str = AUTO,
        port: int = AUTO,
        expert: bool = AUTO,
        **kwargs: dict,
    ):
        """
        Creates a config object.
        Can be called without any arguments to generate a best-practice config,
        which is recommended.
        Calling the object, eg: myconfig(), returns the list of arguments which
        are provided to the browser.
        Additional args can be added using the :py:obj:`~add_argument method`.
        Instances of this class are usually not instantiated by end users.
        :param user_data_dir: the data directory to use
        :param headless: set to True for headless mode
        :param browser_executable_path:
         Specify browser executable, instead of using autodetect.
        :param browser_args: Forwarded to browser executable.
         Eg: ["--some-chromeparam=somevalue", "some-other-param=someval"]
        :param sandbox: disables sandbox
        :param autodiscover_targets: use autodiscovery of targets
        :param lang:
         Language string to use other than the default "en-US,en;q=0.9"
        :param expert: When set to True, "expert" mode is enabled.
         This adds: --disable-web-security --disable-site-isolation-trials,
         as well as some scripts and patching useful for debugging.
         (For example, ensuring shadow-root is always in "open" mode.)
        :param kwargs:
        :type user_data_dir: PathLike
        :type headless: bool
        :type browser_executable_path: PathLike
        :type browser_args: list[str]
        :type sandbox: bool
        :type lang: str
        :type kwargs: dict
        """
        if not browser_args:
            browser_args = []
        if not user_data_dir:
            self._user_data_dir = temp_profile_dir()
            self._custom_data_dir = False
        else:
            self.user_data_dir = user_data_dir
        if not browser_executable_path:
            browser_executable_path = find_chrome_executable()
        self._browser_args = browser_args
        self.browser_executable_path = browser_executable_path
        self.headless = headless
        self.incognito = incognito
        self.guest = guest
        self.sandbox = sandbox
        self.host = host
        self.port = port
        self.expert = expert
        self._extensions = []
        # When using posix-ish operating system and running as root,
        # you must use no_sandbox=True
        if is_posix and is_root() and sandbox:
            logger.info("Detected root usage, auto-disabling sandbox mode.")
            self.sandbox = False
        self.autodiscover_targets = True
        self.lang = lang
        # Other keyword args will be accessible by attribute
        self.__dict__.update(kwargs)
        super().__init__()
        start_width = settings.CHROME_START_WIDTH
        start_height = settings.CHROME_START_HEIGHT
        start_x = settings.WINDOW_START_X
        start_y = settings.WINDOW_START_Y
        self._default_browser_args = [
            "--window-size=%s,%s" % (start_width, start_height),
            "--window-position=%s,%s" % (start_x, start_y),
            "--remote-allow-origins=*",
            "--no-first-run",
            "--no-service-autorun",
            "--disable-auto-reload",
            "--no-default-browser-check",
            "--homepage=about:blank",
            "--no-pings",
            "--wm-window-animations-disabled",
            "--animation-duration-scale=0",
            "--enable-privacy-sandbox-ads-apis",
            "--safebrowsing-disable-download-protection",
            '--simulate-outdated-no-au="Tue, 31 Dec 2099 23:59:59 GMT"',
            "--password-store=basic",
            "--deny-permission-prompts",
            "--disable-infobars",
            "--disable-breakpad",
            "--disable-component-update",
            "--disable-prompt-on-repost",
            "--disable-password-generation",
            "--disable-ipc-flooding-protection",
            "--disable-background-timer-throttling",
            "--disable-search-engine-choice-screen",
            "--disable-backgrounding-occluded-windows",
            "--disable-client-side-phishing-detection",
            "--disable-top-sites",
            "--disable-translate",
            "--disable-renderer-backgrounding",
            "--disable-background-networking",
            "--disable-dev-shm-usage",
            "--disable-features=IsolateOrigins,site-per-process,Translate,"
            "InsecureDownloadWarnings,DownloadBubble,DownloadBubbleV2,"
            "OptimizationTargetPrediction,OptimizationGuideModelDownloading,"
            "SidePanelPinning,UserAgentClientHint,PrivacySandboxSettings4",
        ]

    @property
    def browser_args(self):
        return sorted(self._default_browser_args + self._browser_args)

    @property
    def user_data_dir(self):
        return self._user_data_dir

    @user_data_dir.setter
    def user_data_dir(self, path: PathLike):
        self._user_data_dir = str(path)
        self._custom_data_dir = True

    @property
    def uses_custom_data_dir(self) -> bool:
        return self._custom_data_dir

    def add_extension(self, extension_path: PathLike):
        """
        Adds an extension to load. You can set the extension_path to a
        folder (containing the manifest), or an extension zip file (.crx)
        :param extension_path:
        """
        path = pathlib.Path(extension_path)
        if not path.exists():
            raise FileNotFoundError(
                "Could not find anything here: %s" % str(path)
            )
        if path.is_file():
            tf = tempfile.mkdtemp(
                prefix="extension_", suffix=secrets.token_hex(4)
            )
            with zipfile.ZipFile(path, "r") as z:
                z.extractall(tf)
                self._extensions.append(tf)
        elif path.is_dir():
            for item in path.rglob("manifest.*"):
                path = item.parent
            self._extensions.append(path)

    def __call__(self):
        # The host and port will be added when starting the browser.
        # By the time it starts, the port is probably already taken.
        args = self._default_browser_args.copy()
        args += ["--user-data-dir=%s" % self.user_data_dir]
        args += ["--disable-features=IsolateOrigins,site-per-process"]
        args += ["--disable-session-crashed-bubble"]
        if self.expert:
            args += [
                "--disable-web-security",
                "--disable-site-isolation-trials",
            ]
        if self._browser_args:
            args.extend([arg for arg in self._browser_args if arg not in args])
        if self.headless:
            args.append("--headless=new")
        if self.incognito:
            args.append("--incognito")
        if self.guest:
            args.append("--guest")
        if not self.sandbox:
            args.append("--no-sandbox")
        if self.host:
            args.append("--remote-debugging-host=%s" % self.host)
        if self.port:
            args.append("--remote-debugging-port=%s" % self.port)
        return args

    def add_argument(self, arg: str):
        if any(
            x in arg.lower()
            for x in [
                "headless",
                "data-dir",
                "data_dir",
                "no-sandbox",
                "no_sandbox",
                "lang",
            ]
        ):
            raise ValueError(
                '"%s" is not allowed. Please use one of the '
                'attributes of the Config object to set it.'
                % arg
            )
        self._browser_args.append(arg)

    def __repr__(self):
        s = f"{self.__class__.__name__}"
        for k, v in ({**self.__dict__, **self.__class__.__dict__}).items():
            if k[0] == "_":
                continue
            if not v:
                continue
            if isinstance(v, property):
                v = getattr(self, k)
            if callable(v):
                continue
            s += f"\n\t{k} = {v}"
        return s


def is_root():
    """
    Helper function to determine if the user is trying to launch chrome
    under linux as root, which needs some alternative handling.
    """
    import ctypes
    import os

    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def temp_profile_dir():
    """Generate a temp dir (path)"""
    path = os.path.normpath(tempfile.mkdtemp(prefix="uc_"))
    return path


def find_chrome_executable(return_all=False):
    """
    Finds the chrome, beta, canary, chromium executable
    and returns the disk path.
    """
    candidates = []
    if is_posix:
        for item in os.environ.get("PATH").split(os.pathsep):
            for subitem in (
                "google-chrome",
                "chromium",
                "chromium-browser",
                "chrome",
                "google-chrome-stable",
            ):
                candidates.append(os.sep.join((item, subitem)))
        if "darwin" in sys.platform:
            candidates += [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
    else:
        for item in map(
            os.environ.get,
            (
                "PROGRAMFILES",
                "PROGRAMFILES(X86)",
                "LOCALAPPDATA",
                "PROGRAMW6432",
            ),
        ):
            if item is not None:
                for subitem in (
                    "Google/Chrome/Application",
                    "Google/Chrome Beta/Application",
                    "Google/Chrome Canary/Application",
                ):
                    candidates.append(
                        os.sep.join((item, subitem, "chrome.exe"))
                    )
    rv = []
    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            logger.debug("%s is a valid candidate... " % candidate)
            rv.append(candidate)
        else:
            logger.debug(
                "%s is not a valid candidate because it doesn't exist "
                "or isn't an executable."
                % candidate
            )
    winner = None
    if return_all and rv:
        return rv
    if rv and len(rv) > 1:
        # Assuming the shortest path wins
        winner = min(rv, key=lambda x: len(x))
    elif len(rv) == 1:
        winner = rv[0]
    if winner:
        return os.path.normpath(winner)
    raise FileNotFoundError(
        "Could not find a valid chrome browser binary. "
        "Please make sure Chrome is installed. "
        "Or use the keyword argument: "
        "'browser_executable_path=/path/to/your/browser'."
    )
