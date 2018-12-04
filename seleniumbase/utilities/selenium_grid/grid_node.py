import codecs
import os
import subprocess
import sys


def invalid_run_command():
    exp = ("  ** grid-node **\n\n")
    exp += "  Usage:\n"
    exp += "        seleniumbase grid-node {start|stop|restart} [OPTIONS]\n"
    exp += "  Options:\n"
    exp += "        --hub=[HUB_IP] (The Grid Hub IP Address to connect to.)\n"
    exp += "              (Default: 127.0.0.1 if not set)\n"
    exp += "        -v, --verbose  (Increase verbosity of logging output.)\n"
    exp += "              (Default: Quiet logging / not verbose.)\n"
    exp += "  Output:\n"
    exp += "        Controls the Selenium Grid Node, which serves as a\n"
    exp += "        worker machine for your Selenium Grid Hub Server.\n"
    exp += "        You can start, restart, or stop the Grid Node.\n"
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

    server_ip = "127.0.0.1"
    verbose = "False"
    if num_args >= 4:
        options = sys.argv[3:]
        for option in options:
            if option.startswith('--hub=') and (
                    len(option.split('--hub=')[1]) > 0):
                server_ip = option.split('--hub=')[1]
            elif option == '-v' or option == '--verbose':
                verbose = "True"
            else:
                invalid_run_command()

    data = []
    data.append(server_ip)
    file_path = "%s/%s" % (dir_path, "ip_of_grid_hub.dat")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append(verbose)
    file_path = "%s/%s" % (dir_path, "verbose_node_server.dat")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    from seleniumbase.utilities.selenium_grid import download_selenium_server
    download_selenium_server.main(force_download=False)  # Only runs if needed

    if "linux" in sys.platform or "darwin" in sys.platform:
        if grid_hub_command == "start":
            subprocess.check_call(dir_path + "/grid-node start", shell=True)
        elif grid_hub_command == "restart":
            subprocess.check_call(dir_path + "/grid-node restart", shell=True)
        elif grid_hub_command == "stop":
            subprocess.check_call(dir_path + "/grid-node stop", shell=True)
        else:
            invalid_run_command()
    else:
        if grid_hub_command == "start" or grid_hub_command == "restart":
            shell_command = (
                """java -jar %s/selenium-server-standalone.jar -role node """
                """-hub http://%s:4444/grid/register -browser browser"""
                """Name=chrome,maxInstances=5,version=ANY,seleniumProtocol="""
                """WebDriver -browser browserName=firefox,maxInstances=5,"""
                """version=ANY,seleniumProtocol=WebDriver -browser browser"""
                """Name=MicrosoftEdge,maxInstances=1,version=ANY,"""
                """platform=WIN10,seleniumProtocol=WebDriver"""
                % (dir_path, server_ip))
            print("\nStarting Selenium-WebDriver Grid node...\n")
            print(shell_command)
            print("")
            print("""Browser Sessions: http://127.0.0.1:5555"""
                  """/wd/hub/static/resource/hub.html""")
            print("")
            subprocess.check_call(shell_command, shell=True)
        elif grid_hub_command == "stop":
            print("")
            print("To stop the Grid node, use CTRL-C inside the server shell!")
            print("")
        else:
            invalid_run_command()


if __name__ == "__main__":
    main()
