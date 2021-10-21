import os
import zipfile
from seleniumbase.fixtures import constants

DOWNLOADS_DIR = constants.Files.DOWNLOADS_FOLDER
PROXY_ZIP_PATH = "%s/%s" % (DOWNLOADS_DIR, "proxy.zip")
PROXY_ZIP_LOCK = "%s/%s" % (DOWNLOADS_DIR, "proxy.lock")


def create_proxy_zip(proxy_string, proxy_user, proxy_pass):
    """Implementation of https://stackoverflow.com/a/35293284 for
    https://stackoverflow.com/questions/12848327/
    (Run Selenium on a proxy server that requires authentication.)
    Solution involves creating & adding a Chrome extension on the fly.
    * CHROME-ONLY for now! *
    """
    proxy_host = proxy_string.split(":")[0]
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
        """);""" % (proxy_host, proxy_port, proxy_user, proxy_pass)
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

    lock = threading.RLock()  # Support multi-threaded test runs with Pytest
    with lock:
        abs_path = os.path.abspath(".")
        downloads_path = os.path.join(abs_path, DOWNLOADS_DIR)
        if not os.path.exists(downloads_path):
            os.mkdir(downloads_path)
        zf = zipfile.ZipFile(PROXY_ZIP_PATH, mode="w")
        zf.writestr("background.js", background_js)
        zf.writestr("manifest.json", manifest_json)
        zf.close()


def remove_proxy_zip_if_present():
    """Remove Chrome extension zip file used for proxy server authentication.
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
