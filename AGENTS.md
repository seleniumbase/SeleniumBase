# AGENTS.md

Guidance for AI coding agents working in the SeleniumBase repository.

## Project overview

SeleniumBase is a Python framework for browser automation, end-to-end testing,
web scraping, and bot-detection avoidance. It wraps Selenium/WebDriver and adds:

- **`BaseCase`**: a `unittest.TestCase` subclass used with `pytest` / `pynose` (`self.click(...)`, `self.type(...)`, etc.)
- **`SB()`** context manager and **`Driver()`** manager: for plain `python` scripts
- **UC Mode** (undetected-chromedriver) and **CDP Mode** (`sb_cdp`, `sb.activate_cdp_mode()`): stealth automation on Chromium browsers, including Stealthy Playwright integration
- CLI tools (`seleniumbase` / `sbase`), Recorder, Dashboard, Commander GUI, MasterQA, Presenter, ChartMaker, CasePlans, and `behave` (Gherkin) support

Language: Python (~99%). License: MIT. Docs: https://seleniumbase.io

## Repository layout

| Path | What it is |
| --- | --- |
| `seleniumbase/` | The main package. Core library code lives here (fixtures/`BaseCase`, plugins/pytest plugin, config/settings, console scripts, CDP/UC code, drivers, etc.) |
| `sbase/` | Thin alias package so `sbase` works as a CLI/import name. Rarely needs edits |
| `examples/` | 150+ runnable examples and tests; also serves as the project's main regression suite |
| `examples/cdp_mode/` | CDP Mode, Pure CDP (`sb_cdp`), and Stealthy Playwright examples |
| `help_docs/` | Markdown docs (method summary, CDP methods, syntax formats, options, etc.) |
| `mkdocs_build/`, `mkdocs.yml` | Documentation site build for seleniumbase.io |
| `integrations/` | CI/CD and cloud setup examples (GitHub Actions, Jenkins, Azure, GCP) |
| `.github/` | Workflows and issue/PR templates |
| `pytest.ini`, `setup.cfg`, `pyproject.toml`, `setup.py`, `requirements.txt` | Packaging and test configuration |

Confirm exact module locations by browsing the tree before editing. Do not assume file names from memory.

