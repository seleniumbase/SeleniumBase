from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTourClass(BaseCase):
    def test_google_tour(self):
        self.open("https://google.com/ncr")
        self.wait_for_element('input[title="Search"]')
        self.hide_elements("iframe")

        self.create_bootstrap_tour()  # OR self.create_tour(theme="bootstrap")
        self.add_tour_step("Welcome to Google!", title="SeleniumBase Tours")
        self.add_tour_step("Type in your query here.", 'input[title="Search"]')
        self.play_tour()

        self.highlight_type('input[title="Search"]', "Google")
        self.wait_for_element('[role="listbox"]')  # Wait for autocomplete

        self.create_bootstrap_tour()
        self.add_tour_step("Then click to search.", '[value="Google Search"]')
        self.add_tour_step("Or press [ENTER] after entry.", '[title="Search"]')
        self.play_tour()

        self.highlight_type('input[title="Search"]', "GitHub\n")
        self.ad_block()
        self.wait_for_element("#search")

        self.create_bootstrap_tour()
        self.add_tour_step("3-second autoplay...")
        self.add_tour_step("Here's the next tour:")
        self.play_tour(interval=3)  # Tour automatically continues after 3 sec

        self.open("https://www.google.com/maps/@42.3591234,-71.0915634,15z")
        self.wait_for_element("#searchboxinput", timeout=20)
        self.wait_for_element("#minimap", timeout=20)
        self.wait_for_element("#zoom", timeout=20)

        self.create_bootstrap_tour()
        self.add_tour_step("Welcome to Google Maps", title="SeleniumBase Tour")
        self.add_tour_step(
            "The location goes here.", "#searchboxinput", title="Search Box"
        )
        self.add_tour_step(
            "Then click here to show it on the map.",
            "#searchbox-searchbutton",
            alignment="bottom",
        )
        self.add_tour_step(
            "Or click here to get driving directions.",
            'button[aria-label="Directions"]',
            alignment="bottom",
        )
        self.add_tour_step(
            "Use this button to switch to Satellite view.",
            'button[jsaction*="minimap.main;"]',
            alignment="right",
        )
        self.add_tour_step(
            "Click here to zoom in.", "#widget-zoom-in", alignment="left"
        )
        self.add_tour_step(
            "Or click here to zoom out.", "#widget-zoom-out", alignment="left"
        )
        self.add_tour_step(
            "Use the Menu button to see more options.",
            'button[jsaction*="settings.open;"]',
            alignment="right",
        )
        self.add_tour_step(
            "Or click here to see more Google apps.",
            '[title="Google apps"]',
            alignment="left",
        )
        self.add_tour_step(
            "Thanks for using SeleniumBase Tours!", title="End of Guided Tour"
        )
        self.export_tour(filename="bootstrap_google_maps_tour.js")
        self.play_tour()
