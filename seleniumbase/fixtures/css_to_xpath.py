"""
Convert CSS selectors into XPath selectors
"""

from cssselect import GenericTranslator


def convert_css_to_xpath(css):
    """ Convert CSS Selectors to XPath Selectors.
        Example:
            convert_css_to_xpath('button:contains("Next")')
            Output => "//button[contains(., 'Next')]"
    """
    xpath = GenericTranslator().css_to_xpath(css, prefix='//')
    return xpath
