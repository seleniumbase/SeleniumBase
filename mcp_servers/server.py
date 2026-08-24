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

Model: one persistent `sb_cdp.Chrome` session per server process. Call
start_browser once, drive it with the other tools, then close_browser.

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
from typing import Any
from mcp.server import MCPServer
from seleniumbase import sb_cdp

mcp = MCPServer("seleniumbase-mcp")

_sb: sb_cdp.CDPMethods | None = None


def _get_sb() -> sb_cdp.CDPMethods:
    if _sb is None:
        raise RuntimeError("No browser session. Call start_browser first.")
    return _sb


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
    _sb = sb_cdp.Chrome(url, **kwargs)
    return f"Started Pure CDP Mode browser (url={url!r}, headless={headless})"


@mcp.tool()
def close_browser() -> str:
    """Close the browser and end the session."""
    global _sb
    if _sb is None:
        return "No browser session was running."
    _sb.quit()
    _sb = None
    return "Browser closed."


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

@mcp.tool()
def navigate(url: str) -> str:
    """Navigate to a URL."""
    _get_sb().get(url)
    return f"Navigated to {url}"


@mcp.tool()
def reload_page(ignore_cache: bool = True) -> str:
    """Reload the current page."""
    _get_sb().reload(ignore_cache=ignore_cache)
    return "Page reloaded."


@mcp.tool()
def go_back() -> str:
    """Go back one page in browser history."""
    _get_sb().go_back()
    return "Navigated back."


@mcp.tool()
def go_forward() -> str:
    """Go forward one page in browser history."""
    _get_sb().go_forward()
    return "Navigated forward."


@mcp.tool()
def get_navigation_history() -> Any:
    """Get the browser's navigation history."""
    return _get_sb().get_navigation_history()


@mcp.tool()
def get_current_url() -> str:
    """Get the URL of the current page."""
    return _get_sb().get_current_url()


@mcp.tool()
def get_title() -> str:
    """Get the title of the current page."""
    return _get_sb().get_title()


@mcp.tool()
def get_origin() -> str:
    """Get the origin (scheme + host) of the current page."""
    return _get_sb().get_origin()


# ---------------------------------------------------------------------------
# Finding & reading
# ---------------------------------------------------------------------------

@mcp.tool()
def find_element_info(
    selector: str, best_match: bool = False, timeout: int | None = None
) -> dict:
    """Find one element and return its tag name, text, and outer HTML.

    Args:
        selector: CSS selector, or text to search for (CDP mode can match
            elements by visible text as well as by selector).
        best_match: When matching by text and multiple elements qualify,
            pick the one whose text length is closest to the search text.
        timeout: Seconds to wait for the element to appear.
    """
    el = _get_sb().find_element(
        selector, best_match=best_match, timeout=timeout
    )
    return {"tag_name": el.tag_name, "text": el.text, "html": el.get_html()}


@mcp.tool()
def find_all_info(selector: str, timeout: int | None = None) -> list[dict]:
    """Find all matching elements and return tag name + text for each."""
    els = _get_sb().find_all(selector, timeout=timeout)
    return [{"tag_name": e.tag_name, "text": e.text} for e in els]


@mcp.tool()
def get_text(selector: str = "body") -> str:
    """Get the visible text within an element (default: whole page body)."""
    return _get_sb().get_text(selector)


@mcp.tool()
def get_html_source(include_shadow_dom: bool = True) -> str:
    """Get the full HTML source of the current page."""
    return _get_sb().get_page_source(include_shadow_dom=include_shadow_dom)


@mcp.tool()
def get_element_html(selector: str) -> str:
    """Get the outer HTML of a specific element."""
    return _get_sb().get_element_html(selector)


@mcp.tool()
def get_element_attribute(selector: str, attribute: str) -> Any:
    """Get one attribute's value from an element."""
    return _get_sb().get_element_attribute(selector, attribute)


@mcp.tool()
def get_element_attributes(selector: str) -> dict:
    """Get all attributes of an element as a dict."""
    return _get_sb().get_element_attributes(selector)


@mcp.tool()
def find_elements_count(selector: str, timeout: int | None = None) -> int:
    """Count how many elements on the page match a selector."""
    return len(_get_sb().find_elements(selector, timeout=timeout))


@mcp.tool()
def is_element_present(selector: str) -> bool:
    """Check whether an element matching a selector exists in the DOM."""
    return _get_sb().is_element_present(selector)


@mcp.tool()
def is_element_visible(selector: str) -> bool:
    """Check whether an element matching a selector is visible."""
    return _get_sb().is_element_visible(selector)


