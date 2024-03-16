"""Detect the browser version before launching tests.
Eg. detect_b_ver.get_browser_version_from_os("google-chrome")"""
import datetime
import os
import platform
import re
import subprocess
import sys


class File(object):
    def __init__(self, stream):
        self.content = stream.content
        self.__stream = stream
        self.__temp_name = "driver"

    @property
    def filename(self):
        try:
            filename = re.findall(
                "filename=(.+)", self.__stream.headers["content-disposition"]
            )[0]
        except KeyError:
            filename = "%s.zip" % self.__temp_name
        except IndexError:
            filename = "%s.exe" % self.__temp_name

        if '"' in filename:
            filename = filename.replace('"', "")

        return filename


class OSType(object):
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


class ChromeType(object):
    GOOGLE = "google-chrome"
    MSEDGE = "edge"


PATTERN = {
    ChromeType.GOOGLE: r"\d+\.\d+\.\d+",
    ChromeType.MSEDGE: r"\d+\.\d+\.\d+",
}


def os_name():
    if "linux" in sys.platform:
        return OSType.LINUX
    elif "darwin" in sys.platform:
        return OSType.MAC
    elif "win32" in sys.platform:
        return OSType.WIN
    else:
        raise Exception("Could not determine the OS type!")


def os_architecture():
    if platform.machine().endswith("64"):
        return 64
    else:
        return 32


def os_type():
    return "%s%s" % (os_name(), os_architecture())


def is_arch(os_sys_type):
    if '_m1' in os_sys_type:
        return True
    return platform.processor() != 'i386'


def is_mac_os(os_sys_type):
    return OSType.MAC in os_sys_type


def get_date_diff(date1, date2, date_format):
    a = datetime.datetime.strptime(date1, date_format)
    b = datetime.datetime.strptime(
        str(date2.strftime(date_format)), date_format)
    return (b - a).days


def linux_browser_apps_to_cmd(*apps):
    """Create 'browser --version' command from browser app names."""
    ignore_errors_cmd_part = " 2>/dev/null" if os.getenv(
        "WDM_LOG_LEVEL") == "0" else ""
    return " || ".join(
        "%s --version%s" % (i, ignore_errors_cmd_part) for i in apps
    )


def chrome_on_linux_path(prefer_chromium=False):
    if os_name() != OSType.LINUX:
        return ""
    if prefer_chromium:
        paths = ["/bin/chromium", "/bin/chromium-browser"]
        for path in paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
    paths = ["/bin/google-chrome", "/bin/google-chrome-stable"]
    for path in paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    paths = os.environ["PATH"].split(os.pathsep)
    binaries = []
    binaries.append("google-chrome")
    binaries.append("google-chrome-stable")
    binaries.append("chrome")
    binaries.append("chromium")
    binaries.append("chromium-browser")
    binaries.append("google-chrome-beta")
    binaries.append("google-chrome-dev")
    binaries.append("google-chrome-unstable")
    for binary in binaries:
        for path in paths:
            full_path = os.path.join(path, binary)
            if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                return full_path
    return "/usr/bin/google-chrome"


def edge_on_linux_path():
    if os_name() != OSType.LINUX:
        return ""
    paths = os.environ["PATH"].split(os.pathsep)
    binaries = []
    binaries.append("microsoft-edge")
    binaries.append("microsoft-edge-stable")
    binaries.append("microsoft-edge-beta")
    binaries.append("microsoft-edge-dev")
    for binary in binaries:
        for path in paths:
            full_path = os.path.join(path, binary)
            if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                return full_path
    return "/usr/bin/microsoft-edge"


def chrome_on_windows_path():
    if os_name() != OSType.WIN:
        return ""
    candidates = []
    for item in map(
        os.environ.get,
        (
            "PROGRAMFILES",
            "PROGRAMFILES(X86)",
            "LOCALAPPDATA",
            "PROGRAMW6432",
        ),
    ):
        for subitem in (
            "Google/Chrome/Application",
            "Google/Chrome Beta/Application",
            "Google/Chrome Canary/Application",
        ):
            try:
                candidates.append(os.sep.join((item, subitem, "chrome.exe")))
            except TypeError:
                pass
    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return os.path.normpath(candidate)
    return ""


