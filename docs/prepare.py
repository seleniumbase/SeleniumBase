import codecs
import os
import re
from pathlib import Path

GITHUB_URL = r"https://github.com/seleniumbase/SeleniumBase/blob/master/"
ROOT_DIR = Path(__file__).parents[1]
URL_PATTERN = re.compile(
    r"(?:\(|<a href=\")(?P<url>{}[\w/.]+\.md)(?:\)|\")".format(GITHUB_URL)
)
MD_PATH_PATTERN = re.compile(r"\[.*\]\((?P<path>[\w\\._/]+\.md)\)")
HEADER_PATTERN = re.compile(
    r"^(?P<level>#+)\s*(<[\w\s=\":/.]+>)?\s*\**(?P<header>.*[\w`]):?\**\s*$",
    flags=re.MULTILINE,
)

PROCESSED_PATHS = set()


def normalize_path(path):
    path = Path(path).absolute().relative_to(ROOT_DIR)
    return str(path).replace("\\", "/")


def read_file(file_name):
    path = ROOT_DIR / file_name
    with path.open() as file_handle:
        content = file_handle.read()
    return content


def process_file(file_name):
    content = read_file(file_name)
    urls = URL_PATTERN.findall(content)
    # content = content.replace("<br />", "  \n")
    content = re.sub(HEADER_PATTERN, r"\g<level> \g<header>", content)
    directory = "/".join(normalize_path(file_name).split("/")[:-1])

    paths = set()

    md_paths = MD_PATH_PATTERN.findall(content)
    for md_path in md_paths:
        path = md_path.lstrip("/")
        if (ROOT_DIR / directory / path).exists():
            path = ROOT_DIR / directory / path
        else:
            path = ROOT_DIR / path
        path = path.resolve().relative_to(ROOT_DIR)
        paths.add(normalize_path(path))
        content = content.replace("(" + md_path + ")", normalize_path(path))

    for url in urls:
        path = url[len(GITHUB_URL):]
        paths.add(path)
        content = content.replace(
            url, normalize_path(os.path.relpath(path, directory))
        )

    output_path = ROOT_DIR / "docs" / file_name
    if not output_path.parent.is_dir():
        os.makedirs(output_path.parent)

    with output_path.open("w+") as output_file:
        output_file.write(content)
    PROCESSED_PATHS.add(normalize_path(file_name))

    for path in paths:
        if path not in PROCESSED_PATHS:
            process_file(normalize_path(path))


def main(*args, **kwargs):
    files_to_process = ["README.md"]
    for dir_ in os.listdir(ROOT_DIR / "help_docs"):
        files_to_process.append(os.path.join("help_docs", dir_))

    updated_files_to_process = []
    for file_ in files_to_process:
        if file_.endswith(".md"):
            updated_files_to_process.append(file_)

    for file_ in updated_files_to_process:
        process_file(file_)

    readme_file = "./docs/README.md"
    with open(readme_file, 'r', encoding='utf-8') as f:
        all_code = f.read()
    code_lines = all_code.split('\n')

    changed = False
    seleniumbase_lines = []
    for line in code_lines:
        if ' href="' in line and '.md"' in line:
            changed = True
            line = line.replace('.md"', '/"')
        if "<!-- View on GitHub -->" in line:
            changed = True
            line = (
                r'<p align="center"><div align="center">'
                r'<a href="https://github.com/seleniumbase/SeleniumBase">'
                r'<img src="https://img.shields.io/badge/'
                r'✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀'
                r'-02A79E.svg" alt="SeleniumBase on GitHub" />'
                r'</a></div></p>')
        if "<!-- SeleniumBase Header1 -->" in line:
            changed = True
            line = (
                '<section align="center"><div align="center">'
                '<h2>✅ Reliable Browser Testing</h2>'
                '</div></section>')
        if "<!-- SeleniumBase Docs -->" in line:
            changed = True
            line = (
                '<h2><img src="https://seleniumbase.io/img/sb_icon.png" '
                'title="SeleniumBase" width="20" /> SeleniumBase Docs '
                '<img src="https://seleniumbase.io/img/sb_icon.png" '
                'title="SeleniumBase" width="20" /></h2>')
        seleniumbase_lines.append(line)
    if changed:
        out_file = codecs.open(readme_file, "w+", encoding='utf-8')
        out_file.writelines("\r\n".join(seleniumbase_lines))
        out_file.close()
