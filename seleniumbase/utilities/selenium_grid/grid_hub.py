import codecs
import os
import subprocess
import sys


def invalid_run_command():
    exp = ("  ** grid-hub **\n\n")
    exp += "  Usage:\n"
    exp += "            seleniumbase grid-hub {start|stop|restart}\n"
    exp += "  Options:\n"
    exp += "        -v, --verbose  (Increase verbosity of logging output.)\n"
    exp += "              (Default: Quiet logging / not verbose.)\n"
    exp += "  Output:\n"
    exp += "            Controls the Selenium Grid Hub Server, which allows\n"
    exp += "            for running tests on multiple machines in parallel\n"
    exp += "            to speed up test runs and reduce the total time\n"
    exp += "            of test suite execution.\n"
    exp += "            You can start, restart, or stop the Grid Hub Server.\n"
    raise Exception('INVALID RUN COMMAND!\n\n%s' % exp)


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    num_args = len(sys.argv)
    if sys.argv[0].split('/')[-1] == "seleniumbase" or (
            sys.argv[0].split('\\')[-1] == "seleniumbase"):
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
            else:
                invalid_run_command()

    data = []
    data.append(verbose)
    file_path = "%s/%s" % (dir_path, "verbose_hub_server.dat")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    from seleniumbase.utilities.selenium_grid import download_selenium_server
    download_selenium_server.main()  # Nothing happens if already exists

    if "linux" in sys.platform or "darwin" in sys.platform:
        if grid_hub_command == "start":
            subprocess.check_call(dir_path + "/grid-hub start", shell=True)
        elif grid_hub_command == "restart":
            subprocess.check_call(dir_path + "/grid-hub restart", shell=True)
        elif grid_hub_command == "stop":
            subprocess.check_call(dir_path + "/grid-hub stop", shell=True)
        else:
            invalid_run_command()
    else:
        if grid_hub_command == "start" or grid_hub_command == "restart":
            shell_command = (
                """java -jar %s/selenium-server-standalone.jar -role hub """
                """-timeout 30 -browserTimeout 60 -port 4444""" % dir_path)
            print("\nStarting Selenium-WebDriver Grid Hub...\n")
            print(shell_command)
            print("")
            print("Grid Hub Console: http://127.0.0.1:4444/grid/console")
            print("")
            subprocess.check_call(shell_command, shell=True)
        elif grid_hub_command == "stop":
            print("")
            print("To stop the Grid Hub, use CTRL-C inside the server shell!")
            print("")
        else:
            invalid_run_command()


if __name__ == "__main__":
    main()
