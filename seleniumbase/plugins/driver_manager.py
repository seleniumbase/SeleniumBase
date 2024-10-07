"""
The SeleniumBase Driver as a Python Context Manager or a returnable object.
###########################################################################

The SeleniumBase Driver as a context manager:
Usage --> ``with DriverContext() as driver:``

Example -->

```python
from seleniumbase import DriverContext

with DriverContext() as driver:
    driver.get("https://google.com/ncr")
```

# (The browser exits automatically after the "with" block ends.)

###########################################################################
# Above: The driver as a context manager. (Used with a "with" statement.) #
# ----------------------------------------------------------------------- #
# Below: The driver as a returnable object. (Used with "return" command.) #
###########################################################################

The SeleniumBase Driver as a returnable object:
Usage --> ``driver = Driver()``

Example -->

```python
from seleniumbase import Driver

driver = Driver()
driver.get("https://google.com/ncr")
```

###########################################################################
"""
import os
import sys


class DriverContext():
    def __init__(self, *args, **kwargs):
        self.driver = Driver(*args, **kwargs)

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if (
                hasattr(self, "driver")
                and hasattr(self.driver, "quit")
                and (
                    "win32" not in sys.platform
                    or self.driver.service.process
                )
            ):
                self.driver.quit()
        except Exception:
            pass
        return False


