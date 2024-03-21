"""This module contains useful Javascript utility methods for BaseCase."""
import re
import requests
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from seleniumbase import config as sb_config
from seleniumbase.config import settings
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import css_to_xpath
from seleniumbase.fixtures import xpath_to_css


def wait_for_ready_state_complete(driver, timeout=settings.LARGE_TIMEOUT):
    """The DOM (Document Object Model) has a property called "readyState".
    When the value of this becomes "complete", page resources are considered
      fully loaded (although AJAX and other loads might still be happening).
    This method will wait until document.readyState == "complete".
    This may be redundant, as methods already wait for page elements to load.
    If the timeout is exceeded, the test will still continue
      because readyState == "interactive" may be good enough.
    (Previously, tests would fail immediately if exceeding the timeout.)"""
    if hasattr(settings, "SKIP_JS_WAITS") and settings.SKIP_JS_WAITS:
        return
    if sb_config.time_limit and not sb_config.recorder_mode:
        from seleniumbase.fixtures import shared_utils

    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        if sb_config.time_limit and not sb_config.recorder_mode:
            shared_utils.check_if_time_limit_exceeded()
        try:
            ready_state = driver.execute_script("return document.readyState;")
        except WebDriverException:
            # Bug fix for: [Permission denied to access property "document"]
            time.sleep(0.03)
            return True
        if ready_state == "complete":
            time.sleep(0.01)  # Better be sure everything is done loading
            return True
        else:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    return False  # readyState stayed "interactive" (Not "complete")


def execute_async_script(driver, script, timeout=settings.EXTREME_TIMEOUT):
    driver.set_script_timeout(timeout)
    return driver.execute_async_script(script)


def wait_for_angularjs(driver, timeout=settings.LARGE_TIMEOUT, **kwargs):
    if hasattr(settings, "SKIP_JS_WAITS") and settings.SKIP_JS_WAITS:
        return
    if not settings.WAIT_FOR_ANGULARJS:
        return
    if timeout == settings.MINI_TIMEOUT:
        timeout = settings.MINI_TIMEOUT / 2.0

    NG_WRAPPER = (
        "%(prefix)s"
        "var $elm=document.querySelector("
        "'[data-ng-app],[ng-app],.ng-scope')||document;"
        "if(window.angular && angular.getTestability){"
        "angular.getTestability($elm).whenStable(%(handler)s)"
        "}else{"
        "var $inj;try{$inj=angular.element($elm).injector()||"
        "angular.injector(['ng'])}catch(ex){"
        "$inj=angular.injector(['ng'])};$inj.get=$inj.get||"
        "$inj;$inj.get('$browser')."
        "notifyWhenNoOutstandingRequests(%(handler)s)}"
        "%(suffix)s"
    )
    def_pre = "var cb=arguments[arguments.length-1];if(window.angular){"
    prefix = kwargs.pop("prefix", def_pre)
    handler = kwargs.pop("handler", "function(){cb(true)}")
    suffix = kwargs.pop("suffix", "}else{cb(false)}")
    script = NG_WRAPPER % {
        "prefix": prefix,
        "handler": handler,
        "suffix": suffix,
    }
    try:
        # This closes any pop-up alerts (otherwise the next part fails)
        driver.execute_script("")
    except Exception:
        pass
    try:
        execute_async_script(driver, script, timeout=timeout)
    except Exception:
        time.sleep(0.05)


def convert_to_css_selector(selector, by=By.CSS_SELECTOR):
    if by == By.CSS_SELECTOR:
        return selector
    elif by == By.ID:
        return "#%s" % selector
    elif by == By.CLASS_NAME:
        return ".%s" % selector
    elif by == By.NAME:
        return '[name="%s"]' % selector
    elif by == By.TAG_NAME:
        return selector
    elif (
        by == By.XPATH
        or (
            selector.startswith("/")
            or selector.startswith("./")
            or selector.startswith("(")
        )
    ):
        return xpath_to_css.convert_xpath_to_css(selector)
    elif by == By.LINK_TEXT:
        return 'a:contains("%s")' % selector
    elif by == By.PARTIAL_LINK_TEXT:
        return 'a:contains("%s")' % selector
    else:
        raise Exception(
            "Exception: Could not convert {%s}(by=%s) to CSS_SELECTOR!"
            % (selector, by)
        )


def is_html_inspector_activated(driver):
    try:
        driver.execute_script("HTMLInspector;")  # Fails if not defined
        return True
    except Exception:
        return False


def is_jquery_activated(driver):
    try:
        driver.execute_script("jQuery('html');")  # Fails if jq is not defined
        return True
    except Exception:
        return False


def wait_for_jquery_active(driver, timeout=None):
    if not timeout:
        timeout = 2
    else:
        timeout = int(timeout * 10.0)
    for x in range(timeout):
        # jQuery needs a small amount of time to activate.
        try:
            driver.execute_script("jQuery('html');")
            wait_for_ready_state_complete(driver)
            wait_for_angularjs(driver)
            return
        except Exception:
            time.sleep(0.1)


def raise_unable_to_load_jquery_exception(driver):
    has_csp_error = False
    csp_violation = "violates the following Content Security Policy directive"
    browser_logs = []
    try:
        browser_logs = driver.get_log("browser")
    except (ValueError, WebDriverException):
        pass
    for entry in browser_logs:
        if entry["level"] == "SEVERE":
            if csp_violation in entry["message"]:
                has_csp_error = True
    if has_csp_error:
        raise Exception(
            """Unable to load jQuery on "%s" due to a violation """
            """of the website's Content Security Policy directive. """
            """To override this policy, add "--disable-csp" on the """
            """command-line when running your tests.""" % driver.current_url
        )
    else:
        raise Exception(
            """Unable to load jQuery on "%s" because this website may be """
            """restricting external JavaScript resources from loading."""
            % driver.current_url
        )


