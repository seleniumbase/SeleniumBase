"""
This module contains useful utility methods.
"""
import requests


def jq_format(code):
    """
    Use before throwing raw code such as 'div[tab="advanced"]' into jQuery.
    Selectors with quotes inside of quotes would otherwise break jQuery.
    This is similar to "json.dumps(value)", but with one less layer of quotes.
    """
    code = code.replace('\\', '\\\\').replace('\t', '\\t').replace('\n', '\\n')
    code = code.replace('\"', '\\\"').replace('\'', '\\\'')
    code = code.replace('\v', '\\v').replace('\a', '\\a').replace('\f', '\\f')
    code = code.replace('\b', '\\b').replace('\u', '\\u').replace('\r', '\\r')
    return code


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


def _download_file_to(file_url, destination_folder, new_file_name=None):
    if new_file_name:
        file_name = new_file_name
    else:
        file_name = file_url.split('/')[-1]
    r = requests.get(file_url)
    with open(destination_folder + '/' + file_name, "wb") as code:
        code.write(r.content)
