<h3 align="left"><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/README.md"><img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_m.png" title="SeleniumBase" height="48" /></a></h3>

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3.png" title="SeleniumBase" height="32"> Multi-Language Tests (Python 3 Only!)

**SeleniumBase** supports the following 10 languages:
* English
* Chinese / 中文
* Dutch / Nederlands
* French / Français
* Italian / Italiano
* Japanese / 日本語
* Korean / 한국어
* Portuguese / Português
* Russian / Русский
* Spanish / Español

Multi-language tests are run with **pytest** like any other test. Every test method has a one-to-one mapping to every other supported language. Example:
 ``self.open(URL)`` = ``self.开启网址(URL)``

--------

You can use SeleniumBase to translate any test from one language to another by using the console scripts interface:

```bash
seleniumbase translate
```

```
* Usage:
seleniumbase translate [SB_FILE].py [LANGUAGE] [ACTION]

* Languages:
``--en`` / ``--English``  |  ``--zh`` / ``--Chinese``
``--nl`` / ``--Dutch``    |  ``--fr`` / ``--French``
``--it`` / ``--Italian``  |  ``--ja`` / ``--Japanese``
``--ko`` / ``--Korean``   |  ``--pt`` / ``--Portuguese``
``--ru`` / ``--Russian``  |  ``--es`` / ``--Spanish``

* Actions:
``-p`` / ``--print``  (Print translation output to the screen)
``-o`` / ``--overwrite``  (Overwrite the file being translated)
``-c`` / ``--copy``  (Copy the translation to a new ``.py`` file)

* Examples:
Translate test_1.py into Chinese and only print the output:
>>> seleniumbase translate test_1.py --zh  -p
Translate test_2.py into Portuguese and overwrite the file:
>>> seleniumbase translate test_2.py --pt  -o
Translate test_3.py into Dutch and make a copy of the file:
>>> seleniumbase translate test_3.py --nl  -c

* Output:
Translates a SeleniumBase Python file into the language
specified. Method calls and ``import`` lines get swapped.
Both a language and an action must be specified.
The ``-p`` action can be paired with one other action.
When running with ``-c`` (or ``--copy``) the new file name
will be the orginal name appended with an underscore
plus the 2-letter language code of the new language.
(Example: Translating ``test_1.py`` into Japanese with
``-c`` will create a new file called ``test_1_ja.py``.)
```