def edge_on_windows_path():
    if os_name() != OSType.WIN:
        return ""
    candidates = []
    for item in map(
        os.environ.get,
        (
            "PROGRAMFILES",
            "PROGRAMFILES(X86)",
            "LOCALAPPDATA",
            "PROGRAMW6432",
        ),
    ):
        for subitem in (
            "Microsoft/Edge/Application",
            "Microsoft/Edge Beta/Application",
            "Microsoft/Edge Canary/Application",
        ):
            try:
                candidates.append(os.sep.join((item, subitem, "msedge.exe")))
            except TypeError:
                pass
    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return os.path.normpath(candidate)
    return ""


def windows_browser_apps_to_cmd(*apps):
    """Create analogue of browser --version command for windows."""
    powershell = determine_powershell()
    first_hit_template = "$tmp = {expression}; if ($tmp) {{echo $tmp; Exit;}};"
    script = "$ErrorActionPreference='silentlycontinue'; " + " ".join(
        first_hit_template.format(expression=e) for e in apps
    )
    return '%s -NoProfile "%s"' % (powershell, script)


def get_binary_location(browser_type, prefer_chromium=False):
    """Return the full path of the browser binary.
    If going for better results in UC Mode, use: prefer_chromium=True"""
    cmd_mapping = {
        ChromeType.GOOGLE: {
            OSType.LINUX: chrome_on_linux_path(prefer_chromium),
            OSType.MAC: r"/Applications/Google Chrome.app"
                        r"/Contents/MacOS/Google Chrome",
            OSType.WIN: chrome_on_windows_path(),
        },
        ChromeType.MSEDGE: {
            OSType.LINUX: edge_on_linux_path(),
            OSType.MAC: r"/Applications/Microsoft Edge.app"
                        r"/Contents/MacOS/Microsoft Edge",
            OSType.WIN: edge_on_windows_path(),
        },
    }
    return cmd_mapping[browser_type][os_name()]


def get_browser_version_from_binary(binary_location):
    try:
        if not os.path.exists(binary_location):
            return None
        path = binary_location
        pattern = r"\d+\.\d+\.\d+"
        quad_pattern = r"\d+\.\d+\.\d+\.\d+"
        if os_name() == OSType.WIN:
            path = path.replace(r"\ ", r" ").replace("\\", "\\\\")
            cmd_mapping = (
                '''powershell -command "&{(Get-Item -Path '%s')'''
                '''.VersionInfo.FileVersion}"''' % path
            )
            quad_version = read_version_from_cmd(cmd_mapping, quad_pattern)
            if quad_version and len(str(quad_version)) >= 9:  # Eg. 122.0.0.0
                return quad_version
            return read_version_from_cmd(cmd_mapping, pattern)
        if binary_location.count(r"\ ") != binary_location.count(" "):
            binary_location = binary_location.replace(" ", r"\ ")
        cmd_mapping = binary_location + " --version"
        quad_version = read_version_from_cmd(cmd_mapping, quad_pattern)
        if quad_version and len(str(quad_version)) >= 9:
            return quad_version
        return read_version_from_cmd(cmd_mapping, pattern)
    except Exception:
        return None


