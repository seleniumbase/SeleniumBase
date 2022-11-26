""" For preparing the mkdocs-generated seleniumbase.io website. """

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
        path = url[len(GITHUB_URL) :]  # noqa: E203
        paths.add(path)
        content = content.replace(
            url, normalize_path(os.path.relpath(path, directory))
        )

    output_path = ROOT_DIR / "mkdocs_build" / file_name
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
    scanned_dir_list = []
    scanned_dir_list.append("help_docs")
    scanned_dir_list.append("examples")
    scanned_dir_list.append("examples/behave_bdd")
    scanned_dir_list.append("examples/example_logs")
    scanned_dir_list.append("examples/presenter")
    scanned_dir_list.append("examples/chart_maker")
    scanned_dir_list.append("examples/tour_examples")
    scanned_dir_list.append("examples/visual_testing")
    scanned_dir_list.append("integrations/google_cloud")
    scanned_dir_list.append("seleniumbase/console_scripts")
    for scanned_dir in scanned_dir_list:
        for dir_ in os.listdir(ROOT_DIR / scanned_dir):
            files_to_process.append(os.path.join(scanned_dir, dir_))

    video_embed = (
        '<figure class="wp-block-embed wp-block-embed-youtube is-type-video '
        'is-provider-youtube"><div class="wp-block-embed__wrapper">'
        '<div class="epyt-video-wrapper fluid-width-video-wrapper" '
        'style="padding-top: 3px !important;"><iframe loading="lazy" '
        'id="_ytid_36718" data-origwidth="1200" data-origheight="675" '
        'src="https://www.youtube.com/embed/yt_code?enablejsapi=1&amp;'
        "origin=https://seleniumbase.io&amp;autoplay=0&amp;cc_load_policy=0"
        "&amp;cc_lang_pref=&amp;iv_load_policy=1&amp;loop=0&amp;"
        "modestbranding=1&amp;rel=0&amp;fs=1&amp;playsinline=0&amp;"
        'autohide=2&amp;theme=dark&amp;color=red&amp;controls=1&amp;" '
        'class="__youtube_prefs__ no-lazyload" title="YouTube player" '
        'allow="autoplay; encrypted-media" allowfullscreen="" '
        'data-no-lazy="1" data-skipgform_ajax_framebjll="">'
        "</iframe></div></div></figure>"
    )

    updated_files_to_process = []
    for file_ in files_to_process:
        if file_.endswith(".md"):
            updated_files_to_process.append(file_)

    for file_ in updated_files_to_process:
        process_file(file_)

    for file_ in updated_files_to_process:
        readme_file = "./mkdocs_build/" + file_
        with open(readme_file, "r", encoding="utf-8") as f:
            all_code = f.read()
        code_lines = all_code.split("\n")

        changed = False
        seleniumbase_lines = []
        for line in code_lines:
            if ' href="' in line and '.md"' in line:
                changed = True
                line = line.replace('.md"', '/"')
            if "<!-- SeleniumBase Docs -->" in line:
                changed = True
                new_lines = []
                new_lines.append("---")
                new_lines.append("hide:")
                new_lines.append("  - toc")
                new_lines.append("---")
                for line in new_lines:
                    seleniumbase_lines.append(line)
                continue
            if "<!-- View on GitHub -->" in line:
                changed = True
                line = (
                    r'<p align="center"><div align="center">'
                    r'<a href="https://github.com/seleniumbase/SeleniumBase">'
                    r'<img src="https://img.shields.io/badge/'
                    r"✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀"
                    r'-02A79E.svg" alt="SeleniumBase on GitHub" />'
                    r"</a></div></p>"
                )
            alt_link_badge = (
                '<a href="https://seleniumbase.io">'
                '<img src="https://img.shields.io/badge/docs-seleniumbase.io'
                '-11BBAA.svg" alt="SeleniumBase Docs" /></a>'
            )
            back_to_gh = (
                r'<a href="https://github.com/seleniumbase/SeleniumBase">'
                r'<img src="https://img.shields.io/badge/'
                r"✅%20View%20Code-on%20GitHub%20🌎"
                r'-02A79E.svg" alt="SeleniumBase on GitHub" />'
                r"</a>"
            )
            if alt_link_badge in line:
                line = line.replace(alt_link_badge, back_to_gh)
            if "<!-- GitHub Only -->" in line:
                changed = True
                continue
            if "<!-- YouTube View -->" in line and "watch?v=" in line:
                start_pt = line.find("watch?v=") + len("watch?v=")
                end_pt = line.find('"', start_pt + 1)
                yt_code = line[start_pt:end_pt]
                changed = True
                line = video_embed.replace("yt_code", yt_code)
            if "<!-- SeleniumBase Header1 -->" in line:
                changed = True
                line = (
                    '<section align="center"><div align="center">'
                    "<h2>✅ Reliable Browser Testing</h2>"
                    "</div></section>"
                )
            if "<!-- SeleniumBase Docs -->" in line:
                changed = True
                line = (
                    '<h2><img '
                    'src="https://seleniumbase.github.io/img/logo3b.png" '
                    'title="SeleniumBase" width="24" /> SeleniumBase Docs '
                    '<img '
                    'src="https://seleniumbase.github.io/img/logo3b.png" '
                    'title="SeleniumBase" width="24" /></h2>'
                )
            seleniumbase_lines.append(line)
        if changed:
            out_file = codecs.open(readme_file, "w+", encoding="utf-8")
            out_file.writelines("\r\n".join(seleniumbase_lines))
            out_file.close()
