### Virtual Environment Setup Instructions

#### First install [VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) or [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) (<i>if not installed</i>):

MAC / Linux:
```bash
sudo easy_install --upgrade virtualenv
sudo easy_install --upgrade virtualenvwrapper
```

WINDOWS:
```bash
pip install --upgrade virtualenv
pip install --upgrade virtualenvwrapper-win
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