def activate_jquery(driver):
    # If "jQuery is not defined" on a website, use this method to activate it.
    # This method is needed because jQuery is not always defined on web sites.
    try:
        # Let's first find out if jQuery is already defined.
        driver.execute_script("jQuery('html');")
        # Since that command worked, jQuery is defined. Let's return.
        return
    except Exception:
        # jQuery is not currently defined. Let's proceed by defining it.
        pass
    jquery_js = constants.JQuery.MIN_JS
    add_js_link(driver, jquery_js)
    for x in range(36):
        # jQuery needs a small amount of time to activate.
        try:
            driver.execute_script("jQuery('html');")
            return
        except Exception:
            if x == 18:
                add_js_link(driver, jquery_js)
            time.sleep(0.1)
    # Since jQuery still isn't activating, give up and raise an exception
    raise_unable_to_load_jquery_exception(driver)


def are_quotes_escaped(string):
    if string.count("\\'") != string.count("'") or (
        string.count('\\"') != string.count('"')
    ):
        return True
    return False


def escape_quotes_if_needed(string):
    """re.escape() works differently in Python 3.7.0 than earlier versions:

    Python 3.6.5:
    >>> import re
    >>> re.escape('"')
    '\\"'

    Python 3.7.0:
    >>> import re
    >>> re.escape('"')
    '"'

    SeleniumBase needs quotes to be properly escaped for Javascript calls.
    """
    if are_quotes_escaped(string):
        if string.count("'") != string.count("\\'"):
            string = string.replace("'", "\\'")
        if string.count('"') != string.count('\\"'):
            string = string.replace('"', '\\"')
    return string


def is_in_frame(driver):
    # Returns True if the driver has switched to a frame.
    # Returns False if the driver was on default content.
    in_basic_frame = driver.execute_script(
        """
        var frame = window.frameElement;
        if (frame) {
            return true;
        }
        else {
            return false;
        }
        """
    )
    location_href = driver.execute_script("""return window.location.href;""")
    in_external_frame = False
    if driver.current_url != location_href:
        in_external_frame = True
    if in_basic_frame or in_external_frame:
        return True
    return False


def safe_execute_script(driver, script):
    """When executing a script that contains a jQuery command,
    it's important that the jQuery library has been loaded first.
    This method will load jQuery if it wasn't already loaded."""
    try:
        driver.execute_script(script)
    except Exception:
        # The likely reason this fails is because: "jQuery is not defined"
        activate_jquery(driver)  # It's a good thing we can define it here
        driver.execute_script(script)


def remove_extra_slashes(selector):
    if selector.count('\\"') > 0:
        if selector.count('\\"') == selector.count('"'):
            selector = selector.replace('\\"', '"')
        elif selector.count('\\"') == selector[1:-1].count('"') and (
            "'" not in selector[1:-1]
        ):
            selector = "'" + selector[1:-1].replace('\\"', '"') + "'"
        else:
            pass
    if selector.count("\\'") > 0:
        if selector.count("\\'") == selector.count("'"):
            selector = selector.replace("\\'", "'")
        elif selector.count("\\'") == selector[1:-1].count("'") and (
            '"' not in selector[1:-1]
        ):
            selector = '"' + selector[1:-1].replace("\\'", "'") + '"'
        else:
            pass
    return selector


def optimize_selector(selector):
    if (len(selector) > 2 and selector[0] == "'") and (
        selector[-1] == "'" and '"' not in selector[1:-1]
    ):
        selector = '"' + selector[1:-1] + '"'
    if (
        selector.count('"') == 0
        and selector.count("'") >= 2
        and selector.count("'") % 2 == 0
        and "='" in selector
        and "']" in selector
    ):
        swap_char = "*_SWAP_CHAR_*"
        selector = selector.replace("'", swap_char)
        selector = selector.replace('"', "'")
        selector = selector.replace(swap_char, '"')
    return selector


def wait_for_css_query_selector(
    driver, selector, timeout=settings.LARGE_TIMEOUT
):
    element = None
    selector = escape_quotes_if_needed(selector)
    selector = remove_extra_slashes(selector)
    selector = optimize_selector(selector)
    script = """return document.querySelector('%s');""" % selector
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.execute_script(script)
            if element:
                return element
        except Exception:
            element = None
        if not element:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise NoSuchElementException(
        "Element {%s} was not present after %s seconds!" % (selector, timeout)
    )


def is_valid_by(by):
    return by in [
        "css selector", "class name", "id", "name",
        "link text", "xpath", "tag name", "partial link text",
    ]


def swap_selector_and_by_if_reversed(selector, by):
    if not is_valid_by(by) and is_valid_by(selector):
        selector, by = by, selector
    return (selector, by)


def call_me_later(driver, script, ms):
    """Call script after ms passed."""
    call = "function() {%s}" % script
    driver.execute_script("window.setTimeout(%s, %s);" % (call, ms))


def highlight(driver, selector, by="css selector", loops=4):
    """For driver.highlight() / driver.page.highlight()"""
    swap_selector_and_by_if_reversed(selector, by)
    if ":contains(" in selector:
        by = "xpath"
        selector = css_to_xpath.convert_css_to_xpath(selector)
    element = None
    try:
        element = driver.find_element(by, selector)
    except Exception:
        time.sleep(1)
        element = driver.find_element(by, selector)
    o_bs = ""  # original_box_shadow
    style = element.get_attribute("style")
    if style and "box-shadow: " in style:
        box_start = style.find("box-shadow: ")
        box_end = style.find(";", box_start) + 1
        original_box_shadow = style[box_start:box_end]
        o_bs = original_box_shadow
    highlight_element_with_js(driver, element, loops=loops, o_bs=o_bs)


