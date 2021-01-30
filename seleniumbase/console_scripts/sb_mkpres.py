# -*- coding: utf-8 -*-
"""
Creates a new SeleniumBase presentation with boilerplate code.

Usage:
    seleniumbase mkpres [FILE.py] [LANG]
    or     sbase mkpres [FILE.py] [LANG]

Example:
    sbase mkpres new_presentation.py --en

Language Options:
    --en / --English    |    --zh / --Chinese
    --nl / --Dutch      |    --fr / --French
    --it / --Italian    |    --ja / --Japanese
    --ko / --Korean     |    --pt / --Portuguese
    --ru / --Russian    |    --es / --Spanish

Output:
    Creates a new presentation with 3 example slides.
    If the file already exists, an error is raised.
    By default, the slides are written in English.
    Slides use "serif" theme & "fade" transition.
    This code can be used as a base boilerplate.
"""

import codecs
import colorama
import os
import sys


def invalid_run_command(msg=None):
    exp = ("  ** mkpres **\n\n")
    exp += "  Usage:\n"
    exp += "          seleniumbase mkpres [FILE.py] [LANG]\n"
    exp += "          OR     sbase mkpres [FILE.py] [LANG]\n"
    exp += "  Example:\n"
    exp += "          sbase mkpres new_presentation.py --en\n"
    exp += "  Language Options:\n"
    exp += "          --en / --English    |    --zh / --Chinese\n"
    exp += "          --nl / --Dutch      |    --fr / --French\n"
    exp += "          --it / --Italian    |    --ja / --Japanese\n"
    exp += "          --ko / --Korean     |    --pt / --Portuguese\n"
    exp += "          --ru / --Russian    |    --es / --Spanish\n"
    exp += "  Output:\n"
    exp += '          Creates a new presentation with 3 example slides.\n'
    exp += '          If the file already exists, an error is raised.\n'
    exp += '          By default, the slides are written in English.\n'
    exp += '          Slides use "serif" theme & "fade" transition.\n'
    exp += '          This code can be used as a base boilerplate.\n'
    if not msg:
        raise Exception('INVALID RUN COMMAND!\n\n%s' % exp)
    elif msg == "help":
        print("\n%s" % exp)
        sys.exit()
    else:
        raise Exception('INVALID RUN COMMAND!\n\n%s\n%s\n' % (exp, msg))


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
        error_msg = 'Invalid file name!'
    elif file_name.startswith("-"):
        error_msg = 'File name cannot start with "-"!'
    elif "/" in str(file_name) or "\\" in str(file_name):
        error_msg = 'File must be created in the current directory!'
    elif os.path.exists(os.getcwd() + '/' + file_name):
        error_msg = (
            'File "%s" already exists in this directory!' % file_name)
    if error_msg:
        error_msg = c5 + "ERROR: " + error_msg + cr
        invalid_run_command(error_msg)

    if len(command_args) >= 2:
        options = command_args[1:]
        for option in options:
            option = option.lower()
            if option == "-h" or option == "--help":
                help_me = True
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
                invalid_cmd = invalid_cmd.replace('>> ', ">>" + c5 + " ")
                invalid_cmd = invalid_cmd.replace(' <<', " " + cr + "<<")
                invalid_cmd = invalid_cmd.replace('>>', c7 + ">>" + cr)
                invalid_cmd = invalid_cmd.replace('<<', c7 + "<<" + cr)
                help_me = True
                break
    if help_me:
        invalid_run_command(invalid_cmd)

    if language != "English" and sys.version_info[0] == 2:
        print("")
        msg = 'Multi-language support for "sbase mkpres" '
        msg += 'is not available on Python 2!'
        msg = "\n" + c5 + msg + cr
        msg += '\nPlease run in "English" mode or upgrade to Python 3!\n'
        raise Exception(msg)

    dir_name = os.getcwd()
    file_path = "%s/%s" % (dir_name, file_name)
    html_name = file_name.replace(".py", ".html")

    hello = "Hello"
    update_text = "Update Text"
    goodbye = "Goodbye"
    class_name = "MyTestClass"

    if language == "Chinese":
        hello = "你好"
        update_text = "更新文本"
        goodbye = "再见"
        class_name = "我的测试类"
    elif language == "Dutch":
        hello = "Hallo"
        update_text = "Tekst Bijwerken"
        goodbye = "Dag"
        class_name = "MijnTestklasse"
    elif language == "French":
        hello = "Bonjour"
        update_text = "Modifier Texte"
        goodbye = "Au revoir"
        class_name = "MaClasseDeTest"
    elif language == "Italian":
        hello = "Ciao"
        update_text = "Aggiornare Testo"
        goodbye = "Addio"
        class_name = "MiaClasseDiTest"
    elif language == "Japanese":
        hello = "こんにちは"
        update_text = "テキストを更新"
        goodbye = "さようなら"
        class_name = "私のテストクラス"
    elif language == "Korean":
        hello = "여보세요"
        update_text = "텍스트를 업데이트"
        goodbye = "안녕"
        class_name = "테스트_클래스"
    elif language == "Portuguese":
        hello = "Olá"
        update_text = "Atualizar Texto"
        goodbye = "Tchau"
        class_name = "MinhaClasseDeTeste"
    elif language == "Russian":
        hello = "Привет"
        update_text = "обновить текст"
        goodbye = "До свидания"
        class_name = "МойТестовыйКласс"
    elif language == "Spanish":
        hello = "Hola"
        update_text = "Actualizar Texto"
        goodbye = "Adiós"
        class_name = "MiClaseDePrueba"

    import_line = "from seleniumbase import BaseCase"
    parent_class = "BaseCase"
    class_line = "class MyTestClass(BaseCase):"
    if language != "English":
        from seleniumbase.translate.master_dict import MD_F
        import_line = MD_F.get_import_line(language)
        parent_class = MD_F.get_lang_parent_class(language)
    class_line = "class %s(%s):" % (class_name, parent_class)
    settings = 'theme="serif", transition="fade"'
    img_src = 'src="https://seleniumbase.io/cdn/img/sb6.png"'
    hello_page = (
        "\n            '<h1>%s</h1><br />'"
        "\n            '<img %s>'"
        '' % (hello, img_src))
    update_text_page = "<h2><b>*</b>  %s  <b>*</b></h2>" % update_text
    goodbye_page = "<h2>%s</h2><p>Use SeleniumBase!</p>" % goodbye

    data = []
    data.append("%s" % import_line)
    data.append("")
    data.append("")
    data.append("%s" % class_line)
    data.append("")
    data.append("    def test_presentation(self):")
    data.append('        self.create_presentation(%s)' % settings)
    data.append('        self.add_slide(%s)' % hello_page)
    data.append('        self.add_slide("%s")' % update_text_page)
    data.append('        self.add_slide("%s")' % goodbye_page)
    data.append('        self.begin_presentation(filename="%s")' % html_name)
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
                    new_line = new_line[0:-len("  # noqa")]
                new_data.append(new_line)
                continue
            new_data.append(line)
    data = new_data
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()
    success = (
        '\n' + c1 + '* Presentation: "' + file_name + '" was created! *'
        '' + cr + '\n')
    print(success)


if __name__ == "__main__":
    invalid_run_command()