@mcp.tool()
def is_text_visible(text: str, selector: str = "body") -> bool:
    """Check whether specific text is visible within an element."""
    return _get_sb().is_text_visible(text, selector)


@mcp.tool()
def get_all_urls(absolute: bool = True) -> list[str]:
    """Get all linked URLs (a, link, img, script, meta) on the page."""
    return _get_sb().get_all_urls(absolute=absolute)


# ---------------------------------------------------------------------------
# Interacting with elements
# ---------------------------------------------------------------------------

@mcp.tool()
def click(
    selector: str, timeout: int | None = None, scroll: bool = True
) -> str:
    """Click an element matched by a CSS selector (or by text, e.g.
    'a:contains("Sign in")')."""
    _get_sb().click(selector, timeout=timeout, scroll=scroll)
    return f"Clicked {selector}"


@mcp.tool()
def click_if_visible(selector: str, timeout: int = 0) -> str:
    """Click an element only if it's currently visible; no-op otherwise."""
    _get_sb().click_if_visible(selector, timeout=timeout)
    return f"click_if_visible ran for {selector}"


@mcp.tool()
def click_visible_elements(selector: str, limit: int = 0) -> str:
    """Click every currently-visible element matching a selector, in order
    (e.g. checking every checkbox on a page). limit=0 means no limit."""
    _get_sb().click_visible_elements(selector, limit=limit)
    return f"Clicked visible elements matching {selector}"


@mcp.tool()
def click_nth_element(selector: str, number: int) -> str:
    """Click the Nth element (1-indexed) matching a selector."""
    _get_sb().click_nth_element(selector, number)
    return f"Clicked element #{number} matching {selector}"


@mcp.tool()
def click_link(link_text: str) -> str:
    """Click a link (<a> tag) by its visible text."""
    _get_sb().click_link(link_text)
    return f"Clicked link with text '{link_text}'"


@mcp.tool()
def type_text(selector: str, text: str, timeout: int | None = None) -> str:
    """Clear a field and type text into it."""
    _get_sb().type(selector, text, timeout=timeout)
    return f"Typed into {selector}"


@mcp.tool()
def send_keys(selector: str, text: str, timeout: int | None = None) -> str:
    """Send keystrokes to an element without clearing it first."""
    _get_sb().send_keys(selector, text, timeout=timeout)
    return f"Sent keys to {selector}"


@mcp.tool()
def set_value(selector: str, text: str, timeout: int | None = None) -> str:
    """Set an input's value directly (e.g. for sliders, fast form fills)."""
    _get_sb().set_value(selector, text, timeout=timeout)
    return f"Set value of {selector}"


@mcp.tool()
def clear_input(selector: str, timeout: int | None = None) -> str:
    """Clear an input field."""
    _get_sb().clear_input(selector, timeout=timeout)
    return f"Cleared {selector}"


@mcp.tool()
def submit(selector: str) -> str:
    """Submit a form via a selector inside it."""
    _get_sb().submit(selector)
    return f"Submitted form via {selector}"


@mcp.tool()
def select_option_by_text(dropdown_selector: str, option_text: str) -> str:
    """Select a <select> dropdown option by its visible text."""
    _get_sb().select_option_by_text(dropdown_selector, option_text)
    return f"Selected '{option_text}' in {dropdown_selector}"


@mcp.tool()
def select_option_by_value(dropdown_selector: str, value: str) -> str:
    """Select a <select> dropdown option by its value attribute."""
    _get_sb().select_option_by_value(dropdown_selector, value)
    return f"Selected value '{value}' in {dropdown_selector}"


@mcp.tool()
def select_option_by_index(dropdown_selector: str, index: int) -> str:
    """Select a <select> dropdown option by its 0-based index."""
    _get_sb().select_option_by_index(dropdown_selector, index)
    return f"Selected index {index} in {dropdown_selector}"


@mcp.tool()
def focus(selector: str) -> str:
    """Move focus to an element."""
    el = _get_sb().find_element(selector)
    el.focus()
    return f"Focused {selector}"


@mcp.tool()
def highlight(selector: str) -> str:
    """Briefly highlight an element (useful when narrating actions on
    a visible/headed browser)."""
    _get_sb().highlight(selector)
    return f"Highlighted {selector}"


@mcp.tool()
def nested_click(parent_selector: str, selector: str) -> str:
    """Click an element nested inside another (e.g. inside an iframe)."""
    _get_sb().nested_click(parent_selector, selector)
    return f"Clicked {selector} inside {parent_selector}"


# ---------------------------------------------------------------------------
# Waiting
# ---------------------------------------------------------------------------

