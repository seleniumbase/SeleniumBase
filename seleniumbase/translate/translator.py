"""
Translates a SeleniumBase Python file into a different language

Usage:
        seleniumbase translate [SB_FILE.py] [LANGUAGE] [ACTION]
        OR:    sbase translate [SB_FILE.py] [LANGUAGE] [ACTION]
Languages:
        --en / --English    |    --zh / --Chinese
        --nl / --Dutch      |    --fr / --French
        --it / --Italian    |    --ja / --Japanese
        --ko / --Korean     |    --pt / --Portuguese
        --ru / --Russian    |    --es / --Spanish
Actions:
        -p / --print  (Print translation output to the screen)
        -o / --overwrite  (Overwrite the file being translated)
        -c / --copy  (Copy the translation to a new .py file)
Options:
        -n  (include line Numbers when using the Print action)
Output:
        Translates a SeleniumBase Python file into the language
        specified. Method calls and "import" lines get swapped.
        Both a language and an action must be specified.
        The "-p" action can be paired with one other action.
        When running with "-c" (or "--copy"), the new file name
        will be the original name appended with an underscore
        plus the 2-letter language code of the new language.
        (Example: Translating "test_1.py" into Japanese with
        "-c" will create a new file called "test_1_ja.py".)
"""

import codecs
import colorama
import os
import re
import sys
from seleniumbase.translate import master_dict

MD_F = master_dict.MD_F
MD_L_Codes = master_dict.MD_L_Codes
MD = master_dict.MD


def invalid_run_command(msg=None):
    exp = "  ** translate **\n\n"
    exp += "  Usage:\n"
    exp += "         seleniumbase translate [SB_FILE.py] [LANGUAGE] [ACTION]\n"
    exp += "         OR:    sbase translate [SB_FILE.py] [LANGUAGE] [ACTION]\n"
    exp += "  Languages:\n"
    exp += "         --en / --English    |    --zh / --Chinese\n"
    exp += "         --nl / --Dutch      |    --fr / --French\n"
    exp += "         --it / --Italian    |    --ja / --Japanese\n"
    exp += "         --ko / --Korean     |    --pt / --Portuguese\n"
    exp += "         --ru / --Russian    |    --es / --Spanish\n"
    exp += "  Actions:\n"
    exp += "         -p / --print  (Print translation output to the screen)\n"
    exp += "         -o / --overwrite  (Overwrite the file being translated)\n"
    exp += "         -c / --copy  (Copy the translation to a new .py file)\n"
    exp += "  Options:\n"
    exp += "         -n  (include line Numbers when using the Print action)\n"
    exp += "  Output:\n"
    exp += "         Translates a SeleniumBase Python file into the language\n"
    exp += '         specified. Method calls and "import" lines get swapped.\n'
    exp += "         Both a language and an action must be specified.\n"
    exp += '         The "-p" action can be paired with one other action.\n'
    exp += '         When running with "-c" (or "--copy"), the new file name\n'
    exp += "         will be the original name appended with an underscore\n"
    exp += "         plus the 2-letter language code of the new language.\n"
    exp += '         (Example: Translating "test_1.py" into Japanese with\n'
    exp += '          "-c" will create a new file called "test_1_ja.py".)\n'
    if not msg:
        raise Exception("INVALID RUN COMMAND!\n\n%s" % exp)
    else:
        raise Exception("INVALID RUN COMMAND!\n%s\n\n%s" % (msg, exp))


def sc_ranges():
    # Get the ranges of special double-width characters.
    special_char_ranges = [
        {"from": ord("\u4e00"), "to": ord("\u9FFF")},
        {"from": ord("\u3040"), "to": ord("\u30ff")},
        {"from": ord("\uac00"), "to": ord("\ud7a3")},
        {"from": ord("\uff01"), "to": ord("\uff60")},
    ]
    return special_char_ranges


def is_cjk(char):
    # Returns True if the special character is Chinese, Japanese, or Korean.
    sc = any(
        [range["from"] <= ord(char) <= range["to"] for range in sc_ranges()]
    )
    return sc


def get_width(line):
    # Return the true width of the line. Not the same as line length.
    # Chinese/Japanese/Korean characters take up double width visually.
    line_length = len(line)
    for char in line:
        if is_cjk(char):
            line_length += 1
    return line_length


