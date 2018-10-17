from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_basic(self):
        self.open('https://xkcd.com/1117/')
        self.assert_element('img[alt="My Sky"]')
        self.create_shepherd_tour()
        self.add_tour_step("Welcome to XKCD!")
        self.add_tour_step("This is the XKCD logo.", "#masthead img")
        self.add_tour_step("Here's the daily webcomic.", "#comic img")
        self.add_tour_step("This is the title.", "#ctitle", alignment="top")
        self.add_tour_step("Click here for the next comic.", 'a[rel="next"]')
        self.add_tour_step("Or here for the previous comic.", 'a[rel="prev"]')
        self.add_tour_step("Learn about the author here.", 'a[rel="author"]')
        self.add_tour_step("Click for the license here.", 'a[rel="license"]')
        self.add_tour_step("This selects a random comic.", 'a[href*="random"]')
        self.add_tour_step("Thanks for taking this tour!")
        # self.export_tour()  # Use this to export the tour as [my_tour.js]
        self.play_tour()
