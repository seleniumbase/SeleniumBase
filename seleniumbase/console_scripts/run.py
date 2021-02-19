"""
SeleniumBase console scripts runner

Usage:
seleniumbase [COMMAND] [PARAMETERS]
  OR   sbase [COMMAND] [PARAMETERS]

Examples:
sbase install chromedriver
sbase methods
sbase options
sbase mkdir ui_tests
sbase mkfile new_test.py
sbase mkpres new_presentation.py
sbase convert webdriver_unittest_file.py
sbase print my_first_test.py -n
sbase translate my_first_test.py --zh -p
sbase extract-objects my_first_test.py
sbase inject-objects my_first_test.py
sbase objectify my_first_test.py
sbase revert-objects my_first_test.py
sbase encrypt
sbase decrypt
sbase download server
sbase grid-hub start
sbase grid-node start --hub=127.0.0.1
"""

import colorama
import sys
colorama.init(autoreset=True)


def show_usage():
    show_basic_usage()
    sc = ("")
    sc += ('    Type "sbase help [COMMAND]" for specific command info.\n')
    sc += ('    For info on all commands, type: "seleniumbase --help".\n')
    sc += (' * (Use "pytest" for running tests) *\n')
    if "linux" not in sys.platform:
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
        c4 = colorama.Fore.MAGENTA + colorama.Back.LIGHTYELLOW_EX
        cr = colorama.Style.RESET_ALL
        sc = sc.replace("seleniumbase", c1 + "selenium" + c2 + "base" + cr)
        sc = sc.replace("sbase", c1 + "s" + c2 + "base" + cr)
        sc = sc.replace("pytest", c3 + "pytest" + cr)
        sc = sc.replace("--help", c4 + "--help" + cr)
        sc = sc.replace("help", c4 + "help" + cr)
    print(sc)


def show_basic_usage():
    import time
    from seleniumbase.console_scripts import logo_helper
    seleniumbase_logo = logo_helper.get_seleniumbase_logo()
    print(seleniumbase_logo)
    print()
    time.sleep(0.16)  # Enough time to see the logo
    show_package_location()
    show_version_info()
    print()
    sc = ("")
    sc += (' * USAGE: "seleniumbase [COMMAND] [PARAMETERS]"\n')
    sc += (' *    OR:        "sbase [COMMAND] [PARAMETERS]"\n')
    sc += ("\n")
    sc += ("COMMANDS:\n")
    sc += ("      install         [DRIVER] [OPTIONS]\n")
    sc += ("      methods         (List common Python methods)\n")
    sc += ("      options         (List common pytest options)\n")
    sc += ("      mkdir           [DIRECTORY] [OPTIONS]\n")
    sc += ("      mkfile          [FILE.py] [OPTIONS]\n")
    sc += ("      mkpres          [FILE.py] [LANG]\n")
    sc += ("      print           [FILE] [OPTIONS]\n")
    sc += ("      translate       [SB_FILE.py] [LANG] [ACTION]\n")
    sc += ("      convert         [WEBDRIVER_UNITTEST_FILE.py]\n")
    sc += ("      extract-objects [SB_FILE.py]\n")
    sc += ("      inject-objects  [SB_FILE.py] [OPTIONS]\n")
    sc += ("      objectify       [SB_FILE.py] [OPTIONS]\n")
    sc += ("      revert-objects  [SB_FILE.py] [OPTIONS]\n")
    sc += ("      encrypt         (OR: obfuscate)\n")
    sc += ("      decrypt         (OR: unobfuscate)\n")
    sc += ("      download server (The Selenium Grid JAR file)\n")
    sc += ("      grid-hub        [start|stop] [OPTIONS]\n")
    sc += ("      grid-node       [start|stop] --hub=[HOST/IP]\n")
    sc += (' * (EXAMPLE: "sbase install chromedriver latest")  *\n')
    sc += ("")
    if "linux" not in sys.platform:
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        cr = colorama.Style.RESET_ALL
        sc = sc.replace("seleniumbase", c1 + "selenium" + c2 + "base" + cr)
        sc = sc.replace("sbase", c1 + "s" + c2 + "base" + cr)
    print(sc)


