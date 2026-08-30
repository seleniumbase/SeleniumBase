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

Note on elements: CDP-mode element objects (from find_element/find_all) are
live handles with their own methods (.click(), .get_html(), ...) that can't
cross the MCP boundary as stateful objects. Tools here resolve an element
immediately to a plain dict (tag, text, html) rather than returning a handle.
If you need to act on a *specific* one of several matching elements, use
click_nth_element / click_nth_visible_element rather than find + click.
"""
from __future__ import annotations
import atexit
import sys
from functools import wraps
from typing import Any
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
    incognito: bool = False,
    guest: bool = False,
    proxy: str | None = None,
    ad_block: bool = False,
) -> str:
    """Launch a Pure CDP Mode browser session. Must be called before any
    other tool. The browser is driven entirely over CDP (no WebDriver),
    which is SeleniumBase's most stealth/bot-detection-resistant mode.
    Args:
        url: Optional URL to open immediately on launch.
        headless: Run without a visible window.
        incognito: Launch in a private/incognito window.
        guest: Launch in Chrome guest mode.
        proxy: Proxy string, e.g. "USER:PASS@SERVER:PORT" or "SERVER:PORT".
        ad_block: Block ads.
    """
    global _sb
    if _sb is not None:
        return (
            "A browser session is already running. Call close_browser first."
        )
    kwargs: dict[str, Any] = {"headless": headless}
    if incognito:
        kwargs["incognito"] = True
    if guest:
        kwargs["guest"] = True
    if proxy:
        kwargs["proxy"] = proxy
    if ad_block:
        kwargs["ad_block"] = True
    try:
        _sb = sb_cdp.Chrome(url, **kwargs)
        return (
            f"Started Pure CDP Mode browser "
            f"(url={url!r}, headless={headless})"
        )
    except Exception as e:
        return (
            f"Error starting browser: "
            f"{e.__class__.__name__} - {str(e).strip()}"
        )


@mcp.tool()
def close_browser() -> str:
    """Close the browser and end the session."""
    global _sb
    if _sb is None:
        return "No browser session was running."
    try:
        _sb.quit()
    except Exception:
        pass
    _sb = None
    return "Browser closed."


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def navigate(url: str) -> str:
    """Navigate to the given URL in the web browser.
    If the URL doesn't start with a protocol (eg: `https://`),
      then `https://` is automatically prefixed in before navigation.
    Waits until the initial HTML document is fully parsed and loaded.
    New pages visited will show up in browser navigation history.
    If the URL is invalid or the page can't load due to an issue,
      then the corresponding errors will be raised."""
    _get_sb().get(url)
    return f"Navigated to {url}"


@mcp.tool()
@handle_sb_errors
def reload_page(ignore_cache: bool = True) -> str:
    """Reload the current page.
    Same as clicking the Reload button in the web browser.
    By default, ignores the browser cache on reload."""
    _get_sb().reload(ignore_cache=ignore_cache)
    return "Page reloaded."


@mcp.tool()
@handle_sb_errors
def go_back() -> str:
    """Go back one page in browser history.
    Same as clicking the Back button in the web browser."""
    _get_sb().go_back()
    return "Navigated back."


@mcp.tool()
@handle_sb_errors
def go_forward() -> str:
    """Go forward one page in browser history.
    Same as clicking the Forward button in the web browser."""
    _get_sb().go_forward()
    return "Navigated forward."


@mcp.tool()
@handle_sb_errors
def get_navigation_history() -> Any:
    """Get the browser's navigation history."""
    return _get_sb().get_navigation_history()


@mcp.tool()
@handle_sb_errors
def get_current_url() -> str:
    """Get the URL of the current page."""
    return _get_sb().get_current_url()


@mcp.tool()
@handle_sb_errors
def get_title() -> str:
    """Get the title of the current page."""
    return _get_sb().get_title()


@mcp.tool()
@handle_sb_errors
def get_origin() -> str:
    """Get the origin (scheme + host) of the current page."""
    return _get_sb().get_origin()


# ---------------------------------------------------------------------------
# Finding & reading
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def find_element_info(
    selector: str, best_match: bool = False, timeout: int | None = None
) -> dict | str:
    """Find one element and return its tag name, text, and outer HTML.
    Args:
        selector: CSS selector, or text to search for (CDP mode can match
            elements by visible text as well as by selector).
        best_match: When matching by text and multiple elements qualify,
            pick the one whose text length is closest to the search text.
        timeout: Seconds to wait for the element to appear."""
    el = _get_sb().find_element(
        selector, best_match=best_match, timeout=timeout
    )
    return {"tag_name": el.tag_name, "text": el.text, "html": el.get_html()}


