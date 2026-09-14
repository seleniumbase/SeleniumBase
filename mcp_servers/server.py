#!/usr/bin/env python3
"""
SeleniumBase Pure CDP Mode MCP Server
======================================
Exposes SeleniumBase's Pure CDP Mode (sync API, `seleniumbase.sb_cdp.Chrome`)
as MCP tools. Pure CDP Mode drives the web browser entirely over the Chrome
DevTools Protocol (no WebDriver at all), and can avoid automation signals
that are generally associated with WebDriver-based browser automation tools.
Pure CDP Mode also includes CAPTCHA-solving support for detecting & clicking
CAPTCHA checkboxes via CDP functions.

Reference:
github.com/seleniumbase/SeleniumBase/blob/master/help_docs/cdp_mode_methods.md

Model: One persistent `sb_cdp.Chrome` session per server process.
Call start_browser once; drive it with the other tools; then close_browser.

Selectors:
- CSS selectors are preferred. (All tools that take selectors support CSS.)
- XPath support is tool-dependent: XPath is accepted in several (but not all)
  cases. Some methods utilize the Chrome DevTools protocol, where XPath might
  not be accepted unless SeleniumBase is able to convert those XPath selectors
  into valid CSS selectors first (which SeleniumBase tries to do as needed).
- SeleniumBase includes a visible text selector, e.g. `a:contains("Sign in")`.
  This selector is accepted by multiple individual tools, but not all of them.
- Tool-specific documentation takes precedence when selector behavior differs.

Design notes:
Related SeleniumBase capabilities are consolidated into parameterized tools
using action, mode, state, or check parameters.
This keeps the toolset compact and predictable while giving an MCP client
access to the underlying browser-automation capabilities without
having to choose between multiple near-identical tools.

Tool-selection philosophy:
- Use 'start_browser'/'close_browser' for opening/quitting the web browser.
- Use 'open_url'/'manage_history' for browser navigation and history
  inspection.
- Use 'get_page_info' for reading browser/page metadata such as URL/title.
- Use 'get_content'/'get_attributes' for reading text, HTML, or attributes.
- Use 'find_elements' for discovering and inspecting multiple matching
  elements as structured data.
- Use 'check_if_condition' for an immediate, non-waiting state check.
- Use 'wait_for_condition' when the agent needs to wait for a condition
  to become true.
- Use 'assert_condition' when the agent needs to verify an expected condition
  and treat failure as an assertion error.
- Use 'click_element'/'type_text'/'select_option' for standard page
  interactions.
- Use 'hover_action' for just a hover, with a click, or with a drag/drop.
- Use 'focus_element' for element positioning and visual focus.
- Use 'solve_captcha' for clicking the checkbox of a CAPTCHA on the page.
- Use 'save_page' for saving page output as a PNG, a PDF, or an HTML file.
"""
from __future__ import annotations
import atexit
import sys
from functools import wraps
from typing import Any, Literal
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from seleniumbase import sb_cdp

mcp = MCPServer("seleniumbase-mcp")

_sb: sb_cdp.CDPMethods | None = None


def _get_sb() -> sb_cdp.CDPMethods:
    """Return the active browser session or raise a useful lifecycle error."""
    if _sb is None:
        raise ToolError("No browser session. Call start_browser first.")
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
        except ToolError:
            raise
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
    headless: Literal[False, True, None] = None,
    use_chromium: bool = False,
    browser_executable_path: str | None = None,
    incognito: bool = False,
    guest: bool = False,
    ad_block: bool = False,
    proxy: str | None = None,
) -> str:
    """Launch a persistent SeleniumBase Pure CDP Mode browser session.

    Call this before using browser interaction tools such as open_url,
    get_content, click_element, type_text, or find_elements. The same browser
    session remains active across subsequent MCP tool calls until
    close_browser is called or the server process exits.

    Pure CDP Mode controls the browser through the Chrome DevTools Protocol
    (CDP), not WebDriver.

    Args:
        url: Optional URL to navigate to during browser startup.
            When provided, the tool waits for the browser launch/navigation
            operation to complete before returning. If omitted, the browser
            starts without navigating to a specified URL.

        headless: Controls whether the browser runs without a visible window.
            True forces headless mode; False forces headed mode. If None, this
            tool defaults to headless on Linux and headed on Windows/macOS.

        use_chromium: Use Chromium instead of Google Chrome. This is useful
            when Google Chrome is not installed. SeleniumBase can manage the
            Chromium browser when this option is enabled.

        browser_executable_path: Optional path to the browser executable.
            Use this when the desired browser is installed at a non-standard
            location. Mutually exclusive with use_chromium.

        incognito: Launch Chrome/Chromium in incognito mode.

        guest: Launch Chrome/Chromium in guest mode.
            Do not combine this with incognito=True.

        ad_block: Enable SeleniumBase's basic ad-blocking functionality.

        proxy: Optional proxy server.
            Examples include "SERVER:PORT" or "USER:PASS@SERVER:PORT".

    Returns:
        A confirmation message when the browser starts successfully,
        or a descriptive error if the browser startup fails.

    Startup behavior:
        If the initial launch fails, the tool automatically retries once.

    Lifecycle:
        Call start_browser once at the beginning of a browser automation
        workflow. Reusing the existing session preserves cookies, tabs,
        navigation history, localStorage/sessionStorage, and other browser
        state between tool calls. Call close_browser when finished.
        If a browser session is already running, this tool does not launch
        another browser and instead returns a message indicating that the
        existing session is active.

    Environment requirements:
        The MCP runtime must have a compatible Chrome or Chromium browser
        available. If the browser executable cannot be discovered, use
        use_chromium=True or provide browser_executable_path explicitly.
    """
    global _sb

    if _sb is not None:
        return "A browser session is already running."

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
    except Exception:
        # Retry once if the first launch attempt fails.
        # (A retry helped when testing on Glama's MCP Inspector.)
        # If it fails again, then we'll return the error from
        # the 2nd attempt. (The first error doesn't matter here.)
        try:
            if _sb is not None:
                try:
                    _sb.quit()
                except Exception:
                    pass
                _sb = None
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
        return "No browser session is currently running."

    try:
        _sb.quit()
    except Exception as e:
        return (
            "Error calling `quit()` on the browser session: "
            f"{e.__class__.__name__} - {str(e).strip()}"
        )
    finally:
        _sb = None

    return "The browser session was closed."


