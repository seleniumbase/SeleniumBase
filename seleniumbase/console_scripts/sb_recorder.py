"""
** recorder **

Launches the SeleniumBase Recorder Desktop App.

Usage:
    seleniumbase recorder [OPTIONS]
           sbase recorder [OPTIONS]

Options:
    --uc / --undetected  (Use undetectable mode.)
    --cdp  (Same as "--uc" and "--undetectable".)
    --behave  (Also output Behave/Gherkin files.)

Output:
    Launches the SeleniumBase Recorder Desktop App.
"""
import colorama
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from contextlib import suppress
from seleniumbase import config as sb_config
from seleniumbase.core import detect_b_ver
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import shared_utils
from tkinter import messagebox

sb_config.rec_subprocess_p = None
sb_config.rec_subprocess_used = False
sys_executable = sys.executable
if " " in sys_executable:
    sys_executable = "python"


def set_colors(use_colors):
    c0 = ""
    c1 = ""
    c2 = ""
    c3 = ""
    c4 = ""
    cr = ""
    if use_colors:
        c0 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        c2 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c3 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTYELLOW_EX
        c4 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
        cr = colorama.Style.RESET_ALL
    return c0, c1, c2, c3, c4, cr


def send_window_to_front(window):
    window.lift()
    window.attributes("-topmost", True)
    window.after_idle(window.attributes, "-topmost", False)


def show_already_recording_warning():
    messagebox.showwarning(
        "SeleniumBase Recorder: Already Running!",
        "Please finalize the active recording from the terminal\n"
        'where you opened the Recorder: Type "c" and hit Enter.',
    )


def file_name_error(file_name):
    error_msg = None
    if not file_name.endswith(".py"):
        error_msg = 'File name must end with ".py"!'
    elif "*" in file_name or len(str(file_name)) < 4:
        error_msg = "Invalid file name!"
    elif file_name.startswith("-"):
        error_msg = 'File name cannot start with "-"!'
    elif "/" in str(file_name) or "\\" in str(file_name):
        error_msg = "File must be created in the current directory!"
    return error_msg


def do_recording(
    file_name,
    url,
    overwrite_enabled,
    brx,
    ucb,
    output_format,
    window,
):
    poll = None
    if sb_config.rec_subprocess_used:
        poll = sb_config.rec_subprocess_p.poll()
    if not sb_config.rec_subprocess_used or poll is not None:
        pass
    else:
        show_already_recording_warning()
        send_window_to_front(window)
        poll = sb_config.rec_subprocess_p.poll()
        if poll is None:
            return

    file_name = file_name.strip()
    error_msg = file_name_error(file_name)
    if error_msg:
        messagebox.showwarning(
            "Invalid filename", "Invalid filename: %s" % error_msg
        )
        return

    url = url.strip()
    if not page_utils.is_valid_url(url):
        if page_utils.is_valid_url("https://" + url):
            url = "https://" + url
    if "edge" in brx.lower() and ucb:
        messagebox.showwarning(
            "Invalid selection",
            "MS Edge cannot be combined with UC Mode "
            "because it uses msedgedriver, not chromedriver!",
        )
    elif not page_utils.is_valid_url(url):
        messagebox.showwarning(
            "Invalid URL", "Enter a valid URL! (Eg. seleniumbase.io)"
        )
    else:
        if os.path.exists(os.getcwd() + "/" + file_name):
            if not overwrite_enabled:
                msgbox = tk.messagebox.askquestion(
                    "Overwrite?",
                    'Are you sure you want to overwrite "%s"?' % file_name,
                    icon="warning",
                )
                if msgbox == "yes":
                    os.remove(file_name)
                else:
                    tk.messagebox.showinfo("Cancelled", "Recording Cancelled!")
                    return
            else:
                os.remove(file_name)
        add_on = ""
        if "Behave" in output_format:
            add_on = " --rec-behave"
        elif "SB()" in output_format:
            add_on = " --rec-sb-mgr"
        elif "sb_cdp" in output_format:
            add_on = " --rec-sb-cdp"
        command = (
            "%s -m seleniumbase mkrec %s --url=%s --gui"
            % (sys_executable, file_name, url)
        )
        if '"' not in url:
            command = (
                '%s -m seleniumbase mkrec %s --url="%s" --gui'
                % (sys_executable, file_name, url)
            )
        elif "'" not in url:
            command = (
                "%s -m seleniumbase mkrec %s --url='%s' --gui"
                % (sys_executable, file_name, url)
            )
        if "edge" in brx.lower():
            command += " --edge"
        elif "opera" in brx.lower():
            command += " --opera"
        elif "brave" in brx.lower():
            command += " --brave"
        elif "comet" in brx.lower():
            command += " --comet"
        elif "atlas" in brx.lower():
            command += " --atlas"
        elif "chromium" in brx.lower():
            command += " --use-chromium"
        if ucb:
            command += " --uc"
        command_args = sys.argv[2:]
        if "--ee" in command_args:
            command += " --ee"
        command += add_on
        poll = None
        if sb_config.rec_subprocess_used:
            poll = sb_config.rec_subprocess_p.poll()
        if not sb_config.rec_subprocess_used or poll is not None:
            sb_config.rec_subprocess_p = subprocess.Popen(command, shell=True)
            sb_config.rec_subprocess_used = True
        else:
            show_already_recording_warning()
        send_window_to_front(window)