@mcp.tool()
@handle_sb_errors
def find_all_info(
    selector: str, timeout: int | None = None
) -> list[dict] | str:
    """Find all matching elements and return tag name + text for each."""
    els = _get_sb().find_all(selector, timeout=timeout)
    return [{"tag_name": e.tag_name, "text": e.text} for e in els]


@mcp.tool()
@handle_sb_errors
def get_text(selector: str = "body") -> str:
    """Get the visible text within an element (default: whole page body).
    Raises an exception if the element isn't found within the default timeout.
    """
    return _get_sb().get_text(selector)


@mcp.tool()
@handle_sb_errors
def get_html_source(include_shadow_dom: bool = True) -> str:
    """Get the full HTML source of the current page."""
    return _get_sb().get_page_source(include_shadow_dom=include_shadow_dom)


@mcp.tool()
@handle_sb_errors
def get_element_html(selector: str) -> str:
    """Get the outer HTML of a specific element."""
    return _get_sb().get_element_html(selector)


@mcp.tool()
@handle_sb_errors
def get_element_attribute(selector: str, attribute: str) -> Any:
    """Get one attribute's value from an element."""
    return _get_sb().get_element_attribute(selector, attribute)


@mcp.tool()
@handle_sb_errors
def get_element_attributes(selector: str) -> dict | str:
    """Get all attributes of an element as a dict."""
    return _get_sb().get_element_attributes(selector)


@mcp.tool()
@handle_sb_errors
def find_elements_count(
    selector: str, timeout: int | None = None
) -> int | str:
    """Get the count of how many elements on the page match the selector."""
    return len(_get_sb().find_elements(selector, timeout=timeout))


@mcp.tool()
@handle_sb_errors
def is_element_present(selector: str) -> bool | str:
    """Return whether an element matching the selector exists in the DOM."""
    return _get_sb().is_element_present(selector)


@mcp.tool()
@handle_sb_errors
def is_element_visible(selector: str) -> bool | str:
    """Return whether an element matching the selector is visible."""
    return _get_sb().is_element_visible(selector)


@mcp.tool()
@handle_sb_errors
def is_text_visible(text: str, selector: str = "body") -> bool | str:
    """Return whether the specific text is visible within an element."""
    return _get_sb().is_text_visible(text, selector)


@mcp.tool()
@handle_sb_errors
def get_all_urls(absolute: bool = True) -> list[str] | str:
    """Get all linked URLs (a, link, img, script, meta) on the page."""
    return _get_sb().get_all_urls(absolute=absolute)


# ---------------------------------------------------------------------------
# Interacting with elements
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def click(
    selector: str, timeout: int | None = None, scroll: bool = True
) -> str:
    """Click an element matched by a CSS selector (or by text, e.g.
    'a:contains("Sign in")').
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout."""
    _get_sb().click(selector, timeout=timeout, scroll=scroll)
    return f"Clicked {selector}"


@mcp.tool()
@handle_sb_errors
def click_if_visible(selector: str, timeout: int = 0) -> str:
    """Click an element only if it's currently visible; no-op otherwise.
    If a `timeout` is given, then waits up to that long for the element
      to appear first before performing the click."""
    _get_sb().click_if_visible(selector, timeout=timeout)
    return f"click_if_visible ran for {selector}"


@mcp.tool()
@handle_sb_errors
def click_visible_elements(selector: str, limit: int = 0) -> str:
    """Click every currently-visible element matching a selector, in order
    (e.g. checking every checkbox on a page). limit=0 means no limit."""
    _get_sb().click_visible_elements(selector, limit=limit)
    return f"Clicked visible elements matching {selector}"


@mcp.tool()
@handle_sb_errors
def click_nth_element(selector: str, number: int) -> str:
    """Click the Nth element (1-indexed) matching a selector."""
    _get_sb().click_nth_element(selector, number)
    return f"Clicked element #{number} matching {selector}"


@mcp.tool()
@handle_sb_errors
def click_link(link_text: str) -> str:
    """Click a link (<a> tag) by its visible text."""
    _get_sb().click_link(link_text)
    return f"Clicked link with text '{link_text}'"


@mcp.tool()
@handle_sb_errors
def type_text(selector: str, text: str, timeout: int | None = None) -> str:
    """Clear a field and type text into it.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout."""
    _get_sb().type(selector, text, timeout=timeout)
    return f"Typed into {selector}"


@mcp.tool()
@handle_sb_errors
def send_keys(selector: str, text: str, timeout: int | None = None) -> str:
    """Send keystrokes to an element without clearing it first.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout."""
    _get_sb().send_keys(selector, text, timeout=timeout)
    return f"Sent keys to {selector}"


