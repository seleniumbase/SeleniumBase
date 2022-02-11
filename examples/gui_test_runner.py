"""
GUI TEST RUNNER
Run by Typing: "python gui_test_runner.py"
(Use Python 3 - There are GUI issues when using Python 2)
"""

import subprocess
import sys

if sys.version_info[0] >= 3:
    from tkinter import Tk, Frame, Button, Label
else:
    from Tkinter import Tk, Frame, Button, Label


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.label = Label(root, width=40).pack()
        self.title = Label(frame, text="", fg="black").pack()
        self.title1 = Label(
            frame,
            text=("Run a Test in Chrome (default):"),
            fg="blue",
        ).pack()
        self.run1 = Button(
            frame,
            command=self.run_1,
            text=("pytest my_first_test.py"),
            fg="green",
        ).pack()
        self.title2 = Label(
            frame,
            text=("Run a Test in Firefox:"),
            fg="blue",
        ).pack()
        self.run2 = Button(
            frame,
            command=self.run_2,
            text=("pytest my_first_test.py --firefox"),
            fg="green",
        ).pack()
        self.title3 = Label(
            frame,
            text="Run a Test with Demo Mode:",
            fg="blue",
        ).pack()
        self.run3 = Button(
            frame,
            command=self.run_3,
            text=("pytest my_first_test.py --demo_mode"),
            fg="green",
        ).pack()
        self.title4 = Label(
            frame,
            text="Run a Parameterized Test and reuse session:",
            fg="blue",
        ).pack()
        self.run4 = Button(
            frame,
            command=self.run_4,
            text=("pytest parameterized_test.py --rs"),
            fg="green",
        ).pack()
        self.title5 = Label(
            frame,
            text="Run a Failing Test with a Test Report:",
            fg="blue",
        ).pack()
        self.run5 = Button(
            frame,
            command=self.run_5,
            text=("pytest test_fail.py --html=report.html"),
            fg="red",
        ).pack()
        self.title6 = Label(
            frame,
            text="Run a Failing Test Suite with the Dashboard:",
            fg="blue",
        ).pack()
        self.run6 = Button(
            frame,
            command=self.run_6,
            text=("pytest test_suite.py --rs --dashboard"),
            fg="red",
        ).pack()
        self.title7 = Label(
            frame,
            text="Run a Failing Test with Deferred Asserts:",
            fg="blue",
        ).pack()
        self.run7 = Button(
            frame,
            command=self.run_7,
            text=("pytest test_deferred_asserts.py"),
            fg="red",
        ).pack()
        self.end_title = Label(frame, text="", fg="black").pack()
        self.quit = Button(frame, text="QUIT", command=frame.quit).pack()

    def run_1(self):
        subprocess.Popen("pytest my_first_test.py", shell=True)

    def run_2(self):
        subprocess.Popen("pytest my_first_test.py --firefox", shell=True)

    def run_3(self):
        subprocess.Popen("pytest my_first_test.py --demo_mode", shell=True)

    def run_4(self):
        subprocess.Popen("pytest parameterized_test.py --rs", shell=True)

    def run_5(self):
        subprocess.Popen("pytest test_fail.py --html=report.html", shell=True)

    def run_6(self):
        subprocess.Popen("pytest test_suite.py --rs --dashboard", shell=True)

    def run_7(self):
        subprocess.Popen("pytest test_deferred_asserts.py", shell=True)


if __name__ == "__main__":
    root = Tk()
    root.title("Select Test Job To Run")
    root.minsize(320, 420)
    app = App(root)
    root.mainloop()
