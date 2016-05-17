from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open('http://xkcd.com/353/')
        self.find_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        xkcd_license = self.get_text('center')
        assert('reuse any of my drawings' in xkcd_license)
        self.open('http://xkcd.com/1481/')
        image_object = self.find_element('#comic img')
        caption = image_object.get_attribute('title')
        assert('connections to the server' in caption)
        self.click_link_text('Blag')
        self.find_text('The blag', 'header h2')
        self.update_text('input#s', 'Robots!\n')
        self.find_text('Hooray robots!', '#content')
        self.open('http://xkcd.com/1319/')
        self.find_text('Automation', 'div#ctitle')
