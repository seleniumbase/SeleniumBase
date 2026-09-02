<!-- SeleniumBase Docs -->

# `seleniumbase-mcp`

### The [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) MCP server provides stealthy browser automation over the [Model Context Protocol](https://modelcontextprotocol.io) for MCP clients.

This server, (located in `server.py`), uses SeleniumBase's [Pure CDP Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/cdp_mode_methods.md) (`seleniumbase.sb_cdp.Chrome`), where the browser is driven entirely over the Chrome DevTools Protocol, and there is no WebDriver in the loop at all, which makes it SeleniumBase's stealthiest mode. CAPTCHA-solving is included via the `solve_captcha()` method!

Other SeleniumBase automation styles, (such as `Driver()` and `SB()`),  have their own MCP servers in [seleniumbase/seleniumbase-mcp](https://github.com/seleniumbase/seleniumbase-mcp).

`headless` defaults to `None` in `start_browser`, which resolves to headless on Linux (typical for server/container environments) and headed on Windows/macOS. Pass `headless=True` or `headless=False` explicitly to override this for any OS; headless mode may be less stealthy.

## 1. Install

There are two ways to get the `seleniumbase-mcp` command:

**If you just want to use the server (simplest — no repo clone needed):**

```bash
pip install "seleniumbase[mcp]"
```

This installs `seleniumbase` from PyPI along with the `mcp[cli]` extra, and registers a `seleniumbase-mcp` console-script command. Your MCP client config can be as simple as `{"command": "seleniumbase-mcp"}` (see step 3's Option A).

**If you're working from a `git clone` of this repo (instead of a PyPI install):**

(Requires [uv](https://docs.astral.sh/uv/getting-started/installation/))

This folder lives inside the SeleniumBase repo, so if you've already cloned SeleniumBase, just `cd` into this folder and sync:

```bash
cd mcp_servers
uv sync
```

`uv sync` reads `pyproject.toml`, creates a `.venv/` in this folder, and installs `mcp[cli]` plus `seleniumbase`, which is resolved from the local SeleniumBase checkout one directory up (in editable mode, via `[tool.uv.sources]` in `pyproject.toml`), not from PyPI. It also installs this project itself, which registers a `seleniumbase-mcp` console-script command via `[project.scripts]`, pointing at `server.py`'s `main()` function (`mcp.run(transport="stdio")`). That's what lets `uv run seleniumbase-mcp` work as the MCP client command in steps 3 and 4 below.

Pure CDP Mode doesn't use WebDriver, so no `chromedriver` download is needed... just a working Chrome/Chromium install.

(No `uv`? `python3 -m venv venv && pip install -r requirements.txt` works too. `requirements.txt` installs the local SeleniumBase checkout via `-e .` the same way. Substitute `python server.py` for `uv run seleniumbase-mcp` everywhere below, and use absolute `venv/bin/python` + script path in your MCP client config instead of the path-free options.)

## 2. Try it standalone (optional sanity check)

```bash
uv run mcp dev server.py
```

That opens the MCP Inspector, where you can test commands ("Tools"). Ctrl+C to exit. Next step is wiring it into a client.

## 3. Connect it to Claude Desktop

Claude Desktop doesn't run from a "project" directory the way Claude Code does, so a bare `uv run seleniumbase-mcp` isn't guaranteed to find this folder. Two ways to get a stable config:

**Option A — global install (recommended, zero paths anywhere):**

```bash
uv tool install .    # from inside this folder, installs the command globally
```

This puts `seleniumbase-mcp` on your `PATH` permanently (run `uv tool ensurepath` once if it warns that its bin directory isn't on `PATH` yet). Then `claude_desktop_config.json` can be just:

```json
{
  "mcpServers": {
    "seleniumbase-mcp": { "command": "seleniumbase-mcp" }
  }
}
```

Note this bakes in the location of the SeleniumBase checkout at install time (since `seleniumbase` resolves to `../` via the editable path source). If you move or delete this clone, re-run `uv tool install .` from its new location.

**Option B — point `uv` at this folder directly (one absolute path, but no venv/interpreter path to track down, and no separate install step):**

```json
{
  "mcpServers": {
    "seleniumbase-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/SeleniumBase/mcp_servers", "run", "seleniumbase-mcp"]
    }
  }
}
```

The location of `claude_desktop_config.json` depends on your system:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop. You should see a 🔨 tools icon indicating the server connected, with the following MCP tools available through the tools interface:

* `start_browser`
* `close_browser`
* `navigate`
* `navigate_history`
* `get_page_info`
* `find_elements`
* `get_content`
* `get_attributes`
* `check_for_condition`
* `click`
* `hover_with_action`
* `type_text`
* `select_option`
* `focus_on`
* `wait_for`
* `assert_condition`
* `manage_cookies`
* `manage_storage`
* `scroll`
* `manage_window`
* `manage_tabs`
* `solve_captcha`
* `save_output`
* `run_javascript`
* `wait_seconds`

## 4. Connect it to Claude Code

This folder's `.mcp.json` is checked in and ready to use as-is.
No path editing is required because `uv run seleniumbase-mcp` resolves this project from `pyproject.toml` in the current directory:

```json
{
  "mcpServers": {
    "seleniumbase-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "seleniumbase-mcp"]
    }
  }
}
```

**The `.mcp.json` file helps clients connect to the MCP server.**

1. Claude Code auto-loads `.mcp.json` from whatever directory you launch `claude` in.
2. `uv run seleniumbase-mcp` needs `pyproject.toml` to be discoverable from the current directory. That resolves cleanly when `.mcp.json` and `pyproject.toml` sit next to each other.

Run `claude` from inside `mcp_servers/` or the root folder to get it auto-loaded.

If you'd rather register it manually instead of relying on `.mcp.json`:

```bash
claude mcp add seleniumbase-mcp -- uv run seleniumbase-mcp
```

(run from inside this folder, for the same reason as above.)

## Tools exposed

Tools here are grouped around a shared `selector` convention: `selector` args accept a CSS selector, or visible text (e.g. `a:contains("Sign in")`). Several near-identical one-off tools (e.g. separate click/hover/drag/wait/cookie/storage variants) have been consolidated into a single tool with a `mode`/`action`/`state`/`check` parameter, so there are fewer near-neighbor tools to disambiguate between while every underlying capability stays available.

| Group             | Tool(s)                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Session           | `start_browser(url, headless, use_chromium, browser_executable_path, incognito, guest, ad_block, proxy)`, `close_browser`                        |
| Navigation        | `navigate`, `navigate_history(action: back/forward/reload)`, `get_page_info` (running status, url, title, origin, user agent, history in one call) |
| Finding & reading | `find_elements(selector, timeout, include_html)`, `get_content(selector, output_format: text/html/urls, include_shadow_dom)`, `get_attributes`, `check_for_condition(check: present/visible/count/text_visible)` |
| Interacting       | `click(selector, nth, all_matches, only_if_visible, parent_selector, timeout, scroll)`, `hover_with_action(selector1, selector2, action: none/click/drag_and_drop)`, `type_text(mode: fill_input/append/fast_type/set_value/clear_only)`, `select_option(by: text/value/index)`, `focus_on(action: scroll_to_element/focus/highlight)` |
| Waiting           | `wait_for(state: present/visible/not_visible/absent, text)`                                                                                        |
| Assertions        | `assert_condition(check: element_present/element_visible/text_visible/title/url/url_contains)`                                                     |
| Cookies & storage | `manage_cookies(action: get_all/clear/save/load)`, `manage_storage(storage: local/session, action: get/set)`                                       |
| Scrolling         | `scroll(direction: up/down/top/bottom, amount)`                                                                                                    |
| Windows & tabs    | `manage_window(action: get_rect/set_rect/maximize/minimize)`, `manage_tabs(action: list/open/switch/switch_newest/close_active)`                   |
| Captcha           | `solve_captcha`                                                                                                                                    |
| Output & misc     | `save_output(format: screenshot/html/pdf)`, `run_javascript`, `wait_seconds`                                                                        |

## Design notes / things to adapt for your use case

- **Single global session.** The server holds one browser session at a time. This matches how MCP servers are typically launched (one process per client connection) and keeps the tool surface simple. If you need multiple concurrent browser tabs/sessions, you'd extend this to a dict of named sessions and add a `session_id` parameter to each tool.

- **Blocking calls.** SeleniumBase's calls are synchronous and will block the server while a page loads or an element is waited on. For a single-user local tool this is fine; for a multi-client server you'd want to run them in a thread pool via `asyncio.to_thread`.

- **Errors surface as descriptive strings.** Every tool (aside from session-lifecycle tools, which handle their own errors) is wrapped by a `handle_sb_errors` decorator: if a selector isn't found or an assertion fails, `sb_cdp.Chrome` raises an exception, and the decorator catches it and returns a string like `Error in click: NoSuchElementException - ...` instead of a raw tool error. This lets the calling agent read the failure and self-correct (e.g. by waiting longer or trying a different selector) rather than just seeing an opaque tool-call failure.

- **No standalone session-status tool.** There is no separate `browser_status`-style tool. `get_page_info` doubles as the status check: it returns `{"running": False}` (optionally with an `error` field) when there's no active session or the session errors out, and full page metadata (`running: True`, `url`, `title`, `origin`, `user_agent`, `history`) otherwise.

- **Content reading is consolidated into one tool.** `get_content` replaces what used to be three separate reads: page/element text, page/element HTML, and page-linked URLs. Pick the mode with `output_format` (`"text"`, `"html"`, or `"urls"`) rather than calling a dedicated `get_page_content` or `get_all_urls` tool — those no longer exist. Likewise, there's no standalone `get_user_agent` tool anymore; the User-Agent string is one of the fields returned by `get_page_info`.

- **Hover, click-after-hover, and drag-and-drop share one tool.** `hover_with_action(selector1, selector2, action)` replaces the earlier separate `hover` and `drag_and_drop` tools. `action="none"` hovers `selector1` only; `action="click"` hovers `selector1` then clicks `selector2` (useful for dropdown/submenu items revealed by hovering); `action="drag_and_drop"` drags `selector1` onto `selector2`. (`selector2` is required when `action` is `"click"` or `"drag_and_drop"`.)

- **Non-activating element actions are `focus_on`.** What used to be `act_on_element` is now `focus_on(selector, action)`, with actions `scroll_to_element` (the default), `focus`, and `highlight` — note the default action changed from focusing the element to scrolling it into view. None of these actions click, type into, select from, or otherwise activate the element; use `click`, `type_text`, `select_option`, or `hover_with_action` for that.

- **Elements don't cross the wire as handles.** In native CDP Mode, `find_element()` returns a live object with its own methods (`el.click()`, `el.get_html()`, ...). MCP tools can only return JSON-serializable data, so `find_elements` resolves each match immediately to a plain dict (`tag_name`, `text`, and optionally `html`) instead of returning a handle you could call further methods on. If you need to act on one of several matches, use `click(selector, nth=...)` (acts by position) rather than "find, then click" as two separate steps.

- **CAPTCHA-solving.** `solve_captcha` handles supported challenge types (e.g. Cloudflare Turnstile).

- **Security.** `run_javascript` runs arbitrary JS, and `manage_storage` can expose authentication/session secrets; `manage_cookies` and `save_output` accept filenames/folders that can touch the filesystem. This server can also drive a real browser to real sites — don't expose it over an untrusted network transport; stdio + local trust (the default here) is the safe setup.

## Extending

Adding a tool is just adding a `@mcp.tool()`-decorated function (wrapped in `handle_sb_errors`) that calls the matching `sb_cdp.Chrome` method — SeleniumBase has methods for file uploads, network conditions, and more that aren't wrapped above yet.
