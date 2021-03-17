## Using [seleniumbase/common](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/common) methods.

### Part 1: Decorators - (from [decorators.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/common/decorators.py))

#### Use these Python decorators with your test methods as needed:

* @retry_on_exception(tries=6, delay=1, backoff=2, max_delay=32)

* @rate_limited(max_per_second)

Example demonstrating a rate-limited printing functionality:
```python
import unittest
from seleniumbase import decorators


class MyTestClass(unittest.TestCase):

    @decorators.rate_limited(3.5)  # The arg is max calls per second
    def print_item(self, item):
        print(item)

    def test_rate_limited_printing(self):
        print("\nRunning rate-limited print test:")
        for item in range(1, 11):
            self.print_item(item)
```

### Part 2: String/Password Obfuscation, Encryption, and Decryption

#### Intro:

Often in your tests, you may need to login to a website to perform testing. This generally means storing passwords in plaintext formats. For security reasons, that may not be an optimal solution. For this reason, encryption/obfuscation tools have been built here to help you mask your passwords in your tests. It's not a bulletproof solution, but it can keep anyone looking over your shoulder during test creation from getting your login passwords if they don't have your encryption key, which is stored in a separate file.

#### Usage:

* First, set your custom encryption/decryption key in your local clone of [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py). (If you modify the key later, you'll need to encrypt all your passwords again.)

* Next, use [obfuscate.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/common/obfuscate.py) to obfuscate/encrypt passwords into coded strings:
```bash
python obfuscate.py

Enter password to obfuscate: (CTRL+C to exit)
Password: *********
Verify password:
Password: *********

Here is the obfuscated password:
$^*ENCRYPT=RXlYMSJWTz8HSwM=?&#$
```
(You can also use [unobfuscate.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/common/unobfuscate.py) to encrypt passwords without having them masked while typing them. Or you can use it to decrypt an obfuscated password.)

* Finally, in your tests you can now decrypt obfuscated passwords for use in login methods like this:
```python
from seleniumbase import encryption
...
password = encryption.decrypt('$^*ENCRYPT=RXlYMSJWTz8HSwM=?&#$')
```
(You'll notice that encrypted strings have a common start token and end token. This is to help tell them apart from non-encrypted strings. You can customize these tokens in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py). The current default setting is `$^*ENCRYPT=` for the start token and `?&#$` for the end token.)

See [decryption_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/decryption_test.py) for an example of decrypting encrypted passwords in tests.
