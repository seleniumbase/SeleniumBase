"""
** recorder **

Launches the SeleniumBase Recorder Desktop App.

Usage:
    seleniumbase recorder [OPTIONS]
           sbase recorder [OPTIONS]

Options:
    --uc / --undetected  (Use undetectable mode.)
    --behave  (Also output Behave/Gherkin files.)

Output:
    Launches the SeleniumBase Recorder Desktop App.
"""
import colorama
import os
import subprocess
import sys
from seleniumbase import config as sb_config
from seleniumbase.fixtures import page_utils
from seleniumbase.fixtures import shared_utils

sb_config.rec_subprocess_p = None
sb_config.rec_subprocess_used = False
sys_executable = sys.executable
if " " in sys_executable:
    sys_executable = "python"
if sys.version_info <= (3, 7):
    current_version = ".".join(str(ver) for ver in sys.version_info[:3])
    raise Exception(
        "\n* Recorder Desktop requires Python 3.7 or newer!"
        "\n*** You are currently using Python %s" % current_version
    )
import tkinter as tk  # noqa: E402
from tkinter import messagebox  # noqa: E402


def set_colors(use_colors):
    c0 = ""
    c1 = ""
    c2 = ""
    c3 = ""
    c4 = ""
    cr = ""
    if use_colors:
        if (
            "win32" in sys.platform
            and hasattr(colorama, "just_fix_windows_console")
        ):
            colorama.just_fix_windows_console()
        else:
            colorama.init(autoreset=True)
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


def do_recording(file_name, url, overwrite_enabled, use_chrome, window):
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
    if not page_utils.is_valid_url(url):
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
        command_args = sys.argv[2:]
        if (
            "--rec-behave" in command_args
            or "--behave" in command_args
            or "--gherkin" in command_args
        ):
            add_on = " --rec-behave"
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
        if not use_chrome:
            command += " --edge"
        if (
            "--uc" in command_args
            or "--undetected" in command_args
            or "--undetectable" in command_args
        ):
            command += " --uc"
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


def do_playback(file_name, use_chrome, window, demo_mode=False):
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
    command = "%s -m pytest %s -q -s" % (sys_executable, file_name)
    if shared_utils.is_linux():
        command += " --gui"
    if not use_chrome:
        command += " --edge"
    if demo_mode:
        command += " --demo"
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
    window.geometry("344x388")
    frame = tk.Frame(window)
    frame.pack()

    tk.Label(window, text="").pack()
    fname = tk.StringVar(value=default_file_name)
    tk.Label(window, text="Enter filename to save recording as:").pack()
    entry = tk.Entry(window, textvariable=fname)
    entry.pack()
    cbx = tk.IntVar()
    chk = tk.Checkbutton(window, text="Overwrite existing files", variable=cbx)
    chk.pack()
    chk.select()
    cbb = tk.IntVar()
    chkb = tk.Checkbutton(window, text="Use Chrome over Edge", variable=cbb)
    chkb.pack()
    chkb.select()
    tk.Label(window, text="").pack()
    url = tk.StringVar()
    tk.Label(window, text="Enter the URL to start recording on:").pack()
    entry = tk.Entry(window, textvariable=url)
    entry.pack()
    entry.focus()
    entry.bind(
        "<Return>",
        (
            lambda _: do_recording(
                fname.get(), url.get(), cbx.get(), cbb.get(), window
            )
        ),
    )
    tk.Button(
        window,
        text="Record",
        fg="red",
        command=lambda: do_recording(
            fname.get(), url.get(), cbx.get(), cbb.get(), window
        ),
    ).pack()
    tk.Label(window, text="").pack()
    tk.Label(window, text="Playback recording (Normal Mode):").pack()
    tk.Button(
        window,
        text="Playback",
        fg="green",
        command=lambda: do_playback(fname.get(), cbb.get(), window),
    ).pack()
    tk.Label(window, text="").pack()
    tk.Label(window, text="Playback recording (Demo Mode):").pack()
    try:
        tk.Button(
            window,
            text="Playback (Demo Mode)",
            fg="teal",
            command=lambda: do_playback(
                fname.get(), cbb.get(), window, demo_mode=True
            ),
        ).pack()
    except Exception:
        tk.Button(
            window,
            text="Playback (Demo Mode)",
            fg="blue",
            command=lambda: do_playback(
                fname.get(), cbb.get(), window, demo_mode=True
            ),
        ).pack()

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
