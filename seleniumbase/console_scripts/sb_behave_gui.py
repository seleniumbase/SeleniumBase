"""
Launches SeleniumBase Behave Commander | GUI for Behave.

Usage:
      seleniumbase behave-gui [OPTIONAL PATH or TEST FILE]
             sbase behave-gui [OPTIONAL PATH or TEST FILE]

Examples:
      sbase behave-gui
      sbase behave-gui features/
      sbase behave-gui features/calculator.feature

Output:
      Launches SeleniumBase Behave Commander | GUI for Behave.
"""
import colorama
import subprocess
import sys

if sys.version_info <= (3, 7):
    current_version = ".".join(str(ver) for ver in sys.version_info[:3])
    raise Exception(
        "\n* SBase Commander requires Python 3.7 or newer!"
        "\n** You are currently using Python %s" % current_version
    )
import tkinter as tk  # noqa: E402
from tkinter.scrolledtext import ScrolledText  # noqa: E402

is_windows = False
if sys.platform in ["win32", "win64", "x64"]:
    is_windows = True


def set_colors(use_colors):
    c0 = ""
    c1 = ""
    c2 = ""
    c3 = ""
    c4 = ""
    c5 = ""
    c6 = ""
    cr = ""
    if use_colors:
        colorama.init(autoreset=True)
        c0 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        c2 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c3 = colorama.Fore.BLACK + colorama.Back.LIGHTGREEN_EX
        c4 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c6 = colorama.Fore.MAGENTA + colorama.Back.LIGHTYELLOW_EX
        cr = colorama.Style.RESET_ALL
    return c0, c1, c2, c3, c4, c5, c6, cr


def send_window_to_front(root):
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)


def do_behave_run(
    root,
    tests,
    selected_tests,
    command_string,
    browser_string,
    rs_string,
    quiet_mode,
    demo_mode,
    mobile_mode,
    dashboard,
    headless,
    save_screenshots,
    additional_options,
):
    total_tests = len(tests)
    total_selected_tests = 0
    test_to_run = None
    for selected_test in selected_tests:
        if selected_tests[selected_test].get():
            total_selected_tests += 1

    full_run_command = "%s -m behave" % sys.executable
    if total_selected_tests == 0 or total_tests == total_selected_tests:
        if command_string:
            full_run_command += " "
            full_run_command += command_string
    else:
        for test_number, test in enumerate(tests):
            if selected_tests[test_number].get():
                full_run_command += " "
                test_to_run = test
                if test.startswith("(GROUP)  "):
                    test_to_run = test.split("(GROUP)  ")[1]
                    full_run_command += test_to_run.split(" => ")[0]
                else:
                    full_run_command += test.split(" => ")[0]

    if "(-D edge)" in browser_string:
        full_run_command += " -D edge"
    elif "(-D firefox)" in browser_string:
        full_run_command += " -D firefox"
    elif "(-D safari)" in browser_string:
        full_run_command += " -D safari"

    if "(-D rs)" in rs_string:
        full_run_command += " -D rs"
    elif "(-D rs -D crumbs)" in rs_string:
        full_run_command += " -D rs -D crumbs"
    elif "(-D rcs)" in rs_string:
        full_run_command += " -D rcs"
    elif "(-D rcs -D crumbs)" in rs_string:
        full_run_command += " -D rcs -D crumbs"

    if quiet_mode:
        full_run_command += " --quiet"

    if demo_mode:
        full_run_command += " -D demo"

    if mobile_mode:
        full_run_command += " -D mobile"

    if dashboard:
        full_run_command += " -D dashboard"

    if headless:
        full_run_command += " -D headless"
    elif "linux" in sys.platform:
        full_run_command += " -D gui"

    if save_screenshots:
        full_run_command += " -D screenshot"

    additional_options_list = additional_options.split(" ")
    dash_T_needed = False
    if (
        "-T" not in additional_options_list
        and "--no-timings" not in additional_options_list
        and "--show-timings" not in additional_options_list
    ):
        dash_T_needed = True
    dash_k_needed = False
    if (
        "-k" not in additional_options_list
        and "--no-skipped" not in additional_options_list
        and "--show-skipped" not in additional_options_list
    ):
        dash_k_needed = True
    additional_options = additional_options.strip()
    if additional_options:
        full_run_command += " "
        full_run_command += additional_options
    if dash_T_needed:
        full_run_command += " -T"
    if dash_k_needed:
        full_run_command += " -k"

    print(full_run_command)
    if not additional_options or " " not in additional_options:
        subprocess.Popen(full_run_command, shell=True)
    else:
        proc = subprocess.Popen(
            full_run_command, stderr=subprocess.PIPE, shell=True
        )
        (output, error) = proc.communicate()
        if error and proc.returncode == 2:
            if str(error).startswith("b'") and str(error).endswith("\\n'"):
                error = str(error)[2:-3]
            elif str(error).startswith("b'") and str(error).endswith("'"):
                error = str(error)[2:-1]
            else:
                error = str(error)
            error = error.replace("\\n", "\n")
            print(error)
    send_window_to_front(root)


