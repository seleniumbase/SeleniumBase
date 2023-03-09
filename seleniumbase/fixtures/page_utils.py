"""This module contains useful utility methods."""
import codecs
import fasteners
import os
import re
import requests
from seleniumbase.fixtures import constants


def get_domain_url(url):
    """
    Use this to convert a url like this:
    https://blog.xkcd.com/2014/07/22/what-if-book-tour/
    Into this:
    https://blog.xkcd.com
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        return url
    url_header = url.split("://")[0]
    simple_url = url.split("://")[1]
    base_url = simple_url.split("/")[0]
    domain_url = url_header + "://" + base_url
    return domain_url


def is_xpath_selector(selector):
    """Determine if a selector is an xpath selector."""
    if (
        selector.startswith("/")
        or selector.startswith("./")
        or selector.startswith("(")
    ):
        return True
    return False


def is_link_text_selector(selector):
    """Determine if a selector is a link text selector."""
    if (
        selector.startswith("link=")
        or selector.startswith("link_text=")
        or selector.startswith("text=")
    ):
        return True
    return False


def is_partial_link_text_selector(selector):
    """Determine if a selector is a partial link text selector."""
    if (
        selector.startswith("partial_link=")
        or selector.startswith("partial_link_text=")
        or selector.startswith("partial_text=")
        or selector.startswith("p_link=")
        or selector.startswith("p_link_text=")
        or selector.startswith("p_text=")
    ):
        return True
    return False


def is_name_selector(selector):
    """Determine if a selector is a name selector."""
    if selector.startswith("name=") or selector.startswith("&"):
        return True
    return False


def get_link_text_from_selector(selector):
    """Get the link text from a link text selector."""
    if selector.startswith("link="):
        return selector[len("link="):]
    elif selector.startswith("link_text="):
        return selector[len("link_text="):]
    elif selector.startswith("text="):
        return selector[len("text="):]
    return selector


def get_partial_link_text_from_selector(selector):
    """Get the partial link text from a partial link selector."""
    if selector.startswith("partial_link="):
        return selector[len("partial_link="):]
    elif selector.startswith("partial_link_text="):
        return selector[len("partial_link_text="):]
    elif selector.startswith("partial_text="):
        return selector[len("partial_text="):]
    elif selector.startswith("p_link="):
        return selector[len("p_link="):]
    elif selector.startswith("p_link_text="):
        return selector[len("p_link_text="):]
    elif selector.startswith("p_text="):
        return selector[len("p_text="):]
    return selector


def get_name_from_selector(selector):
    """Get the name from a name selector."""
    if selector.startswith("name="):
        return selector[len("name="):]
    if selector.startswith("&"):
        return selector[len("&"):]
    return selector


def is_valid_url(url):
    regex = re.compile(
        r"^(?:http)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+"
        r"(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    if (
        regex.match(url)
        or url.startswith("about:")
        or url.startswith("data:")
        or url.startswith("chrome:")
        or url.startswith("edge:")
        or url.startswith("opera:")
        or url.startswith("file:")
    ):
        return True
    else:
        return False


def _get_unique_links(page_url, soup):
    """Returns all unique links.
    Includes:
        "a"->"href", "img"->"src", "link"->"href", and "script"->"src" links.
    """
    if not page_url.startswith("http://") and not page_url.startswith(
        "https://"
    ):
        return []
    prefix = "http:"
    if page_url.startswith("https:"):
        prefix = "https:"
    simple_url = page_url.split("://")[1]
    base_url = simple_url.split("/")[0]
    full_base_url = prefix + "//" + base_url

    raw_links = []
    raw_unique_links = []

    # Get "href" from all "a" tags
    links = soup.find_all("a")
    for link in links:
        raw_links.append(link.get("href"))

    # Get "src" from all "img" tags
    img_links = soup.find_all("img")
    for img_link in img_links:
        raw_links.append(img_link.get("src"))

    # Get "href" from all "link" tags
    links = soup.find_all("link")
    for link in links:
        raw_links.append(link.get("href"))

    # Get "src" from all "script" tags
    img_links = soup.find_all("script")
    for img_link in img_links:
        raw_links.append(img_link.get("src"))

    for link in raw_links:
        if link not in raw_unique_links:
            raw_unique_links.append(link)

    unique_links = []
    for link in raw_unique_links:
        if link and len(link) > 1:
            if link.startswith("//"):
                link = prefix + link
            elif link.startswith("/"):
                link = full_base_url + link
            elif link.startswith("./"):
                f_b_url = full_base_url
                if len(simple_url.split("/")) > 1:
                    f_b_url = full_base_url + "/" + simple_url.split("/")[1]
                link = f_b_url + link[1:]
            elif link.startswith("#"):
                link = full_base_url + link
            elif "//" not in link:
                f_b_url = full_base_url
                if len(simple_url.split("/")) > 1:
                    f_b_url = full_base_url + "/" + simple_url.split("/")[1]
                link = f_b_url + "/" + link
            elif link.startswith('"') and link.endswith('"') and len(link) > 4:
                link = link[1:-1]
            else:
                pass
            unique_links.append(link)

    links = unique_links
    links = list(set(links))  # Make sure all duplicates were removed
    links = sorted(links)  # Sort all the links alphabetically
    return links


def _get_link_status_code(
    link,
    allow_redirects=False,
    timeout=5,
    verify=False,
):
    """Get the status code of a link.
    If the timeout is exceeded, will return a 404.
    If "verify" is False, will ignore certificate errors.
    For a list of available status codes, see:
    https://en.wikipedia.org/wiki/List_of_HTTP_status_codes """
    status_code = None
    try:
        response = requests.head(
            link,
            allow_redirects=allow_redirects,
            timeout=timeout,
            verify=verify,
        )
        status_code = response.status_code
    except Exception:
        status_code = 404
    return status_code


