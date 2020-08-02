from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_create_tour(self):
        self.open("https://www.google.com/maps/@42.3598616,-71.0912631,15z")
        self.wait_for_element("#searchboxinput", timeout=20)
        self.wait_for_element("#minimap", timeout=20)
        self.wait_for_element("#zoom", timeout=20)

        # Create a website tour using the DriverJS library
        # Same as:  self.create_driverjs_tour()
        self.create_tour(theme="driverjs")
        self.add_tour_step("🗺️ Welcome to Google Maps 🗺️", "html",
                           title="✅ SeleniumBase Tours 🌎")
        self.add_tour_step("You can type a location into this Search box.",
                           "#searchboxinput")
        self.add_tour_step("Then click here to view it on the map.",
                           "#searchbox-searchbutton", alignment="bottom")
        self.add_tour_step("Or click here to get driving directions.",
                           "#searchbox-directions", alignment="bottom")
        self.add_tour_step("Use this button to get a Satellite view.",
                           "#minimap div.widget-minimap", alignment="right")
        self.add_tour_step("Click here to zoom in.",
                           "#widget-zoom-in", alignment="left")
        self.add_tour_step("Or click here to zoom out.",
                           "#widget-zoom-out", alignment="left")
        self.add_tour_step("Use the Menu button for more options.",
                           ".searchbox-hamburger-container", alignment="right")
        self.add_tour_step("Or click here to see more Google apps.",
                           '[title="Google apps"]', alignment="left")
        self.add_tour_step("Thanks for using SeleniumBase Tours", "html",
                           title="🚃 End of Guided Tour 🚃")
        self.export_tour()  # The default name for exports is "my_tour.js"
        self.play_tour(interval=0)  # If interval > 0, autoplay after N seconds
