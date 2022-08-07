## [<img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) SeleniumBase Installation

<h4>If installing SeleniumBase directly from <a href="https://pypi.python.org/pypi/seleniumbase">PyPI</a>, (the Python Package Index), use:</h4>

```bash
pip install seleniumbase
```

To upgrade an existing ``seleniumbase`` install from PyPI:

```bash
pip install -U seleniumbase
```

<h4>If installing SeleniumBase from a Git clone, use:</h4>

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install .
```

<h4>For a development mode install in editable mode, use:</h4>

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install -e .
```

To upgrade an existing ``seleniumbase`` install from GitHub:

```bash
git pull  # To pull the latest version
pip install -e .  # Or "pip install ."
```

<h4>If installing SeleniumBase from a <a href="https://github.com/seleniumbase/SeleniumBase">GitHub branch</a>, use:</h4>

```bash
pip install git+https://github.com/seleniumbase/SeleniumBase.git@master#egg=seleniumbase
```

<h3><code>pip install</code> can be customized:</h3>

* (Add ``--upgrade`` OR ``-U`` to upgrade SeleniumBase.)
* (Add ``--force-reinstall`` to upgrade dependencies.)
* (Add ``--index-url=http://pypi.python.org/simple/`` if blocked by a VPN.)
* (Use ``pip3`` if multiple versions of Python are present.)

(If you're not using a virtual environment, you may need to add <code>--user</code> to your <code>pip</code> command if you're seeing errors during installation.)

--------

[<img src="https://seleniumbase.io/cdn/img/sb_logo_10t.png" title="SeleniumBase" width="200">](https://github.com/seleniumbase/SeleniumBase/)