# ---------------------------------------------------------------------------
# Page information
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def get_page_info() -> dict[str, Any]:
    """Get current browser session and page metadata.

    Use this as the primary tool for determining where the browser currently
    is after navigation, clicks, form submissions, redirects, reloads, or
    tab switches.

    This is a READ-ONLY metadata operation. It does not inspect arbitrary
    page content, find elements, check visibility, wait for conditions, or
    assert expected values.

    Returns:
        A dictionary containing:
        - running: True when browser metadata was successfully retrieved.
          False when no session is available or metadata retrieval failed.
        - url: The complete current page URL, including path and query string.
        - title: The current document title.
        - origin: The current page origin (scheme, host, and port).
        - user_agent: The browser's current User-Agent string.

    Tool selection:
        - Need URL, title, origin, or User-Agent -> use get_page_info.
        - Need visible page text or HTML -> use get_content.
        - Need information about matching elements -> use find_elements.
        - Need an immediate state check -> use check_if_condition.
        - Need to wait for a condition -> use wait_for_condition.
        - Need to verify an expected condition -> use assert_condition.

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
def open_url(url: str) -> str:
    """Navigate the current browser tab to the URL provided.

    Use this when the browser needs to visit a new URL rather than move
    through its existing back/forward history.

    If the URL does not include a protocol such as "https://", SeleniumBase
    automatically prefixes "https://" before navigation. For example,
    "seleniumbase.io" becomes "https://seleniumbase.io".

    Navigation waits for the browser's navigation operation to complete
    before returning. Dynamic content may still be loading;
    use wait_for_condition when synchronization is required.
    If there's an error, that gets propagated through @handle_sb_errors.

    Args:
        url: The destination URL. May be a complete URL such as
            "https://example.com", or a hostname such as "example.com".

    Returns:
        A confirmation message containing the requested URL if successful.

    Tool selection:
        - Navigate to a new URL -> use open_url.
        - Return to the previous page -> use manage_history(action="back").
        - Go forward in history -> use manage_history(action="forward").
        - Refresh the current page -> use manage_history(action="reload").
    """
    sb = _get_sb()
    sb.get(url)
    return f"Navigated to {url}"


@mcp.tool()
@handle_sb_errors
def manage_history(
    action: Literal["back", "forward", "reload", "list"] = "list",
) -> str | dict[str, Any]:
    """Manage or inspect the current browser tab's navigation history.

    Use 'back' or 'forward' for history navigation, 'reload' to refresh
    while bypassing the cache, or 'list' to inspect history.
    Use 'open_url' for navigation to an arbitrary URL.

    Args:
        action:
            - "back": Go to the previous history entry, if available.
            - "forward": Go to the next history entry, if available.
            - "reload": Reload the current page while ignoring the cache.
            - "list": Return the current history position and entries.

    Navigation actions can trigger page loads or redirects.
    Use get_page_info afterward to verify the resulting URL or title.
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

    if action == "list":
        position, entries = sb.get_navigation_history()
        return {
            "position": position,
            "entries": [
                {
                    "id": entry.id_,
                    "url": entry.url,
                    "user_typed_url": entry.user_typed_url,
                    "title": entry.title,
                    "transition_type": entry.transition_type.value,
                }
                for entry in entries
            ],
        }

    return (
        f"Error: unknown action '{action}'. "
        "Use 'back', 'forward', 'reload', or 'list'."
    )