def create_tkinter_gui(tests, command_string, t_count, f_count, s_tests):
    root = tk.Tk()
    root.title("SeleniumBase Behave Commander | GUI for Behave")
    root.minsize(820, 656)
    tk.Label(root, text="").pack()

    options_list = [
        "Use Chrome Browser  (Default)",
        "Use Edge Browser  (-D edge)",
        "Use Firefox Browser  (-D firefox)",
    ]
    if "darwin" in sys.platform:
        options_list.append("Use Safari Browser  (-D safari)")
    brx = tk.StringVar(root)
    brx.set(options_list[0])
    question_menu = tk.OptionMenu(root, brx, *options_list)
    question_menu.pack()

    options_list = [
        "New Session Per Test  (Default)",
        "Reuse Session for ALL the tests  (-D rs)",
        "Reuse Session and clear cookies  (-D rs -D crumbs)",
        "Reuse Session in the SAME class/feature  (-D rcs)",
        "Reuse Session in class and clear cookies  (-D rcs -D crumbs)",
    ]
    rsx = tk.StringVar(root)
    rsx.set(options_list[0])
    question_menu = tk.OptionMenu(root, rsx, *options_list)
    question_menu.pack()

    qmx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Quiet Mode  (--quiet)", variable=qmx, pady=0
    )
    chk.pack()

    dmx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Demo Mode  (-D demo)", variable=dmx, pady=0
    )
    chk.pack()

    mmx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Mobile Mode  (-D mobile)", variable=mmx, pady=0
    )
    chk.pack()

    dbx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Dashboard  (-D dashboard)", variable=dbx, pady=0
    )
    chk.pack()
    chk.select()

    hbx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Headless Browser  (-D headless)", variable=hbx, pady=0
    )
    chk.pack()

    ssx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Save Screenshots  (-D screenshot)", variable=ssx, pady=0
    )
    chk.pack()

    tk.Label(root, text="").pack()
    plural = "s"
    if f_count == 1:
        plural = ""
    run_display = (
        "Select from %s rows (%s feature%s with %s scenarios):  "
        "(All tests will run if none are selected)"
        % (len(tests), f_count, plural, t_count)
    )
    if t_count == 1:
        run_display = "Only ONE TEST was found and will be run:"
        tests = s_tests
    tk.Label(root, text=run_display, bg="yellow", fg="magenta").pack()
    text_area = ScrolledText(
        root, width=100, height=12, wrap="word", state=tk.DISABLED
    )
    text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    count = 0
    ara = {}
    for row in tests:
        row += " " * 200
        ara[count] = tk.IntVar()
        cb = None
        if not is_windows:
            cb = tk.Checkbutton(
                text_area,
                text=(row),
                bg="teal",
                fg="yellow",
                anchor="w",
                pady=0,
                variable=ara[count],
            )
        else:
            cb = tk.Checkbutton(
                text_area,
                text=(row),
                bg="teal",
                fg="yellow",
                anchor="w",
                pady=0,
                borderwidth=0,
                highlightthickness=0,
                variable=ara[count],
            )
        text_area.window_create("end", window=cb)
        text_area.insert("end", "\n")
        count += 1

    tk.Label(root, text="").pack()
    additional_options = ""
    aopts = tk.StringVar(value=additional_options)
    tk.Label(
        root,
        text='Additional "behave" Options:  (Eg. "-D incognito --junit")',
        bg="yellow", fg="blue",
    ).pack()
    entry = tk.Entry(root, textvariable=aopts)
    entry.pack()
    entry.focus()
    entry.bind(
        "<Return>",
        (
            lambda _: do_behave_run(
                root,
                tests,
                ara,
                command_string,
                brx.get(),
                rsx.get(),
                qmx.get(),
                dmx.get(),
                mmx.get(),
                dbx.get(),
                hbx.get(),
                ssx.get(),
                aopts.get(),
            )
        ),
    )
    tk.Button(
        root,
        text="Run Selected Tests",
        fg="green",
        bg="gray",
        command=lambda: do_behave_run(
            root,
            tests,
            ara,
            command_string,
            brx.get(),
            rsx.get(),
            qmx.get(),
            dmx.get(),
            mmx.get(),
            dbx.get(),
            hbx.get(),
            ssx.get(),
            aopts.get(),
        ),
    ).pack()
    tk.Label(root, text="\n").pack()

    # Bring form window to front
    send_window_to_front(root)
    # Use decoy to set correct focus on main window
    decoy = tk.Tk()
    decoy.geometry("1x1")
    decoy.iconify()
    decoy.update()
    decoy.deiconify()
    decoy.destroy()
    # Start tkinter
    root.mainloop()


