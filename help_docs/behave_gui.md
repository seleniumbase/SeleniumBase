<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) SeleniumBase Behave GUI / Commander 🐝🎖️

🐝🎖️ The <b>SeleniumBase Behave GUI</b> lets you run <code>behave</code> scripts from a Desktop GUI.<br>

🐝🎖️ To launch it, call ``sbase behave-gui`` or ``sbase gui-behave``:

```bash
> sbase behave-gui
* Starting the SeleniumBase Behave Commander GUI App...
```

<img src="https://seleniumbase.github.io/cdn/img/sbase_behave_gui_wide_5.png" title="SeleniumBase Behave GUI" width="600">

🐝🎖️ <b>SeleniumBase Behave GUI</b> loads the same tests that are found by:

```bash
behave -d
```

🐝🎖️ You can customize which tests are loaded by passing additional args:

```bash
sbase behave-gui [OPTIONAL PATH or TEST FILE]
```

🐝🎖️ Here are examples of customizing test collection:

```bash
sbase behave-gui  # all tests
sbase behave-gui -i=calculator  # tests with "calculator" in the name
sbase behave-gui features/  # tests located in the "features/" folder
sbase behave-gui features/calculator.feature  # tests in that feature
```

🐝🎖️ Once launched, you can further customize which tests to run and what settings to use. There are various controls for changing settings, modes, and other "behave" command line options that are specific to SeleniumBase. You can also set additional options that don't have a visible toggle. When you're ready to run the selected tests with the specified options, click on the <code>Run Selected Tests</code> button.

🐝⚪ With the Dashboard enabled, you'll get one of these:

<img src="https://seleniumbase.github.io/cdn/img/sb_behave_dashboard.png" title="SeleniumBase" width="600">

--------

<div>To learn more about SeleniumBase, check out the Docs Site:</div>
<a href="https://seleniumbase.io">
<img src="https://img.shields.io/badge/docs-%20%20SeleniumBase.io-11BBDD.svg" alt="SeleniumBase.io Docs" /></a>

<div>All the code is on GitHub:</div>
<a href="https://github.com/seleniumbase/SeleniumBase">
<img src="https://img.shields.io/badge/✅%20💛%20View%20Code-on%20GitHub%20🌎%20🚀-02A79E.svg" alt="SeleniumBase on GitHub" /></a>
