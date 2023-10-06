"""
Creates a new SeleniumBase test file with boilerplate code.

Usage:
    seleniumbase mkfile [FILE.py] [OPTIONS]
    or     sbase mkfile [FILE.py] [OPTIONS]

Example:
    sbase mkfile new_test.py

Options:
    -b / --basic  (Basic boilerplate / single-line test)
    -r / --rec  (adds Pdb+ breakpoint for Recorder Mode)
    --url=URL  (makes the test start on a specific page)

Language Options:
    --en / --English    |    --zh / --Chinese
    --nl / --Dutch      |    --fr / --French
    --it / --Italian    |    --ja / --Japanese
    --ko / --Korean     |    --pt / --Portuguese
    --ru / --Russian    |    --es / --Spanish

Syntax Formats:
    --bc / --basecase       (BaseCase class inheritance)
    --pf / --pytest-fixture          (sb pytest fixture)
    --cf / --class-fixture   (class + sb pytest fixture)
    --cm / --context-manager        (SB context manager)
    --dc / --driver-context      (DriverContext manager)
    --dm / --driver-manager             (Driver manager)

Output:
    Creates a new SBase test file with boilerplate code.
    If the file already exists, an error is raised.
    By default, uses English with BaseCase inheritance,
    and creates a boilerplate with common SeleniumBase
    methods: "open", "type", "click", "assert_element",
    and "assert_text". If using the basic boilerplate
    option, only the "open" method is included. Only the
    BaseCase format supports Languages or Recorder Mode.
"""
import codecs
import colorama
import os
import sys


