<!-- SeleniumBase Docs -->

## Virtual Environment Tutorial

There are multiple ways of creating a **[Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)**. This tutorial covers three of those:

* The `venv` command.
* The virtualenvwrapper `mkvirtualenv` command.
* The [uv](https://docs.astral.sh/uv/) commands: `uv venv` and `uv sync`.

`venv` creates virtual environments in the location where run (<i>generally with Python projects</i>).

`mkvirtualenv` creates virtual environments in one place (<i>generally in your home directory</i>).

`uv venv` creates virtual environments in the location where run (<i>like `venv`, but faster</i>).

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Option 1: Using "venv"</h3>

> macOS/Linux terminal (`python3 -m venv ENV`)

```zsh
python3 -m venv sbase_env
source sbase_env/bin/activate
```

> Windows CMD prompt (`py -m venv ENV`):

```zsh
py -m venv sbase_env
call sbase_env\\Scripts\\activate
```

To exit a virtual env, type `deactivate`.

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Option 2: Using virtualenvwrapper</h3>

> macOS/Linux terminal:

```zsh
python3 -m pip install virtualenvwrapper --force-reinstall
export WORKON_HOME=$HOME/.virtualenvs
source `which virtualenvwrapper.sh`
```

(*Shortcut*: Run `source virtualenv_install.sh` from the top-level SeleniumBase folder to perform the above steps.)

(If you add ``source `which virtualenvwrapper.sh` `` to your local bash file (`~/.bash_profile` on macOS, or `~/.bashrc` on Linux), virtualenvwrapper commands such as `mkvirtualenv` will be available whenever you open a new command prompt.)

> Windows CMD prompt:

```zsh
py -m pip install virtualenvwrapper-win --force-reinstall --user
```

(*Shortcut*: Run `win_virtualenv.bat` from the top-level SeleniumBase folder to perform the above step.)


<h3>Create a virtual environment:</h3>

* `mkvirtualenv ENV`.

```zsh
mkvirtualenv sbase_env
```

(If you have multiple versions of Python installed on your machine, and you want your virtual environment to use a specific Python version, add `--python=PATH_TO_PYTHON_EXE` to your `mkvirtualenv` command with the Python executable to use.)

<h4>Leave your current virtual environment:</h4>

```zsh
deactivate
```

<h4>Return to an existing virtual environment:</h4>

```zsh
workon sbase_env
```

<h4>List all virtual environments:</h4>

```zsh
workon
```

<h4>Delete a virtual environment:</h4>

```zsh
rmvirtualenv sbase_env
```

--------

<h3><img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32" /> Option 3: Using <code>uv</code></h3>

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager that can also create virtual environments.

> Install uv (macOS/Linux terminal):

```zsh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> Install uv (Windows PowerShell):

```zsh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

(uv can also be installed with `pip install uv`, or with `pip install seleniumbase[uv]`. See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for more options.)

<h3>Create a virtual environment with <b><code>uv venv</code></b>:</h3>

> macOS/Linux terminal:

```zsh
uv venv sbase_env
source sbase_env/bin/activate
```

> Windows CMD prompt:

```zsh
uv venv sbase_env
call sbase_env\\Scripts\\activate
```

(If you don't provide a name, `uv venv` creates a virtual environment named `.venv` in the current directory.)

Once the virtual environment is active, install SeleniumBase with `uv pip`:

```zsh
uv pip install seleniumbase
```

(*Note*: Virtual environments created with `uv venv` don't include `pip` by default. SeleniumBase lists `pip` as a dependency, so it gets installed along with SeleniumBase. For other projects, use `uv pip install ...` in place of `pip install ...`, or create the environment with `uv venv --seed sbase_env` to include `pip` from the start.)

If you want your virtual environment to use a specific Python version, add `--python` to your `uv venv` command. uv can download that Python version for you if it isn't installed yet:

```zsh
uv venv --python 3.15 sbase_env
```

(To install a Python version without creating a virtual environment, use: `uv python install 3.15`.)

To exit a virtual env, type `deactivate`.

To delete a virtual env, remove its folder (`rm -rf sbase_env` on macOS/Linux, or `rmdir /s /q sbase_env` on Windows CMD).


<h3>Work from a local clone with <code>uv sync</code>:</h3>

If you've cloned the SeleniumBase repo and want to work on it locally, `uv sync` can create the virtual environment and install the dependencies in a single step:

```zsh
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase
uv sync
```

`uv sync` creates a `.venv` folder in the top-level SeleniumBase folder (if one doesn't exist yet), installs the dependencies listed in `setup.py`, and installs SeleniumBase itself in editable mode, so changes to your local files take effect right away. It also writes a `uv.lock` file that records the exact versions that were resolved.

You can activate the environment as usual:

```zsh
source .venv/bin/activate
```

(On Windows CMD: `call .venv\\Scripts\\activate`)

Or skip activation and use `uv run` to run commands inside the environment:

```zsh
uv run sbase --help
uv run pytest examples/my_first_test.py
```

To update the environment after pulling new changes, run `uv sync` again.

To use a specific Python version, add `--python`:

```zsh
uv sync --python 3.15
```

<h3>Optional extras with <code>uv sync</code>:</h3>

SeleniumBase defines several optional extras in `setup.py`. Add the ones you need with `--extra`:

```zsh
uv sync --extra mcp
uv sync --extra pillow --extra pdfminer
```

To install all of them at once:

```zsh
uv sync --all-extras
```

Available extras: `allure`, `coverage`, `flake8`, `mcp`, `mss`, `pdfminer`, `pillow`, `pip-system-certs`, `playwright`, `proxy`, `pyautogui`, and `uv`.

(In an environment that was created with `uv venv`, the `pip` equivalent is `uv pip install -e ".[mcp]"`.)

--------

If the `python` and `python3` versions don't match (*while in a virtualenv on macOS or Linux*), the following command will sync the versions:

```zsh
alias python=python3
```

(To remove an alias, use: `unalias NAME`. Note that setting an alias is temporary for the current shell session. Users should add `alias python=python3` to their shell profile (`~/.zshrc` or `~/.bashrc`) if they want it to persist across terminal restarts.)

--------

To verify the `python` version, use:

```zsh
python --version
```

To see the PATH of your `python` (macOS/Linux), use:

```zsh
which python
```

--------

> <i>[python-guide.org/en/latest/dev/virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) has more information about Python virtual environments. For specific details about VirtualEnv and VirtualEnvWrapper, see [http://virtualenv.readthedocs.org/en/latest/](http://virtualenv.readthedocs.org/en/latest/) and [http://virtualenvwrapper.readthedocs.org/en/latest/](http://virtualenvwrapper.readthedocs.org/en/latest/). For uv, see [docs.astral.sh/uv](https://docs.astral.sh/uv/).</i>
