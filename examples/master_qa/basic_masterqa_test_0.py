from seleniumbase import MasterQA


class MasterQATests(MasterQA):
    def test_masterqa(self):
        self.open("https://xkcd.com/1700/")
        self.verify("Do you see a webcomic?")
        self.open("https://store.xkcd.com/collections/everything")
        self.highlight_click('[title="things for walls"]')
        self.verify("Do you see posters for sale?")
        self.highlight_update_text("input.search-input", "book\n")
        self.verify("Do you see books in the search results?")
