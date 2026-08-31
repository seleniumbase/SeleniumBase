#!/usr/bin/env python3
"""
SeleniumBase Pure CDP Mode MCP Server
======================================
Exposes SeleniumBase's Pure CDP Mode (sync API, `seleniumbase.sb_cdp.Chrome`)
as MCP tools. Pure CDP Mode drives the browser entirely over the Chrome
DevTools Protocol (no WebDriver), which is SeleniumBase's stealthiest mode
and includes captcha-solving support.

Reference:
github.com/seleniumbase/SeleniumBase/blob/master/help_docs/cdp_mode_methods.md

Model: One persistent `sb_cdp.Chrome` session per server process.
Call start_browser once; drive it with the other tools; then close_browser.

Design notes (v2):
Tools are grouped around one CSS-selector-or-text-matched-by convention:
`selector` args accept a CSS selector, or visible text (e.g.
'a:contains("Sign in")'). Where the original tool set had several
near-identical tools for one concept (e.g. five click variants, five wait
variants, eight cookie/storage variants), those are now a single tool with
a mode/action/state/check parameter, to reduce the number of near-neighbor
tools an agent has to disambiguate between while keeping every underlying
capability available.

Note on elements: CDP-mode element objects (from find_element/find_all) are
live handles with their own methods (.click(), .get_html(), ...) that can't
cross the MCP boundary as stateful objects. Tools here resolve elements
immediately to plain dicts (tag, text, html) rather than returning handles.
To act on one of several matches, use click(selector, nth=...) rather than
find + click.
"""
from __future__ import annotations
import atexit
import sys
from functools import wraps
from typing import Any, Literal
from mcp.server import MCPServer
from seleniumbase import sb_cdp

mcp = MCPServer("seleniumbase-mcp")

_sb: sb_cdp.CDPMethods | None = None


def _get_sb() -> sb_cdp.CDPMethods:
    if _sb is None:
        raise RuntimeError("No browser session. Call start_browser first.")
    return _sb


