### Virtual Environment Setup Instructions

Mac: (If you're using ``virtualenv``):

```bash
mkdir -p ~/Envs
virtualenv ~/Envs/seleniumbase
source ~/Envs/seleniumbase/bin/activate
```

Mac: (If you're using ``virtualenvwrapper``):

```bash
mkvirtualenv seleniumbase
```

Windows: (Just use ``virtualenvwrapper``)

```bash
mkvirtualenv seleniumbase
```

If you ever need to leave your virtual environment, use the following command:

```bash
deactivate
```

You can always jump back in later:

(If you're using ``virtualenv``):
```bash
source ~/Envs/seleniumbase/bin/activate
```

(If you're using ``virtualenvwrapper``):
```bash
workon seleniumbase
```