def Driver(
    browser=None,  # Choose from "chrome", "edge", "firefox", or "safari".
    headless=None,  # Use the default headless mode for Chromium and Firefox.
    headless1=None,  # Use Chromium's old headless mode. (Fast, but limited)
    headless2=None,  # Use Chromium's new headless mode. (Has more features)
    headed=None,  # Run tests in headed/GUI mode on Linux, where not default.
    locale_code=None,  # Set the Language Locale Code for the web browser.
    protocol=None,  # The Selenium Grid protocol: "http" or "https".
    servername=None,  # The Selenium Grid server/IP used for tests.
    port=None,  # The Selenium Grid port used by the test server.
    proxy=None,  # Use proxy. Format: "SERVER:PORT" or "USER:PASS@SERVER:PORT".
    proxy_bypass_list=None,  # Skip proxy when using the listed domains.
    proxy_pac_url=None,  # Use PAC file. (Format: URL or USERNAME:PASSWORD@URL)
    multi_proxy=None,  # Allow multiple proxies with auth when multi-threaded.
    agent=None,  # Modify the web browser's User-Agent string.
    cap_file=None,  # The desired capabilities to use with a Selenium Grid.
    cap_string=None,  # The desired capabilities to use with a Selenium Grid.
    recorder_ext=None,  # Enables the SeleniumBase Recorder Chromium extension.
    disable_cookies=None,  # Disable Cookies on websites. (Pages might break!)
    disable_js=None,  # Disable JavaScript on websites. (Pages might break!)
    disable_csp=None,  # Disable the Content Security Policy of websites.
    enable_ws=None,  # Enable Web Security on Chromium-based browsers.
    disable_ws=None,  # Reverse of "enable_ws". (None and False are different)
    enable_sync=None,  # Enable "Chrome Sync" on websites.
    use_auto_ext=None,  # Use Chrome's automation extension.
    undetectable=None,  # Use undetected-chromedriver to evade bot-detection.
    uc_cdp_events=None,  # Capture CDP events in undetected-chromedriver mode.
    uc_subprocess=None,  # Use undetected-chromedriver as a subprocess.
    log_cdp_events=None,  # Capture {"performance": "ALL", "browser": "ALL"}
    no_sandbox=None,  # (DEPRECATED) - "--no-sandbox" is always used now.
    disable_gpu=None,  # (DEPRECATED) - GPU is disabled if not "swiftshader".
    incognito=None,  # Enable Chromium's Incognito mode.
    guest_mode=None,  # Enable Chromium's Guest mode.
    dark_mode=None,  # Enable Chromium's Dark mode.
    devtools=None,  # Open Chromium's DevTools when the browser opens.
    remote_debug=None,  # Enable Chrome's Debugger on "http://localhost:9222".
    enable_3d_apis=None,  # Enable WebGL and 3D APIs.
    swiftshader=None,  # Chrome: --use-gl=angle / --use-angle=swiftshader-webgl
    ad_block_on=None,  # Block some types of display ads from loading.
    host_resolver_rules=None,  # Set host-resolver-rules, comma-separated.
    block_images=None,  # Block images from loading during tests.
    do_not_track=None,  # Tell websites that you don't want to be tracked.
    chromium_arg=None,  # "ARG=N,ARG2" (Set Chromium args, ","-separated.)
    firefox_arg=None,  # "ARG=N,ARG2" (Set Firefox args, comma-separated.)
    firefox_pref=None,  # SET (Set Firefox PREFERENCE:VALUE set, ","-separated)
    user_data_dir=None,  # Set the Chrome user data directory to use.
    extension_zip=None,  # Load a Chrome Extension .zip|.crx, comma-separated.
    extension_dir=None,  # Load a Chrome Extension directory, comma-separated.
    disable_features=None,  # "F1,F2" (Disable Chrome features, ","-separated.)
    binary_location=None,  # Set path of the Chromium browser binary to use.
    driver_version=None,  # Set the chromedriver or uc_driver version to use.
    page_load_strategy=None,  # Set Chrome PLS to "normal", "eager", or "none".
    use_wire=None,  # Use selenium-wire's webdriver over selenium webdriver.
    external_pdf=None,  # Set Chrome "plugins.always_open_pdf_externally":True.
    window_position=None,  # Set the browser's starting window position: "X,Y"
    window_size=None,  # Set the browser's starting window size: "Width,Height"
    is_mobile=None,  # Use the mobile device emulator while running tests.
    mobile=None,  # Shortcut / Duplicate of "is_mobile".
    d_width=None,  # Set device width
    d_height=None,  # Set device height
    d_p_r=None,  # Set device pixel ratio
    uc=None,  # Shortcut / Duplicate of "undetectable".
    undetected=None,  # Shortcut / Duplicate of "undetectable".
    uc_cdp=None,  # Shortcut / Duplicate of "uc_cdp_events".
    uc_sub=None,  # Shortcut / Duplicate of "uc_subprocess".
    log_cdp=None,  # Shortcut / Duplicate of "log_cdp_events".
    ad_block=None,  # Shortcut / Duplicate of "ad_block_on".
    server=None,  # Shortcut / Duplicate of "servername".
    guest=None,  # Shortcut / Duplicate of "guest_mode".
    wire=None,  # Shortcut / Duplicate of "use_wire".
    pls=None,  # Shortcut / Duplicate of "page_load_strategy".
):
    """
    * SeleniumBase Driver as a Python Context Manager or a returnable object. *

    Example 1: (context manager format)
    -----------------------------------
    .. code-block:: python
        from seleniumbase import DriverContext

        with DriverContext() as driver:
            driver.get("https://google.com/ncr")

    Example 2: (as a Python returnable)
    -----------------------------------
    .. code-block:: python
        from seleniumbase import Driver

        driver = Driver()
        driver.get("https://google.com/ncr")

    Optional Parameters:
    --------------------
    browser (str):  Choose from "chrome", "edge", "firefox", or "safari".
    headless (bool):  Use the default headless mode for Chromium and Firefox.
    headless1 (bool):  Use Chromium's old headless mode. (Fast, but limited)
    headless2 (bool):  Use Chromium's new headless mode. (Has more features)
    headed (bool):  Run tests in headed/GUI mode on Linux, where not default.
    locale_code (str):  Set the Language Locale Code for the web browser.
    protocol (str):  The Selenium Grid protocol: "http" or "https".
    servername (str):  The Selenium Grid server/IP used for tests.
    port (int):  The Selenium Grid port used by the test server.
    proxy (str):  Use proxy. Format: "SERVER:PORT" or "USER:PASS@SERVER:PORT".
    proxy_bypass_list (str):  Skip proxy when using the listed domains.
    proxy_pac_url (str):  Use PAC file. (Format: URL or USERNAME:PASSWORD@URL)
    multi_proxy (bool):  Allow multiple proxies with auth when multi-threaded.
    agent (str):  Modify the web browser's User-Agent string.
    cap_file (str):  The desired capabilities to use with a Selenium Grid.
    cap_string (str):  The desired capabilities to use with a Selenium Grid.
    recorder_ext (bool):  Enables the SeleniumBase Recorder Chromium extension.
    disable_cookies (bool):  Disable Cookies on websites. (Pages might break!)
    disable_js (bool):  Disable JavaScript on websites. (Pages might break!)
    disable_csp (bool):  Disable the Content Security Policy of websites.
    enable_ws (bool):  Enable Web Security on Chromium-based browsers.
    disable_ws (bool):  Reverse of "enable_ws". (None and False are different)
    enable_sync (bool):  Enable "Chrome Sync" on websites.
    use_auto_ext (bool):  Use Chrome's automation extension.
    undetectable (bool):  Use undetected-chromedriver to evade bot-detection.
    uc_cdp_events (bool):  Capture CDP events in undetected-chromedriver mode.
    uc_subprocess (bool):  Use undetected-chromedriver as a subprocess.
    log_cdp_events (bool):  Capture {"performance": "ALL", "browser": "ALL"}
    no_sandbox (bool):  (DEPRECATED) - "--no-sandbox" is always used now.
    disable_gpu (bool):  (DEPRECATED) - GPU is disabled if not "swiftshader".
    incognito (bool):  Enable Chromium's Incognito mode.
    guest_mode (bool):  Enable Chromium's Guest mode.
    dark_mode (bool):  Enable Chromium's Dark mode.
    devtools (bool):  Open Chromium's DevTools when the browser opens.
    remote_debug (bool):  Enable Chrome's Debugger on "http://localhost:9222".
    enable_3d_apis (bool):  Enable WebGL and 3D APIs.
    swiftshader (bool):  Chrome: --use-gl=angle / --use-angle=swiftshader-webgl
    ad_block_on (bool):  Block some types of display ads from loading.
    host_resolver_rules (str):  Set host-resolver-rules, comma-separated.
    block_images (bool):  Block images from loading during tests.
    do_not_track (bool):  Tell websites that you don't want to be tracked.
    chromium_arg (str):  "ARG=N,ARG2" (Set Chromium args, ","-separated.)
    firefox_arg (str):  "ARG=N,ARG2" (Set Firefox args, comma-separated.)
    firefox_pref (str):  SET (Set Firefox PREFERENCE:VALUE set, ","-separated)
    user_data_dir (str):  Set the Chrome user data directory to use.
    extension_zip (str):  Load a Chrome Extension .zip|.crx, comma-separated.
    extension_dir (str):  Load a Chrome Extension directory, comma-separated.
    disable_features (str):  "F1,F2" (Disable Chrome features, ","-separated.)
    binary_location (str):  Set path of the Chromium browser binary to use.
    driver_version (str):  Set the chromedriver or uc_driver version to use.
    page_load_strategy (str):  Set Chrome PLS to "normal", "eager", or "none".
    use_wire (bool):  Use selenium-wire's webdriver over selenium webdriver.
    external_pdf (bool):  Set Chrome "plugins.always_open_pdf_externally":True
    window_position (x,y):  Set the browser's starting window position: "X,Y"
    window_size (w,h):  Set the browser's starting window size: "Width,Height"
    is_mobile (bool):  Use the mobile device emulator while running tests.
    mobile (bool):  Shortcut / Duplicate of "is_mobile".
    d_width (int):  Set device width
    d_height (int):  Set device height
    d_p_r (float):  Set device pixel ratio
    uc (bool):  Shortcut / Duplicate of "undetectable".
    undetected (bool):  Shortcut / Duplicate of "undetectable".
    uc_cdp (bool):  Shortcut / Duplicate of "uc_cdp_events".
    uc_sub (bool):  Shortcut / Duplicate of "uc_subprocess".
    log_cdp (bool):  Shortcut / Duplicate of "log_cdp_events".
    ad_block (bool):  Shortcut / Duplicate of "ad_block_on".
    server (str):  Shortcut / Duplicate of "servername".
    guest (bool):  Shortcut / Duplicate of "guest_mode".
    wire (bool):  Shortcut / Duplicate of "use_wire".
    pls (str):  Shortcut / Duplicate of "page_load_strategy".
    """
    from seleniumbase import config as sb_config
    from seleniumbase.config import settings
    from seleniumbase.fixtures import constants
    from seleniumbase.fixtures import shared_utils

    sys_argv = sys.argv
    arg_join = " ".join(sys_argv)
    existing_runner = False
    collect_only = ("--co" in sys_argv or "--collect-only" in sys_argv)
    all_scripts = (hasattr(sb_config, "all_scripts") and sb_config.all_scripts)
    if (
        (hasattr(sb_config, "is_behave") and sb_config.is_behave)
        or (hasattr(sb_config, "is_pytest") and sb_config.is_pytest)
        or (hasattr(sb_config, "is_nosetest") and sb_config.is_nosetest)
    ):
        existing_runner = True
    if (
        existing_runner
        and not hasattr(sb_config, "_context_of_runner")
    ):
        if hasattr(sb_config, "is_pytest") and sb_config.is_pytest:
            import pytest
            msg = "Skipping `Driver()` script. (Use `python`, not `pytest`)"
            if not collect_only and not all_scripts:
                print("\n  *** %s" % msg)
            if collect_only or not all_scripts:
                pytest.skip(allow_module_level=True)
        elif hasattr(sb_config, "is_nosetest") and sb_config.is_nosetest:
            raise Exception(
                "\n  A Driver() script was triggered by nosetest collection!"
                '\n  (Prevent that by using: ``if __name__ == "__main__":``)'
            )
    elif existing_runner:
        sb_config._context_of_runner = True
    browser_changes = 0
    browser_set = None
    browser_text = None
    browser_list = []
    # As a shortcut, you can use "--edge" instead of "--browser=edge", etc,
    # but you can only specify one default browser for tests. (Default: chrome)
    if "--browser=chrome" in sys_argv or "--browser chrome" in sys_argv:
        browser_changes += 1
        browser_set = "chrome"
        browser_list.append("--browser=chrome")
    if "--browser=edge" in sys_argv or "--browser edge" in sys_argv:
        browser_changes += 1
        browser_set = "edge"
        browser_list.append("--browser=edge")
    if "--browser=firefox" in sys_argv or "--browser firefox" in sys_argv:
        browser_changes += 1
        browser_set = "firefox"
        browser_list.append("--browser=firefox")
    if "--browser=safari" in sys_argv or "--browser safari" in sys_argv:
        browser_changes += 1
        browser_set = "safari"
        browser_list.append("--browser=safari")
    if "--browser=ie" in sys_argv or "--browser ie" in sys_argv:
        browser_changes += 1
        browser_set = "ie"
        browser_list.append("--browser=ie")
    if "--browser=remote" in sys_argv or "--browser remote" in sys_argv:
        browser_changes += 1
        browser_set = "remote"
        browser_list.append("--browser=remote")
    browser_text = browser_set
    if "--chrome" in sys_argv and not browser_set == "chrome":
        browser_changes += 1
        browser_text = "chrome"
        browser_list.append("--chrome")
    if "--edge" in sys_argv and not browser_set == "edge":
        browser_changes += 1
        browser_text = "edge"
        browser_list.append("--edge")
    if "--firefox" in sys_argv and not browser_set == "firefox":
        browser_changes += 1
        browser_text = "firefox"
        browser_list.append("--firefox")
    if "--ie" in sys_argv and not browser_set == "ie":
        browser_changes += 1
        browser_text = "ie"
        browser_list.append("--ie")
    if "--safari" in sys_argv and not browser_set == "safari":
        browser_changes += 1
        browser_text = "safari"
        browser_list.append("--safari")
    if browser_changes > 1:
        message = "\n\n  TOO MANY browser types were entered!"
        message += "\n  There were %s found:\n  >  %s" % (
            browser_changes,
            ", ".join(browser_list),
        )
        message += "\n  ONLY ONE default browser is allowed!"
        message += "\n  Select a single browser & try again!\n"
        if not browser:
            raise Exception(message)
    if browser is None:
        if browser_text:
            browser = browser_text
        else:
            browser = "chrome"
    else:
        browser = browser.lower()
    valid_browsers = constants.ValidBrowsers.valid_browsers
    if browser not in valid_browsers:
        raise Exception(
            "Browser: {%s} is not a valid browser option. "
            "Valid options = {%s}" % (browser, valid_browsers)
        )
    if headless is None:
        if "--headless" in sys_argv:
            headless = True
        else:
            headless = False
    if headless1 is None:
        if "--headless1" in sys_argv:
            headless1 = True
        else:
            headless1 = False
    if headless1:
        headless = True
    if headless2 is None:
        if "--headless2" in sys_argv:
            headless2 = True
        else:
            headless2 = False
    if protocol is None:
        protocol = "http"  # For the Selenium Grid only!
    if server is not None and servername is None:
        servername = server
    if servername is None:
        servername = "localhost"  # For the Selenium Grid only!
    use_grid = False
    if servername != "localhost":
        # Use Selenium Grid (Use "127.0.0.1" for localhost Grid)
        use_grid = True
    if port is None:
        port = "4444"  # For the Selenium Grid only!
    if incognito is None:
        if "--incognito" in sys_argv:
            incognito = True
        else:
            incognito = False
    if guest is not None and guest_mode is None:
        guest_mode = guest
    if guest_mode is None:
        if "--guest" in sys_argv:
            guest_mode = True
        else:
            guest_mode = False
    if dark_mode is None:
        if "--dark" in sys_argv:
            dark_mode = True
        else:
            dark_mode = False
    if devtools is None:
        if "--devtools" in sys_argv:
            devtools = True
        else:
            devtools = False
    if mobile is not None and is_mobile is None:
        is_mobile = mobile
    if is_mobile is None:
        if "--mobile" in sys_argv:
            is_mobile = True
        else:
            is_mobile = False
    test_id = "direct_driver"
    proxy_string = proxy
    if proxy_string is None and "--proxy" in arg_join:
        if "--proxy=" in arg_join:
            proxy_string = arg_join.split("--proxy=")[1].split(" ")[0]
        elif "--proxy " in arg_join:
            proxy_string = arg_join.split("--proxy ")[1].split(" ")[0]
        if proxy_string:
            if proxy_string.startswith('"') and proxy_string.endswith('"'):
                proxy_string = proxy_string[1:-1]
            elif proxy_string.startswith("'") and proxy_string.endswith("'"):
                proxy_string = proxy_string[1:-1]
    c_a = chromium_arg
    if c_a is None and "--chromium-arg" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--chromium-arg="):
                c_a = arg.split("--chromium-arg=")[1]
                break
            elif arg == "--chromium-arg" and len(sys_argv) > count + 1:
                c_a = sys_argv[count + 1]
                if c_a.startswith("-"):
                    c_a = None
                break
            count += 1
    chromium_arg = c_a
    d_f = disable_features
    if d_f is None and "--disable-features" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--disable-features="):
                d_f = arg.split("--disable-features=")[1]
                break
            elif arg == "--disable-features" and len(sys_argv) > count + 1:
                d_f = sys_argv[count + 1]
                if d_f.startswith("-"):
                    d_f = None
                break
            count += 1
    disable_features = d_f
    w_p = window_position
    if w_p is None and "--window-position" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--window-position="):
                w_p = arg.split("--window-position=")[1]
                break
            elif arg == "--window-position" and len(sys_argv) > count + 1:
                w_p = sys_argv[count + 1]
                if w_p.startswith("-"):
                    w_p = None
                break
            count += 1
        window_position = w_p
        if window_position:
            if window_position.count(",") != 1:
                message = (
                    '\n\n  window_position expects an "x,y" string!'
                    '\n  (Your input was: "%s")\n' % window_position
                )
                raise Exception(message)
            window_position = window_position.replace(" ", "")
            win_x = None
            win_y = None
            try:
                win_x = int(window_position.split(",")[0])
                win_y = int(window_position.split(",")[1])
            except Exception:
                message = (
                    '\n\n  Expecting integer values for "x,y"!'
                    '\n  (window_position input was: "%s")\n'
                    % window_position
                )
                raise Exception(message)
            settings.WINDOW_START_X = win_x
            settings.WINDOW_START_Y = win_y
    w_s = window_size
    if w_s is None and "--window-size" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--window-size="):
                w_s = arg.split("--window-size=")[1]
                break
            elif arg == "--window-size" and len(sys_argv) > count + 1:
                w_s = sys_argv[count + 1]
                if w_s.startswith("-"):
                    w_s = None
                break
            count += 1
        window_size = w_s
        if window_size:
            if window_size.count(",") != 1:
                message = (
                    '\n\n  window_size expects a "width,height" string!'
                    '\n  (Your input was: "%s")\n' % window_size
                )
                raise Exception(message)
            window_size = window_size.replace(" ", "")
            width = None
            height = None
            try:
                width = int(window_size.split(",")[0])
                height = int(window_size.split(",")[1])
            except Exception:
                message = (
                    '\n\n  Expecting integer values for "width,height"!'
                    '\n  (window_size input was: "%s")\n' % window_size
                )
                raise Exception(message)
            settings.CHROME_START_WIDTH = width
            settings.CHROME_START_HEIGHT = height
            settings.HEADLESS_START_WIDTH = width
            settings.HEADLESS_START_HEIGHT = height
    if agent is None and "--agent" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--agent="):
                agent = arg.split("--agent=")[1]
                break
            elif arg == "--agent" and len(sys_argv) > count + 1:
                agent = sys_argv[count + 1]
                if agent.startswith("-"):
                    agent = None
                break
            count += 1
    user_agent = agent
    recorder_mode = False
    if recorder_ext:
        recorder_mode = True
    if (
        "--recorder" in sys_argv
        or "--record" in sys_argv
        or "--rec" in sys_argv
    ):
        recorder_mode = True
        recorder_ext = True
    if (
        undetectable
        or undetected
        or uc
        or uc_cdp_events
        or uc_cdp
        or uc_subprocess
        or uc_sub
    ):
        undetectable = True
    if (
        (undetectable or undetected or uc)
        and (uc_subprocess is None)
        and (uc_sub is None)
    ):
        uc_subprocess = True  # Use UC as a subprocess by default.
    elif (
        "--undetectable" in sys_argv
        or "--undetected" in sys_argv
        or "--uc" in sys_argv
        or "--uc-cdp-events" in sys_argv
        or "--uc_cdp_events" in sys_argv
        or "--uc-cdp" in sys_argv
        or "--uc-subprocess" in sys_argv
        or "--uc_subprocess" in sys_argv
        or "--uc-sub" in sys_argv
    ):
        undetectable = True
        if uc_subprocess is None and uc_sub is None:
            uc_subprocess = True  # Use UC as a subprocess by default.
    else:
        undetectable = False
    if uc_subprocess or uc_sub:
        uc_subprocess = True
    elif (
        "--uc-subprocess" in sys_argv
        or "--uc_subprocess" in sys_argv
        or "--uc-sub" in sys_argv
    ):
        uc_subprocess = True
    else:
        uc_subprocess = False
    if uc_cdp_events or uc_cdp:
        undetectable = True
        uc_cdp_events = True
    elif (
        "--uc-cdp-events" in sys_argv
        or "--uc_cdp_events" in sys_argv
        or "--uc-cdp" in sys_argv
        or "--uc_cdp" in sys_argv
    ):
        undetectable = True
        uc_cdp_events = True
    else:
        uc_cdp_events = False
    if undetectable and browser != "chrome":
        message = (
            '\n  Undetected-Chromedriver Mode ONLY supports Chrome!'
            '\n  ("uc=True" / "undetectable=True" / "--uc")'
            '\n  (Your browser choice was: "%s".)'
            '\n  (Will use "%s" without UC Mode.)\n' % (browser, browser)
        )
        print(message)
    if headed is None:
        # Override the default headless mode on Linux if set.
        if "--gui" in sys_argv or "--headed" in sys_argv:
            headed = True
        else:
            headed = False
    if (
        shared_utils.is_linux()
        and not headed
        and not headless
        and not headless2
        and (
            not undetectable
            or "DISPLAY" not in os.environ.keys()
            or not os.environ["DISPLAY"]
        )
    ):
        headless = True
    if recorder_mode and headless:
        headless = False
        headless1 = False
        headless2 = True
    if headless2 and browser == "firefox":
        headless2 = False  # Only for Chromium browsers
        headless = True  # Firefox has regular headless
    elif browser not in ["chrome", "edge"]:
        headless2 = False  # Only for Chromium browsers
    if disable_csp is None:
        if (
            "--disable-csp" in sys_argv
            or "--no-csp" in sys_argv
            or "--dcsp" in sys_argv
        ):
            disable_csp = True
        else:
            disable_csp = False
    if (
        (enable_ws is None and disable_ws is None)
        and (
            "--disable-web-security" in sys_argv
            or "--disable-ws" in sys_argv
            or "--dws" in sys_argv
        )
    ):
        enable_ws = False
    elif (
        (enable_ws is None and disable_ws is None)
        or (disable_ws is not None and not disable_ws)
        or (enable_ws is not None and enable_ws)
    ):
        enable_ws = True
    else:
        enable_ws = False
    if log_cdp_events is None and log_cdp is None:
        if (
            "--log-cdp-events" in sys_argv
            or "--log_cdp_events" in sys_argv
            or "--log-cdp" in sys_argv
            or "--log_cdp" in sys_argv
        ):
            log_cdp_events = True
        else:
            log_cdp_events = False
    elif log_cdp_events or log_cdp:
        log_cdp_events = True
    else:
        log_cdp_events = False
    if use_auto_ext is None:
        if "--use-auto-ext" in sys_argv:
            use_auto_ext = True
        else:
            use_auto_ext = False
    if disable_cookies is None:
        if "--disable-cookies" in sys_argv:
            disable_cookies = True
        else:
            disable_cookies = False
    if disable_js is None:
        if "--disable-js" in sys_argv:
            disable_js = True
        else:
            disable_js = False
    if pls is not None and page_load_strategy is None:
        page_load_strategy = pls
    if not page_load_strategy and "--pls=" in arg_join:
        if "--pls=none" in sys_argv or '--pls="none"' in sys_argv:
            page_load_strategy = "none"
        elif "--pls=eager" in sys_argv or '--pls="eager"' in sys_argv:
            page_load_strategy = "eager"
        elif "--pls=normal" in sys_argv or '--pls="normal"' in sys_argv:
            page_load_strategy = "normal"
    if page_load_strategy is not None:
        if page_load_strategy.lower() not in ["normal", "eager", "none"]:
            raise Exception(
                'page_load_strategy must be "normal", "eager", or "none"!'
            )
        page_load_strategy = page_load_strategy.lower()
    elif "--pls=normal" in sys_argv or '--pls="normal"' in sys_argv:
        page_load_strategy = "normal"
    elif "--pls=eager" in sys_argv or '--pls="eager"' in sys_argv:
        page_load_strategy = "eager"
    elif "--pls=none" in sys_argv or '--pls="none"' in sys_argv:
        page_load_strategy = "none"
    if block_images is None:
        if "--block-images" in sys_argv or "--block_images" in sys_argv:
            block_images = True
        else:
            block_images = False
    if do_not_track is None:
        if "--do-not-track" in sys_argv or "--do_not_track" in sys_argv:
            do_not_track = True
        else:
            do_not_track = False
    if use_wire is None and wire is None:
        if "--wire" in sys_argv:
            use_wire = True
        else:
            use_wire = False
    elif use_wire or wire:
        use_wire = True
    else:
        use_wire = False
    if external_pdf is None:
        if "--external-pdf" in sys_argv or "--external_pdf" in sys_argv:
            external_pdf = True
        else:
            external_pdf = False
    if remote_debug is None:
        if "--remote-debug" in sys_argv or "--remote_debug" in sys_argv:
            remote_debug = True
        else:
            remote_debug = False
    if enable_3d_apis is None:
        if "--enable-3d-apis" in sys_argv or "--enable_3d_apis" in sys_argv:
            enable_3d_apis = True
        else:
            enable_3d_apis = False
    if swiftshader is None:
        if "--swiftshader" in sys_argv:
            swiftshader = True
        else:
            swiftshader = False
    if ad_block is not None and ad_block_on is None:
        ad_block_on = ad_block
    if ad_block_on is None:
        if "--ad-block" in sys_argv or "--ad_block" in sys_argv:
            ad_block_on = True
        else:
            ad_block_on = False
    if host_resolver_rules is None:
        if '--host-resolver-rules="' in arg_join:
            host_resolver_rules = (
                arg_join.split('--host-resolver-rules="')[1].split('"')[0]
            )
        elif '--host_resolver_rules="' in arg_join:
            host_resolver_rules = (
                arg_join.split("--host_resolver_rules=")[1].split('"')[0]
            )
    if driver_version is None and "--driver-version" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--driver-version="):
                driver_version = arg.split("--driver-version=")[1]
                break
            elif arg == "--driver-version" and len(sys_argv) > count + 1:
                driver_version = sys_argv[count + 1]
                if driver_version.startswith("-"):
                    driver_version = None
                break
            count += 1
    if driver_version is None and "--driver_version" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--driver_version="):
                driver_version = arg.split("--driver_version=")[1]
                break
            elif arg == "--driver_version" and len(sys_argv) > count + 1:
                driver_version = sys_argv[count + 1]
                if driver_version.startswith("-"):
                    driver_version = None
                break
            count += 1
    browser_name = browser

    # Launch a web browser
    from seleniumbase.core import browser_launcher

    driver = browser_launcher.get_driver(
        browser_name=browser_name,
        headless=headless,
        locale_code=locale_code,
        use_grid=use_grid,
        protocol=protocol,
        servername=servername,
        port=port,
        proxy_string=proxy_string,
        proxy_bypass_list=proxy_bypass_list,
        proxy_pac_url=proxy_pac_url,
        multi_proxy=multi_proxy,
        user_agent=user_agent,
        cap_file=cap_file,
        cap_string=cap_string,
        recorder_ext=recorder_ext,
        disable_cookies=disable_cookies,
        disable_js=disable_js,
        disable_csp=disable_csp,
        enable_ws=enable_ws,
        enable_sync=enable_sync,
        use_auto_ext=use_auto_ext,
        undetectable=undetectable,
        uc_cdp_events=uc_cdp_events,
        uc_subprocess=uc_subprocess,
        log_cdp_events=log_cdp_events,
        no_sandbox=no_sandbox,
        disable_gpu=disable_gpu,
        headless1=headless1,
        headless2=headless2,
        incognito=incognito,
        guest_mode=guest_mode,
        dark_mode=dark_mode,
        devtools=devtools,
        remote_debug=remote_debug,
        enable_3d_apis=enable_3d_apis,
        swiftshader=swiftshader,
        ad_block_on=ad_block_on,
        host_resolver_rules=host_resolver_rules,
        block_images=block_images,
        do_not_track=do_not_track,
        chromium_arg=chromium_arg,
        firefox_arg=firefox_arg,
        firefox_pref=firefox_pref,
        user_data_dir=user_data_dir,
        extension_zip=extension_zip,
        extension_dir=extension_dir,
        disable_features=disable_features,
        binary_location=binary_location,
        driver_version=driver_version,
        page_load_strategy=page_load_strategy,
        use_wire=use_wire,
        external_pdf=external_pdf,
        test_id=test_id,
        mobile_emulator=is_mobile,
        device_width=d_width,
        device_height=d_height,
        device_pixel_ratio=d_p_r,
        browser=browser_name,
    )
    return driver