def _print_unique_links_with_status_codes(page_url, soup):
    """Finds all unique links in the html of the page source
    and then prints out those links with their status codes.
    Format:  ["link"  ->  "status_code"]  (per line)
    Page links include those obtained from:
    "a"->"href", "img"->"src", "link"->"href", and "script"->"src". """
    links = _get_unique_links(page_url, soup)
    for link in links:
        status_code = _get_link_status_code(link)
        print(link, " -> ", status_code)


def _download_file_to(file_url, destination_folder, new_file_name=None):
    if new_file_name:
        file_name = new_file_name
    else:
        file_name = file_url.split("/")[-1]
    r = requests.get(file_url)
    file_path = os.path.join(destination_folder, file_name)
    download_file_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.DOWNLOAD_FILE_LOCK
    )
    with download_file_lock:
        with open(file_path, "wb") as code:
            code.write(r.content)


def _save_data_as(data, destination_folder, file_name):
    download_file_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.DOWNLOAD_FILE_LOCK
    )
    with download_file_lock:
        out_file = codecs.open(
            os.path.join(destination_folder, file_name), "w+", encoding="utf-8"
        )
        out_file.writelines(data)
        out_file.close()


def _append_data_to_file(data, destination_folder, file_name):
    download_file_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.DOWNLOAD_FILE_LOCK
    )
    with download_file_lock:
        existing_data = ""
        if os.path.exists(os.path.join(destination_folder, file_name)):
            with open(os.path.join(destination_folder, file_name), "r") as f:
                existing_data = f.read()
            if not existing_data.split("\n")[-1] == "":
                existing_data += "\n"
        out_file = codecs.open(
            os.path.join(destination_folder, file_name), "w+", encoding="utf-8"
        )
        out_file.writelines("%s%s" % (existing_data, data))
        out_file.close()


def _get_file_data(folder, file_name):
    download_file_lock = fasteners.InterProcessLock(
        constants.MultiBrowser.DOWNLOAD_FILE_LOCK
    )
    with download_file_lock:
        if not os.path.exists(os.path.join(folder, file_name)):
            raise Exception("File not found!")
        with open(os.path.join(folder, file_name), "r") as f:
            data = f.read()
        return data


def make_css_match_first_element_only(selector):
    # Only get the first match
    last_syllable = selector.split(" ")[-1]
    if ":first" not in last_syllable:
        selector += ":first"
    return selector
