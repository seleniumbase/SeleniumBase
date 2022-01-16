"""
Convert XPath selectors into CSS selectors
"""
import re

_sub_regexes = {
    "tag": r"([a-zA-Z][a-zA-Z0-9]{0,10}|\*)",
    "attribute": r"[.a-zA-Z_:][-\w:.]*(\(\))?)",
    "value": r"\s*[\w/:][-/\w\s,:;.\S]*",
}

_validation_re = (
    r"(?P<node>"
    r"("
    r"^id\([\"\']?(?P<idvalue>%(value)s)[\"\']?\)"
    r"|"
    r"(?P<nav>//?)(?P<tag>%(tag)s)"
    r"(\[("
    r"(?P<matched>(?P<mattr>@?%(attribute)s=[\"\']"
    r"(?P<mvalue>%(value)s))[\"\']"
    r"|"
    r"(?P<contained>contains\((?P<cattr>@?%(attribute)s,\s*[\"\']"
    r"(?P<cvalue>%(value)s)[\"\']\))"
    r")\])?"
    r"(\[(?P<nth>\d+)\])?"
    r")"
    r")" % _sub_regexes
)

prog = re.compile(_validation_re)


class XpathException(Exception):
    pass


def _handle_brackets_in_strings(xpath):
    # Edge Case: Brackets in strings.
    # Example from GitHub.com -
    # '<input type="text" id="user[login]">' => '//*[@id="user[login]"]'
    # Need to tell apart string-brackets from regular brackets
    new_xpath = ""
    chunks = xpath.split('"')
    len_chunks = len(chunks)
    for chunk_num in range(len_chunks):
        if chunk_num % 2 != 0:
            chunks[chunk_num] = chunks[chunk_num].replace(
                "[", "_STR_L_bracket_"
            )
            chunks[chunk_num] = chunks[chunk_num].replace(
                "]", "_STR_R_bracket_"
            )
        new_xpath += chunks[chunk_num]
        if chunk_num != len_chunks - 1:
            new_xpath += '"'
    return new_xpath


def _filter_xpath_grouping(xpath):
    """
    This method removes the outer parentheses for xpath grouping.
    The xpath converter will break otherwise.
    Example:
    "(//button[@type='submit'])[1]" becomes "//button[@type='submit'][1]"
    """

    # First remove the first open parentheses
    xpath = xpath[1:]

    # Next remove the last closed parentheses
    index = xpath.rfind(")")
    index_p1 = index + 1  # Make "flake8" and "black" agree
    if index == -1:
        raise XpathException("Invalid or unsupported Xpath: %s" % xpath)
    xpath = xpath[:index] + xpath[index_p1:]
    return xpath


def _get_raw_css_from_xpath(xpath):
    css = ""
    attr = ""
    position = 0

    while position < len(xpath):
        node = prog.match(xpath[position:])
        if node is None:
            raise XpathException("Invalid or unsupported Xpath: %s" % xpath)
        match = node.groupdict()

        if position != 0:
            nav = " " if match["nav"] == "//" else " > "
        else:
            nav = ""

        tag = "" if match["tag"] == "*" else match["tag"] or ""

        if match["idvalue"]:
            attr = "#%s" % match["idvalue"].replace(" ", "#")
        elif match["matched"]:
            if match["mattr"] == "@id":
                attr = "#%s" % match["mvalue"].replace(" ", "#")
            elif match["mattr"] == "@class":
                attr = ".%s" % match["mvalue"].replace(" ", ".")
            elif match["mattr"] in ["text()", "."]:
                attr = ":contains('%s')" % match["mvalue"]
            elif match["mattr"]:
                attr = '[%s="%s"]' % (
                    match["mattr"].replace("@", ""),
                    match["mvalue"],
                )
        elif match["contained"]:
            if match["cattr"].startswith("@"):
                attr = '[%s*="%s"]' % (
                    match["cattr"].replace("@", ""),
                    match["cvalue"],
                )
            elif match["cattr"] == "text()":
                attr = ':contains("%s")' % match["cvalue"]
            elif match["cattr"] == ".":
                attr = ':contains("%s")' % match["cvalue"]
        else:
            attr = ""

        if match["nth"]:
            nth = ":nth-of-type(%s)" % match["nth"]
        else:
            nth = ""

        node_css = nav + tag + attr + nth
        css += node_css
        position += node.end()
    else:
        css = css.strip()
        return css


