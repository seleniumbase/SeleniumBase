"""
This test demonstrates the use of encryption/decryption.
(Technically, obfuscation/unobfuscation.)
"""

from seleniumbase import BaseCase
from seleniumbase import encryption


class MyTestClass(BaseCase):

    def test_decrypt_password(self):
        self.open("https://www.saucedemo.com/")
        self.type("#user-name", "standard_user")

        encrypted_password = "$^*ENCRYPT=S3BDTAdCWzMmKEY8Gjg=?&#$"
        print("\nEncrypted Password = %s" % encrypted_password)
        password = encryption.decrypt(encrypted_password)
        print("Decrypted Password = %s" % password)
        self.type("#password", password)

        self.click('input[type="submit"]')
        self.assert_text("Products", "div.product_label")
        self.assert_element("#inventory_container")
