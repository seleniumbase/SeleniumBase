"""
Convert CSS selectors into XPath selectors
"""
from cssselect.xpath import GenericTranslator


class ConvertibleToCssTranslator(GenericTranslator):
    """An implementation of :py:class:`cssselect.GenericTranslator` with
    XPath output that more readily converts back to CSS selectors.
    The simplified examples in https://devhints.io/xpath were used as a
    reference here.
    """
    def css_to_xpath(self, css, prefix='//'):
        return super(ConvertibleToCssTranslator, self).css_to_xpath(css,
                                                                    prefix)

    def xpath_attrib_equals(self, xpath, name, value):
        xpath.add_condition('%s=%s' % (name, self.xpath_literal(value)))
        return xpath

    def xpath_attrib_includes(self, xpath, name, value):
        from cssselect.xpath import is_non_whitespace
        if is_non_whitespace(value):
            xpath.add_condition(
                "contains(%s, %s)"
                % (name, self.xpath_literal(value)))
        else:
            xpath.add_condition('0')
        return xpath

    def xpath_attrib_substringmatch(self, xpath, name, value):
        if value:
            # Attribute selectors are case sensitive
            xpath.add_condition('contains(%s, %s)' % (
                name, self.xpath_literal(value)))
        else:
            xpath.add_condition('0')
        return xpath

    def xpath_class(self, class_selector):
        xpath = self.xpath(class_selector.selector)
        return self.xpath_attrib_includes(
            xpath, '@class', class_selector.class_name)

    def xpath_descendant_combinator(self, left, right):
        """right is a child, grand-child or further descendant of left"""
        return left.join('//', right)


def convert_css_to_xpath(css):
    """ Convert CSS Selectors to XPath Selectors.
        Example:
            convert_css_to_xpath('button:contains("Next")')
            Output => "//button[contains(., 'Next')]"
    """
    xpath = ConvertibleToCssTranslator().css_to_xpath(css)
    return xpath
