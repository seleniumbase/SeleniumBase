""" Run this file using `python recorder.py` """

import os
import sys
from seleniumbase.fixtures import page_utils

if sys.version_info[0] < 3:
    raise Exception("This script is for Python 3 only!")
import tkinter as tk
from tkinter import messagebox  # noqa: E402


def do_recording(file_name, url):
    url = url.strip()
    if not page_utils.is_valid_url(url):
        if page_utils.is_valid_url("https://" + url):
            url = "https://" + url
    if not page_utils.is_valid_url(url):
        messagebox.showwarning(
            "Invalid URL", "Enter a valid URL. (Eg. https://google.com)")
    else:
        if os.path.exists(file_name):
            os.remove(file_name)
        os.system("python -m sbase mkrec %s --url=%s" % (file_name, url))


def do_playback(file_name):
    os.system("pytest %s --verbose --capture=no" % file_name)


def create_tkinter_gui(file_name):
    window = tk.Tk()
    window.title("Recorder App")
    window.geometry("360x175")
    frame = tk.Frame(window)
    frame.pack()

    a = tk.StringVar()
    tk.Label(window, text="Enter URL to start recording on:").pack()
    entry = tk.Entry(window, textvariable=a)
    entry.pack()
    entry.focus()
    entry.bind("<Return>", (lambda _: do_recording(file_name, a.get())))
    tk.Button(
        window, text="Record", command=lambda: do_recording(file_name, a.get())
    ).pack()
    tk.Label(window, text="").pack()
    tk.Label(
        window, text="Playback the latest recording:").pack()
    tk.Button(
        window, text="Playback", command=lambda: do_playback(file_name)
    ).pack()

    # Bring form to front
    window.lift()
    window.attributes("-topmost", True)
    window.after_idle(window.attributes, "-topmost", False)
    window.mainloop()


if __name__ == "__main__":
    file_name = "new_recording.py"
    create_tkinter_gui(file_name)
