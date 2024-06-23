###############################################################################
# recorder_js - Save browser actions to sessionStorage with good CSS selectors.
###############################################################################

recorder_js = r"""
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
    return /[_-]\d/.test(str) || /\d[a-z]/.test(str);
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

function useHref(tag_name, el) {
    return (tag_name === 'a' && el.hasAttribute('href') &&
            el.getAttribute('href').length > 0 && el.origin != 'null');
};
function saveRecordedActions() {
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
};
function new_tab_on_new_origin() {
    var AllAnchorTags = document.getElementsByTagName('a');
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
            }, false);
        }
    }
};
new_tab_on_new_origin();
var AllInputTags = document.getElementsByTagName('input');
var AllButtonTags = document.getElementsByTagName('button');
var All_IB_Tags = [];
All_IB_Tags.push(...AllInputTags, ...AllButtonTags);
for (var i = 0; i < All_IB_Tags.length; i++) {
    All_IB_Tags[i].addEventListener('click', function (event) {
        rec_mode = sessionStorage.getItem('recorder_mode');
        if (rec_mode === '2' || rec_mode === '3')
        { event.preventDefault(); event.stopPropagation(); }
    }, false);
}
var SearchInputs = document.querySelectorAll('input[type="search"]');
for (var i = 0; i < SearchInputs.length; i++) {
    SearchInputs[i].addEventListener('change', function (event) {
        new_tab_on_new_origin();
    }, false);
}
var AwayForms = document.querySelectorAll('form[action^="//"]');
for (var i = 0; i < AwayForms.length; i++) {
    AwayForms[i].target = '_blank';
}
var reset_recorder_state = function() {
    document.recorded_actions = [];
    sessionStorage.setItem('pause_recorder', 'no');
    sessionStorage.setItem('recorder_mode', '1');
    sessionStorage.setItem('recorder_title', document.title);
    const d_now = Date.now();
    document.recorder_last_mouseup = d_now;
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
    saveRecordedActions();
    return;
};
reset_recorder_state();
var reset_if_recorder_undefined = function() {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
};
var set_border = function(color) {
    document.querySelector('body').style.border = '5px solid ' + color;
    document.querySelector('body').style.borderRadius = '10px';
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
window.addEventListener('blur', () => {
    setTimeout(() => {
    reset_if_recorder_undefined();
    rec_mode = sessionStorage.getItem('recorder_mode');
    if (rec_mode === '2' || rec_mode === '3') return;
    const el = document.activeElement;
    const d_now = Date.now();
    const d_now2 = d_now + 1;
    const doc_t = document.title;
    skip_open = false;
    if (tagName(el) === 'iframe' &&
        doc_t.startsWith('iframe') &&
        Date.now() - document.recorder_last_mouseup > 32)
    {
        const selector = getBestSelector(el);
        const el_cw = el.contentWindow;
        origin = window.location.origin;
        if (el.hasAttribute('src') && el.getAttribute('src').length > 0) {
            if (el.src.startsWith('data:')) return;
            skip_open = true; window.open(el.src, "_blank");
        }
        else document.body.innerHTML = el_cw.document.body.innerHTML;
        window.focus();
        document.recorded_actions.push(['sw_fr', selector, origin, d_now]);
        if (skip_open)
            document.recorded_actions.push(['sk_fo', '', origin, d_now2]);
        saveRecordedActions();
    }
    });
}, { once: false });
document.body.addEventListener('click', function (event) {
    // do nothing
});
document.body.addEventListener('dblclick', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    document.recorded_actions.push(['dbclk', '', '', Date.now()+1]);
    saveRecordedActions();
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
        saveRecordedActions();
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
        saveRecordedActions();
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
    if (rec_mode === '2' || rec_mode === '3') return;
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn' &&
        document.recorded_actions[ra_len-1][1] === selector)
    {
        document.recorded_actions.pop();
    }
    if (el.draggable === true) {
        document.recorded_actions.push(['drags', selector, '', d_now]);
    }
    saveRecordedActions();
});
document.body.addEventListener('dragend', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'drags')
    {
        document.recorded_actions.pop();
        saveRecordedActions();
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
        saveRecordedActions();
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
    saveRecordedActions();
});
document.body.addEventListener('mousedown', function (event) {
    reset_if_recorder_undefined();
    new_tab_on_new_origin();
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
        text = el.innerText;
        t_con = el.textContent;
        origin = window.location.origin;
        sel_has_contains = selector.includes(':contains(');
        if (!text) { text = ''; }
        text = text.trim();
        if (el.tagName.toLowerCase() == "input")
            text = el.value.trim();
        if (!t_con) { t_con = ''; }
        if (rec_mode === '2' || (
            rec_mode === '3' && sel_has_contains && text === t_con.trim()))
        {
            document.recorded_actions.push(['as_el', selector, origin, d_now]);
            saveRecordedActions();
            return;
        }
        else if (rec_mode === '3') {
            action = 'as_et';
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
            saveRecordedActions();
            return;
        }
    }
    if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'mo_dn')
        document.recorded_actions.pop();
    if (tag_name === 'select') {
        // do nothing ('change' action)
    }
    else
        document.recorded_actions.push(['mo_dn', selector, '', d_now]);
    saveRecordedActions();
});
document.body.addEventListener('mouseup', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    document.recorder_last_mouseup = d_now;
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
    if (rec_mode === '2' || rec_mode === '3') return;
    if (parent_el.parentElement != null) {
        grand_el = parent_el.parentElement; grand_tag_name = tagName(grand_el);
    }
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][1] === selector &&
        (document.recorded_actions[ra_len-1][0] === 'mo_dn' ||
         tag_name === 'a' || parent_tag_name === 'a') && tag_name !== 'select')
    {
        href = '';
        if (useHref(tag_name, el))
        {
            href = el.href; origin = el.origin;
        }
        else if (useHref(parent_tag_name, parent_el))
        {
            href = parent_el.href; origin = parent_el.origin;
        }
        else if (useHref(grand_tag_name, grand_el))
        {
            href = grand_el.href; origin = grand_el.origin;
        }
        document.recorded_actions.pop();
        child_count = ssOccurrences(selector, ' > ');
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
        // hover+click
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
        else if (tag_name === 'canvas')
        {
            rect = el.getBoundingClientRect();
            p_x = event.clientX - rect.left;
            p_y = event.clientY - rect.top;
            c_offset = [selector, p_x, p_y];
            document.recorded_actions.pop();
            document.recorded_actions.push(['canva', c_offset, href, d_now]);
        }
    }
    else if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn' &&
        document.recorded_actions[ra_len-1][1] === selector &&
        tag_name === 'select')
    { document.recorded_actions.pop(); }
    else if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn')
    {
        // accidental drag&drop
        document.recorded_actions.pop();
    }
    saveRecordedActions();
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
        saveRecordedActions();
    }
});
document.body.addEventListener('keydown', function (event) {
    reset_if_recorder_undefined();
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    if (document.recorded_actions.length == 0) return;
    const el = event.target;
    const selector = getBestSelector(el);
    const d_now = Date.now();
    const tag_name = tagName(el);
    const l_key = event.key.toLowerCase();
    if (l_key === 'enter' && (tag_name === 'button' || tag_name === 'a'))
    {
        href = '';
        if (useHref(tag_name, el))
            href = el.href;
        document.recorded_actions.push(['click', selector, href, d_now]);
        saveRecordedActions();
    }
});
document.body.addEventListener('keyup', function (event) {
    reset_if_recorder_undefined();
    // pause+resume controls
    pause_rec = sessionStorage.getItem('pause_recorder');
    rec_mode = sessionStorage.getItem('recorder_mode');
    l_key = event.key.toLowerCase();
    no_border = 'none';
    if (l_key === 'escape' && pause_rec === 'no' && rec_mode === '1') {
        sessionStorage.setItem('pause_recorder', 'yes');
        pause_rec = 'yes';
        console.log('SeleniumBase Recorder paused');
        document.querySelector('body').style.border = no_border;
        document.title = sessionStorage.getItem('recorder_title');
    }
    else if ((event.key === '`' || event.key === '~') && pause_rec === 'yes') {
        sessionStorage.setItem('pause_recorder', 'no');
        pause_rec = 'no';
        console.log('SeleniumBase Recorder resumed');
        set_border('#F43344');
    }
    else if (event.key === '^' && pause_rec === 'no') {
        sessionStorage.setItem('recorder_mode', '2');
        set_border('#EF5BE9');
    }
    else if (event.key === '&' && pause_rec === 'no') {
        sessionStorage.setItem('recorder_mode', '3');
        set_border('#30C6C6');
    }
    else if (pause_rec === 'no' && l_key !== 'shift' && l_key !== 'backspace')
    {
        sessionStorage.setItem('recorder_mode', '1');
        set_border('#F43344');
    }
    // after switching modes
    if (sessionStorage.getItem('pause_recorder') === 'yes') return;
    const d_now = Date.now();
    const el = event.target;
    const selector = getBestSelector(el);
    skip_input = false;
    if ((tagName(el) === 'input' &&
        el.type !== 'checkbox' &&
        el.type !== 'range') ||
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
            !document.recorded_actions[ra_len-1][2].endsWith('\n') &&
            l_key !== 'tab')
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
        if (!skip_input && !el.hasAttribute('readonly') && l_key !== 'tab') {
            document.recorded_actions.push(
                ['input', selector, el.value, d_now]);
        }
    }
    saveRecordedActions();
});
set_border('#F43344');
"""
