"""
Launches the SeleniumBase Case Plans Generator.

Usage:
      seleniumbase caseplans [OPTIONAL PATH or TEST FILE]
             sbase caseplans [OPTIONAL PATH or TEST FILE]

Examples:
      sbase caseplans
      sbase caseplans -k agent
      sbase caseplans -m marker2
      sbase caseplans test_suite.py
      sbase caseplans offline_examples/

Output:
      Launches the SeleniumBase Case Plans Generator.
"""
import codecs
import colorama
import os
import subprocess
import sys

if sys.version_info <= (3, 7):
    current_version = ".".join(str(ver) for ver in sys.version_info[:3])
    raise Exception(
        "\n* SBase Case Plans Generator requires Python 3.7 or newer!"
        "\n** You are currently using Python %s" % current_version
    )
import tkinter as tk  # noqa: E402
from tkinter import messagebox  # noqa: E402
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
    cr = ""
    if use_colors:
        colorama.init(autoreset=True)
        c0 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        c2 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c3 = colorama.Fore.BLACK + colorama.Back.LIGHTCYAN_EX
        c4 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        cr = colorama.Style.RESET_ALL
    return c0, c1, c2, c3, c4, c5, cr


def send_window_to_front(root):
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)


def show_no_case_plans_warning():
    messagebox.showwarning(
        "No existing Case Plans found!",
        "\nNo existing Case Plans found!!\n\nCreate some boilerplates first!",
    )


def get_test_id(display_id):
    """The id used in various places such as the test log path."""
    return display_id.replace(".py::", ".").replace("::", ".")


def generate_case_plan_boilerplates(
    root,
    tests,
    selected_tests,
    tests_with_case_plan,
    tests_without_case_plan,
):
    total_tests = len(tests)
    total_selected_tests = 0
    for selected_test in selected_tests:
        if selected_tests[selected_test].get():
            total_selected_tests += 1

    test_cases = []
    case_plans_to_create = []
    if total_selected_tests == 0:
        messagebox.showwarning(
            "No tests were selected!",
            "\nℹ️ No tests were selected!\nSelect tests for Case Plans!",
        )
        send_window_to_front(root)
        return
    elif total_tests == total_selected_tests:
        for test in tests:
            test_cases.append(test)
    else:
        for test_number, test in enumerate(tests):
            if selected_tests[test_number].get():
                test_cases.append(test)

    for test_case in test_cases:
        if (
            test_case in tests_without_case_plan
            and test_case not in tests_with_case_plan
        ):
            case_plans_to_create.append(test_case)

    new_plans = 0
    for case_plan in case_plans_to_create:
        parts = case_plan.split("/")
        test_address = None
        folder_path = None
        if len(parts) == 1:
            test_address = parts[0]
        if len(parts) > 1:
            test_address = parts[-1]
            folder_path = "/".join(parts[0:-1])
        test_id = get_test_id(test_address)
        case_id = test_id + ".md"
        full_folder_path = None
        if len(parts) == 1:
            full_folder_path = "case_plans"
            if not os.path.exists(full_folder_path):
                os.makedirs(full_folder_path)
        else:
            full_folder_path = os.path.join(folder_path, "case_plans")
            if not os.path.exists(full_folder_path):
                os.makedirs(full_folder_path)

        data = []
        data.append("``%s``" % test_address)
        data.append("---")
        data.append("| # | Step Description | Expected Result |")
        data.append("| - | ---------------- | --------------- |")
        data.append("| 1 | Perform Action 1 | Verify Action 1 |")
        data.append("| 2 | Perform Action 2 | Verify Action 2 |")
        data.append("")
        file_name = case_id
        file_path = os.path.join(full_folder_path, file_name)
        if not os.path.exists(file_path):
            out_file = codecs.open(file_path, "w+", "utf-8")
            out_file.writelines("\r\n".join(data))
            out_file.close()
            new_plans += 1
            print("Created %s" % file_path)

    if new_plans == 1:
        messagebox.showinfo(
            "A new Case Plan was generated!",
            '\n✅ %s new boilerplate Case Plan was generated!' % new_plans,
        )
    elif new_plans >= 2:
        messagebox.showinfo(
            "New Case Plans were generated!",
            '\n✅ %s new boilerplate Case Plans were generated!' % new_plans,
        )
    else:
        messagebox.showwarning(
            "No new Case Plans were generated!",
            "\nℹ️ No new boilerplates were generated!\n\n"
            "The selected tests already have Case Plans!",
        )
    send_window_to_front(root)


