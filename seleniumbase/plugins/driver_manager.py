"""
The SeleniumBase Driver as a Python Context Manager or a returnable object.
###########################################################################

The SeleniumBase Driver as a context manager:
Usage --> ``with DriverContext() as driver:``
Usage example -->
    from seleniumbase import Driver
    with DriverContext() as driver:
        driver.get("https://google.com/ncr")
    # The browser exits automatically after the "with" block ends.

###########################################################################
# Above: The driver as a context manager. (Used with a "with" statement.) #
# ----------------------------------------------------------------------- #
# Below: The driver as a returnable object. (Used with "return" command.) #
###########################################################################

The SeleniumBase Driver as a returnable object:
Usage --> ``driver = Driver()``
Usage example -->
    from seleniumbase import Driver
    driver = Driver()
    driver.get("https://google.com/ncr")

###########################################################################
"""
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
                    sys.platform not in ["win32", "win64", "x64"]
                    or self.driver.service.process
                )
            ):
                self.driver.quit()
        except Exception:
            pass
        return False


def Driver(
    browser=None,  # Choose from "chrome", "edge", "firefox", or "safari".
    headless=None,  # The original headless mode for Chromium and Firefox.
    headless2=None,  # Chromium's new headless mode. (Has more features)
    headed=None,  # Run tests in headed/GUI mode on Linux, where not default.
    locale_code=None,  # Set the Language Locale Code for the web browser.
    protocol=None,  # The Selenium Grid protocol: "http" or "https".
    servername=None,  # The Selenium Grid server/IP used for tests.
    port=None,  # The Selenium Grid port used by the test server.
    proxy=None,  # Use proxy. Format: "SERVER:PORT" or "USER:PASS@SERVER:PORT".
    proxy_bypass_list=None,  # Skip proxy when using the listed domains.
    proxy_pac_url=None,  # Use PAC file. (Format: URL or USERNAME:PASSWORD@URL)
    agent=None,  # Modify the web browser's User-Agent string.
    cap_file=None,  # The desired capabilities to use with a Selenium Grid.
    cap_string=None,  # The desired capabilities to use with a Selenium Grid.
    recorder_ext=None,  # Enables the SeleniumBase Recorder Chromium extension.
    disable_js=None,  # Disable JavaScript on websites. Pages might break!
    disable_csp=None,  # Disable the Content Security Policy of websites.
    enable_ws=None,  # Enable Web Security on Chromium-based browsers.
    disable_ws=None,  # Reverse of "enable_ws". (None and False are different)
    enable_sync=None,  # Enable "Chrome Sync" on websites.
    use_auto_ext=None,  # Use Chrome's automation extension.
    undetectable=None,  # Use undetected-chromedriver to evade bot-detection.
    uc_subprocess=None,  # Use undetected-chromedriver as a subprocess.
    no_sandbox=None,  # (DEPRECATED) - "--no-sandbox" is always used now.
    disable_gpu=None,  # (DEPRECATED) - GPU is disabled if no "swiftshader".
    incognito=None,  # Enable Chromium's Incognito mode.
    guest_mode=None,  # Enable Chromium's Guest mode.
    devtools=None,  # Open Chromium's DevTools when the browser opens.
    remote_debug=None,  # Enable Chrome's Debugger on "http://localhost:9222".
    enable_3d_apis=None,  # Enable WebGL and 3D APIs.
    swiftshader=None,  # Use Chrome's "--use-gl=swiftshader" feature.
    ad_block_on=None,  # Block some types of display ads from loading.
    block_images=None,  # Block images from loading during tests.
    do_not_track=None,  # Tell websites that you don't want to be tracked.
    chromium_arg=None,  # "ARG=N,ARG2" (Set Chromium args, ","-separated.)
    firefox_arg=None,  # "ARG=N,ARG2" (Set Firefox args, comma-separated.)
    firefox_pref=None,  # SET (Set Firefox PREFERENCE:VALUE set, ","-separated)
    user_data_dir=None,  # Set the Chrome user data directory to use.
    extension_zip=None,  # Load a Chrome Extension .zip|.crx, comma-separated.)
    extension_dir=None,  # Load a Chrome Extension directory, comma-separated.)
    page_load_strategy=None,  # Set Chrome PLS to "normal", "eager", or "none".
    use_wire=None,  # Use selenium-wire's webdriver over selenium webdriver.
    external_pdf=None,  # Set Chrome "plugins.always_open_pdf_externally":True.
    is_mobile=None,  # Use the mobile device emulator while running tests.
    mobile=None,  # Shortcut / Duplicate of "is_mobile".
    d_width=None,  # Set device width
    d_height=None,  # Set device height
    d_p_r=None,  # Set device pixel ratio
    uc=None,  # Shortcut / Duplicate of "undetectable".
    undetected=None,  # Shortcut / Duplicate of "undetectable".
    uc_sub=None,  # Shortcut / Duplicate of "uc_subprocess".
    wire=None,  # Shortcut / Duplicate of "use_wire".
    pls=None,  # Shortcut / Duplicate of "page_load_strategy".
):
    from seleniumbase.fixtures import constants

    sys_argv = sys.argv
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
    if "--browser=opera" in sys_argv or "--browser opera" in sys_argv:
        browser_changes += 1
        browser_set = "opera"
        browser_list.append("--browser=opera")
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
    if "--opera" in sys_argv and not browser_set == "opera":
        browser_changes += 1
        browser_text = "opera"
        browser_list.append("--opera")
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
    if headless2 is None:
        if "--headless2" in sys_argv:
            headless2 = True
        else:
            headless2 = False
    if protocol is None:
        protocol = "http"  # For the Selenium Grid only!
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
    if guest_mode is None:
        if "--guest" in sys_argv:
            guest_mode = True
        else:
            guest_mode = False
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
        "linux" in sys.platform
        and not headed
        and not headless
        and not headless2
    ):
        headless = True
    if recorder_mode and headless:
        headless = False
        headless2 = True
    if headless2 and browser == "firefox":
        headless2 = False  # Only for Chromium browsers
        headless = True  # Firefox has regular headless
    elif browser not in ["chrome", "edge"]:
        headless2 = False  # Only for Chromium browsers
    if disable_csp is None:
        disable_csp = False
    if (
        (enable_ws is None and disable_ws is None)
        or (disable_ws is not None and not disable_ws)
        or (enable_ws is not None and enable_ws)
    ):
        enable_ws = True
    else:
        enable_ws = False
    if undetectable or undetected or uc or uc_subprocess or uc_sub:
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
    if undetectable and is_mobile:
        is_mobile = False
        user_agent = None
    if use_auto_ext is None:
        if "--use-auto-ext" in sys_argv:
            use_auto_ext = True
        else:
            use_auto_ext = False
    if disable_js is None:
        if "--disable-js" in sys_argv:
            disable_js = True
        else:
            disable_js = False
    if pls is not None and page_load_strategy is None:
        page_load_strategy = pls
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
    if ad_block_on is None:
        if "--ad-block" in sys_argv or "--ad_block" in sys_argv:
            ad_block_on = True
        else:
            ad_block_on = False
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
        user_agent=user_agent,
        cap_file=cap_file,
        cap_string=cap_string,
        recorder_ext=recorder_ext,
        disable_js=disable_js,
        disable_csp=disable_csp,
        enable_ws=enable_ws,
        enable_sync=enable_sync,
        use_auto_ext=use_auto_ext,
        undetectable=undetectable,
        uc_subprocess=uc_subprocess,
        no_sandbox=no_sandbox,
        disable_gpu=disable_gpu,
        headless2=headless2,
        incognito=incognito,
        guest_mode=guest_mode,
        devtools=devtools,
        remote_debug=remote_debug,
        enable_3d_apis=enable_3d_apis,
        swiftshader=swiftshader,
        ad_block_on=ad_block_on,
        block_images=block_images,
        do_not_track=do_not_track,
        chromium_arg=chromium_arg,
        firefox_arg=firefox_arg,
        firefox_pref=firefox_pref,
        user_data_dir=user_data_dir,
        extension_zip=extension_zip,
        extension_dir=extension_dir,
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
