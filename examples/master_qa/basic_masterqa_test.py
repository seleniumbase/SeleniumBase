from seleniumbase import MasterQA


class MasterQATests(MasterQA):

    def test_masterqa(self):
        self.open("https://xkcd.com/1700/")
        self.verify("Do you see a webcomic?")
        self.highlight_click('link=Blag')
        self.verify('Do you see a blog archive?')
        self.highlight_update_text("input#s", "Dragons\n")
        self.verify('Do you see "dragons" in the search results?')
