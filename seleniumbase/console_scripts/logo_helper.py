""" SeleniumBase Logo Processing  (for the console scripts interface)
    Logo generated from:
    http://www.patorjk.com/software/taag/#p=display&f=Slant&t=SeleniumBase """

import colorama

r'''
   ______     __           _                 ____
  / ____/__  / /__  ____  (_)_  ______ ___  / __ `____  ________
  \__ \/ _ \/ / _ \/ __ \/ / / / / __ `__ \/ /_/ / __ `/ ___/ _ \
 ___/ /  __/ /  __/ / / / / /_/ / / / / / / /_) / /_/ (__  )  __/
/____/\___/_/\___/_/ /_/_/\__,_/_/ /_/ /_/_____/\__,_/____/\___/
'''


def get_seleniumbase_logo():
    colorama.init(autoreset=True)
    c1 = colorama.Fore.BLUE + colorama.Back.CYAN
    c2 = colorama.Fore.CYAN + colorama.Back.BLUE
    cr = colorama.Style.RESET_ALL
    sb = " "
    sb += c1
    sb += "\n"
    sb += c1
    sb += "   ______     __           _                 "
    sb += c2
    sb += "____                "
    sb += c1
    sb += "\n"
    sb += c1
    sb += "  / ____/__  / /__  ____  (_)_  ______ ___  "
    sb += c2
    sb += "/ __ `____  ________ "
    sb += c1
    sb += "\n"
    sb += c1
    sb += "  \\__ \\/ _ \\/ / _ \\/ __ \\/ / / / / __ `__ \\"
    sb += c2
    sb += "/ /_/ / __ `/ ___/ _ \\"
    sb += c1
    sb += "\n"
    sb += c1
    sb += " ___/ /  __/ /  __/ / / / / /_/ / / / / / "
    sb += c2
    sb += "/ /_) / /_/ (__  )  __/"
    sb += c1
    sb += "\n"
    sb += c1
    sb += "/____/\\___/_/\\___/_/ /_/_/\\__,_/_/ /_/ /_"
    sb += c2
    sb += "/_____/\\__,_/____/\\___/ "
    sb += c1
    sb += "\n"
    sb += c1
    sb += "                                        "
    sb += c2
    sb += "                         "
    sb += c1
    sb += cr
    return sb