# ---------------------------------------------------------------------------
# Finding & reading
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def find_elements(
    selector: str,
    timeout: float = 0.5,
    include_html: bool = False,
) -> dict | str:
    """Find matching elements and return structured element information.

    Use this tool when you need to discover how many elements match a
    selector, inspect their text/tag names, or inspect the HTML of multiple
    matches.

    This tool converts matching elements into ordinary serializable
    dictionaries. It does not return live SeleniumBase element objects.

    Args:
        selector: A CSS selector, or an XPath selector that SeleniumBase can
            convert to CSS. In sb.find_elements, SeleniumBase automatically
            attempts to convert XPath to CSS. Some XPath expressions, such
            as those using `contains(...)`, cannot be converted to CSS and
            therefore aren't supported by this tool.

        timeout: Maximum number of seconds to wait for at least one matching
            element to appear. If the selector is an XPath selector that
            cannot be converted into a valid CSS selector, then the wait
            might be less than the timeout.

        include_html: If True, include each matching element's outer HTML.
            If False, return only tag name and text.

    Returns:
        A dictionary containing:
        - count: Number of matching elements found.
        - matches: A list of element dictionaries containing tag_name and
          text, plus html when include_html=True.
        If there's an error during search, then "error" is added into the
        returned dictionary with error details.

    Tool selection:
        - Need structured information about matching elements ->
          use find_elements.
        - Need the visible text/HTML of a page or a single element ->
          use get_content.
        - Need to click one of several matches -> use click_element with nth.
        - Need to know whether an element is present/visible ->
          use check_if_condition.

    Notes:
        Element handles cannot be persisted across MCP calls. If you find
        elements and then need to act on one, resolve it again with the
        appropriate interaction tool.

        For uncaught errors, @handle_sb_errors returns strings.
    """
    sb = _get_sb()
    try:
        elements = sb.find_elements(selector, timeout=timeout)
    except Exception as e:
        return {
            "count": 0,
            "matches": [],
            "error": str(e),
        }

    matches = []
    for element in elements:
        match = {
            "tag_name": element.tag_name,
            "text": element.text,
        }
        if include_html:
            match["html"] = element.get_html()
        matches.append(match)

    return {
        "count": len(matches),
        "matches": matches,
    }


@mcp.tool()
@handle_sb_errors
def get_content(
    selector: str = "body",
    output_format: Literal["text", "html", "urls"] = "text",
    timeout: float = 5,
) -> str | list[str]:
    """Read visible text, HTML, or discovered URLs from the selected element.

    Use this tool when you need to get actual page content or URL information
    rather than page metadata.

    Args:
        selector: CSS selector or SeleniumBase-supported XPath selector.
            Default: "body".

        output_format:
            - "text": Return visible text from the selected element.
            - "html": Return HTML from the selected element.
            - "urls": Return URLs discovered by SeleniumBase within the
              selected element. Returned URLs are normalized to full URLs
              with their protocol prefixes.

        timeout: Maximum seconds to wait for the target element. Default: 5.

    Tool selection:
        - Need URL, title, origin, or User-Agent -> use get_page_info.
        - Need visible text, html, or URLs on a page -> use get_content.
        - Need structured information about matching elements ->
          use find_elements.
        - Need to check element presence/visibility -> use check_if_condition.
        - Need to wait for content to appear -> use wait_for_condition.

    If there's no matching element found within the timeout,
        then @handle_sb_errors returns details from the exception raised.
    """
    sb = _get_sb()

    if output_format == "text":
        return sb.get_text(selector, timeout=timeout)

    if output_format == "html":
        return sb.get_element_html(selector, timeout=timeout)

    if output_format == "urls":
        return sb.get_all_urls(selector=selector, timeout=timeout)

    return (
        f"Error: unknown output_format '{output_format}'. "
        "Use 'text', 'html', or 'urls'."
    )


@mcp.tool()
@handle_sb_errors
def get_attributes(
    selector: str,
    attribute: str | None = None,
    timeout: float = 5,
) -> str | dict[str, Any] | None:
    """Read HTML attributes from the first matching element.

    Use this tool when you need the value of a specific HTML attribute,
    or all HTML attributes of an element. Attributes could be something
    such as href, src, value, class, id, name, type, aria-label, etc.

    Args:
        selector: CSS selector or SeleniumBase-supported XPath selector.

        attribute: Specific HTML attribute to retrieve. When omitted, return
            all HTML attributes of the first matching element as a dictionary.

        timeout: Maximum seconds to wait for the target element. Default: 5.

    Tool selection:
        - Need one or more HTML attribute values from a specific element ->
          use this tool.
        - Need to discover multiple matching elements or inspect their text ->
          use 'find_elements'.
        - Need visible text or HTML content -> use 'get_content'.
        - Need to check element presence/visibility ->
          use 'check_if_condition'.

    This is a read-only operation.

    If there's no matching element found within the timeout,
        then @handle_sb_errors returns details from the exception raised.
    """
    sb = _get_sb()

    if attribute:
        return sb.get_attribute(selector, attribute, timeout=timeout)

    return sb.get_element_attributes(selector, timeout=timeout)


@mcp.tool()
@handle_sb_errors
def check_if_condition(
    check: Literal["present", "visible"] = "visible",
    selector: str = "body",
    text: str | None = None,
) -> bool | str:
    """Check the current state of an element or text without waiting
    for the condition to become true.

    Use this tool when you need an immediate boolean observation of the current
    page state. Use wait_for_condition when the condition may become true later
    and the workflow should wait for it. Use assert_condition when the
    condition is an expected requirement and failure should be treated as an
    assertion error.

    Args:
        check:
            The element state to inspect when text is not provided:
            - "present": Return True when at least one matching element exists.
            - "visible": Return True when the matching element is visible.
            `check` is ignored when `text` is provided.

        selector:
            CSS selector or SeleniumBase selector identifying the element.

        text:
            Optional text to check for visibility within `selector`. When
            provided, this takes precedence over `check`; the tool checks text
            visibility instead of element presence or visibility. Use this when
            the question is "Is this text currently visible?" rather than
            whether the element itself is present or visible.

    Returns:
        True or False indicating whether the requested condition is currently
        satisfied. Missing elements return False rather than raising an
        exception. If there's an error, returns a string with error details.

    Tool selection:
        - Immediate boolean observation -> use check_if_condition.
        - Wait for a state/content transition -> use wait_for_condition.
        - Verify an expected condition -> use assert_condition.
        - Need element details of matching elements -> use find_elements.
        - Need to read page or element content -> use get_content.

    Notes:
        This tool does not intentionally wait for elements or text to appear.
        It is intended for checking the current state only. If page timing or
        asynchronous loading matters, use wait_for_condition instead.

        When `text` is provided, `check` is ignored.
    """
    sb = _get_sb()

    if text:
        return sb.is_text_visible(text, selector)

    if check == "present":
        return sb.is_element_present(selector)

    if check == "visible":
        return sb.is_element_visible(selector)

    return (
        f"Error: Unknown check {check!r}. Use 'present' or 'visible'."
    )


