"""
Launches SeleniumBase Commander | GUI for pytest.

Usage:
      seleniumbase commander [OPTIONAL PATH or TEST FILE]
             sbase commander [OPTIONAL PATH or TEST FILE]
            seleniumbase gui [OPTIONAL PATH or TEST FILE]
                   sbase gui [OPTIONAL PATH or TEST FILE]

Examples:
      sbase gui
      sbase gui -k agent
      sbase gui -m marker2
      sbase gui test_suite.py
      sbase gui offline_examples/

Output:
      Launches SeleniumBase Commander | GUI for pytest.
"""
import colorama
import os
import subprocess
import sys

if sys.version_info <= (3, 7):
    current_version = ".".join(str(ver) for ver in sys.version_info[:3])
    raise Exception(
        "\n* SBase Commander requires Python 3.7 or newer!"
        "\n** You are currently using Python %s" % current_version
    )
from seleniumbase.fixtures import shared_utils
import tkinter as tk  # noqa: E402
from tkinter.scrolledtext import ScrolledText  # noqa: E402


def set_colors(use_colors):
    c0 = ""
    c1 = ""
    c2 = ""
    c3 = ""
    c4 = ""
    c5 = ""
    cr = ""
    if use_colors:
        if (
            shared_utils.is_windows()
            and hasattr(colorama, "just_fix_windows_console")
        ):
            colorama.just_fix_windows_console()
        else:
            colorama.init(autoreset=True)
        c0 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        c2 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c3 = colorama.Fore.BLACK + colorama.Back.LIGHTGREEN_EX
        c4 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        cr = colorama.Style.RESET_ALL
    return c0, c1, c2, c3, c4, c5, cr


def send_window_to_front(root):
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)


def do_pytest_run(
    root,
    tests,
    selected_tests,
    command_string,
    browser_string,
    rs_string,
    thread_string,
    verbose,
    demo_mode,
    mobile_mode,
    dashboard,
    html_report,
    headless,
    save_screenshots,
    additional_options,
):
    cleaned_tests = []
    for test in tests:
        if test.startswith("(FILE)  "):
            clean_test = test.split("(FILE)  ")[1].split("  =>  ")[0]
            cleaned_tests.append(clean_test)
        else:
            cleaned_tests.append(test)
    tests = cleaned_tests
    total_tests = len(tests)
    total_selected_tests = 0
    for selected_test in selected_tests:
        if selected_tests[selected_test].get():
            total_selected_tests += 1

    full_run_command = '"%s" -m pytest' % sys.executable
    if total_selected_tests == 0 or total_tests == total_selected_tests:
        if command_string:
            full_run_command += " "
            full_run_command += command_string
    else:
        for test_number, test in enumerate(tests):
            if selected_tests[test_number].get():
                full_run_command += " "
                if ' ' not in test:
                    full_run_command += test
                elif '"' not in test:
                    full_run_command += '"%s"' % test
                else:
                    full_run_command += test.replace(" ", "\\ ")

    if "(--edge)" in browser_string:
        full_run_command += " --edge"
    elif "(--firefox)" in browser_string:
        full_run_command += " --firefox"
    elif "(--safari)" in browser_string:
        full_run_command += " --safari"

    if "(--rs)" in rs_string:
        full_run_command += " --rs"
    elif "(--rs --crumbs)" in rs_string:
        full_run_command += " --rs --crumbs"
    elif "(--rcs)" in rs_string:
        full_run_command += " --rcs"
    elif "(--rcs --crumbs)" in rs_string:
        full_run_command += " --rcs --crumbs"

    if "(-n=2)" in thread_string:
        full_run_command += " -n=2"
    elif "(-n=3)" in thread_string:
        full_run_command += " -n=3"
    elif "(-n=4)" in thread_string:
        full_run_command += " -n=4"
    elif "(-n=5)" in thread_string:
        full_run_command += " -n=5"
    elif "(-n=6)" in thread_string:
        full_run_command += " -n=6"
    elif "(-n=7)" in thread_string:
        full_run_command += " -n=7"
    elif "(-n=8)" in thread_string:
        full_run_command += " -n=8"

    if demo_mode:
        full_run_command += " --demo"

    if mobile_mode:
        full_run_command += " --mobile"

    if dashboard:
        full_run_command += " --dashboard"

    if html_report:
        full_run_command += " --html=report.html"

    if headless:
        full_run_command += " --headless"
    elif shared_utils.is_linux():
        full_run_command += " --gui"

    if save_screenshots:
        full_run_command += " --screenshot"

    dash_s_needed = False
    if "-s" not in additional_options.split(" "):
        dash_s_needed = True

    additional_options = additional_options.strip()
    if additional_options:
        full_run_command += " "
        full_run_command += additional_options

    if verbose:
        full_run_command += " -v"

    if dash_s_needed:
        full_run_command += " -s"

    print(full_run_command)
    subprocess.Popen(full_run_command, shell=True)
    send_window_to_front(root)


