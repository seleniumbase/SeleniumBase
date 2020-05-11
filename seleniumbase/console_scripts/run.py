"""
SeleniumBase console scripts runner

Usage:
seleniumbase [COMMAND] [PARAMETERS]

Examples:
seleniumbase install chromedriver
seleniumbase mkdir browser_tests
seleniumbase convert my_old_webdriver_unittest.py
seleniumbase translate my_first_test.py --zh -p
seleniumbase extract-objects my_first_test.py
seleniumbase inject-objects my_first_test.py
seleniumbase objectify my_first_test.py
seleniumbase revert-objects my_first_test.py
seleniumbase encrypt OR seleniumbase obfuscate
seleniumbase decrypt OR seleniumbase unobfuscate
seleniumbase download server
seleniumbase grid-hub start
seleniumbase grid-node start --hub=127.0.0.1
"""

import colorama
import sys
from seleniumbase.common import obfuscate
from seleniumbase.common import unobfuscate
from seleniumbase.console_scripts import logo_helper
from seleniumbase.console_scripts import objectify
from seleniumbase.console_scripts import sb_mkdir
from seleniumbase.console_scripts import sb_install
from seleniumbase.utilities.selenium_grid import download_selenium_server
from seleniumbase.utilities.selenium_grid import grid_hub
from seleniumbase.utilities.selenium_grid import grid_node
from seleniumbase.utilities.selenium_ide import convert_ide


def show_usage():
    show_basic_usage()
    sc = ("")
    sc += ('Type "seleniumbase --help" for details on all commands.\n')
    sc += ('Type "seleniumbase help [COMMAND]" for specific command info.\n')
    sc += ('* (Use "pytest" for running tests) *\n')
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c4 = colorama.Fore.MAGENTA + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = sc.replace("seleniumbase", c1 + "selenium" + c2 + "base" + cr)
    sc = sc.replace("pytest", c3 + "pytest" + cr)
    sc = sc.replace("--help", c4 + "--help" + cr)
    sc = sc.replace("help", c4 + "help" + cr)
    print(sc)


def show_basic_usage():
    seleniumbase_logo = logo_helper.get_seleniumbase_logo()
    print(seleniumbase_logo)
    print("%s" % get_version()[0:1])
    print("")
    sc = ("\n")
    sc += ('Usage: "seleniumbase [COMMAND] [PARAMETERS]"\n')
    sc += ("Commands:\n")
    sc += ("       install [DRIVER_NAME] [OPTIONS]\n")
    sc += ("       mkdir [NEW_TEST_DIRECTORY_NAME]\n")
    sc += ("       convert [PYTHON_WEBDRIVER_UNITTEST_FILE]\n")
    sc += ("       translate [SB_PYTHON_FILE] [LANGUAGE] [ACTION]\n")
    sc += ("       extract-objects [SB_PYTHON_FILE]\n")
    sc += ("       inject-objects [SB_PYTHON_FILE] [OPTIONS]\n")
    sc += ("       objectify [SB_PYTHON_FILE] [OPTIONS]\n")
    sc += ("       revert-objects [SB_PYTHON_FILE]\n")
    sc += ("       encrypt  (OR: obfuscate)\n")
    sc += ("       decrypt  (OR: unobfuscate)\n")
    sc += ("       download server  (The Selenium Server JAR file)\n")
    sc += ("       grid-hub [start|stop] [OPTIONS]\n")
    sc += ("       grid-node [start|stop] --hub=[HUB_IP] [OPTIONS]\n")
    sc += ('  * (EXAMPLE: "seleniumbase install chromedriver latest") *\n')
    sc += ("")
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    cr = colorama.Style.RESET_ALL
    sc = sc.replace("seleniumbase", c1 + "selenium" + c2 + "base" + cr)
    print(sc)