# ---------------------------------------------------------------------------
# Interacting with elements
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def click_element(
    selector: str,
    nth: int | None = None,
    all_matches: bool = False,
    only_if_visible: bool = False,
    parent_selector: str | None = None,
    timeout: float = 5,
    scroll: bool = True,
) -> str:
    """Click element(s) matching a CSS, XPath, or supported text selector.

    Use this tool for normal clicks, clicking a specific matching occurrence,
    clicking all visible matches, conditional clicks, or clicks scoped to a
    parent element.

    Selection behavior:
        - `nth` is 1-based and takes precedence over every other click mode.
        - Otherwise, `all_matches=True` clicks every currently visible match.
        - Otherwise, `only_if_visible=True` clicks only if a match is visible.
        - Otherwise, `parent_selector` scopes the click to a nested element.
        - With none of the above, performs a normal SeleniumBase click.

    Args:
        selector: CSS selector, XPath selector, or supported SeleniumBase
            text-matching selector. Text-matching selectors such as
            `a:contains("Sign in")` are supported only for single-element
            clicks; do not use them with `all_matches=True`.

        nth: 1-based occurrence to click when multiple elements match.
            Must be >= 1 if provided. Takes precedence over `all_matches`,
            `only_if_visible`, and `parent_selector`.

        all_matches: If True, click every currently visible matching element
            in order of appearance. Ignored when `nth` is provided. Use only
            when multiple clicks are intentionally desired, such as for
            clicking all the checkboxes in a section of a webpage.
            If any of the click actions induces page navigation, then
            subsequent clicks are cancelled without any exceptions raised.

        only_if_visible: If True, click only when the target is already
            visible; do not wait for it to become visible.

        parent_selector: CSS/XPath selector for the parent/container in which
            to find `selector`. Used only for the nested-click mode.
            Can be used to click an element inside a parent iframe.

        timeout: Maximum seconds to wait for a normal click operation.
            Default: 5. Not used by conditional or bulk click modes.

        scroll: If True, scroll the target into view before a normal or
            indexed click. Default: True.

    Examples:
        - Click the first button: `click_element("button")`
        - Click the 2nd button: `click_element("button", nth=2)`
        - Click all checkboxes:
          `click_element('input[type="checkbox"]', all_matches=True)`
        - Click the first visible link:
          `click_element("a", only_if_visible=True)`
        - Click the first button that's inside the first iframe:
          `click_element("button", parent_selector="iframe")`

    Error behavior:
        With the exception of using 'only_if_visible=True', if there's no
        matching element found within the timeout, then @handle_sb_errors
        returns details from the exception raised.

    When not to use:
        - Do not use this tool if you need to hover an element first before
          clicking; use hover_action with action="hover_and_click" instead.
    """
    sb = _get_sb()

    if nth:
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
def hover_action(
    selector: str,
    secondary_selector: str | None = None,
    action: Literal["hover", "hover_and_click", "drag_and_drop"] = "hover",
    timeout: float = 5,
) -> str:
    """Hover over an element, optionally click another, or drag-and-drop.

    Use this tool for hover interactions, hover-triggered menus, and
    drag-and-drop operations.

    Args:
        selector:
            The primary element selector.
            For action="hover", this is the element to hover over.
            For action="hover_and_click", this is the element to hover over
            before clicking 'secondary_selector'.
            For action="drag_and_drop", this is the draggable source element.

        secondary_selector:
            The secondary element selector.
            Required for action="hover_and_click", where it identifies
            the element to click after hovering 'selector'.
            Required for action="drag_and_drop", where it identifies the
            destination/drop target.
            Not used for action="hover".

        action:
            - "hover": Hover over 'selector' only.
            - "hover_and_click": Hover over 'selector', then click
              'secondary_selector' after a short moment has passed.
            - "drag_and_drop": Drag 'selector' and drop it onto
              'secondary_selector'.

        timeout: Maximum seconds to wait for 'selector'.
            For drag_and_drop, the same timeout applies to secondary_selector.
            For hover_and_click, SeleniumBase uses its own short wait for
            secondary_selector; this parameter does not extend that secondary
            wait.

    Returns:
        A confirmation message describing the performed operation's result.

    Error behavior:
        If a required element cannot be found or interacted with within the
        applicable wait period, or if an error occurs during the action, the
        resulting exception message is returned through @handle_sb_errors.
        Failing actions such as failed hover_and_click will raise exceptions.

    When not to use:
        - Do not use this tool to click if you don't need to hover an element
          before clicking another; use 'click' instead.
    """
    sb = _get_sb()

    if timeout < 0:
        return "Error: timeout must be >= 0."

    if action == "hover":
        sb.hover_element(selector, timeout=timeout)
        return f"Hovered {selector}"

    if action == "hover_and_click":
        if not secondary_selector:
            return (
                "Error: action='hover_and_click' requires secondary_selector."
            )
        sb.hover_and_click(selector, secondary_selector, timeout=timeout)
        return f"Hovered {selector} and clicked {secondary_selector}"

    if action == "drag_and_drop":
        if not secondary_selector:
            return (
                "Error: action='drag_and_drop' requires secondary_selector."
            )
        sb.drag_and_drop(selector, secondary_selector, timeout=timeout)
        return f"Dragged {selector} onto {secondary_selector}"

    return (
        f"Error: unknown action '{action}'. "
        "Use 'hover', 'hover_and_click', or 'drag_and_drop'."
    )


