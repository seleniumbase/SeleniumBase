# -*- coding: utf-8 -*-
"""
Creates a new SeleniumBase test file with boilerplate code.

Usage:
    seleniumbase mkfile [FILE.py] [OPTIONS]
    or     sbase mkfile [FILE.py] [OPTIONS]

Example:
    sbase mkfile new_test.py

Options:
    -b / --basic  (Basic boilerplate / single-line test)

Language Options:
    --en / --English    |    --zh / --Chinese
    --nl / --Dutch      |    --fr / --French
    --it / --Italian    |    --ja / --Japanese
    --ko / --Korean     |    --pt / --Portuguese
    --ru / --Russian    |    --es / --Spanish

Output:
    Creates a new SBase test file with boilerplate code.
    If the file already exists, an error is raised.
    By default, uses English mode and creates a
    boilerplate with the 5 most common SeleniumBase
    methods, which are "open", "type", "click",
    "assert_element", and "assert_text". If using the
    basic boilerplate option, only the "open" method
    is included.
"""

import codecs
import colorama
import os
import sys


def invalid_run_command(msg=None):
    exp = "  ** mkfile **\n\n"
    exp += "  Usage:\n"
    exp += "          seleniumbase mkfile [FILE.py] [OPTIONS]\n"
    exp += "          OR     sbase mkfile [FILE.py] [OPTIONS]\n"
    exp += "  Example:\n"
    exp += "          sbase mkfile new_test.py\n"
    exp += "  Options:\n"
    exp += "          -b / --basic  (Basic boilerplate / single-line test)\n"
    exp += "  Language Options:\n"
    exp += "          --en / --English    |    --zh / --Chinese\n"
    exp += "          --nl / --Dutch      |    --fr / --French\n"
    exp += "          --it / --Italian    |    --ja / --Japanese\n"
    exp += "          --ko / --Korean     |    --pt / --Portuguese\n"
    exp += "          --ru / --Russian    |    --es / --Spanish\n"
    exp += "  Output:\n"
    exp += "          Creates a new SBase test file with boilerplate code.\n"
    exp += "          If the file already exists, an error is raised.\n"
    exp += "          By default, uses English mode and creates a\n"
    exp += "          boilerplate with the 5 most common SeleniumBase\n"
    exp += '          methods, which are "open", "type", "click",\n'
    exp += '          "assert_element", and "assert_text". If using the\n'
    exp += '          basic boilerplate option, only the "open" method\n'
    exp += "          is included.\n"
    if not msg:
        raise Exception("INVALID RUN COMMAND!\n\n%s" % exp)
    elif msg == "help":
        print("\n%s" % exp)
        sys.exit()
    else:
        raise Exception("INVALID RUN COMMAND!\n\n%s\n%s\n" % (exp, msg))