def create_tkinter_gui(tests, command_string, files, solo_tests):
    root = tk.Tk()
    root.title("SeleniumBase Commander | GUI for pytest")
    if shared_utils.is_windows():
        root.minsize(820, 696)
    else:
        root.minsize(820, 702)
    tk.Label(root, text="").pack()

    options_list = [
        "Use Chrome Browser  (Default)",
        "Use Edge Browser  (--edge)",
        "Use Firefox Browser  (--firefox)",
    ]
    if shared_utils.is_mac():
        options_list.append("Use Safari Browser  (--safari)")
    brx = tk.StringVar(root)
    brx.set(options_list[0])
    question_menu = tk.OptionMenu(root, brx, *options_list)
    question_menu.pack()

    options_list = [
        "New Session Per Test  (Default)",
        "Reuse Session for ALL tests in thread  (--rs)",
        "Reuse Session and also clear cookies  (--rs --crumbs)",
        "Reuse Session for tests with same CLASS  (--rcs)",
        "Reuse Session for class and clear cookies  (--rcs --crumbs)",
    ]
    rsx = tk.StringVar(root)
    rsx.set(options_list[0])
    question_menu = tk.OptionMenu(root, rsx, *options_list)
    question_menu.pack()

    options_list = [
        "Number of Threads: 1  (Default)",
        "Number of Threads: 2  (-n=2)",
        "Number of Threads: 3  (-n=3)",
        "Number of Threads: 4  (-n=4)",
    ]
    try:
        if int(os.cpu_count()) >= 8:
            options_list.append("Number of Threads: 5  (-n=5)")
            options_list.append("Number of Threads: 6  (-n=6)")
            options_list.append("Number of Threads: 7  (-n=7)")
            options_list.append("Number of Threads: 8  (-n=8)")
    except Exception:
        pass

    ntx = tk.StringVar(root)
    ntx.set(options_list[0])
    question_menu = tk.OptionMenu(root, ntx, *options_list)
    question_menu.pack()

    vox = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Verbose Output  (-v)", variable=vox, pady=0
    )
    chk.pack()
    chk.select()

    dmx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Demo Mode  (--demo)", variable=dmx, pady=0
    )
    chk.pack()

    mmx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Mobile Mode  (--mobile)", variable=mmx, pady=0
    )
    chk.pack()

    dbx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Dashboard  (--dashboard)", variable=dbx, pady=0
    )
    chk.pack()
    chk.select()

    hrx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Report  (--html=report.html)", variable=hrx, pady=0
    )
    chk.pack()
    chk.select()

    hbx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Headless Browser  (--headless)", variable=hbx, pady=0
    )
    chk.pack()

    ssx = tk.IntVar()
    chk = tk.Checkbutton(
        root, text="Save Screenshots  (--screenshot)", variable=ssx, pady=0
    )
    chk.pack()

    tk.Label(root, text="").pack()
    run_display = (
        "Select from %s rows (%s files with %s tests):  "
        "(All tests will run if none are selected)"
        % (len(tests), len(files), len(solo_tests))
    )
    if len(solo_tests) == 1:
        run_display = "Only ONE TEST was found and will be run:"
        tests = solo_tests
    elif len(files) == 1:
        run_display = (
            "Select from %s tests:  "
            "(All tests will run if none are selected)"
            % (len(solo_tests))
        )
        tests = solo_tests
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
        if shared_utils.is_windows():
            cb = tk.Checkbutton(
                text_area,
                text=(row),
                bg="white",
                fg="black",
                anchor="w",
                pady=0,
                borderwidth=1,
                highlightthickness=1,
                variable=ara[count],
            )
        else:
            cb = tk.Checkbutton(
                text_area,
                text=(row),
                bg="white",
                fg="black",
                anchor="w",
                pady=0,
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
        text='Additional "pytest" Options:  (Eg. "--incognito --slow")',
        bg="yellow", fg="blue",
    ).pack()
    entry = tk.Entry(root, textvariable=aopts)
    entry.pack()
    entry.focus()
    entry.bind(
        "<Return>",
        (
            lambda _: do_pytest_run(
                root,
                tests,
                ara,
                command_string,
                brx.get(),
                rsx.get(),
                ntx.get(),
                vox.get(),
                dmx.get(),
                mmx.get(),
                dbx.get(),
                hrx.get(),
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
        command=lambda: do_pytest_run(
            root,
            tests,
            ara,
            command_string,
            brx.get(),
            rsx.get(),
            ntx.get(),
            vox.get(),
            dmx.get(),
            mmx.get(),
            dbx.get(),
            hrx.get(),
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
    if shared_utils.is_linux():
        use_colors = False
    c0, c1, c2, c3, c4, c5, cr = set_colors(use_colors)
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
    message += c3
    message += "Commander"
    message += c4
    message += " Desktop App"
    message += c2
    message += "..."
    message += cr
    print(message)

    proc = subprocess.Popen(
        '"%s" -m pytest --collect-only -q --rootdir="./" %s'
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
    tests = []
    if shared_utils.is_windows():
        output = output.decode("latin1")
    else:
        output = output.decode("utf-8")
    for row in output.replace("\r", "").split("\n"):
        if ("::") in row:
            tests.append(row)
    if not tests:
        error_msg = "No tests found! Exiting SeleniumBase Commander..."
        error_msg = c5 + "ERROR: " + error_msg + cr
        print(error_msg)
        return
    groups = []
    for row in tests:
        if row.count("::") >= 1:
            g_name = "(FILE)  %s" % row.split("::")[0]
            groups.append(g_name)
    files = []
    used_files = []
    for row in groups:
        if row not in used_files:
            used_files.append(row)
            plural = "s"
            if groups.count(row) == 1:
                plural = ""
            f_row = "%s  =>  (%s Test%s)" % (row, groups.count(row), plural)
            files.append(f_row)
    solo_tests = tests
    tests = [*files, *tests]

    create_tkinter_gui(tests, command_string, files, solo_tests)


if __name__ == "__main__":
    print('To open SBase Commander, type "sbase commander" or "sbase gui"')
