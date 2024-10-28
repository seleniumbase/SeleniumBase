import io
import logging
import os
import random
import re
import string
import sys
import time
import zipfile
from contextlib import suppress

logger = logging.getLogger(__name__)
IS_POSIX = sys.platform.startswith(("darwin", "cygwin", "linux"))


class Patcher(object):
    from seleniumbase.core import download_helper

    url_repo = "https://chromedriver.storage.googleapis.com"
    zip_name = "chromedriver_%s.zip"
    exe_name = "chromedriver%s"
    sys_plat = sys.platform
    # downloads_folder = "~/.undetected_drivers"
    if sys_plat.endswith("win32"):
        zip_name %= "win32"
        exe_name %= ".exe"
        # downloads_folder = "~/appdata/roaming/undetected_drivers"
    if sys_plat.endswith("linux"):
        zip_name %= "linux64"
        exe_name %= ""
        # downloads_folder = "~/.local/share/undetected_drivers"
    if sys_plat.endswith("darwin"):
        zip_name %= "mac64"
        exe_name %= ""
        # downloads_folder = "~/Library/Application Support/undetected_drivers"
    downloads_folder = download_helper.get_downloads_folder()
    if not os.path.exists(downloads_folder):
        try:
            os.makedirs(downloads_folder, exist_ok=True)
        except Exception:
            pass  # Only possible during multithreaded tests
    data_path = os.path.abspath(os.path.expanduser(downloads_folder))

    def __init__(self, executable_path=None, force=False, version_main=0):
        """Args:
        executable_path: None = automatic
            A full file path to the chromedriver executable
        force: False
            Terminate processes which are holding lock
        version_main: 0 = auto
            Specify main chrome version (rounded, ex: 82) """
        self.force = force
        self.executable_path = None
        prefix = "undetected"
        if not os.path.exists(self.data_path):
            with suppress(Exception):
                os.makedirs(self.data_path, exist_ok=True)
        if not executable_path:
            self.executable_path = os.path.join(
                self.data_path, "_".join([prefix, self.exe_name])
            )
        if not IS_POSIX:
            if executable_path:
                if not executable_path[-4:] == ".exe":
                    executable_path += ".exe"
        self.zip_path = os.path.join(self.data_path, prefix)
        if not executable_path:
            self.executable_path = os.path.abspath(
                os.path.join(".", self.executable_path)
            )
        self._custom_exe_path = False
        if executable_path:
            self._custom_exe_path = True
            self.executable_path = executable_path
        self.version_main = version_main
        self.version_full = None

    def auto(self, executable_path=None, force=False, version_main=None):
        if executable_path:
            self.executable_path = executable_path
            self._custom_exe_path = True
        if self._custom_exe_path:
            ispatched = self.is_binary_patched(self.executable_path)
            if not ispatched:
                return self.patch_exe()
            else:
                return
        if version_main:
            self.version_main = version_main
        if force is True:
            self.force = force
        try:
            os.unlink(self.executable_path)
        except PermissionError:
            if self.force:
                self.force_kill_instances(self.executable_path)
                not_force = not self.force
                return self.auto(force=not_force)
            try:
                if self.is_binary_patched():
                    return True  # Running AND patched
            except PermissionError:
                pass
        except FileNotFoundError:
            pass
        release = self.fetch_release_number()
        self.version_main = release.split(".")[0]
        self.version_full = release
        self.unzip_package(self.fetch_package())
        return self.patch()

    def patch(self):
        self.patch_exe()
        return self.is_binary_patched()

    def fetch_release_number(self):
        from urllib.request import urlopen

        path = "/latest_release"
        if self.version_main:
            path += "_%s" % self.version_main
        path = path.upper()
        logger.debug("Getting release number from %s" % path)
        return urlopen(self.url_repo + path).read().decode()

    def fetch_package(self):
        """Downloads chromedriver from source.
        :return: path to downloaded file """
        from urllib.request import urlretrieve

        u = "%s/%s/%s" % (
            self.url_repo, self.version_full, self.zip_name
        )
        logger.debug("Downloading from %s" % u)
        return urlretrieve(u)[0]

    def unzip_package(self, fp):
        """ :return: path to unpacked executable """
        logger.debug("Unzipping %s" % fp)
        try:
            os.unlink(self.zip_path)
        except (FileNotFoundError, OSError):
            pass
        try:
            os.makedirs(self.zip_path, mode=0o755, exist_ok=True)
        except Exception:
            pass
        with zipfile.ZipFile(fp, mode="r") as zf:
            zf.extract(self.exe_name, self.zip_path)
        try:
            os.rename(
                os.path.join(self.zip_path, self.exe_name),
                self.executable_path,
            )
            os.remove(fp)
        except PermissionError:
            pass
        try:
            os.rmdir(self.zip_path)
            os.chmod(self.executable_path, 0o755)
        except PermissionError:
            pass
        return self.executable_path

    @staticmethod
    def force_kill_instances(exe_name):
        """Terminate instances of UC.
        :param: Executable name to kill. (Can be a path)
        :return: True on success else False."""
        exe_name = os.path.basename(exe_name)
        if IS_POSIX:
            r = os.system("kill -f -9 $(pidof %s)" % exe_name)
        else:
            r = os.system("taskkill /f /im %s" % exe_name)
        return not r

    @staticmethod
    def gen_random_cdc():
        cdc = random.choices(string.ascii_lowercase, k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def is_binary_patched(self, executable_path=None):
        executable_path = executable_path or self.executable_path
        with io.open(executable_path, "rb") as fh:
            if re.search(
                b"window.cdc_adoQpoasnfa76pfcZLmcfl_"
                b"(Array|Promise|Symbol|Object|Proxy|JSON)",
                fh.read()
            ):
                return False
        return True

    def patch_exe(self):
        """Patches the ChromeDriver binary"""
        def gen_js_whitespaces(match):
            return b"\n" * len(match.group())

        def gen_call_function_js_cache_name(match):
            rep_len = len(match.group()) - 3
            ran_len = random.randint(6, rep_len)
            bb = b"'" + bytes(str().join(random.choices(
                population=string.ascii_letters, k=ran_len
            )), 'ascii') + b"';" + (b"\n" * (rep_len - ran_len))
            return bb

        with io.open(self.executable_path, "r+b") as fh:
            file_bin = fh.read()
            file_bin = re.sub(
                b"window\\.cdc_[a-zA-Z0-9]{22}_"
                b"(Array|Promise|Symbol|Object|Proxy|JSON)"
                b" = window\\.(Array|Promise|Symbol|Object|Proxy|JSON);",
                gen_js_whitespaces,
                file_bin,
            )
            file_bin = re.sub(
                b"window\\.cdc_[a-zA-Z0-9]{22}_"
                b"(Array|Promise|Symbol|Object|Proxy|JSON) \\|\\|",
                gen_js_whitespaces,
                file_bin,
            )
            file_bin = re.sub(
                b"'\\$cdc_[a-zA-Z0-9]{22}_';",
                gen_call_function_js_cache_name,
                file_bin,
            )
            fh.seek(0)
            fh.write(file_bin)
        return True

    @staticmethod
    def gen_random_cdc_beta():
        cdc = random.choices(string.ascii_letters, k=27)
        return "".join(cdc).encode()

    def is_binary_patched_beta(self, executable_path=None):
        executable_path = executable_path or self.executable_path
        try:
            with io.open(executable_path, "rb") as fh:
                return fh.read().find(b"undetected chromedriver") != -1
        except FileNotFoundError:
            return False

    def patch_exe_beta(self):
        with io.open(self.executable_path, "r+b") as fh:
            content = fh.read()
            match_injected_codeblock = re.search(
                rb"\{window\.cdc.*?;\}", content
            )
            target_bytes = None
            if match_injected_codeblock:
                target_bytes = match_injected_codeblock[0]
                new_target_bytes = (
                    b'{console.log("chromedriver is undetectable!")}'.ljust(
                        len(target_bytes), b" "
                    )
                )
            if target_bytes:
                new_content = content.replace(target_bytes, new_target_bytes)
                if new_content == content:
                    pass  # Unable to patch driver
                else:
                    fh.seek(0)
                    fh.write(new_content)

    def __repr__(self):
        return "{0:s}({1:s})".format(
            self.__class__.__name__,
            self.executable_path,
        )

    def __del__(self):
        if self._custom_exe_path:
            # If the driver binary is specified by the user,
            # then assume it is important enough to keep it.
            return
        else:
            timeout = 3
            t = time.monotonic()
            while True:
                now = time.monotonic()
                if now - t > timeout:
                    logger.debug(
                        "Could not unlink %s in time (%d seconds)"
                        % (self.executable_path, timeout)
                    )
                    break
                try:
                    os.unlink(self.executable_path)
                    logger.debug(
                        "Successfully unlinked %s"
                        % self.executable_path
                    )
                    break
                except (OSError, RuntimeError, PermissionError):
                    time.sleep(0.1)
                    continue
                except FileNotFoundError:
                    break