def highlight_with_js(driver, selector, loops=4, o_bs=""):
    try:
        # This closes any pop-up alerts
        driver.execute_script("")
    except Exception:
        pass
    if selector == "html":
        selector = "body"
    selector_no_spaces = selector.replace(" ", "")
    early_exit = False
    if '[style=\\"' in selector_no_spaces:
        if "box\\-shadow:" in selector:
            early_exit = True  # Changing the box-shadow changes the selector
        elif '[style=\\"' in selector:
            selector = selector.replace('[style=\\"', '[style\\*=\\"')
        else:
            early_exit = True  # Changing the box-shadow changes the selector
        if early_exit:
            return
    script = (
        """document.querySelector('%s').style.boxShadow =
        '0px 0px 6px 6px rgba(128, 128, 128, 0.5)';"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    for n in range(loops):
        script = (
            """document.querySelector('%s').style.boxShadow =
            '0px 0px 6px 6px rgba(255, 0, 0, 1)';"""
            % selector
        )
        try:
            driver.execute_script(script)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """document.querySelector('%s').style.boxShadow =
            '0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
            % selector
        )
        try:
            driver.execute_script(script)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """document.querySelector('%s').style.boxShadow =
            '0px 0px 6px 6px rgba(0, 0, 255, 1)';"""
            % selector
        )
        try:
            driver.execute_script(script)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """document.querySelector('%s').style.boxShadow =
            '0px 0px 6px 6px rgba(0, 255, 0, 1)';"""
            % selector
        )
        try:
            driver.execute_script(script)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """document.querySelector('%s').style.boxShadow =
            '0px 0px 6px 6px rgba(128, 128, 0, 1)';"""
            % selector
        )
        try:
            driver.execute_script(script)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """document.querySelector('%s').style.boxShadow =
            '0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
            % selector
        )
        try:
            driver.execute_script(script)
        except Exception:
            return
        time.sleep(0.0181)
    script = """document.querySelector('%s').style.boxShadow =
        '%s';""" % (
        selector,
        o_bs,
    )
    try:
        driver.execute_script(script)
    except Exception:
        return


def highlight_element_with_js(driver, element, loops=4, o_bs=""):
    try:
        # This closes any pop-up alerts
        driver.execute_script("")
    except Exception:
        pass
    script = (
        """arguments[0].style.boxShadow =
        '0px 0px 6px 6px rgba(128, 128, 128, 0.5)';"""
    )
    try:
        driver.execute_script(script, element)
    except Exception:
        return
    for n in range(loops):
        script = (
            """arguments[0].style.boxShadow =
            '0px 0px 6px 6px rgba(255, 0, 0, 1)';"""
        )
        try:
            driver.execute_script(script, element)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """arguments[0].style.boxShadow =
            '0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
        )
        try:
            driver.execute_script(script, element)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """arguments[0].style.boxShadow =
            '0px 0px 6px 6px rgba(0, 0, 255, 1)';"""
        )
        try:
            driver.execute_script(script, element)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """arguments[0].style.boxShadow =
            '0px 0px 6px 6px rgba(0, 255, 0, 1)';"""
        )
        try:
            driver.execute_script(script, element)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """arguments[0].style.boxShadow =
            '0px 0px 6px 6px rgba(128, 128, 0, 1)';"""
        )
        try:
            driver.execute_script(script, element)
        except Exception:
            return
        time.sleep(0.0181)
        script = (
            """arguments[0].style.boxShadow =
            '0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
        )
        try:
            driver.execute_script(script, element)
        except Exception:
            return
        time.sleep(0.0181)
    script = """arguments[0].style.boxShadow = '%s';""" % (o_bs)
    try:
        driver.execute_script(script, element)
    except Exception:
        return


def highlight_with_jquery(driver, selector, loops=4, o_bs=""):
    try:
        # This closes any pop-up alerts
        driver.execute_script("")
    except Exception:
        pass
    if selector == "html":
        selector = "body"
    selector_no_spaces = selector.replace(" ", "")
    early_exit = False
    if '[style=\\"' in selector_no_spaces:
        if "box\\-shadow:" in selector:
            early_exit = True  # Changing the box-shadow changes the selector
        elif '[style=\\"' in selector:
            selector = selector.replace('[style=\\"', '[style\\*=\\"')
        else:
            early_exit = True  # Changing the box-shadow changes the selector
        if early_exit:
            return
    script = (
        """jQuery('%s').css('box-shadow',
        '0px 0px 6px 6px rgba(128, 128, 128, 0.5)');"""
        % selector
    )
    safe_execute_script(driver, script)
    for n in range(loops):
        script = (
            """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(255, 0, 0, 1)');"""
            % selector
        )
        driver.execute_script(script)
        time.sleep(0.0181)
        script = (
            """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(128, 0, 128, 1)');"""
            % selector
        )
        driver.execute_script(script)
        time.sleep(0.0181)
        script = (
            """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(0, 0, 255, 1)');"""
            % selector
        )
        driver.execute_script(script)
        time.sleep(0.0181)
        script = (
            """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(0, 255, 0, 1)');"""
            % selector
        )
        driver.execute_script(script)
        time.sleep(0.0181)
        script = (
            """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(128, 128, 0, 1)');"""
            % selector
        )
        driver.execute_script(script)
        time.sleep(0.0181)
        script = (
            """jQuery('%s').css('box-shadow',
            '0px 0px 6px 6px rgba(128, 0, 128, 1)');"""
            % selector
        )
        driver.execute_script(script)
        time.sleep(0.0181)
    script = """jQuery('%s').css('box-shadow', '%s');""" % (selector, o_bs)
    driver.execute_script(script)


