""" Testing the @pytest.mark.xfail marker.
    https://docs.pytest.org/en/latest/skipping.html
    (The test is expected to fail, but don't fail the entire build for it.)
"""

import pytest
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    @pytest.mark.xfail
    def test_xfail(self):
        self.open("https://xkcd.com/376/")
        self.sleep(1)  # Time to read the comic
        self.fail("There is a known bug here!")
