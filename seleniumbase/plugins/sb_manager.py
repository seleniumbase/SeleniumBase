"""
SeleniumBase as a Python Context Manager.
#########################################

The SeleniumBase SB Context Manager:
Usage --> ``with SB() as sb:``

Example -->

```python
from seleniumbase import SB

with SB() as sb:  # Many args! Eg. SB(browser="edge")
    sb.open("https://google.com/ncr")
    sb.type('[name="q"]', "SeleniumBase on GitHub\n")
    sb.click('a[href*="github.com/seleniumbase"]')
    sb.highlight("div.Layout-main")
    sb.highlight("div.Layout-sidebar")
    sb.sleep(0.5)
```

# (The browser exits automatically after the "with" block ends.)

#########################################
"""
from contextlib import contextmanager


@contextmanager  # Usage: -> ``with SB() as sb:``
def SB(
    test=None,  # Test Mode: Output, Logging, Continue on failure unless "rtf".
    rtf=None,  # Shortcut / Duplicate of "raise_test_failure".
    raise_test_failure=None,  # If "test" mode, raise Exception on 1st failure.
    browser=None,  # Choose from "chrome", "edge", "firefox", or "safari".
    headless=None,  # Use the default headless mode for Chromium and Firefox.
    headless1=None,  # Use Chromium's old headless mode. (Fast, but limited)
    headless2=None,  # Use Chromium's new headless mode. (Has more features)
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
    enable_sync=None,  # Enable "Chrome Sync" on websites.
    use_auto_ext=None,  # Use Chrome's automation extension.
    undetectable=None,  # Use undetected-chromedriver to evade bot-detection.
    uc_cdp_events=None,  # Capture CDP events in undetected-chromedriver mode.
    uc_subprocess=None,  # Use undetected-chromedriver as a subprocess.
    log_cdp_events=None,  # Capture {"performance": "ALL", "browser": "ALL"}
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
    skip_js_waits=None,  # Skip JS Waits (readyState=="complete" and Angular).
    wait_for_angularjs=None,  # Wait for AngularJS to load after some actions.
    use_wire=None,  # Use selenium-wire's webdriver over selenium webdriver.
    external_pdf=None,  # Set Chrome "plugins.always_open_pdf_externally":True.
    window_position=None,  # Set the browser's starting window position: "X,Y"
    window_size=None,  # Set the browser's starting window size: "Width,Height"
    is_mobile=None,  # Use the mobile device emulator while running tests.
    mobile=None,  # Shortcut / Duplicate of "is_mobile".
    device_metrics=None,  # Set mobile metrics: "CSSWidth,CSSHeight,PixelRatio"
    xvfb=None,  # Run tests using the Xvfb virtual display server on Linux OS.
    xvfb_metrics=None,  # Set Xvfb display size on Linux: "Width,Height".
    start_page=None,  # The starting URL for the web browser when tests begin.
    rec_print=None,  # If Recorder is enabled, prints output after tests end.
    rec_behave=None,  # Like Recorder Mode, but also generates behave-gherkin.
    record_sleep=None,  # If Recorder enabled, also records self.sleep calls.
    data=None,  # Extra test data. Access with "self.data" in tests.
    var1=None,  # Extra test data. Access with "self.var1" in tests.
    var2=None,  # Extra test data. Access with "self.var2" in tests.
    var3=None,  # Extra test data. Access with "self.var3" in tests.
    variables=None,  # DICT (Extra test data. Access with "self.variables")
    account=None,  # Set account. Access with "self.account" in tests.
    environment=None,  # Set the test env. Access with "self.env" in tests.
    headed=None,  # Run tests in headed/GUI mode on Linux, where not default.
    maximize=None,  # Start tests with the browser window maximized.
    disable_ws=None,  # Reverse of "enable_ws". (None and False are different)
    disable_beforeunload=None,  # Disable the "beforeunload" event on Chromium.
    settings_file=None,  # A file for overriding default SeleniumBase settings.
    position=None,  # Shortcut / Duplicate of "window_position".
    size=None,  # Shortcut / Duplicate of "window_size".
    uc=None,  # Shortcut / Duplicate of "undetectable".
    undetected=None,  # Shortcut / Duplicate of "undetectable".
    uc_cdp=None,  # Shortcut / Duplicate of "uc_cdp_events".
    uc_sub=None,  # Shortcut / Duplicate of "uc_subprocess".
    locale=None,  # Shortcut / Duplicate of "locale_code".
    log_cdp=None,  # Shortcut / Duplicate of "log_cdp_events".
    ad_block=None,  # Shortcut / Duplicate of "ad_block_on".
    server=None,  # Shortcut / Duplicate of "servername".
    guest=None,  # Shortcut / Duplicate of "guest_mode".
    wire=None,  # Shortcut / Duplicate of "use_wire".
    pls=None,  # Shortcut / Duplicate of "page_load_strategy".
    sjw=None,  # Shortcut / Duplicate of "skip_js_waits".
    wfa=None,  # Shortcut / Duplicate of "wait_for_angularjs".
    save_screenshot=None,  # Save a screenshot at the end of each test.
    no_screenshot=None,  # No screenshots saved unless tests directly ask it.
    page_load_strategy=None,  # Set Chrome PLS to "normal", "eager", or "none".
    timeout_multiplier=None,  # Multiplies the default timeout values.
    js_checking_on=None,  # Check for JavaScript errors after page loads.
    slow=None,  # Slow down the automation. Faster than using Demo Mode.
    demo=None,  # Slow down and visually see test actions as they occur.
    demo_sleep=None,  # SECONDS (Set wait time after Slow & Demo Mode actions.)
    message_duration=None,  # SECONDS (The time length for Messenger alerts.)
    highlights=None,  # Number of highlight animations for Demo Mode actions.
    interval=None,  # SECONDS (Autoplay interval for SB Slides & Tour steps.)
    time_limit=None,  # SECONDS (Safely fail tests that exceed the time limit.)
):
    """
    * SeleniumBase as a Python Context Manager *

    Example:
    --------
    .. code-block:: python
        from seleniumbase import SB

        with SB() as sb:  # Many args! Eg. SB(browser="edge")
            sb.open("https://google.com/ncr")
            sb.type('[name="q"]', "SeleniumBase on GitHub")
            sb.submit('[name="q"]')
            sb.click('a[href*="github.com/seleniumbase"]')
            sb.highlight("div.Layout-main")
            sb.highlight("div.Layout-sidebar")
            sb.sleep(0.5)

    Optional Parameters:
    --------------------
    test (bool):  Test Mode: Output, Logging, Continue on failure unless "rtf".
    rtf (bool):  Shortcut / Duplicate of "raise_test_failure".
    raise_test_failure (bool):  If "test" mode, raise Exception on 1st failure.
    browser (str):  Choose from "chrome", "edge", "firefox", or "safari".
    headless (bool):  Use the default headless mode for Chromium and Firefox.
    headless1 (bool):  Use Chromium's old headless mode. (Fast, but limited)
    headless2 (bool):  Use Chromium's new headless mode. (Has more features)
    locale_code (str):  Set the Language Locale Code for the web browser.
    protocol (str):  The Selenium Grid protocol: "http" or "https".
    servername (str):  The Selenium Grid server/IP used for tests.
    port (int):  The Selenium Grid port used by the test server.
    proxy (str):  Use proxy. Format: "SERVER:PORT" or "USER:PASS@SERVER:PORT".
    proxy_bypass_list (str):  Skip proxy when using the listed domains.
    proxy_pac_url (str):  Use PAC file. (Format: URL or USERNAME:PASSWORD@URL)
    multi_proxy (bool):  # Allow multiple proxies with auth when multithreaded.
    agent (str):  Modify the web browser's User-Agent string.
    cap_file (str):  The desired capabilities to use with a Selenium Grid.
    cap_string (str):  The desired capabilities to use with a Selenium Grid.
    recorder_ext (bool):  Enables the SeleniumBase Recorder Chromium extension.
    disable_cookies (bool):  Disable Cookies on websites. (Pages might break!)
    disable_js (bool):  Disable JavaScript on websites. (Pages might break!)
    disable_csp (bool):  Disable the Content Security Policy of websites.
    enable_ws (bool):  Enable Web Security on Chromium-based browsers.
    enable_sync (bool):  Enable "Chrome Sync" on websites.
    use_auto_ext (bool):  Use Chrome's automation extension.
    undetectable (bool):  Use undetected-chromedriver to evade bot-detection.
    uc_cdp_events (bool):  Capture CDP events in undetected-chromedriver mode.
    uc_subprocess (bool):  Use undetected-chromedriver as a subprocess.
    log_cdp_events (bool):  Capture {"performance": "ALL", "browser": "ALL"}
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
    skip_js_waits (bool):  Skip JS Waits (readyState=="complete" and Angular).
    wait_for_angularjs (bool):  Wait for AngularJS to load after some actions.
    use_wire (bool):  Use selenium-wire's webdriver over selenium webdriver.
    external_pdf (bool):  Set Chrome "plugins.always_open_pdf_externally":True.
    window_position (x,y):  Set the browser's starting window position: "X,Y"
    window_size (w,h):  Set the browser's starting window size: "Width,Height"
    is_mobile (bool):  Use the mobile device emulator while running tests.
    mobile (bool):  Shortcut / Duplicate of "is_mobile".
    device_metrics (w,h,pr):  Mobile metrics: "CSSWidth,CSSHeight,PixelRatio"
    xvfb (bool):  Run tests using the Xvfb virtual display server on Linux OS.
    xvfb_metrics (w,h):  Set Xvfb display size on Linux: "Width,Height".
    start_page (str):  The starting URL for the web browser when tests begin.
    rec_print (bool):  If Recorder is enabled, prints output after tests end.
    rec_behave (bool):  Like Recorder Mode, but also generates behave-gherkin.
    record_sleep (bool):  If Recorder enabled, also records self.sleep calls.
    data (str):  Extra test data. Access with "self.data" in tests.
    var1 (str):  Extra test data. Access with "self.var1" in tests.
    var2 (str):  Extra test data. Access with "self.var2" in tests.
    var3 (str):  Extra test data. Access with "self.var3" in tests.
    variables (dict):  Extra test data. Access with "self.variables".
    account (str):  Set account. Access with "self.account" in tests.
    environment (str):  Set the test env. Access with "self.env" in tests.
    headed (bool):  Run tests in headed/GUI mode on Linux, where not default.
    maximize (bool):  Start tests with the browser window maximized.
    disable_ws (bool):  Reverse of "enable_ws". (None and False are different)
    disable_beforeunload (bool):  Disable the "beforeunload" event on Chromium.
    settings_file (str):  A file for overriding default SeleniumBase settings.
    position (x,y):  Shortcut / Duplicate of "window_position".
    size (w,h):  Shortcut / Duplicate of "window_size".
    uc (bool):  Shortcut / Duplicate of "undetectable".
    undetected (bool):  Shortcut / Duplicate of "undetectable".
    uc_cdp (bool):  Shortcut / Duplicate of "uc_cdp_events".
    uc_sub (bool):  Shortcut / Duplicate of "uc_subprocess".
    locale (str):  Shortcut / Duplicate of "locale_code".
    log_cdp (bool):  Shortcut / Duplicate of "log_cdp_events".
    ad_block (bool):  Shortcut / Duplicate of "ad_block_on".
    server (str):  Shortcut / Duplicate of "servername".
    guest (bool):  Shortcut / Duplicate of "guest_mode".
    wire (bool):  Shortcut / Duplicate of "use_wire".
    pls (str):  Shortcut / Duplicate of "page_load_strategy".
    sjw (bool):  Shortcut / Duplicate of "skip_js_waits".
    wfa (bool):  Shortcut / Duplicate of "wait_for_angularjs".
    save_screenshot (bool):  Save a screenshot at the end of each test.
    no_screenshot (bool):  No screenshots saved unless tests directly ask it.
    page_load_strategy (str):  Set Chrome PLS to "normal", "eager", or "none".
    timeout_multiplier (float):  Multiplies the default timeout values.
    js_checking_on (bool):  Check for JavaScript errors after page loads.
    slow (bool):  Slow down the automation. Faster than using Demo Mode.
    demo (bool):  Slow down and visually see test actions as they occur.
    demo_sleep (float):  SECONDS (Set wait time after Slow & Demo Mode actions)
    message_duration (float):  SECONDS (The time length for Messenger alerts.)
    highlights (int):  Number of highlight animations for Demo Mode actions.
    interval (float):  SECONDS (Autoplay interval for SB Slides & Tour steps.)
    time_limit (float):  SECONDS (Safely fail tests that exceed the time limit)
    """
    import colorama
    import os
    import sys
    import time
    import traceback
    from seleniumbase import BaseCase
    from seleniumbase import config as sb_config
    from seleniumbase.config import settings
    from seleniumbase.fixtures import constants
    from seleniumbase.fixtures import shared_utils

    sb_config_backup = sb_config
    sb_config._do_sb_post_mortem = False
    sys_argv = sys.argv
    arg_join = " ".join(sys_argv)
    archive_logs = False
    existing_runner = False
    collect_only = ("--co" in sys_argv or "--collect-only" in sys_argv)
    all_scripts = (hasattr(sb_config, "all_scripts") and sb_config.all_scripts)
    do_log_folder_setup = False  # The first "test=True" run does it
    if (
        (hasattr(sb_config, "is_behave") and sb_config.is_behave)
        or (hasattr(sb_config, "is_pytest") and sb_config.is_pytest)
        or (hasattr(sb_config, "is_nosetest") and sb_config.is_nosetest)
    ):
        existing_runner = True
        test = False  # Already using a test runner. Skip extra test steps.
    elif test is None and "--test" in sys_argv:
        test = True
    if existing_runner and not hasattr(sb_config, "_context_of_runner"):
        if hasattr(sb_config, "is_pytest") and sb_config.is_pytest:
            import pytest
            msg = "Skipping `SB()` script. (Use `python`, not `pytest`)"
            if not collect_only and not all_scripts:
                print("\n  *** %s" % msg)
            if collect_only or not all_scripts:
                pytest.skip(allow_module_level=True)
        elif hasattr(sb_config, "is_nosetest") and sb_config.is_nosetest:
            raise Exception(
                "\n  SB Manager script was triggered by nosetest collection!"
                '\n  (Prevent that by using: ``if __name__ == "__main__":``)'
            )
    elif existing_runner:
        sb_config._context_of_runner = True
    if (
        not existing_runner
        and not hasattr(sb_config, "_has_older_context")
        and test
    ):
        # This is the first "test" from context manager scripts run.
        sb_config._has_older_context = True
        do_log_folder_setup = True
    else:
        if test:
            pass  # Not the first "test" of context manager scripts.
        else:
            pass  # Not in "test" mode. (No special output/logging.)
    with_testing_base = False
    if test:
        with_testing_base = True
    if (
        raise_test_failure
        or rtf
        or "--raise-test-failure" in sys_argv
        or "--raise_test_failure" in sys_argv
        or "--rtf" in sys_argv
        or "-x" in sys_argv  # Carry-over from "pytest"
        or "--exitfirst" in sys_argv  # Carry-over from "pytest"
    ):
        raise_test_failure = True  # Exit on first error or failed test.
    else:
        raise_test_failure = False
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
        sb_config._browser_shortcut = "chrome"
        browser_list.append("--chrome")
    if "--edge" in sys_argv and not browser_set == "edge":
        browser_changes += 1
        browser_text = "edge"
        sb_config._browser_shortcut = "edge"
        browser_list.append("--edge")
    if "--firefox" in sys_argv and not browser_set == "firefox":
        browser_changes += 1
        browser_text = "firefox"
        sb_config._browser_shortcut = "firefox"
        browser_list.append("--firefox")
    if "--ie" in sys_argv and not browser_set == "ie":
        browser_changes += 1
        browser_text = "ie"
        sb_config._browser_shortcut = "ie"
        browser_list.append("--ie")
    if "--safari" in sys_argv and not browser_set == "safari":
        browser_changes += 1
        browser_text = "safari"
        sb_config._browser_shortcut = "safari"
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
    if port is None:
        port = "4444"  # For the Selenium Grid only!
    if not environment:
        environment = "test"
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
    if is_mobile:
        sb_config.mobile_emulator = True
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
    if window_position is None and position is not None:
        window_position = position
    w_p = window_position
    if (
        w_p is None
        and ("--window-position" in arg_join or "--position" in arg_join)
    ):
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
    if window_size is None and size is not None:
        window_size = size
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
    x_m = xvfb_metrics
    if x_m is None and "--xvfb-metrics" in arg_join:
        count = 0
        for arg in sys_argv:
            if arg.startswith("--xvfb-metrics="):
                x_m = arg.split("--xvfb-metrics=")[1]
                break
            elif arg == "--xvfb-metrics" and len(sys_argv) > count + 1:
                x_m = sys_argv[count + 1]
                if x_m.startswith("-"):
                    x_m = None
                break
            count += 1
    xvfb_metrics = x_m
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
    if rec_print is None:
        if "--rec-print" in sys_argv:
            rec_print = True
        else:
            rec_print = False
    if rec_behave is None:
        if "--rec-behave" in sys_argv:
            rec_behave = True
        else:
            rec_behave = False
    if record_sleep is None:
        if "--rec-sleep" in sys_argv or "--record-sleep" in sys_argv:
            record_sleep = True
        else:
            record_sleep = False
    if xvfb is None:
        if "--xvfb" in sys_argv:
            xvfb = True
        else:
            xvfb = False
    if not shared_utils.is_linux():
        # The Xvfb virtual display server is for Linux OS Only!
        xvfb = False
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
    if undetectable or undetected or uc:
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
        and not xvfb
    ):
        if not undetectable:
            headless = True
        else:
            xvfb = True
    if headless2 and browser == "firefox":
        headless2 = False  # Only for Chromium browsers
        headless = True  # Firefox has regular headless
    elif browser not in ["chrome", "edge"]:
        headless2 = False  # Only for Chromium browsers
    if not headless and not headless2:
        headed = True
    if rec_print and not recorder_mode:
        recorder_mode = True
        recorder_ext = True
    elif rec_behave and not recorder_mode:
        recorder_mode = True
        recorder_ext = True
    elif record_sleep and not recorder_mode:
        recorder_mode = True
        recorder_ext = True
    if recorder_mode and headless:
        headless = False
        headless1 = False
        headless2 = True
    sb_config.proxy_driver = False
    if "--proxy-driver" in sys_argv or "--proxy_driver" in sys_argv:
        sb_config.proxy_driver = True
    if variables and isinstance(variables, str) and len(variables) > 0:
        import ast
        bad_input = False
        if (
            not variables.startswith("{")
            or not variables.endswith("}")
        ):
            bad_input = True
        else:
            try:
                variables = ast.literal_eval(variables)
                if not isinstance(variables, dict):
                    bad_input = True
            except Exception:
                bad_input = True
        if bad_input:
            raise Exception(
                '\nExpecting a Python dictionary for "variables"!'
                "\nEg. --variables=\"{'KEY1':'VALUE', 'KEY2':123}\""
            )
    else:
        variables = {}
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
        disable_ws = True
    elif (
        (enable_ws is None and disable_ws is None)
        or (disable_ws is not None and not disable_ws)
        or (enable_ws is not None and enable_ws)
    ):
        enable_ws = True
        disable_ws = False
    else:
        enable_ws = False
        disable_ws = True
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
    maximize_option = False
    if maximize or "--maximize" in sys_argv:
        maximize_option = True
    _disable_beforeunload = False
    if disable_beforeunload:
        _disable_beforeunload = True
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
    if sjw is not None and skip_js_waits is None:
        skip_js_waits = sjw
    if skip_js_waits is None:
        if (
            "--sjw" in sys_argv
            or "--skip_js_waits" in sys_argv
            or "--skip-js-waits" in sys_argv
        ):
            settings.SKIP_JS_WAITS = True
    elif skip_js_waits:
        settings.SKIP_JS_WAITS = skip_js_waits
    if wfa is not None and wait_for_angularjs is None:
        wait_for_angularjs = wfa
    if wait_for_angularjs is None:
        if (
            "--wfa" in sys_argv
            or "--wait_for_angularjs" in sys_argv
            or "--wait-for-angularjs" in sys_argv
        ):
            settings.WAIT_FOR_ANGULARJS = True
    elif wait_for_angularjs:
        settings.WAIT_FOR_ANGULARJS = wait_for_angularjs
    if save_screenshot is None:
        if (
            "--screenshot" in sys_argv
            or "--save-screenshot" in sys_argv
            or "--ss" in sys_argv
        ):
            save_screenshot = True
        else:
            save_screenshot = False
    if no_screenshot is None:
        if "--no-screenshot" in sys_argv or "--ns" in sys_argv:
            no_screenshot = True
        else:
            no_screenshot = False
    if save_screenshot and no_screenshot:
        save_screenshot = False  # "no_screenshot" has priority
    if browser == "safari" and headless:
        headless = False  # Safari doesn't support headless mode
        headless1 = False
    if js_checking_on is None:
        if "--check-js" in sys_argv:
            js_checking_on = True
        else:
            js_checking_on = False
    slow_mode = False
    if slow:
        slow_mode = True
    elif "--slow" in sys_argv:
        slow_mode = True
    demo_mode = False
    if demo:
        demo_mode = True
    elif "--demo" in sys_argv:
        demo_mode = True
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
    if locale is not None and locale_code is None:
        locale_code = locale
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
    if highlights is not None:
        try:
            highlights = int(highlights)
        except Exception:
            raise Exception('"highlights" must be an integer!')
    if interval is not None:
        try:
            interval = float(interval)
        except Exception:
            raise Exception('"interval" must be numeric!')
    if time_limit is not None:
        try:
            time_limit = float(time_limit)
        except Exception:
            raise Exception('"time_limit" must be numeric!')

    sb_config.with_testing_base = with_testing_base
    sb_config.browser = browser
    if not hasattr(sb_config, "is_behave"):
        sb_config.is_behave = False
    if not hasattr(sb_config, "is_pytest"):
        sb_config.is_pytest = False
    if not hasattr(sb_config, "is_nosetest"):
        sb_config.is_nosetest = False
    sb_config.is_context_manager = True
    sb_config.headless = headless
    sb_config.headless1 = headless1
    sb_config.headless2 = headless2
    sb_config.headed = headed
    sb_config.xvfb = xvfb
    sb_config.xvfb_metrics = xvfb_metrics
    sb_config.start_page = start_page
    sb_config.locale_code = locale_code
    sb_config.protocol = protocol
    sb_config.servername = servername
    sb_config.port = port
    sb_config.data = data
    sb_config.var1 = var1
    sb_config.var2 = var2
    sb_config.var3 = var3
    sb_config.variables = variables
    sb_config.account = account
    sb_config.environment = environment
    sb_config.env = environment
    sb_config.user_agent = user_agent
    sb_config.incognito = incognito
    sb_config.guest_mode = guest_mode
    sb_config.dark_mode = dark_mode
    sb_config.devtools = devtools
    sb_config.mobile_emulator = is_mobile
    sb_config.device_metrics = device_metrics
    sb_config.extension_zip = extension_zip
    sb_config.extension_dir = extension_dir
    sb_config.database_env = "test"
    sb_config.log_path = constants.Logs.LATEST
    sb_config.archive_logs = archive_logs
    sb_config.disable_csp = disable_csp
    sb_config.disable_ws = disable_ws
    sb_config.enable_ws = enable_ws
    sb_config.enable_sync = enable_sync
    sb_config.use_auto_ext = use_auto_ext
    sb_config.undetectable = undetectable
    sb_config.uc_cdp_events = uc_cdp_events
    sb_config.uc_subprocess = uc_subprocess
    sb_config.log_cdp_events = log_cdp_events
    sb_config.no_sandbox = None
    sb_config.disable_gpu = None
    sb_config.disable_cookies = disable_cookies
    sb_config.disable_js = disable_js
    sb_config._multithreaded = False
    sb_config.reuse_session = False
    sb_config.crumbs = False
    sb_config.final_debug = False
    sb_config.visual_baseline = False
    sb_config.window_position = window_position
    sb_config.window_size = window_size
    sb_config.maximize_option = maximize_option
    sb_config._disable_beforeunload = _disable_beforeunload
    sb_config.save_screenshot = save_screenshot
    sb_config.no_screenshot = no_screenshot
    sb_config.binary_location = binary_location
    sb_config.driver_version = driver_version
    sb_config.page_load_strategy = page_load_strategy
    sb_config.timeout_multiplier = timeout_multiplier
    sb_config.pytest_html_report = None
    sb_config.with_db_reporting = False
    sb_config.with_s3_logging = False
    sb_config.js_checking_on = js_checking_on
    sb_config.recorder_mode = recorder_mode
    sb_config.recorder_ext = recorder_ext
    sb_config.record_sleep = record_sleep
    sb_config.rec_behave = rec_behave
    sb_config.rec_print = rec_print
    sb_config.report_on = False
    sb_config.slow_mode = slow_mode
    sb_config.demo_mode = demo_mode
    sb_config._time_limit = time_limit
    sb_config.demo_sleep = demo_sleep
    sb_config.dashboard = False
    sb_config._dashboard_initialized = False
    sb_config.message_duration = message_duration
    sb_config.host_resolver_rules = host_resolver_rules
    sb_config.block_images = block_images
    sb_config.do_not_track = do_not_track
    sb_config.use_wire = use_wire
    sb_config.external_pdf = external_pdf
    sb_config.remote_debug = remote_debug
    sb_config.settings_file = settings_file
    sb_config.user_data_dir = user_data_dir
    sb_config.chromium_arg = chromium_arg
    sb_config.firefox_arg = firefox_arg
    sb_config.firefox_pref = firefox_pref
    sb_config.disable_features = disable_features
    sb_config.proxy_string = proxy_string
    sb_config.proxy_bypass_list = proxy_bypass_list
    sb_config.proxy_pac_url = proxy_pac_url
    sb_config.multi_proxy = multi_proxy
    sb_config.enable_3d_apis = enable_3d_apis
    sb_config.swiftshader = swiftshader
    sb_config.ad_block_on = ad_block_on
    sb_config.highlights = highlights
    sb_config.interval = interval
    sb_config.cap_file = cap_file
    sb_config.cap_string = cap_string

    sb = BaseCase()
    sb.with_testing_base = sb_config.with_testing_base
    sb.browser = sb_config.browser
    sb.is_behave = False
    sb.is_pytest = False
    sb.is_nosetest = False
    sb.is_context_manager = sb_config.is_context_manager
    sb.headless = sb_config.headless
    sb.headless1 = sb_config.headless1
    sb.headless2 = sb_config.headless2
    sb.headed = sb_config.headed
    sb.xvfb = sb_config.xvfb
    sb.xvfb_metrics = sb_config.xvfb_metrics
    sb.start_page = sb_config.start_page
    sb.locale_code = sb_config.locale_code
    sb.protocol = sb_config.protocol
    sb.servername = sb_config.servername
    sb.port = sb_config.port
    sb.data = sb_config.data
    sb.var1 = sb_config.var1
    sb.var2 = sb_config.var2
    sb.var3 = sb_config.var3
    sb.variables = sb_config.variables
    sb.account = sb_config.account
    sb.environment = sb_config.environment
    sb.env = sb_config.env
    sb.user_agent = sb_config.user_agent
    sb.incognito = sb_config.incognito
    sb.guest_mode = sb_config.guest_mode
    sb.dark_mode = sb_config.dark_mode
    sb.devtools = sb_config.devtools
    sb.binary_location = sb_config.binary_location
    sb.driver_version = sb_config.driver_version
    sb.mobile_emulator = sb_config.mobile_emulator
    sb.device_metrics = sb_config.device_metrics
    sb.extension_zip = sb_config.extension_zip
    sb.extension_dir = sb_config.extension_dir
    sb.database_env = sb_config.database_env
    sb.log_path = sb_config.log_path
    sb.archive_logs = sb_config.archive_logs
    sb.disable_csp = sb_config.disable_csp
    sb.disable_ws = sb_config.disable_ws
    sb.enable_ws = sb_config.enable_ws
    sb.enable_sync = sb_config.enable_sync
    sb.use_auto_ext = sb_config.use_auto_ext
    sb.undetectable = sb_config.undetectable
    sb.uc_cdp_events = sb_config.uc_cdp_events
    sb.uc_subprocess = sb_config.uc_subprocess
    sb.log_cdp_events = sb_config.log_cdp_events
    sb.no_sandbox = sb_config.no_sandbox
    sb.disable_gpu = sb_config.disable_gpu
    sb.disable_cookies = sb_config.disable_cookies
    sb.disable_js = sb_config.disable_js
    sb._multithreaded = sb_config._multithreaded
    sb._reuse_session = sb_config.reuse_session
    sb._crumbs = sb_config.crumbs
    sb._final_debug = sb_config.final_debug
    sb.visual_baseline = sb_config.visual_baseline
    sb.window_position = sb_config.window_position
    sb.window_size = sb_config.window_size
    sb.maximize_option = sb_config.maximize_option
    sb._disable_beforeunload = sb_config._disable_beforeunload
    sb.save_screenshot_after_test = sb_config.save_screenshot
    sb.no_screenshot_after_test = sb_config.no_screenshot
    sb.page_load_strategy = sb_config.page_load_strategy
    sb.timeout_multiplier = sb_config.timeout_multiplier
    sb.pytest_html_report = sb_config.pytest_html_report
    sb.with_db_reporting = sb_config.with_db_reporting
    sb.with_s3_logging = sb_config.with_s3_logging
    sb.js_checking_on = sb_config.js_checking_on
    sb.recorder_mode = sb_config.recorder_mode
    sb.recorder_ext = sb_config.recorder_ext
    sb.record_sleep = sb_config.record_sleep
    sb.rec_behave = sb_config.rec_behave
    sb.rec_print = sb_config.rec_print
    sb.report_on = sb_config.report_on
    sb.slow_mode = sb_config.slow_mode
    sb.demo_mode = sb_config.demo_mode
    sb.time_limit = sb_config._time_limit
    sb.demo_sleep = sb_config.demo_sleep
    sb.dashboard = sb_config.dashboard
    sb._dash_initialized = sb_config._dashboard_initialized
    sb.message_duration = sb_config.message_duration
    sb.host_resolver_rules = sb_config.host_resolver_rules
    sb.block_images = sb_config.block_images
    sb.do_not_track = sb_config.do_not_track
    sb.use_wire = sb_config.use_wire
    sb.external_pdf = sb_config.external_pdf
    sb.remote_debug = sb_config.remote_debug
    sb.settings_file = sb_config.settings_file
    sb.user_data_dir = sb_config.user_data_dir
    sb.chromium_arg = sb_config.chromium_arg
    sb.firefox_arg = sb_config.firefox_arg
    sb.firefox_pref = sb_config.firefox_pref
    sb.disable_features = sb_config.disable_features
    sb.proxy_string = sb_config.proxy_string
    sb.proxy_bypass_list = sb_config.proxy_bypass_list
    sb.proxy_pac_url = sb_config.proxy_pac_url
    sb.multi_proxy = sb_config.multi_proxy
    sb.enable_3d_apis = sb_config.enable_3d_apis
    sb._swiftshader = sb_config.swiftshader
    sb.ad_block_on = sb_config.ad_block_on
    sb.highlights = sb_config.highlights
    sb.interval = sb_config.interval
    sb.cap_file = sb_config.cap_file
    sb.cap_string = sb_config.cap_string
    sb._has_failure = False  # This may change
    if hasattr(sb_config, "headless_active"):
        sb.headless_active = sb_config.headless_active
    else:
        sb.headless_active = False
    test_name = None
    terminal_width = shared_utils.get_terminal_width()
    if test:
        c1 = colorama.Fore.GREEN
        b1 = colorama.Style.BRIGHT
        cr = colorama.Style.RESET_ALL
        stack_base = traceback.format_stack()[0].split(os.sep)[-1]
        test_name = stack_base.split(", in ")[0].replace('", line ', ":")
        test_name += ":SB"
        start_text = "=== {%s} starts ===" % test_name
        remaining_spaces = terminal_width - len(start_text)
        left_space = ""
        right_space = ""
        if remaining_spaces > 0:
            left_spaces = int(remaining_spaces / 2)
            left_space = left_spaces * "="
            right_spaces = remaining_spaces - left_spaces
            right_space = right_spaces * "="
        if not test_name.startswith("runpy.py:"):
            print("%s%s%s%s%s" % (b1, left_space, start_text, right_space, cr))
    if do_log_folder_setup:
        from seleniumbase.core import log_helper
        from seleniumbase.core import download_helper
        from seleniumbase.core import proxy_helper

        log_helper.log_folder_setup(constants.Logs.LATEST + os.sep)
        log_helper.clear_empty_logs()
        download_helper.reset_downloads_folder()
        if not sb_config.multi_proxy:
            proxy_helper.remove_proxy_zip_if_present()
    start_time = time.time()
    sb.setUp()
    test_passed = True  # This can change later
    teardown_exception = None
    if "--trace" in sys_argv:
        import pdb

        pdb.set_trace()  # Debug Mode
        # Type "s" and press [Enter] to step into "yield sb".
    try:
        yield sb
    except Exception as e:
        sb._has_failure = True
        exception = e
        test_passed = False
        if not test_name:
            raise
        else:
            the_traceback = traceback.format_exc().strip()
            try:
                p2 = the_traceback.split(', in ')[1].split('", line ')[0]
                filename = p2.split(os.sep)[-1]
                sb.cm_filename = filename
            except Exception:
                sb.cm_filename = None
        # Tests will raise an exception if raise_test_failure is True
    finally:
        if sb._has_failure and "--pdb" in sys_argv:
            sb_config._do_sb_post_mortem = True
        elif (
            "--final-debug" in sys_argv
            or "--final-trace" in sys_argv
            or "--fdebug" in sys_argv
            or "--ftrace" in sys_argv
        ):
            sb_config._do_sb_final_trace = True
        try:
            sb.tearDown()
        except Exception as t_e:
            teardown_exception = t_e
            print(traceback.format_exc().strip())
            if test and not test_passed:
                print("********** ERROR: The test AND the tearDown() FAILED!")
        end_time = time.time()
        run_time = end_time - start_time
        sb_config = sb_config_backup
        if test:
            sb_config._has_older_context = True
        if test_name:
            result = "passed"
            if test and not test_passed:
                result = "failed"
                c1 = colorama.Fore.RED
            end_text = (
                "=== {%s} %s in %.2fs ==="
                % (test_name, result, run_time)
            )
            remaining_spaces = terminal_width - len(end_text)
            end_text = (
                "=== %s%s{%s} %s%s%s in %.2fs ==="
                % (b1, c1, test_name, result, cr, c1, run_time)
            )
            left_space = ""
            right_space = ""
            if remaining_spaces > 0:
                left_spaces = int(remaining_spaces / 2)
                left_space = left_spaces * "="
                right_spaces = remaining_spaces - left_spaces
                right_space = right_spaces * "="
            if test and not test_passed:
                print(the_traceback)
            if not test_name.startswith("runpy.py:"):
                print(
                    "%s%s%s%s%s"
                    % (c1, left_space, end_text, right_space, cr)
                )
    if test and test_name and not test_passed and raise_test_failure:
        raise exception
    elif (
        teardown_exception
        and (
            not test
            or (test_passed and raise_test_failure)
        )
    ):
        raise teardown_exception