def add_css_link(driver, css_link):
    script_to_add_css = """function injectCSS(css) {
          var head_tag=document.getElementsByTagName("head")[0];
          var link_tag=document.createElement("link");
          link_tag.rel="stylesheet";
          link_tag.type="text/css";
          link_tag.href=css;
          link_tag.crossorigin="anonymous";
          head_tag.appendChild(link_tag);
       }
       injectCSS("%s");"""
    css_link = escape_quotes_if_needed(css_link)
    driver.execute_script(script_to_add_css % css_link)


def add_js_link(driver, js_link):
    script_to_add_js = """function injectJS(link) {
          var body_tag=document.getElementsByTagName("body")[0];
          var script_tag=document.createElement("script");
          script_tag.src=link;
          script_tag.type="text/javascript";
          script_tag.crossorigin="anonymous";
          script_tag.defer;
          script_tag.onload=function() { null };
          body_tag.appendChild(script_tag);
       }
       injectJS("%s");"""
    js_link = escape_quotes_if_needed(js_link)
    driver.execute_script(script_to_add_js % js_link)


def add_css_style(driver, css_style):
    add_css_style_script = """function injectStyle(css) {
          var head_tag=document.getElementsByTagName("head")[0];
          var style_tag=document.createElement("style");
          style_tag.type="text/css";
          style_tag.appendChild(document.createTextNode(css));
          head_tag.appendChild(style_tag);
       }
       injectStyle("%s");"""
    css_style = css_style.replace("\n", "")
    css_style = escape_quotes_if_needed(css_style)
    driver.execute_script(add_css_style_script % css_style)


def add_js_code_from_link(driver, js_link):
    if js_link.startswith("//"):
        js_link = "http:" + js_link
    js_code = requests.get(js_link, timeout=5).text
    add_js_code_script = (
        """var body_tag=document.getElementsByTagName('body').item(0);"""
        """var script_tag=document.createElement("script");"""
        """script_tag.type="text/javascript";"""
        """script_tag.onload=function() { null };"""
        """script_tag.appendChild(document.createTextNode("%s"));"""
        """body_tag.appendChild(script_tag);"""
    )
    js_code = js_code.replace("\n", " ")
    js_code = escape_quotes_if_needed(js_code)
    driver.execute_script(add_js_code_script % js_code)


def add_js_code(driver, js_code):
    add_js_code_script = (
        """var body_tag=document.getElementsByTagName('body').item(0);"""
        """var script_tag=document.createElement("script");"""
        """script_tag.type="text/javascript";"""
        """script_tag.onload=function() { null };"""
        """script_tag.appendChild(document.createTextNode("%s"));"""
        """body_tag.appendChild(script_tag);"""
    )
    js_code = js_code.replace("\n", " ")
    js_code = escape_quotes_if_needed(js_code)
    driver.execute_script(add_js_code_script % js_code)


def add_meta_tag(driver, http_equiv=None, content=None):
    if http_equiv is None:
        http_equiv = "Content-Security-Policy"
    if content is None:
        content = (
            "default-src *; style-src 'self' 'unsafe-inline'; "
            "script-src: 'self' 'unsafe-inline' 'unsafe-eval'"
        )
    script_to_add_meta = """function injectMeta() {
           var meta_tag=document.createElement('meta');
           meta_tag.httpEquiv="%s";
           meta_tag.content="%s";
           document.getElementsByTagName('head')[0].appendChild(meta_tag);
        }
        injectMeta();""" % (
        http_equiv,
        content,
    )
    driver.execute_script(script_to_add_meta)


def is_jquery_confirm_activated(driver):
    try:
        driver.execute_script("jconfirm;")  # Fails if jconfirm is not defined
        return True
    except Exception:
        return False


def activate_jquery_confirm(driver):
    jquery_js = constants.JQuery.MIN_JS
    jq_confirm_css = constants.JqueryConfirm.MIN_CSS
    jq_confirm_js = constants.JqueryConfirm.MIN_JS

    if not is_jquery_activated(driver):
        add_js_link(driver, jquery_js)
        wait_for_jquery_active(driver, timeout=1.2)
    add_css_link(driver, jq_confirm_css)
    add_js_link(driver, jq_confirm_js)

    for x in range(28):
        # jQuery-Confirm needs a small amount of time to load & activate.
        if x == 14:
            add_css_link(driver, jq_confirm_css)
            add_js_link(driver, jq_confirm_js)
        try:
            driver.execute_script("jconfirm;")
            wait_for_ready_state_complete(driver)
            wait_for_angularjs(driver)
            return
        except Exception:
            time.sleep(0.1)


def activate_html_inspector(driver):
    jquery_js = constants.JQuery.MIN_JS
    html_inspector_js = constants.HtmlInspector.MIN_JS

    if is_html_inspector_activated(driver):
        return
    if not is_jquery_activated(driver):
        add_js_link(driver, jquery_js)
        wait_for_jquery_active(driver, timeout=1.2)
        wait_for_ready_state_complete(driver)
        wait_for_angularjs(driver)
    add_js_link(driver, html_inspector_js)
    wait_for_ready_state_complete(driver)
    wait_for_angularjs(driver)

    for x in range(25):
        # HTML-Inspector needs a small amount of time to load & activate.
        try:
            driver.execute_script("HTMLInspector;")
            wait_for_ready_state_complete(driver)
            wait_for_angularjs(driver)
            return
        except Exception:
            time.sleep(0.1)
    wait_for_ready_state_complete(driver)
    wait_for_angularjs(driver)