def show_install_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "install" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase install [DRIVER_NAME] [OPTIONS]")
    print("           OR:    sbase install [DRIVER_NAME] [OPTIONS]")
    print("                 (Drivers: chromedriver, geckodriver, edgedriver")
    print("                           iedriver, operadriver)")
    print("  Options:")
    print("           VERSION         Specify the version.")
    print("                           (Default Chromedriver version = 2.44)")
    print('                           Use "latest" for the latest version.')
    print("           -p OR --path    Also copy the driver to /usr/local/bin")
    print("  Example:")
    print("           sbase install chromedriver")
    print("           sbase install geckodriver")
    print("           sbase install edgedriver")
    print("           sbase install chromedriver 85")
    print("           sbase install chromedriver 85.0.4183.87")
    print("           sbase install chromedriver latest")
    print("           sbase install chromedriver -p")
    print("           sbase install chromedriver latest -p")
    print("           sbase install edgedriver 85.0.564.68")
    print("  Output:")
    print("           Installs the chosen webdriver to seleniumbase/drivers/")
    print("           (chromedriver is required for Chrome automation)")
    print("           (geckodriver is required for Firefox automation)")
    print("           (edgedriver is required for Microsoft Edge automation)")
    print("           (iedriver is required for InternetExplorer automation)")
    print("           (operadriver is required for Opera Browser automation)")
    print("")


def show_mkdir_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "mkdir" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase mkdir [DIRECTORY] [OPTIONS]")
    print("           OR:    sbase mkdir [DIRECTORY] [OPTIONS]")
    print("  Example:")
    print("           sbase mkdir ui_tests")
    print("  Options:")
    print("         -b / --basic  (Only config files. No tests added.)")
    print("  Output:")
    print("           Creates a new folder for running SBase scripts.")
    print("           The new folder contains default config files,")
    print("           sample tests for helping new users get started,")
    print("           and Python boilerplates for setting up customized")
    print("           test frameworks.")
    print("")


def show_mkfile_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "mkfile" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase mkfile [FILE.py] [OPTIONS]")
    print("           OR:    sbase mkfile [FILE.py] [OPTIONS]")
    print("  Example:")
    print("           sbase mkfile new_test.py")
    print("  Options:")
    print("          -b / --basic  (Basic boilerplate / single-line test)")
    print("  Language Options:")
    print("          --en / --English    |    --zh / --Chinese")
    print("          --nl / --Dutch      |    --fr / --French")
    print("          --it / --Italian    |    --ja / --Japanese")
    print("          --ko / --Korean     |    --pt / --Portuguese")
    print("          --ru / --Russian    |    --es / --Spanish")
    print("  Output:")
    print("          Creates a new SBase test file with boilerplate code.")
    print("          If the file already exists, an error is raised.")
    print("          By default, uses English mode and creates a")
    print("          boilerplate with the 5 most common SeleniumBase")
    print('          methods, which are "open", "type", "click",')
    print('          "assert_element", and "assert_text". If using the')
    print('          basic boilerplate option, only the "open" method')
    print('          is included.')
    print("")


def show_mkpres_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "mkpres" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase mkpres [FILE.py] [LANG]")
    print("           OR:    sbase mkpres [FILE.py] [LANG]")
    print("  Example:")
    print("           sbase mkpres new_presentation.py --en")
    print("  Language Options:")
    print("          --en / --English    |    --zh / --Chinese")
    print("          --nl / --Dutch      |    --fr / --French")
    print("          --it / --Italian    |    --ja / --Japanese")
    print("          --ko / --Korean     |    --pt / --Portuguese")
    print("          --ru / --Russian    |    --es / --Spanish")
    print("  Output:")
    print("          Creates a new presentation with 3 example slides.")
    print("          If the file already exists, an error is raised.")
    print("          By default, the slides are written in English.")
    print('          Slides use "serif" theme & "fade" transition.')
    print("          This code can be used as a base boilerplate.")
    print("")


def show_convert_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "convert" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase convert [WEBDRIVER_UNITTEST_FILE.py]")
    print("           OR:    sbase convert [WEBDRIVER_UNITTEST_FILE.py]")
    print("  Output:")
    print("           Converts a Selenium IDE exported WebDriver unittest")
    print("           file into a SeleniumBase file. Adds _SB to the new")
    print("           file name while keeping the original file intact.")
    print("           Works with Katalon Recorder scripts.")
    print("           See: http://www.katalon.com/automation-recorder")
    print("")


