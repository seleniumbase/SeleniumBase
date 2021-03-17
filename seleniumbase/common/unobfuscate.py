"""
Unobfuscates an encrypted string/password into a plaintext string/password.

Usage:
python unobfuscate.py
Then enter the encrypted string/password.
The result is a plaintext string/password.
Works the same as obfuscate.py, but doesn't mask the input.
"""

from seleniumbase.common import encryption
import sys
import time


def main():
    if sys.version_info[0] >= 3:
        input_method = input  # Using Python 3 (or higher)
    else:
        # Python 2 has the raw_input() method. Python 3 does not.
        input_method = raw_input  # noqa: ignore=F821
    try:
        while(1):
            code = input_method(
                '\nEnter obfuscated/encrypted string: (CTRL+C to exit):\n')
            print("\nHere is the unobfuscated string/password:")
            time.sleep(0.07)
            print(encryption.decrypt(code))
            time.sleep(0.21)
    except KeyboardInterrupt:
        print("\nExiting...\n")


if __name__ == "__main__":
    main()