def do_playback(file_name, brx, window, demo_mode=False):
    file_name = file_name.strip()
    error_msg = file_name_error(file_name)
    if error_msg:
        messagebox.showwarning(
            "Invalid filename", "Invalid filename: %s" % error_msg
        )
        return
    if not os.path.exists(os.getcwd() + "/" + file_name):
        messagebox.showwarning(
            "File does not exist",
            'File "%s" does not exist in the current directory!' % file_name,
        )
        return
    # command = "%s -m pytest %s -q -s" % (sys_executable, file_name)
    command = "%s %s -q -s" % (sys_executable, file_name)
    if shared_utils.is_linux():
        command += " --gui"
    if "edge" in brx.lower():
        command += " --edge"
    elif "opera" in brx.lower():
        command += " --opera"
    elif "brave" in brx.lower():
        command += " --brave"
    elif "comet" in brx.lower():
        command += " --comet"
    elif "atlas" in brx.lower():
        command += " --atlas"
    elif "chromium" in brx.lower():
        command += " --use-chromium"
    if demo_mode:
        command += " --demo"
    command_args = sys.argv[2:]
    if (
        "--uc" in command_args
        or "--cdp" in command_args
        or "--undetected" in command_args
        or "--undetectable" in command_args
    ):
        command += " --uc"
    poll = None
    if sb_config.rec_subprocess_used:
        poll = sb_config.rec_subprocess_p.poll()
    if not sb_config.rec_subprocess_used or poll is not None:
        print(command)
        subprocess.Popen(command, shell=True)
    else:
        messagebox.showwarning(
            "SeleniumBase Recorder: Already Running!",
            "Please finalize the active recording from the terminal\n"
            'where you opened the Recorder: Type "c" and hit Enter.',
        )
    send_window_to_front(window)


