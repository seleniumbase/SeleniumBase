###############################################################################
# active_css_js - Return the Best CSS Selector of the Currently Active Element.
###############################################################################

get_active_element_css = r"""
var cssPathById = function(el) {
    if (!(el instanceof Element)) return;
    var path = [];
    while (el != null && el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.id) {
            elid = el.id;
            if (/\s/.test(elid) || elid.includes(',') || elid.includes('.') ||
                elid.includes('(') || elid.includes(':') || hasDigit(elid[0]))
                return cssPathByAttribute(el, 'id');
            selector += '#' + elid;
            path.unshift(selector);
            break;
        } else {
            var sib = el, nth = 1;
            while (sib = sib.previousElementSibling) {
                if (sib.nodeName.toLowerCase() == selector)
                    nth++;
            }
            if (nth != 1)
                selector += ':nth-of-type('+nth+')';
        }
        path.unshift(selector);
        el = el.parentNode;
    }
    return path.join(' > ');
};
var cssPathByAttribute = function(el, attr) {
    if (!(el instanceof Element)) return;
    var path = [];
    while (el !== null && el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.hasAttribute(attr) &&
            el.getAttribute(attr).length > 0 &&
            !el.getAttribute(attr).includes('\n'))
        {
            the_attr = el.getAttribute(attr);
            the_attr = the_attr.replaceAll('"', '\\"');
            the_attr = the_attr.replaceAll("'", "\\'");
            selector += '[' + attr + '="' + the_attr + '"]';
            path.unshift(selector);
            break;
        } else {
            var sib = el, nth = 1;
            while (sib = sib.previousElementSibling) {
                if (sib.nodeName.toLowerCase() == selector)
                    nth++;
            }
            if (nth != 1)
                selector += ':nth-of-type('+nth+')';
        }
        path.unshift(selector);
        el = el.parentNode;
    }
    return path.join(' > ');
};
var cssPathByClass = function(el) {
    if (!(el instanceof Element)) return;
    var path = [];
    while (el !== null && el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.hasAttribute('class') &&
            el.getAttribute('class').length > 0 &&
            !el.getAttribute('class').includes(' ') &&
                (el.getAttribute('class').includes('-')) &&
            document.querySelectorAll(
                selector + '.' + el.getAttribute('class')).length == 1) {
            selector += '.' + el.getAttribute('class');
            path.unshift(selector);
            break;
        } else {
            var sib = el, nth = 1;
            while (sib = sib.previousElementSibling) {
                if (sib.nodeName.toLowerCase() == selector) nth++;
            }
            if (nth != 1)
                selector += ':nth-of-type('+nth+')';
        }
        path.unshift(selector);
        el = el.parentNode;
    }
    return path.join(' > ');
};
var ssOccurrences = function(string, subString, allowOverlapping) {
    if (subString.length <= 0)
        return (string.length + 1);
    var n = 0;
    var pos = 0;
    var step = allowOverlapping ? 1 : subString.length;
    while (true) {
        pos = string.indexOf(subString, pos);
        if (pos >= 0) { ++n; pos += step; }
        else break;
    }
    return n;
};
function hasDigit(str) {
    return /\d/.test(str);
};
function isGen(str) {
    return /[_-]\d/.test(str);
};
function tagName(el) {
    return el.tagName.toLowerCase();
};
function turnIntoParentAsNeeded(el) {
    if (tagName(el) == 'span' || tagName(el) == 'i') {
        if (tagName(el.parentElement) == 'button') {
            el = el.parentElement;
        }
        else if (tagName(el.parentElement.parentElement) == 'button') {
            el = el.parentElement.parentElement;
        }
    }
    return el;
}
var getBestSelector = function(el) {
    if (!(el instanceof Element)) return;
    el = turnIntoParentAsNeeded(el);
    sel_by_id = cssPathById(el);
    if (!sel_by_id.includes(' > ') && !isGen(sel_by_id)) return sel_by_id;
    child_count_by_id = ssOccurrences(sel_by_id, ' > ');
    selector_by_class = cssPathByClass(el);
    tag_name = tagName(el);
    non_id_attributes = [];
    non_id_attributes.push('name');
    non_id_attributes.push('data-qa');
    non_id_attributes.push('data-tid');
    non_id_attributes.push('data-el');
    non_id_attributes.push('data-se');
    non_id_attributes.push('data-name');
    non_id_attributes.push('data-auto');
    non_id_attributes.push('data-text');
    non_id_attributes.push('data-test');
    non_id_attributes.push('data-testid');
    non_id_attributes.push('data-test-id');
    non_id_attributes.push('data-test-selector');
    non_id_attributes.push('data-nav');
    non_id_attributes.push('data-sb');
    non_id_attributes.push('data-cy');
    non_id_attributes.push('data-action');
    non_id_attributes.push('data-target');
    non_id_attributes.push('data-tooltip');
    non_id_attributes.push('alt');
    non_id_attributes.push('title');
    non_id_attributes.push('heading');
    non_id_attributes.push('translate');
    non_id_attributes.push('aria-label');
    non_id_attributes.push('aria-describedby');
    non_id_attributes.push('rel');
    non_id_attributes.push('ng-model');
    non_id_attributes.push('ng-href');
    non_id_attributes.push('href');
    non_id_attributes.push('label');
    non_id_attributes.push('data-content');
    non_id_attributes.push('data-tip');
    non_id_attributes.push('data-for');
    non_id_attributes.push('class');
    non_id_attributes.push('for');
    non_id_attributes.push('placeholder');
    non_id_attributes.push('value');
    non_id_attributes.push('ng-click');
    non_id_attributes.push('ng-if');
    non_id_attributes.push('src');
    selector_by_attr = [];
    all_by_attr = [];
    num_by_attr = [];
    child_count_by_attr = [];
    for (var i = 0; i < non_id_attributes.length; i++) {
        n_i_attr = non_id_attributes[i];
        selector_by_attr[i] = null;
        if (n_i_attr == 'class') selector_by_attr[i] = selector_by_class;
        else selector_by_attr[i] = cssPathByAttribute(el, n_i_attr);
        all_by_attr[i] = document.querySelectorAll(selector_by_attr[i]);
        num_by_attr[i] = all_by_attr[i].length;
        if (!selector_by_attr[i].includes(' > ') &&
            ((num_by_attr[i] == 1) || (el == all_by_attr[i][0])))
        {
            if (n_i_attr.startsWith('aria') || n_i_attr == 'for')
                if (hasDigit(selector_by_attr[i])) continue;
            return selector_by_attr[i];
        }
        child_count_by_attr[i] = ssOccurrences(selector_by_attr[i], ' > ');
    }
    basic_tags = [];
    basic_tags.push('h1');
    basic_tags.push('h2');
    basic_tags.push('h3');
    basic_tags.push('canvas');
    basic_tags.push('center');
    basic_tags.push('input');
    basic_tags.push('textarea');
    for (var i = 0; i < basic_tags.length; i++) {
        d_qsa = document.querySelectorAll(basic_tags[i]);
        if (tag_name == basic_tags[i] && d_qsa.length == 1 && el == d_qsa[0])
            return basic_tags[i];
    }
    contains_tags = [];
    contains_tags.push('a');
    contains_tags.push('b');
    contains_tags.push('h1');
    contains_tags.push('h2');
    contains_tags.push('h3');
    contains_tags.push('h4');
    contains_tags.push('h5');
    contains_tags.push('code');
    contains_tags.push('mark');
    contains_tags.push('button');
    contains_tags.push('label');
    contains_tags.push('legend');
    contains_tags.push('li');
    contains_tags.push('td');
    contains_tags.push('th');
    contains_tags.push('i');
    contains_tags.push('small');
    contains_tags.push('strong');
    contains_tags.push('summary');
    contains_tags.push('span');
    all_by_tag = [];
    text_content = '';
    if (el.textContent)
        text_content = el.textContent.trim();
    for (var i = 0; i < contains_tags.length; i++) {
        if (tag_name == contains_tags[i] &&
            text_content.length >= 2 && text_content.length <= 64)
        {
            t_count = 0;
            all_by_tag[i] = document.querySelectorAll(contains_tags[i]);
            for (var j = 0; j < all_by_tag[i].length; j++) {
                if (all_by_tag[i][j].textContent.includes(text_content))
                    t_count += 1;
            }
            if (t_count === 1 && !text_content.includes('\n')) {
                text_content = text_content.replaceAll("'", "\\'");
                text_content = text_content.replaceAll('"', '\\"');
                return tag_name += ':contains("'+text_content+'")';
            }
        }
    }
    best_selector = sel_by_id;
    lowest_child_count = child_count_by_id;
    child_count_by_class = ssOccurrences(selector_by_class, ' > ');
    if (child_count_by_class < lowest_child_count) {
        best_selector = selector_by_class;
        lowest_child_count = child_count_by_class;
    }
    for (var i = 0; i < non_id_attributes.length; i++) {
        if (child_count_by_attr[i] < lowest_child_count &&
            ((num_by_attr[i] == 1) || (el == all_by_attr[i][0])))
        {
            best_selector = selector_by_attr[i];
            lowest_child_count = child_count_by_attr[i];
        }
    }
    best_selector = best_selector.replaceAll('html > body', 'body');
    selector = best_selector.replaceAll(' > ', ' ');
    selector = selector.replaceAll(' div ', ' ');
    if (document.querySelector(selector) == el)
        best_selector = selector;
    return best_selector;
};
return getBestSelector(document.activeElement);
"""
