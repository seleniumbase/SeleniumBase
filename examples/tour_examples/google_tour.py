from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class MyTourClass(BaseCase):
    def test_google_tour(self):
        self.open("https://google.com/ncr")
        self.wait_for_element('[title="Search"]')
        self.hide_elements("iframe")

        # Create a website tour using the ShepherdJS library with "dark" theme
        # Same as:  self.create_shepherd_tour(theme="dark")
        self.create_tour(theme="dark")
        self.add_tour_step("Welcome to Google!", title="SeleniumBase Tours")
        self.add_tour_step("Type in your query here.", '[title="Search"]')
        self.play_tour()

        self.highlight_type('[title="Search"]', "Google")
        self.wait_for_element('[role="listbox"]')  # Wait for autocomplete

        # Create a website tour using the ShepherdJS library with "light" theme
        # Same as:  self.create_shepherd_tour(theme="light")
        self.create_tour(theme="light")
        self.add_tour_step("Then click to search.", '[value="Google Search"]')
        self.add_tour_step("Or press [ENTER] after entry.", '[title="Search"]')
        self.play_tour()

        self.highlight_type('[title="Search"]', "GitHub\n")
        self.ad_block()
        self.wait_for_element("#search")

        # Create a website tour using the Bootstrap Tour JS library
        # Same as:  self.create_bootstrap_tour()
        self.create_tour(theme="bootstrap")
        self.add_tour_step("3-second autoplay...")
        self.add_tour_step("Here's the next tour:")
        self.play_tour(interval=3)  # Tour automatically continues after 3 sec

        self.open("https://www.google.com/maps/@42.3591234,-71.0915634,15z")
        self.wait_for_element("#searchboxinput")
        self.wait_for_element("#minimap")
        self.wait_for_element("#zoom")

        # Create a website tour using the IntroJS library
        # Same as:  self.create_introjs_tour()
        self.create_tour(theme="introjs")
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
        if self.is_element_visible('button[jsaction*="settings.open;"]'):
            self.add_tour_step(
                "Use the Menu button to see more options.",
                'button[jsaction*="settings.open;"]',
                alignment="right",
            )
        elif self.is_element_visible('button[jsaction="navigationrail.more"]'):
            self.add_tour_step(
                "Use the Menu button to see more options.",
                'button[jsaction="navigationrail.more"]',
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
        self.export_tour()  # The default name for exports is "my_tour.js"
        self.play_tour()
