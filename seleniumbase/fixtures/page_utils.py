"""
This module contains useful utility methods.
"""
import codecs
import re
import requests


def get_domain_url(url):
    """
    Use this to convert a url like this:
    https://blog.xkcd.com/2014/07/22/what-if-book-tour/
    Into this:
    https://blog.xkcd.com
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        return url
    url_header = url.split('://')[0]
    simple_url = url.split('://')[1]
    base_url = simple_url.split('/')[0]
    domain_url = url_header + '://' + base_url
    return domain_url


def is_xpath_selector(selector):
    """
    A basic method to determine if a selector is an xpath selector.
    """
    if (selector.startswith('/') or selector.startswith('./') or (
            selector.startswith('('))):
        return True
    return False


def is_link_text_selector(selector):
    """
    A basic method to determine if a selector is a link text selector.
    """
    if (selector.startswith('link=') or selector.startswith('link_text=') or (
            selector.startswith('text='))):
        return True
    return False


def is_partial_link_text_selector(selector):
    """
    A basic method to determine if a selector is a partial link text selector.
    """
    if (selector.startswith('partial_link=') or (
            selector.startswith('partial_link_text=') or (
            selector.startswith('partial_text=')))):
        return True
    return False


def is_name_selector(selector):
    """
    A basic method to determine if a selector is a name selector.
    """
    if selector.startswith('name='):
        return True
    return False


def get_link_text_from_selector(selector):
    """
    A basic method to get the link text from a link text selector.
    """
    if selector.startswith('link='):
        return selector.split('link=')[1]
    elif selector.startswith('link_text='):
        return selector.split('link_text=')[1]
    elif selector.startswith('text='):
        return selector.split('text=')[1]
    return selector


def get_partial_link_text_from_selector(selector):
    """
    A basic method to get the partial link text from a partial link selector.
    """
    if selector.startswith('partial_link='):
        return selector.split('partial_link=')[1]
    elif selector.startswith('partial_link_text='):
        return selector.split('partial_link_text=')[1]
    elif selector.startswith('partial_text='):
        return selector.split('partial_text=')[1]
    return selector


def get_name_from_selector(selector):
    """
    A basic method to get the name from a name selector.
    """
    if selector.startswith('name='):
        return selector.split('name=')[1]
    return selector


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.match(url) or ((url.startswith("about:") or (
            url.startswith("data:") or url.startswith("chrome:") or (
            url.startswith("edge:") or url.startswith("opera:") or (
            url.startswith("file:")))))):
        return True
    else:
        return False


def _get_unique_links(page_url, soup):
    """
    Returns all unique links.
    Includes:
        "a"->"href", "img"->"src", "link"->"href", and "script"->"src" links.
    """
    if not page_url.startswith("http://") and (
            not page_url.startswith("https://")):
        return []
    prefix = 'http:'
    if page_url.startswith('https:'):
        prefix = 'https:'
    simple_url = page_url.split('://')[1]
    base_url = simple_url.split('/')[0]
    full_base_url = prefix + "//" + base_url

    raw_links = []
    raw_unique_links = []

    # Get "href" from all "a" tags
    links = soup.find_all('a')
    for link in links:
        raw_links.append(link.get('href'))

    # Get "src" from all "img" tags
    img_links = soup.find_all('img')
    for img_link in img_links:
        raw_links.append(img_link.get('src'))

    # Get "href" from all "link" tags
    links = soup.find_all('link')
    for link in links:
        raw_links.append(link.get('href'))

    # Get "src" from all "script" tags
    img_links = soup.find_all('script')
    for img_link in img_links:
        raw_links.append(img_link.get('src'))

    for link in raw_links:
        if link not in raw_unique_links:
            raw_unique_links.append(link)

    unique_links = []
    for link in raw_unique_links:
        if link and len(link) > 1:
            if link.startswith('//'):
                link = prefix + link
            elif link.startswith('/'):
                link = full_base_url + link
            elif link.startswith('./'):
                link = full_base_url + link[1:]
            elif link.startswith('#'):
                link = full_base_url + link
            elif '//' not in link:
                link = full_base_url + "/" + link
            else:
                pass
            unique_links.append(link)

    return unique_links


def _get_link_status_code(link, allow_redirects=False, timeout=5):
    """ Get the status code of a link.
        If the timeout is exceeded, will return a 404.
        For a list of available status codes, see:
        https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    """
    status_code = None
    try:
        response = requests.get(
            link, allow_redirects=allow_redirects, timeout=timeout)
        status_code = response.status_code
    except Exception:
        status_code = 404
    return status_code


def _print_unique_links_with_status_codes(page_url, soup):
    """ Finds all unique links in the html of the page source
        and then prints out those links with their status codes.
        Format:  ["link"  ->  "status_code"]  (per line)
        Page links include those obtained from:
        "a"->"href", "img"->"src", "link"->"href", and "script"->"src".
    """
    links = _get_unique_links(page_url, soup)
    for link in links:
        status_code = _get_link_status_code(link)
        print(link, " -> ", status_code)


def _download_file_to(file_url, destination_folder, new_file_name=None):
    if new_file_name:
        file_name = new_file_name
    else:
        file_name = file_url.split('/')[-1]
    r = requests.get(file_url)
    with open(destination_folder + '/' + file_name, "wb") as code:
        code.write(r.content)


def _save_data_as(data, destination_folder, file_name):
    out_file = codecs.open(
        destination_folder + '/' + file_name, "w+", encoding="utf-8")
    out_file.writelines(data)
    out_file.close()


def make_css_match_first_element_only(selector):
    # Only get the first match
    last_syllable = selector.split(' ')[-1]
    if ':' not in last_syllable and ':contains' not in selector:
        selector += ':first'
    return selector