## Setup

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
python -m venv .venv && source .venv/bin/activate   # a virtualenv is recommended
pip install -e .
seleniumbase --help                                  # or: sbase --help (verifies the install)
```

- Webdrivers (e.g. `chromedriver`) are downloaded automatically on first use, so network access is needed the first time. Manual fetch: `sbase get chromedriver`.
- Google Chrome is the default browser. Unbranded Chromium and Chrome-for-Testing are auto-installed if needed.
- After pulling upstream changes, re-run `pip install -e .`.

## Running tests

Tests are run from inside `examples/` (which has its own `pytest.ini`):

```bash
cd examples/
pytest my_first_test.py                 # run one file
pytest test_demo_site.py::DemoSiteTests::test_demo_site   # run one test (FILE::CLASS::METHOD)
pytest --co -q                          # dry run: list what would be collected
pytest my_first_test.py --headless      # no visible browser (good for CI/sandboxes)
pytest my_first_test.py --demo          # slow, highlighted actions for debugging
pytest test_suite.py --rs --headless    # reuse one browser session
```

Useful options: `-x` (stop on first failure), `-n=NUM` (parallel), `--browser=firefox|edge|...`,
`--uc` (UC Mode), `--html=report.html`, `--dashboard`, `--reruns=N`, `--pdb` / `--trace` (never in CI).

Things to know:

- **Most tests need a real browser and live websites.** They can fail from network problems, site changes, or bot-detection rather than from your changes. Run the smallest relevant test(s), not the whole `examples/` folder, and use `--headless` when no display is available.
- `test_fail.py` and parts of `test_suite.py` **fail on purpose** to demonstrate logging. Do not "fix" them.
- Files named `raw_*.py` are run with plain `python`, not `pytest`.
- Tests using the `sb` pytest fixture only work with `pytest`.
- Failure logs and screenshots go to `latest_logs/` (older ones to `archived_logs/`). Do not commit these.
- Test discovery: files matching `test_*.py` or `*_test.py`; methods starting with `test_`.

## Code style and conventions

- Match the surrounding code. This is a large, long-lived codebase; avoid drive-by reformatting or unrelated refactors.
- Follow the repo's flake8/PEP 8 configuration (see `setup.cfg` / CI config). Python lines follow the default flake8 settings, e.g. the 79-character limit.
- Keep Python version compatibility with what `setup.py` / `pyproject.toml` declare as supported. Don't use syntax newer than the minimum supported version.
- Public API naming: prefer the current names (`goto`, not `open`; `sb.goto(...)` in CDP Mode). Older aliases are kept for backwards compatibility. Don't remove or rename public methods without a strong reason.
- Selectors: CSS selectors by default; XPath is auto-detected. `:contains("text")` is supported in SeleniumBase selectors.
- Prefer built-in SeleniumBase methods (automatic waits, clean errors) over raw `self.driver` calls. Use raw WebDriver only when no SeleniumBase method exists.
- Avoid `time.sleep()` in library code; use the framework's wait methods and timeouts. `self.sleep()` is acceptable in demo/example scripts.
- Do not add heavy new dependencies. Any dependency change must be reflected in `requirements.txt`, `setup.py`, and `pyproject.toml` as applicable.

## Making changes

**Adding or changing a public method**

1. Implement it in the relevant module under `seleniumbase/`. Where the method exists in more than one API surface (e.g. `BaseCase`, `SB`/`Driver`, CDP Mode `sb_cdp`), keep them consistent.
2. Add or update an example/test in `examples/` (CDP examples in `examples/cdp_mode/`).
3. Update the relevant doc in `help_docs/` (e.g. `method_summary.md`, `cdp_mode_methods.md`), and `README.md` only if it's a headline feature.
4. If the change is user-visible, note it in `CHANGELOG.md` only if maintainers' convention for the release requires it. Check recent entries first.

**Adding a command-line option**

Options are defined in the pytest plugin (`seleniumbase/plugins/pytest_plugin.py`) and mirrored elsewhere (pynose plugin, `behave` support, `sb_manager` / `SB()` args, docs in `help_docs/customizing_test_runs.md`, and the `options` console script). Update every place the option surfaces.

**Docs**

Docs are Markdown in `help_docs/` and `examples/**/ReadMe.md`. Keep links relative to GitHub `master` consistent with existing ones.

## Stealth / bot-detection code: extra care

UC Mode and CDP Mode are among the project's most actively developed and most fragile areas.

- Small changes to launch flags, driver patching, timing, or CDP calls can silently break stealth on real sites. Test against the bot-detection examples (e.g. `examples/cdp_mode/raw_cdp_browserscan.py`, `raw_gitlab.py`) in **headed** mode where possible.
- Don't add code whose purpose is to help users abuse, attack, or harm third-party sites. Legitimate automation, testing, and scraping use cases are the scope.
- Be conservative with anything touching CAPTCHA handling (`solve_captcha`), proxies, and user-agent handling.

## Safety and hygiene

- **Never commit secrets**: proxy credentials, API keys, 2FA keys, DB or S3 credentials (these can live in `settings.py` / custom settings files). Use placeholders.
- Don't commit generated artifacts: `latest_logs/`, `archived_logs/`, `downloaded_files/`, `dashboard.html`, `report.html`, `__pycache__/`, downloaded drivers in `seleniumbase/drivers/`.
- Don't hit third-party sites in a loop or at load. Keep example scripts polite and short.
- Avoid destructive shell commands outside the repo directory. Browser profiles and driver folders can be large; clean up test-created folders you generate.

## Pull request checklist

- [ ] Change is focused and minimal; no unrelated formatting churn
- [ ] Relevant examples run locally (`pytest <file> --headless` or plain `python` for `raw_*.py`)
- [ ] flake8-clean for touched files
- [ ] New/changed public behavior has an example and doc update
- [ ] No secrets, logs, or generated files included
- [ ] See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` for project policy

## Useful references

- Docs site: https://seleniumbase.io
- Method summary: `help_docs/method_summary.md`
- CDP Mode methods: `help_docs/cdp_mode_methods.md`
- CDP Mode guide: `examples/cdp_mode/ReadMe.md`
- Syntax formats (BaseCase / SB / Driver / sb fixture / sb_cdp): `help_docs/syntax_formats.md`
- CLI options: `help_docs/customizing_test_runs.md`
- UC Mode: `help_docs/uc_mode.md`
- Console scripts: `seleniumbase/console_scripts/ReadMe.md`
