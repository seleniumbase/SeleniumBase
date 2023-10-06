""" SeleniumBase Logo Processing  (for the console scripts interface)
    Logo generated from:
    http://www.patorjk.com/software/taag/#p=display&f=Slant&t=SeleniumBase """

import colorama
import sys

r"""
   ______     __           _                  ____
  / ____/__  / /__  ____  (_)_  ______ ___   / _  \____  ________
  \__ \/ _ \/ / _ \/ __ \/ / / / / __ `__ \ / /_) / __ \/ ___/ _ \
 ___/ /  __/ /  __/ / / / / /_/ / / / / / // /_) / (_/ /__  /  __/
/____/\___/_/\___/_/ /_/_/\__,_/_/ /_/ /_//_____/\__,_/____/\___/
"""


def get_seleniumbase_logo():
    if (
        "win32" in sys.platform
        and hasattr(colorama, "just_fix_windows_console")
    ):
        colorama.just_fix_windows_console()
    else:
        colorama.init(autoreset=True)
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Back.CYAN
    c4 = colorama.Back.GREEN
    cr = colorama.Style.RESET_ALL
    sb = " "
    sb += cr
    sb += "\n"
    sb += c1
    sb += "   ______     __           _                  "
    sb += c2
    sb += "____                "
    sb += cr
    sb += "\n"
    sb += c1
    sb += "  / ____/__  / /__  ____  (_)_  ______ ___   "
    sb += c2
    sb += "/ _  \\____  ________ "
    sb += cr
    sb += "\n"
    sb += c1
    sb += "  \\__ \\/ _ \\/ / _ \\/ __ \\/ / / / / __ `__ \\ "
    sb += c2
    sb += "/ /_) / __ \\/ ___/ _ \\"
    sb += cr
    sb += "\n"
    sb += c1
    sb += " ___/ /  __/ /  __/ / / / / /_/ / / / / / /"
    sb += c2
    sb += "/ /_) / (_/ /__  /  __/"
    sb += cr
    sb += "\n"
    sb += c1
    sb += "/____/\\___/_/\\___/_/ /_/_/\\__,_/_/ /_/ /_/"
    sb += c2
    sb += "/_____/\\__,_/____/\\___/ "
    sb += cr
    sb += "\n"
    sb += c3
    sb += "                                          "
    sb += c4
    sb += "                        "
    sb += cr
    sb += cr
    return sb
