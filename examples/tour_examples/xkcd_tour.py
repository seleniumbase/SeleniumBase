from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_create_tour(self):
        self.open('https://xkcd.com/1117/')
        self.assert_element('img[alt="My Sky"]')
        self.create_tour(theme="dark")
        self.add_tour_step("Welcome to XKCD!")
        self.add_tour_step("This is the XKCD logo.", "#masthead img")
        self.add_tour_step("Here's the daily webcomic.", "#comic img")
        self.add_tour_step("This is the title.", "#ctitle", alignment="top")
        self.add_tour_step("Click here for the next comic.", 'a[rel="next"]')
        self.add_tour_step("Click here for the previous one.", 'a[rel="prev"]')
        self.add_tour_step("Learn about the author here.", 'a[rel="author"]')
        self.add_tour_step("Click here for the license.", 'a[rel="license"]')
        self.add_tour_step("Click for a random comic.", 'a[href*="/random/"]')
        self.add_tour_step("Thanks for taking this tour!")
        self.export_tour(filename="xkcd_tour.js")  # Exports the tour
        self.play_tour()  # Plays the tour
