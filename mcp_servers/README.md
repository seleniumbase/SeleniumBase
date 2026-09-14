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
* `open_url`
* `manage_history`
* `get_page_info`
* `find_elements`
* `get_content`
* `get_attributes`
* `check_if_condition`
* `click_element`
* `hover_action`
* `type_text`
* `select_option`
* `focus_element`
* `wait_for_condition`
* `assert_condition`
* `manage_cookies`
* `manage_storage`
* `scroll_page`
* `manage_window`
* `manage_tabs`
* `solve_captcha`
* `save_page`
* `run_javascript`

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

## Selectors

Most tools accept a `selector` argument. Behavior varies slightly by tool, so check a tool's own docstring when it matters:

- **CSS selectors** are preferred and supported by every tool that takes a selector.
- **XPath** is accepted by several (not all) tools. Some tools go through SeleniumBase's XPath-to-CSS conversion first; expressions that can't be converted (e.g. `contains(...)`) aren't supported by those tools.
- **SeleniumBase's visible-text selector** syntax, e.g. `a:contains("Sign in")`, is accepted by several tools (including `click_element`, when not using `all_matches`) but not all of them — `find_elements`, for example, only supports CSS/XPath.

## Tools exposed

Tools here are grouped around a shared `selector` convention. Several near-identical one-off tools (e.g. separate click/hover/drag/wait/cookie/storage variants) have been consolidated into a single tool with a `mode`/`action`/`state`/`check` parameter, so there are fewer near-neighbor tools to disambiguate between while every underlying capability stays available. Tool names also follow a verb+object convention (`click_element`, `focus_element`, `scroll_page`, `save_page`, `open_url`) rather than bare verbs, so a tool's name signals what it acts on without needing to read its description.

| Group             | Tool(s)                                                                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------  |
| Session           | `start_browser(url, headless, use_chromium, browser_executable_path, incognito, guest, ad_block, proxy)`, `close_browser`                          |
| Navigation        | `open_url`, `manage_history(action: back/forward/reload/list)`, `get_page_info` (running status, url, title, origin, user agent in one call)       |
| Finding & reading | `find_elements(selector, timeout, include_html)`, `get_content(selector, output_format: text/html/urls, timeout)`, `get_attributes(selector, attribute, timeout)`, `check_if_condition(check: present/visible, text)` |
| Interacting       | `click_element(selector, nth, all_matches, only_if_visible, parent_selector, timeout, scroll)`, `hover_action(selector1, selector2, action: hover/hover_and_click/drag_and_drop)`, `type_text(mode: fill_input/append/fast_type/set_value/clear_only)`, `select_option(by: text/value/index)`, `focus_element(action: scroll_to_element/focus/highlight, timeout)` |
| Waiting           | `wait_for_condition(state: present/visible/not_visible/absent/seconds_passed, text)`                                                               |
| Assertions        | `assert_condition(check: element_present/element_visible/text_visible/title/url/url_contains)`                                                     |
| Cookies & storage | `manage_cookies(action: get_all/clear/save/load)`, `manage_storage(storage: local/session, action: get/set)`                                       |
| Scrolling         | `scroll_page(direction: up/down/top/bottom, amount)`                                                                                                |
| Windows & tabs    | `manage_window(action: get_rect/set_rect/maximize/minimize)`, `manage_tabs(action: list_tabs/open_new_tab/switch_to_tab/switch_to_newest_tab/close_active_tab)`                   |
| Captcha           | `solve_captcha`                                                                                                                                    |
| Output & misc     | `save_page(format: screenshot/html/pdf)`, `run_javascript`                                                                                          |

## Design notes / things to adapt for your use case

- **Single global session.** The server holds one browser session at a time. This matches how MCP servers are typically launched (one process per client connection) and keeps the tool surface simple. If you need multiple concurrent browser tabs/sessions, you'd extend this to a dict of named sessions and add a `session_id` parameter to each tool.

