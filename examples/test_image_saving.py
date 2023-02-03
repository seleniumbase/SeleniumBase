""" Image-saving with "save_element_as_image_file()".

    Also shown are ways of ordering tests. (Currently commented out)
    For ordering tests, add the marker "@pytest.mark.run(order=NUM)"
        before a test definition or class definition.
    This changes the global test order when running "pytest".
    Eg: If you want a test to always run first before any test
        from all discovered files, add "@pytest.mark.run(order=0)".
    For local class/module test-ordering, name your tests
        using alphabetical order to set the order desired.
    Eg: "def test_AAAAA" will run before "def test_ZZZZZ".
    You can also add in numbers to force a specific order.
    Eg: "def test_1_ZZZ" will run before "def test_2_AAA".
"""
import os
# import pytest  # For ordering tests globally with @pytest.mark.run()
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ImageTests(BaseCase):
    # @pytest.mark.run(order=1)
    def test_1_save_element_as_image_file(self):
        """Pull an image from a website and save it as a PNG file."""
        self.open("https://xkcd.com/1117/")
        selector = "#comic"
        file_name = "comic.png"
        folder = "images_exported"
        self.save_element_as_image_file(selector, file_name, folder)
        file_path = os.path.join(folder, file_name)
        self.assert_true(os.path.exists(file_path))
        print('\n"%s" was saved!' % file_path)

    # @pytest.mark.run(order=2)
    def test_2_add_text_overlay_to_image(self):
        """Add a text overlay to an image."""
        self.open("https://xkcd.com/1117/")
        selector = "#comic"
        file_name = "image_overlay.png"
        folder = "images_exported"
        overlay_text = 'This is an XKCD comic!\nTitle: "My Sky"'
        self.save_element_as_image_file(
            selector, file_name, folder, overlay_text
        )
        file_path = os.path.join(folder, file_name)
        self.assert_true(os.path.exists(file_path))
        print('\n"%s" was saved!' % file_path)

    # @pytest.mark.run(order=3)
    def test_3_add_text_overlay_to_page_section(self):
        """Add a text overlay to a section of a page."""
        self.open("https://xkcd.com/2200/")
        selector = "#middleContainer"
        file_name = "section_overlay.png"
        folder = "images_exported"
        overlay_text = (
            "Welcome to %s\n"
            "This is a comment added to the image.\n"
            "Unreachable states come from logic errors."
            % self.get_current_url()
        )
        self.save_element_as_image_file(
            selector, file_name, folder, overlay_text
        )
        file_path = os.path.join(folder, file_name)
        self.assert_true(os.path.exists(file_path))
        print('\n"%s" was saved!' % file_path)

    # @pytest.mark.run(order=4)
    def test_4_add_text_overlay_to_full_page(self):
        """Add a text overlay to a full page."""
        self.open("https://xkcd.com/1922/")
        self.remove_element("#bottom")
        selector = "body"
        file_name = "page_overlay.png"
        folder = "images_exported"
        overlay_text = "A text overlay on %s" % self.get_current_url()
        self.save_element_as_image_file(
            selector, file_name, folder, overlay_text
        )
        file_path = os.path.join(folder, file_name)
        self.assert_true(os.path.exists(file_path))
        print('\n"%s" was saved!' % file_path)