@mcp.tool()
@handle_sb_errors
def set_value(selector: str, text: str, timeout: int | None = None) -> str:
    """Set an input's value directly (e.g. for sliders, fast form fills).
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout."""
    _get_sb().set_value(selector, text, timeout=timeout)
    return f"Set value of {selector}"


@mcp.tool()
@handle_sb_errors
def clear_input(selector: str, timeout: int | None = None) -> str:
    """Clear an input field.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout. """
    _get_sb().clear_input(selector, timeout=timeout)
    return f"Cleared {selector}"


@mcp.tool()
@handle_sb_errors
def submit(selector: str) -> str:
    """Submit a form via a selector inside it."""
    _get_sb().submit(selector)
    return f"Submitted form via {selector}"


@mcp.tool()
@handle_sb_errors
def select_option_by_text(dropdown_selector: str, option: str) -> str:
    """Select a <select> dropdown option by its visible text.
    Raises an exception if the element or option aren't found
      within the default timeout, which is 7 seconds."""
    _get_sb().select_option_by_text(dropdown_selector, option)
    return f"Selected text '{option}' in {dropdown_selector}"


@mcp.tool()
@handle_sb_errors
def select_option_by_value(dropdown_selector: str, option: str) -> str:
    """Select a <select> dropdown option by its value attribute.
    Raises an exception if the element or option aren't found
      within the default timeout, which is 7 seconds."""
    _get_sb().select_option_by_value(dropdown_selector, option)
    return f"Selected value '{option}' in {dropdown_selector}"


@mcp.tool()
@handle_sb_errors
def select_option_by_index(dropdown_selector: str, option: int) -> str:
    """Select a <select> dropdown option by its 0-based index.
    Raises an exception if the element or option aren't found
      within the default timeout, which is 7 seconds."""
    _get_sb().select_option_by_index(dropdown_selector, option)
    return f"Selected index {option} in {dropdown_selector}"


@mcp.tool()
@handle_sb_errors
def focus(selector: str) -> str:
    """Move focus to an element.
    Raises an exception if the element isn't found within the default timeout.
    """
    el = _get_sb().find_element(selector)
    el.focus()
    return f"Focused {selector}"


@mcp.tool()
@handle_sb_errors
def highlight(selector: str) -> str:
    """Briefly highlight an element (useful when narrating actions on
    a visible/headed browser).
    Raises an exception if the element isn't found within the default timeout.
    """
    _get_sb().highlight(selector)
    return f"Highlighted {selector}"


@mcp.tool()
@handle_sb_errors
def nested_click(parent_selector: str, selector: str) -> str:
    """Click an element nested inside another (e.g. inside an iframe).
    Raises an exception if the element isn't found within the default timeout.
    """
    _get_sb().nested_click(parent_selector, selector)
    return f"Clicked {selector} inside {parent_selector}"


# ---------------------------------------------------------------------------
# Waiting
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def wait_for_element_present(selector: str, timeout: int | None = None) -> str:
    """Wait until the element is present in the DOM.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout."""
    _get_sb().wait_for_element_present(selector, timeout=timeout)
    return f"Element {selector} is present."


@mcp.tool()
@handle_sb_errors
def wait_for_element_visible(selector: str, timeout: int | None = None) -> str:
    """Wait until the element is visible on the page.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't visible within the timeout."""
    _get_sb().wait_for_element_visible(selector, timeout=timeout)
    return f"Element {selector} is visible."


@mcp.tool()
@handle_sb_errors
def wait_for_element_not_visible(
    selector: str, timeout: int | None = None
) -> str:
    """Wait until an element is no longer visible on the page.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element is still visible after the timeout."""
    _get_sb().wait_for_element_not_visible(selector, timeout=timeout)
    return f"Element {selector} is no longer visible."


@mcp.tool()
@handle_sb_errors
def wait_for_element_absent(selector: str, timeout: int | None = None) -> str:
    """Wait until an element is removed from the DOM.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element is still present after the timeout."""
    _get_sb().wait_for_element_absent(selector, timeout=timeout)
    return f"Element {selector} is now absent."


@mcp.tool()
@handle_sb_errors
def wait_for_text(
    text: str, selector: str = "body", timeout: int | None = None
) -> str:
    """Wait until the text substring appears within an element.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't visible within the timeout."""
    _get_sb().wait_for_text(text, selector, timeout=timeout)
    return f"Text '{text}' appeared in {selector}."


