"""
Convert XPath selectors into CSS selectors
"""

import re

_sub_regexes = {
    "tag": "([a-zA-Z][a-zA-Z0-9]{0,10}|\*)",
    "attribute": "[.a-zA-Z_:][-\w:.]*(\(\))?)",
    "value": "\s*[\w/:][-/\w\s,:;.]*"
}

_validation_re = (
    "(?P<node>"
    "("
    "^id\([\"\']?(?P<idvalue>%(value)s)[\"\']?\)"
    "|"
    "(?P<nav>//?)(?P<tag>%(tag)s)"
    "(\[("
    "(?P<matched>(?P<mattr>@?%(attribute)s=[\"\']"
    "(?P<mvalue>%(value)s))[\"\']"
    "|"
    "(?P<contained>contains\((?P<cattr>@?%(attribute)s,\s*[\"\']"
    "(?P<cvalue>%(value)s)[\"\']\))"
    ")\])?"
    "(\[(?P<nth>\d)\])?"
    ")"
    ")" % _sub_regexes
)

prog = re.compile(_validation_re)


class XpathException(Exception):
    pass


def convert_xpath_to_css(xpath):
    css = ""
    position = 0

    while position < len(xpath):
        node = prog.match(xpath[position:])
        if node is None:
            raise XpathException("Invalid or unsupported Xpath: %s" % xpath)
        match = node.groupdict()

        if position != 0:
            nav = " " if match['nav'] == "//" else " > "
        else:
            nav = ""

        tag = "" if match['tag'] == "*" else match['tag'] or ""

        if match['idvalue']:
            attr = "#%s" % match['idvalue'].replace(" ", "#")
        elif match['matched']:
            if match['mattr'] == "@id":
                attr = "#%s" % match['mvalue'].replace(" ", "#")
            elif match['mattr'] == "@class":
                attr = ".%s" % match['mvalue'].replace(" ", ".")
            elif match['mattr'] in ["text()", "."]:
                attr = ":contains(^%s$)" % match['mvalue']
            elif match['mattr']:
                if match["mvalue"].find(" ") != -1:
                    match["mvalue"] = "\"%s\"" % match["mvalue"]
                attr = "[%s=%s]" % (match['mattr'].replace("@", ""),
                                    match['mvalue'])
        elif match['contained']:
            if match['cattr'].startswith("@"):
                attr = "[%s*=%s]" % (match['cattr'].replace("@", ""),
                                     match['cvalue'])
            elif match['cattr'] == "text()":
                attr = ":contains(%s)" % match['cvalue']
        else:
            attr = ""

        if match['nth']:
            nth = ":nth-of-type(%s)" % match['nth']
        else:
            nth = ""

        node_css = nav + tag + attr + nth
        css += node_css
        position += node.end()
    else:
        css = css.strip()
        return css
