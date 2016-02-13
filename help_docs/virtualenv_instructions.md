### Virtual Environment Setup Instructions

Mac: (If you're using virtualenv):

```bash
mkdir -p ~/Envs
virtualenv ~/Envs/seleniumbase
source ~/Envs/seleniumbase/bin/activate
```

Mac: (If you're using virtualenvwrapper):

```bash
mkvirtualenv seleniumbase
```

Windows:

Use the "virtualenv" version above instead of "mkvirtualenv", but also make the following changes:
1: Don't use "-p"
2: Replace "~/" from above with the location of your home directory
3: Instead of using the "source" command, go into the folder created and type ``activate``

If you ever need to leave your virtual environment, use the following command:

```bash
deactivate
```

You can always jump back in later:

(If you're using virtualenv):
```bash
source ~/Envs/seleniumbase/bin/activate
```

(If you're using virtualenvwrapper):
```bash
workon seleniumbase
```