def invalid_run_command(msg=None):
    exp = "  ** mkfile **\n\n"
    exp += "  Usage:\n"
    exp += "           seleniumbase mkfile [FILE.py] [OPTIONS]\n"
    exp += "           OR     sbase mkfile [FILE.py] [OPTIONS]\n"
    exp += "  Example:\n"
    exp += "           sbase mkfile new_test.py\n"
    exp += "  Options:\n"
    exp += "           -b / --basic  (Basic boilerplate / single-line test)\n"
    exp += "           -r / --rec  (adds Pdb+ breakpoint for Recorder Mode)\n"
    exp += "           --url=URL  (makes the test start on a specific page)\n"
    exp += "  Language Options:\n"
    exp += "           --en / --English    |    --zh / --Chinese\n"
    exp += "           --nl / --Dutch      |    --fr / --French\n"
    exp += "           --it / --Italian    |    --ja / --Japanese\n"
    exp += "           --ko / --Korean     |    --pt / --Portuguese\n"
    exp += "           --ru / --Russian    |    --es / --Spanish\n"
    exp += "  Syntax Formats:\n"
    exp += "           --bc / --basecase       (BaseCase class inheritance)\n"
    exp += "           --pf / --pytest-fixture          (sb pytest fixture)\n"
    exp += "           --cf / --class-fixture   (class + sb pytest fixture)\n"
    exp += "           --cm / --context-manager        (SB context manager)\n"
    exp += "           --dc / --driver-context      (DriverContext manager)\n"
    exp += "           --dm / --driver-manager             (Driver manager)\n"
    exp += "  Output:\n"
    exp += "           Creates a new SBase test file with boilerplate code.\n"
    exp += "           If the file already exists, an error is raised.\n"
    exp += "           By default, uses English with BaseCase inheritance,\n"
    exp += "           and creates a boilerplate with common SeleniumBase\n"
    exp += '           methods: "open", "type", "click", "assert_element",\n'
    exp += '           and "assert_text". If using the basic boilerplate\n'
    exp += '           option, only the "open" method is included. Only the\n'
    exp += "           BaseCase format supports Languages or Recorder Mode.\n"
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
        if (
            "win32" in sys.platform
            and hasattr(colorama, "just_fix_windows_console")
        ):
            colorama.just_fix_windows_console()
        else:
            colorama.init(autoreset=True)
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
        cr = colorama.Style.RESET_ALL

    basic = False
    help_me = False
    recorder = False
    error_msg = None
    start_page = None
    invalid_cmd = None
    syntax = "BaseCase"
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
            elif option.startswith("--url=") and len(option) > 6:
                from seleniumbase.fixtures import page_utils
                start_page = option.split("--url=")[1]
                if not page_utils.is_valid_url(start_page):
                    if page_utils.is_valid_url("https://" + start_page):
                        start_page = "https://" + start_page
                    else:
                        raise Exception("Invalid URL: %s" % start_page)
                basic = True
            elif option == "-b" or option == "--basic":
                basic = True
            elif option == "-r" or option == "--rec":
                recorder = True
            elif option == "--record" or option == "--recorder":
                recorder = True
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
            elif option == "--bc" or option == "--basecase":
                syntax = "BaseCase"
            elif option == "--pf" or option == "--pytest-fixture":
                syntax = "PytestFixture"
            elif option == "--cf" or option == "--class-fixture":
                syntax = "ClassFixture"
            elif option == "--cm" or option == "--context-manager":
                syntax = "ContextManager"
            elif option == "--dc" or option == "--driver-context":
                syntax = "DriverContext"
            elif option == "--dm" or option == "--driver-manager":
                syntax = "DriverManager"
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

    dir_name = os.getcwd()
    file_path = "%s/%s" % (dir_name, file_name)

    body = "body"
    para1 = "html body > p"
    para2 = "p"
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
    if start_page:
        url = start_page
    elif basic:
        url = "about:blank"
    elif language not in ["English", "Dutch", "French", "Italian"]:
        url = "data:text/html,<meta charset='utf-8'><p>%s<br><input>" % hello
    else:
        url = "data:text/html,<p>%s<br><input>" % hello

    import_line = "from seleniumbase import BaseCase"
    main_line = "BaseCase.main(__name__, __file__)"
    parent_class = "BaseCase"
    if language != "English":
        from seleniumbase.translate.master_dict import MD_F

        import_line = MD_F.get_import_line(language)
        parent_class = MD_F.get_lang_parent_class(language)
    class_line = "class %s(%s):" % (class_name, parent_class)

    data = []
    data.append("%s" % import_line)
    if not recorder:
        data.append(main_line)
    data.append("")
    data.append("")
    data.append("%s" % class_line)
    data.append("    def test_base(self):")
    if not recorder:
        data.append('        self.open("%s")' % url)
    else:
        data.append("        if self.recorder_ext and not self.xvfb:")
        data.append("            import pdb; pdb.set_trace()")
    if not basic and not recorder:
        data.append(
            '        self.type("input", "%s")' "  # selector, text" % goodbye
        )
        data.append('        self.click("%s")  # selector' % para1)
        data.append('        self.assert_element("%s")  # selector' % body)
        data.append(
            '        self.assert_text("%s", "%s")'
            "  # text, selector" % (hello, para2)
        )
    data.append("")

    new_data = []
    if language == "English" and syntax == "BaseCase":
        new_data = data
    elif language == "English" and syntax == "PytestFixture":
        data = []
        data.append("def test_base(sb):")
        data.append('    sb.open("data:text/html,<p>Hello<br><input>")')
        if not basic:
            data.append('    sb.type("input", "Goodbye")  # selector, text')
            data.append('    sb.click("html body > p")  # selector')
            data.append('    sb.assert_element("body")  # selector')
            data.append('    sb.assert_text("Hello", "p")  # text, selector')
        data.append("")
        new_data = data
    elif language == "English" and syntax == "ClassFixture":
        data = []
        data.append("class %s:" % class_name)
        data.append("    def test_base(self, sb):")
        data.append('        sb.open("data:text/html,<p>Hello<br><input>")')
        if not basic:
            data.append(
                '        sb.type("input", "Goodbye")  # selector, text'
            )
            data.append('        sb.click("html body > p")  # selector')
            data.append('        sb.assert_element("body")  # selector')
            data.append(
                '        sb.assert_text("Hello", "p")  # text, selector'
            )
        data.append("")
        new_data = data
    elif language == "English" and syntax == "ContextManager":
        data = []
        data.append("from seleniumbase import SB")
        data.append("")
        data.append('with SB(browser="chrome") as sb:')
        data.append(
            '    sb.open("data:text/html,<div>Hello<br><input></div>")'
        )
        if not basic:
            data.append('    sb.type("input", "Goodbye")  # selector, text')
            data.append('    sb.click("html body > div")  # selector')
            data.append('    sb.assert_element("input")  # selector')
            data.append('    sb.assert_text("Hello", "div")  # text, selector')
            data.append('    sb.highlight("div")  # selector')
            data.append("    sb.sleep(0.5)  # seconds")
        data.append("")
        new_data = data
    elif language == "English" and syntax == "DriverContext":
        data = []
        data.append("from seleniumbase import DriverContext")
        data.append("")
        data.append('with DriverContext(browser="chrome") as driver:')
        data.append('    driver.get("data:text/html,<p>Hello<br><input>")')
        data.append("")
        new_data = data
    elif language == "English" and syntax == "DriverManager":
        data = []
        data.append("from seleniumbase import Driver")
        data.append("")
        data.append('driver = Driver(browser="chrome")')
        data.append("try:")
        data.append('    driver.get("data:text/html,<p>Hello<br><input>")')
        data.append("finally:")
        data.append("    driver.quit()")
        data.append("")
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
            if main_line in line:
                new_main = "%s.main(__name__, __file__)" % parent_class
                new_line = line.replace(main_line, new_main)
                found_swap = True
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
    if " " not in file_name:
        os.system("sbase print %s -n" % file_name)
    elif '"' not in file_name:
        os.system('sbase print "%s" -n' % file_name)
    else:
        os.system("sbase print '%s' -n" % file_name)
    success = (
        "\n" + c1 + '* Test file: "' + file_name + '" was created! *'
        "" + cr + "\n"
    )
    print(success)


if __name__ == "__main__":
    invalid_run_command()