def activate_messenger(driver):
    from seleniumbase.core.style_sheet import get_messenger_style

    jquery_js = constants.JQuery.MIN_JS
    messenger_css = constants.Messenger.MIN_CSS
    messenger_js = constants.Messenger.MIN_JS
    msgr_theme_flat_js = constants.Messenger.THEME_FLAT_JS
    msgr_theme_future_js = constants.Messenger.THEME_FUTURE_JS
    msgr_theme_flat_css = constants.Messenger.THEME_FLAT_CSS
    msgr_theme_future_css = constants.Messenger.THEME_FUTURE_CSS
    msgr_theme_block_css = constants.Messenger.THEME_BLOCK_CSS
    msgr_theme_air_css = constants.Messenger.THEME_AIR_CSS
    msgr_theme_ice_css = constants.Messenger.THEME_ICE_CSS
    spinner_css = constants.Messenger.SPINNER_CSS
    underscore_js = constants.Underscore.MIN_JS

    msg_style = (
        "Messenger.options = {'maxMessages': 8, "
        "extraClasses: 'messenger-fixed "
        "messenger-on-bottom messenger-on-right', "
        "theme: 'future'}"
    )

    if not is_jquery_activated(driver):
        add_js_link(driver, jquery_js)
        wait_for_jquery_active(driver, timeout=1.1)
    add_css_link(driver, messenger_css)
    add_css_link(driver, msgr_theme_flat_css)
    add_css_link(driver, msgr_theme_future_css)
    add_css_link(driver, msgr_theme_block_css)
    add_css_link(driver, msgr_theme_air_css)
    add_css_link(driver, msgr_theme_ice_css)
    add_js_link(driver, underscore_js)
    add_css_link(driver, spinner_css)
    add_js_link(driver, messenger_js)
    add_css_style(driver, get_messenger_style())

    for x in range(10):
        # Messenger needs a small amount of time to load & activate.
        try:
            result = driver.execute_script(
                """ if (typeof Messenger === 'undefined') { return "U"; } """
            )
            if result == "U":
                time.sleep(0.022)
                continue
            else:
                break
        except Exception:
            time.sleep(0.02)
    try:
        driver.execute_script(msg_style)
        add_js_link(driver, msgr_theme_flat_js)
        add_js_link(driver, msgr_theme_future_js)
        wait_for_ready_state_complete(driver)
        wait_for_angularjs(driver)
        return
    except Exception:
        time.sleep(0.1)


def set_messenger_theme(
    driver, theme="default", location="default", max_messages="default"
):
    if theme == "default":
        theme = "future"
    if location == "default":
        location = "bottom_right"
        if hasattr(sb_config, "mobile_emulator") and sb_config.mobile_emulator:
            location = "top_center"
    if max_messages == "default":
        max_messages = "8"

    valid_themes = ["flat", "future", "block", "air", "ice"]
    if theme not in valid_themes:
        raise Exception("Theme: %s is not in %s!" % (theme, valid_themes))
    valid_locations = [
        "top_left",
        "top_center",
        "top_right",
        "bottom_left",
        "bottom_center",
        "bottom_right",
    ]
    if location not in valid_locations:
        raise Exception(
            "Location: %s is not in %s!" % (location, valid_locations)
        )

    if location == "top_left":
        messenger_location = "messenger-on-top messenger-on-left"
    elif location == "top_center":
        messenger_location = "messenger-on-top"
    elif location == "top_right":
        messenger_location = "messenger-on-top messenger-on-right"
    elif location == "bottom_left":
        messenger_location = "messenger-on-bottom messenger-on-left"
    elif location == "bottom_center":
        messenger_location = "messenger-on-bottom"
    elif location == "bottom_right":
        messenger_location = "messenger-on-bottom messenger-on-right"

    msg_style = (
        "Messenger.options = {'maxMessages': %s, "
        "extraClasses: 'messenger-fixed %s', theme: '%s'}"
        % (max_messages, messenger_location, theme)
    )
    try:
        driver.execute_script(msg_style)
    except Exception:
        time.sleep(0.03)
        activate_messenger(driver)
        time.sleep(0.15)
        try:
            driver.execute_script(msg_style)
            time.sleep(0.02)
        except Exception:
            pass
    time.sleep(0.05)


def post_message(driver, message, msg_dur=None, style="info"):
    """A helper method to post a message on the screen with Messenger.
    (Should only be called from post_message() in base_case.py)"""
    if not msg_dur:
        msg_dur = settings.DEFAULT_MESSAGE_DURATION
    msg_dur = float(msg_dur)
    message = re.escape(message)
    message = escape_quotes_if_needed(message)
    messenger_script = (
        """Messenger().post({message: "%s", type: "%s", """
        """hideAfter: %s, hideOnNavigate: true});"""
        % (message, style, msg_dur)
    )
    try:
        driver.execute_script(messenger_script)
    except Exception:
        activate_messenger(driver)
        set_messenger_theme(driver)
        try:
            driver.execute_script(messenger_script)
        except Exception:
            time.sleep(0.17)
            activate_messenger(driver)
            time.sleep(0.17)
            set_messenger_theme(driver)
            time.sleep(0.27)
            driver.execute_script(messenger_script)


def post_messenger_success_message(driver, message, msg_dur=None):
    if not msg_dur:
        msg_dur = settings.DEFAULT_MESSAGE_DURATION
    msg_dur = float(msg_dur)
    try:
        theme = "future"
        location = "bottom_right"
        if hasattr(sb_config, "mobile_emulator") and sb_config.mobile_emulator:
            location = "top_right"
        set_messenger_theme(driver, theme=theme, location=location)
        post_message(driver, message, msg_dur, style="success")
        time.sleep(msg_dur + 0.07)
    except Exception:
        pass


