## Installation instructions for Git, Python, and Pip

### [Git](http://www.git-scm.com)

You can [download Git from here](http://git-scm.com/downloads).

(<i>A Git GUI tool like [SourceTree](https://www.sourcetreeapp.com/) or [GitHub Desktop](https://desktop.github.com/) can help you with Git commands.</i>)

(You can also download SeleniumBase from GitHub without using git-related commands.)

### [Python 2.7 or 3.x](https://www.python.org/downloads/)

#### macOS:

Python should already come preinstalled. You can use both Python 2.7 or Python 3.6+ with SeleniumBase. If you have [Homebrew](https://brew.sh/) installed, you can use: ``brew install python3`` to install Python 3. Or you can just get everything from [https://www.python.org/downloads/](https://www.python.org/downloads/).

The official docs.python-guide.org instructions here: [Installing Python 2 on Mac OS X](https://docs.python-guide.org/starting/install/osx/) and [Installing Python 3 on Mac OS X](https://docs.python-guide.org/starting/install3/osx/#install3-osx). (NOTE: Apple has rebranded OS X as macOS but this has not been reflected in the official docs.python-guide.org instructions yet.)

#### Windows:

You can [download Python 2.7 from here](https://www.python.org/downloads/release/python-2713/) OR [download Python 3.6.6 from here](https://www.python.org/downloads/release/python-366/).

### [Pip](https://en.wikipedia.org/wiki/Pip_%28package_manager%29)

You might already have pip and setuptools installed, but if you don't:

On macOS / Windows / Linux, run the following command:
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

When done, make sure the location of pip is on your path, which is `$PATH` for macOS/Linux. (On Windows, it's the System Variables `Path` within System Environment Variables. Ex: Add "C:/Python27/Scripts/" to the end of the `Path` variable.)

You can also get pip (or fix pip) by using:
```bash
curl https://bootstrap.pypa.io/get-pip.py | python
```
* (If you get SSL errors while trying to install packages with pip, see [this Stackoverflow post](https://stackoverflow.com/questions/49768770/not-able-to-install-python-packages-ssl-tlsv1-alert-protocol-version), which tells you to run the above command.)

**Keep Pip and Setuptools up-to-date:**
```
python -m pip install -U pip setuptools
```
* (Depending on your user permissions, you may need to add ``--user`` to the command if you're not inside a [Python virtual environment](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md), or use "[sudo](https://en.wikipedia.org/wiki/Sudo)" on a UNIX-based OS if you're getting errors during installation.)
