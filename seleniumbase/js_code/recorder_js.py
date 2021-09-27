###############################################################################
# recorder_js - Save browser actions to sessionStorage with good CSS selectors.
###############################################################################

recorder_js = r"""
var cssPathById = function(el) {
    if (!(el instanceof Element))
        return;
    var path = [];
    while (el !== null && el.nodeType === Node.ELEMENT_NODE) {
        var selector = el.nodeName.toLowerCase();
        if (el.id) {
            selector += '#' + el.id;
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
            el.getAttribute(attr).length > 0) {
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
        if (pos >= 0) {
            ++n;
            pos += step;
        }
        else break;
    }
    return n;
};
var getBestSelector = function(el) {
    if (!(el instanceof Element))
        return;
    child_sep = ' > ';
    selector_by_id = cssPathById(el);
    if (selector_by_id.includes('.') ||
        selector_by_id.includes('(') || selector_by_id.includes(')'))
    {
        selector_by_id = cssPathByAttribute(el, 'id');
    }
    if (!selector_by_id.includes(child_sep))
        return selector_by_id;
    child_count_by_id = ssOccurrences(selector_by_id, child_sep);
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
    non_id_attributes.push('data-test-id');
    non_id_attributes.push('data-test-selector');
    non_id_attributes.push('data-nav');
    non_id_attributes.push('data-action');
    non_id_attributes.push('data-target');
    non_id_attributes.push('alt');
    non_id_attributes.push('title');
    non_id_attributes.push('heading');
    non_id_attributes.push('translate');
    non_id_attributes.push('aria-label');
    non_id_attributes.push('ng-href');
    non_id_attributes.push('href');
    non_id_attributes.push('label');
    non_id_attributes.push('value');
    non_id_attributes.push('ng-model');
    non_id_attributes.push('ng-if');
    selector_by_attr = [];
    all_by_attr = [];
    num_by_attr = [];
    child_count_by_attr = [];
    for (var i = 0; i < non_id_attributes.length; i++) {
        selector_by_attr[i] = cssPathByAttribute(el, non_id_attributes[i]);
        all_by_attr[i] = document.querySelectorAll(selector_by_attr[i]);
        num_by_attr[i] = all_by_attr[i].length;
        if (!selector_by_attr[i].includes(child_sep) &&
            ((num_by_attr[i] == 1) || (el == all_by_attr[i][0])))
        {
            return selector_by_attr[i];
        }
        child_count_by_attr[i] = ssOccurrences(selector_by_attr[i], child_sep);
    }
    tag_name = el.tagName.toLowerCase();
    basic_tags = [];
    basic_tags.push('h1');
    basic_tags.push('input');
    basic_tags.push('textarea');
    for (var i = 0; i < basic_tags.length; i++) {
        if (tag_name == basic_tags[i] &&
            el == document.querySelector(basic_tags[i]))
        {
            return basic_tags[i];
        }
    }
    contains_tags = [];
    contains_tags.push('a');
    contains_tags.push('b');
    contains_tags.push('i');
    contains_tags.push('h1');
    contains_tags.push('h2');
    contains_tags.push('h3');
    contains_tags.push('h4');
    contains_tags.push('td');
    contains_tags.push('code');
    contains_tags.push('button');
    contains_tags.push('strong');
    all_by_tag = [];
    inner_text = el.innerText.trim();
    for (var i = 0; i < contains_tags.length; i++) {
        if (tag_name == contains_tags[i] &&
            inner_text.length >= 2 && inner_text.length <= 64)
        {
            t_count = 0;
            all_by_tag[i] = document.querySelectorAll(contains_tags[i]);
            for (var j = 0; j < all_by_tag[i].length; j++) {
                if (all_by_tag[i][j].innerText.includes(inner_text))
                    t_count += 1;
            }
            if (t_count === 1 && !inner_text.includes('\n')) {
                inner_text = inner_text.replace("'", "\\'");
                inner_text = inner_text.replace('"', '\\"');
                return tag_name += ':contains("'+inner_text+'")';
            }
        }
    }
    if (tag_name == "span" && inner_text.length > 1 && inner_text.length <= 64)
    {
        parent_element = el.parentElement;
        parent_tag_name = parent_element.tagName.toLowerCase();
        grand_element = parent_element.parentElement;
        grand_tag_name = grand_element.tagName.toLowerCase();
        if (parent_tag_name == "button" || grand_tag_name == "button") {
            qsa_element = "span";
            if (parent_tag_name == "button")
                qsa_element = "button > span";
            else { qsa_element = "button > "+parent_tag_name+" > span" }
            t_count = 0;
            all_el_found = document.querySelectorAll(qsa_element);
            for (var j = 0; j < all_el_found.length; j++) {
                if (all_el_found[j].innerText.includes(inner_text))
                    t_count += 1;
            }
            if (t_count === 1 && !inner_text.includes('\n')) {
                inner_text = inner_text.replace("'", "\\'");
                inner_text = inner_text.replace('"', '\\"');
                return qsa_element += ':contains("'+inner_text+'")';
            }
        }
    }
    best_selector = selector_by_id;
    lowest_child_count = child_count_by_id;
    for (var i = 0; i < non_id_attributes.length; i++) {
        if (child_count_by_attr[i] < lowest_child_count &&
            ((num_by_attr[i] == 1) || (el == all_by_attr[i][0])))
        {
            best_selector = selector_by_attr[i];
            lowest_child_count = child_count_by_attr[i];
        }
    }
    return best_selector;
};

var AllTheAnchorTags = document.getElementsByTagName("a");
for (var i = 0; i < AllTheAnchorTags.length; i++) {
    AllTheAnchorTags[i].addEventListener('click', function (event) {
        if (this.origin &&
            this.origin != 'null' &&
            this.origin != document.location.origin)
        {
            if (this.hasAttribute('href')) {
                event.preventDefault();
                window.open(this.href, '_blank').focus();
            }
        }
    },
    false);
}

var reset_recorder_state = function() {
    document.recorded_actions = [];
    sessionStorage.setItem('pause_recorder', 'no');
    const d_now = Date.now();
    if (sessionStorage.getItem('recorder_activated') === 'yes') {
        ss_ra = JSON.parse(sessionStorage.getItem('recorded_actions'));
        document.recorded_actions = ss_ra;
        w_orig = window.location.origin;
        w_href = window.location.href;
        ra_len = document.recorded_actions.length;
        if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'begin') {
            document.recorded_actions.pop();
            document.recorded_actions.push(['begin', w_orig, w_href, d_now]);
        }
        else if (ra_len > 0 &&
                 document.recorded_actions[ra_len-1][0] === '_url_')
        {
            document.recorded_actions.pop();
            document.recorded_actions.push(['_url_', w_orig, w_href, d_now]);
        }
        else {
            document.recorded_actions.push(['_url_', w_orig, w_href, d_now]);
        }
    }
    else {
        sessionStorage.setItem('recorder_activated', 'yes');
        w_orig = window.location.origin;
        w_href = window.location.href;
        document.recorded_actions.push(['begin', w_orig, w_href, d_now]);
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
    return;
};
reset_recorder_state();

document.body.addEventListener('click', function (event) {
    // Do nothing here.
});
document.body.addEventListener('formdata', function (event) {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
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
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    const d_now = Date.now();
    const element = event.target;
    const selector = getBestSelector(element);
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][0] === 'mo_dn' &&
        document.recorded_actions[ra_len-1][1] === selector)
    {
        document.recorded_actions.pop();
    }
    if (element.draggable === true)
        document.recorded_actions.push(['drags', selector, '', d_now]);
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('dragend', function (event) {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    ra_len = document.recorded_actions.length;
    if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'drags')
    {
        document.recorded_actions.pop();
        json_rec_act = JSON.stringify(document.recorded_actions);
        sessionStorage.setItem('recorded_actions', json_rec_act);
    }
});
document.body.addEventListener('drop', function (event) {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    const d_now = Date.now();
    const element = event.target;
    const selector = getBestSelector(element);
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
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    const d_now = Date.now();
    const element = event.target;
    const selector = getBestSelector(element);
    ra_len = document.recorded_actions.length;
    tag_name = element.tagName.toLowerCase();
    if (tag_name === 'select')
    {
        el_computed = document.querySelector(selector);
        optxt = el_computed.options[el_computed.selectedIndex].text;
        document.recorded_actions.push(['s_opt', selector, optxt, d_now]);
    }
    else if (tag_name === 'input' && element.type === 'range')
    {
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
        {
            document.recorded_actions.pop();
            ra_len = document.recorded_actions.length;
        }
        // Do it twice for click and multiple changes.
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
        {
            document.recorded_actions.pop();
            ra_len = document.recorded_actions.length;
        }
        value = element.value;
        document.recorded_actions.push(['set_v', selector, value, d_now]);
    }
    else if (tag_name === 'input' && element.type === 'file') {
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
        {
            document.recorded_actions.pop();
            ra_len = document.recorded_actions.length;
        }
        value = element.value;
        document.recorded_actions.push(['cho_f', selector, value, d_now]);
    }
    else if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][1] === selector &&
        tag_name === 'input' && element.type === 'checkbox')
    {
        // The checkbox state only needs to be set once. (Pop duplicates.)
        document.recorded_actions.pop();
        ra_len = document.recorded_actions.length;
        if (ra_len > 0 && document.recorded_actions[ra_len-1][1] === selector)
            document.recorded_actions.pop();
    }
    // Go back to `if`, not `else if`.
    if (tag_name === 'input' && element.type === 'checkbox' && element.checked)
    {
        document.recorded_actions.push(['c_box', selector, 'yes', d_now]);
    }
    else if (tag_name === 'input' && element.type === 'checkbox' &&
             !element.checked)
    {
        document.recorded_actions.push(['c_box', selector, 'no', d_now]);
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('mousedown', function (event) {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    const d_now = Date.now();
    const element = event.target;
    const selector = getBestSelector(element);
    ra_len = document.recorded_actions.length;
    tag_name = element.tagName.toLowerCase();
    if (ra_len > 0 && document.recorded_actions[ra_len-1][0] === 'mo_dn') {
        document.recorded_actions.pop();
    }
    if (tag_name === 'select') {
        // Do Nothing. (Handle select in 'change' action.)
    }
    else {
        document.recorded_actions.push(['mo_dn', selector, '', d_now]);
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('mouseup', function (event) {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    const d_now = Date.now();
    const element = event.target;
    const selector = getBestSelector(element);
    ra_len = document.recorded_actions.length;
    tag_name = element.tagName.toLowerCase();
    parent_element = element.parentElement;
    parent_tag_name = parent_element.tagName.toLowerCase();
    grand_element = "";
    grand_tag_name = "";
    origin = "";
    if (parent_element.parentElement != 'null') {
        grand_element = parent_element.parentElement;
        grand_tag_name = grand_element.tagName.toLowerCase();
    }
    if (ra_len > 0 &&
        document.recorded_actions[ra_len-1][1] === selector &&
        (document.recorded_actions[ra_len-1][0] === 'mo_dn' ||
         tag_name === 'a' || parent_tag_name === 'a') &&
        tag_name !== 'select')
    {
        href = '';
        if (tag_name === 'a' &&
            element.hasAttribute('href') &&
            element.getAttribute('href').length > 0 &&
            element.origin != 'null')
        {
            href = element.href;
            origin = element.origin;
        }
        else if (parent_tag_name === 'a' &&
            parent_element.hasAttribute('href') &&
            parent_element.getAttribute('href').length > 0 &&
            parent_element.origin != 'null')
        {
            href = parent_element.href;
            origin = parent_element.origin;
        }
        else if (grand_tag_name === 'a' &&
            grand_element.hasAttribute('href') &&
            grand_element.getAttribute('href').length > 0 &&
            grand_element.origin != 'null')
        {
            href = grand_element.href;
            origin = grand_element.origin;
        }
        document.recorded_actions.pop();
        child_sep = ' > ';
        child_count = ssOccurrences(selector, child_sep);
        if ((tag_name === "a" && !element.hasAttribute('onclick') &&
             child_count > 0 && href.length > 0) ||
            (parent_tag_name === "a" && href.length > 0 &&
             child_count > 1 && !parent_element.hasAttribute('onclick')) ||
            (grand_tag_name === "a" && href.length > 0 &&
             child_count > 2 && !grand_element.hasAttribute('onclick')))
        {
            w_orig = window.location.origin;
            if (origin === w_orig) {
                document.recorded_actions.push(['_url_', origin, href, d_now]);
            }
            else {
                document.recorded_actions.push(['begin', origin, href, d_now]);
            }
        }
        else {
            document.recorded_actions.push(['click', selector, href, d_now]);
        }
        // Switch to hover_click() if in a dropdown.
        if (element.parentElement.classList.contains('dropdown-content') &&
            element.parentElement.parentElement.classList.contains('dropdown'))
        {
            ch_s = selector;
            pa_el = element.parentElement.parentElement;
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
        // Probably an accidental drag & drop action.
        document.recorded_actions.pop();
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
document.body.addEventListener('contextmenu', function (event) {
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    const element = event.target;
    const selector = getBestSelector(element);
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
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
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
    if (typeof document.recorded_actions === 'undefined')
        reset_recorder_state();
    // Controls for Pausing and Resuming the Recorder.
    if (event.key.toLowerCase() === 'escape' &&
        sessionStorage.getItem('pause_recorder') === 'no')
    {
        sessionStorage.setItem('pause_recorder', 'yes');
        console.log('The SeleniumBase Recorder has paused.');
        no_border = 'none';
        document.querySelector('body').style.border = no_border;
    }
    else if ((event.key === '`' || event.key === '~') &&
        sessionStorage.getItem('pause_recorder') === 'yes')
    {
        sessionStorage.setItem('pause_recorder', 'no');
        console.log('The SeleniumBase Recorder has resumed.');
        red_border = 'thick solid #EE3344';
        document.querySelector('body').style.border = red_border;
    }
    // Continue after checking for pause/resume controls.
    if (sessionStorage.getItem('pause_recorder') === 'yes')
        return;
    const d_now = Date.now();
    const element = event.target;
    const selector = getBestSelector(element);
    skip_input = false;
    if ((element.tagName.toLowerCase() === 'input' &&
        element.type !== 'checkbox' && element.type !== 'range') ||
        element.tagName.toLowerCase() === 'textarea')
    {
        ra_len = document.recorded_actions.length;
        if (ra_len > 0 &&
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
                ['input', selector, element.value, d_now]);
        }
    }
    json_rec_act = JSON.stringify(document.recorded_actions);
    sessionStorage.setItem('recorded_actions', json_rec_act);
});
var r_border_style = 'thick solid #EE3344';
document.querySelector('body').style.border = r_border_style;
"""