def show_print_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "print" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("         seleniumbase print [FILE] [OPTIONS]")
    print("         OR:    sbase print [FILE] [OPTIONS]")
    print("  Options:")
    print("         -n   (Add line Numbers to the rows)")
    print("  Output:")
    print("         Prints the code/text of any file")
    print("         with syntax-highlighting.")
    print("")


def show_translate_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "translate" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("         seleniumbase translate [SB_FILE.py] [LANG] [ACTION]")
    print("         OR:    sbase translate [SB_FILE.py] [LANG] [ACTION]")
    print("  Languages:")
    print("         --en / --English    |    --zh / --Chinese")
    print("         --nl / --Dutch      |    --fr / --French")
    print("         --it / --Italian    |    --ja / --Japanese")
    print("         --ko / --Korean     |    --pt / --Portuguese")
    print("         --ru / --Russian    |    --es / --Spanish")
    print("  Actions:")
    print("         -p / --print  (Print translation output to the screen)")
    print("         -o / --overwrite  (Overwrite the file being translated)")
    print("         -c / --copy  (Copy the translation to a new .py file)")
    print("  Options:")
    print("         -n  (include line Numbers when using the Print action)")
    print("  Output:")
    print("         Translates a SeleniumBase Python file into the language")
    print('         specified. Method calls and "import" lines get swapped.')
    print("         Both a language and an action must be specified.")
    print('         The "-p" action can be paired with one other action.')
    print('         When running with "-c" (or "--copy"), the new file name')
    print('         will be the original name appended with an underscore')
    print("         plus the 2-letter language code of the new language.")
    print('         (Example: Translating "test_1.py" into Japanese with')
    print('          "-c" will create a new file called "test_1_ja.py".)')
    print("")


def show_extract_objects_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "extract-objects" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase extract-objects [SB_FILE.py]")
    print("           OR:    sbase extract-objects [SB_FILE.py]")
    print("  Output:")
    print("           Creates page objects based on selectors found in a")
    print("           seleniumbase Python file and saves those objects to the")
    print('           "page_objects.py" file in the same folder as the tests.')
    print("")


def show_inject_objects_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "inject-objects" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase inject-objects [SB_FILE.py] [OPTIONS]")
    print("           OR:    sbase inject-objects [SB_FILE.py] [OPTIONS]")
    print("  Options:")
    print("           -c, --comments  (Add object selectors to the comments.)")
    print("                           (Default: No added comments.)")
    print("  Output:")
    print('           Takes the page objects found in the "page_objects.py"')
    print('           file and uses those to replace matching selectors in')
    print('           the selected seleniumbase Python file.')
    print("")


def show_objectify_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "objectify" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase objectify [SB_FILE.py] [OPTIONS]")
    print("           OR:    sbase objectify [SB_FILE.py] [OPTIONS]")
    print("  Options:")
    print("           -c, --comments  (Add object selectors to the comments.)")
    print("                           (Default: No added comments.)")
    print("  Output:")
    print('           A modified version of the file where the selectors')
    print('           have been replaced with variable names defined in')
    print('           "page_objects.py", supporting the Page Object Pattern.')
    print("")
    print('           (seleniumbase "objectify" has the same outcome as')
    print('            combining "extract-objects" with "inject-objects")')
    print("")


def show_revert_objects_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "revert-objects" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase revert-objects [SB_FILE.py] [OPTIONS]")
    print("           OR:    sbase revert-objects [SB_FILE.py] [OPTIONS]")
    print("  Options:")
    print("           -c, --comments  (Keep existing comments for the lines.)")
    print("                           (Default: No comments are kept.)")
    print("  Output:")
    print('           Reverts the changes made by "seleniumbase objectify" or')
    print('           "seleniumbase inject-objects" when run against a')
    print('           seleniumbase Python file. Objects will get replaced by')
    print('           selectors stored in the "page_objects.py" file.')
    print("")


def show_encrypt_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "encrypt OR obfuscate" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase encrypt   ||   seleniumbase obfuscate")
    print("                                --OR--")
    print("                  sbase encrypt   ||          sbase obfuscate")
    print("  Output:")
    print("           Runs the password encryption/obfuscation tool.")
    print("           (Where you can enter a password to encrypt/obfuscate.)")
    print("")


def show_decrypt_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "decrypt OR unobfuscate" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase decrypt   ||   seleniumbase unobfuscate")
    print("                                --OR--")
    print("                  sbase decrypt   ||          sbase unobfuscate")
    print("  Output:")
    print("           Runs the password decryption/unobfuscation tool.")
    print("           (Where you can enter an encrypted password to decrypt.)")
    print("")


