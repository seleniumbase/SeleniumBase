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

Design notes:
Tools follow a consistent CSS-selector-or-text matching convention:
selector arguments accept a CSS selector or visible text (for example,
a:contains("Sign in")). Related SeleniumBase capabilities are consolidated
into parameterized tools using action, mode, state, or check parameters.
This keeps the toolset compact and predictable while giving an MCP client
access to the underlying browser-automation capabilities without
having to choose between multiple near-identical tools.

Tool-selection philosophy:
- Use get_page_info for browser/page metadata such as URL, title, origin,
  and navigation history.
- Use get_content for reading visible text or HTML.
- Use find_elements for discovering and inspecting multiple matching
  elements as structured data.
- Use check_state for an immediate, non-waiting state check.
- Use wait_for when the agent needs to wait for a condition to become true.
- Use assert_that when the agent needs to verify an expected condition and
  treat failure as an assertion error.
- Use click/fill_input/select_option/hover/act_on_element for interactions.

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
    """Return the active browser session or raise a useful lifecycle error."""
    if _sb is None:
        raise RuntimeError("No browser session. Call start_browser first.")
    return _sb


def handle_sb_errors(func):
    """Convert SeleniumBase/runtime exceptions into descriptive MCP results.

    Browser automation failures are returned as readable error strings so
    an MCP client/LLM can inspect the error and decide whether to retry,
    change a selector, wait for a condition, navigate elsewhere, or take
    another corrective action.
    """
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
    headless: bool | None = None,
    use_chromium: bool = False,
    browser_executable_path: str | None = None,
    incognito: bool = False,
    guest: bool = False,
    ad_block: bool = False,
    proxy: str | None = None,
) -> str:
    """Launch a persistent SeleniumBase Pure CDP Mode browser session.

    This must be called before browser interaction tools such as navigate,
    get_content, click, fill_input, or find_elements. The same browser
    session remains active across subsequent MCP tool calls until
    close_browser is called or the server process exits.

    Pure CDP Mode communicates directly with the browser through the Chrome
    DevTools Protocol rather than WebDriver. This provides SeleniumBase's
    CDP-based browser automation capabilities without using WebDriver as the
    browser-control layer.

    Args:
        url: Optional URL to open immediately after the browser launches.
            If omitted, the browser starts without navigating to a requested
            page.

        headless: Controls whether the browser runs without a visible window.
            If True, always run headless. If False, always run headed.
            If omitted (None), the default depends on the operating system:
            Linux defaults to headless because MCP/server environments
            commonly do not have a graphical desktop, while Windows and macOS
            default to headed so that a visible browser window is available.
            Use True or False to explicitly override the OS-specific default
            on any operating system.

        use_chromium: Use Chromium instead of Google Chrome. This is useful
            when Google Chrome is not installed. SeleniumBase can manage the
            Chromium browser when this option is enabled.

        browser_executable_path: Explicit filesystem path to the browser
            executable when it is not installed in a standard location.
            Do not combine this with use_chromium=True.

        incognito: Launch Chrome/Chromium in incognito mode.

        guest: Launch Chrome/Chromium in guest mode. Do not combine this with
            incognito=True.

        ad_block: Enable SeleniumBase's basic ad-blocking functionality.

        proxy: Optional proxy server. Examples include
            "SERVER:PORT" or "USER:PASS@SERVER:PORT".

    Returns:
        A confirmation message when the browser starts successfully, including
        the effective headless setting, or a descriptive error when browser
        startup fails.

    Lifecycle:
        Call start_browser once at the beginning of a browser automation
        workflow. Reusing the existing session preserves cookies, tabs,
        navigation history, localStorage/sessionStorage, and other browser
        state between tool calls. Call close_browser when finished.

    Environment requirements:
        The MCP runtime must have a compatible Chrome or Chromium browser
        available. If the browser executable cannot be discovered, use
        use_chromium=True or provide browser_executable_path explicitly.

        On Linux, the default is headless=True so the browser can run in
        typical server/container environments without a graphical desktop.
        Set headless=False when a graphical display is available and a visible
        browser is desired. On Windows and macOS, the default is
        headless=False. Set headless=True when running without a desktop or
        when a visible browser window is not desired.
    """
    global _sb

    if _sb is not None:
        return (
            "A browser session is already running. "
            "Call close_browser first."
        )

    if incognito and guest:
        return "Error: incognito and guest cannot both be enabled."

    if use_chromium and browser_executable_path:
        return (
            "Error: use_chromium and browser_executable_path "
            "cannot both be used at the same time."
        )

    # OS-specific default:
    # - Linux: headless by default for server/container compatibility.
    # - Windows/macOS: headed by default for interactive desktop use.
    # - Explicit True/False always overrides the OS default.
    if headless is None:
        effective_headless = sys.platform.startswith("linux")
    else:
        effective_headless = headless

    kwargs: dict[str, Any] = {"headless": effective_headless}

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
            f"(url={url!r}, headless={effective_headless}, "
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
    """Close the active browser session and release browser resources.

    Call this when the browser automation workflow is finished. Closing the
    session ends the persistent browser state, including its open tabs,
    cookies, navigation history, and page state. If browser automation is
    needed afterward, start a new session with start_browser.

    This operation is safe to call when no browser session is active.
    """
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
# Page information
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def get_page_info() -> dict | str:
    """Get current browser session and page metadata.

    Use this as the primary tool for determining where the browser currently
    is after navigation, clicks, form submissions, redirects, reloads, or
    tab switches.

    This is a READ-ONLY metadata operation. It does not inspect arbitrary
    page content, find elements, check visibility, wait for conditions, or
    assert expected values.

    Returns:
        A dictionary containing:
        - running: True when a browser session is active.
        - url: The complete current page URL, including path and query string.
        - title: The current document title.
        - origin: The current page origin (scheme, host, and port).
        - user_agent: The browser's current User-Agent string.
        - history: The browser navigation history for the current session.

    Tool selection:
        - Need URL, title, origin, User-Agent, or navigation history ->
          use get_page_info.
        - Need visible page text or HTML -> use get_content.
        - Need information about matching elements -> use find_elements.
        - Need an immediate state check -> use check_state.
        - Need to wait for a condition -> use wait_for.
        - Need to verify an expected condition -> use assert_that.

    Unlike a dedicated browser-status tool, get_page_info is the single
    source of browser/page metadata. If no browser session is active, it
    returns {"running": False} instead of attempting to access a page.

    This operation does not navigate, reload, click, type, or otherwise
    modify the current page.
    """
    if _sb is None:
        return {"running": False}

    try:
        return {
            "running": True,
            "url": _sb.get_current_url(),
            "title": _sb.get_title(),
            "origin": _sb.get_origin(),
            "user_agent": _sb.get_user_agent(),
            "history": _sb.get_navigation_history(),
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
    """Navigate the current browser tab to a URL.

    Use this when the browser needs to visit a new URL rather than move
    through its existing back/forward history.

    If the URL does not include a protocol such as "https://", SeleniumBase
    automatically prefixes "https://" before navigation. For example,
    "seleniumbase.io" becomes "https://seleniumbase.io".

    Navigation waits for the initial HTML document to be loaded before
    returning. The visited page becomes part of the browser's navigation
    history.

    Args:
        url: Destination URL. May be a complete URL such as
            "https://example.com" or a hostname such as "example.com".

    Returns:
        A confirmation containing the requested URL.

    Tool selection:
        - Go to a new URL -> use navigate.
        - Return to the previous page -> use navigate_history(action="back").
        - Go forward in history -> use navigate_history(action="forward").
        - Refresh the current page -> use navigate_history(action="reload").
    """
    _get_sb().get(url)
    return f"Navigated to {url}"


@mcp.tool()
@handle_sb_errors
def navigate_history(
    action: Literal["back", "forward", "reload"] = "back",
) -> str:
    """Navigate through the current browser history or reload the page.

    Use this tool only for navigation relative to the current browser
    history. Use navigate when going to an arbitrary URL.

    Args:
        action:
            - "back": Navigate to the previous history entry. Has no useful
              effect when there is no previous history entry.
            - "forward": Navigate to the next history entry. Has no useful
              effect when there is no forward history entry.
            - "reload": Reload the current page while ignoring the browser
              cache so page resources are fetched again.

    Returns:
        A confirmation message describing the operation performed.

    Notes:
        These operations can trigger page loads, redirects, and other
        navigation events. Use get_page_info afterward when you need to
        verify the resulting URL or title.

    Tool selection:
        - Arbitrary destination URL -> use navigate.
        - Previous/next browser history entry -> use this tool.
        - Refresh current page -> use this tool with action="reload".
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
    """Find matching elements and return structured element information.

    Use this tool when you need to discover how many elements match a
    selector, inspect their text/tag names, or inspect the HTML of multiple
    matches.

    This tool resolves element handles immediately into ordinary JSON-like
    dictionaries. It does not return live SeleniumBase element objects.

    Args:
        selector: CSS selector, or a SeleniumBase selector that can match
            visible text. Examples include "button", ".login-link", or
            'a:contains("Sign in")'.
        timeout: Maximum number of seconds to wait for matching elements.
            Defaults to 7 seconds.
        include_html: If True, include each matching element's outer HTML.
            If False, return only tag name and text.

    Returns:
        A dictionary containing:
        - count: Number of matching elements found.
        - matches: A list of element dictionaries containing tag_name and
          text, plus html when include_html=True.

    Tool selection:
        - Need structured information about matching elements ->
          use find_elements.
        - Need the visible text/HTML of a page or a single element ->
          use get_content.
        - Need to click one of several matches -> use click with nth.
        - Need to know whether an element is present/visible ->
          use check_state.

    Note:
        Element handles cannot be persisted across MCP calls. If you find
        elements and then need to act on one, resolve it again with the
        appropriate interaction tool.
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
                }
                for e in els
            ],
        }

    return {
        "count": len(els),
        "matches": [
            {
                "tag_name": e.tag_name,
                "text": e.text,
            }
            for e in els
        ],
    }


