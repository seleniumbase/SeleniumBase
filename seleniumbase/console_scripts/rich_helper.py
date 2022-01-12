from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax


def process_syntax(code, lang, theme, line_numbers, code_width, word_wrap):
    syntax = Syntax(
        code,
        lang,
        theme=theme,
        line_numbers=line_numbers,
        code_width=code_width,
        word_wrap=word_wrap,
    )
    return syntax


def display_markdown(code):
    try:
        markdown = Markdown(code)
        console = Console()
        console.print(markdown)  # noqa
        return True  # Success
    except Exception:
        return False  # Failure


def display_code(code):
    try:
        console = Console()
        console.print(code)  # noqa
        return True  # Success
    except Exception:
        return False  # Failure


def fix_emoji_spacing(code):
    try:
        # Fix the display width of certain emojis that take up two spaces
        double_width_emojis = [
            "🗺️", "🖼️", "🗄️", "⏺️", "♻️", "🗂️", "🖥️", "🕹️", "🎞️"
        ]
        for emoji in double_width_emojis:
            if emoji in code:
                code = code.replace(emoji, emoji + " ")
    except Exception:
        pass
    return code