def show_download_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "download" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase download server")
    print("           OR:    sbase download server")
    print("  Output:")
    print("           Downloads the Selenium Standalone Server.")
    print("           (Server is required for using your own Selenium Grid.)")
    print("")


def show_grid_hub_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "grid-hub" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase grid-hub {start|stop|restart} [OPTIONS]")
    print("           OR:    sbase grid-hub {start|stop|restart} [OPTIONS]")
    print("  Options:")
    print("           -v, --verbose  (Increase verbosity of logging output.)")
    print("                          (Default: Quiet logging / not verbose.)")
    print("           --timeout=TIMEOUT  (Close idle browser after TIMEOUT.)")
    print("                              (The default TIMEOUT: 230 seconds.)")
    print("                              (Use --timeout=0 to skip timeouts.)")
    print("  Example:")
    print("           seleniumbase grid-hub start")
    print("  Output:")
    print("           Controls the Selenium Grid Hub Server, which allows")
    print("           for running tests on multiple machines in parallel")
    print("           to speed up test runs and reduce the total time")
    print("           of test suite execution.")
    print('           You can "start" or "stop" the Grid Hub server.')
    print("")


def show_grid_node_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("  " + c2 + "** " + c3 + "grid-node" + c2 + " **" + cr)
    print(sc)
    print("")
    print("  Usage:")
    print("           seleniumbase grid-node {start|stop|restart} [OPTIONS]")
    print("           OR:    sbase grid-node {start|stop|restart} [OPTIONS]")
    print("  Options:")
    print("           --hub=[HOST/IP]  (The Grid Hub Hostname / IP Address.)")
    print("                                 (Default: 127.0.0.1 if not set.)")
    print("           -v, --verbose  (Increase verbosity of logging output.)")
    print("                          (Default: Quiet logging / Not verbose.)")
    print("  Example:")
    print("           seleniumbase grid-node start --hub=127.0.0.1")
    print("  Output:")
    print("           Controls the Selenium Grid node, which serves as a")
    print("           worker machine for your Selenium Grid Hub server.")
    print('           You can "start" or "stop" the Grid node.')
    print("")


def get_version_info():
    # from pkg_resources import get_distribution
    # version = get_distribution("seleniumbase").version
    from seleniumbase import __version__
    version_info = None
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sb_text = c1 + "selenium" + c2 + "base" + cr
    version_info = "%s %s%s%s" % (sb_text, c3, __version__, cr)
    return version_info


def show_version_info():
    version_info = get_version_info()
    print('%s' % version_info)


def get_package_location():
    # from pkg_resources import get_distribution
    # location = get_distribution("seleniumbase").location
    import os
    import seleniumbase
    location = os.path.dirname(os.path.realpath(seleniumbase.__file__))
    if location.endswith("seleniumbase"):
        location = location[0:-len("seleniumbase")]
    return location


def show_package_location():
    location = get_package_location()
    print("%s" % location)


