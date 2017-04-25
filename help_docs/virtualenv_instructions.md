### Virtual Environment Setup Instructions

* If you haven't yet installed ``virtualenv`` or ``virtualenvwrapper``, **[follow these instructions first](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/requirements_installation.md#virtual_environment)**.

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