- **Blocking calls.** SeleniumBase's calls are synchronous and will block the server while a page loads or an element is waited on. For a single-user local tool this is fine; for a multi-client server you'd want to run them in a thread pool via `asyncio.to_thread`.

- **`start_browser` retries once before failing.** If the first launch attempt raises, it's retried once automatically before returning an error. This was added after seeing occasional first-attempt failures when testing against Glama's MCP Inspector; it costs nothing on the common case where the first launch already succeeds.

- **Two error-handling paths, by design.** Most failures (a selector isn't found, an assertion fails, an invalid `action`/`mode`/`check` value is passed) are caught by the `handle_sb_errors` decorator and returned as a descriptive string, e.g. `Error in click_element: NoSuchElementException - ...`, so the calling agent can read the failure and self-correct. There's one deliberate exception: calling any tool other than `start_browser`/`close_browser` when no browser session is running raises `ToolError` (via the shared `_get_sb()` helper) instead of returning a string. `handle_sb_errors` explicitly re-raises `ToolError` rather than catching it, so this surfaces to the MCP client as a real tool-call error (`is_error=True`), not as ordinary text the agent has to pattern-match on. `start_browser` and `close_browser` handle their own lifecycle errors directly (e.g. "already running", a failed `quit()`) and also return strings rather than raising.

- **`find_elements` catches its own lookup failures.** Its default `timeout` is 0.5 seconds (not 5, unlike most other tools here). A failed or empty lookup never raises: no matches returns `{"count": 0, "matches": []}`, and an actual lookup error (e.g. an unsupported selector) returns `{"count": 0, "matches": [], "error": "<details>"}` — the error lives inside the returned dict rather than surfacing as a top-level string from `handle_sb_errors`. Pass a longer `timeout` explicitly if the elements you're looking for may still be loading.

- **Hover, hover-and-click, and drag-and-drop share one tool.** In `hover_action(selector1, selector2, action)`, `action="hover"` (the default) hovers `selector1` only; `action="hover_and_click"` hovers `selector1` then clicks `selector2` (useful for dropdown/submenu items revealed by hovering); `action="drag_and_drop"` drags `selector1` onto `selector2`. (`selector2` is required when `action` is `"hover_and_click"` or `"drag_and_drop"`.)

- **`scroll_page`'s `amount` isn't capped at 100.** Relative up/down scrolling by more than 100% of the viewport height is allowed (e.g. `amount=200` scrolls roughly two viewport heights); negative amounts are rejected for `"up"`/`"down"`.

- **Elements don't cross the wire as handles.** In native CDP Mode, `find_element()` returns a live object with its own methods (`el.click()`, `el.get_html()`, ...). MCP tools can only return JSON-serializable data, so `find_elements` resolves each match immediately to a plain dict (`tag_name`, `text`, and optionally `html`) instead of returning a handle you could call further methods on. If you need to act on one of several matches, use `click_element(selector, nth=...)` (acts by position) rather than "find, then click" as two separate steps.

- **CAPTCHA-solving.** `solve_captcha` attempts to detect and interact with several challenge types over CDP (e.g. Cloudflare Turnstile, reCAPTCHA, hCaptcha, DataDome Slider, FriendlyCaptcha), including slider-style drag interactions, without guaranteeing success.

- **Security.** `run_javascript` runs arbitrary JS, and `manage_storage` can expose authentication/session secrets; `manage_cookies` and `save_page` accept filenames/folders that can touch the filesystem. This server can also drive a real browser to real sites — don't expose it over an untrusted network transport; stdio + local trust (the default here) is the safe setup.

## Extending

Adding a tool is just adding a `@mcp.tool()`-decorated function (wrapped in `handle_sb_errors`) that calls the matching `sb_cdp.Chrome` method — SeleniumBase has methods for file uploads, network conditions, and more that aren't wrapped above yet.
