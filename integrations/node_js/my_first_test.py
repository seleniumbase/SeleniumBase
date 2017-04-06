from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open('http://xkcd.com/353/')
        self.assert_element('img[alt="Python"]')
        self.click('a[rel="license"]')
        self.assert_text('copy and reuse', 'div center')
        self.open('http://xkcd.com/1481/')
        image_object = self.find_element('#comic img')
        caption = image_object.get_attribute('title')
        self.assertTrue('connections to the server' in caption)
        self.click_link_text('Blag')
        self.assert_text('xkcd', '#site-title')
        header_text = self.get_text('header h2')
        self.assertTrue('The blag of the webcomic' in header_text)
        self.update_text('input#s', 'Robots!\n')
        self.assert_text('Hooray robots!', '#content')
        self.open('http://xkcd.com/1319/')
        self.assert_text('Automation', 'div#ctitle')