def get_browser_version_from_os(browser_type):
    """Return installed browser version."""
    cmd_mapping = {
        ChromeType.GOOGLE: {
            OSType.LINUX: linux_browser_apps_to_cmd(
                "google-chrome",
                "google-chrome-stable",
                "chrome",
                "chromium",
                "chromium-browser",
                "google-chrome-beta",
                "google-chrome-dev",
                "google-chrome-unstable",
            ),
            OSType.MAC: r"/Applications/Google\ Chrome.app"
                        r"/Contents/MacOS/Google\ Chrome --version",
            OSType.WIN: windows_browser_apps_to_cmd(
                r'(Get-Item -Path "$env:PROGRAMFILES\Google\Chrome'
                r'\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Google\Chrome'
                r'\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:LOCALAPPDATA\Google\Chrome'
                r'\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE'
                r'\Google\Chrome\BLBeacon").version',
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE'
                r'\Wow6432Node\Microsoft\Windows'
                r'\CurrentVersion\Uninstall\Google Chrome").version',
            ),
        },
        ChromeType.MSEDGE: {
            OSType.LINUX: linux_browser_apps_to_cmd(
                "microsoft-edge",
                "microsoft-edge-stable",
                "microsoft-edge-beta",
                "microsoft-edge-dev",
            ),
            OSType.MAC: r"/Applications/Microsoft\ Edge.app"
                        r"/Contents/MacOS/Microsoft\ Edge --version",
            OSType.WIN: windows_browser_apps_to_cmd(
                # stable edge
                r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft'
                r'\Edge\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE'
                r'\Microsoft\Edge\BLBeacon").version',
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE'
                r'\Microsoft\EdgeUpdate\Clients'
                r'\{56EB18F8-8008-4CBD-B6D2-8C97FE7E9062}").pv',
                # beta edge
                r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge Beta'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge Beta'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge Beta'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft'
                r'\Edge Beta\BLBeacon").version',
                # dev edge
                r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge Dev'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge Dev'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge Dev'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft'
                r'\Edge Dev\BLBeacon").version',
                # canary edge
                r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge SxS'
                r'\Application\msedge.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE'
                r'\Microsoft\Edge SxS\BLBeacon").version',
                # highest edge
                r"(Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft"
                r"\Windows\CurrentVersion\App Paths\msedge.exe')."
                r"'(Default)').VersionInfo.ProductVersion",
                r"[System.Diagnostics.FileVersionInfo]::GetVersionInfo(("
                r"Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows"
                r"\CurrentVersion\App Paths\msedge.exe')."
                r"'(Default)').ProductVersion",
                r"Get-AppxPackage -Name *MicrosoftEdge.* | Foreach Version",
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node'
                r'\Microsoft\Windows\CurrentVersion\Uninstall'
                r'\Microsoft Edge").version',
            ),
        },
    }
    try:
        cmd_mapping = cmd_mapping[browser_type][os_name()]
        pattern = PATTERN[browser_type]
        quad_pattern = r"\d+\.\d+\.\d+\.\d+"
        quad_version = read_version_from_cmd(cmd_mapping, quad_pattern)
        if quad_version and len(str(quad_version)) >= 9:  # Eg. 115.0.0.0
            return quad_version
        version = read_version_from_cmd(cmd_mapping, pattern)
        return version
    except Exception:
        raise Exception(
            "Can not find browser %s installed in your system!" % browser_type
        )


def format_version(browser_type, version):
    if not version or version == 'latest':
        return 'latest'
    try:
        pattern = PATTERN[browser_type]
        result = re.search(pattern, version)
        return result.group(0) if result else version
    except Exception:
        return "latest"


def get_browser_version(browser_type, metadata):
    pattern = PATTERN[browser_type]
    version_from_os = metadata['version']
    result = re.search(pattern, version_from_os)
    version = result.group(0) if version_from_os else None
    return version


def read_version_from_cmd(cmd, pattern):
    with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True,
    ) as stream:
        stdout = stream.communicate()[0].decode()
        version = re.search(pattern, stdout)
        version = version.group(0) if version else None
    return version


def determine_powershell():
    """Returns "True" if runs in Powershell and "False" if another console."""
    cmd = "(dir 2>&1 *`|echo CMD);&<# rem #>echo powershell"
    with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True,
    ) as stream:
        stdout = stream.communicate()[0].decode()
    return "" if stdout == "powershell" else "powershell"