def view_summary_of_existing_case_plans(root, tests):
    case_data_storage = []
    case_to_test_hash = {}
    full_t = []
    for test_index, test in enumerate(tests):
        full_t.append(test)
        parts = test.strip().split("/")
        test_address = None
        folder_path = None
        if len(parts) == 1:
            test_address = parts[0]
            folder_path = "."
        if len(parts) > 1:
            test_address = parts[-1]
            folder_path = "/".join(parts[0:-1])
        test_id = get_test_id(test_address)
        case_id = test_id + ".md"
        case_path = None
        if len(parts) == 1:
            case_path = os.path.join("case_plans", case_id)
        else:
            case_path = os.path.join(folder_path, "case_plans", case_id)
        if os.path.exists(case_path):
            f = open(case_path, "r")
            case_data = f.read()
            f.close()
            case_data_storage.append(case_data)
            case_to_test_hash[len(case_data_storage) - 1] = test_index

    full_plan = []
    if len(case_data_storage) > 0:
        full_plan.append(
            "<h2>Summary of existing Case Plans</h2>"
        )
        full_plan.append("")
        full_plan.append("|   |   |")
        full_plan.append("| - | - |")
        full_plan.append("|  🔵  | Plans with customized step definitions. |")
        full_plan.append("|  ⭕  | Plans using default boilerplate code. |")
        full_plan.append("|  🚧  | Plans under construction with no table. |")
        full_plan.append("")
        full_plan.append("--------")
    else:
        show_no_case_plans_warning()
        send_window_to_front(root)
        return
    full_plan.append("")
    full_plan.append("<h3>🔎 (Click rows to expand) 🔍</h3>")
    full_plan.append("")

    full_plan = []
    num_ready_cases = 0
    num_boilerplate = 0
    num_in_progress = 0
    for case_index, case_data in enumerate(case_data_storage):
        icon = "🔵"
        table_missing = False
        if "| 1 | Perform Action 1 | Verify Action 1 |" in case_data:
            # Still using raw boilerplate code. (Missing real test steps)
            icon = "⭕"
        if case_data.count("|") < 9 or case_data.count("-") < 3:
            # Not enough characters for a minimal Markdown case plan file.
            # The dash(es) on line 2, and the Markdown table are required.
            # This is what a minimal case plan file might look like:
            """
            TEST_ADDRESS
            -
            | Steps | Results |
            |   -   |    -    |
            | Step1 | Result1 |
            """
            icon = "🚧"
            table_missing = True
        lines = case_data.split("\n")
        if len(lines) >= 3 and not table_missing:
            first_line = lines[0]
            first_line = first_line.strip()
            if not (first_line.startswith("``") and first_line.endswith("``")):
                first_line = "``%s``" % tests[case_to_test_hash[case_index]]
                lines.insert(0, first_line)
            else:
                first_line = "``%s``" % tests[case_to_test_hash[case_index]]
                lines[0] = first_line
            lines.insert(0, "<details>")
            lines[1] = (
                "<summary> %s <code><b>" % icon
                + first_line[2:-2]
                + "</b></code></summary>"
            )
            if (
                lines[2].strip().startswith("-")
                and lines[2].strip().endswith("-")
            ):
                lines[2] = ""
            elif lines[2].strip() != "":
                lines.insert(2, "")
            if lines[-1].strip() != "":
                lines.append("")
            lines.append("</details>")
            full_plan.append("\r\n".join(lines))
        else:
            # No existing Case Plan found. / File is missing boilerplate.
            icon = "🚧"
            lines = []
            first_line = tests[case_to_test_hash[case_index]]
            first_line = "%s <code><b>%s</b></code>" % (icon, first_line)
            lines.insert(0, first_line)
            full_plan.append("\r\n".join(lines))
        full_plan.append("")
        if icon == "🔵":
            num_ready_cases += 1
        elif icon == "⭕":
            num_boilerplate += 1
        elif icon == "🚧":
            num_in_progress += 1

    msg_ready_cases = "%s Case Plans with customized tables" % num_ready_cases
    if num_ready_cases == 1:
        msg_ready_cases = "1 Case Plan with a customized table"
    msg_boilerplate = "%s Case Plans using boilerplate code" % num_boilerplate
    if num_boilerplate == 1:
        msg_boilerplate = "1 Case Plan using boilerplate code"
    msg_in_progress = "%s Case Plans that are missing tables" % num_in_progress
    if num_in_progress == 1:
        msg_in_progress = "1 Case Plan that is missing a table"

    msg_r = " ".join(msg_ready_cases.split(" ")[1:])
    msg_b = " ".join(msg_boilerplate.split(" ")[1:])
    msg_i = " ".join(msg_in_progress.split(" ")[1:])

    plan_head = []
    if len(case_data_storage) > 0:
        plan_head.append(
            "<h2>Summary of existing Case Plans</h2>"
        )
        plan_head.append("")
        plan_head.append("|   |    |   |")
        plan_head.append("| - | -: | - |")
        plan_head.append("| 🔵 | %s | %s |" % (num_ready_cases, msg_r))
        plan_head.append("| ⭕ | %s | %s |" % (num_boilerplate, msg_b))
        plan_head.append("| 🚧 | %s | %s |" % (num_in_progress, msg_i))
        plan_head.append("")
        plan_head.append("--------")
    else:
        show_no_case_plans_warning()
        send_window_to_front(root)
        return
    plan_head.append("")
    plan_head.append("<h3>🔎 (Click rows to expand) 🔍</h3>")
    plan_head.append("")

    for row in full_plan:
        plan_head.append(row)
    full_plan = plan_head

    file_path = "case_summary.md"
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(full_plan))
    file.close()

    if num_ready_cases < 10:
        msg_ready_cases = " %s" % msg_ready_cases
    if num_ready_cases < 100:
        msg_ready_cases = " %s" % msg_ready_cases
    if num_boilerplate < 10:
        msg_boilerplate = " %s" % msg_boilerplate
    if num_boilerplate < 100:
        msg_boilerplate = " %s" % msg_boilerplate
    if num_in_progress < 10:
        msg_in_progress = " %s" % msg_in_progress
    if num_in_progress < 100:
        msg_in_progress = " %s" % msg_in_progress
    gen_message = (
        '🗂️  Summary generated at "case_summary.md":'
        '\n🔵 %s'
        '\n⭕ %s'
        '\n🚧 %s'
        % (msg_ready_cases, msg_boilerplate, msg_in_progress)
    )
    print(gen_message)
    if num_ready_cases < 10:
        msg_ready_cases = " %s" % msg_ready_cases
    if num_ready_cases < 100:
        msg_ready_cases = " %s" % msg_ready_cases
    if num_boilerplate < 10:
        msg_boilerplate = " %s" % msg_boilerplate
    if num_boilerplate < 100:
        msg_boilerplate = " %s" % msg_boilerplate
    if num_in_progress < 10:
        msg_in_progress = " %s" % msg_in_progress
    if num_in_progress < 100:
        msg_in_progress = " %s" % msg_in_progress
    messagebox.showinfo(
        "Case Plans Summary generated!",
        '\nSummary generated at "case_summary.md"'
        '\n🔵 %s'
        '\n⭕ %s'
        '\n🚧 %s'
        % (msg_ready_cases, msg_boilerplate, msg_in_progress)
    )
    send_window_to_front(root)