@mcp.tool()
@handle_sb_errors
def type_text(
    selector: str,
    text: str = "",
    mode: Literal[
        "fill_input",
        "append",
        "fast_type",
        "set_value",
        "clear_only",
    ] = "fill_input",
    timeout: float = 5,
) -> str:
    """Enter, append, directly set, or clear a value on a page element.

    Use this tool to modify text/value fields such as inputs, textareas,
    contenteditable elements, and supported input sliders. It changes the
    target element's value or content; it does not submit a form or click
    other elements.

    Choose the mode based on the desired interaction:
    - "fill_input": Normal user-like entry; clears the existing value first.
    - "append": Preserves the existing value and adds text via keystrokes.
    - "fast_type": Clears the existing value and types without typing pauses.
    - "set_value": Sets the value directly without simulating key events;
      prefer this for fast programmatic value changes when keyboard events
      are not required.
    - "clear_only": Clears the existing value; `text` is ignored.

    The tool waits up to `timeout` seconds for the target element. If the
    target cannot be used successfully, the underlying SeleniumBase error is
    handled by `handle_sb_errors` rather than returning a success message.

    Args:
        selector: CSS or SeleniumBase selector identifying the target element.

        text: Text/value to enter or set. Ignored for "clear_only".

        mode: Interaction mode. See the mode descriptions above.

        timeout: Maximum seconds to wait for the target element.
            Must be appropriate for the page's expected load/interaction time.

    Returns:
        A confirmation message after the operation succeeds;
        otherwise the error handler returns the resulting failure.
    """
    sb = _get_sb()

    if mode == "fill_input":
        sb.type(selector, text, timeout=timeout)
    elif mode == "append":
        sb.send_keys(selector, text, timeout=timeout)
    elif mode == "fast_type":
        sb.fast_type(selector, text, timeout=timeout)
    elif mode == "set_value":
        sb.set_value(selector, text, timeout=timeout)
    elif mode == "clear_only":
        sb.clear_input(selector, timeout=timeout)
    else:
        return (
            f"Error: unknown mode '{mode}'. "
            "Use 'fill_input', 'append', 'fast_type', "
            "'set_value', or 'clear_only'."
        )

    return f"type_text(mode={mode!r}) done for {selector}"


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
    dropdowns made from div/button/list elements, use click_element
    or other element-interaction tools instead.
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
def focus_element(
    selector: str,
    action: Literal[
        "scroll_to_element",
        "focus",
        "highlight",
    ] = "scroll_to_element",
    timeout: float = 5,
) -> str:
    """Scroll to, focus, or highlight an element.

    This tool does not click, type, select, hover, or otherwise activate the
    element. Use `click_element`, `type_text`, or `hover_action` for those
    operations.

    Args:
        selector: CSS selector or SeleniumBase selector identifying the target.

        action:
            - "scroll_to_element": Scroll the element into the viewport.
            - "focus": Move keyboard focus to the element.
            - "highlight": Temporarily highlight the element for debugging or
              demonstration by changing the border color. May affect timing
              and/or reduce stealth.

        timeout: Maximum seconds to wait for the target element. Default: 5.

    If there's no matching element found within the timeout,
        then @handle_sb_errors returns details from the exception raised.
    """
    sb = _get_sb()

    if action == "scroll_to_element":
        sb.scroll_into_view(selector, timeout=timeout)
    elif action == "focus":
        sb.find_element(selector, timeout=timeout).focus()
    elif action == "highlight":
        sb.highlight(selector, timeout=timeout)
    else:
        return (
            f"Error: unknown action '{action}'. "
            "Use 'scroll_to_element', 'focus', or 'highlight'."
        )

    return f"{action} done for {selector}"