@mcp.tool()
@handle_sb_errors
def get_content(
    selector: str | None = None,
    output_format: Literal["text", "html", "urls"] = "text",
    include_shadow_dom: bool = True,
) -> str | list[str]:
    """Read visible text, HTML, or discovered URLs from the current page.

    Use this tool when you need actual page content or URL information rather
    than page metadata.

    Args:
        selector: Optional CSS selector or SeleniumBase text-matching selector
            identifying the element whose content should be read. For
            output_format="text" or "html", the selector scopes the returned
            content to that element. For output_format="urls", the selector
            scopes URL discovery to URLs within that element. When omitted,
            the operation applies to the whole page.

        output_format:
            - "text": Return visible text from the page or selected element.
            - "html": Return HTML from the page or selected element.
            - "urls": Return all discovered linked/resource URLs on the page
              or within the selected element. URLs associated with elements
              such as anchors, links, images, scripts, and metadata may be
              included. SeleniumBase returns full URLs with their URL
              prefixes.

        include_shadow_dom: When output_format="html" and selector is omitted,
            include any shadow-root HTML present in the page. This option has
            no effect for "text" or "urls", or when a selector is specified.

    Returns:
        For output_format="text", a string containing visible text.
        For output_format="html", a string containing HTML.
        For output_format="urls", a list of URL strings. This is useful for
        crawling, link discovery, resource inspection, and finding candidate
        URLs before navigating to them.

    Tool selection:
        - Need URL, title, origin, User-Agent, or navigation history ->
          use get_page_info.
        - Need visible text -> use output_format="text".
        - Need page or element HTML -> use output_format="html".
        - Need URLs from the page or an element -> use output_format="urls".
        - Need structured information about matching elements ->
          use find_elements.
        - Need to check whether an element is present or visible ->
          use check_state.
        - Need to wait for content to appear -> use wait_for.
    """
    sb = _get_sb()

    if output_format == "urls":
        return sb.get_all_urls(selector=selector)

    if selector is None:
        if output_format == "html":
            return sb.get_page_source(
                include_shadow_dom=include_shadow_dom
            )
        return sb.get_text("body")

    if output_format == "html":
        return sb.get_element_html(selector)

    return sb.get_text(selector)


