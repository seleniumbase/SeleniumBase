"""
SeleniumBase console scripts runner

Usage:
seleniumbase [COMMAND] [PARAMETERS]

Examples:
seleniumbase install chromedriver
seleniumbase mkdir browser_tests
seleniumbase convert my_old_webdriver_unittest.py
seleniumbase grid-hub start
seleniumbase grid-node start --hub=127.0.0.1
"""

import sys
from seleniumbase.console_scripts import sb_mkdir
from seleniumbase.console_scripts import sb_install
from seleniumbase.utilities.selenium_grid import grid_hub
from seleniumbase.utilities.selenium_grid import grid_node
from seleniumbase.utilities.selenium_ide import convert_ide


def show_usage():
    show_basic_usage()
    print('Type "seleniumbase help" for details on all commands. OR,')
    print('Type "seleniumbase help [COMMAND]" for specific command info.\n')


def show_basic_usage():
    print("")
    print(">>>>>>>>>>>>")
    print("")
    print('Usage: "seleniumbase [command] [parameters]"')
    print("")
    print("Commands:")
    print("")
    print("    install [DRIVER_NAME]")
    print("    mkdir [NEW_TEST_DIRECTORY_NAME]")
    print("    convert [PYTHON_WEBDRIVER_UNITTEST_FILE]")
    print("    grid-hub {start|stop|restart} [OPTIONS]")
    print("    grid-node {start|stop|restart} --hub=[HUB_IP] [OPTIONS]")
    print("")


def show_install_usage():
    print("  ** install **")
    print("")
    print("  Usage:")
    print("            seleniumbase install [DRIVER_NAME]")
    print("                  (Drivers: chromedriver, geckodriver, edgedriver")
    print("                            iedriver, operadriver)")
    print("  Example:")
    print("            seleniumbase install chromedriver")
    print("  Output:")
    print("            Installs the specified webdriver.")
    print("            (chromedriver is required for Chrome automation)")
    print("            (geckodriver is required for Firefox automation)")
    print("            (edgedriver is required for Microsoft Edge automation)")
    print("            (iedriver is required for InternetExplorer automation)")
    print("            (operadriver is required for Opera Browser automation)")
    print("")


def show_mkdir_usage():
    print("  ** mkdir **")
    print("")
    print("  Usage:")
    print("            seleniumbase mkdir [DIRECTORY_NAME]")
    print("  Example:")
    print("            seleniumbase mkdir browser_tests")
    print("  Output:")
    print("            Creates a new folder for running SeleniumBase scripts.")
    print("            The new folder contains default config files,")
    print("            sample tests for helping new users get started, and")
    print("            Python boilerplates for setting up customized")
    print("            test frameworks.")
    print("")


def show_convert_usage():
    print("  ** convert **")
    print("")
    print("  Usage:")
    print("            seleniumbase convert [PYTHON_WEBDRIVER_UNITTEST_FILE]")
    print("  Output:")
    print("            Converts a Selenium IDE exported WebDriver unittest")
    print("            file into a SeleniumBase file. Adds _SB to the new")
    print("            file name while keeping the original file intact.")
    print("            Works with Katalon Recorder scripts.")
    print("            See: http://www.katalon.com/automation-recorder")
    print("")


def show_grid_hub_usage():
    print("  ** grid-hub **")
    print("")
    print("  Usage:")
    print("            seleniumbase grid-hub {start|stop|restart}")
    print("  Options:")
    print("            -v, --verbose  (Increase verbosity of logging output.)")
    print("                  (Default: Quiet logging / not verbose.)")
    print("  Output:")
    print("            Controls the Selenium Grid Hub Server, which allows")
    print("            for running tests on multiple machines in parallel")
    print("            to speed up test runs and reduce the total time")
    print("            of test suite execution.")
    print("            You can start, restart, or stop the Grid Hub server.")
    print("")


def show_grid_node_usage():
    print("  ** grid-node **")
    print("")
    print("  Usage:")
    print("            seleniumbase grid-node {start|stop|restart} [OPTIONS]")
    print("  Options:")
    print("            --hub=HUB_IP (The Grid Hub IP Address to connect to.)")
    print("                  (Default: 127.0.0.1 if not set)")
    print("            -v, --verbose  (Increase verbosity of logging output.)")
    print("                  (Default: Quiet logging / not verbose.)")
    print("  Output:")
    print("            Controls the Selenium Grid node, which serves as a")
    print("            worker machine for your Selenium Grid Hub server.")
    print("            You can start, restart, or stop the Grid node.")
    print("")


def show_detailed_help():
    show_basic_usage()
    print("More Info:")
    print("")
    show_install_usage()
    show_mkdir_usage()
    show_convert_usage()
    show_grid_hub_usage()
    show_grid_node_usage()


def main():
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

    if command == "install":
        if len(command_args) >= 1:
            sb_install.main()
        else:
            show_basic_usage()
            show_install_usage()
    elif command == "convert":
        if len(command_args) == 1:
            convert_ide.main()
        else:
            show_basic_usage()
            show_convert_usage()
    elif command == "mkdir":
        if len(command_args) >= 1:
            sb_mkdir.main()
        else:
            show_basic_usage()
            show_mkdir_usage()
    elif command == "grid-hub":
        if len(command_args) >= 1:
            grid_hub.main()
        else:
            show_basic_usage()
            show_grid_hub_usage()
    elif command == "grid-node":
        if len(command_args) >= 1:
            grid_node.main()
        else:
            show_basic_usage()
            show_grid_node_usage()
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
