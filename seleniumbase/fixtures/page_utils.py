"""
This module contains useful utility methods.
"""


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
    url_header = url.split('://')[0]
    simple_url = url.split('://')[1]
    base_url = simple_url.split('/')[0]
    domain_url = url_header + '://' + base_url
    return domain_url
