### Virtual Environment Setup Instructions

#### First install [VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) or [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) (<i>if not installed</i>):

MAC / Linux:
```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper
```

WINDOWS:
```bash
python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper-win
```

#### Now use VirtualEnv or VirtualEnvWrapper to create a virtual environment:

MAC:

(If using ``virtualenv``):

```bash
mkdir -p ~/Envs
virtualenv ~/Envs/seleniumbase
source ~/Envs/seleniumbase/bin/activate
```

(If using ``virtualenvwrapper``):

```bash
mkvirtualenv seleniumbase
```

WINDOWS:

```bash
mkvirtualenv seleniumbase
```

If you ever need to leave your virtual environment, use the following command:

```bash
deactivate
```

You can always jump back into your virtual environment later:

(If using ``virtualenv``):
```bash
source ~/Envs/seleniumbase/bin/activate
```

(If using ``virtualenvwrapper``):
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

<br><br><i>[python-guide.org/en/latest/dev/virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/) has more information about Python virtual environments.</i>
