<!-- SeleniumBase Docs -->

<h2><a href="https://github.com/seleniumbase/SeleniumBase/"><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32"></a> SeleniumBase Installation</h2>

<h4>If installing <code>seleniumbase</code> directly from <a href="https://pypi.python.org/pypi/seleniumbase">PyPI</a>, (the Python Package Index), use:</h4>

```zsh
pip install seleniumbase
```

<h4>To upgrade an existing <code>seleniumbase</code> install from PyPI:</h4>

```zsh
pip install -U seleniumbase
```

<h4>If installing <code>seleniumbase</code> from a Git clone, use:</h4>

```zsh
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install .
```

<h4>For a development mode install in editable mode, use:</h4>

```zsh
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install -e .
```

<h4>To upgrade an existing <code>seleniumbase</code> install from GitHub:</h4>

```zsh
git pull  # To pull the latest version
pip install -e .  # Or "pip install ."
```

<h4>If installing <code>seleniumbase</code> from a <a href="https://github.com/seleniumbase/SeleniumBase">GitHub branch</a>, use:</h4>

```zsh
pip install git+https://github.com/seleniumbase/SeleniumBase.git@master#egg=seleniumbase
```

<h3><code>pip install</code> can be customized:</h3>

* (Add ``--upgrade`` OR ``-U`` to upgrade SeleniumBase.)
* (Add ``--force-reinstall`` to upgrade indirect libraries.)

(If you're not using a virtual environment, you may need to add ``--user`` to your ``pip`` command if you're seeing errors during installation.)

--------

[<img src="https://seleniumbase.github.io/cdn/img/sb_logo_10t.png" title="SeleniumBase" width="290" />](https://github.com/seleniumbase/SeleniumBase/)
