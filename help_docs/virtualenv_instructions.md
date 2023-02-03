<!-- SeleniumBase Docs -->

## Virtual Environment Tutorial

There are multiple ways of creating a **[Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)**. This tutorial covers two of those:

* The ``venv`` command (<i>included with Python 3+</i>).
* The virtualenvwrapper ``mkvirtualenv`` command.

``venv`` creates virtual environments in the location where run (<i>generally with Python projects</i>).

``mkvirtualenv`` creates virtual environments in one place (<i>generally in your home directory</i>).

(The [Python Software Foundation](https://www.python.org/psf/) recommends ``venv`` for creating virtual environments.)


<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Option 1: Using "venv"</h3>

> macOS/Linux terminal (``python3 -m venv ENV``)

```bash
python3 -m venv sbase_env
source sbase_env/bin/activate
```

> Windows CMD prompt (``py -m venv ENV``):

```bash
py -m venv sbase_env
call sbase_env\\Scripts\\activate
```

To exit a virtual env, type ``deactivate``.

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Option 2: Using virtualenvwrapper</h3>

> macOS/Linux terminal:

```bash
python3 -m pip install virtualenvwrapper --force-reinstall
export WORKON_HOME=$HOME/.virtualenvs
source `which virtualenvwrapper.sh`
```

(*Shortcut*: Run ``source virtualenv_install.sh`` from the top-level SeleniumBase folder to perform the above steps.)

(If you add ``source `which virtualenvwrapper.sh` `` to your local bash file (``~/.bash_profile`` on macOS, or ``~/.bashrc`` on Linux), virtualenvwrapper commands such as ``mkvirtualenv`` will be available whenever you open a new command prompt.)

> Windows CMD prompt:

```bash
py -m pip install virtualenvwrapper-win --force-reinstall --user
```

(*Shortcut*: Run ``win_virtualenv.bat`` from the top-level SeleniumBase folder to perform the above step.)


<h3>Create a virtual environment:</h3>

* ``mkvirtualenv ENV``:

```bash
mkvirtualenv sbase_env
```

(If you have multiple versions of Python installed on your machine, and you want your virtual environment to use a specific Python version, add ``--python=PATH_TO_PYTHON_EXE`` to your ``mkvirtualenv`` command with the Python executable to use.)


<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> virtualenvwrapper commands:</h3>

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
workon
```

Deleting a virtual environment:

```bash
rmvirtualenv sbase_env
```

--------

If the ``python`` and ``python3`` versions don't match (*while in a virtualenv on macOS or Linux*), the following command will sync the versions:

```bash
alias python=python3
```

(To remove an alias, use: ``unalias NAME``)

--------

To verify the ``python`` version, use:

```bash
python --version
```

To see the PATH of your ``python`` (macOS/Linux), use:

```bash
which python
```

--------

> <i>[python-guide.org/en/latest/dev/virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) has more information about Python virtual environments. For specific details about VirtualEnv and VirtualEnvWrapper, see [http://virtualenv.readthedocs.org/en/latest/](http://virtualenv.readthedocs.org/en/latest/) and [http://virtualenvwrapper.readthedocs.org/en/latest/](http://virtualenvwrapper.readthedocs.org/en/latest/).</i>