def show_methods():
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c4 = colorama.Fore.MAGENTA + colorama.Back.LIGHTYELLOW_EX
    c5 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTGREEN_EX
    cr = colorama.Style.RESET_ALL
    sc = ("\n " + c2 + " ** " + c3 + " SeleniumBase Python Methods "
          "" + c2 + " ** " + cr)
    print(sc)
    print("")
    line = "Here are some common methods that come with SeleniumBase:"
    line = c1 + line + cr
    print(line)
    line = "(Some optional args are not shown here)"
    print(line)
    print("")
    sbm = ""
    sbm += ('*.open(url) => Navigate the browser window to the URL.\n')
    sbm += ('*.type(selector, text) => Update the field with the text.\n')
    sbm += ('*.click(selector) => Click the element with the selector.\n')
    sbm += ('*.click_link(link_text) => Click the link containing text.\n')
    sbm += ('*.go_back() => Navigate back to the previous URL.\n')
    sbm += ('*.select_option_by_text(dropdown_selector, option)\n')
    sbm += ('*.hover_and_click(hover_selector, click_selector)\n')
    sbm += ('*.drag_and_drop(drag_selector, drop_selector)\n')
    sbm += ('*.get_text(selector) => Get the text from the element.\n')
    sbm += ('*.get_current_url() => Get the URL of the current page.\n')
    sbm += ('*.get_page_source() => Get the HTML of the current page.\n')
    sbm += ('*.get_attribute(selector, attribute) => Get element attribute.\n')
    sbm += ('*.get_title() => Get the title of the current page.\n')
    sbm += ('*.switch_to_frame(frame) => Switch into the iframe container.\n')
    sbm += ('*.switch_to_default_content() => Leave the iframe container.\n')
    sbm += ('*.open_new_window() => Open a new window in the same browser.\n')
    sbm += ('*.switch_to_window(window) => Switch to the browser window.\n')
    sbm += ('*.switch_to_default_window() => Switch to the original window.\n')
    sbm += ('*.get_new_driver(OPTIONS) => Open a new driver with OPTIONS.\n')
    sbm += ('*.switch_to_driver(driver) => Switch to the browser driver.\n')
    sbm += ('*.switch_to_default_driver() => Switch to the original driver.\n')
    sbm += ('*.wait_for_element(selector) => Wait until element is visible.\n')
    sbm += ('*.is_element_visible(selector) => Return element visibility.\n')
    sbm += ('*.is_text_visible(text, selector) => Return text visibility.\n')
    sbm += ('*.sleep(seconds) => Do nothing for the given amount of time.\n')
    sbm += ('*.save_screenshot(name) => Save a screenshot in .png format.\n')
    sbm += ('*.assert_element(selector) => Verify the element is visible.\n')
    sbm += ('*.assert_text(text, selector) => Verify text in the element.\n')
    sbm += ('*.assert_title(title) => Verify the title of the web page.\n')
    sbm += ('*.assert_downloaded_file(file) => Verify file was downloaded.\n')
    sbm += ('*.assert_no_404_errors() => Verify there are no broken links.\n')
    sbm += ('*.assert_no_js_errors() => Verify there are no JS errors.\n')
    sbm = sbm.replace("*.", "self." + c1).replace('(', cr + '(')
    sbm = sbm.replace("self.", c2 + "self" + c5 + "." + cr)
    sbm = sbm.replace('(', c3 + '(' + c4)
    sbm = sbm.replace(')', c3 + ')' + cr)
    print(sbm)


def show_options():
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = ("\n " + c2 + " ** " + c3 + " pytest CLI Options " + c2 + " ** " + cr)
    print(sc)
    print("")
    line = "Here are some common pytest options to use with SeleniumBase:"
    line = c1 + line + cr
    print(line)
    line = '(Some options are Chromium-specific, e.g. "--guest --mobile")'
    print(line)
    op = "\n"
    op += '--browser=BROWSER  (The web browser to use. Default: "chrome".)\n'
    op += '--headless  (Run tests headlessly. Default mode on Linux OS.)\n'
    op += '--demo  (Slow down and visually see test actions as they occur.)\n'
    op += '--slow  (Slow down the automation. Faster than using Demo Mode.)\n'
    op += '--reuse-session / --rs  (Reuse browser session between tests.)\n'
    op += '--crumbs  (Delete all cookies between tests reusing a session.)\n'
    op += '--maximize  (Start tests with the web browser window maximized.)\n'
    op += "--dashboard  (Enable SeleniumBase's Dashboard at dashboard.html)\n"
    op += "--incognito  (Enable Chromium's Incognito mode.)\n"
    op += "--guest  (Enable Chromium's Guest mode.)\n"
    op += '-m=MARKER  (Run tests with the specified pytest marker.)\n'
    op += '-n=NUM  (Multithread the tests using that many threads.)\n'
    op += '-v  (Verbose mode. Prints the full names of each test run.)\n'
    op += '--html=report.html  (Create a detailed pytest-html report.)\n'
    op += '--collect-only / --co  (Only show discovered tests. No run.)\n'
    op += '--co -q  (Only show full names of discovered tests. No run.)\n'
    op += '--trace  (Enter Debug Mode immediately after starting any test.\n'
    op += '          n: Next line of method. s: Step through. c: Continue.)\n'
    op += '--pdb  (Enter Debug Mode if a test fails. h: Help. c: Continue.\n'
    op += '        where: Stacktrace location. u: Up stack. d: Down stack.\n'
    op += '        longlist / ll: See code. dir(): List namespace objects.)\n'
    op += '-x  (Stop running the tests after the first failure is reached.)\n'
    op += '--archive-logs  (Archive old log files instead of deleting them.)\n'
    op += '--save-screenshot  (Save a screenshot at the end of each test.)\n'
    op += '--check-js  (Check for JavaScript errors after page loads.)\n'
    op += '--start-page=URL  (The browser start page when tests begin.)\n'
    op += "--agent=STRING  (Modify the web browser's User-Agent string.)\n"
    op += "--mobile  (Use Chromium's mobile device emulator during tests.)\n"
    op += '--metrics=STRING  (Set mobile "CSSWidth,CSSHeight,PixelRatio".)\n'
    op += '--ad-block  (Block some types of display ads after page loads.)\n'
    op += '--settings-file=FILE  (Override default SeleniumBase settings.)\n'
    op += '--env=ENV  (Set the test env. Access with "self.env" in tests.)\n'
    op += '--data=DATA  (Extra test data. Access with "self.data" in tests.)\n'
    op += '--disable-csp  (Disable the Content Security Policy of websites.)\n'
    op += '--server=SERVER  (The Selenium Grid server/IP used for tests.)\n'
    op += '--port=PORT  (The Selenium Grid port used by the test server.)\n'
    op += '--proxy=SERVER:PORT  (Connect to a proxy server:port for tests.)\n'
    op += '--proxy=USER:PASS@SERVER:PORT  (Use authenticated proxy server.)\n'
    op += cr
    op = op.replace("\n-", "\n" + c1 + "-").replace('  (', cr + '  (')
    op = op.replace(" / -", cr + " / " + c1 + "-")
    op = op.replace("=", c2 + "=" + c3)
    print(op)
    line = 'For the full list of ' + c2 + 'command-line options' + cr
    line += ', type: "' + c3 + 'pytest' + cr + ' ' + c1 + '--help' + cr + '".'
    print(line)
    print("")