def handle_sb_errors(func):
    """Catches SeleniumBase errors and surfaces them as descriptive strings
    so the LLM agent can read them and self-correct."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type = e.__class__.__name__
            error_msg = str(e).strip()
            return f"Error in {func.__name__}: {error_type} - {error_msg}"
    return wrapper


# ---------------------------------------------------------------------------
# Session lifecycle
# ---------------------------------------------------------------------------

@mcp.tool()
def start_browser(
    url: str | None = None,
    headless: bool = False,
    use_chromium: bool = False,
    browser_executable_path: str | None = None,
    incognito: bool = False,
    guest: bool = False,
    ad_block: bool = False,
    proxy: str | None = None,
) -> str:
    """Launch a Pure CDP Mode browser session. Must be called before any
    other tool. The browser is driven entirely over CDP (no WebDriver),
    which is SeleniumBase's most stealth/bot-detection-resistant mode.
    Args:
        url: Optional URL to open immediately on launch.
        headless: Run without a visible browser. (Mainly for macOS or Windows
            because Xvfb automatically provides a virtual display on Linux.)
        use_chromium: Use Chromium instead of Google Chrome. This is useful
            on environments where Google Chrome is not installed because
            SeleniumBase automatically downloads Chromium if it's not found.
        browser_executable_path: If Google Chrome is not installed in the
            default location, you can set the direct path with this arg.
            (This option should not be used if setting use_chromium to True.)
        incognito: Launch in a private/incognito window.
        guest: Launch in Chrome guest mode. (Don't use with incognito mode)
        ad_block: Enables basic ad-blocking functionality.
        proxy: Proxy string, e.g. "USER:PASS@SERVER:PORT" or "SERVER:PORT".
    """
    global _sb
    if _sb is not None:
        return (
            "A browser session is already running. Call close_browser first."
        )
    if incognito and guest:
        return "Error: incognito and guest cannot both be enabled."
    if use_chromium and browser_executable_path:
        return (
            "Error: use_chromium and browser_executable_path "
            "cannot both be used at the same time."
        )
    kwargs: dict[str, Any] = {"headless": headless}
    if use_chromium:
        kwargs["use_chromium"] = True
    if browser_executable_path:
        kwargs["browser_executable_path"] = browser_executable_path
    if incognito:
        kwargs["incognito"] = True
    if guest:
        kwargs["guest"] = True
    if ad_block:
        kwargs["ad_block"] = True
    if proxy:
        kwargs["proxy"] = proxy
    try:
        _sb = sb_cdp.Chrome(url, **kwargs)
        return (
            f"Started Pure CDP Mode browser "
            f"(url={url!r}, headless={headless}, "
            f"use_chromium={use_chromium})"
        )
    except Exception as e:
        if _sb is not None:
            try:
                _sb.quit()
            except Exception:
                pass
            _sb = None
        return (
            f"Error starting browser: "
            f"{e.__class__.__name__} - {str(e).strip()}"
        )


@mcp.tool()
def close_browser() -> str:
    """Close the browser and end the session.
    This tool should be called after you have finished using the browser
    so that you can conclude the session and free up any resources that
    were being used by Chrome/Chromium. If you need to perform more
    browser actions after using this tool, then you'll need to use the
    'start_browser' tool again in order to begin a new browser session."""
    global _sb
    if _sb is None:
        return "No browser session was running."
    try:
        _sb.quit()
    except Exception:
        pass
    _sb = None
    return "Browser closed."


@mcp.tool()
def browser_status() -> dict:
    """Return whether a browser session is currently active, along with
    the URL and title of the current page if the browser session is active.
    This tool can be used for debugging, as well as for gathering basic
    info on the current page. For instance, if a click action navigates
    the browser window to a new page, you can use this tool to find out
    the URL/title of the new page that the browser window navigated to."""
    if _sb is None:
        return {"running": False}

    try:
        return {
            "running": True,
            "url": _sb.get_current_url(),
            "title": _sb.get_title(),
        }
    except Exception as e:
        return {
            "running": False,
            "error": f"{e.__class__.__name__}: {str(e).strip()}",
        }


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def navigate(url: str) -> str:
    """Navigate to the given URL in the web browser.
    If the URL doesn't start with a protocol (eg: "https://"),
        then "https://"" is automatically prefixed in before navigation.
        (eg: "seleniumbase.io" becomes "https://seleniumbase.io")
    Waits until the initial HTML document is fully parsed and loaded.
    New pages visited will show up in browser navigation history.
    If the URL is invalid or the page can't load due to an issue,
        then the corresponding errors will be raised."""
    _get_sb().get(url)
    return f"Navigated to {url}"


@mcp.tool()
@handle_sb_errors
def navigate_history(
    action: Literal["back", "forward", "reload"] = "back",
) -> str:
    """Navigate through the current browser history or reload the current page.
    Use this tool to move backward or forward through pages already visited in
    the current browser session, or to reload the current page when its latest
    content should be fetched again. This is useful for returning to a
    previously visited page, retracing browser navigation, recovering from
    accidental navigation, or refreshing page content.
    Args:
        action: The browser navigation operation to perform:
            - "back": Navigate to the previous page in the browser history.
              Has no effect if there is no previous history entry.
            - "forward": Navigate to the next page in the browser history.
              Has no effect if there is no forward history entry.
            - "reload": Reload the current page while ignoring the browser
              cache, forcing the page resources to be fetched again.
    Returns:
        A confirmation message describing the navigation operation that was
        performed.
    Notes:
        These operations modify the current browser page and may trigger page
        loads, redirects, or other navigation events. After navigation, use
        page-information or page-content tools when you need to verify the
        resulting URL, title, or page state.
        "back" and "forward" operate on the browser's existing navigation
        history; they do not navigate to an arbitrary URL. "reload" stays on
        the current page but bypasses the browser cache.
    """
    sb = _get_sb()
    if action == "back":
        sb.go_back()
        return "Navigated back."
    if action == "forward":
        sb.go_forward()
        return "Navigated forward."
    if action == "reload":
        sb.reload(ignore_cache=True)
        return "Page reloaded."
    return (
        f"Error: unknown action '{action}'. "
        "Use 'back', 'forward', or 'reload'."
    )


@mcp.tool()
@handle_sb_errors
def get_page_info() -> dict | str:
    """Get comprehensive information about the current browser page.
    Returns the current URL, document title, origin, and navigation history.
    Use this tool after navigation or page interactions when you need to verify
    where the browser is currently located, identify the loaded page, determine
    the site's origin, or inspect how the browser reached the current page.
    Returns:
        A dictionary containing:
        - url: The current page URL, including the path and query string.
        - title: The current document title.
        - origin: The page origin (scheme, host, and port), useful for
          identifying the current website or comparing cross-origin navigation.
        - history: The browser's navigation history, useful for understanding
          the sequence of pages visited during the current session.
    This is a read-only operation and does not navigate, reload, or modify
    the current page.
    """
    sb = _get_sb()
    return {
        "url": sb.get_current_url(),
        "title": sb.get_title(),
        "origin": sb.get_origin(),
        "history": sb.get_navigation_history(),
    }


# ---------------------------------------------------------------------------
# Finding & reading
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def find_elements(
    selector: str,
    timeout: int | float | None = 7,
    include_html: bool = False,
) -> dict | str:
    """Find element(s) matching a CSS selector or visible text, and return
    their tag name, text, and outer HTML (optional).
    Args:
        selector: CSS selector, or text to search for (CDP Mode can match
            elements by selector or visible text, eg. 'a:contains("Sign in")').
        timeout: Seconds to wait for at least one match to appear.
        include_html: Whether to include the html with each matching element.
    Returns a dict with 'count' (total matches found) and 'matches' (a list
    of {tag_name, text, html} dicts, or {tag_name, text} dicts if not
    including html).
    """
    sb = _get_sb()
    els = sb.find_all(selector, timeout=timeout)
    if include_html:
        return {
            "count": len(els),
            "matches": [
                {
                    "tag_name": e.tag_name,
                    "text": e.text,
                    "html": e.get_html(),
                } for e in els
            ],
        }
    else:
        return {
            "count": len(els),
            "matches": [
                {
                    "tag_name": e.tag_name,
                    "text": e.text,
                } for e in els
            ],
        }


@mcp.tool()
@handle_sb_errors
def get_page_content(
    selector: str | None = None,
    as_html: bool = False,
    include_shadow_dom: bool = True,
) -> str:
    """Get the visible text or HTML of an element, or of the whole page.
    You can optionally include any shadow-root elements (default: True).
    Args:
        selector: Element to read from. Omit (or pass None) to read the
            whole page instead of one element.
        as_html: If True, return HTML instead of visible text.
        include_shadow_dom: Only applies when reading the whole page as HTML.
    """
    sb = _get_sb()
    if selector is None:
        if as_html:
            return sb.get_page_source(include_shadow_dom=include_shadow_dom)
        return sb.get_text("body")
    if as_html:
        return sb.get_element_html(selector)
    return sb.get_text(selector)


@mcp.tool()
@handle_sb_errors
def get_attributes(selector: str, attribute: str | None = None) -> Any:
    """Get one attribute's value from an element, or all of its attributes
    as a dict if `attribute` isn't given.
    Args:
        selector: The CSS selector of the element to get the attribute from.
        attribute: The HTML attribute of the element that you want to get."""
    sb = _get_sb()
    if attribute:
        return sb.get_element_attribute(selector, attribute)
    return sb.get_element_attributes(selector)


@mcp.tool()
@handle_sb_errors
def check_state(
    check: Literal["present", "visible", "count", "text_visible"] = "visible",
    selector: str = "body",
    text: str | None = None,
) -> Any:
    """Check the current state of the page or an element.
    Unless setting 'count', where it may wait up to 1 second, this never waits.
    Never raises exceptions — use wait_for if you want to wait for a state.
    For 'count',  if there are no matching elements, then it waits up to
    1 second for a single match to appear. If no matches after 1 second,
    then 'count' returns 0.
    Args:
        check: 'present', 'visible', 'count', 'text_visible'.
            (`text_visible` requires value for `text`.)
        selector: The CSS Selector for the chosen check.
        text: The text to use for the `text_visible` check.
    """
    sb = _get_sb()
    if check == "present":
        return sb.is_element_present(selector)
    if check == "visible":
        return sb.is_element_visible(selector)
    if check == "count":
        return len(sb.find_elements(selector, timeout=1))
    if check == "text_visible":
        if text is None:
            return (
                "Error: The 'text_visible' check requires value for 'text'."
            )
        return sb.is_text_visible(text, selector)
    return (
        f"Error: unknown check '{check}'. "
        "Use 'present', 'visible', 'count', or 'text_visible'."
    )


@mcp.tool()
@handle_sb_errors
def get_all_urls() -> list[str] | str:
    """Get a list of all linked URLs (a, link, img, script, meta) on the page.
    The full URL with the prefix will be returned for each item in the list.
    Eg: `["https://seleniumbase.io", "https://seleniumbase.com"]`.
    Depending on the element, the URL could be obtained via "href" or "src".
    This is useful for web-crawlers when looking for more links to crawl."""
    return _get_sb().get_all_urls()


# ---------------------------------------------------------------------------
# Interacting with elements
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def click(
    selector: str,
    nth: int | None = None,
    all_matches: bool = False,
    only_if_visible: bool = False,
    parent_selector: str | None = None,
    timeout: int | float | None = 7,
    scroll: bool = True,
) -> str:
    """Click an element matched by a CSS selector, or by visible text
    (e.g. 'a:contains("Sign in")').
    Args:
        nth: Click only the Nth match (1-indexed), when several elements
            match. Takes priority over `all_matches`. (`nth` set to 1 is
            no different than a regular click, since the first matching
            selector would be clicked.)
        all_matches: Click every currently-visible match, in order (e.g.
            checking every checkbox on a page). Ignored if `nth` is given.
        only_if_visible: Only try the click if the element is visible.
            Do nothing (no error or wait) if the element isn't currently
            visible, instead of waiting for it or raising an exception.
        parent_selector: If set, look for `selector` nested inside parent.
            (This option can be used to click on elements inside iframes).
        timeout: Seconds to wait for the element when doing a basic click
            without nth, all_matches, only_if_visible, or parent_selector.
            (Defaults to 7 seconds).
        scroll: Whether to scroll the element into view before clicking.
    """
    sb = _get_sb()
    if nth is not None:
        if nth < 1:
            return "Error: nth must be >= 1."
        sb.click_nth_element(selector, nth, scroll=scroll)
        return f"Clicked match #{nth} of {selector}"
    if all_matches:
        sb.click_visible_elements(selector)
        return f"Clicked all visible matches of {selector}"
    if only_if_visible:
        sb.click_if_visible(selector)
        return f"click (only_if_visible) ran for {selector}"
    if parent_selector:
        sb.nested_click(parent_selector, selector)
        return f"Clicked {selector} inside {parent_selector}"
    sb.click(selector, timeout=timeout, scroll=scroll)
    return f"Clicked {selector}"


@mcp.tool()
@handle_sb_errors
def hover(selector: str, then_click_selector: str | None = None) -> str:
    """Simulate a mouse hover over an element,
    optionally then clicking a second element that the hover reveals
    (e.g. an item in a dropdown menu).
    This is useful when clicking an item in a dropdown menu that requires
    a hover action for the dropdown list of options to appear.
    Args:
        selector: Element to hover over.
        then_click_selector: If given, click this element after hovering.
    """
    sb = _get_sb()
    if then_click_selector:
        sb.hover_and_click(selector, then_click_selector)
        return f"Hovered {selector} and clicked {then_click_selector}"
    sb.hover_element(selector)
    return f"Hovered {selector}"


@mcp.tool()
@handle_sb_errors
def drag_and_drop(source_selector: str, target_selector: str) -> str:
    """Drag a "draggable" element and drop it onto another element
    by simulating mouse actions via the Chrome DevTools Protocol (CDP).
    `source_selector` and `target_selector` should be CSS selectors.
    A wide range of events are simulated to get the most natural
    drag-and-drop effect, which include "pointerdown", "mousedown",
    "dragstart", "dragenter", "dragover", "drop", "dragend", "mouseup",
    and "pointerup", in that specific order.
    """
    _get_sb().drag_and_drop(source_selector, target_selector)
    return f"Dragged {source_selector} onto {target_selector}"


@mcp.tool()
@handle_sb_errors
def fill_input(
    selector: str,
    text: str = "",
    mode: Literal[
        "type",
        "append",
        "set_value",
        "fast_type",
        "clear",
    ] = "type",
    timeout: int | float | None = 7,
) -> str:
    """Set the value of an input, textarea, or contenteditable element.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout.
    Args:
        mode: 'type' (default) clears the field then types `text`;
            'append' sends `text` as keystrokes without clearing first;
            'set_value' sets the value directly and instantly (good for
                sliders and other fast form fills; skips key events);
            'fast_type' clears the field then types `text` fast
                (good for when the extra stealth doesn't matter);
            'clear' empties the field — `text` is ignored.
    """
    sb = _get_sb()
    if mode == "type":
        sb.type(selector, text, timeout=timeout)
    elif mode == "append":
        sb.send_keys(selector, text, timeout=timeout)
    elif mode == "set_value":
        sb.set_value(selector, text, timeout=timeout)
    elif mode == "fast_type":
        sb.fast_type(selector, text, timeout=timeout)
    elif mode == "clear":
        sb.clear_input(selector, timeout=timeout)
    else:
        return (
            f"Error: unknown mode '{mode}'. "
            "Use 'type', 'append', 'set_value', 'fast_type', or 'clear'."
        )
    return f"fill_input(mode={mode!r}) done for {selector}"


@mcp.tool()
@handle_sb_errors
def select_option(
    dropdown_selector: str,
    value: str | int,
    by: Literal["text", "value", "index"] = "text",
) -> str:
    """Select an option in a <select> dropdown.
    Raises an exception if the element or option aren't found within the
    default timeout, which is 7 seconds.
    Args:
        value: The option's visible text, its `value` attribute, or its
            0-based index (as a string), depending on `by`.
        by: 'text' (default), 'value', or 'index'.
    Using "index" for `by` is type-safe. (Eg. 4 and "4" both work the same)
    """
    sb = _get_sb()
    if by == "text":
        sb.select_option_by_text(dropdown_selector, str(value))
    elif by == "value":
        sb.select_option_by_value(dropdown_selector, str(value))
    elif by == "index":
        sb.select_option_by_index(dropdown_selector, int(value))
    else:
        return f"Error: unknown by='{by}'. Use 'text', 'value', or 'index'."
    return f"Selected ({by}={value!r}) in {dropdown_selector}"


@mcp.tool()
@handle_sb_errors
def element_action(
    selector: str,
    action: Literal["focus", "highlight", "scroll_into_view"] = "focus",
) -> str:
    """Perform a simple positioning/emphasis action on an element.
    Raises an exception if the element isn't found within the default
    timeout.
    Args:
        action: 'focus' (move keyboard focus to it), 'highlight' (briefly
            flash it using JavaScript — useful for narrating actions
            on a visible/headed browser), or 'scroll_into_view'.
    The "focus" action is useful when an element isn't fully interactable
        until the element is in focus.
    The "highlight" action is mainly for debugging and demoing purposes.
        It briefly changes the border color of an element so that a human
        watching the web browser can have their attention be called to
        that specific element being highlighted. This "highlight" action
        briefly slows the automation during the action. This action may
        also reduce stealth on some websites, which may be undesirable.
    The "scroll_into_view" action scrolls the page to the element if the
        element is not currently in view at the current scroll position.
    """
    sb = _get_sb()
    if action == "focus":
        sb.find_element(selector).focus()
    elif action == "highlight":
        sb.highlight(selector)
    elif action == "scroll_into_view":
        sb.scroll_into_view(selector)
    else:
        return (
            f"Error: unknown action '{action}'. "
            "Use 'focus', 'highlight', or 'scroll_into_view'."
        )
    return f"{action} done for {selector}"


# ---------------------------------------------------------------------------
# Waiting & assertions
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def wait_for(
    state: Literal["present", "visible", "not_visible", "absent"] = "visible",
    selector: str | None = None,
    text: str | None = None,
    timeout: int | float | None = 7,
) -> str:
    """Wait for an element or text to reach a given state before returning.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the state isn't reached within the timeout.
    Args:
        state: 'present', 'visible', 'not_visible', or 'absent' — describes
            what `selector` should reach. Ignored if `text` is given.
        selector: Element to wait on.
            Defaults to 'body' when waiting on `text`.
        text: If given, waits for this text to appear within `selector`
            instead of waiting on the element's presence/visibility.
        timeout: Seconds to wait.
    """
    sb = _get_sb()
    if selector is None and text is None:
        return "Error: `selector` and `text` cannot both be None."
    if text is not None:
        sb.wait_for_text(text, selector or "body", timeout=timeout)
        return f"Text '{text}' appeared in {selector or 'body'}."
    if state == "present":
        sb.wait_for_element_present(selector, timeout=timeout)
    elif state == "visible":
        sb.wait_for_element_visible(selector, timeout=timeout)
    elif state == "not_visible":
        sb.wait_for_element_not_visible(selector, timeout=timeout)
    elif state == "absent":
        sb.wait_for_element_absent(selector, timeout=timeout)
    else:
        return (
            f"Error: unknown state '{state}'. "
            "Use 'present', 'visible', 'not_visible', or 'absent'."
        )
    return f"Element {selector} reached state '{state}'."


@mcp.tool()
@handle_sb_errors
def assert_that(
    check: Literal[
        "element_present",
        "element_visible",
        "text",
        "title",
        "url",
        "url_contains"
    ] = "element_visible",
    selector: str | None = None,
    expected: str | None = None,
    exact: bool = False,
    timeout: int | float | None = 7,
) -> str:
    """Assert a condition about the page or an element. Raises an exception
    (surfaced back as an error string) if the assertion fails within the
    timeout (default 7 seconds). `timeout` applies only to element/text checks.
    (For url or title checks, the assertion either passes or fails right away.)
    Args:
        check: 'element_present', 'element_visible' (need `selector`);
            'text' (substring of `expected` within `selector`, default
            'html'); 'title', 'url' (exact match), or 'url_contains'
            (need `expected`).
        selector: Element to check. Used by 'element_present',
            'element_visible', and 'text'.
        expected: The text/title/url to check against. Not used for the
            element-only checks.
        exact: For check='text', require an exact match instead of a
            substring match.
        timeout: Seconds to wait before failing.
    """
    sb = _get_sb()
    if check in ("element_present", "element_visible") and selector is None:
        return f"Error: check='{check}' requires value for `selector`."
    if check in ("text", "title", "url", "url_contains") and expected is None:
        return f"Error: check='{check}' requires value for `expected`."
    if check == "element_present":
        sb.assert_element(selector, timeout=timeout)
        return f"Confirmed {selector} is present."
    if check == "element_visible":
        sb.assert_element_visible(selector, timeout=timeout)
        return f"Confirmed {selector} is visible."
    if check == "text":
        target = selector or "html"
        if exact:
            sb.assert_exact_text(expected, target, timeout=timeout)
        else:
            sb.assert_text(expected, target, timeout=timeout)
        return f"Confirmed text in {target}."
    if check == "title":
        sb.assert_title(expected)
        return f"Confirmed title is '{expected}'."
    if check == "url":
        sb.assert_url(expected)
        return f"Confirmed URL is '{expected}'."
    if check == "url_contains":
        sb.assert_url_contains(expected)
        return f"Confirmed URL contains '{expected}'."
    return (
        f"Error: unknown check '{check}'. Use 'element_present', "
        f"'element_visible', 'text', 'title', 'url', or 'url_contains'."
    )


# ---------------------------------------------------------------------------
# Cookies & storage
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def manage_cookies(
    action: Literal["get_all", "clear", "save", "load"] = "get_all",
    filename: str = "cookies.txt",
) -> Any:
    """Manage cookies for the current browser session.
    Use this tool to inspect, clear, save, or restore browser cookies. Cookie
    management is useful for inspecting session state, preserving login
    sessions between browser runs, restoring previously saved sessions, or
    resetting website state during testing.
    Args:
        action: The cookie operation to perform:
            - "get_all": Return all cookies currently available to the browser,
              including cookie attributes such as name, value, domain, path,
              expiry, and security flags.
            - "clear": Delete all cookies from the current browser session.
              Useful for resetting authentication and website state.
            - "save": Save the current browser cookies to `filename` so they
              can be restored in a later browser session. The file may be
              created or overwritten.
            - "load": Load cookies from `filename` into the current browser
              session. Useful for restoring previously saved authentication or
              session state.
        filename: Path used by the "save" and "load" actions. Defaults to
            "cookies.txt". This argument is ignored for "get_all" and "clear".
            The path is passed to SeleniumBase's cookie persistence methods.
    Returns:
        "get_all": The current browser cookies.
        "clear": A confirmation message after cookies are cleared.
        "save": A confirmation message containing the destination filename.
        "load": A confirmation message containing the source filename.
    Security:
        Cookie data can contain sensitive authentication credentials, session
        identifiers, and other private information. Only inspect, save, load,
        or share cookies when explicitly authorized.
        `filename` can access the filesystem available to the MCP server.
        Use only trusted and authorized file paths. The "save" action may
        overwrite an existing file, so avoid unintended or sensitive
        destinations.
    Notes:
        Cookies belong to the current browser session. Loading previously
        saved cookies does not guarantee that a login session will be
        restored because cookies may be expired, invalidated, domain-specific,
        or dependent on other browser state. Navigate to the appropriate
        website before loading cookies when the browser must associate them
        with a particular domain.
    """
    sb = _get_sb()
    if action == "get_all":
        return sb.get_all_cookies()
    if action == "clear":
        sb.clear_cookies()
        return "Cookies cleared."
    if action == "save":
        sb.save_cookies(name=filename)
        return f"Cookies saved to {filename}"
    if action == "load":
        sb.load_cookies(name=filename)
        return f"Cookies loaded from {filename}"
    return (
        f"Error: unknown action '{action}'. "
        "Use 'get_all', 'clear', 'save', or 'load'."
    )


@mcp.tool()
@handle_sb_errors
def manage_storage(
    key: str,
    value: str | None = None,
    storage: Literal["local", "session"] = "local",
    action: Literal["get", "set"] = "get",
) -> Any:
    """Get or set a key in the page's localStorage or sessionStorage.
    Args:
        key: The localStorage or sessionStorage key to use.
        value: The value to set when using 'set' as the `action`.
        storage: 'local' (localStorage) or 'session' (sessionStorage).
        action: 'get' or 'set'. ('set' requires `value`).
    Use this tool for managing localStorage and/or sessionStorage.
    Storage is managed via the simple JavaScript calls listed below:
        `localStorage.getItem(key)`
        `sessionStorage.getItem(key)`
        `localStorage.setItem(key, value)`
        `sessionStorage.setItem(key, value)`
    WARNING: This tool can expose authentication/session secrets that
        are are stored in localStorage/sessionStorage on the site.
        Only use against trusted sites and with trusted MCP clients.
    """
    sb = _get_sb()
    if action not in ("get", "set"):
        return "Error: action must be 'get' or 'set'."
    if action == "set" and value is None:
        return "Error: value is required when action='set'."
    if storage == "local":
        if action == "get":
            return sb.get_local_storage_item(key)
        sb.set_local_storage_item(key, value)
        return f"Set localStorage[{key!r}]"
    if storage == "session":
        if action == "get":
            return sb.get_session_storage_item(key)
        sb.set_session_storage_item(key, value)
        return f"Set sessionStorage[{key!r}]"
    return f"Error: unknown storage '{storage}'. Use 'local' or 'session'."


# ---------------------------------------------------------------------------
# Scrolling
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def scroll(
    direction: Literal["up", "down", "top", "bottom"] = "down",
    amount: int = 25,
) -> str:
    """Scroll the page by the given amount or to the location given.
    Args:
        direction: 'up' or 'down' (relative, by `amount`), 'top', or 'bottom'.
        amount: Relative scroll distance; only used for 'up'/'down'.
    When scrolling with `direction` 'up' or 'down', the `amount` represents
    a percentage of the window height. (Eg. 'down' with `amount` 25 means
    scroll the page down by 25% of the current window height.) If setting the
    `direction` to 'top' or 'bottom', then the 'amount' value is ignored. 'top'
    scrolls to the top of the page. 'bottom' scrolls to the bottom of the page.
    """
    sb = _get_sb()
    if direction == "up":
        sb.scroll_up(amount=amount)
    elif direction == "down":
        sb.scroll_down(amount=amount)
    elif direction == "top":
        sb.scroll_to_top()
    elif direction == "bottom":
        sb.scroll_to_bottom()
    else:
        return (
            f"Error: unknown direction '{direction}'. "
            "Use 'up', 'down', 'top', or 'bottom'."
        )
    return f"Scrolled {direction}."


# ---------------------------------------------------------------------------
# Windows & tabs
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def manage_window(
    action: Literal[
        "get_rect",
        "set_rect",
        "maximize",
        "minimize",
    ] = "get_rect",
    x: int | None = None,
    y: int | None = None,
    width: int | None = None,
    height: int | None = None,
) -> Any:
    """Get or change the browser window's size, position, or state.
    Args:
        action: 'get_rect', 'set_rect' (requires x, y, width, height),
            'maximize', or 'minimize'.
        x: The x position on screen for the 'set_rect' `action` only.
        y: The y position on screen for the 'set_rect' `action` only.
        width: The window width for the 'set_rect' `action` only.
        height: The window height for the 'set_rect' `action` only.
    The 'get_rect' action returns the coordinates of the browser window.
    The 'set_rect' action lets you set new coordinates for the browser window.
    The 'maximize' action maximizes the current browser window.
    The 'minimize' action minimizes the current browser window.
    The Chrome DevTools Protocol (CDP) is used to change the window state.
    """
    sb = _get_sb()
    if action == "get_rect":
        return sb.get_window_rect()
    if action == "set_rect":
        if None in (x, y, width, height):
            return "Error: set_rect requires x, y, width, and height."
        sb.set_window_rect(x, y, width, height)
        return f"Window set to ({x}, {y}, {width}x{height})"
    if action == "maximize":
        sb.maximize()
        return "Window maximized."
    if action == "minimize":
        sb.minimize()
        return "Window minimized."
    return (
        f"Error: unknown action '{action}'. "
        "Use 'get_rect', 'set_rect', 'maximize', or 'minimize'."
    )


@mcp.tool()
@handle_sb_errors
def manage_tabs(
    action: Literal[
        "list",
        "open",
        "switch",
        "switch_newest",
        "close_active",
    ] = "list",
    url: str | None = None,
    tab_index: int | None = None,
    switch_to: bool = True,
) -> Any:
    """List, open, switch between, or close browser tabs.
    Args:
        action: 'list' (returns each open tab's index/url/title — call this
            before 'switch' to find the right tab_index), 'open' (a new
            tab, optionally navigating to `url`), 'switch' (to `tab_index`),
            'switch_newest', or 'close_active'.
        url: Used with action='open'.
        tab_index: Used with action='switch'; the index as returned by 'list'.
        switch_to: Used with action='open'; whether to switch to the new tab.
    Since performing browser actions (such as clicking on a link) can open new
    tabs, it is important to keep track of any new tabs opened so that you can
    switch to the new tab as needed (or close the active tab). Additionally,
    you may want to open a new tab yourself if you need to use multiple tabs
    within the same browser session. Listing tabs with the 'list' `action` is
    important so that your 'tab_index' for switching tabs is not out-of-range.
    """
    sb = _get_sb()
    if action == "list":
        tabs = sb.get_tabs()
        return [
            {
                "index": i, "url": getattr(t, "url", None),
                "title": getattr(t, "title", None)
            }
            for i, t in enumerate(tabs)
        ]
    if action == "open":
        sb.open_new_tab(url=url, switch_to=switch_to)
        return f"Opened new tab (url={url!r}, switch_to={switch_to})"
    if action == "switch":
        if tab_index is None:
            return (
                "Error: action='switch' requires tab_index "
                "(see action='list')."
            )
        tabs = sb.get_tabs()
        if tab_index < 0 or tab_index >= len(tabs):
            return (
                f"Error: tab_index={tab_index} out of range. "
                f"Available indexes: 0-{len(tabs) - 1}."
            )
        sb.switch_to_tab(tabs[tab_index])
        return f"Switched to tab {tab_index}"
    if action == "switch_newest":
        sb.switch_to_newest_tab()
        return "Switched to newest tab."
    if action == "close_active":
        sb.close_active_tab()
        return "Closed active tab."
    return (
        f"Error: unknown action '{action}'. Use 'list', 'open', 'switch', "
        f"'switch_newest', or 'close_active'."
    )


# ---------------------------------------------------------------------------
# Captcha solving
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def solve_captcha() -> str:
    """Attempt to solve a CAPTCHA (e.g. Cloudflare Turnstile) on the page.
    This tool uses the Chrome DevTools Protocol (CDP) in order to perform
    a click (with offset) in order to click the checkbox that's located
    in various CAPTCHAs such as Cloudflare Turnstile, reCAPTCHA, and the
    FriendlyCaptcha. Since this click is performed with CDP, it is much
    stealthier than JavaScript clicks that set 'isTrusted' to False.
    Since many of these CAPTCHAs are generally located inside shadow-root
    elements, it is not straightforward to determine if the click succeeded.
    Therefore, this tool will only state that it attempted to solve a
    CAPTCHA, rather than state the result. Since solving a Cloudflare
    Turnstile CAPTCHA often results in a "cf_clearance" cookie appearing
    within browser cookies, a follow-up to this tool could involve using
    the 'manage_cookies' tool to see if that "cf_clearance" cookie appeared
    after using this method to solve that CAPTCHA. To determine if there's
    a CAPTCHA on the page before using this tool, you could first use the
    'get_page_content' tool to inspect the page HTML for any CAPTCHAs."""
    _get_sb().solve_captcha()
    return "Attempted CAPTCHA solve."


# ---------------------------------------------------------------------------
# Output & misc
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def save_output(
    format: Literal["screenshot", "html", "pdf"] = "screenshot",
    filename: str | None = None,
    folder: str | None = None
) -> str:
    """Save the current page as a screenshot, HTML source, or PDF file.
    Args:
        format: 'screenshot', 'html', or 'pdf'.
        filename: Output filename. Defaults to 'screenshot.png',
            'page_source.html', or 'page.pdf' depending on `format`.
        folder: Optional folder to save into.
    If 'screenshot' format, then the page is saved as a PNG (.png) file.
    If 'html' format, then the page source is saved to an HTML (.html) file.
    If 'pdf' format, then the page is saved as a PDF (.pdf) file.
    This method is useful for creating artifacts as a result of scraping data
    from websites. This is especially important for saving results and data
    to your local machine for further processing. (For example, if this MCP
    server is being used for automated testing, then if this server finds a
    bug on a website, then it can save all the details to the local machine
    using any of this tool's supported formats: "screenshot", "html", "pdf".)
    SECURITY: `filename`/`folder` can potentially expose filesystem operations
        to an MCP client. Existing files could get overwritten during a save.
    """
    sb = _get_sb()
    if format == "screenshot":
        name = filename or "screenshot.png"
        sb.save_screenshot(name, folder=folder)
    elif format == "html":
        name = filename or "page_source.html"
        sb.save_page_source(name, folder=folder)
    elif format == "pdf":
        name = filename or "page.pdf"
        sb.save_as_pdf(name, folder=folder)
    else:
        return (
            f"Error: unknown format '{format}'. "
            "Use 'screenshot', 'html', or 'pdf'."
        )
    return f"Saved {format} as {name}"


@mcp.tool()
@handle_sb_errors
def run_javascript(expression: str) -> Any:
    """Evaluate a JavaScript expression in the page context and return the
    result. This method can run any arbitrary JavaScript on any visited site.
    JavaScript evaluation is handled by the 'Runtime.evaluate' function of the
    Chrome DevTools Protocol (CDP). When CDP's `Runtime.evaluate` function is
    called, it also sets these optional parameters: 'returnByValue' to True,
    'userGesture' to True, 'allowUnsafeEvalBlockedByCSP' to True, and
    'awaitPromise' to True. See the Chrome DevTools Protocol docs for details.
    SECURITY: This provides unrestricted JavaScript execution in the browser
    context. Only expose this MCP server to trusted clients."""
    return _get_sb().evaluate(expression)


@mcp.tool()
@handle_sb_errors
def wait_seconds(seconds: int | float) -> str:
    """Pause script execution for a duration of seconds (int or float).
    All this does is call Python `time.sleep(seconds)` in the backend.
    It is blocking behavior - no actions are performed while waiting.
    Don't use this if you need to call other tools during the wait."""
    _get_sb().sleep(seconds)
    return f"Waited {seconds}s"


@mcp.tool()
@handle_sb_errors
def get_user_agent() -> str:
    """Get the browser's current user agent string."""
    return _get_sb().get_user_agent()


def _cleanup_browser():
    global _sb
    if _sb is not None:
        try:
            _sb.quit()
        except Exception:
            pass
        _sb = None


def main():
    atexit.register(_cleanup_browser)
    print(f'Running the "{mcp.name}" server...', file=sys.stderr)
    try:
        mcp.run(transport="stdio")
    except (KeyboardInterrupt, SystemExit):
        print(f'\nThe "{mcp.name}" server was stopped.', file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
