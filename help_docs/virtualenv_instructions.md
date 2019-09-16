## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Virtual Environment Tutorial

### **Step 1**: Install VirtualEnv and VirtualEnvWrapper:

### macOS / Linux:

(*Shortcut*: Run "``source virtualenv_install.sh``" from the top-level SeleniumBase folder to perform the following steps.)

```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source `which virtualenvwrapper.sh`
```

If you add ``source `which virtualenvwrapper.sh` `` to your local bash file (``~/.bash_profile`` on macOS, or ``~/.bashrc`` on Linux), virtualenvwrapper commands such as ``mkvirtualenv`` will be available whenever you open a new command prompt.

### Windows:

(*Shortcut*: Run "``virtualenv_install.bat``" from the top-level SeleniumBase folder to perform the following steps.)

```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper-win
```

### **Step 2**: Create a virtual environment:

### macOS / Linux / Windows:

* Using ``mkvirtualenv``:
```bash
mkvirtualenv seleniumbase_venv
```
(If you have multiple versions of Python installed on your machine, and you want your virtual environment to use a specific Python version, add ``--python=PATH_TO_PYTHON_EXE`` with the Python executable to use.)

* Using ``virtualenv``:
```bash
virtualenv seleniumbase_venv
source seleniumbase_venv/bin/activate
```

* (Python 3) Using ``mvenv``:
```bash
python3 -mvenv seleniumbase_venv
source seleniumbase_venv/bin/activate
```

---

If you ever need to leave your virtual environment, use the following command:

```bash
deactivate
```

You can always jump back into your virtual environment later:

```bash
workon seleniumbase_venv
```

To list all existing virtual environments:

```bash
lsvirtualenv
```

To delete a virtual environment:

```bash
rmvirtualenv VIRTUAL_ENV_NAME
```

<br><i>[python-guide.org/en/latest/dev/virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) has more information about Python virtual environments. For specific details about VirtualEnv and VirtualEnvWrapper, see [http://virtualenv.readthedocs.org/en/latest/](http://virtualenv.readthedocs.org/en/latest/) and [http://virtualenvwrapper.readthedocs.org/en/latest/](http://virtualenvwrapper.readthedocs.org/en/latest/).</i>