@mcp.tool()
def wait_for_element(selector: str, timeout: int | None = None) -> str:
    """Wait until an element is present in the DOM."""
    _get_sb().wait_for_element(selector, timeout=timeout)
    return f"Element {selector} is present."


@mcp.tool()
def wait_for_element_visible(selector: str, timeout: int | None = None) -> str:
    """Wait until an element is visible."""
    _get_sb().wait_for_element_visible(selector, timeout=timeout)
    return f"Element {selector} is visible."


@mcp.tool()
def wait_for_element_not_visible(
    selector: str, timeout: int | None = None
) -> str:
    """Wait until an element is no longer visible."""
    _get_sb().wait_for_element_not_visible(selector, timeout=timeout)
    return f"Element {selector} is no longer visible."


@mcp.tool()
def wait_for_element_absent(selector: str, timeout: int | None = None) -> str:
    """Wait until an element is removed from the DOM."""
    _get_sb().wait_for_element_absent(selector, timeout=timeout)
    return f"Element {selector} is now absent."


@mcp.tool()
def wait_for_text(
    text: str, selector: str = "body", timeout: int | None = None
) -> str:
    """Wait until specific text appears within an element."""
    _get_sb().wait_for_text(text, selector, timeout=timeout)
    return f"Text '{text}' appeared in {selector}."


# ---------------------------------------------------------------------------
# Assertions (raise an error, surfaced to the MCP client, if they fail)
# ---------------------------------------------------------------------------

@mcp.tool()
def assert_element(selector: str, timeout: int | None = None) -> str:
    """Assert an element is present in the DOM."""
    _get_sb().assert_element(selector, timeout=timeout)
    return f"Confirmed {selector} is present."


@mcp.tool()
def assert_element_visible(selector: str, timeout: int | None = None) -> str:
    """Assert an element is visible."""
    _get_sb().assert_element_visible(selector, timeout=timeout)
    return f"Confirmed {selector} is visible."


@mcp.tool()
def assert_text(
    text: str, selector: str = "html", timeout: int | None = None
) -> str:
    """Assert text is present within an element."""
    _get_sb().assert_text(text, selector, timeout=timeout)
    return f"Confirmed '{text}' is present in {selector}."


@mcp.tool()
def assert_exact_text(
    text: str, selector: str = "html", timeout: int | None = None
) -> str:
    """Assert an element's text matches exactly."""
    _get_sb().assert_exact_text(text, selector, timeout=timeout)
    return f"Confirmed {selector} text is exactly '{text}'."


@mcp.tool()
def assert_title(title: str) -> str:
    """Assert the page title matches exactly."""
    _get_sb().assert_title(title)
    return f"Confirmed title is '{title}'."


@mcp.tool()
def assert_url(url: str) -> str:
    """Assert the current URL matches exactly."""
    _get_sb().assert_url(url)
    return f"Confirmed URL is '{url}'."


@mcp.tool()
def assert_url_contains(substring: str) -> str:
    """Assert the current URL contains a substring."""
    _get_sb().assert_url_contains(substring)
    return f"Confirmed URL contains '{substring}'."


# ---------------------------------------------------------------------------
# Cookies & storage
# ---------------------------------------------------------------------------

@mcp.tool()
def get_all_cookies() -> Any:
    """Get all cookies for the current session."""
    return _get_sb().get_all_cookies()


@mcp.tool()
def clear_cookies() -> str:
    """Clear all cookies."""
    _get_sb().clear_cookies()
    return "Cookies cleared."


@mcp.tool()
def save_cookies(name: str = "cookies.txt") -> str:
    """Save current cookies to a file."""
    _get_sb().save_cookies(name=name)
    return f"Cookies saved to {name}"


@mcp.tool()
def load_cookies(name: str = "cookies.txt") -> str:
    """Load cookies from a previously saved file."""
    _get_sb().load_cookies(name=name)
    return f"Cookies loaded from {name}"


@mcp.tool()
def get_local_storage_item(key: str) -> Any:
    """Get a value from the page's localStorage."""
    return _get_sb().get_local_storage_item(key)


@mcp.tool()
def set_local_storage_item(key: str, value: str) -> str:
    """Set a value in the page's localStorage."""
    _get_sb().set_local_storage_item(key, value)
    return f"Set localStorage[{key!r}]"


@mcp.tool()
def get_session_storage_item(key: str) -> Any:
    """Get a value from the page's sessionStorage."""
    return _get_sb().get_session_storage_item(key)


@mcp.tool()
def set_session_storage_item(key: str, value: str) -> str:
    """Set a value in the page's sessionStorage."""
    _get_sb().set_session_storage_item(key, value)
    return f"Set sessionStorage[{key!r}]"