# ---------------------------------------------------------------------------
# Waiting & assertions
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def wait_for_condition(
    state: Literal[
        "present",
        "visible",
        "not_visible",
        "absent",
        "seconds_passed",
    ] = "visible",
    selector: str | None = None,
    text: str | None = None,
    timeout: float = 5,
) -> str:
    """Wait for a page condition or for a specified duration.

    Use this for synchronization when a dynamic page may need time to reach
    a condition before the next automation step. The tool blocks until the
    condition is met or the timeout expires. It does not intentionally scroll,
    click, or otherwise modify the page while waiting.

    Use check_if_condition to inspect the current state without waiting.
    Use assert_condition to verify an expected condition rather than
    synchronize with a changing page.

    When the condition is not reached before `timeout`, the underlying
    SeleniumBase wait failure is handled by the tool's error handler rather
    than returning a success confirmation.

    If `state="seconds_passed"`, `selector` and `text` are ignored and the
    tool blocks for the full `timeout` seconds.

    If `text` is supplied, `present`/`visible` wait for the text to appear,
    while `absent`/`not_visible` wait for the text to disappear.
    If no selector is supplied, text is searched within the page body.

    Args:
        state:
            - "present": Wait until the matching element exists.
            - "visible": Wait until the matching element is visible.
            - "not_visible": Wait until the matching element is not visible.
            - "absent": Wait until the matching element no longer exists.
            - "seconds_passed": Wait for the full `timeout` duration.

        selector: CSS or SeleniumBase selector for the element.
            Required unless `text` is supplied or `state="seconds_passed"`.

        text: Optional text to wait for or wait to disappear.
            With text, `present` and `visible` are equivalent,
            as are `absent` and `not_visible`.

        timeout: Maximum seconds to wait for the condition;
            for `seconds_passed`, the exact duration to wait. Must be >= 0.

    Returns:
        A success message when the requested condition is reached.
        If the condition times out or the underlying wait fails,
        the tool returns the error produced by its error handler.

    Tool selection:
        - Inspect current state immediately -> check_if_condition.
        - Wait for a state change -> wait_for_condition.
        - Verify an expectation -> assert_condition.
    """
    sb = _get_sb()

    if state != "seconds_passed" and not selector and not text:
        return (
            "Error: `selector` and `text` cannot both be empty "
            "unless 'state' is set to 'seconds_passed'."
        )

    if timeout < 0:
        return "Error: timeout must be >= 0."

    if state == "seconds_passed":
        # This ignores any values that are set for `selector` or `text`.
        sb.sleep(timeout)
        return f"Waited for {timeout}s"

    if text:
        if state in ("present", "visible"):
            sb.wait_for_text(text, selector or "body", timeout=timeout)
            return f"Text '{text}' found in {selector or 'the page'}."
        if state in ("absent", "not_visible"):
            sb.wait_for_text_not_visible(
                text, selector or "body", timeout=timeout
            )
            return f"Text '{text}' not found in {selector or 'the page'}."

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
            "Use 'present', 'visible', 'not_visible', 'absent' "
            "or 'seconds_passed'."
        )

    return f"Element {selector} reached state '{state}'."


