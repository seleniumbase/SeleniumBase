<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) SeleniumBase Commander 🎖️

🎖️ <b>SeleniumBase Commander</b> lets you run <code>pytest</code> scripts from a Desktop GUI.<br>

🎖️ To launch it, call ``sbase commander`` or ``sbase gui``:

```bash
sbase gui
* Starting the SeleniumBase Commander Desktop App...
```

<img src="https://seleniumbase.github.io/cdn/img/sbase_commander_wide.png" title="SeleniumBase Commander" width="600">

🎖️ <b>SeleniumBase Commander</b> loads the same tests that are found by:

```bash
pytest --co -q
```

🎖️ You can customize which tests are loaded by passing additional args:

```bash
sbase commander [OPTIONAL PATH or TEST FILE]
sbase gui [OPTIONAL PATH or TEST FILE]
```

🎖️ Here are examples of customizing test collection:

```bash
sbase gui
sbase gui -k agent
sbase gui -m marker2
sbase gui test_suite.py
sbase gui offline_examples/
```

🎖️ Once launched, you can further customize which tests to run and what settings to use. There are various controls for changing settings, modes, and other pytest command line options that are specific to SeleniumBase. You can also set additional options that don't have a visible toggle. When you're ready to run the selected tests with the specified options, click on the <code>Run Selected Tests</code> button.

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Other SeleniumBase Commanders:</h3>

* 🐝🎖️ [SeleniumBase Behave GUI / Commander](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/behave_gui.md)

<a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/behave_gui.md"><img src="https://seleniumbase.github.io/cdn/img/sbase_behave_gui_wide_5.png" title="SeleniumBase Behave GUI" width="400"></a>

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