def post_messenger_error_message(driver, message, msg_dur=None):
    if not msg_dur:
        msg_dur = settings.DEFAULT_MESSAGE_DURATION
    msg_dur = float(msg_dur)
    try:
        set_messenger_theme(driver, theme="block", location="top_center")
        post_message(driver, message, msg_dur, style="error")
        time.sleep(msg_dur + 0.07)
    except Exception:
        pass


def highlight_with_js_2(driver, message, selector, o_bs, msg_dur):
    try:
        # This closes any pop-up alerts
        driver.execute_script("")
    except Exception:
        pass
    if selector == "html":
        selector = "body"
    selector_no_spaces = selector.replace(" ", "")
    early_exit = False
    if '[style=\\"' in selector_no_spaces:
        if "box\\-shadow:" in selector:
            early_exit = True  # Changing the box-shadow changes the selector
        elif '[style=\\"' in selector:
            selector = selector.replace('[style=\\"', '[style\\*=\\"')
        else:
            early_exit = True  # Changing the box-shadow changes the selector
        if early_exit:
            try:
                activate_jquery(driver)
                post_messenger_success_message(driver, message, msg_dur)
            except Exception:
                pass
            return
    script = (
        """document.querySelector('%s').style.boxShadow =
        '0px 0px 6px 6px rgba(128, 128, 128, 0.5)';"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """document.querySelector('%s').style.boxShadow =
        '0px 0px 6px 6px rgba(205, 30, 0, 1)';"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """document.querySelector('%s').style.boxShadow =
        '0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """document.querySelector('%s').style.boxShadow =
        '0px 0px 6px 6px rgba(50, 50, 128, 1)';"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """document.querySelector('%s').style.boxShadow =
        '0px 0px 6px 6px rgba(50, 205, 50, 1)';"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    try:
        activate_jquery(driver)
        post_messenger_success_message(driver, message, msg_dur)
    except Exception:
        pass
    script = """document.querySelector('%s').style.boxShadow = '%s';""" % (
        selector,
        o_bs,
    )
    try:
        driver.execute_script(script)
    except Exception:
        return


def highlight_element_with_js_2(driver, message, element, o_bs, msg_dur):
    try:
        # This closes any pop-up alerts
        driver.execute_script("")
    except Exception:
        pass
    script = (
        """arguments[0].style.boxShadow =
        '0px 0px 6px 6px rgba(128, 128, 128, 0.5)';"""
    )
    try:
        driver.execute_script(script, element)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """arguments[0].style.boxShadow =
        '0px 0px 6px 6px rgba(205, 30, 0, 1)';"""
    )
    try:
        driver.execute_script(script, element)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """arguments[0].style.boxShadow =
        '0px 0px 6px 6px rgba(128, 0, 128, 1)';"""
    )
    try:
        driver.execute_script(script, element)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """arguments[0].style.boxShadow =
        '0px 0px 6px 6px rgba(50, 50, 128, 1)';"""
    )
    try:
        driver.execute_script(script, element)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """arguments[0].style.boxShadow =
        '0px 0px 6px 6px rgba(50, 205, 50, 1)';"""
    )
    try:
        driver.execute_script(script, element)
    except Exception:
        return
    time.sleep(0.0181)
    try:
        activate_jquery(driver)
        post_messenger_success_message(driver, message, msg_dur)
    except Exception:
        pass
    script = """arguments[0].style.boxShadow = '%s';""" % (o_bs)
    try:
        driver.execute_script(script, element)
    except Exception:
        return


