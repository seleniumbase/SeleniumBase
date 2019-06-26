from seleniumbase import BaseCase


class FileUploadButtonTests(BaseCase):

    """ The main purpose of this is to test the self.choose_file() method. """

    def test_file_upload_button(self):
        self.open("https://www.w3schools.com/jsref/tryit.asp"
                  "?filename=tryjsref_fileupload_get")
        self.wait_for_element('[id*="google_ads"]')
        self.remove_elements('[id*="google_ads"]')
        self.switch_to_frame('iframeResult')
        self.add_css_style(
            'input[type="file"]{zoom: 1.5;-moz-transform: scale(1.5);}')
        self.highlight('input[type="file"]')
        self.choose_file('input[type="file"]', "example_logs/screenshot.png")
        self.demo_mode = True  # Adds highlighting to the assert statement
        self.assert_element('input[type="file"]')