def main():
    c1 = ""
    c5 = ""
    c7 = ""
    cr = ""
    if "linux" not in sys.platform:
        colorama.init(autoreset=True)
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
        cr = colorama.Style.RESET_ALL

    basic = False
    help_me = False
    error_msg = None
    invalid_cmd = None
    language = "English"

    command_args = sys.argv[2:]
    file_name = command_args[0]
    if file_name == "-h" or file_name == "--help":
        invalid_run_command("help")
    elif not file_name.endswith(".py"):
        error_msg = 'File name must end with ".py"!'
    elif "*" in file_name or len(str(file_name)) < 4:
        error_msg = "Invalid file name!"
    elif file_name.startswith("-"):
        error_msg = 'File name cannot start with "-"!'
    elif "/" in str(file_name) or "\\" in str(file_name):
        error_msg = "File must be created in the current directory!"
    elif os.path.exists(os.getcwd() + "/" + file_name):
        error_msg = 'File "%s" already exists in this directory!' % file_name
    if error_msg:
        error_msg = c5 + "ERROR: " + error_msg + cr
        invalid_run_command(error_msg)

    if len(command_args) >= 2:
        options = command_args[1:]
        for option in options:
            option = option.lower()
            if option == "-h" or option == "--help":
                help_me = True
            elif option == "-b" or option == "--basic":
                basic = True
            elif option == "--en" or option == "--english":
                language = "English"
            elif option == "--zh" or option == "--chinese":
                language = "Chinese"
            elif option == "--nl" or option == "--dutch":
                language = "Dutch"
            elif option == "--fr" or option == "--french":
                language = "French"
            elif option == "--it" or option == "--italian":
                language = "Italian"
            elif option == "--ja" or option == "--japanese":
                language = "Japanese"
            elif option == "--ko" or option == "--korean":
                language = "Korean"
            elif option == "--pt" or option == "--portuguese":
                language = "Portuguese"
            elif option == "--ru" or option == "--russian":
                language = "Russian"
            elif option == "--es" or option == "--spanish":
                language = "Spanish"
            else:
                invalid_cmd = "\n===> INVALID OPTION: >> %s <<\n" % option
                invalid_cmd = invalid_cmd.replace(">> ", ">>" + c5 + " ")
                invalid_cmd = invalid_cmd.replace(" <<", " " + cr + "<<")
                invalid_cmd = invalid_cmd.replace(">>", c7 + ">>" + cr)
                invalid_cmd = invalid_cmd.replace("<<", c7 + "<<" + cr)
                help_me = True
                break
    if help_me:
        invalid_run_command(invalid_cmd)

    if language != "English" and sys.version_info[0] == 2:
        print("")
        msg = 'Multi-language support for "sbase mkfile" '
        msg += "is not available on Python 2!"
        msg = "\n" + c5 + msg + cr
        msg += '\nPlease run in "English" mode or upgrade to Python 3!\n'
        raise Exception(msg)

    dir_name = os.getcwd()
    file_path = "%s/%s" % (dir_name, file_name)

    body = "html > body"
    para = "body p"
    hello = "Hello"
    goodbye = "Goodbye"
    class_name = "MyTestClass"
    if language == "Chinese":
        hello = "你好"
        goodbye = "再见"
        class_name = "我的测试类"
    elif language == "Dutch":
        hello = "Hallo"
        goodbye = "Dag"
        class_name = "MijnTestklasse"
    elif language == "French":
        hello = "Bonjour"
        goodbye = "Au revoir"
        class_name = "MaClasseDeTest"
    elif language == "Italian":
        hello = "Ciao"
        goodbye = "Addio"
        class_name = "MiaClasseDiTest"
    elif language == "Japanese":
        hello = "こんにちは"
        goodbye = "さようなら"
        class_name = "私のテストクラス"
    elif language == "Korean":
        hello = "여보세요"
        goodbye = "안녕"
        class_name = "테스트_클래스"
    elif language == "Portuguese":
        hello = "Olá"
        goodbye = "Tchau"
        class_name = "MinhaClasseDeTeste"
    elif language == "Russian":
        hello = "Привет"
        goodbye = "До свидания"
        class_name = "МойТестовыйКласс"
    elif language == "Spanish":
        hello = "Hola"
        goodbye = "Adiós"
        class_name = "MiClaseDePrueba"
    url = ""
    if basic:
        url = "about:blank"
    elif language not in ["English", "Dutch", "French", "Italian"]:
        url = "data:text/html,<meta charset='utf-8'><p>%s <input>" % hello
    else:
        url = "data:text/html,<p>%s<br><input></p>" % hello

    import_line = "from seleniumbase import BaseCase"
    parent_class = "BaseCase"
    class_line = "class MyTestClass(BaseCase):"
    if language != "English":
        from seleniumbase.translate.master_dict import MD_F

        import_line = MD_F.get_import_line(language)
        parent_class = MD_F.get_lang_parent_class(language)
    class_line = "class %s(%s):" % (class_name, parent_class)

    data = []
    data.append("%s" % import_line)
    data.append("")
    data.append("")
    data.append("%s" % class_line)
    data.append("    def test_base(self):")
    data.append('        self.open("%s")' % url)
    if not basic:
        data.append('        self.assert_element("%s")  # selector' % body)
        data.append(
            '        self.assert_text("%s", "%s")'
            "  # text, selector" % (hello, para)
        )
        data.append(
            '        self.type("input", "%s")' "  # selector, text" % goodbye
        )
        data.append('        self.click("%s")  # selector' % para)
    data.append("")

    new_data = []
    if language == "English":
        new_data = data
    else:
        from seleniumbase.translate.master_dict import MD
        from seleniumbase.translate.master_dict import MD_L_Codes

        md = MD.md
        lang_codes = MD_L_Codes.lang
        nl_code = lang_codes[language]
        dl_code = lang_codes["English"]
        for line in data:
            found_swap = False
            replace_count = line.count("self.")  # Total possible replacements
            for key in md.keys():
                original = "self." + md[key][dl_code] + "("
                if original in line:
                    replacement = "self." + md[key][nl_code] + "("
                    new_line = line.replace(original, replacement)
                    found_swap = True
                    replace_count -= 1
                    if replace_count == 0:
                        break  # Done making replacements
                    else:
                        # There might be another method to replace in the line.
                        # Example: self.assert_true("Name" in self.get_title())
                        line = new_line
                        continue
            if found_swap:
                if new_line.endswith("  # noqa"):  # Remove flake8 skip
                    new_line = new_line[0 : -len("  # noqa")]
                new_data.append(new_line)
                continue
            new_data.append(line)
    data = new_data
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()
    success = (
        "\n" + c1 + '* Test file: "' + file_name + '" was created! *'
        "" + cr + "\n"
    )
    print(success)


if __name__ == "__main__":
    invalid_run_command()
