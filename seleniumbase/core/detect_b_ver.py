"""
Detect the browser version before launching tests.
Eg. detect_b_ver.get_browser_version_from_os("google-chrome")
"""
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


PATTERN = {
    ChromeType.GOOGLE: r"\d+\.\d+\.\d+",
}


def os_name():
    pl = sys.platform
    if pl == "linux" or pl == "linux2":
        return OSType.LINUX
    elif pl == "darwin":
        return OSType.MAC
    elif pl == "win32":
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


def windows_browser_apps_to_cmd(*apps):
    """Create analogue of browser --version command for windows."""
    powershell = determine_powershell()
    first_hit_template = "$tmp = {expression}; if ($tmp) {{echo $tmp; Exit;}};"
    script = "$ErrorActionPreference='silentlycontinue'; " + " ".join(
        first_hit_template.format(expression=e) for e in apps
    )
    return '%s -NoProfile "%s"' % (powershell, script)


def get_browser_version_from_os(browser_type=None):
    """Return installed browser version."""
    cmd_mapping = {
        ChromeType.GOOGLE: {
            OSType.LINUX: linux_browser_apps_to_cmd(
                "google-chrome",
                "google-chrome-stable",
                "google-chrome-beta",
                "google-chrome-dev",
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
    }
    try:
        cmd_mapping = cmd_mapping[browser_type][os_name()]
        pattern = PATTERN[browser_type]
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