def process_test_file(code_lines, new_lang):
    detected_lang = None
    changed = False
    found_bc = False  # Found BaseCase or a translation
    seleniumbase_lines = []
    lang_codes = MD_L_Codes.lang
    nl_code = lang_codes[new_lang]  # new_lang language code
    dl_code = None  # detected_lang language code
    md = MD.md  # Master Dictionary

    for line in code_lines:
        line = line.rstrip()

        # Find imports that determine the language
        if line.lstrip().startswith("from seleniumbase") and "import" in line:
            added_line = False
            for lang in MD_F.get_languages_list():
                data = re.match(
                    r"^\s*" + MD_F.get_import_line(lang) + r"([\S\s]*)$", line
                )
                if data:
                    comments = "%s" % data.group(1)
                    new_line = None
                    detected_lang = lang
                    dl_code = lang_codes[detected_lang]
                    if detected_lang != new_lang:
                        changed = True
                        new_line = MD_F.get_import_line(new_lang) + comments
                    else:
                        found_bc = True
                        new_line = line
                    if new_line.endswith("  # noqa"):  # Remove flake8 skip
                        new_line = new_line[0 : -len("  # noqa")]
                    seleniumbase_lines.append(new_line)
                    added_line = True
                    break
                data = re.match(
                    r"^\s*" + MD_F.get_mqa_im_line(lang) + r"([\S\s]*)$", line
                )
                if data:
                    comments = "%s" % data.group(1)
                    new_line = None
                    detected_lang = lang
                    dl_code = lang_codes[detected_lang]
                    if detected_lang != new_lang:
                        changed = True
                        new_line = MD_F.get_mqa_im_line(new_lang) + comments
                    else:
                        found_bc = True
                        new_line = line
                    if new_line.endswith("  # noqa"):  # Remove flake8 skip
                        new_line = new_line[0 : -len("  # noqa")]
                    seleniumbase_lines.append(new_line)
                    added_line = True
                    break
            if not added_line:
                # Probably a language missing from the translator.
                # Add the import line as it is and move on.
                seleniumbase_lines.append(line)
            continue

        # Find class definitions that determine the language
        if line.lstrip().startswith("class ") and ":" in line:
            added_line = False
            data = re.match(
                r"""^(\s*)class\s+([\S]+)\(([\S]+)\):([\S\s]*)$""", line
            )
            if data:
                whitespace = data.group(1)
                name = "%s" % data.group(2)
                parent_class = "%s" % data.group(3)
                comments = "%s" % data.group(4)
                if parent_class in MD_F.get_parent_classes_list():
                    detected_lang = MD_F.get_parent_class_lang(parent_class)
                    dl_code = lang_codes[detected_lang]
                    if detected_lang != new_lang:
                        changed = True
                        new_parent = MD_F.get_lang_parent_class(new_lang)
                        new_line = "%sclass %s(%s):%s" "" % (
                            whitespace,
                            name,
                            new_parent,
                            comments,
                        )
                    else:
                        found_bc = True
                        new_line = line
                    if new_line.endswith("  # noqa"):  # Remove flake8 skip
                        new_line = new_line[0 : -len("  # noqa")]
                    seleniumbase_lines.append(new_line)
                    added_line = True
                    continue
                elif parent_class in MD_F.get_masterqa_parent_classes_list():
                    detected_lang = MD_F.get_mqa_par_class_lang(parent_class)
                    dl_code = lang_codes[detected_lang]
                    if detected_lang != new_lang:
                        changed = True
                        new_parent = MD_F.get_mqa_lang_par_class(new_lang)
                        new_line = "%sclass %s(%s):%s" "" % (
                            whitespace,
                            name,
                            new_parent,
                            comments,
                        )
                    else:
                        found_bc = True
                        new_line = line
                    if new_line.endswith("  # noqa"):  # Remove flake8 skip
                        new_line = new_line[0 : -len("  # noqa")]
                    seleniumbase_lines.append(new_line)
                    added_line = True
                    continue
            if not added_line:
                # Probably a language missing from the translator.
                # Add the class definition line as it is and move on.
                seleniumbase_lines.append(line)
            continue

        if (
            ".main(__name__, __file__)" in line
            and detected_lang
            and new_lang
            and (detected_lang != new_lang)
        ):
            old_basecase = MD_F.get_lang_parent_class(detected_lang)
            new_basecase = MD_F.get_lang_parent_class(new_lang)
            if old_basecase in line:
                new_line = line.replace(old_basecase, new_basecase)
                seleniumbase_lines.append(new_line)
                continue

        if (
            "self." in line
            and "(" in line
            and detected_lang
            and (detected_lang != new_lang)
        ):
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
                seleniumbase_lines.append(new_line)
                continue

        seleniumbase_lines.append(line)

    return seleniumbase_lines, changed, detected_lang, found_bc


