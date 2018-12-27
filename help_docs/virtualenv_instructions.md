## Virtual Environment Tutorial

### **Step 1**: First install [VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) and [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) (<i>if not installed</i>):

### MAC / Linux:

(*Shortcut*: Run "``source virtualenv_install.sh``" from the top-level SeleniumBase folder to perform the following steps.)

```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper
source `which virtualenvwrapper.sh`
export WORKON_HOME=$HOME/.virtualenvs
```

If you add ``source `which virtualenvwrapper.sh` `` to your local bash file (``~/.bash_profile`` on a Mac, or ``~/.bashrc`` on Linux), virtualenvwrapper commands such as ``mkvirtualenv`` will be available whenever you open a new command prompt.

### WINDOWS:

(*Shortcut*: Run "``virtualenv_install.bat``" from the top-level SeleniumBase folder to perform the following steps.)

```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper-win
```

### **Step 2**: Now use VirtualEnv or VirtualEnvWrapper to create a virtual environment:

### MAC / Linux / WINDOWS:

```bash
mkvirtualenv seleniumbase
```
(If you have multiple versions of Python installed on your machine, and you want your virtual environment to use a specific Python version, add ``--python=PATH_TO_PYTHON_EXE`` with the Python executable to use.)

---

If you ever need to leave your virtual environment, use the following command:

```bash
deactivate
```

You can always jump back into your virtual environment later:

```bash
workon seleniumbase
```

To list all existing virtual environments:

```bash
lsvirtualenv
```

To delete a virtual environment:

```bash
rmvirtualenv VIRTUAL_ENV_NAME
```

<br><i>[python-guide.org/en/latest/dev/virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) has more information about Python virtual environments.</i>
