# -*- coding: utf-8 -*-
"""
Launches the SeleniumBase Recorder Desktop App.

Usage:
      seleniumbase recorder
             sbase recorder

Output:
    Launches the SeleniumBase Recorder Desktop App.
"""

import colorama
import os
import sys
from seleniumbase.fixtures import page_utils

if sys.version_info[0] < 3:
    raise Exception("This script is for Python 3 only!")
import tkinter as tk  # noqa: E402
from tkinter import messagebox  # noqa: E402


def set_colors(use_colors):
    c0 = ""
    c1 = ""
    c2 = ""
    c3 = ""
    cr = ""
    if use_colors:
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
    file_name = file_name.strip()
    error_msg = file_name_error(file_name)
    if error_msg:
        messagebox.showwarning(
            "Invalid filename", "Invalid filename: %s" % error_msg)
        return

    url = url.strip()
    if not page_utils.is_valid_url(url):
        if page_utils.is_valid_url("https://" + url):
            url = "https://" + url
    if not page_utils.is_valid_url(url):
        messagebox.showwarning(
            "Invalid URL", "Enter a valid URL! (Eg. seleniumbase.io)")
    else:
        if os.path.exists(os.getcwd() + "/" + file_name):
            if not overwrite_enabled:
                msgbox = tk.messagebox.askquestion(
                    "Overwrite?",
                    'Are you sure you want to overwrite "%s"?' % file_name,
                    icon="warning"
                )
                if msgbox == "yes":
                    os.remove(file_name)
                else:
                    tk.messagebox.showinfo("Cancelled", "Recording Cancelled!")
                    return
            else:
                os.remove(file_name)
        command = "python -m sbase mkrec %s --url=%s" % (file_name, url)
        if not use_chrome:
            command += " --edge"
        os.system(command)
        send_window_to_front(window)


def do_playback(file_name, use_chrome, window, demo_mode=False):
    file_name = file_name.strip()
    error_msg = file_name_error(file_name)
    if error_msg:
        messagebox.showwarning(
            "Invalid filename", "Invalid filename: %s" % error_msg)
        return
    if not os.path.exists(os.getcwd() + "/" + file_name):
        messagebox.showwarning(
            "File does not exist",
            'File "%s" does not exist in the current directory!' % file_name
        )
        return
    command = "pytest %s -q -s" % file_name
    if not use_chrome:
        command += " --edge"
    if demo_mode:
        command += " --demo"
    print(command)
    os.system(command)
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
        (lambda _: do_recording(
            fname.get(), url.get(), cbx.get(), cbb.get(), window))
    )
    tk.Button(
        window, text="Record", fg="red",
        command=lambda: do_recording(
            fname.get(), url.get(), cbx.get(), cbb.get(), window)
    ).pack()
    tk.Label(window, text="").pack()
    tk.Label(
        window, text="Playback recording (Normal Mode):").pack()
    tk.Button(
        window, text="Playback", fg="green",
        command=lambda: do_playback(fname.get(), cbb.get(), window)
    ).pack()
    tk.Label(window, text="").pack()
    tk.Label(
        window, text="Playback recording (Demo Mode):").pack()
    tk.Button(
        window, text="Playback (Demo Mode)", fg="teal",
        command=lambda: do_playback(
            fname.get(), cbb.get(), window, demo_mode=True)).pack()

    # Bring form window to front
    send_window_to_front(window)
    window.mainloop()


def main():
    use_colors = True
    if "linux" in sys.platform:
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
    print('To open the Recorder Desktop App: "sbase recorder"')
