""" These tests demonstrate pytest marker use for finding and running tests.

    Usage examples from this file:
        pytest -v -m marker_test_suite                 # Runs A, B, C, D
        pytest -v -m marker1                           # Runs A
        pytest -v -m marker2                           # Runs B, C
        pytest -v -m marker3                           # Runs C
        pytest test_markers.py -v -m "not marker2"     # Runs A, D

    (The "-v" will display the names of tests as they run.)
    (Add "--collect-only" to display names of tests without running them.)
"""

import pytest
from seleniumbase import BaseCase


@pytest.mark.marker_test_suite
class MarkerTestSuite(BaseCase):

    @pytest.mark.marker1
    def test_A(self):
        self.open("https://xkcd.com/1319/")
        self.assert_text("Automation", "div#ctitle")

    @pytest.mark.marker2
    def test_B(self):
        self.open("https://www.xkcd.com/1700/")
        self.assert_text("New Bug", "div#ctitle")

    @pytest.mark.marker2
    @pytest.mark.marker3  # Tests can have multiple markers
    def test_C(self):
        self.open("https://xkcd.com/844/")
        self.assert_text("Good Code", "div#ctitle")

    def test_D(self):
        self.open("https://xkcd.com/2021/")
        self.assert_text("Software Development", "div#ctitle")