def highlight_with_jquery_2(driver, message, selector, o_bs, msg_dur):
    if selector == "html":
        selector = "body"
    selector_no_spaces = selector.replace(" ", "")
    early_exit = False
    if '[style=\\"' in selector_no_spaces:
        if "box\\-shadow:" in selector:
            early_exit = True  # Changing the box-shadow changes the selector
        elif '[style=\\"' in selector:
            selector = selector.replace('[style=\\"', '[style\\*=\\"')
        else:
            early_exit = True  # Changing the box-shadow changes the selector
        if early_exit:
            try:
                activate_jquery(driver)
                post_messenger_success_message(driver, message, msg_dur)
            except Exception:
                pass
            return
    script = (
        """jQuery('%s').css('box-shadow',
        '0px 0px 6px 6px rgba(128, 128, 128, 0.5)');"""
        % selector
    )
    try:
        safe_execute_script(driver, script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """jQuery('%s').css('box-shadow',
        '0px 0px 6px 6px rgba(205, 30, 0, 1)');"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """jQuery('%s').css('box-shadow',
        '0px 0px 6px 6px rgba(128, 0, 128, 1)');"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """jQuery('%s').css('box-shadow',
        '0px 0px 6px 6px rgba(50, 50, 200, 1)');"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)
    script = (
        """jQuery('%s').css('box-shadow',
        '0px 0px 6px 6px rgba(50, 205, 50, 1)');"""
        % selector
    )
    try:
        driver.execute_script(script)
    except Exception:
        return
    time.sleep(0.0181)

    try:
        activate_jquery(driver)
        post_messenger_success_message(driver, message, msg_dur)
    except Exception:
        pass

    script = """jQuery('%s').css('box-shadow', '%s');""" % (selector, o_bs)
    try:
        driver.execute_script(script)
    except Exception:
        return


def get_active_element_css(driver):
    from seleniumbase.js_code import active_css_js

    return driver.execute_script(active_css_js.get_active_element_css)


def get_locale_code(driver):
    script = "return navigator.language || navigator.languages[0];"
    return driver.execute_script(script)


def get_origin(driver):
    return driver.execute_script("return window.location.origin;")


def get_user_agent(driver):
    return driver.execute_script("return navigator.userAgent;")


def get_scroll_distance_to_element(driver, element):
    try:
        scroll_position = driver.execute_script("return window.scrollY;")
        element_location = None
        element_location = element.location["y"]
        element_location = element_location - constants.Scroll.Y_OFFSET
        if element_location < 0:
            element_location = 0
        distance = element_location - scroll_position
        return distance
    except Exception:
        return 0


def scroll_to_element(driver, element):
    element_location_y = None
    element_location_x = None
    element_width = 0
    screen_width = 0
    try:
        element_location_y = element.location["y"]
    except Exception:
        return False
    try:
        element_location_x = element.location["x"]
        element_width = element.size["width"]
        screen_width = driver.get_window_size()["width"]
    except Exception:
        element_location_x = 0
    element_location_y = element_location_y - constants.Scroll.Y_OFFSET
    if element_location_y < 0:
        element_location_y = 0
    element_location_x_fix = element_location_x - 400
    if element_location_x_fix < 0:
        element_location_x_fix = 0
    if element_location_x + element_width <= screen_width:
        element_location_x_fix = 0
    scroll_script = "window.scrollTo(%s, %s);" % (
        element_location_x_fix, element_location_y
    )
    # The old jQuery scroll_script required by=By.CSS_SELECTOR
    # scroll_script = "jQuery('%s')[0].scrollIntoView()" % selector
    # This other scroll_script does not centralize the element
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    try:
        driver.execute_script(scroll_script)
        return True
    except Exception:
        return False


def slow_scroll_to_element(driver, element, *args, **kwargs):
    if driver.capabilities["browserName"] == "internet explorer":
        # IE breaks on slow-scrolling. Do a fast scroll instead.
        scroll_to_element(driver, element)
        return
    scroll_position = driver.execute_script("return window.scrollY;")
    element_location_y = None
    try:
        element_location_y = element.location["y"]
    except Exception:
        element.location_once_scrolled_into_view
        return
    try:
        element_location_x = element.location["x"]
        element_width = element.size["width"]
        screen_width = driver.get_window_size()["width"]
    except Exception:
        element_location_x = 0
    element_location_y = element_location_y - constants.Scroll.Y_OFFSET
    if element_location_y < 0:
        element_location_y = 0
    element_location_x_fix = element_location_x - 400
    if element_location_x_fix < 0:
        element_location_x_fix = 0
    if element_location_x + element_width <= screen_width:
        element_location_x_fix = 0
    distance = element_location_y - scroll_position
    if distance != 0:
        total_steps = int(abs(distance) / 50.0) + 2.0
        step_value = float(distance) / total_steps
        new_position = scroll_position
        for y in range(int(total_steps)):
            time.sleep(0.011)
            new_position += step_value
            scroll_script = "window.scrollTo(0, %s);" % new_position
            driver.execute_script(scroll_script)
    time.sleep(0.01)
    scroll_script = "window.scrollTo(%s, %s);" % (
        element_location_x_fix, element_location_y
    )
    driver.execute_script(scroll_script)
    time.sleep(0.01)
    if distance > 430 or distance < -300:
        # Add small recovery time for long-distance slow-scrolling
        time.sleep(0.162)
    else:
        time.sleep(0.045)


def get_drag_and_drop_script():
    # This script uses jQuery to perform a Drag-and-Drop action.
    # (Requires the Drag-selector and the Drop-selector to work)
    script = r"""(function( $ ) {
        $.fn.simulateDragDrop = function(options) {
                return this.each(function() {
                        new $.simulateDragDrop(this, options);
                });
        };
        $.simulateDragDrop = function(elem, options) {
                this.options = options;
                this.simulateEvent(elem, options);
        };
        $.extend($.simulateDragDrop.prototype, {
                simulateEvent: function(elem, options) {
                        /*Simulating drag start*/
                        var type = 'dragstart';
                        var event = this.createEvent(type);
                        this.dispatchEvent(elem, type, event);

                        /*Simulating drop*/
                        type = 'drop';
                        var dropEvent = this.createEvent(type, {});
                        dropEvent.dataTransfer = event.dataTransfer;
                        this.dispatchEvent(
                            $(options.dropTarget)[0], type, dropEvent);

                        /*Simulating drag end*/
                        type = 'dragend';
                        var dragEndEvent = this.createEvent(type, {});
                        dragEndEvent.dataTransfer = event.dataTransfer;
                        this.dispatchEvent(elem, type, dragEndEvent);
                },
                createEvent: function(type) {
                        var event = document.createEvent("CustomEvent");
                        event.initCustomEvent(type, true, true, null);
                        event.dataTransfer = {
                                data: {
                                },
                                setData: function(type, val){
                                        this.data[type] = val;
                                },
                                getData: function(type){
                                        return this.data[type];
                                }
                        };
                        return event;
                },
                dispatchEvent: function(elem, type, event) {
                        if(elem.dispatchEvent) {
                                elem.dispatchEvent(event);
                        }else if( elem.fireEvent ) {
                                elem.fireEvent("on"+type, event);
                        }
                }
        });
        })(jQuery);"""
    return script


def get_js_drag_and_drop_script():
    # HTML5 Drag-and-Drop script (Requires extra parameters to work)
    # param1 (WebElement): Source element to drag
    # param2 (WebElement): Target element for the drop (Optional)
    # param3 (int): Optional - Drop offset x relative to the target
    # param4 (int): Optional - Drop offset y relative to the target
    # param4 (int): Optional - Delay in milliseconds (default = 1ms)
    # param5 (string): Optional - Key pressed (ALT or CTRL or SHIFT)
    script = """var t=arguments,e=t[0],n=t[1],i=t[2]||0,o=t[3]||0,r=t[4]||1,
        a=t[5]||'',s='alt'===a||'\ue00a'===a,l='ctrl'===a||'\ue009'===a,
        c='shift'===a||'\ue008'===a,u=e.ownerDocument,
        f=e.getBoundingClientRect(),g=n?n.getBoundingClientRect():f,
        p=f.left+f.width/2,d=f.top+f.height/2,h=g.left+(i||g.width/2),
        m=g.top+(o||g.height/2),v=u.elementFromPoint(p,d),
        y=u.elementFromPoint(h,m);if(!v||!y){
        var E=new Error('source or target element is not interactable');
        throw E.code=15,E}var _={constructor:DataTransfer,effectAllowed:null,
        dropEffect:null,types:[],files:Object.setPrototypeOf([],null),
        _items:Object.setPrototypeOf([],{add:function(t,e){
        this[this.length]={_data:''+t,kind:'string',
        type:e,getAsFile:function(){},getAsString:function(t){t(this._data)}},
        _.types.push(e)},remove:function(t){
        Array.prototype.splice.call(this,65535&t,1),_.types.splice(65535&t,1)},
        clear:function(t,e){this.length=0,_.types.length=0}}),
        setData:function(t,e){this.clearData(t),this._items.add(e,t)},
        getData:function(t){for(var e=this._items.length;
        e--&&this._items[e].type!==t;);return e>=0?this._items[e]._data:null},
        clearData:function(t){for(var e=this._items.length;
        e--&&this._items[e].type!==t;);this._items.remove(e)},
        setDragImage:function(t){}};function w(t,e,n,i){
        for(var o=0;o<e.length;++o){var r=u.createEvent('MouseEvent');
        r.initMouseEvent(e[o],!0,!0,u.defaultView,0,0,0,p,d,l,s,c,!1,0,null),
        t.dispatchEvent(r)}i&&setTimeout(i,n)}function D(t,e,n,i){
        var o=u.createEvent('DragEvent');o.initMouseEvent(
        e,!0,!0,u.defaultView,0,0,0,p,d,l,s,c,!1,0,null),Object.setPrototypeOf(
        o,null),o.dataTransfer=_,Object.setPrototypeOf(o,DragEvent.prototype),
        t.dispatchEvent(o),i&&setTimeout(i,n)}
        'items'in DataTransfer.prototype&&(_.items=_._items),
        w(v,['pointerdown','mousedown'],1,function(){
        for(var t=v;t&&!t.draggable;)t=t.parentElement;if(t&&t.contains(v)){
        var e=y.getBoundingClientRect();D(v,'dragstart',r,function(){
        var t=y.getBoundingClientRect();p=t.left+h-e.left,d=t.top+m-e.top,D(
        y,'dragenter',1,function(){D(y,'dragover',r,
        function(){D(u.elementFromPoint(p,d),'drop',1,function(){D(v,'dragend',
        1,function(){w(u.elementFromPoint(p,d),
        ['mouseup','pointerup'])})})})})})}})"""
    return script


def get_drag_and_drop_with_offset_script(selector, x, y):
    # This script uses pure JS (No jQuery)
    script_a = """
        var source = document.querySelector("%s");
        var offsetX = %f;
        var offsetY = %f;
        """ % (
        selector,
        x,
        y,
    )
    script_b = r"""
        var rect = source.getBoundingClientRect();
        var dragPt = {x: rect.left + (rect.width >> 1),
                      y: rect.top + (rect.height >> 1)};
        var dropPt = {x: dragPt.x + offsetX, y: dragPt.y + offsetY};
        var target = document.elementFromPoint(dropPt.x, dropPt.y);
        var dataTransfer = {
          dropEffect: '',
          effectAllowed: 'all',
          files: [],
          items: {},
          types: [],
          setData: function (format, data) {
            this.items[format] = data;
            this.types.push(format);
          },
          getData: function (format) {
            return this.items[format];
          },
          clearData: function (format) { }
        };
        var emit = function (event, target, pt) {
          var evt = document.createEvent('MouseEvent');
          evt.initMouseEvent(event, true, true, window, 0, 0, 0, pt.x, pt.y,
                             false, false, false, false, 0, null);
          evt.dataTransfer = dataTransfer;
          target.dispatchEvent(evt);
        };
        emit('mousedown', source, dragPt);
        emit('mousemove', source, dragPt);
        emit('mousemove', source, dropPt);
        emit('mouseup',   source, dropPt);"""
    script = script_a + script_b
    return script


def clear_out_console_logs(driver):
    try:
        # Clear out the current page log before navigating to a new page
        # (To make sure that assert_no_js_errors() uses current results)
        driver.get_log("browser")
    except Exception:
        pass


def _jq_format(code):
    """
    DEPRECATED - Use re.escape() instead, which performs the intended action.
    Use before throwing raw code such as 'div[tab="advanced"]' into jQuery.
    Selectors with quotes inside of quotes would otherwise break jQuery.
    If you just want to escape quotes, there's escape_quotes_if_needed().
    This is similar to "json.dumps(value)", but with one less layer of quotes.
    """
    code = code.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")
    code = code.replace('"', '\\"').replace("'", "\\'")
    code = code.replace("\v", "\\v").replace("\a", "\\a").replace("\f", "\\f")
    code = code.replace("\b", "\\b").replace(r"\u", "\\u").replace("\r", "\\r")
    return code