# ---------------------------------------------------------------------------
# Scrolling
# ---------------------------------------------------------------------------

@mcp.tool()
def scroll_into_view(selector: str) -> str:
    """Scroll an element into view."""
    _get_sb().scroll_into_view(selector)
    return f"Scrolled {selector} into view."


@mcp.tool()
def scroll_to_top() -> str:
    """Scroll to the top of the page."""
    _get_sb().scroll_to_top()
    return "Scrolled to top."


@mcp.tool()
def scroll_to_bottom() -> str:
    """Scroll to the bottom of the page."""
    _get_sb().scroll_to_bottom()
    return "Scrolled to bottom."


@mcp.tool()
def scroll_up(amount: int = 25) -> str:
    """Scroll up by a relative amount."""
    _get_sb().scroll_up(amount=amount)
    return f"Scrolled up {amount}."


@mcp.tool()
def scroll_down(amount: int = 25) -> str:
    """Scroll down by a relative amount."""
    _get_sb().scroll_down(amount=amount)
    return f"Scrolled down {amount}."


# ---------------------------------------------------------------------------
# Windows & tabs
# ---------------------------------------------------------------------------

@mcp.tool()
def get_window_rect() -> dict:
    """Get the current window's position and size."""
    return _get_sb().get_window_rect()


@mcp.tool()
def set_window_rect(x: int, y: int, width: int, height: int) -> str:
    """Set the current window's position and size."""
    _get_sb().set_window_rect(x, y, width, height)
    return f"Window set to ({x}, {y}, {width}x{height})"


@mcp.tool()
def maximize() -> str:
    """Maximize the browser window."""
    _get_sb().maximize()
    return "Window maximized."


@mcp.tool()
def minimize() -> str:
    """Minimize the browser window."""
    _get_sb().minimize()
    return "Window minimized."


@mcp.tool()
def open_new_tab(url: str | None = None, switch_to: bool = True) -> str:
    """Open a new browser tab, optionally navigating and switching to it."""
    _get_sb().open_new_tab(url=url, switch_to=switch_to)
    return f"Opened new tab (url={url!r}, switch_to={switch_to})"


@mcp.tool()
def switch_to_tab(tab_index: int) -> str:
    """Switch to a tab by its index (as returned by get_tabs)."""
    tabs = _get_sb().get_tabs()
    _get_sb().switch_to_tab(tabs[tab_index])
    return f"Switched to tab {tab_index}"


@mcp.tool()
def switch_to_newest_tab() -> str:
    """Switch to the most recently opened tab."""
    _get_sb().switch_to_newest_tab()
    return "Switched to newest tab."


@mcp.tool()
def close_active_tab() -> str:
    """Close the currently active tab."""
    _get_sb().close_active_tab()
    return "Closed active tab."


@mcp.tool()
def get_tabs_count() -> int:
    """Get how many tabs are currently open."""
    return len(_get_sb().get_tabs())


# ---------------------------------------------------------------------------
# Captcha solving
# ---------------------------------------------------------------------------

@mcp.tool()
def solve_captcha() -> str:
    """Attempt to solve a captcha (e.g. Cloudflare Turnstile) on the page."""
    _get_sb().solve_captcha()
    return "Attempted captcha solve."


# ---------------------------------------------------------------------------
# Output & misc
# ---------------------------------------------------------------------------

@mcp.tool()
def save_screenshot(
    name: str = "screenshot.png", folder: str | None = None
) -> str:
    """Save a screenshot of the current page."""
    _get_sb().save_screenshot(name, folder=folder)
    return f"Screenshot saved as {name}"


@mcp.tool()
def save_page_source(
    name: str = "page_source.html", folder: str | None = None
) -> str:
    """Save the current page's HTML source to a file."""
    _get_sb().save_page_source(name, folder=folder)
    return f"Page source saved as {name}"


@mcp.tool()
def save_as_pdf(name: str = "page.pdf", folder: str | None = None) -> str:
    """Print the current page to a PDF file."""
    _get_sb().save_as_pdf(name, folder=folder)
    return f"Page saved as PDF: {name}"


@mcp.tool()
def evaluate(expression: str) -> Any:
    """Evaluate a JavaScript expression in the page context and return the
    result. Equivalent to execute_script."""
    return _get_sb().evaluate(expression)


@mcp.tool()
def sleep(seconds: float) -> str:
    """Pause execution for a number of seconds."""
    _get_sb().sleep(seconds)
    return f"Slept {seconds}s"


@mcp.tool()
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