@mcp.tool()
@handle_sb_errors
def assert_condition(
    check: Literal[
        "element_present",
        "element_visible",
        "text_visible",
        "title",
        "url",
        "url_contains",
    ] = "element_visible",
    selector: str | None = None,
    expected: str | None = None,
    exact: bool = False,
    timeout: float = 5,
) -> str:
    """Verify a browser condition and report failure as an error.

    Use this tool when an expected page state must be explicitly verified.
    It is a read-only verification operation: it does not click, type,
    navigate, scroll, or otherwise intentionally modify the page.

    Element and text assertions may block while SeleniumBase waits for the
    condition, up to `timeout` seconds. Title and URL assertions are checked
    immediately and ignore `timeout`. A failed assertion or timeout is
    handled by `handle_sb_errors` and returned as a descriptive tool error;
    it is not reported as a successful result.

    Unlike check_if_condition, this tool does not merely return whether a
    condition is true: a failed expectation is an error.
    Unlike wait_for_condition, its purpose is to verify an expectation,
    not merely synchronize with a changing page.

    Args:
        check:
            - "element_present": Verify that the selector identifies a
              present element.
            - "element_visible": Verify that the selector identifies a
              visible element.
            - "text_visible": Verify that expected text is visible within
              selector, or within the whole HTML document if selector is
              omitted.
            - "title": Verify the exact current page title immediately.
            - "url": Verify the exact current URL immediately.
            - "url_contains": Verify that the current URL contains expected
              immediately.

        selector: CSS or SeleniumBase selector for element and text checks.
            Required for element checks; optional for text_visible.

        expected: Expected text, title, or URL value. Required for
            text_visible, title, url, and url_contains.

        exact: For text_visible only, require an exact text match instead
            of a substring match.

        timeout: Maximum seconds to wait for element/text assertions.
            Must be >= 0. Ignored for title and URL assertions.

    Returns:
        A confirmation message when the assertion passes. If the assertion
        fails or times out, the error handler returns the resulting error
        instead of a success message.

    Tool selection:
        - Inspect a condition without failing -> check_if_condition.
        - Wait for a condition to become true -> wait_for_condition.
        - Verify that an expected condition is true -> assert_condition.
    """
    sb = _get_sb()

    if check in ("element_present", "element_visible") and selector is None:
        return f"Error: check='{check}' requires value for `selector`."

    if check in (
        "text_visible", "title", "url", "url_contains"
    ) and expected is None:
        return f"Error: check='{check}' requires value for `expected`."

    if check == "element_present":
        sb.assert_element(selector, timeout=timeout)
        return f"Confirmed {selector} is present."

    if check == "element_visible":
        sb.assert_element_visible(selector, timeout=timeout)
        return f"Confirmed {selector} is visible."

    if check == "text_visible":
        target = selector or "html"
        if exact:
            sb.assert_exact_text(expected, target, timeout=timeout)
        else:
            sb.assert_text(expected, target, timeout=timeout)
        return f"Confirmed visible text {expected} in {target}."

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
        "'element_visible', 'text_visible', 'title', 'url', "
        "or 'url_contains'."
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

        filename: Filesystem path used by save/load.
            Ignored for get_all and clear.

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

    Use this tool when the browser workflow needs to inspect or modify
    JavaScript Web Storage belonging to the current page origin.

    Tool selection:
        - Need localStorage/sessionStorage -> use this tool.
        - Need cookies or authentication cookies -> use manage_cookies.
        - Need arbitrary JavaScript or storage operations not covered here ->
          use run_javascript.
        - Need visible page content or HTML -> use get_content.
        - Need an element's HTML attributes -> use get_attributes.

    When not to use:
        - Do not use this tool for HTTP cookies; use manage_cookies instead.
        - Do not use this tool for arbitrary page JavaScript;
          use run_javascript when a higher-level tool is insufficient.
        - Do not use this tool to inspect values from another origin;
          storage is scoped to the current page origin.

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
def scroll_page(
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

    Notes:
        Values greater than 100 for `amount` are allowed.
        For example, 200 means approximately two viewport heights.

    Tool selection:
        - Need to reveal a specific element ->
          use 'focus_element' with action="scroll_to_element".
        - Need to scroll the page by a relative amount -> use 'scroll_page'.
    """
    sb = _get_sb()

    if direction in ("up", "down") and amount < 0:
        return "Error: `amount` cannot be negative for 'up' or 'down'."

    if direction == "up":
        sb.scroll_up(amount=amount)
        return f"Scrolled up by {amount}%."
    elif direction == "down":
        sb.scroll_down(amount=amount)
        return f"Scrolled down by {amount}%."
    elif direction == "top":
        sb.scroll_to_top()
        return "Scrolled to the top."
    elif direction == "bottom":
        sb.scroll_to_bottom()
        return "Scrolled to the bottom."
    else:
        return (
            f"Error: unknown direction '{direction}'. "
            "Use 'up', 'down', 'top', or 'bottom'."
        )


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
) -> str | dict[str, Any]:
    """Get or change browser window geometry or state.

    Args:
        action:
            - "get_rect": Return the current window position and size.
            - "set_rect": Set x, y, width, and height. All four are required.
            - "maximize": Maximize the browser window.
            - "minimize": Minimize the browser window.

        x: Horizontal screen position for "set_rect".

        y: Vertical screen position for "set_rect".

        width: Window width for "set_rect".

        height: Window height for "set_rect".

    Notes:
        Use this tool for browser-window geometry and state.
        Use `manage_tabs` for switching between browser tabs.
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
        "list_tabs",
        "open_new_tab",
        "switch_to_tab",
        "switch_to_newest_tab",
        "close_active_tab",
    ] = "list_tabs",
    url: str | None = None,
    tab_index: int | None = None,
    switch_to: bool = True,
) -> str | list[dict[str, Any]]:
    """Manage browser tabs, including opening new ones.

    Use this for listing, opening, switching, or closing tabs.
    Use `open_url` and `manage_history` for navigation within the active tab.

    Args:
        action:
            - "list_tabs": Return each tab's index, URL, and title.
              Use this to find the tab_index for "switch_to_tab".
            - "open_new_tab": Open a new tab, optionally navigating to `url`.
            - "switch_to_tab": Switch to the tab at tab_index from "list_tabs".
            - "switch_to_newest_tab": Switch to the newest tab.
            - "close_active_tab": Close the active tab. This action must be
              followed by a 'manage_tabs' action that switches to a new
              tab, such as "switch_to_tab" or "switch_to_newest_tab".

        url: URL for "open_new_tab". If not provided, "about:blank" is used.

        tab_index: Tab index from "list_tabs" that is only used for the
            "switch_to_tab" action.)

        switch_to: If using "open_new_tab", switch to the new tab when True.

    Notes:
        Tab indexes are session-relative and may change after tabs are opened
        or closed. Use "list_tabs" to get current indexes before switching
        by index.

    Error behavior:
        If there's an error during any of the tab actions, then
        @handle_sb_errors will propagate the exception as an error message.
    """
    sb = _get_sb()

    if action == "list_tabs":
        tabs = sb.get_tabs()
        return [
            {
                "index": i,
                "url": getattr(t, "url", None),
                "title": getattr(t, "title", None),
            }
            for i, t in enumerate(tabs)
        ]

    if action == "open_new_tab":
        if not url:
            url = "about:blank"
        sb.open_new_tab(url=url, switch_to=switch_to)
        return f"Opened new tab (url={url!r}, switch_to={switch_to})"

    if action == "switch_to_tab":
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

    if action == "switch_to_newest_tab":
        sb.switch_to_newest_tab()
        return "Switched to newest tab."

    if action == "close_active_tab":
        sb.close_active_tab()
        return "Closed active tab."

    return (
        f"Error: unknown action '{action}'. Use 'list_tabs', 'open_new_tab', "
        f"'switch_to_tab', 'switch_to_newest_tab', or 'close_active_tab'."
    )


