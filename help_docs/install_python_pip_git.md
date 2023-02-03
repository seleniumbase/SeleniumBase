<!-- SeleniumBase Docs -->

## Installation instructions for ``Git``, ``Python``, and ``pip``

### [Git](http://www.git-scm.com)

You can [download Git from here](http://git-scm.com/downloads).

(<i>A Git GUI tool like [SourceTree](https://www.sourcetreeapp.com/) or [GitHub Desktop](https://desktop.github.com/) can help you with Git commands.</i>)

(You can also download SeleniumBase from GitHub without using git-related commands.)

### [Python](https://www.python.org)

You can download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) if it's not already preinstalled on your machine.

### [pip](https://en.wikipedia.org/wiki/Pip_%28package_manager%29)

**``pip`` already comes with Python!** (It lets you install packages, such as ``seleniumbase``.)

⚠️ If something went wrong with your ``pip`` installation, try this:

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

If you're having any trouble getting pip, you can [GET PIP HERE](https://pip.pypa.io/en/latest/installation/).

When done, make sure the location of pip is on your path, which is ``$PATH`` for macOS/Linux. (On Windows, it's the System Variables ``Path`` within System Environment Variables.)

You can also get pip (or fix pip) by using:

```bash
curl https://bootstrap.pypa.io/get-pip.py | python
```

* (If you get SSL errors while trying to install packages with pip, see [this Stackoverflow post](https://stackoverflow.com/questions/49768770/not-able-to-install-python-packages-ssl-tlsv1-alert-protocol-version), which tells you to run the above command.)

**Keep Pip and Setuptools up-to-date:**

```bash
python -m pip install -U pip setuptools
```

* (Depending on your user permissions, you may need to add ``--user`` to the command if you're not inside a [Python virtual environment](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md), or use "[sudo](https://en.wikipedia.org/wiki/Sudo)" on a UNIX-based OS if you're getting errors during installation.)