# ---------------------------------------------------------------------------
# Assertions (raise an error, surfaced to the MCP client, if they fail)
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def assert_element(selector: str, timeout: int | None = None) -> str:
    """Assert that an element is present in the DOM.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout."""
    _get_sb().assert_element(selector, timeout=timeout)
    return f"Confirmed {selector} is present."


@mcp.tool()
@handle_sb_errors
def assert_element_visible(selector: str, timeout: int | None = None) -> str:
    """Assert that an element is visible on the page.
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found within the timeout."""
    _get_sb().assert_element_visible(selector, timeout=timeout)
    return f"Confirmed {selector} is visible."


@mcp.tool()
@handle_sb_errors
def assert_text(
    text: str, selector: str = "html", timeout: int | None = None
) -> str:
    """Assert that the text substring appears within the given element
      (with the matching selector) in the given timeout (seconds),
      with leading and trailing whitespace automatically ignored.
    If no `selector` given, then it defaults to "html" (CSS selector).
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found or assertion fails."""
    _get_sb().assert_text(text, selector, timeout=timeout)
    return f"Confirmed '{text}' is present in {selector}."


@mcp.tool()
@handle_sb_errors
def assert_exact_text(
    text: str, selector: str = "html", timeout: int | None = None
) -> str:
    """Assert that the text matches the element's text exactly
      (with leading/trailing whitespace automatically ignored)
      in the given timeout (seconds).
    If no `selector` given, then it defaults to "html" (CSS selector).
    If no `timeout` given (0 or None), then SeleniumBase uses 7 seconds.
    Raises an exception if the element isn't found or assertion fails."""
    _get_sb().assert_exact_text(text, selector, timeout=timeout)
    return f"Confirmed {selector} text is exactly '{text}'."


@mcp.tool()
@handle_sb_errors
def assert_title(title: str) -> str:
    """Assert that the title matches the page title exactly,
      with leading and trailing whitespace ignored.
    Raises an exception if the expected title doesn't
      match the actual title within 7 seconds."""
    _get_sb().assert_title(title)
    return f"Confirmed title is '{title}'."


@mcp.tool()
@handle_sb_errors
def assert_url(url: str) -> str:
    """Assert that the url matches the current URL exactly.
    Raises an exception if the expected url doesn't
      match the actual url within 7 seconds."""
    _get_sb().assert_url(url)
    return f"Confirmed URL is '{url}'."


@mcp.tool()
@handle_sb_errors
def assert_url_contains(substring: str) -> str:
    """Assert that the current URL contains the given substring.
    Raises an exception if the expected substring isn't
      found in the actual url within 7 seconds."""
    _get_sb().assert_url_contains(substring)
    return f"Confirmed URL contains '{substring}'."


# ---------------------------------------------------------------------------
# Cookies & storage
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def get_all_cookies() -> Any:
    """Get all cookies for the current session."""
    return _get_sb().get_all_cookies()


@mcp.tool()
@handle_sb_errors
def clear_cookies() -> str:
    """Clear all cookies."""
    _get_sb().clear_cookies()
    return "Cookies cleared."


@mcp.tool()
@handle_sb_errors
def save_cookies(name: str = "cookies.txt") -> str:
    """Save current cookies to a file."""
    _get_sb().save_cookies(name=name)
    return f"Cookies saved to {name}"


@mcp.tool()
@handle_sb_errors
def load_cookies(name: str = "cookies.txt") -> str:
    """Load cookies from a previously saved file."""
    _get_sb().load_cookies(name=name)
    return f"Cookies loaded from {name}"


@mcp.tool()
@handle_sb_errors
def get_local_storage_item(key: str) -> Any:
    """Get a value from the page's localStorage."""
    return _get_sb().get_local_storage_item(key)


@mcp.tool()
@handle_sb_errors
def set_local_storage_item(key: str, value: str) -> str:
    """Set a value in the page's localStorage."""
    _get_sb().set_local_storage_item(key, value)
    return f"Set localStorage[{key!r}]"


@mcp.tool()
@handle_sb_errors
def get_session_storage_item(key: str) -> Any:
    """Get a value from the page's sessionStorage."""
    return _get_sb().get_session_storage_item(key)


@mcp.tool()
@handle_sb_errors
def set_session_storage_item(key: str, value: str) -> str:
    """Set a value in the page's sessionStorage."""
    _get_sb().set_session_storage_item(key, value)
    return f"Set sessionStorage[{key!r}]"


# ---------------------------------------------------------------------------
# Scrolling
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def scroll_into_view(selector: str) -> str:
    """Scroll an element into view."""
    _get_sb().scroll_into_view(selector)
    return f"Scrolled {selector} into view."


