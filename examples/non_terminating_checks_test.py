from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_non_terminating_checks(self):
        self.open('http://xkcd.com/993/')
        self.wait_for_element('#comic')
        self.check_assert_element('img[alt="Brand Identity"]')
        self.check_assert_element('img[alt="Rocket Ship"]')  # Will Fail
        self.check_assert_element('#comicmap')
        self.check_assert_text('Fake Item', '#middleContainer')  # Will Fail
        self.check_assert_text('Random', '#middleContainer')
        self.check_assert_element('a[name="Super Fake !!!"]')  # Will Fail
        self.process_checks()
