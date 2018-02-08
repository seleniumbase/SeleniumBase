"""
Obfuscates a string/password into a string that can be decrypted later on.

Usage:
python obfuscate.py
Then enter the password.
The result is an encrypted password.
"""

from seleniumbase.common import encryption
import getpass
import time


def main():
    try:
        while(1):
            print("\nEnter password to obfuscate: (CTRL-C to exit)")
            password = getpass.getpass()
            print("Verify password:")
            verify_password = getpass.getpass()
            if password != verify_password:
                print("*** ERROR: Passwords don't match! .. Please try again!")
                continue
            print("\nHere is the obfuscated password:")
            time.sleep(0.07)
            print(encryption.decrypt(password))
            time.sleep(0.21)
    except KeyboardInterrupt:
        print("\nExiting...\n")


if __name__ == "__main__":
    main()
