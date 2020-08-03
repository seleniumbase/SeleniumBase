from seleniumbase import BaseCase


class MyTourClass(BaseCase):

    def test_google_tour(self):
        self.open('https://google.com/ncr')
        self.wait_for_element('input[title="Search"]')

        self.create_hopscotch_tour()  # OR self.create_tour(theme="hopscotch")
        self.add_tour_step("Welcome to Google!", title="SeleniumBase Tours")
        self.add_tour_step("Type in your query here.", 'input[title="Search"]')
        self.play_tour()

        self.highlight_update_text('input[title="Search"]', "Google")
        self.wait_for_element('[role="listbox"]')  # Wait for autocomplete

        self.create_hopscotch_tour()
        self.add_tour_step("Then click to search.", '[value="Google Search"]')
        self.add_tour_step("Or press [ENTER] after entry.", '[title="Search"]')
        self.play_tour()

        self.highlight_update_text('input[title="Search"]', "GitHub\n")
        self.wait_for_element("#search")

        self.create_hopscotch_tour()
        self.add_tour_step("See Results Here!", title="(5-second autoplay)")
        self.add_tour_step("Here's the next tour:")
        self.play_tour(interval=5)  # Tour automatically continues after 5 sec

        self.open("https://www.google.com/maps/@42.3598616,-71.0912631,15z")
        self.wait_for_element("#searchboxinput", timeout=20)
        self.wait_for_element("#minimap", timeout=20)
        self.wait_for_element("#zoom", timeout=20)

        self.create_hopscotch_tour()
        self.add_tour_step("Welcome to Google Maps!")
        self.add_tour_step("Type in a location here.",
                           "#searchboxinput", title="Search Box")
        self.add_tour_step("Then click here to show it on the map.",
                           "#searchbox-searchbutton", alignment="bottom")
        self.add_tour_step("Or click here to get driving directions.",
                           "#searchbox-directions", alignment="bottom")
        self.add_tour_step("Use this button to switch to Satellite view.",
                           "#minimap div.widget-minimap", alignment="right")
        self.add_tour_step("Click here to zoom in.",
                           "#widget-zoom-in", alignment="left")
        self.add_tour_step("Or click here to zoom out.",
                           "#widget-zoom-out", alignment="left")
        self.add_tour_step("Use the Menu button to see more options.",
                           ".searchbox-hamburger-container", alignment="right")
        self.add_tour_step("Or click here to see more Google apps.",
                           '[title="Google apps"]', alignment="left")
        self.add_tour_step("Thanks for using SeleniumBase Tours!",
                           title="End of Guided Tour")
        self.export_tour(filename="hopscotch_google_maps_tour.js")
        self.play_tour()