@mcp.tool()
@handle_sb_errors
def get_attributes(
    selector: str,
    attribute: str | None = None,
) -> Any:
    """Read HTML attributes from a matching element.

    Args:
        selector: CSS selector or SeleniumBase text-matching selector for
            the target element.
        attribute: Specific HTML attribute to retrieve. When omitted, return
            all available attributes as a dictionary.

    Returns:
        The requested attribute value, or a dictionary containing all
        attributes when attribute is omitted.

    This is a read-only operation and does not modify the element.
    """
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
    """Immediately inspect the current state of an element or page.

    Use this tool when you need an observation of the current state and do
    NOT want to wait for a condition. For waiting behavior, use wait_for.
    For an expectation that should fail as an assertion, use assert_that.

    Args:
        check:
            - "present": Return whether at least one matching element exists.
            - "visible": Return whether the matching element is visible.
            - "count": Return the number of matching elements. This check may
              wait up to 1 second for a match.
            - "text_visible": Return whether the specified text is visible
              within the selected element. Requires text.
        selector: CSS selector or SeleniumBase selector for the element.
            Defaults to "body".
        text: Text to check when check="text_visible".

    Returns:
        A boolean for present/visible/text_visible, or an integer count for
        count. Missing elements do not cause an exception for these checks.

    Tool selection:
        - Immediate yes/no/count observation -> use check_state.
        - Wait until a state becomes true/false -> use wait_for.
        - Verify an expected condition and fail when it is not met ->
          use assert_that.

    Note:
        Except for count's short lookup, this tool does not wait for elements
        to appear. Use wait_for when page timing matters.
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
    """Click one or more elements matching a selector.

    This is the primary element-clicking tool. The selector may be a CSS
    selector or SeleniumBase text-matching selector such as
    'a:contains("Sign in")'.

    Args:
        selector: Target CSS selector or text-matching selector.
        nth: Click only the Nth matching element, using 1-based indexing.
            Takes priority over all_matches.
        all_matches: Click every currently visible matching element, in order.
            Ignored when nth is provided.
        only_if_visible: Attempt the click only when the target is already
            visible. Does not wait for the element to become visible.
        parent_selector: Restrict the nested lookup to a parent element.
            Useful for elements inside iframes or nested containers when
            supported by SeleniumBase.
        timeout: Seconds to wait for a basic click when no specialized mode
            is selected. Defaults to 7 seconds.
        scroll: Scroll the target into view before clicking.

    Tool selection:
        - Click one matching element -> basic click.
        - Click a specific matching occurrence -> set nth.
        - Click every visible match -> set all_matches=True.
        - Click only when already visible -> set only_if_visible=True.
        - Click an element nested inside another element -> set
          parent_selector.
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
def hover(
    selector: str,
    then_click_selector: str | None = None,
) -> str:
    """Hover over an element, optionally clicking an element revealed by hover.

    Use this for menus, dropdowns, tooltips, or other interfaces where an
    element must first be hovered before its target becomes available.

    Args:
        selector: Element to hover over.
        then_click_selector: Optional element to click after the hover.
            Useful for a submenu item or dropdown option revealed by hover.

    Returns:
        A confirmation describing the hover/click operation.
    """
    sb = _get_sb()

    if then_click_selector:
        sb.hover_and_click(selector, then_click_selector)
        return f"Hovered {selector} and clicked {then_click_selector}"

    sb.hover_element(selector)
    return f"Hovered {selector}"


