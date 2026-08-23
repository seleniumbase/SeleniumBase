# mcp_servers

Exposes [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) browser automation as tools over the [Model Context Protocol](https://modelcontextprotocol.io), so any
MCP client can drive a real browser.

This folder has a single server, `server.py`, built on SeleniumBase's
[Pure CDP Mode](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/cdp_mode_methods.md)
(`seleniumbase.sb_cdp.Chrome`) — the browser is driven entirely over the
Chrome DevTools Protocol, no WebDriver in the loop at all, which makes it
SeleniumBase's stealthiest mode and includes captcha-solving. That's the
mode most people reaching for browser automation from an MCP client
actually want, so it's the one MCP server included in this repo.

Other SeleniumBase automation styles — `Driver()` (WebDriver-based) and
`SB()` (broadest API, including UC Mode stealth, MFA codes, file
downloads) — have their own MCP servers too, just not here. They live in
[seleniumbase/seleniumbase-mcp](https://github.com/seleniumbase/seleniumbase-mcp)
as a separate repo, to keep this one simple and unambiguous: one server,
one name, one obvious thing it does.

Defaults to `headless=False` — the browser window is visible unless you
pass `headless=True` when starting a session.

## 1. Install

There are two ways to get the `seleniumbase-mcp` command, depending on
whether you just want to *use* the server or you're developing this repo.

**If you just want to use the server (simplest — no repo clone needed):**

```bash
pip install "seleniumbase[mcp]"
```

That's it. This installs `seleniumbase` from PyPI along with the `mcp[cli]`
extra, and registers a `seleniumbase-mcp` console-script command — the
same one `[project.scripts]`/`setup.py` wire up either way, just via a
real released package instead of a local checkout. Skip straight to step 2
or 3/4 below; you don't need `uv`, and your MCP client config can be as
simple as `{"command": "seleniumbase-mcp"}` (see step 3's Option A).

**If you're working from a `git clone` of this repo instead of a PyPI install:**

(Requires [uv](https://docs.astral.sh/uv/getting-started/installation/))

This folder lives inside the SeleniumBase repo, so if you've already
cloned SeleniumBase, just `cd` into this folder and sync:

```bash
cd mcp_servers
uv sync
```

`uv sync` reads `pyproject.toml`, creates a `.venv/` in this folder, and
installs `mcp[cli]` plus `seleniumbase` — the latter resolved from the
local SeleniumBase checkout one directory up (in editable mode, via
`[tool.uv.sources]` in `pyproject.toml`), not from PyPI. It also installs
this project itself, which registers a `seleniumbase-mcp` console-script
command via `[project.scripts]`, pointing at `server.py`'s `main()`
function (`mcp.run(transport="stdio")`). This is what lets `uv run
seleniumbase-mcp` — no python path, no venv path, no script path — work
as the MCP client command in steps 3 and 4 below.


Pure CDP Mode doesn't use WebDriver, so no `chromedriver` download is
needed — just a working Chrome/Chromium install.

(No `uv`? `python3 -m venv venv && pip install -r requirements.txt` works
too — `requirements.txt` installs the local SeleniumBase checkout via
`-e ..` the same way. Substitute `python server.py` for `uv run
seleniumbase-mcp` everywhere below, and use absolute `venv/bin/python` +
script path in your MCP client config instead of the path-free options.)

## 2. Try it standalone (optional sanity check)

```bash
uv run mcp dev server.py
```

That opens the MCP Inspector, where you can test commands ("Tools").
Ctrl+C to exit. The real test is wiring it into a client (next step).

## 3. Connect it to Claude Desktop

Claude Desktop doesn't run from a "project" directory the way Claude Code
does, so a bare `uv run seleniumbase-mcp` isn't guaranteed to find this
folder. Two ways to get a stable config:

**Option A — global install (recommended, zero paths anywhere):**

```bash
uv tool install .    # from inside this folder, installs the command globally
```

This puts `seleniumbase-mcp` on your `PATH` permanently (run `uv tool
ensurepath` once if it warns that its bin directory isn't on `PATH` yet).
Then `claude_desktop_config.json` can be just:

```json
{
  "mcpServers": {
    "seleniumbase-mcp": { "command": "seleniumbase-mcp" }
  }
}
```

Note this bakes in the location of the SeleniumBase checkout at install
time (since `seleniumbase` resolves to `../` via the editable path
source) — if you move or delete this clone, re-run `uv tool install .`
from its new location.

**Option B — point `uv` at this folder directly (one absolute path, but no
venv/interpreter path to track down, and no separate install step):**

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

Restart Claude Desktop. You should see a 🔨 tools icon indicating the
server connected, with tools like `start_browser`, `navigate`, `click`,
etc. available.

## 4. Connect it to Claude Code

This folder's `.mcp.json` is checked in and ready to use as-is — no path
editing required, because `uv run seleniumbase-mcp` resolves this project
from `pyproject.toml` in the current directory:

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

**Where does `.mcp.json` go — here, or the SeleniumBase repo root?** It
stays here, in `mcp_servers/`, not at the repo root, for two reasons:

1. Claude Code auto-loads `.mcp.json` from whatever directory you launch
   `claude` in. If it lived at the repo root, every contributor running
   Claude Code anywhere in the (large, mostly unrelated) SeleniumBase
   monorepo would have this browser-automation server silently
   registered — not something a random contributor fixing a docs typo is
   expecting or wants prompted about.
2. `uv run seleniumbase-mcp` needs `pyproject.toml` to be discoverable
   from the current directory. That resolves cleanly when `.mcp.json` and
   `pyproject.toml` sit next to each other in `mcp_servers/`; from the
   repo root it would need `uv --directory mcp_servers run
   seleniumbase-mcp` instead (an absolute or relative path baked into the
   command).

So: run `claude` from inside `mcp_servers/` to get it auto-loaded. If you
want repo-root convenience too, you can add an opt-in `.mcp.json` at the
SeleniumBase root using the `--directory mcp_servers` form (same idea as
Option B above, with a relative path) — just know that doing so makes
this server available by default in every root-level Claude Code session
across the whole repo, which the maintainers may or may not want.

If you'd rather register it manually instead of relying on `.mcp.json`:

```bash
claude mcp add seleniumbase-mcp -- uv run seleniumbase-mcp
```

(run from inside this folder, for the same reason as above.)

## Tools exposed

| Group             | Examples                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Session           | `start_browser(url, headless, incognito, guest, proxy, ad_block)`, `close_browser`                                                                |
| Navigation        | `navigate`, `reload_page`, `go_back`/`go_forward`, `get_current_url`, `get_title`                                                                 |
| Finding & reading | `find_element_info`, `find_all_info`, `get_text`, `get_html_source`, `get_element_attribute(s)`, `is_element_present/visible`                     |
| Interacting       | `click`, `click_if_visible`, `click_visible_elements`, `type_text`, `send_keys`, `set_value`, `select_option_by_text/value/index`, `nested_click` |
| Waiting           | `wait_for_element`, `wait_for_element_visible/not_visible/absent`, `wait_for_text`                                                                |
| Assertions        | `assert_element`, `assert_text`, `assert_exact_text`, `assert_title`, `assert_url(_contains)`                                                     |
| Cookies & storage | `get_all_cookies`, `save_cookies`/`load_cookies`, `get/set_local_storage_item`, `get/set_session_storage_item`                                    |
| Scrolling         | `scroll_into_view`, `scroll_to_top/bottom`, `scroll_up/down`                                                                                      |
| Tabs & windows    | `open_new_tab`, `switch_to_tab`/`switch_to_newest_tab`, `close_active_tab`, `maximize`/`minimize`, `get/set_window_rect`                          |
| Captcha           | `solve_captcha`                                                                                                                                   |
| Output            | `save_screenshot`, `save_page_source`, `save_as_pdf`, `evaluate` (run JS)                                                                         |

## Design notes / things to adapt for your use case

- **Single global session.** The server holds one browser session at a
  time. This matches how MCP servers are typically launched (one process
  per client connection) and keeps the tool surface simple. If you need
  multiple concurrent browser tabs/sessions, you'd extend this to a
  dict of named sessions and add a `session_id` parameter to each tool.

- **Blocking calls.** SeleniumBase's calls are synchronous and will block
  the server while a page loads or an element is waited on. For a
  single-user local tool this is fine; for a multi-client server you'd
  want to run them in a thread pool via `asyncio.to_thread`.

- **Errors surface as tool errors.** If a selector isn't found or an
  assertion fails, `sb_cdp.Chrome` raises an exception, which the MCP SDK
  turns into a tool error the client sees and can react to (e.g. by
  waiting longer or trying a different selector).

- **Elements don't cross the wire as handles.** In native CDP Mode,
  `find_element()` returns a live object with its own methods
  (`el.click()`, `el.get_html()`, ...). MCP tools can only return
  JSON-serializable data, so `find_element_info`/`find_all_info` resolve
  the element immediately to a plain dict (`tag_name`, `text`, `html`)
  instead of returning a handle you could call further methods on. If you
  need to act on one of several matches, use `click_nth_element` (acts by
  position) rather than "find, then click" as two separate steps.

- **Captcha solving isn't universal.** `solve_captcha` handles supported
  challenge types (e.g. Cloudflare Turnstile); not a guaranteed bypass
  for every type of CAPTCHA.

- **Security.** `evaluate` runs arbitrary JS and this server can drive a
  real browser to real sites — don't expose it over an untrusted network
  transport; stdio + local trust (the default here) is the safe setup.

## Extending

Adding a tool is just adding a `@mcp.tool()`-decorated function that calls
the matching `sb_cdp.Chrome` method — SeleniumBase has methods for file
uploads, drag-and-drop, hovering, network conditions, and more that aren't
wrapped above yet.
