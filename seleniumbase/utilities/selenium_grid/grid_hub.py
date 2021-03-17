import codecs
import os
import subprocess
import sys
from seleniumbase import drivers  # webdriver storage folder for SeleniumBase
DRIVER_DIR = os.path.dirname(os.path.realpath(drivers.__file__))
# Make sure that the SeleniumBase DRIVER_DIR is at the top of the System PATH
# (Changes to the System PATH with os.environ only last during the test run)
if not os.environ["PATH"].startswith(DRIVER_DIR):
    # Remove existing SeleniumBase DRIVER_DIR from System PATH if present
    os.environ["PATH"] = os.environ["PATH"].replace(DRIVER_DIR, "")
    # If two path separators are next to each other, replace with just one
    os.environ["PATH"] = os.environ["PATH"].replace(
        os.pathsep + os.pathsep, os.pathsep)
    # Put the SeleniumBase DRIVER_DIR at the beginning of the System PATH
    os.environ["PATH"] = DRIVER_DIR + os.pathsep + os.environ["PATH"]


def invalid_run_command(msg=None):
    exp = ("  ** grid-hub **\n\n")
    exp += "  Usage:\n"
    exp += "        seleniumbase grid-hub {start|stop|restart} [OPTIONS]\n"
    exp += "  Options:\n"
    exp += "        -v, --verbose  (Increase verbosity of logging output.)\n"
    exp += "                       (Default: Quiet logging / not verbose.)\n"
    exp += "        --timeout=TIMEOUT  (Close idle browser after TIMEOUT.)\n"
    exp += "                           (The default TIMEOUT: 230 seconds.)\n"
    exp += "                           (Use --timeout=0 to skip timeouts.)\n"
    exp += "  Example:\n"
    exp += "        seleniumbase grid-hub start\n"
    exp += "  Output:\n"
    exp += "        Controls the Selenium Grid Hub Server, which allows\n"
    exp += "        for running tests on multiple machines in parallel\n"
    exp += "        to speed up test runs and reduce the total time\n"
    exp += "        of test suite execution.\n"
    exp += "        You can start, restart, or stop the Grid Hub Server.\n"
    if msg:
        exp += msg
    raise Exception('INVALID RUN COMMAND!\n\n%s' % exp)


def main():
    timeout = 230  # The default number of seconds that a test can be idle
    dir_path = os.path.dirname(os.path.realpath(__file__))
    num_args = len(sys.argv)
    if sys.argv[0].split('/')[-1] == "seleniumbase" or (
            sys.argv[0].split('\\')[-1] == "seleniumbase") or (
            sys.argv[0].split('/')[-1] == "sbase") or (
            sys.argv[0].split('\\')[-1] == "sbase"):
        if num_args < 3:
            invalid_run_command()
    else:
        invalid_run_command()
    grid_hub_command = sys.argv[2]
    if grid_hub_command not in ["start", "stop", "restart"]:
        invalid_run_command()

    verbose = "False"
    if num_args >= 4:
        options = sys.argv[3:]
        for option in options:
            if option == '-v' or option == '--verbose':
                verbose = "True"
            elif option.startswith("--timeout=") and len(option) > 10:
                timeout = option.split("--timeout=")[1]
                if not timeout.isdigit():
                    msg = '\n"timeout" must be a non-negative integer!\n'
                    print(msg)
                    invalid_run_command(msg)
            else:
                invalid_run_command()

    data = []
    data.append(verbose)
    file_path = "%s/%s" % (dir_path, "verbose_hub_server.dat")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    from seleniumbase.utilities.selenium_grid import download_selenium_server
    download_selenium_server.main(force_download=False)  # Only runs if needed

    if "linux" in sys.platform or "darwin" in sys.platform:
        if grid_hub_command == "start":
            subprocess.check_call(
                dir_path + "/grid-hub start %s" % timeout, shell=True)
        elif grid_hub_command == "restart":
            subprocess.check_call(dir_path + "/grid-hub stop .", shell=True)
            subprocess.check_call(
                dir_path + "/grid-hub start %s" % timeout, shell=True)
        elif grid_hub_command == "stop":
            subprocess.check_call(dir_path + "/grid-hub stop .", shell=True)
        else:
            invalid_run_command()
    else:
        if grid_hub_command == "start" or grid_hub_command == "restart":
            shell_command = (
                """java -jar %s/selenium-server-standalone.jar -role hub """
                """-timeout %s -browserTimeout 170 -port 4444"""
                "" % (dir_path, timeout))
            print("\nStarting Selenium-WebDriver Grid Hub...\n")
            print(shell_command)
            print("")
            print("Grid Hub Console: http://127.0.0.1:4444/grid/console")
            print("")
            subprocess.check_call(shell_command, shell=True)
        elif grid_hub_command == "stop":
            print("")
            print("To stop the Grid Hub, use CTRL+C inside the server shell!")
            print("")
        else:
            invalid_run_command()


if __name__ == "__main__":
    main()
