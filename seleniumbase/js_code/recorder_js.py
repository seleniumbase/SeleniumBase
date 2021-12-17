###############################################################################
# recorder_js - Save browser actions to sessionStorage with good CSS selectors.
###############################################################################

recorder_js = r"""
var cssPathById = function(el) {
    if (!(el instanceof Element))
        return;
    var path = [];
    while (el != null && el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.id) {
            elid = el.id;
            if (elid.includes(',') || elid.includes('.') ||
                elid.includes('(') || elid.includes(')'))
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
    if (!(el instanceof Element))
        return;
    var path = [];
    while (el !== null && el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.hasAttribute(attr) &&
            el.getAttribute(attr).length > 0 &&
            !el.getAttribute(attr).includes('\n'))
        {
            the_attr = el.getAttribute(attr);
            if (the_attr.includes('"'))
                the_attr = the_attr.replace('"', '\\"');
            if (the_attr.includes("'"))
                the_attr = the_attr.replace("'", "\\'");
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
    if (!(el instanceof Element))
        return;
    var path = [];
    while (el !== null && el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.hasAttribute("class") &&
            el.getAttribute("class").length > 0 &&
            !el.getAttribute("class").includes(' ') &&
                (el.getAttribute("class").includes('-')) &&
            document.querySelectorAll(
                selector + '.' + el.getAttribute("class")).length == 1) {
            selector += '.' + el.getAttribute("class");
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
var ssOccurrences = function(string, subString, allowOverlapping) {
    string += '';
    subString += '';
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
function hasNumber(str) {
    return /\d/.test(str);
};
function tagName(el) {
    return el.tagName.toLowerCase();
};
function turnIntoParentAsNeeded(el) {
    if (tagName(el) == 'span') {
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
    if (!(el instanceof Element))
        return;
    el = turnIntoParentAsNeeded(el);
    child_sep = ' > ';
    selector_by_id = cssPathById(el);
    if (!selector_by_id.includes(child_sep))
        return selector_by_id;
    child_count_by_id = ssOccurrences(selector_by_id, child_sep);
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
    non_id_attributes.push('data-content');
    non_id_attributes.push('alt');
    non_id_attributes.push('title');
    non_id_attributes.push('heading');
    non_id_attributes.push('translate');
    non_id_attributes.push('aria-label');
    non_id_attributes.push('ng-model');
    non_id_attributes.push('ng-href');
    non_id_attributes.push('href');
    non_id_attributes.push('label');
    non_id_attributes.push('class');
    non_id_attributes.push('value');
    non_id_attributes.push('for');
    non_id_attributes.push('placeholder');
    non_id_attributes.push('ng-if');
    non_id_attributes.push('src');
    selector_by_attr = [];
    all_by_attr = [];
    num_by_attr = [];
    child_count_by_attr = [];
    for (var i = 0; i < non_id_attributes.length; i++) {
        n_i_attr = non_id_attributes[i];
        selector_by_attr[i] = null;
        if (n_i_attr == 'class') {
            selector_by_attr[i] = selector_by_class;
        }
        else {
            selector_by_attr[i] = cssPathByAttribute(el, n_i_attr);
        }
        all_by_attr[i] = document.querySelectorAll(selector_by_attr[i]);
        num_by_attr[i] = all_by_attr[i].length;
        if (!selector_by_attr[i].includes(child_sep) &&
            ((num_by_attr[i] == 1) || (el == all_by_attr[i][0])))
        {
            if (n_i_attr == 'aria-label' || n_i_attr == 'for')
                if (hasNumber(selector_by_attr[i]))
                    continue;
            return selector_by_attr[i];
        }
        child_count_by_attr[i] = ssOccurrences(selector_by_attr[i], child_sep);
    }
    basic_tags = [];
    basic_tags.push('h1');
    basic_tags.push('h2');
    basic_tags.push('h3');
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
    contains_tags.push('i');
    contains_tags.push('h1');
    contains_tags.push('h2');
    contains_tags.push('h3');
    contains_tags.push('h4');
    contains_tags.push('h5');
    contains_tags.push('li');
    contains_tags.push('td');
    contains_tags.push('th');
    contains_tags.push('code');
    contains_tags.push('mark');
    contains_tags.push('label');
    contains_tags.push('small');
    contains_tags.push('button');
    contains_tags.push('legend');
    contains_tags.push('strong');
    contains_tags.push('summary');
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
    best_selector = selector_by_id;
    lowest_child_count = child_count_by_id;
    child_count_by_class = ssOccurrences(selector_by_class, child_sep);
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

function new_tab_on_new_origin() {
    var AllAnchorTags = document.getElementsByTagName("a");
    for (var i = 0; i < AllAnchorTags.length; i++) {
        if (!AllAnchorTags[i].sbset) {
            AllAnchorTags[i].sbset = true;
            AllAnchorTags[i].addEventListener('click', function (event) {
                rec_mode = sessionStorage.getItem('recorder_mode');
                if (rec_mode !== '2' && rec_mode !== '3') {
                    if (this.origin &&
                        this.origin != 'null' &&
                        this.origin != document.location.origin &&
                        this.hasAttribute('href'))
                    {
                        event.preventDefault();
                        window.open(this.href, '_blank').focus();
                    }
                } else { event.preventDefault(); event.stopPropagation(); }
            },
            false);
        }
    }
};
new_tab_on_new_origin();
var AllInputTags = document.getElementsByTagName("input");
var AllButtonTags = document.getElementsByTagName("button");
var All_IB_Tags = [];
All_IB_Tags.push(...AllInputTags, ...AllButtonTags);
for (var i = 0; i < All_IB_Tags.length; i++) {
    All_IB_Tags[i].addEventListener('click', function (event) {
        rec_mode = sessionStorage.getItem('recorder_mode');
        if (rec_mode === '2' || rec_mode === '3')
        { event.preventDefault(); event.stopPropagation(); }
    },
    false);
}
var SearchInputs = document.querySelectorAll('input[type="search"]');
for (var i = 0; i < SearchInputs.length; i++) {
    SearchInputs[i].addEventListener('change', function (event) {
        new_tab_on_new_origin();
    },
    false);
}
var AwayForms = document.querySelectorAll('form[action^="//"]');
for (var i = 0; i < AwayForms.length; i++) {
    AwayForms[i].target = '_blank';
}

var reset_recorder_state = function() {
    document.recorded_actions = [];
    sessionStorage.setItem('pause_recorder', 'no');
    sessionStorage.setItem('recorder_mode', '1');
    sessionStorage.setItem('recorder_title', document.title)
    const d_now = Date.now();
    w_orig = window.location.origin;
    w_href = window.location.href;
    if (sessionStorage.getItem('recorder_activated') === 'yes') {
        ss_ra = JSON.parse(sessionStorage.getItem('recorded_actions'));
        document.recorded_actions = ss_ra;
        document.recorded_actions.push(['_url_', w_orig, w_href, d_now]);
    }
    else {
        sessionStorage.setItem('recorder_activated', 'yes');
        document.recorded_actions.push(['begin', w_orig, w_href, d_now]);
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
    return;
};
reset_recorder_state();

var reset_if_recorder_undefined = function() {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
};

document.body.addEventListener('mouseover', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const el = event.target;
    const selector = getBestSelector(el);
    if (!selector.startsWith('body') && !selector.includes(' div')) {
        document.title = selector;
    }
});
document.body.addEventListener('mouseout', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    document.title = sessionStorage.getItem('recorder_title');
});
document.body.addEventListener('click', function (event) {
    // Do Nothing.
});
document.body.addEventListener('submit', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'input' &&
        !document.recorded_actions[ra_len-1][2].endsWith('\n'))
    {
        selector = document.recorded_actions[ra_len-1][1];
        text = document.recorded_actions[ra_len-1][2] + '\n';
        document.recorded_actions.pop();
        document.recorded_actions.push(['input', selector, text, d_now]);
        json_rec_act = JSON.stringify(document.recorded_actions);
        sessionStorage.setItem('recorded_actions', json_rec_act);
    }
});
document.body.addEventListener('formdata', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'input' &&
        !document.recorded_actions[ra_len-1][2].endsWith('\n'))
    {
        selector = document.recorded_actions[ra_len-1][1];
        text = document.querySelector(selector).value + '\n';
        document.recorded_actions.pop();
        document.recorded_actions.push(['input', selector, text, d_now]);
        json_rec_act = JSON.stringify(document.recorded_actions);
        sessionStorage.setItem('recorded_actions', json_rec_act);
    }
});
document.body.addEventListener('dragstart', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    const el = event.target;
    const selector = getBestSelector(el);
    ra_len = document.recorded_actions.length;
    rec_mode = sessionStorage.getItem('recorder_mode');
    if (rec_mode === '2' || rec_mode === '3')
        return;
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn' &&
        document.recorded_actions[ra_len-1][1] === selector)
    {
        document.recorded_actions.pop();
    }
    if (el.draggable === true) {
        document.recorded_actions.push(['drags', selector, '', d_now]);
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('dragend', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'drags')
    {
        document.recorded_actions.pop();
        json_rec_act = JSON.stringify(document.recorded_actions);
        sessionStorage.setItem('recorded_actions', json_rec_act);
    }
});
document.body.addEventListener('drop', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    const el = event.target;
    const selector = getBestSelector(el);
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'drags')
    {
        drg_s = document.recorded_actions[ra_len-1][1];
        document.recorded_actions.pop();
        document.recorded_actions.push(['ddrop', drg_s, selector, d_now]);
        json_rec_act = JSON.stringify(document.recorded_actions);
        sessionStorage.setItem('recorded_actions', json_rec_act);
    }
});
document.body.addEventListener('change', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    const el = event.target;
    const selector = getBestSelector(el);
    ra_len = document.recorded_actions.length;
    tag_name = tagName(el);
    e_type = el.type;
    if (tag_name === 'select')
    {
        el_computed = document.querySelector(selector);
        optxt = el_computed.options[el_computed.selectedIndex].text;
        document.recorded_actions.push(['s_opt', selector, optxt, d_now]);
    }
    else if (tag_name === 'input' && e_type === 'range')
    {
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
        {
            document.recorded_actions.pop();
            ra_len = document.recorded_actions.length;
        }
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
        {
            document.recorded_actions.pop();
            ra_len = document.recorded_actions.length;
        }
        value = el.value;
        document.recorded_actions.push(['set_v', selector, value, d_now]);
    }
    else if (tag_name === 'input' && e_type === 'file') {
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
        {
            document.recorded_actions.pop();
            ra_len = document.recorded_actions.length;
        }
        value = el.value;
        document.recorded_actions.push(['cho_f', selector, value, d_now]);
    }
    else if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][1] === selector &&
        tag_name === 'input' && e_type === 'checkbox')
    {
        document.recorded_actions.pop();
        ra_len = document.recorded_actions.length;
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
            document.recorded_actions.pop();
    }
    if (tag_name === 'input' && e_type === 'checkbox' && el.checked)
        document.recorded_actions.push(['c_box', selector, 'yes', d_now]);
    else if (tag_name === 'input' && e_type === 'checkbox' && !el.checked)
        document.recorded_actions.push(['c_box', selector, 'no', d_now]);
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('mousedown', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    el = event.target;
    const selector = getBestSelector(el);
    ra_len = document.recorded_actions.length;
    rec_mode = sessionStorage.getItem('recorder_mode');
    tag_name = tagName(el);
    if (rec_mode === '2' || rec_mode === '3')
    {
        el = turnIntoParentAsNeeded(el);
        texts = [el.innerText, el.textContent];
        text = texts[0];
        t_con = texts[1];
        origin = window.location.origin;
        sel_has_contains = selector.includes(':contains(');
        if (!text) { text = ''; }
        if (rec_mode === '2' || (
            rec_mode === '3' && sel_has_contains && text === t_con))
        {
            document.recorded_actions.push(['as_el', selector, origin, d_now]);
            json_rec_act = JSON.stringify(document.recorded_actions);
            sessionStorage.setItem('recorded_actions', json_rec_act);
            return;
        }
        else if (rec_mode === '3') {
            action = 'as_et';
            text = text.trim();
            var match = /\r|\n/.exec(text);
            if (match) {
                lines = text.split(/\r\n|\r|\n/g);
                text = '';
                for (var i = 0; i < lines.length; i++) {
                    if (lines[i].length > 0) {
                        action = 'as_te'; text = lines[i]; break;
                    }
                }
            }
            tex_sel = [text, selector];
            document.recorded_actions.push([action, tex_sel, origin, d_now]);
            json_rec_act = JSON.stringify(document.recorded_actions);
            sessionStorage.setItem('recorded_actions', json_rec_act);
            return;
        }
    }
    if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'mo_dn')
        document.recorded_actions.pop();
    if (tag_name === 'select') {
        // Do Nothing. ('change' action.)
    }
    else
        document.recorded_actions.push(['mo_dn', selector, '', d_now]);
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('mouseup', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    const el = event.target;
    selector = getBestSelector(el);
    ra_len = document.recorded_actions.length;
    tag_name = tagName(el);
    parent_el = el.parentElement;
    parent_tag_name = tagName(parent_el);
    grand_el = "";
    grand_tag_name = "";
    origin = "";
    rec_mode = sessionStorage.getItem('recorder_mode');
    if (rec_mode === '2' || rec_mode === '3')
        return;
    if (parent_el.parentElement != null) {
        grand_el = parent_el.parentElement;
        grand_tag_name = tagName(grand_el);
    }
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][1] === selector &&
        (document.recorded_actions[ra_len-1][0] === 'mo_dn' ||
         tag_name === 'a' || parent_tag_name === 'a') &&
        tag_name !== 'select')
    {
        href = '';
        if (tag_name === 'a' &&
            el.hasAttribute('href') &&
            el.getAttribute('href').length > 0 &&
            el.origin != 'null')
        {
            href = el.href;
            origin = el.origin;
        }
        else if (parent_tag_name === 'a' &&
            parent_el.hasAttribute('href') &&
            parent_el.getAttribute('href').length > 0 &&
            parent_el.origin != 'null')
        {
            href = parent_el.href;
            origin = parent_el.origin;
        }
        else if (grand_tag_name === 'a' &&
            grand_el.hasAttribute('href') &&
            grand_el.getAttribute('href').length > 0 &&
            grand_el.origin != 'null')
        {
            href = grand_el.href;
            origin = grand_el.origin;
        }
        document.recorded_actions.pop();
        child_sep = ' > ';
        child_count = ssOccurrences(selector, child_sep);
        if ((tag_name === "a" && !el.hasAttribute('onclick') &&
             child_count > 0 && href.length > 0) ||
            (parent_tag_name === "a" && href.length > 0 &&
             child_count > 1 && !parent_el.hasAttribute('onclick')) ||
            (grand_tag_name === "a" && href.length > 0 &&
             child_count > 2 && !grand_el.hasAttribute('onclick')))
        {
            w_orig = window.location.origin;
            if (origin === w_orig)
                document.recorded_actions.push(['_url_', origin, href, d_now]);
            else
                document.recorded_actions.push(['begin', origin, href, d_now]);
        }
        else
            document.recorded_actions.push(['click', selector, href, d_now]);
        // hover_click() if dropdown.
        if (el.parentElement.classList.contains('dropdown-content') &&
            el.parentElement.parentElement.classList.contains('dropdown'))
        {
            ch_s = selector;
            pa_el = el.parentElement.parentElement;
            pa_s = getBestSelector(pa_el);
            if (pa_el.childElementCount >= 2 &&
               !pa_el.firstElementChild.classList.contains('dropdown-content'))
            {
                pa_el = pa_el.firstElementChild;
                pa_s = getBestSelector(pa_el);
            }
            document.recorded_actions.pop();
            document.recorded_actions.push(['h_clk', pa_s, ch_s, d_now]);
        }
    }
    else if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn' &&
        document.recorded_actions[ra_len-1][1] === selector &&
        tag_name === 'select')
    {
        document.recorded_actions.pop();
    }
    else if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn')
    {
        // Maybe accidental drag & drop.
        document.recorded_actions.pop();
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('contextmenu', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const el = event.target;
    const selector = getBestSelector(el);
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn' &&
        document.recorded_actions[ra_len-1][1] === selector)
    {
        document.recorded_actions.pop();
        json_rec_act = JSON.stringify(document.recorded_actions);
        sessionStorage.setItem('recorded_actions', json_rec_act);
    }
});
document.body.addEventListener('keydown', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn' &&
        document.recorded_actions[ra_len-1][1] === selector)
    {
        document.recorded_actions.pop();
        json_rec_act = JSON.stringify(document.recorded_actions);
        sessionStorage.setItem('recorded_actions', json_rec_act);
    }
});
document.body.addEventListener('keyup', function (event) {
    reset_if_recorder_undefined();
    // Controls to pause & resume.
    pause_rec = sessionStorage.getItem('pause_recorder');
    rec_mode = sessionStorage.getItem('recorder_mode');
    l_key = event.key.toLowerCase();
    if (l_key === 'escape' && pause_rec === 'no' && rec_mode === '1') {
        sessionStorage.setItem('pause_recorder', 'yes');
        pause_rec = 'yes';
        console.log('SeleniumBase Recorder paused');
        no_border = 'none';
        document.querySelector('body').style.border = no_border;
        document.title = sessionStorage.getItem('recorder_title');
    }
    else if ((event.key === '`' || event.key === '~') && pause_rec === 'yes') {
        sessionStorage.setItem('pause_recorder', 'no');
        pause_rec = 'no';
        console.log('SeleniumBase Recorder resumed');
        red_border = 'thick solid #EE3344';
        document.querySelector('body').style.border = red_border;
    }
    else if (event.key === '^' && pause_rec === 'no') {
        sessionStorage.setItem('recorder_mode', '2');
        purple_border = 'thick solid #EF5BE9';
        document.querySelector('body').style.border = purple_border;
    }
    else if (event.key === '&' && pause_rec === 'no') {
        sessionStorage.setItem('recorder_mode', '3');
        teal_border = 'thick solid #30C6C6';
        document.querySelector('body').style.border = teal_border;
    }
    else if (pause_rec === 'no' && l_key !== 'shift' && l_key !== 'backspace')
    {
        sessionStorage.setItem('recorder_mode', '1');
        red_border = 'thick solid #EE3344';
        document.querySelector('body').style.border = red_border;
    }
    // After controls for switching modes.
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    const el = event.target;
    const selector = getBestSelector(el);
    skip_input = false;
    if ((tagName(el) === 'input' &&
        el.type !== 'checkbox' && el.type !== 'range') ||
        tagName(el) === 'textarea')
    {
        ra_len = document.recorded_actions.length;
        if (ra_len > 0 && l_key === 'enter' &&
            document.recorded_actions[ra_len-1][0] === 'input' &&
            document.recorded_actions[ra_len-1][1] === selector &&
            !document.recorded_actions[ra_len-1][2].endsWith('\n'))
        {
            s_text = document.recorded_actions[ra_len-1][2] + '\n';
            document.recorded_actions.pop();
            document.recorded_actions.push(['input', selector, s_text, d_now]);
            document.recorded_actions.push(['submi', selector, s_text, d_now]);
            skip_input = true;
        }
        else if (ra_len > 0 &&
            document.recorded_actions[ra_len-1][0] === 'click' &&
            document.recorded_actions[ra_len-1][1] === selector)
        {
            document.recorded_actions.pop();
        }
        else if (ra_len > 0 &&
            document.recorded_actions[ra_len-1][0] === 'input' &&
            document.recorded_actions[ra_len-1][1] === selector &&
            !document.recorded_actions[ra_len-1][2].endsWith('\n'))
        {
            document.recorded_actions.pop();
        }
        else if (ra_len > 0 &&
            document.recorded_actions[ra_len-1][0] === 'input' &&
            document.recorded_actions[ra_len-1][1] === selector &&
            document.recorded_actions[ra_len-1][2].endsWith('\n'))
        {
            skip_input = true;
        }
        if (!skip_input) {
            document.recorded_actions.push(
                ['input', selector, el.value, d_now]);
        }
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
var r_border_style = 'thick solid #EE3344';
document.querySelector('body').style.border = r_border_style;
"""