def show_detailed_help():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c6 = colorama.Back.CYAN
    cr = colorama.Style.RESET_ALL
    show_basic_usage()
    print(c6 + "            " + c2 + "  Commands:  " + c6 + "            ")
    print(cr)
    show_install_usage()
    show_mkdir_usage()
    show_mkfile_usage()
    show_mkpres_usage()
    show_convert_usage()
    show_print_usage()
    show_translate_usage()
    show_extract_objects_usage()
    show_inject_objects_usage()
    show_objectify_usage()
    show_revert_objects_usage()
    show_encrypt_usage()
    show_decrypt_usage()
    show_download_usage()
    show_grid_hub_usage()
    show_grid_node_usage()
    print('* (Use "' + c3 + 'pytest' + cr + '" for running tests) *\n')


def main():
    command = None
    command_args = None
    num_args = len(sys.argv)
    if num_args == 1:
        show_usage()
        return
    elif num_args == 2:
        command = sys.argv[1]
        command_args = []
    elif num_args > 2:
        command = sys.argv[1]
        command_args = sys.argv[2:]
    command = command.lower()

    if command == "install":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import sb_install
            sb_install.main()
        else:
            show_basic_usage()
            show_install_usage()
    elif command == "mkdir":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import sb_mkdir
            sb_mkdir.main()
        else:
            show_basic_usage()
            show_mkdir_usage()
    elif command == "mkfile":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import sb_mkfile
            sb_mkfile.main()
        else:
            show_basic_usage()
            show_mkfile_usage()
    elif command == "mkpres":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import sb_mkpres
            sb_mkpres.main()
        else:
            show_basic_usage()
            show_mkpres_usage()
    elif command == "convert":
        if len(command_args) == 1:
            from seleniumbase.utilities.selenium_ide import convert_ide
            convert_ide.main()
        else:
            show_basic_usage()
            show_convert_usage()
    elif command == "print":
        if len(command_args) >= 1:
            if sys.version_info[0] == 2:
                c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
                cr = colorama.Style.RESET_ALL
                msg = '"sbase print" does NOT support Python 2! '
                msg += 'Try using the Unix "cat" command instead!'
                message = "\n" + c5 + msg + cr + "\n"
                print("")
                raise Exception(message)
            from seleniumbase.console_scripts import sb_print
            sb_print.main()
        else:
            show_basic_usage()
            show_print_usage()
    elif command == "translate":
        if len(command_args) >= 1:
            if sys.version_info[0] == 2:
                c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
                cr = colorama.Style.RESET_ALL
                msg = "The SeleniumBase Translator does NOT support Python 2!"
                message = "\n" + c5 + msg + cr + "\n"
                print("")
                raise Exception(message)
            from seleniumbase.translate import translator
            translator.main()
        else:
            show_basic_usage()
            show_translate_usage()
    elif command == "extract-objects" or command == "extract_objects":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import objectify
            objectify.extract_objects()
        else:
            show_basic_usage()
            show_extract_objects_usage()
    elif command == "inject-objects" or command == "inject_objects":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import objectify
            objectify.inject_objects()
        else:
            show_basic_usage()
            show_inject_objects_usage()
    elif command == "objectify":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import objectify
            objectify.objectify()
        else:
            show_basic_usage()
            show_objectify_usage()
    elif command == "revert-objects" or command == "revert_objects":
        if len(command_args) >= 1:
            from seleniumbase.console_scripts import objectify
            objectify.revert_objects()
        else:
            show_basic_usage()
            show_revert_objects_usage()
    elif command == "encrypt" or command == "obfuscate":
        if len(command_args) >= 0:
            from seleniumbase.common import obfuscate
            obfuscate.main()
        else:
            show_basic_usage()
            show_encrypt_usage()
    elif command == "decrypt" or command == "unobfuscate":
        if len(command_args) >= 0:
            from seleniumbase.common import unobfuscate
            unobfuscate.main()
        else:
            show_basic_usage()
            show_decrypt_usage()
    elif command == "download":
        if len(command_args) >= 1 and command_args[0].lower() == "server":
            from seleniumbase.utilities.selenium_grid import (
                download_selenium_server)
            download_selenium_server.main(force_download=True)
        else:
            show_basic_usage()
            show_download_usage()
    elif command == "grid-hub" or command == "grid_hub":
        if len(command_args) >= 1:
            from seleniumbase.utilities.selenium_grid import grid_hub
            grid_hub.main()
        else:
            show_basic_usage()
            show_grid_hub_usage()
    elif command == "grid-node" or command == "grid_node":
        if len(command_args) >= 1:
            from seleniumbase.utilities.selenium_grid import grid_node
            grid_node.main()
        else:
            show_basic_usage()
            show_grid_node_usage()
    elif command == "version" or command == "--version":
        if len(command_args) == 0:
            from seleniumbase.console_scripts import logo_helper
            seleniumbase_logo = logo_helper.get_seleniumbase_logo()
            print(seleniumbase_logo)
            print()
            show_package_location()
            show_version_info()
            print()
        else:
            show_basic_usage()
    elif command == "methods" or command == "--methods":
        show_methods()
    elif command == "options" or command == "--options":
        show_options()
    elif command == "help" or command == "--help":
        if len(command_args) >= 1:
            if command_args[0] == "install":
                print("")
                show_install_usage()
                return
            elif command_args[0] == "mkdir":
                print("")
                show_mkdir_usage()
                return
            elif command_args[0] == "mkfile":
                print("")
                show_mkfile_usage()
                return
            elif command_args[0] == "mkpres":
                print("")
                show_mkpres_usage()
                return
            elif command_args[0] == "convert":
                print("")
                show_convert_usage()
                return
            elif command_args[0] == "print":
                print("")
                show_print_usage()
                return
            elif command_args[0] == "translate":
                print("")
                show_translate_usage()
                return
            elif command_args[0] == "extract-objects":
                print("")
                show_extract_objects_usage()
                return
            elif command_args[0] == "inject-objects":
                print("")
                show_inject_objects_usage()
                return
            elif command_args[0] == "objectify":
                print("")
                show_objectify_usage()
                return
            elif command_args[0] == "revert-objects":
                print("")
                show_revert_objects_usage()
                return
            elif command_args[0] == "encrypt":
                print("")
                show_encrypt_usage()
                return
            elif command_args[0] == "obfuscate":
                print("")
                show_encrypt_usage()
                return
            elif command_args[0] == "decrypt":
                print("")
                show_decrypt_usage()
                return
            elif command_args[0] == "unobfuscate":
                print("")
                show_decrypt_usage()
                return
            elif command_args[0] == "download":
                print("")
                show_download_usage()
                return
            elif command_args[0] == "grid-hub":
                print("")
                show_grid_hub_usage()
                return
            elif command_args[0] == "grid-node":
                print("")
                show_grid_node_usage()
                return
        show_detailed_help()
    else:
        show_usage()


if __name__ == "__main__":
    main()
