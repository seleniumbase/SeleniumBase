<h2><img src="https://seleniumbase.io/img/sb_icon.png" title="SeleniumBase" width="30" /> Virtual Environment Tutorial</h2>

### Step 0: Install VirtualEnvWrapper (<i>optional</i>):

* ``virtualenvwrapper`` can make it easier to work with [Python virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) by giving you the ``mkvirtualenv`` command.

### macOS / Linux:

(*Shortcut*: Run "``source virtualenv_install.sh``" from the top-level SeleniumBase folder to perform the following steps.)

```bash
python3 -m pip install virtualenvwrapper --force-reinstall
export WORKON_HOME=$HOME/.virtualenvs
source `which virtualenvwrapper.sh`
```

If you add ``source `which virtualenvwrapper.sh` `` to your local bash file (``~/.bash_profile`` on macOS, or ``~/.bashrc`` on Linux), virtualenvwrapper commands such as ``mkvirtualenv`` will be available whenever you open a new command prompt.

### Windows:

(*Shortcut*: Run "``win_virtualenv.bat``" from the top-level SeleniumBase folder to perform the following steps.)

```bash
py -m pip install virtualenvwrapper-win --force-reinstall --user
```

### Step 1: Create a virtual environment:

### macOS / Linux:

* (Python 3) ``python3 -m venv ENV``:

```bash
python3 -m venv sbase_env
source sbase_env/bin/activate
```

* (Python 2, 3) ``mkvirtualenv ENV``:

```bash
mkvirtualenv sbase_env
```
(If you have multiple versions of Python installed on your machine, and you want your virtual environment to use a specific Python version, add ``--python=PATH_TO_PYTHON_EXE`` with the Python executable to use.)

### Windows:

* (Python 3) ``py -m venv ENV``:

```bash
py -m venv sbase_env
call sbase_env\\Scripts\\activate
```

* (Python 2, 3) ``mkvirtualenv ENV``:
```bash
mkvirtualenv sbase_env
```
(If you have multiple versions of Python installed on your machine, and you want your virtual environment to use a specific Python version, add ``--python=PATH_TO_PYTHON_EXE`` with the Python executable to use.)

---

### mkvirtualenv Commands

Creating a virtual environment:

```bash
mkvirtualenv sbase_env
```

Leaving your virtual environment:

```bash
deactivate
```

Returning to a virtual environment:

```bash
workon sbase_env
```

Listing all virtual environments:

```bash
lsvirtualenv
```

Deleting a virtual environment:

```bash
rmvirtualenv VIRTUAL_ENV_NAME
```

<br><i>[python-guide.org/en/latest/dev/virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) has more information about Python virtual environments. For specific details about VirtualEnv and VirtualEnvWrapper, see [http://virtualenv.readthedocs.org/en/latest/](http://virtualenv.readthedocs.org/en/latest/) and [http://virtualenvwrapper.readthedocs.org/en/latest/](http://virtualenvwrapper.readthedocs.org/en/latest/).</i>