@mcp.tool()
@handle_sb_errors
def drag_and_drop(
    source_selector: str,
    target_selector: str,
) -> str:
    """Drag a draggable element and drop it onto another element.

    Drag-and-drop is performed through SeleniumBase's CDP browser controls,
    simulating the pointer and mouse events expected by web applications.

    Args:
        source_selector: CSS selector identifying the draggable source.
        target_selector: CSS selector identifying the drop target.

    The simulated interaction includes events such as pointerdown,
    mousedown, dragstart, dragenter, dragover, drop, dragend, mouseup, and
    pointerup.
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
    """Enter, append, directly set, or clear text in a form control.

    Use this tool for input elements, textareas, and contenteditable elements.

    Args:
        selector: CSS selector or SeleniumBase selector identifying the
            input, textarea, or contenteditable element.
        text: Text to enter or set. Ignored when mode="clear".
        mode:
            - "type": Clear the field and type text normally.
            - "append": Keep the existing value and send text as keystrokes.
            - "set_value": Set the value directly and immediately. This can
              be useful for fast form filling but does not simulate normal
              key events.
            - "fast_type": Clear the field and type text quickly.
            - "clear": Empty the field; text is ignored.
        timeout: Maximum seconds to wait for the target element.

    Tool selection:
        - Normal human-like text entry -> mode="type".
        - Add text without clearing -> mode="append".
        - Directly set a value -> mode="set_value".
        - Fast typing -> mode="fast_type".
        - Empty a field -> mode="clear".
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
    """Select an option from an HTML <select> dropdown.

    Args:
        dropdown_selector: CSS selector identifying the <select> element.
        value: The option's visible text, its HTML value attribute, or its
            0-based index, depending on by.
        by:
            - "text": Match the option's visible text.
            - "value": Match the option's HTML value attribute.
            - "index": Match the option's 0-based position. Both integer and
              numeric-string values are accepted.

    Raises:
        An error when the dropdown or requested option cannot be found.

    This tool is for native <select> elements. For custom JavaScript
    dropdowns made from div/button/list elements, use click or other
    element-interaction tools instead.
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
def act_on_element(
    selector: str,
    action: Literal[
        "focus",
        "highlight",
        "scroll_into_view",
    ] = "focus",
) -> str:
    """Perform a non-click positioning or debugging action on an element.

    Use this tool when an element needs to be focused, highlighted for human
    observation/debugging, or scrolled into the viewport.

    This tool does NOT click, type into, select from, hover over, or otherwise
    activate the element.

    Args:
        selector: CSS selector or SeleniumBase selector identifying the target.
        action:
            - "focus": Move keyboard focus to the element.
            - "highlight": Temporarily highlight the element for debugging or
              demonstration. This can affect timing and may reduce stealth.
            - "scroll_into_view": Scroll the page until the element is in the
              current viewport.

    Tool selection:
        - Click -> use click.
        - Type into a form control -> use fill_input.
        - Hover -> use hover.
        - Focus, highlight, or scroll without activating -> use
          act_on_element.
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
    state: Literal[
        "present",
        "visible",
        "not_visible",
        "absent",
    ] = "visible",
    selector: str | None = None,
    text: str | None = None,
    timeout: int | float | None = 7,
) -> str:
    """Wait until an element or text reaches a requested state.

    Use this tool when the page is dynamic and an automation step must wait
    for a condition before continuing.

    Unlike check_state, this tool intentionally waits. Unlike assert_that,
    its purpose is synchronization rather than validating a test expectation.

    Args:
        state:
            - "present": Wait until the matching element exists.
            - "visible": Wait until the matching element is visible.
            - "not_visible": Wait until the matching element is not visible.
            - "absent": Wait until the matching element no longer exists.
              Ignored when text is provided.
        selector: CSS selector or SeleniumBase selector for the element.
            Required unless text is supplied.
        text: If supplied, wait for this text to appear within selector
            (or within "body" when selector is omitted).
        timeout: Maximum seconds to wait. Defaults to 7 seconds.

    Returns:
        A confirmation when the requested condition is reached.

    Tool selection:
        - Check current state immediately -> use check_state.
        - Wait for a state/content transition -> use wait_for.
        - Verify an expected value/condition -> use assert_that.
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
        "url_contains",
    ] = "element_visible",
    selector: str | None = None,
    expected: str | None = None,
    exact: bool = False,
    timeout: int | float | None = 7,
) -> str:
    """Verify an expected browser condition and fail when it is not met.

    Use this tool for explicit verification. Unlike check_state, which simply
    reports the current state, assert_that treats a failed expectation as an
    error. Unlike wait_for, URL/title checks do not wait.

    Args:
        check:
            - "element_present": Verify selector identifies a present element.
            - "element_visible": Verify selector identifies a visible element.
            - "text": Verify expected text within selector, or within the
              whole HTML document when selector is omitted.
            - "title": Verify the exact page title.
            - "url": Verify the exact current URL.
            - "url_contains": Verify that the current URL contains expected.
        selector: Element selector for element_present, element_visible, and
            text checks.
        expected: Expected text/title/URL value for text, title, url, and
            url_contains.
        exact: For check="text", require exact text rather than a substring.
        timeout: Maximum seconds to wait for element/text checks.

    Returns:
        A confirmation when the expectation passes.

    Raises:
        An assertion-related SeleniumBase exception when the expectation
        fails; the MCP error wrapper converts it to a descriptive result.

    Tool selection:
        - Just inspect current state -> use check_state.
        - Wait for a condition to become true -> use wait_for.
        - Verify that an expected condition is true -> use assert_that.
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
        action:
            - "get_all": Return all cookies currently available to the browser,
              including attributes such as name, value, domain, path, expiry,
              and security flags.
            - "clear": Delete all cookies from the current browser session.
            - "save": Save current cookies to filename. The file may be
              created or overwritten.
            - "load": Load cookies from filename into the current browser
              session.
        filename: Filesystem path used by save/load. Defaults to
            "cookies.txt". Ignored for get_all and clear.

    Returns:
        "get_all": Current browser cookies.
        "clear": Confirmation that cookies were cleared.
        "save": Confirmation containing the destination filename.
        "load": Confirmation containing the source filename.

    Security:
        Cookie data can contain authentication credentials, session
        identifiers, and other private information. Only inspect, save,
        load, or share cookies when explicitly authorized.

        `filename` is passed to SeleniumBase's cookie persistence methods and
        can access the filesystem available to the MCP server. Use only
        trusted, authorized paths. The save action may overwrite an existing
        file.

    Notes:
        Loading saved cookies does not guarantee restoration of a login.
        Cookies may be expired, invalidated, domain/path restricted, or
        dependent on other browser state. Navigate to the relevant site when
        necessary so the browser has the appropriate origin for the cookies.
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
    """Get or set a key in localStorage or sessionStorage.

    Args:
        key: Storage key to read or modify.
        value: Value to store when action="set". Required for set.
        storage: "local" for localStorage or "session" for sessionStorage.
        action: "get" to read the key or "set" to write the key.

    Returns:
        The stored value for get, or a confirmation message for set.

    Security:
        Web storage can contain authentication tokens, session identifiers,
        and other sensitive application state. Only use this tool with trusted
        sites and authorized MCP clients.

    Notes:
        Storage belongs to the current page origin. Values from one website
        are not generally available to another origin.
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
    """Scroll the current page vertically.

    Args:
        direction:
            - "up": Scroll upward by amount percent of the window height.
            - "down": Scroll downward by amount percent of the window height.
            - "top": Scroll directly to the top; amount is ignored.
            - "bottom": Scroll directly to the bottom; amount is ignored.
        amount: Percentage of the current viewport height used for relative
            up/down scrolling. For example, amount=25 scrolls approximately
            one quarter of the viewport height.

    Use act_on_element(action="scroll_into_view") when the goal is to reveal
    a specific element rather than scroll the page by a relative amount.
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
    """Get or change browser window geometry and state.

    Args:
        action:
            - "get_rect": Return the current window coordinates and size.
            - "set_rect": Set x, y, width, and height. All four are required.
            - "maximize": Maximize the browser window.
            - "minimize": Minimize the browser window.
        x: Horizontal screen position for set_rect.
        y: Vertical screen position for set_rect.
        width: Window width for set_rect.
        height: Window height for set_rect.

    Use this tool for browser-window geometry/state. For switching between
    browser tabs, use manage_tabs instead.
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

    Use this tool for tab management. Browser navigation within the current
    tab belongs to navigate and navigate_history.

    Args:
        action:
            - "list": Return each open tab's index, URL, and title. Call this
              before switch when you need to determine a tab_index.
            - "open": Open a new tab, optionally navigating it to url.
            - "switch": Switch to the tab identified by tab_index from list.
            - "switch_newest": Switch to the newest tab.
            - "close_active": Close the currently active tab.
        url: URL for action="open".
        tab_index: Index returned by action="list" for action="switch".
        switch_to: For action="open", switch to the newly created tab when
            True.

    Notes:
        Clicking a link or performing another browser action may open a new
        tab. Use action="list" to inspect available tabs before switching by
        index. Tab indexes should be treated as current-session values and
        may change after tabs are opened or closed.
    """
    sb = _get_sb()

    if action == "list":
        tabs = sb.get_tabs()
        return [
            {
                "index": i,
                "url": getattr(t, "url", None),
                "title": getattr(t, "title", None),
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
    """Attempt a SeleniumBase CDP-based CAPTCHA interaction.

    This tool attempts to interact with CAPTCHA controls such as Cloudflare
    Turnstile, reCAPTCHA, or FriendlyCaptcha using browser/CDP interaction.

    The tool does not guarantee that a CAPTCHA was solved. Some CAPTCHA
    controls are embedded inside shadow DOM or otherwise do not expose an
    easy success signal. A successful attempt may result in changes to page
    state or browser cookies.

    Tool workflow:
        1. Inspect the page with get_content when you need to determine
           whether CAPTCHA-related controls are present.
        2. Call solve_captcha to attempt the interaction.
        3. Use get_page_info, get_content, check_state, or manage_cookies
           to inspect resulting page/session state.

    Returns:
        A message confirming that the CAPTCHA interaction was attempted, not
        a guarantee that the CAPTCHA challenge was solved.
    """
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
    folder: str | None = None,
) -> str:
    """Save the current browser page as a screenshot, HTML file, or PDF.

    Use this tool when an automation workflow needs a persistent artifact
    from the current page, such as a screenshot for debugging, page source
    for inspection, or a PDF representation.

    Args:
        format:
            - "screenshot": Save a PNG screenshot.
            - "html": Save the current page source as HTML.
            - "pdf": Save the current page as a PDF.
        filename: Output filename. Defaults to screenshot.png,
            page_source.html, or page.pdf depending on format.
        folder: Optional destination folder.

    Returns:
        A confirmation containing the output format and filename.

    Security:
        filename and folder can affect filesystem paths available to the MCP
        server. Existing files may be overwritten. Use trusted, authorized
        paths only.
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
    """Evaluate arbitrary JavaScript in the current page context.

    Use this only when the required browser operation cannot be accomplished
    through the higher-level SeleniumBase tools.

    The expression is evaluated through the Chrome DevTools Protocol
    Runtime.evaluate mechanism. Promise results are awaited and values are
    returned by value.

    Args:
        expression: JavaScript expression to evaluate in the current page
            context.

    Returns:
        The JavaScript evaluation result when it can be represented across
        the MCP boundary.

    Security:
        This provides unrestricted JavaScript execution in the current browser
        page. It can read or modify page data and interact with the page in
        ways that bypass the higher-level tool abstractions. Only expose this
        MCP server to trusted clients.
    """
    return _get_sb().evaluate(expression)


@mcp.tool()
@handle_sb_errors
def wait_seconds(seconds: int | float) -> str:
    """Block the MCP server for a fixed number of seconds.

    This is a low-level timing tool. It performs no browser action while
    waiting and should not be used when waiting for a page condition.

    Prefer wait_for when waiting for an element or text to appear/disappear,
    because wait_for can return as soon as the requested condition is met.

    Args:
        seconds: Number of seconds to block. May be an integer or float.
    """
    _get_sb().sleep(seconds)
    return f"Waited {seconds}s"


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
        print(
            f'\nThe "{mcp.name}" server was stopped.',
            file=sys.stderr,
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
