"""
Creates a new SeleniumBase chart presentation with boilerplate code.

Usage:
    seleniumbase mkchart [FILE.py] [LANG]
    or     sbase mkchart [FILE.py] [LANG]

Example:
    sbase mkchart new_chart.py --en

Language Options:
    --en / --English    |    --zh / --Chinese
    --nl / --Dutch      |    --fr / --French
    --it / --Italian    |    --ja / --Japanese
    --ko / --Korean     |    --pt / --Portuguese
    --ru / --Russian    |    --es / --Spanish

Output:
    Creates a new SeleniumBase chart presentation.
    If the file already exists, an error is raised.
    By default, the slides are written in English,
    and use a "sky" theme with "slide" transition.
    The chart can be used as a basic boilerplate.
"""
import codecs
import colorama
import os
import sys


def invalid_run_command(msg=None):
    exp = "  ** mkchart **\n\n"
    exp += "  Usage:\n"
    exp += "          seleniumbase mkchart [FILE.py] [LANG]\n"
    exp += "          OR     sbase mkchart [FILE.py] [LANG]\n"
    exp += "  Example:\n"
    exp += "          sbase mkchart new_chart.py --en\n"
    exp += "  Language Options:\n"
    exp += "          --en / --English    |    --zh / --Chinese\n"
    exp += "          --nl / --Dutch      |    --fr / --French\n"
    exp += "          --it / --Italian    |    --ja / --Japanese\n"
    exp += "          --ko / --Korean     |    --pt / --Portuguese\n"
    exp += "          --ru / --Russian    |    --es / --Spanish\n"
    exp += "  Output:\n"
    exp += "          Creates a new SeleniumBase chart presentation.\n"
    exp += "          If the file already exists, an error is raised.\n"
    exp += "          By default, the slides are written in English,\n"
    exp += '          and use a "sky" theme with "slide" transition.\n'
    exp += "          The chart can be used as a basic boilerplate.\n"
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

    dir_name = os.getcwd()
    file_path = "%s/%s" % (dir_name, file_name)
    html_name = file_name.replace(".py", ".html")
    class_name = "MyTestClass"
    item = "Item"
    select_option = "Select option"
    chart_options = '"pie", "bar", "column", "line", "area"'

    if language == "Chinese":
        class_name = "我的测试类"
        item = "目的"
        select_option = "选择选项"
        chart_options = '"饼图", "条形图", "柱形图", "折线图", "面积图"'
    elif language == "Dutch":
        class_name = "MijnTestklasse"
        item = "Voorwerp"
        select_option = "Optie selecteren"
        chart_options = '"cirkel", "staaf", "kolom", "lijn", "vlak"'
    elif language == "French":
        class_name = "MaClasseDeTest"
        item = "Objet"
        select_option = "Sélectionner option"
        chart_options = '"secteurs" "barres" "colonnes" "linéaire" "aires"'
    elif language == "Italian":
        class_name = "MiaClasseDiTest"
        item = "Oggetto"
        select_option = "Selezionare opzione"
        chart_options = '"torta", "barre", "colonne", "linee", "area"'
    elif language == "Japanese":
        class_name = "私のテストクラス"
        item = "物体"
        select_option = "でオプションを選択"
        chart_options = '"円", "棒", "縦棒", "折れ線", "面"'
    elif language == "Korean":
        class_name = "테스트_클래스"
        item = "물체"
        select_option = "옵션 선택"
        chart_options = '"원형", "막대", "열", "선", "영역"'
    elif language == "Portuguese":
        class_name = "MinhaClasseDeTeste"
        item = "Objeto"
        select_option = "Selecionar opção"
        chart_options = '"pizza", "barras", "colunas", "linhas", "área"'
    elif language == "Russian":
        class_name = "МойТестовыйКласс"
        item = "Вещь"
        select_option = "Выбрать опцию"
        chart_options = '"круговую" "бар" "столбчатую" "линейную" "области"'
    elif language == "Spanish":
        class_name = "MiClaseDePrueba"
        item = "Objeto"
        select_option = "Seleccionar opción"
        chart_options = '"circular", "barras", "columnas", "líneas", "área"'

    import_line = "from seleniumbase import BaseCase"
    parent_class = "BaseCase"
    class_line = "class MyTestClass(BaseCase):"
    if language != "English":
        from seleniumbase.translate.master_dict import MD_F

        import_line = MD_F.get_import_line(language)
        parent_class = MD_F.get_lang_parent_class(language)
    class_line = "class %s(%s):" % (class_name, parent_class)
    settings = 'theme="sky", transition="slide"'
    chart_settings = 'title="Chart 1"'
    add_slide = '"<p>Chart Demo</p>" + self.extract_chart()'
    data = []
    data.append("%s" % import_line)
    data.append("")
    data.append("")
    data.append("%s" % class_line)
    data.append("    def test_chart_presentation(self):")
    data.append("        self.create_presentation(%s)" % settings)
    data.append("")
    data.append("        # %s => %s" % (select_option, chart_options))
    data.append("        self.create_pie_chart(%s)" % chart_settings)
    data.append('        self.add_data_point("%s A", 50)' % item)
    data.append('        self.add_data_point("%s B", 40)' % item)
    data.append('        self.add_data_point("%s C", 35)' % item)
    data.append('        self.add_data_point("%s D", 30)' % item)
    data.append('        self.add_data_point("%s E", 25)' % item)
    data.append('        self.add_data_point("%s F", 20)' % item)
    data.append("        self.add_slide(%s)" % add_slide)
    data.append("")
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
        "\n" + c1 + '* Chart Presentation: "' + file_name + '" was created! *'
        "" + cr + "\n"
    )
    print(success)


if __name__ == "__main__":
    invalid_run_command()