# ---------------------------------------------------------------------------
# Captcha solving
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def solve_captcha() -> str:
    """Attempt a SeleniumBase CDP-based CAPTCHA interaction, such as clicking
    a CAPTCHA checkbox, or performing a drag/drop action on a slider CAPTCHA.

    This tool attempts to interact with CAPTCHA controls such as Cloudflare
    Turnstile, reCAPTCHA, hCaptcha, DataDome Slider, or FriendlyCaptcha via
    the Chrome DevTools Protocol (CDP), which is usually stealthier than
    JavaScript because CDP actions can avoid triggering `isTrusted: false`.

    This tool automatically detects the coordinates of CAPTCHA checkboxes
    for determining the correct location to perform the click. If no CAPTCHA
    is detected on the current page, then no click action is attempted.

    The tool does not guarantee that the CAPTCHA was solved. Some CAPTCHA
    controls are embedded inside shadow DOM or otherwise do not expose an
    easy success signal. A successful attempt may result in changes to page
    state or browser cookies.

    Tool workflow:
        1. Inspect the webpage with get_content when you need to
           determine whether CAPTCHA-related controls are present.
        2. Call 'solve_captcha' to attempt the CAPTCHA interaction.
        3. Use 'get_page_info', 'get_content', 'check_if_condition',
           or 'manage_cookies' to inspect resulting page/session state.

    Returns:
        A message confirming that the CAPTCHA interaction was attempted.
        The message is the same for both successful and failed attempts.
    """
    sb = _get_sb()
    sb.solve_captcha()
    return "Attempted CAPTCHA solve."


# ---------------------------------------------------------------------------
# Output & misc
# ---------------------------------------------------------------------------

@mcp.tool()
@handle_sb_errors
def save_page(
    format: Literal["screenshot", "html", "pdf"] = "screenshot",
    filename: str | None = None,
    folder: str | None = None,
) -> str:
    """Save the current browser page to a local filesystem file.

    Use this tool when the browser workflow needs a persistent file artifact
    from the current page: a PNG screenshot, the current page source as HTML,
    or a PDF representation of the current page.

    A browser session must already be running. This tool operates on the
    currently active browser tab and does not navigate, click, type, or
    otherwise modify the webpage.

    Args:
        format:
            - "screenshot": Save a PNG screenshot of the current page.
            - "html": Save the current page source as an HTML file.
            - "pdf": Save the current page as a PDF.

        filename:
            Optional output filename. If omitted, defaults to:
            - "screenshot.png" for format="screenshot"
            - "page_source.html" for format="html"
            - "page.pdf" for format="pdf"

        folder:
            Optional destination folder passed to SeleniumBase.
            If omitted, SeleniumBase uses its default output location.

    Side effects and filesystem behavior:
        This tool writes a file to the filesystem and may overwrite an
        existing file with the same output name. Only use trusted and
        authorized filesystem paths. The MCP process must have permission
        to write to the requested destination.

        The tool does not upload, publish, or transmit the saved file by
        itself. The resulting file remains in the filesystem available to
        the MCP server process.

    Error behavior:
        If the browser session is not running, the tool returns a lifecycle
        error. Filesystem, browser, or SeleniumBase failures are converted
        into descriptive MCP error results by the server's error handler.

    When not to use:
        - Do not use this tool merely to read page text or HTML; use
          get_content instead.
        - Do not use this tool when you only need page metadata such as the
          URL or title; use get_page_info instead.
        - Do not use this tool to manipulate the page; use the appropriate
          interaction tool such as click_element, type_text, or select_option.

    Returns:
        A confirmation message containing the requested output format and
        filename after the save operation succeeds.
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
    """Evaluate a JavaScript expression in the current page context.

    Use this only when the required browser operation cannot be accomplished
    through the higher-level SeleniumBase tools.

    The expression is evaluated through Chrome DevTools Protocol
    Runtime.evaluate in the currently active page. It executes with access
    to the page's JavaScript context, including DOM APIs, browser storage,
    and other same-origin page resources available to JavaScript.

    Tool selection:
        - Prefer click_element, type_text, select_option, hover_action,
          focus_element, scroll_page, and other higher-level tools for normal
          browser interactions.
        - Prefer get_content, get_attributes, and find_elements for reading
          page content or element information.
        - Prefer manage_storage for ordinary localStorage/sessionStorage
          reads and writes.
        - Prefer manage_cookies for browser cookie operations.
        - Use this tool when a required operation needs arbitrary JavaScript
          that the higher-level tools do not expose.

    Args:
        expression: A JavaScript expression or executable JavaScript code
            evaluated in the current page. It may reference standard browser
            globals such as document and window and may use DOM APIs.

            Examples:
                - "document.title"
                - "document.querySelector('button')?.textContent"
                - "localStorage.getItem('theme')"
                - "document.body.classList.contains('dark')"
                - "document.querySelector('#slider').value = '50'"

            The expression should produce a value when a result is needed.
            JavaScript that returns a Promise is supported and its resolved
            value is returned.

    Returns:
        The JavaScript evaluation result when it can be serialized and
        returned across the MCP boundary. Primitive values, arrays, plain
        objects, and null are generally suitable return values. DOM objects,
        functions, symbols, and other non-serializable JavaScript values may
        not be returned directly; extract the needed property or convert the
        value to a serializable form first.

    Security:
        This provides unrestricted JavaScript execution in the current browser
        page. It can read or modify page data and interact with the page in
        ways that bypass the higher-level tool abstractions. Only expose this
        MCP server to trusted clients.
    """
    sb = _get_sb()
    return sb.evaluate(expression)


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
