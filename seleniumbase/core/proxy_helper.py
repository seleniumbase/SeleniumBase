import os
import re
import warnings
import zipfile
from seleniumbase.config import proxy_list
from seleniumbase.config import settings
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import page_utils

DOWNLOADS_DIR = constants.Files.DOWNLOADS_FOLDER
PROXY_ZIP_PATH = os.path.join(DOWNLOADS_DIR, "proxy.zip")
PROXY_ZIP_LOCK = os.path.join(DOWNLOADS_DIR, "proxy.lock")
PROXY_DIR_PATH = os.path.join(DOWNLOADS_DIR, "proxy_ext_dir")
PROXY_DIR_LOCK = os.path.join(DOWNLOADS_DIR, "proxy_dir.lock")


def create_proxy_ext(
    proxy_string, proxy_user, proxy_pass, bypass_list=None, zip_it=True
):
    """Implementation of https://stackoverflow.com/a/35293284 for
    https://stackoverflow.com/questions/12848327/
    (Run Selenium on a proxy server that requires authentication.)
    Solution involves creating & adding a Chromium extension at runtime.
    CHROMIUM-ONLY! *** Only Chrome and Edge browsers are supported. ***
    """
    background_js = None
    if not bypass_list:
        bypass_list = ""
    if proxy_string:
        proxy_protocol = ""
        if proxy_string.count("://") == 1:
            proxy_protocol = proxy_string.split("://")[0] + "://"
            proxy_string = proxy_string.split("://")[1]
        proxy_host = proxy_protocol + proxy_string.split(":")[0]
        proxy_port = proxy_string.split(":")[1]
        background_js = (
            """var config = {\n"""
            """    mode: "fixed_servers",\n"""
            """    rules: {\n"""
            """      singleProxy: {\n"""
            """        scheme: "http",\n"""
            """        host: "%s",\n"""
            """        port: parseInt("%s")\n"""
            """      },\n"""
            """    bypassList: ["%s"]\n"""
            """    }\n"""
            """  };\n"""
            """chrome.proxy.settings.set("""
            """{value: config, scope: "regular"}, function() {"""
            """});\n"""
            """function callbackFn(details) {\n"""
            """    return {\n"""
            """        authCredentials: {\n"""
            """            username: "%s",\n"""
            """            password: "%s"\n"""
            """        }\n"""
            """    };\n"""
            """}\n"""
            """chrome.webRequest.onAuthRequired.addListener(\n"""
            """        callbackFn,\n"""
            """        {urls: ["<all_urls>"]},\n"""
            """        ['blocking']\n"""
            """);""" % (
                proxy_host, proxy_port, bypass_list, proxy_user, proxy_pass
            )
        )
    else:
        background_js = (
            """var config = {\n"""
            """    mode: "fixed_servers",\n"""
            """    rules: {\n"""
            """    },\n"""
            """    bypassList: ["%s"]\n"""
            """  };\n"""
            """chrome.proxy.settings.set("""
            """{value: config, scope: "regular"}, function() {"""
            """});\n"""
            """function callbackFn(details) {\n"""
            """    return {\n"""
            """        authCredentials: {\n"""
            """            username: "%s",\n"""
            """            password: "%s"\n"""
            """        }\n"""
            """    };\n"""
            """}\n"""
            """chrome.webRequest.onAuthRequired.addListener(\n"""
            """        callbackFn,\n"""
            """        {urls: ["<all_urls>"]},\n"""
            """        ['blocking']\n"""
            """);""" % (bypass_list, proxy_user, proxy_pass)
        )
    manifest_json = (
        """{\n"""
        """"version": "1.0.0",\n"""
        """"manifest_version": 2,\n"""
        """"name": "Chrome Proxy",\n"""
        """"permissions": [\n"""
        """    "proxy",\n"""
        """    "tabs",\n"""
        """    "unlimitedStorage",\n"""
        """    "storage",\n"""
        """    "<all_urls>",\n"""
        """    "webRequest",\n"""
        """    "webRequestBlocking"\n"""
        """],\n"""
        """"background": {\n"""
        """    "scripts": ["background.js"]\n"""
        """},\n"""
        """"minimum_chrome_version":"22.0.0"\n"""
        """}"""
    )
    import threading

    lock = threading.RLock()  # Support multi-threaded tests. Eg. "pytest -n=4"
    with lock:
        abs_path = os.path.abspath(".")
        downloads_path = os.path.join(abs_path, DOWNLOADS_DIR)
        if not os.path.exists(downloads_path):
            os.mkdir(downloads_path)
        if zip_it:
            zf = zipfile.ZipFile(PROXY_ZIP_PATH, mode="w")
            zf.writestr("background.js", background_js)
            zf.writestr("manifest.json", manifest_json)
            zf.close()
        else:
            proxy_ext_dir = PROXY_DIR_PATH
            if not os.path.exists(proxy_ext_dir):
                os.mkdir(proxy_ext_dir)
            manifest_file = os.path.join(proxy_ext_dir, "manifest.json")
            with open(manifest_file, mode="w") as f:
                f.write(manifest_json)
            proxy_host = proxy_string.split(":")[0]
            proxy_port = proxy_string.split(":")[1]
            background_file = os.path.join(proxy_ext_dir, "background.js")
            with open(background_file, mode="w") as f:
                f.write(background_js)


