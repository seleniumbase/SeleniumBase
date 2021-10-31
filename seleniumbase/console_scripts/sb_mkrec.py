# -*- coding: utf-8 -*-
"""
Creates a new SeleniumBase test file using the Recorder.

Usage:
      seleniumbase mkrec [FILE.py] [OPTIONS]
             sbase mkrec [FILE.py] [OPTIONS]
    seleniumbase codegen [FILE.py] [OPTIONS]
           sbase codegen [FILE.py] [OPTIONS]

Examples:
    sbase mkrec new_test.py
    sbase mkrec new_test.py --url=seleniumbase.io
    sbase codegen new_test.py
    sbase codegen new_test.py --url=wikipedia.org

Options:
    --url=URL  (Sets the initial start page URL.)
    --edge  (Use Edge browser instead of Chrome.)
    --gui / --headed  (Use headed mode on Linux.)

Output:
    Creates a new SeleniumBase test using the Recorder.
    If the filename already exists, an error is raised.
"""

import codecs
import colorama
import shutil
import os
import sys


def invalid_run_command(msg=None):
    exp = "  ** mkrec / codegen **\n\n"
    exp += "  Usage:\n"
    exp += "           seleniumbase mkrec [FILE.py]\n"
    exp += "                  sbase mkrec [FILE.py]\n"
    exp += "         seleniumbase codegen [FILE.py]\n"
    exp += "                sbase codegen [FILE.py]\n"
    exp += "  Examples:\n"
    exp += "           sbase mkrec new_test.py\n"
    exp += "           sbase codegen new_test.py\n"
    exp += "  Options:\n"
    exp += "           --url=URL  (Sets the initial start page URL.)\n"
    exp += "           --edge  (Use Edge browser instead of Chrome.)\n"
    exp += "           --gui / --headed  (Use headed mode on Linux.)\n"
    exp += "  Output:\n"
    exp += "           Creates a new SeleniumBase test using the Recorder.\n"
    exp += "           If the filename already exists, an error is raised.\n"
    if not msg:
        raise Exception("INVALID RUN COMMAND!\n\n%s" % exp)
    elif msg == "help":
        print("\n%s" % exp)
        sys.exit()
    else:
        raise Exception("INVALID RUN COMMAND!\n\n%s\n%s\n" % (exp, msg))


def set_colors(use_colors):
    c0 = ""
    c1 = ""
    c2 = ""
    c5 = ""
    c7 = ""
    cr = ""
    if use_colors:
        colorama.init(autoreset=True)
        c0 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c1 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c2 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTYELLOW_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
        cr = colorama.Style.RESET_ALL
    return c0, c1, c2, c5, c7, cr


def main():
    help_me = False
    error_msg = None
    invalid_cmd = None
    use_edge = False
    start_page = None
    next_is_url = False
    use_colors = True
    force_gui = False

    if "linux" in sys.platform:
        use_colors = False
    c0, c1, c2, c5, c7, cr = set_colors(use_colors)

    command_args = sys.argv[2:]
    file_name = command_args[0]
    if file_name == "-h" or file_name == "--help":
        invalid_run_command("help")
    elif not file_name.endswith(".py"):
        error_msg = 'File name must end with ".py"!'
    elif "*" in file_name or len(str(file_name)) < 4:
        error_msg = "Invalid file name!"
    elif file_name.startswith("-"):
        error_msg = 'File name cannot start with "-"!'
    elif "/" in str(file_name) or "\\" in str(file_name):
        error_msg = "File must be created in the current directory!"
    elif os.path.exists(os.getcwd() + "/" + file_name):
        error_msg = 'File "%s" already exists in this directory!' % file_name
    if error_msg:
        error_msg = c5 + "ERROR: " + error_msg + cr
        invalid_run_command(error_msg)

    if len(command_args) >= 2:
        options = command_args[1:]
        for option in options:
            if option.lower() == "-h" or option.lower() == "--help":
                help_me = True
            elif option.lower() == "--edge":
                use_edge = True
            elif (
                option.lower() in ("--gui", "--headed")
                and "linux" in sys.platform
            ):
                use_colors = True
                c0, c1, c2, c5, c7, cr = set_colors(use_colors)
                force_gui = True
            elif option.lower().startswith("--url="):
                start_page = option[len("--url="):]
            elif option.lower() == "--url":
                next_is_url = True
            elif next_is_url:
                start_page = option
                next_is_url = False
            else:
                invalid_cmd = "\n===> INVALID OPTION: >> %s <<\n" % option
                invalid_cmd = invalid_cmd.replace(">> ", ">>" + c5 + " ")
                invalid_cmd = invalid_cmd.replace(" <<", " " + cr + "<<")
                invalid_cmd = invalid_cmd.replace(">>", c7 + ">>" + cr)
                invalid_cmd = invalid_cmd.replace("<<", c7 + "<<" + cr)
                help_me = True
                break
    if help_me:
        invalid_run_command(invalid_cmd)

    dir_name = os.getcwd()
    file_path = "%s/%s" % (dir_name, file_name)

    data = []
    data.append("from seleniumbase import BaseCase")
    data.append("")
    data.append("")
    data.append("class RecorderTests(BaseCase):")
    data.append("    def test_recording(self):")
    data.append('        if self.recorder_ext and not self.xvfb:')
    data.append('            import ipdb; ipdb.set_trace()')
    data.append("")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()
    success = (
        "\n" + c0 + '* RECORDING initialized:' + cr + " "
        "" + c1 + file_name + "" + cr + "\n"
    )
    print(success)
    if not start_page:
        run_cmd = "pytest %s --rec -q -s" % file_name
        if use_edge:
            run_cmd += " --edge"
        if force_gui:
            run_cmd += " --gui"
        print(run_cmd)
        os.system(run_cmd)
    else:
        run_cmd = "pytest %s --rec -q -s --url=%s" % (file_name, start_page)
        if use_edge:
            run_cmd += " --edge"
        if force_gui:
            run_cmd += " --gui"
        print(run_cmd)
        os.system(run_cmd)
    if os.path.exists(file_path):
        os.remove(file_path)
    recorded_filename = file_name[:-3] + "_rec.py"
    recordings_dir = os.path.join(dir_name, "recordings")
    recorded_file = os.path.join(recordings_dir, recorded_filename)
    if " " not in recorded_file:
        os.system("sbase print %s -n" % recorded_file)
    elif '"' not in recorded_file:
        os.system('sbase print "%s" -n' % recorded_file)
    else:
        os.system("sbase print '%s' -n" % recorded_file)
    shutil.copy(recorded_file, file_path)
    success = (
        "\n" + c2 + "***" + cr + " RECORDING COPIED to: "
        "" + c1 + file_name + cr + "\n"
    )
    print(success)


if __name__ == "__main__":
    invalid_run_command()