def show_install_usage():
    print("  ** install **")
    print("")
    print("  Usage:")
    print("           seleniumbase install [DRIVER_NAME] [OPTIONS]")
    print("                 (Drivers: chromedriver, geckodriver, edgedriver")
    print("                           iedriver, operadriver)")
    print("  Options:")
    print("           VERSION         Specify the version.")
    print("                           (Default Chromedriver version = 2.44)")
    print('                           Use "latest" for the latest version.')
    print("           -p OR --path    Also copy the driver to /usr/local/bin")
    print("  Example:")
    print("           seleniumbase install chromedriver")
    print("           seleniumbase install geckodriver")
    print("           seleniumbase install chromedriver 76.0.3809.126")
    print("           seleniumbase install chromedriver latest")
    print("           seleniumbase install chromedriver -p")
    print("           seleniumbase install chromedriver latest -p")
    print("  Output:")
    print("           Installs the chosen webdriver to seleniumbase/drivers/")
    print("           (chromedriver is required for Chrome automation)")
    print("           (geckodriver is required for Firefox automation)")
    print("           (edgedriver is required for Microsoft Edge automation)")
    print("           (iedriver is required for InternetExplorer automation)")
    print("           (operadriver is required for Opera Browser automation)")
    print("")


def show_mkdir_usage():
    print("  ** mkdir **")
    print("")
    print("  Usage:")
    print("           seleniumbase mkdir [DIRECTORY_NAME]")
    print("  Example:")
    print("           seleniumbase mkdir browser_tests")
    print("  Output:")
    print("           Creates a new folder for running SeleniumBase scripts.")
    print("           The new folder contains default config files,")
    print("           sample tests for helping new users get started, and")
    print("           Python boilerplates for setting up customized")
    print("           test frameworks.")
    print("")


def show_convert_usage():
    print("  ** convert **")
    print("")
    print("  Usage:")
    print("           seleniumbase convert [PYTHON_WEBDRIVER_UNITTEST_FILE]")
    print("  Output:")
    print("           Converts a Selenium IDE exported WebDriver unittest")
    print("           file into a SeleniumBase file. Adds _SB to the new")
    print("           file name while keeping the original file intact.")
    print("           Works with Katalon Recorder scripts.")
    print("           See: http://www.katalon.com/automation-recorder")
    print("")


def show_translate_usage():
    print("  ** translate **")
    print("  Usage:")
    print("         seleniumbase translate [SB_FILE].py [LANGUAGE] [ACTION]")
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
    print("  Output:")
    print("         Translates a SeleniumBase Python file into the language")
    print('         specified. Method calls and "import" lines get swapped.')
    print("         Both a language and an action must be specified.")
    print('         The "-p" action can be paired with one other action.')
    print('         When running with "-c" (or "--copy"), the new file name')
    print('         will be the orginal name appended with an underscore')
    print("         plus the 2-letter language code of the new language.")
    print('         (Example: Translating "test_1.py" into Japanese with')
    print('          "-c" will create a new file called "test_1_ja.py".)')
    print("")


def show_extract_objects_usage():
    print("  ** extract-objects **")
    print("")
    print("  Usage:")
    print("           seleniumbase extract-objects [SELENIUMBASE_PYTHON_FILE]")
    print("  Output:")
    print("           Creates page objects based on selectors found in a")
    print("           seleniumbase Python file and saves those objects to the")
    print('           "page_objects.py" file in the same folder as the tests.')
    print("")


def show_inject_objects_usage():
    print("  ** inject-objects **")
    print("")
    print("  Usage:")
    print("           seleniumbase inject-objects [SELENIUMBASE_PYTHON_FILE]")
    print("  Options:")
    print("           -c, --comments  (Add object selectors to the comments.)")
    print("                           (Default: No added comments.)")
    print("  Output:")
    print('           Takes the page objects found in the "page_objects.py"')
    print('           file and uses those to replace matching selectors in')
    print('           the selected seleniumbase Python file.')
    print("")


def show_objectify_usage():
    print("  ** objectify **")
    print("")
    print("  Usage:")
    print("           seleniumbase objectify [SELENIUMBASE_PYTHON_FILE]")
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
    print("  ** revert-objects **")
    print("")
    print("  Usage:")
    print("           seleniumbase revert-objects [SELENIUMBASE_PYTHON_FILE]")
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
    print("  ** encrypt OR obfuscate **")
    print("")
    print("  Usage:")
    print("           seleniumbase encrypt")
    print("                        OR")
    print("           seleniumbase obfuscate")
    print("  Output:")
    print("           Runs the password obfuscation tool.")
    print("           (Where you can enter a password to encrypt/obfuscate.)")
    print("")


def show_decrypt_usage():
    print("  ** decrypt OR unobfuscate **")
    print("")
    print("  Usage:")
    print("           seleniumbase decrypt")
    print("                        OR")
    print("           seleniumbase unobfuscate")
    print("  Output:")
    print("           Runs the password decryption/unobfuscation tool.")
    print("           (Where you can enter an encrypted password to decrypt.)")
    print("")


