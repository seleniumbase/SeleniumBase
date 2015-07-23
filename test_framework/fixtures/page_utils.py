"""
This module contains useful utility methods.
"""

def jq_format(code):
    """
    Use before throwing raw code such as 'div[tab="advanced"]' into jQuery.
    Selectors with quotes inside of quotes would otherwise break jQuery. (One example)
    This is similar to "json.dumps(value)".
    """
    code = code.replace('\\','\\\\').replace('\t','\\t').replace('\n', '\\n').replace('\"','\\\"').replace('\'','\\\'').replace('\r', '\\r').replace('\v', '\\v').replace('\a', '\\a').replace('\f', '\\f').replace('\b', '\\b').replace('\u', '\\u')
    return code
