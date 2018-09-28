## Installation instructions for Python, pip, brew, git, virtualenv, and virtualenvwrapper

### [Python 2.7 or 3.*](https://www.python.org/downloads/)

If you're a MAC user, Python should already come preinstalled on your machine. You can use both Python 2.7 or Python 3.6+ with SeleniumBase. If you're on a MAC and have [Homebrew](https://brew.sh/) installed, you can use: ``brew install python3`` to install Python 3. Or you can just get everything from [https://www.python.org/downloads/](https://www.python.org/downloads/).

For MAC, there's also the official docs.python-guide.org instructions here: [Installing Python 2 on Mac OS X](https://docs.python-guide.org/starting/install/osx/) and [Installing Python 3 on Mac OS X](https://docs.python-guide.org/starting/install3/osx/#install3-osx).

If you're a WINDOWS user, [download Python 2.7 from here](https://www.python.org/downloads/release/python-2713/) OR [download Python 3.6.6 from here](https://www.python.org/downloads/release/python-366/).

### [Pip](https://en.wikipedia.org/wiki/Pip_%28package_manager%29)

You might already have pip and setuptools installed, but if you don't:

On MAC / Windows / Linux, run the following command:
```bash
python -m ensurepip --default-pip
```

If your existing version of pip is old, upgrade to the latest version:
```bash
python -m pip install --upgrade pip setuptools
```

On CentOS 7 and some versions of Linux, you may need to install pip with ``yum``:
```bash
yum -y update
yum -y install python-pip
```

If you're having any trouble getting pip, you can [GET PIP HERE](https://pip.pypa.io/en/latest/installing/).

When done, make sure the location of pip is on your path, which is `$PATH` for Mac/Linux. (On Windows, it's the System Variables `Path` within System Environment Variables. Ex: Add "C:/Python27/Scripts/" to the end of the `Path` variable.)

You can also get pip (or fix pip) by using:
```bash
curl https://bootstrap.pypa.io/get-pip.py | python
```

(If you get SSL errors while trying to install packages with pip, see [this Stackoverflow post](https://stackoverflow.com/questions/49768770/not-able-to-install-python-packages-ssl-tlsv1-alert-protocol-version), which tells you to run the above command.)

### [Homebrew](http://brew.sh/) (MAC-ONLY) (OPTIONAL)

The Homebrew package manager allows you to install things more easily on MacOS, such as Git and Chromedriver.

Here's the command line script to install Homebrew (*from [https://brew.sh/](https://brew.sh/)*):
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
If you haven't updated Homebrew in awhile, you probably should. Here's how:
```bash
brew update
```

### [Git](http://www.git-scm.com)

You can [download Git from here](http://git-scm.com/downloads).

MAC-ONLY shortcut: (This step only works if you installed Homebrew in the previous step)
```bash
brew install git
```

(You can also download the SeleniumBase repository right from GitHub and skip all the git-related commands.)

<a id="virtual_environment"></a>
### [VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) and [VirtualEnvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

Virtual environments allow each your Python projects to have a unique set of packaged dependencies.

To learn how to create a Python virtual environment, [see this ReadMe](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md).
