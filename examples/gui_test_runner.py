'''
GUI TEST RUNNER
Run by Typing: "python gui_test_runner.py"
'''

try:
    # Python 2
    from Tkinter import Tk, Frame, Button, Label
except Exception:
    # Python 3
    from tkinter import Tk, Frame, Button, Label
import os


class App:

    def __init__(self, master):
        frame = Frame()
        frame.pack()
        root.title("Select Test Job To Run")
        self.label = Label(root, width=40).pack()
        self.title = Label(frame, text="", fg="black").pack()
        self.title1 = Label(
            frame, text="Basic Test Run in Chrome:", fg="blue").pack()
        self.run1 = Button(
            frame, command=self.run_1,
            text=("pytest my_first_test.py"
                  " --browser=chrome")).pack()
        self.title2 = Label(
            frame, text="Basic Test Run in Firefox:", fg="blue").pack()
        self.run2 = Button(
            frame, command=self.run_2,
            text=("pytest my_first_test.py"
                  " --browser=firefox")).pack()
        self.title3 = Label(
            frame, text="Basic Test Run in Demo Mode:", fg="blue").pack()
        self.run3 = Button(
            frame, command=self.run_3,
            text=("pytest my_first_test.py"
                  " --browser=chrome --demo_mode")).pack()
        self.title4 = Label(
            frame,
            text="Basic Failing Test Run with Screenshots:",
            fg="blue").pack()
        self.run4 = Button(
            frame, command=self.run_4,
            text=("nosetests test_fail.py"
                  " --browser=chrome --demo_mode")).pack()
        self.title5 = Label(
            frame,
            text="Basic Failing Test Suite Run with Test Report:",
            fg="blue").pack()
        self.run5 = Button(
            frame, command=self.run_5,
            text=("nosetests my_test_suite.py --report --show_report")).pack()
        self.title6 = Label(
            frame,
            text="Basic Failing Test Run showing the Multiple-Checks feature:",
            fg="blue").pack()
        self.run6 = Button(
            frame, command=self.run_6,
            text=("nosetests delayed_assert_test.py --browser=chrome")).pack()
        self.title7 = Label(
            frame,
            text="Use MySQL DB Reporting: (See ReadMe.md for Setup Steps!)",
            fg="blue").pack()
        self.run7 = Button(
            frame, command=self.run_7,
            text=("nosetests my_test_suite.py"
                  " --browser=chrome --with-db_reporting")).pack()
        self.end_title = Label(frame, text="", fg="black").pack()
        self.quit = Button(frame, text="QUIT", command=frame.quit).pack()

    def run_1(self):
        os.system(
            'pytest my_first_test.py --browser=chrome')

    def run_2(self):
        os.system(
            'pytest my_first_test.py --browser=firefox')

    def run_3(self):
        os.system(
            'pytest my_first_test.py --demo_mode'
            ' --browser=chrome')

    def run_4(self):
        os.system(
            'nosetests test_fail.py --browser=chrome --demo_mode')

    def run_5(self):
        os.system(
            'nosetests my_test_suite.py --report --show_report')

    def run_6(self):
        os.system(
            'nosetests delayed_assert_test.py --browser=chrome')

    def run_7(self):
        os.system(
            'nosetests my_test_suite.py'
            ' --browser=chrome --with-db_reporting')


if __name__ == "__main__":
    root = Tk()
    root.minsize(532, 444)
    app = App(root)
    root.mainloop()