def main():
    colorama.init(autoreset=True)
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c3 = colorama.Fore.RED + colorama.Back.LIGHTGREEN_EX
    c4 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
    c6 = colorama.Fore.RED + colorama.Back.LIGHTCYAN_EX
    c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
    cr = colorama.Style.RESET_ALL
    new_lang = None
    overwrite = False
    copy = False
    print_only = False
    help_me = False
    invalid_cmd = None
    line_numbers = False
    word_wrap = True  # Always use word wrap now

    expected_arg = "A SeleniumBase Python file"
    command_args = sys.argv[2:]
    seleniumbase_file = command_args[0]
    if not seleniumbase_file.endswith(".py"):
        seleniumbase_file = (
            c7 + ">>" + c5 + " " + seleniumbase_file + " " + c7 + "<<" + cr
        )
        bad_file_error = (
            "\n`%s` is not a Python file!\n\n"
            "Expecting: [%s]" % (seleniumbase_file, expected_arg)
        )
        bad_file_error = bad_file_error.replace(
            "is not a Python file!", c3 + "is not a Python file!" + cr
        )
        bad_file_error = bad_file_error.replace(
            expected_arg, c4 + expected_arg + cr
        )
        bad_file_error = bad_file_error.replace(
            "Expecting:", c3 + "Expecting:" + cr
        )
        print(bad_file_error)
        help_me = True

    if len(command_args) >= 2 and not help_me:
        options = command_args[1:]
        for option in options:
            option = option.lower()
            if option == "help" or option == "--help":
                help_me = True
            elif option == "-o" or option == "--overwrite":
                overwrite = True
            elif option == "-c" or option == "--copy":
                copy = True
            elif option == "-p" or option == "--print":
                print_only = True
            elif option == "-n":
                line_numbers = True
            elif option == "--en" or option == "--english":
                new_lang = "English"
            elif option == "--zh" or option == "--chinese":
                new_lang = "Chinese"
            elif option == "--nl" or option == "--dutch":
                new_lang = "Dutch"
            elif option == "--fr" or option == "--french":
                new_lang = "French"
            elif option == "--it" or option == "--italian":
                new_lang = "Italian"
            elif option == "--ja" or option == "--japanese":
                new_lang = "Japanese"
            elif option == "--ko" or option == "--korean":
                new_lang = "Korean"
            elif option == "--pt" or option == "--portuguese":
                new_lang = "Portuguese"
            elif option == "--ru" or option == "--russian":
                new_lang = "Russian"
            elif option == "--es" or option == "--spanish":
                new_lang = "Spanish"
            else:
                invalid_cmd = "\n===> INVALID OPTION: >> %s <<\n" % option
                invalid_cmd = invalid_cmd.replace(">> ", ">>" + c5 + " ")
                invalid_cmd = invalid_cmd.replace(" <<", " " + cr + "<<")
                invalid_cmd = invalid_cmd.replace(">>", c7 + ">>" + cr)
                invalid_cmd = invalid_cmd.replace("<<", c7 + "<<" + cr)
                help_me = True
                break
    else:
        help_me = True

    specify_lang = (
        "\n>* You must specify a language to translate to! *<\n"
        "\n"
        ">    ********  Language Options:  ********    <\n"
        "   --en / --English    |    --zh / --Chinese\n"
        "   --nl / --Dutch      |    --fr / --French\n"
        "   --it / --Italian    |    --ja / --Japanese\n"
        "   --ko / --Korean     |    --pt / --Portuguese\n"
        "   --ru / --Russian    |    --es / --Spanish\n"
    )
    specify_action = (
        "\n>* You must specify an action type! *<\n"
        "\n"
        "> *** Action Options: *** <\n"
        "      -p / --print\n"
        "      -o / --overwrite\n"
        "      -c / --copy\n"
    )
    example_run = (
        "\n> *** Examples: *** <\n"
        "Translate test_1.py into Chinese and only print the output:\n"
        " >$ sbase translate test_1.py --zh -p\n"
        "Translate test_2.py into Portuguese and overwrite the file:\n"
        " >$ sbase translate test_2.py --pt -o\n"
        "Translate test_3.py into Dutch and make a copy of the file:\n"
        " >$ sbase translate test_3.py --nl -c\n"
    )
    usage = (
        "\n> *** Usage: *** <\n"
        " >$ sbase translate [SB_FILE.py] [LANGUAGE] [ACTION]\n"
    )
    specify_lang = specify_lang.replace(">*", c5 + ">*")
    specify_lang = specify_lang.replace("*<", "*<" + cr)
    specify_lang = specify_lang.replace(
        "Language Options:", c4 + "Language Options:" + cr
    )
    specify_lang = specify_lang.replace(
        ">    ********  ", c3 + ">    ********  " + cr
    )
    specify_lang = specify_lang.replace(
        "  ********    <", c3 + "  ********    <" + cr
    )
    specify_lang = specify_lang.replace("--en", c2 + "--en" + cr)
    specify_lang = specify_lang.replace("--zh", c2 + "--zh" + cr)
    specify_lang = specify_lang.replace("--nl", c2 + "--nl" + cr)
    specify_lang = specify_lang.replace("--fr", c2 + "--fr" + cr)
    specify_lang = specify_lang.replace("--it", c2 + "--it" + cr)
    specify_lang = specify_lang.replace("--ja", c2 + "--ja" + cr)
    specify_lang = specify_lang.replace("--ko", c2 + "--ko" + cr)
    specify_lang = specify_lang.replace("--pt", c2 + "--pt" + cr)
    specify_lang = specify_lang.replace("--ru", c2 + "--ru" + cr)
    specify_lang = specify_lang.replace("--es", c2 + "--es" + cr)
    specify_lang = specify_lang.replace("--English", c2 + "--English" + cr)
    specify_lang = specify_lang.replace("--Chinese", c2 + "--Chinese" + cr)
    specify_lang = specify_lang.replace("--Dutch", c2 + "--Dutch" + cr)
    specify_lang = specify_lang.replace("--French", c2 + "--French" + cr)
    specify_lang = specify_lang.replace("--Italian", c2 + "--Italian" + cr)
    specify_lang = specify_lang.replace("--Japanese", c2 + "--Japanese" + cr)
    specify_lang = specify_lang.replace("--Korean", c2 + "--Korean" + cr)
    specify_lang = specify_lang.replace(
        "--Portuguese", c2 + "--Portuguese" + cr
    )
    specify_lang = specify_lang.replace("--Russian", c2 + "--Russian" + cr)
    specify_lang = specify_lang.replace("--Spanish", c2 + "--Spanish" + cr)
    specify_action = specify_action.replace(">*", c6 + ">*")
    specify_action = specify_action.replace("*<", "*<" + cr)
    specify_action = specify_action.replace(
        "Action Options:", c4 + "Action Options:" + cr
    )
    specify_action = specify_action.replace("> *** ", c3 + "> *** " + cr)
    specify_action = specify_action.replace(" *** <", c3 + " *** <" + cr)
    specify_action = specify_action.replace(" -p", " " + c1 + "-p" + cr)
    specify_action = specify_action.replace(" -o", " " + c1 + "-o" + cr)
    specify_action = specify_action.replace(" -c", " " + c1 + "-c" + cr)
    specify_action = specify_action.replace(
        " --print", " " + c1 + "--print" + cr
    )
    specify_action = specify_action.replace(
        " --overwrite", " " + c1 + "--overwrite" + cr
    )
    specify_action = specify_action.replace(
        " --copy", " " + c1 + "--copy" + cr
    )
    example_run = example_run.replace("Examples:", c4 + "Examples:" + cr)
    example_run = example_run.replace("> *** ", c3 + "> *** " + cr)
    example_run = example_run.replace(" *** <", c3 + " *** <" + cr)
    example_run = example_run.replace(" -p", " " + c1 + "-p" + cr)
    example_run = example_run.replace(" -o", " " + c1 + "-o" + cr)
    example_run = example_run.replace(" -c", " " + c1 + "-c" + cr)
    example_run = example_run.replace("Chinese", c2 + "Chinese" + cr)
    example_run = example_run.replace("Portuguese", c2 + "Portuguese" + cr)
    example_run = example_run.replace("Dutch", c2 + "Dutch" + cr)
    example_run = example_run.replace(" --zh", " " + c2 + "--zh" + cr)
    example_run = example_run.replace(" --pt", " " + c2 + "--pt" + cr)
    example_run = example_run.replace(" --nl", " " + c2 + "--nl" + cr)
    example_run = example_run.replace("sbase", c4 + "sbase" + cr)
    usage = usage.replace("Usage:", c4 + "Usage:" + cr)
    usage = usage.replace("> *** ", c3 + "> *** " + cr)
    usage = usage.replace(" *** <", c3 + " *** <" + cr)
    usage = usage.replace("SB_FILE.py", c4 + "SB_FILE.py" + cr)
    usage = usage.replace("LANGUAGE", c2 + "LANGUAGE" + cr)
    usage = usage.replace("ACTION", c1 + "ACTION" + cr)

    if help_me:
        message = ""
        if invalid_cmd:
            message += invalid_cmd
        message += specify_lang + specify_action + example_run + usage
        print("")
        raise Exception(message)
    if not overwrite and not copy and not print_only:
        message = specify_action + example_run + usage
        if not new_lang:
            message = specify_lang + specify_action + example_run + usage
        print("")
        raise Exception(message)
    if not new_lang:
        print("")
        raise Exception(specify_lang + example_run + usage)
    if overwrite and copy:
        part_1 = (
            "\n* You can choose either {-o / --overwrite} "
            "OR {-c / --copy}, BUT * NOT BOTH *!\n"
        )
        part_1 = part_1.replace("-o ", c1 + "-o" + cr + " ")
        part_1 = part_1.replace("--overwrite", c1 + "--overwrite" + cr)
        part_1 = part_1.replace("-c ", c1 + "-c" + cr + " ")
        part_1 = part_1.replace("--copy", c1 + "--copy" + cr)
        part_1 = part_1.replace("* NOT BOTH *", c6 + "* NOT BOTH *" + cr)
        message = part_1 + example_run + usage
        print("")
        raise Exception(message)

    with open(seleniumbase_file, "r", encoding="utf-8") as f:
        all_code = f.read()
    if "def test_" not in all_code and "from seleniumbase" not in all_code:
        print("")
        raise Exception(
            "\n\n`%s` is not a valid SeleniumBase test file!\n"
            "\nExpecting: [%s]\n" % (seleniumbase_file, expected_arg)
        )
    all_code = all_code.replace("\t", "    ")
    code_lines = all_code.split("\n")

    sb_lines, changed, d_l, found_bc = process_test_file(code_lines, new_lang)
    seleniumbase_lines = sb_lines
    detected_lang = d_l
    found_basecase = found_bc

    if not changed and found_basecase:
        print("")
        msg1 = " [[[[%s]]]] was already in [[[%s]]]!\n\n" "" % (
            seleniumbase_file,
            new_lang,
        )
        msg1 = msg1.replace("[[[[", "" + c3).replace("]]]]", cr + "")
        msg1 = msg1.replace("[[[", "" + c5).replace("]]]", cr + "")
        msg2 = None
        if print_only:
            msg2 = "*> ***  No changes to display!  *** <*"
        elif overwrite:
            msg2 = "*> ***  No changes were made!  *** <*"
        else:  # "copy" action
            msg2 = "*> ***  No action was taken!  *** <*"
        msg2 = msg2.replace("*>", " " + c6).replace("<*", cr + "\n")
        print(msg1 + msg2)
        return

    if not changed and not found_basecase:
        print("")
        filename = c3 + seleniumbase_file + cr
        from_sb = c5 + "from seleniumbase" + cr
        msg0 = " * In order to translate the script,\n"
        msg1 = ' %s requires "%s..."\n' % (filename, from_sb)
        msg2 = " and a BaseCase import in a supported language!\n\n"
        msg3 = None
        if print_only:
            msg3 = "*> ***  No changes to display!  *** <*"
        elif overwrite:
            msg3 = "*> ***  No changes were made!  *** <*"
        else:  # "copy" action
            msg3 = "*> ***  No action was taken!  *** <*"
        msg3 = msg3.replace("*>", " " + c6).replace("<*", cr + "\n")
        print(msg0 + msg1 + msg2 + msg3)
        return

    save_line = (
        " [[[[%s]]]] was translated to [[[%s]]]! "
        "(Previous: %s)\n"
        "" % (seleniumbase_file, new_lang, detected_lang)
    )
    save_line = save_line.replace("[[[[", "" + c4)
    save_line = save_line.replace("]]]]", cr + "")
    save_line = save_line.replace("[[[", "" + c2)
    save_line = save_line.replace("]]]", cr + "")

    if print_only:
        console_width = None  # width of console output when running script
        used_width = None  # code_width and few spaces on right for padding
        magic_console = None
        magic_syntax = None
        try:
            console_width = os.popen("stty size", "r").read().split()[1]
            if console_width:
                console_width = int(console_width)
        except Exception:
            console_width = None

        if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
            from rich.console import Console
            from rich.syntax import Syntax

            python_code = "\n".join(seleniumbase_lines)
            code_width = 1

            w = 0  # line number whitespace
            if line_numbers:
                w = 4
                num_lines = len(code_lines)
                if num_lines >= 10:
                    w = 5
                if num_lines >= 100:
                    w = 6
                if num_lines >= 1000:
                    w = 7

            new_sb_lines = []
            for line in seleniumbase_lines:
                if line.endswith("  # noqa") and line.count("  # noqa") == 1:
                    line = line.replace("  # noqa", "")
                line_length2 = len(line)  # Normal Python string length used
                line_length = get_width(line)  # Special characters count 2X
                if line_length > code_width:
                    code_width = line_length

                if console_width:
                    # If line is larger than console_width, try to optimize it.
                    # Smart Python word wrap to be used with valid indentation.
                    if line_length + w > console_width:  # 5 is line number ws
                        if line.strip().startswith("#"):
                            new_sb_lines.append(line)
                            continue
                        elif (
                            line.count("  # ") == 1
                            and get_width(line.split("  # ")[0]) + w
                            <= console_width
                        ):
                            # Line is short enough once comment is removed
                            line = line.split("  # ")[0]
                            new_sb_lines.append(line)
                            continue
                        elif (
                            line.count(" # ") == 1
                            and get_width(line.split(" # ")[0]) + w
                            <= console_width
                        ):
                            # L-Length good if removing bad flake8 comment
                            line = line.split("  # ")[0]
                            new_sb_lines.append(line)
                            continue
                        if line.startswith("from") and " import " in line:
                            line1 = line.split(" import ")[0] + " \\"
                            line2 = "    import " + line.split(" import ")[1]
                            new_sb_lines.append(line1)
                            new_sb_lines.append(line2)
                            continue
                        if line.count("(") == 1 and line.count(")") == 1:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split("(")[0] + "("
                            line2 = new_ws + line.split("(")[1]
                            if not ("):") in line2:
                                new_sb_lines.append(line1)
                                if get_width(line2) + w > console_width:
                                    if line2.count('", "') == 1:
                                        line2a = line2.split('", "')[0] + '",'
                                        line2b = (
                                            new_ws
                                            + '"'
                                            + (line2.split('", "')[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        new_sb_lines.append(line2b)
                                        continue
                                    elif line2.count("', '") == 1:
                                        line2a = line2.split("', '")[0] + "',"
                                        line2b = (
                                            new_ws
                                            + "'"
                                            + (line2.split("', '")[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        new_sb_lines.append(line2b)
                                        continue
                                    elif line2.count("://") == 1 and (
                                        line2.count('")') == 1
                                    ):
                                        line2a = line2.split("://")[0] + '://"'
                                        line2b = (
                                            new_ws
                                            + '"'
                                            + (line2.split("://")[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        if get_width(line2b) + w > (
                                            console_width
                                        ):
                                            if line2b.count("/") > 0:
                                                slash_one = line2b.find("/")
                                                slash_one_p1 = slash_one + 1
                                                line2b1 = (
                                                    line2b[:slash_one_p1] + '"'
                                                )
                                                line2b2 = (
                                                    new_ws
                                                    + '"'
                                                    + (line2b[slash_one_p1:])
                                                )
                                                new_sb_lines.append(line2b1)
                                                if line2b2.count(")  # ") == 1:
                                                    line2b2 = (
                                                        line2b2.split(")  # ")[
                                                            0
                                                        ]
                                                        + ")"
                                                    )
                                                new_sb_lines.append(line2b2)
                                                continue
                                        new_sb_lines.append(line2b)
                                        continue
                                    elif line2.count("://") == 1 and (
                                        line2.count("')") == 1
                                    ):
                                        line2a = line2.split("://")[0] + "://'"
                                        line2b = (
                                            new_ws
                                            + "'"
                                            + (line2.split("://")[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        if get_width(line2b) + w > (
                                            console_width
                                        ):
                                            if line2b.count("/") > 0:
                                                slash_one = line2b.find("/")
                                                slash_one_p1 = slash_one + 1
                                                line2b1 = (
                                                    line2b[:slash_one_p1] + "'"
                                                )
                                                line2b2 = (
                                                    new_ws
                                                    + "'"
                                                    + (line2b[slash_one_p1:])
                                                )
                                                new_sb_lines.append(line2b1)
                                                if line2b2.count(")  # ") == 1:
                                                    line2b2 = (
                                                        line2b2.split(")  # ")[
                                                            0
                                                        ]
                                                        + ")"
                                                    )
                                                new_sb_lines.append(line2b2)
                                                continue
                                        new_sb_lines.append(line2b)
                                        continue
                                    elif line2.count(", ") == 1:
                                        line2a = line2.split(", ")[0] + ","
                                        line2b = new_ws + (
                                            line2.split(", ")[1]
                                        )
                                        new_sb_lines.append(line2a)
                                        new_sb_lines.append(line2b)
                                        continue
                                    elif line2.count('="') == 1 and (
                                        line2.lstrip().startswith("'")
                                    ):
                                        line2a = line2.split('="')[0] + "='"
                                        line2b = (
                                            new_ws
                                            + "'\""
                                            + (line2.split('="')[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        new_sb_lines.append(line2b)
                                        continue
                                    elif line2.count("='") == 1 and (
                                        line2.lstrip().startswith('"')
                                    ):
                                        line2a = line2.split("='")[0] + '="'
                                        line2b = (
                                            new_ws
                                            + "\"'"
                                            + (line2.split("='")[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        new_sb_lines.append(line2b)
                                        continue
                                new_sb_lines.append(line2)
                            elif get_width(line2) + 4 + w <= console_width:
                                line2 = "    " + line2
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                            else:
                                new_sb_lines.append(line)
                            continue
                        if line.count('("') == 1:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split('("')[0] + "("
                            line2 = new_ws + '"' + line.split('("')[1]
                            if not ("):") in line2:
                                new_sb_lines.append(line1)
                                if get_width(line2) + w > console_width:
                                    if line2.count('" in self.') == 1:
                                        line2a = (
                                            line2.split('" in self.')[0]
                                            + '" in'
                                        )
                                        line2b = (
                                            new_ws
                                            + "self."
                                            + (line2.split('" in self.')[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        new_sb_lines.append(line2b)
                                        continue
                                new_sb_lines.append(line2)
                            elif get_width(line2) + 4 + w <= console_width:
                                line2 = "    " + line2
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                            else:
                                new_sb_lines.append(line)
                            continue
                        if line.count("('") == 1:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split("('")[0] + "("
                            line2 = new_ws + "'" + line.split("('")[1]
                            if not ("):") in line2:
                                new_sb_lines.append(line1)
                                if get_width(line2) + w > console_width:
                                    if line2.count("' in self.") == 1:
                                        line2a = (
                                            line2.split("' in self.")[0]
                                            + "' in"
                                        )
                                        line2b = (
                                            new_ws
                                            + "self."
                                            + (line2.split("' in self.")[1])
                                        )
                                        new_sb_lines.append(line2a)
                                        new_sb_lines.append(line2b)
                                        continue
                                new_sb_lines.append(line2)
                            elif get_width(line2) + 4 + w <= console_width:
                                line2 = "    " + line2
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                            else:
                                new_sb_lines.append(line)
                            continue
                        if line.count('= "') == 1 and line.count("://") == 1:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split("://")[0] + '://" \\'
                            line2 = new_ws + '"' + line.split("://")[1]
                            new_sb_lines.append(line1)
                            if get_width(line2) + w > console_width:
                                if line2.count("/") > 0:
                                    slash_one = line2.find("/")
                                    slash_one_p1 = slash_one + 1
                                    line2a = line2[:slash_one_p1] + '" \\'
                                    line2b = (
                                        new_ws + '"' + line2[slash_one_p1:]
                                    )
                                    new_sb_lines.append(line2a)
                                    new_sb_lines.append(line2b)
                                    continue
                            new_sb_lines.append(line2)
                            continue
                        if line.count("= '") == 1 and line.count("://") == 1:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split("://")[0] + "://' \\"
                            line2 = new_ws + "'" + line.split("://")[1]
                            new_sb_lines.append(line1)
                            if get_width(line2) + w > console_width:
                                if line2.count("/") > 0:
                                    slash_one = line2.find("/")
                                    slash_one_p1 = slash_one + 1
                                    line2a = line2[:slash_one_p1] + "' \\"
                                    line2b = (
                                        new_ws + "'" + line2[slash_one_p1:]
                                    )
                                    new_sb_lines.append(line2a)
                                    new_sb_lines.append(line2b)
                                    continue
                            new_sb_lines.append(line2)
                            continue
                        if line.count("(self.") == 1 and not ("):") in line:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split("(self.")[0] + "("
                            line2 = new_ws + "self." + line.split("(self.")[1]
                            if get_width(line1) + w <= console_width:
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                                continue
                        if line.count(" == ") == 1 and not (
                            line.endswith(":") or (":  #") in line
                        ):
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split(" == ")[0] + " == ("
                            line2 = new_ws + line.split(" == ")[1] + ")"
                            if get_width(line1) + w <= console_width and (
                                get_width(line2) + w <= console_width
                            ):
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                                continue
                        if line.count(" == ") == 1 and line.endswith(":"):
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "        "
                            line1 = line.split(" == ")[0] + " == ("
                            line2 = new_ws + line.split(" == ")[1][:-1] + "):"
                            if get_width(line1) + w <= console_width and (
                                get_width(line2) + w <= console_width
                            ):
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                                continue
                        if (
                            line.count(" == ") == 1
                            and (line.count(":  #") == 1)
                            and (line.find(" == ") < line.find(":  #"))
                        ):
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "        "
                            comments = "  #" + line.split(":  #")[1]
                            line0 = line.split(":  #")[0] + ":"
                            line1 = line0.split(" == ")[0] + " == ("
                            line2 = new_ws + line0.split(" == ")[1][:-1] + "):"
                            if get_width(line1) + w <= console_width and (
                                get_width(line2) + w <= console_width
                            ):
                                new_sb_lines.append(line1)
                                if (
                                    get_width(line2 + comments) + w
                                    <= console_width
                                ):
                                    new_sb_lines.append(line2 + comments)
                                else:
                                    new_sb_lines.append(line2)
                                continue
                        if line.count(" % ") == 1 and not ("):") in line:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split(" % ")[0] + " \\"
                            line2 = new_ws + "% " + line.split(" % ")[1]
                            if get_width(line1) + w <= console_width:
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                                continue
                        if line.count(" = ") == 1 and not ("  # ") in line:
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "    "
                            line1 = line.split(" = ")[0] + " = ("
                            line2 = new_ws + line.split(" = ")[1] + ")"
                            if get_width(line1) + w <= console_width and (
                                get_width(line2) + w <= console_width
                            ):
                                new_sb_lines.append(line1)
                                new_sb_lines.append(line2)
                                continue
                            elif get_width(line1) + w <= console_width:
                                if line2.count(" % ") == 1 and not (
                                    line2.endswith(":")
                                ):
                                    whitespace = line_length2 - len(
                                        line2.lstrip()
                                    )
                                    line2a = line2.split(" % ")[0] + " \\"
                                    line2b = (
                                        new_ws + "% " + line2.split(" % ")[1]
                                    )
                                    if get_width(line2a) + w <= console_width:
                                        if (
                                            get_width(line2b) + w
                                            <= console_width
                                        ):
                                            new_sb_lines.append(line1)
                                            new_sb_lines.append(line2a)
                                            new_sb_lines.append(line2b)
                                            continue
                        if (
                            line.count(" = ") == 1
                            and (line.count("  # ") == 1)
                            and (line.find(" = ") < line.find("  # "))
                        ):
                            whitespace = line_length2 - len(line.lstrip())
                            new_ws = line[0:whitespace] + "        "
                            comments = "  # " + line.split("  # ")[1]
                            line0 = line.split("  # ")[0]
                            line1 = line0.split(" = ")[0] + " = ("
                            line2 = new_ws + line0.split(" = ")[1] + ")"
                            if get_width(line1) + w <= console_width and (
                                get_width(line2) + w <= console_width
                            ):
                                new_sb_lines.append(line1)
                                if (
                                    get_width(line2 + comments) + w
                                    <= console_width
                                ):
                                    new_sb_lines.append(line2 + comments)
                                else:
                                    new_sb_lines.append(line2)
                                continue
                    new_sb_lines.append(line)

            if new_sb_lines:
                seleniumbase_lines = new_sb_lines
                python_code = "\n".join(seleniumbase_lines)

            extra_r_spaces = 2
            if console_width and (code_width + extra_r_spaces < console_width):
                used_width = code_width + extra_r_spaces

            magic_syntax = Syntax(
                python_code,
                "python",
                theme="monokai",
                line_numbers=line_numbers,
                code_width=used_width,
                word_wrap=word_wrap,
            )
            magic_console = Console()
        print("")
        print(save_line)
        print(" " + c1 + " ***  Here are the results:  >>> " + cr)
        # ----------------------------------------
        dash_length = 62  # May change
        if used_width and used_width + w < console_width:
            dash_length = used_width + w
        elif console_width:
            dash_length = console_width
        dashes = "-" * dash_length
        print(dashes)
        print_success = False
        if magic_syntax:
            try:
                magic_console.print(magic_syntax)
                print_success = True
            except Exception:
                pass
        if not magic_syntax or not print_success:
            for line in seleniumbase_lines:
                print(line)
        print(dashes)
        # ----------------------------------------

    new_file_name = None
    if copy:
        base_file_name = seleniumbase_file.split(".py")[0]
        new_locale = MD_F.get_locale_code(new_lang)
        new_ext = "_" + new_locale + ".py"
        for locale in MD_F.get_locale_list():
            ext = "_" + locale + ".py"
            if seleniumbase_file.endswith(ext):
                base_file_name = seleniumbase_file.split(ext)[0]
                break
        new_file_name = base_file_name + new_ext
    elif overwrite:
        new_file_name = seleniumbase_file
    else:
        pass  # Print-only run already done

    if not print_only:
        print("")
        print(save_line)
    else:
        pass  # Print-only run already done

    if new_file_name:
        out_file = codecs.open(new_file_name, "w+", encoding="utf-8")
        out_file.writelines("\r\n".join(seleniumbase_lines))
        out_file.close()
        results_saved = (
            "The translation was saved to: [[[%s]]]\n" "" % new_file_name
        )
        results_saved = results_saved.replace("[[[", "" + c1)
        results_saved = results_saved.replace("]]]", cr + "")
        print(results_saved)


if __name__ == "__main__":
    invalid_run_command()
