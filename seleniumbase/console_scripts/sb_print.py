"""
Prints the code/text of any file with syntax-highlighting

Usage:
        seleniumbase print [FILE] [OPTIONS]
        OR:    sbase print [FILE] [OPTIONS]
Options:
        -n   (Add line Numbers to the rows)
Output:
        Prints the code/text of any file
        with syntax-highlighting.
"""

import colorama
import os
import sys


def invalid_run_command(msg=None):
    exp = "  ** print **\n\n"
    exp += "  Usage:\n"
    exp += "         seleniumbase print [FILE] [OPTIONS]\n"
    exp += "         OR:    sbase print [FILE] [OPTIONS]\n"
    exp += "  Options:\n"
    exp += "         -n   (Add line Numbers to the rows)\n"
    exp += "  Output:\n"
    exp += "         Prints the code/text of any file\n"
    exp += "         with syntax-highlighting.\n"
    if not msg:
        raise Exception("INVALID RUN COMMAND!\n\n%s" % exp)
    else:
        raise Exception("INVALID RUN COMMAND!\n%s\n\n%s" % (msg, exp))


def sc_ranges():
    # Get the ranges of special characters of Chinese, Japanese, and Korean.
    special_char_ranges = [
        {"from": ord("\u4e00"), "to": ord("\u9FFF")},
        {"from": ord("\u3040"), "to": ord("\u30ff")},
        {"from": ord("\uac00"), "to": ord("\ud7a3")},
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


def main():
    colorama.init(autoreset=True)
    c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
    c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
    cr = colorama.Style.RESET_ALL
    line_numbers = False
    word_wrap = True  # Always use word wrap now
    help_me = False
    invalid_cmd = None
    is_python_file = False
    code_lang = None

    command_args = sys.argv[2:]
    file_to_print = command_args[0]
    if file_to_print.lower().endswith(".py"):
        is_python_file = True
        code_lang = "python"
    elif file_to_print.lower().endswith(".js"):
        code_lang = "javascript"
    elif file_to_print.lower().endswith(".md"):
        code_lang = "markdown"
    elif file_to_print.lower().endswith(".html"):
        code_lang = "html"
    elif file_to_print.lower().endswith(".css"):
        code_lang = "css"
    elif file_to_print.lower().endswith(".go"):
        code_lang = "go"
    elif file_to_print.lower().endswith(".java"):
        code_lang = "java"
    elif "." not in file_to_print:
        code_lang = "markdown"
    else:
        code_lang = file_to_print.split(".")[-1].lower()

    if len(command_args) >= 2:
        options = command_args[1:]
        for option in options:
            option = option.lower()
            if option == "-n":
                line_numbers = True
            elif option == "-w":
                word_wrap = True
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

    with open(file_to_print, "r", encoding="utf-8") as f:
        all_code = f.read()
    all_code = all_code.replace("\t", "    ")
    code_lines = all_code.split("\n")

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

    use_rich = False
    if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
        use_rich = True

    if use_rich:
        from rich.console import Console
        from rich.syntax import Syntax

        the_code = "\n".join(code_lines)
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

        if is_python_file:
            new_sb_lines = []
            for line in code_lines:
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
                                                    line2b[: slash_one + 1]
                                                    + '"'
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
                                                    line2b[: slash_one + 1]
                                                    + "'"
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
                                    line2a = line2[: slash_one + 1] + '" \\'
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
                                    line2a = line2[: slash_one + 1] + "' \\"
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
                code_lines = new_sb_lines
                the_code = "\n".join(code_lines)

        if code_lang != "python":
            for line in code_lines:
                line_length = get_width(line)
                if line_length > code_width:
                    code_width = line_length

        extra_r_spaces = 2
        if console_width and (code_width + extra_r_spaces < console_width):
            used_width = code_width + extra_r_spaces

        try:
            if "🗺️" in the_code:
                # Fix width of an emoji
                the_code = the_code.replace("🗺️", "🗺️ ")
        except Exception:
            pass

        magic_syntax = Syntax(
            the_code,
            code_lang,
            theme="monokai",
            line_numbers=line_numbers,
            code_width=used_width,
            word_wrap=word_wrap,
        )
        magic_console = Console()
    # ----------------------------------------
    dash_length = 62  # May change
    if used_width and used_width + w < console_width:
        dash_length = used_width + w
    elif console_width:
        dash_length = console_width
    dashes = "-" * dash_length
    print(dashes)
    print_success = False
    if use_rich and code_lang == "markdown":
        try:
            from rich.markdown import Markdown

            markdown = Markdown(all_code)
            markdown_console = Console()
            markdown_console.print(markdown)  # noqa
            print_success = True
        except Exception:
            pass
    elif use_rich and magic_syntax:
        try:
            magic_console.print(magic_syntax)  # noqa
            print_success = True
        except Exception:
            pass
    if not use_rich or not magic_syntax or not print_success:
        for line in code_lines:
            print(line)
    print(dashes)
    # ----------------------------------------


if __name__ == "__main__":
    invalid_run_command()
