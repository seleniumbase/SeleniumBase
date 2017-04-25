## Installation instructions for Python, pip, brew, git, virtualenv, and virtualenvwrapper


### [Python 2.7](https://www.python.org/downloads/)

If you're a MAC user, that should already come preinstalled on your machine. Although Python 3 exists, you'll want Python 2 instead.

If you're a WINDOWS user, [download Python 2.7 from here](https://www.python.org/downloads/release/python-2713/).


### [Pip](https://en.wikipedia.org/wiki/Pip_%28package_manager%29)

You might already have pip installed, but if you don't:

On a MAC, run the following command:
```bash
sudo easy_install pip
```

If you're not using the latest version of pip & setuptools, you'll need to upgrade:
```bash
pip install -U pip setuptools
```

On WINDOWS, run the following command:
```bash
python -m pip install -U pip setuptools
```

If you're having any trouble with that, you can [GET PIP HERE](https://pip.pypa.io/en/latest/installing/).

When done, make sure pip is on your path. ($PATH on Mac/Linux. System Environment Variables on WINDOWS.)


### [Homebrew](http://brew.sh/) (MAC-ONLY) (OPTIONAL)

Homebrew allows you to install things more easily, such as Git, Chromedriver, and PhantomJS.

```bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
```

### [Git](http://www.git-scm.com)

(NOTE: You can download the SeleniumBase repository right from GitHub and skip all the git-related commands. That's probably the fastest way if you want to quickly get a live demo of this tool up and running.)

MAC-ONLY: (This step only works if you installed Homebrew in the previous step)
```bash
brew install git
```

(WINDOWS users: Skip the Homebrew part and [download Git here](http://git-scm.com/downloads).)

<a id="virtual_environment"></a>
### [VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) and [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

(NOTE: Virtual environments allow each your Python projects to have a unique set of packaged dependencies.)

MAC:
```bash
sudo easy_install --upgrade virtualenv
sudo easy_install --upgrade virtualenvwrapper
```

WINDOWS:
```bash
pip install --upgrade virtualenv
pip install --upgrade virtualenvwrapper-win
```
