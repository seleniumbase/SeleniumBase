## ![http://seleniumbase.com](https://cdn2.hubspot.net/hubfs/100006/images/super_logo_tiny.png "SeleniumBase") SeleniumBase Installation

If you're installing SeleniumBase from a cloned copy on your machine, use:
```
pip install -r requirements.txt

python setup.py develop
```

If you're installing SeleniumBase from the [Python Package Index](https://pypi.python.org/pypi/seleniumbase), use:
```bash
pip install seleniumbase
```

If you're installing SeleniumBase directly from GitHub, use:
```bash
pip install -e git+https://github.com/seleniumbase/SeleniumBase.git@master#egg=seleniumbase
```

(If you already have an older version installed, you may want to add ``--upgrade`` to your ``pip`` command to update existing Python packages. If you're not using a virtual environment, you may need to add ``--user`` to your ``pip`` command if you're getting errors during installation.)

(If you want to use Python 3.x instead of Python 2.7, use ``pip3`` in place of ``pip`` and ``python3`` in place of ``python``.)
