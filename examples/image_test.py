from seleniumbase import BaseCase


class ImageTest(BaseCase):

    def test_pull_image_from_website(self):
        """ Pull an image from a website and save it as a PNG file. """
        self.open("https://xkcd.com/1117/")
        selector = "#comic"
        file_name = "comic.png"
        folder = "images_exported"
        self.save_element_as_image_file(selector, file_name, folder)
        print('"%s/%s" has been saved!' % (folder, file_name))

    def test_add_text_overlay_to_image(self):
        """ Add a text overlay to an image. """
        self.open("https://xkcd.com/1117/")
        selector = "#comic"
        file_name = "image_overlay.png"
        folder = "images_exported"
        overlay_text = 'This is an XKCD comic!\nTitle: "My Sky"'
        self.save_element_as_image_file(
            selector, file_name, folder, overlay_text)
        print('"%s/%s" has been saved!' % (folder, file_name))

    def test_add_text_overlay_to_page_section(self):
        """ Add a text overlay to a section of a page. """
        self.open("https://xkcd.com/2200/")
        selector = "#middleContainer"
        file_name = "section_overlay.png"
        folder = "images_exported"
        overlay_text = (
            'Welcome to %s\n'
            'This is a comment added to the image.\n'
            'Unreachable states come from logic errors.'
            % self.get_current_url())
        self.save_element_as_image_file(
            selector, file_name, folder, overlay_text)
        print('"%s/%s" has been saved!' % (folder, file_name))

    def test_add_text_overlay_to_full_page(self):
        """ Add a text overlay to a full page. """
        self.open("https://xkcd.com/1922/")
        self.remove_element("#bottom")
        selector = "body"
        file_name = "page_overlay.png"
        folder = "images_exported"
        overlay_text = ("A text overlay on %s" % self.get_current_url())
        self.save_element_as_image_file(
            selector, file_name, folder, overlay_text)
        print('"%s/%s" has been saved!' % (folder, file_name))