def convert_xpath_to_css(xpath):
    xpath = xpath.replace(" = '", "='")

    # **** Start of handling special xpath edge cases instantly ****

    # Handle a special edge case that converts to: 'tag.class:contains("TEXT")'
    c3 = "@class and contains(concat(' ', normalize-space(@class), ' '), ' "
    if c3 in xpath and xpath.count(c3) == 1 and xpath.count("[@") == 1:
        p2 = " ') and (contains(., '"
        if (
            xpath.count(p2) == 1
            and xpath.endswith("'))]")
            and xpath.count("//") == 1
            and xpath.count(" ') and (") == 1
        ):
            s_contains = xpath.split(p2)[1].split("'))]")[0]
            s_tag = xpath.split("//")[1].split("[@class")[0]
            s_class = xpath.split(c3)[1].split(" ') and (")[0]
            return '%s.%s:contains("%s")' % (s_tag, s_class, s_contains)

    # Find instance of: //tag[@attribute='value' and (contains(., 'TEXT'))]
    data = re.match(
        r"""^\s*//(\S+)\[@(\S+)='(\S+)'\s+and\s+"""
        r"""\(contains\(\.,\s'(\S+)'\)\)\]""",
        xpath,
    )
    if data:
        s_tag = data.group(1)
        s_atr = data.group(2)
        s_val = data.group(3)
        s_contains = data.group(4)
        return '%s[%s="%s"]:contains("%s")' % (s_tag, s_atr, s_val, s_contains)

    # Find instance of: //tag[@attribute1='value1' and (@attribute2='value2')]
    data = re.match(
        r"""^\s*//(\S+)\[@(\S+)='(\S+)'\s+and\s+"""
        r"""\(@(\S+)='(\S+)'\)\]""",
        xpath,
    )
    if data:
        s_tag = data.group(1)
        s_atr1 = data.group(2)
        s_val1 = data.group(3)
        s_atr2 = data.group(4)
        s_val2 = data.group(5)
        return '%s[%s="%s"][%s="%s"]' % (s_tag, s_atr1, s_val1, s_atr2, s_val2)

    # **** End of handling special xpath edge cases instantly ****

    if xpath[0] != '"' and xpath[-1] != '"' and xpath.count('"') % 2 == 0:
        xpath = _handle_brackets_in_strings(xpath)
    xpath = xpath.replace("descendant-or-self::*/", "descORself/")
    if len(xpath) > 3:
        xpath = xpath[0:3] + xpath[3:].replace("//", "/descORself/")

    if " and contains(@" in xpath and xpath.count(" and contains(@") == 1:
        spot1 = xpath.find(" and contains(@")
        spot1 = spot1 + len(" and contains(@")
        spot2 = xpath.find(",", spot1)
        attr = xpath[spot1:spot2]
        swap = " and contains(@%s, " % attr
        if swap in xpath:
            swap_spot = xpath.find(swap)
            close_paren = xpath.find("]", swap_spot) - 1
            close_paren_p1 = close_paren + 1  # Make "flake8" and "black" agree
            if close_paren > 1:
                xpath = xpath[:close_paren] + xpath[close_paren_p1:]
                xpath = xpath.replace(swap, "_STAR_=")

    if xpath.startswith("("):
        xpath = _filter_xpath_grouping(xpath)

    css = ""
    if "/descORself/" in xpath and ("@id" in xpath or "@class" in xpath):
        css_sections = []
        xpath_sections = xpath.split("/descORself/")
        for xpath_section in xpath_sections:
            if not xpath_section.startswith("//"):
                xpath_section = "//" + xpath_section
            css_sections.append(_get_raw_css_from_xpath(xpath_section))
        css = "/descORself/".join(css_sections)
    else:
        css = _get_raw_css_from_xpath(xpath)

    attribute_defs = re.findall(r"(\[\w+\=\S+\])", css)
    for attr_def in attribute_defs:
        if (
            attr_def.count("[") == 1
            and attr_def.count("]") == 1
            and attr_def.count("=") == 1
            and attr_def.count('"') == 0
            and attr_def.count("'") == 0
            and attr_def.count(" ") == 0
        ):
            # Now safe to manipulate
            q1 = attr_def.find("=") + 1
            q2 = attr_def.find("]")
            new_attr_def = attr_def[:q1] + "'" + attr_def[q1:q2] + "']"
            css = css.replace(attr_def, new_attr_def)

    # Replace the string-brackets with escaped ones
    css = css.replace("_STR_L_bracket_", "\\[")
    css = css.replace("_STR_R_bracket_", "\\]")

    # Handle a lot of edge cases with conversion
    css = css.replace(" > descORself > ", " ")
    css = css.replace(" descORself > ", " ")
    css = css.replace("/descORself/*", " ")
    css = css.replace("/descORself/", " ")
    css = css.replace("descORself > ", "")
    css = css.replace("descORself/", " ")
    css = css.replace("descORself", " ")
    css = css.replace("_STAR_=", "*=")
    css = css.replace("]/", "] ")
    css = css.replace("] *[", "] > [")
    css = css.replace("'", '"')
    css = css.replace("[@", "[")

    return css