def main():
    use_colors = True
    if "linux" in sys.platform:
        use_colors = False
    c0, c1, c2, c3, c4, c5, c6, cr = set_colors(use_colors)
    command_args = sys.argv[2:]
    command_string = " ".join(command_args)
    message = ""
    message += c2
    message += "*"
    message += c4
    message += " Starting the "
    message += c0
    message += "Selenium"
    message += c1
    message += "Base"
    message += c2
    message += " "
    message += c6
    message += "Behave"
    message += c4
    message += " "
    message += c3
    message += "Commander"
    message += c4
    message += " GUI App"
    message += c2
    message += "..."
    message += cr
    print(message)
    command_string = command_string.replace("--quiet", "")
    command_string = command_string.replace("-q", "")
    proc = subprocess.Popen(
        "%s -m behave -d %s --show-source"
        % (sys.executable, command_string),
        stdout=subprocess.PIPE,
        shell=True,
    )
    (output, error) = proc.communicate()
    if error:
        error_msg = "Error collecting tests: %s" % str(error)
        error_msg = c5 + error_msg + cr
        print(error_msg)
        return
    filename = None
    feature_name = None
    scenario_name = None
    f_tests = []  # Features
    s_tests = []  # Scenarios
    tests = []  # All tests
    file_scenario_count = {}
    f_count = 0
    s_count = 0
    t_count = 0
    if is_windows:
        output = output.decode("latin1")
    else:
        output = output.decode("utf-8")
    for row in output.replace("\r", "").split("\n"):
        if row.startswith("Feature: "):
            if f_count > 0:
                file_scenario_count[str(f_count)] = s_count
            f_count += 1
            s_count = 0
        elif row.startswith("  Scenario: "):
            s_count += 1
            file_scenario_count[str(f_count)] = s_count
        elif row.startswith("  Scenario Outline: "):
            s_count += 1
            file_scenario_count[str(f_count)] = s_count
    file_scenario_count[str(f_count)] = s_count
    f_count = 0
    s_count = 0
    for row in output.replace("\r", "").split("\n"):
        if row.startswith("Feature: "):
            f_count += 1
            feature_name = row.split("Feature: ")[1]
            if " # features/" in feature_name:
                filename = feature_name.split(" # features/")[-1]
                filename = "features/" + filename.split(":")[0]
                feature_name = feature_name.split(" # features/")[0]
            elif " # features\\" in feature_name:
                filename = feature_name.split(" # features\\")[-1]
                filename = "features\\" + filename.split(":")[0]
                feature_name = feature_name.split(" # features\\")[0]
            else:
                filename = feature_name.split(" # ")[-1]
                filename = filename.split(":")[0]
                feature_name = feature_name.split(" # ")[-1]
            s_count = file_scenario_count[str(f_count)]
            filename = filename.strip()
            t_name = "(GROUP)  %s => %s" % (filename, feature_name)
            t_name += "  <>  (%s Total)" % s_count
            f_tests.append(t_name)
        elif (
            row.startswith("  Scenario: ")
            or row.startswith("  Scenario Outline: ")
        ):
            t_count += 1
            line_num = row.split(":")[-1]
            scenario_name = None
            if row.startswith("  Scenario: "):
                scenario_name = row.split("  Scenario: ")[-1]
            else:
                scenario_name = row.split("  Scenario Outline: ")[-1]
            if " -- @" in scenario_name:
                scenario_name = scenario_name.split(" # ")[0].rstrip()
            elif " # features/" in scenario_name:
                scenario_name = scenario_name.split(" # features/")[0]
            else:
                scenario_name = scenario_name.split(" # ")[0]
            scenario_name = scenario_name.strip()
            s_tests.append("%s:%s => %s" % (filename, line_num, scenario_name))
    tests = f_tests + s_tests
    if not tests:
        err_msg_0 = c5 + "ERROR:" + cr + "\n"
        err_msg_1 = '  No "behave" tests found! Expecting "*.feature" files!'
        err_msg_1 = c6 + err_msg_1 + cr + "\n"
        err_msg_2 = '  "*.feature" files would live in a "features/" folder.'
        err_msg_2 = c6 + err_msg_2 + cr + "\n"
        err_msg_3 = "Exiting SBase Behave Commander..."
        err_msg_3 = c5 + err_msg_3 + cr
        error_msg = err_msg_0 + err_msg_1 + err_msg_2 + err_msg_3
        print(error_msg)
        return

    create_tkinter_gui(tests, command_string, t_count, f_count, s_tests)


if __name__ == "__main__":
    print('To open SBase Behave Commander, type "sbase behave-gui"')
