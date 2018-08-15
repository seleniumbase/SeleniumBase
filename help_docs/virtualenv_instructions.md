## Virtual Environment Tutorial

### **Step 1**: First install [VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) and [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) (<i>if not installed</i>):

### MAC / Linux:

```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

If you add ``source /usr/local/bin/virtualenvwrapper.sh`` to your local bash file (``~/.bash_profile`` on a Mac, or ``~/.bashrc`` on Linux), virtualenvwrapper commands will be available whenever you open a new command prompt.

### WINDOWS:

```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper-win
```

### **Step 2**: Now use VirtualEnv or VirtualEnvWrapper to create a virtual environment:

### MAC / Linux / WINDOWS:

```bash
mkvirtualenv seleniumbase
```

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