@mcp.tool()
@handle_sb_errors
def scroll_to_top() -> str:
    """Scroll to the top of the page."""
    _get_sb().scroll_to_top()
    return "Scrolled to top."


@mcp.tool()
@handle_sb_errors
def scroll_to_bottom() -> str:
    """Scroll to the bottom of the page."""
    _get_sb().scroll_to_bottom()
    return "Scrolled to bottom."


@mcp.tool()
@handle_sb_errors
def scroll_up(amount: int = 25) -> str:
    """Scroll up by a relative amount."""
    _get_sb().scroll_up(amount=amount)
    return f"Scrolled up {amount}."


@mcp.tool()
@handle_sb_errors
def scroll_down(amount: int = 25) -> str:
    """Scroll down by a relative amount."""
    _get_sb().scroll_down(amount=amount)
    return f"Scrolled down {amount}."


# ---------------------------------------------------------------------------
# Windows & tabs
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def get_window_rect() -> dict | str:
    """Get the current window's position and size."""
    return _get_sb().get_window_rect()


@mcp.tool()
@handle_sb_errors
def set_window_rect(x: int, y: int, width: int, height: int) -> str:
    """Set the current window's position and size."""
    _get_sb().set_window_rect(x, y, width, height)
    return f"Window set to ({x}, {y}, {width}x{height})"


@mcp.tool()
@handle_sb_errors
def maximize() -> str:
    """Maximize the browser window."""
    _get_sb().maximize()
    return "Window maximized."


@mcp.tool()
@handle_sb_errors
def minimize() -> str:
    """Minimize the browser window."""
    _get_sb().minimize()
    return "Window minimized."


@mcp.tool()
@handle_sb_errors
def open_new_tab(url: str | None = None, switch_to: bool = True) -> str:
    """Open a new browser tab, optionally navigating and switching to it."""
    _get_sb().open_new_tab(url=url, switch_to=switch_to)
    return f"Opened new tab (url={url!r}, switch_to={switch_to})"


@mcp.tool()
@handle_sb_errors
def switch_to_tab(tab_index: int) -> str:
    """Switch to a tab by its index (as returned by get_tabs)."""
    tabs = _get_sb().get_tabs()
    _get_sb().switch_to_tab(tabs[tab_index])
    return f"Switched to tab {tab_index}"


@mcp.tool()
@handle_sb_errors
def switch_to_newest_tab() -> str:
    """Switch to the most recently opened tab."""
    _get_sb().switch_to_newest_tab()
    return "Switched to newest tab."


@mcp.tool()
@handle_sb_errors
def close_active_tab() -> str:
    """Close the currently active tab."""
    _get_sb().close_active_tab()
    return "Closed active tab."


@mcp.tool()
@handle_sb_errors
def get_tabs_count() -> int | str:
    """Get how many tabs are currently open."""
    return len(_get_sb().get_tabs())


# ---------------------------------------------------------------------------
# Captcha solving
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def solve_captcha() -> str:
    """Attempt to solve a captcha (e.g. Cloudflare Turnstile) on the page."""
    _get_sb().solve_captcha()
    return "Attempted captcha solve."


# ---------------------------------------------------------------------------
# Output & misc
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def save_screenshot(
    name: str = "screenshot.png", folder: str | None = None
) -> str:
    """Save a screenshot of the current page."""
    _get_sb().save_screenshot(name, folder=folder)
    return f"Screenshot saved as {name}"


@mcp.tool()
@handle_sb_errors
def save_page_source(
    name: str = "page_source.html", folder: str | None = None
) -> str:
    """Save the current page's HTML source to a file."""
    _get_sb().save_page_source(name, folder=folder)
    return f"Page source saved as {name}"


@mcp.tool()
@handle_sb_errors
def save_as_pdf(name: str = "page.pdf", folder: str | None = None) -> str:
    """Print the current page to a PDF file."""
    _get_sb().save_as_pdf(name, folder=folder)
    return f"Page saved as PDF: {name}"


@mcp.tool()
@handle_sb_errors
def evaluate(expression: str) -> Any:
    """Evaluate a JavaScript expression in the page context and return the
    result. Equivalent to execute_script. This method can run any arbitrary
    JavaScript on any site, so take any necessary precautions to prevent
    AI harnesses from running scripts that you don't want them to run."""
    return _get_sb().evaluate(expression)


@mcp.tool()
@handle_sb_errors
def sleep(seconds: float) -> str:
    """Pause execution for a number of seconds."""
    _get_sb().sleep(seconds)
    return f"Slept {seconds}s"


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