def remove_proxy_zip_if_present():
    """Remove Chromium extension zip file used for proxy server authentication.
    Used in the implementation of https://stackoverflow.com/a/35293284
    for https://stackoverflow.com/questions/12848327/
    """
    try:
        if os.path.exists(PROXY_ZIP_PATH):
            os.remove(PROXY_ZIP_PATH)
        if os.path.exists(PROXY_ZIP_LOCK):
            os.remove(PROXY_ZIP_LOCK)
    except Exception:
        pass


def validate_proxy_string(proxy_string):
    if proxy_string in proxy_list.PROXY_LIST.keys():
        proxy_string = proxy_list.PROXY_LIST[proxy_string]
        if not proxy_string:
            return None
    valid = False
    val_ip = re.match(
        r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$", proxy_string
    )
    if not val_ip:
        if proxy_string.startswith("http://"):
            proxy_string = proxy_string.split("http://")[1]
        elif proxy_string.startswith("https://"):
            proxy_string = proxy_string.split("https://")[1]
        elif "://" in proxy_string:
            if not proxy_string.startswith("socks4://") and not (
                proxy_string.startswith("socks5://")
            ):
                proxy_string = proxy_string.split("://")[1]
        chunks = proxy_string.split(":")
        if len(chunks) == 2:
            if re.match(r"^\d+$", chunks[1]):
                if page_utils.is_valid_url("http://" + proxy_string):
                    valid = True
        elif len(chunks) == 3:
            if re.match(r"^\d+$", chunks[2]):
                if page_utils.is_valid_url("http:" + ":".join(chunks[1:])):
                    if chunks[0] == "http":
                        valid = True
                    elif chunks[0] == "https":
                        valid = True
                    elif chunks[0] == "socks4":
                        valid = True
                    elif chunks[0] == "socks5":
                        valid = True
    else:
        proxy_string = val_ip.group()
        valid = True
    if not valid:
        __display_proxy_warning(proxy_string)
        proxy_string = None
    return proxy_string


def __display_proxy_warning(proxy_string):
    message = (
        '\nWARNING: Proxy String ["%s"] is NOT in the expected '
        '"ip_address:port" or "server:port" format, '
        "(OR the key does not exist in "
        "seleniumbase.config.proxy_list.PROXY_LIST)." % proxy_string
    )
    if settings.RAISE_INVALID_PROXY_STRING_EXCEPTION:
        raise Exception(message)
    else:
        message += " *** DEFAULTING to NOT USING a Proxy Server! ***"
        warnings.simplefilter("always", Warning)  # See Warnings
        warnings.warn(message, category=Warning, stacklevel=2)
        warnings.simplefilter("default", Warning)  # Set Default