def create_tkinter_gui():
    default_file_name = "new_recording.py"
    window = tk.Tk()
    window.title("SeleniumBase Recorder App")
    window.geometry("344x564")
    my_font = ("TkDefaultFont", 11)
    frame = tk.Frame(window)
    frame.pack()

    fname = tk.StringVar(value=default_file_name)
    label = tk.Label(window, text="Enter filename to save recording as:")
    label.pack(pady=(20, 0.2))
    entry = tk.Entry(window, textvariable=fname)
    entry.config(width=21)
    entry.pack(pady=(0.6, 0.2))
    cbx = tk.IntVar()
    chk = tk.Checkbutton(window, text="Overwrite existing files", variable=cbx)
    chk.pack()
    chk.select()
    use_stealth = False
    use_behave = False
    use_sb_mgr = False
    use_sb_cdp = False
    use_atlas = False
    command_args = sys.argv[2:]
    if (
        "--uc" in command_args
        or "--cdp" in command_args
        or "--stealth" in command_args
        or "--undetected" in command_args
        or "--undetectable" in command_args
    ):
        use_stealth = True
    if (
        "--rec-behave" in command_args
        or "--behave" in command_args
        or "--gherkin" in command_args
    ):
        use_behave = True
    if "--rec-sb-mgr" in command_args:
        use_sb_mgr = True
    if "--rec-sb-cdp" in command_args:
        use_sb_cdp = True
    if "--atlas" in command_args:
        use_atlas = True

    tk.Label(window, text="\nSelect a web browser to use:").pack()
    br_count = 2
    br_order = {"chrome": 0, "chromium": 1}
    options_list = ["Google Chrome"]
    options_list.append("Chromium Browser")
    if shared_utils.is_windows():
        options_list.append("MS Edge  (No Stealth)")
        br_order["edge"] = br_count
        br_count += 1
    else:
        with suppress(Exception):
            if os.path.exists(detect_b_ver.get_binary_location("edge")):
                options_list.append("MS Edge  (No Stealth)")
                br_order["edge"] = br_count
                br_count += 1
    with suppress(Exception):
        if os.path.exists(detect_b_ver.get_binary_location("opera")):
            options_list.append("Opera Browser")
            br_order["opera"] = br_count
            br_count += 1
    with suppress(Exception):
        if os.path.exists(detect_b_ver.get_binary_location("brave")):
            options_list.append("Brave Browser")
            br_order["brave"] = br_count
            br_count += 1
    with suppress(Exception):
        if os.path.exists(detect_b_ver.get_binary_location("comet")):
            options_list.append("Comet Browser")
            br_order["comet"] = br_count
            br_count += 1
    if use_atlas:
        with suppress(Exception):
            if os.path.exists(detect_b_ver.get_binary_location("atlas")):
                options_list.append("Atlas Browser")
                br_order["atlas"] = br_count
                br_count += 1
    brx = tk.StringVar(window)
    if "--use-chromium" in command_args or "--chromium" in command_args:
        brx.set(options_list[1])
    elif (
        "--edge" in command_args
        and "edge" in br_order
    ):
        brx.set(options_list[2])
        use_stealth = False
    elif "--opera" in command_args and "opera" in br_order:
        brx.set(options_list[br_order["opera"]])
    elif "--brave" in command_args and "brave" in br_order:
        brx.set(options_list[br_order["brave"]])
    elif "--comet" in command_args and "comet" in br_order:
        brx.set(options_list[br_order["comet"]])
    elif "--atlas" in command_args and "atlas" in br_order:
        brx.set(options_list[br_order["atlas"]])
    else:
        brx.set(options_list[0])
    question_menu = tk.OptionMenu(window, brx, *options_list)
    question_menu.config(width=16)
    question_menu.pack(pady=(0.6, 0.2))

    ucb = tk.IntVar()
    chkb = tk.Checkbutton(
        window, text="Stealth Mode / UC + CDP Mode", variable=ucb
    )
    chkb.pack(pady=(0.4, 0.4))
    if use_stealth:
        chkb.select()
        # chkb.config(state=tk.DISABLED)

    tk.Label(window, text="\nSelect an output format to use:").pack()
    options_list = ["pytest format / BaseCase"]
    options_list.append("Context Manager / SB()")
    options_list.append("Pure CDP Mode / sb_cdp")
    if use_behave:
        options_list.append("BehaveBDD Gherkin File")
    frx = tk.StringVar(window)
    if use_behave and not use_sb_mgr and not use_sb_cdp:
        frx.set(options_list[3])
    elif use_sb_mgr:
        frx.set(options_list[1])
    elif use_sb_cdp:
        frx.set(options_list[2])
    else:
        frx.set(options_list[0])
    question_menu = tk.OptionMenu(window, frx, *options_list)
    question_menu.config(width=18)
    question_menu.pack(pady=(0.6, 0.2))

    url = tk.StringVar()
    label = tk.Label(window, text="Enter a URL to start recording on:")
    label.pack(pady=(20, 0.2))
    entry = tk.Entry(window, textvariable=url)
    entry.config(width=23)
    entry.pack()
    entry.focus()
    entry.bind(
        "<Return>",
        (
            lambda _: do_recording(
                fname.get(),
                url.get(),
                cbx.get(),
                brx.get(),
                ucb.get(),
                frx.get(),
                window,
            )
        ),
    )
    # Automatically set focus on URL field when clicking back into the app
    window.bind(
        "<FocusIn>", lambda event: entry.focus_set()
        if event.widget == window
        else None
    )
    style = ttk.Style()
    style.configure(
        "Record.TButton",
        foreground="red",
        font=("TkDefaultFont", 12, "bold"),
        width="8",
        padding=(4, 3, 4, 1)
    )
    ttk.Button(
        window,
        text="Record",
        style="Record.TButton",
        command=lambda: do_recording(
            fname.get(),
            url.get(),
            cbx.get(),
            brx.get(),
            ucb.get(),
            frx.get(),
            window,
        ),
    ).pack(pady=0.2)
    label = tk.Label(window, text="Playback recording (Normal Mode):")
    label.pack(pady=(18, 0))

    style.configure(
        "Playback.TButton",
        foreground="green",
        font=("TkDefaultFont", 11, "bold"),
        width="8",
        padding=(4, 3, 4, 1)
    )
    ttk.Button(
        window,
        text="Playback",
        style="Playback.TButton",
        command=lambda: do_playback(fname.get(), brx.get(), window),
    ).pack(pady=0.2)
    label = tk.Label(window, text="Playback recording (Demo Mode):")
    label.pack(pady=(14, 0))
    try:
        style.configure(
            "PlaybackDemo.TButton",
            foreground="teal",
            font=("TkDefaultFont", 11, "bold"),
            width="16",
            padding=(4, 3, 4, 1)
        )
        ttk.Button(
            window,
            text="Playback (Demo Mode)",
            style="PlaybackDemo.TButton",
            command=lambda: do_playback(
                fname.get(), brx.get(), window, demo_mode=True
            ),
        ).pack(pady=0.2)
    except Exception:
        style.configure(
            "PlaybackDemo.TButton",
            foreground="blue",
            font=("TkDefaultFont", 11, "bold"),
            padding=(4, 3, 4, 1)
        )
        ttk.Button(
            window,
            text="Playback (Demo Mode)",
            style="PlaybackDemo.TButton",
            command=lambda: do_playback(
                fname.get(), brx.get(), window, demo_mode=True
            ),
        ).pack(pady=0.2)

    # Bring form window to front
    send_window_to_front(window)
    # Use decoy to set correct focus on main window
    decoy = tk.Tk()
    decoy.geometry("1x1")
    decoy.iconify()
    decoy.update()
    decoy.deiconify()
    decoy.destroy()
    # Start tkinter
    for widget in window.winfo_children():
        if isinstance(
            widget, (tk.Label, tk.Entry, tk.Checkbutton, tk.OptionMenu)
        ):
            widget.configure(font=my_font)
    window.deiconify()  # Force the OS to redraw it actively on top
    window.focus_force()  # Force keyboard focus into the entry fields
    window.mainloop()
    end_program()


def recorder_still_running():
    poll = None
    if sb_config.rec_subprocess_used:
        try:
            poll = sb_config.rec_subprocess_p.poll()
        except Exception:
            return False
    else:
        return False
    if poll is not None:
        return False
    return True


def show_still_running_warning():
    """Give the user a chance to end the recording safely via the
    pytest pdb Debug Mode so that processes such as chromedriver
    and Python don't remain open and hanging in the background."""
    messagebox.showwarning(
        "SeleniumBase Recorder: Still Running!",
        "Please finalize the active recording from the terminal\n"
        'where you opened the Recorder: Type "c" and hit Enter.\n'
        "(Then you can safely close this alert.)",
    )


def end_program():
    if recorder_still_running():
        show_still_running_warning()


def main():
    use_colors = True
    if shared_utils.is_linux():
        use_colors = False
    c0, c1, c2, c3, c4, cr = set_colors(use_colors)
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
    message += "Recorder"
    message += c4
    message += " Desktop App"
    message += c2
    message += "..."
    message += cr
    print(message)
    create_tkinter_gui()


if __name__ == "__main__":
    print('To open the Recorder Desktop App: "seleniumbase recorder"')