def create_tkinter_gui(tests, command_string):
    root = tk.Tk()
    root.title("SeleniumBase Case Plans Generator")
    root.minsize(820, 652)
    tk.Label(root, text="").pack()
    run_display = (
        "Select from %s tests found:  "
        "(Boilerplate Case Plans will be generated as needed)"
        % len(tests)
    )
    if len(tests) == 1:
        run_display = (
            "Select from 1 test found:  "
            "(Boilerplate Case Plans will be generated as needed)"
        )
    run_display_2 = "(Tests with existing Case Plans are already checked)"
    tk.Label(root, text=run_display, fg="blue").pack()
    tk.Label(root, text=run_display_2, fg="purple").pack()
    text_area = ScrolledText(
        root, width=100, height=12, wrap="word", state=tk.DISABLED
    )
    text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    count = 0
    ara = {}
    tests_with_case_plan = []
    tests_without_case_plan = []
    for row in tests:
        row += " " * 200
        ara[count] = tk.IntVar()
        cb = None
        if not is_windows:
            cb = tk.Checkbutton(
                text_area,
                text=(row),
                bg="white",
                anchor="w",
                pady=0,
                variable=ara[count],
            )
        else:
            cb = tk.Checkbutton(
                text_area,
                text=(row),
                bg="white",
                anchor="w",
                pady=0,
                borderwidth=0,
                highlightthickness=0,
                variable=ara[count],
            )
        parts = row.strip().split("/")
        test_address = None
        folder_path = None
        if len(parts) == 1:
            test_address = parts[0]
        if len(parts) > 1:
            test_address = parts[-1]
            folder_path = "/".join(parts[0:-1])
        test_id = get_test_id(test_address)
        case_id = test_id + ".md"
        case_path = None
        if len(parts) == 1:
            case_path = os.path.join("case_plans", case_id)
        else:
            case_path = os.path.join(folder_path, "case_plans", case_id)
        if os.path.exists(case_path):
            cb.select()
            tests_with_case_plan.append(row.strip())
        else:
            tests_without_case_plan.append(row.strip())
        text_area.window_create("end", window=cb)
        text_area.insert("end", "\n")
        count += 1

    tk.Label(root, text="").pack()
    tk.Button(
        root,
        text=(
            "Generate boilerplate Case Plans "
            "for selected tests missing them"),
        fg="green",
        command=lambda: generate_case_plan_boilerplates(
            root,
            tests,
            ara,
            tests_with_case_plan,
            tests_without_case_plan,
        ),
    ).pack()

    tk.Label(root, text="").pack()
    tk.Button(
        root,
        text=(
            "Generate Summary of existing Case Plans"),
        fg="teal",
        command=lambda: view_summary_of_existing_case_plans(root, tests),
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
    message += "Case Plans"
    message += c4
    message += " Generator"
    message += c2
    message += "..."
    message += cr
    print(message)

    proc = subprocess.Popen(
        'pytest --co -q --rootdir="./" %s' % command_string,
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
    for row in output.decode("utf-8").split("\n"):
        if ("::") in row:
            tests.append(row)
    if not tests:
        error_msg = "No tests found! Exiting the Case Plans Generator..."
        error_msg = c5 + "ERROR: " + error_msg + cr
        print(error_msg)
        return

    create_tkinter_gui(tests, command_string)


if __name__ == "__main__":
    print('To open the Case Plans Generator, type "sbase caseplans"')
