## Installation Instructions for Python, pip, brew, git, and virtualenv (or virtualenvwrapper)


### [Python 2.7](https://www.python.org/downloads/)

If you're a MAC user, that should already come preinstalled on your machine. Although Python 3 exists, you'll want Python 2 (both of these major versions are being improved in parallel). Python 2.7.10 is the one I've been using on my Mac.

If you're a WINDOWS user, [download the latest 2.* version from here](https://www.python.org/downloads/release/python-2710/).

### [Pip](https://en.wikipedia.org/wiki/Pip_%28package_manager%29)

If "pip" did not come with your Python installation, you can [GET PIP HERE](https://pip.pypa.io/en/latest/installing/).

On a Mac, you can also install pip easily with the following command:
```bash
sudo easy_install pip
```
Then make sure it's on your path.

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

### [Virtualenv](http://virtualenv.readthedocs.org/en/latest/) or [Virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

Mac: (The old regular way):

```bash
sudo easy_install virtualenv
```

Mac: (The new fancy way):

```bash
sudo easy_install virtualenvwrapper
```

Windows:

```bash
pip install virtualenv
```
