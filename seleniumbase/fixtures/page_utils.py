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
    url_header = url.split('://')[0]
    simple_url = url.split('://')[1]
    base_url = simple_url.split('/')[0]
    domain_url = url_header + '://' + base_url
    return domain_url


def is_xpath_selector(selector):
    """
    A basic method to determine if a selector is an xpath selector.
    """
    if (selector.startswith('/') or
            selector.startswith('./') or
            selector.startswith('(')):
        return True
    return False


def is_link_text_selector(selector):
    """
    A basic method to determine if a selector is a link text selector.
    """
    if (selector.startswith('link=') or
            selector.startswith('link_text=')):
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
    if regex.match(url) or url == 'about:blank' or url == 'data:,':
        return True
    else:
        return False


def _download_file_to(file_url, destination_folder, new_file_name=None):
    if new_file_name:
        file_name = new_file_name
    else:
        file_name = file_url.split('/')[-1]
    r = requests.get(file_url)
    with open(destination_folder + '/' + file_name, "wb") as code:
        code.write(r.content)


def _save_data_as(data, destination_folder, file_name):
    out_file = codecs.open(destination_folder + '/' + file_name, "w+")
    out_file.writelines(data)
    out_file.close()


def are_quotes_escaped(string):
    if (string.count("\\'") != string.count("'") or
            string.count('\\"') != string.count('"')):
        return True
    return False


def escape_quotes_if_needed(string):
    """
    re.escape() works differently in Python 3.7.0 than earlier versions:

    Python 3.6.5:
    >>> import re
    >>> re.escape('"')
    '\\"'

    Python 3.7.0:
    >>> import re
    >>> re.escape('"')
    '"'

    SeleniumBase needs quotes to be properly escaped for Javascript calls.
    """
    if are_quotes_escaped(string):
        if string.count("'") != string.count("\\'"):
            string = string.replace("'", "\\'")
        if string.count('"') != string.count('\\"'):
            string = string.replace('"', '\\"')
    return string


def make_css_match_first_element_only(selector):
    # Only get the first match
    last_syllable = selector.split(' ')[-1]
    if ':' not in last_syllable and ':contains' not in selector:
        selector += ':first'
    return selector


def _jq_format(code):
    """
    DEPRECATED - Use re.escape() instead, which performs the intended action.
    Use before throwing raw code such as 'div[tab="advanced"]' into jQuery.
    Selectors with quotes inside of quotes would otherwise break jQuery.
    If you just want to escape quotes, there's escape_quotes_if_needed().
    This is similar to "json.dumps(value)", but with one less layer of quotes.
    """
    code = code.replace('\\', '\\\\').replace('\t', '\\t').replace('\n', '\\n')
    code = code.replace('\"', '\\\"').replace('\'', '\\\'')
    code = code.replace('\v', '\\v').replace('\a', '\\a').replace('\f', '\\f')
    code = code.replace('\b', '\\b').replace(r'\u', '\\u').replace('\r', '\\r')
    return code
