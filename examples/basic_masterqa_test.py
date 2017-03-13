from seleniumbase import MasterQA


class MasterQATests(MasterQA):

    def test_masterqa(self):
        self.open("http://xkcd.com/1700/")
        self.verify("Do you see a webcomic?")
        self.click_link_text('Store')
        self.click_link_text('all the things')
        self.verify("Do you see items for sale?")
        self.update_text("input.search-input", "Robots\n")
        self.verify("Do you see robots in the search results?")