def show_download_usage():
    print("  ** download **")
    print("")
    print("  Usage:")
    print("           seleniumbase download server")
    print("  Output:")
    print("           Downloads the Selenium Standalone Server.")
    print("           (Server is required for using your own Selenium Grid.)")
    print("")


def show_grid_hub_usage():
    print("  ** grid-hub **")
    print("")
    print("  Usage:")
    print("           seleniumbase grid-hub {start|stop}")
    print("  Options:")
    print("           -v, --verbose  (Increase verbosity of logging output.)")
    print("                          (Default: Quiet logging / not verbose.)")
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
    print("  ** grid-node **")
    print("")
    print("  Usage:")
    print("           seleniumbase grid-node {start|stop} [OPTIONS]")
    print("  Options:")
    print("           --hub=[HUB_IP] (The Grid Hub IP Address to connect to.)")
    print("                          (Default: 127.0.0.1 if not set)")
    print("           -v, --verbose  (Increase verbosity of logging output.)")
    print("                          (Default: Quiet logging / not verbose.)")
    print("  Example:")
    print("           seleniumbase grid-node start --hub=127.0.0.1")
    print("  Output:")
    print("           Controls the Selenium Grid node, which serves as a")
    print("           worker machine for your Selenium Grid Hub server.")
    print('           You can "start" or "stop" the Grid node.')
    print("")


def get_version():
    import pkg_resources
    version_info = None
    try:
        version_info = pkg_resources.require("seleniumbase")[0:1]
    except Exception:
        version_info = ["ERROR: Cannot detect version! Please reinstall!"]
    return version_info


def show_version_info():
    version = get_version()
    print('\n%s\n' % version)


def show_detailed_help():
    show_basic_usage()
    print("More Info:")
    print("")
    show_install_usage()
    show_mkdir_usage()
    show_convert_usage()
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
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
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
            sb_install.main()
        else:
            show_basic_usage()
            show_install_usage()
    elif command == "mkdir":
        if len(command_args) >= 1:
            sb_mkdir.main()
        else:
            show_basic_usage()
            show_mkdir_usage()
    elif command == "convert":
        if len(command_args) == 1:
            convert_ide.main()
        else:
            show_basic_usage()
            show_convert_usage()
    elif command == "translate":
        if len(command_args) >= 1:
            from seleniumbase.translate import translator
            translator.main()
        else:
            show_basic_usage()
            show_translate_usage()
    elif command == "extract-objects" or command == "extract_objects":
        if len(command_args) >= 1:
            objectify.extract_objects()
        else:
            show_basic_usage()
            show_extract_objects_usage()
    elif command == "inject-objects" or command == "inject_objects":
        if len(command_args) >= 1:
            objectify.inject_objects()
        else:
            show_basic_usage()
            show_inject_objects_usage()
    elif command == "objectify":
        if len(command_args) >= 1:
            objectify.objectify()
        else:
            show_basic_usage()
            show_objectify_usage()
    elif command == "revert-objects" or command == "revert_objects":
        if len(command_args) >= 1:
            objectify.revert_objects()
        else:
            show_basic_usage()
            show_revert_objects_usage()
    elif command == "encrypt" or command == "obfuscate":
        if len(command_args) >= 0:
            obfuscate.main()
        else:
            show_basic_usage()
            show_encrypt_usage()
    elif command == "decrypt" or command == "unobfuscate":
        if len(command_args) >= 0:
            unobfuscate.main()
        else:
            show_basic_usage()
            show_decrypt_usage()
    elif command == "download":
        if len(command_args) >= 1 and command_args[0].lower() == "server":
            download_selenium_server.main(force_download=True)
        else:
            show_basic_usage()
            show_download_usage()
    elif command == "grid-hub" or command == "grid_hub":
        if len(command_args) >= 1:
            grid_hub.main()
        else:
            show_basic_usage()
            show_grid_hub_usage()
    elif command == "grid-node" or command == "grid_node":
        if len(command_args) >= 1:
            grid_node.main()
        else:
            show_basic_usage()
            show_grid_node_usage()
    elif command == "version" or command == "--version":
        if len(command_args) == 0:
            show_version_info()
        else:
            show_basic_usage()
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
            elif command_args[0] == "convert":
                print("")
                show_convert_usage()
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
