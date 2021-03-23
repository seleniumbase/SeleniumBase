from seleniumbase import BaseCase


class MyTourClass(BaseCase):

    def test_octocat_tour(self):
        self.maximize_window()
        self.open("https://seleniumbase.io/error_page/")
        self.wait_for_element("#parallax_octocat")
        self.create_tour(theme="bootstrap")
        self.add_tour_step("Welcome to the Octocat Tour!")
        self.add_tour_step("This is Octocat", "#parallax_octocat")
        self.add_tour_step("This is Octobi-Wan Catnobi", "#octobi_wan_catnobi")
        self.add_tour_step("<h1><b>Ooops!!!</b></h1>", "#parallax_error_text")
        self.add_tour_step("This is a Star Wars speeder.", "#speeder")
        self.add_tour_step("This is a sign with a 500-Error", "#parallax_sign")
        self.add_tour_step(
            "This is not the page you're looking for.", 'img[alt*="404"]')
        self.add_tour_step("<b>Have a great day!</b>", title="☀️ ☀️ ☀️ ☀️")
        self.add_tour_step("<b>And may the Force be with you!</b>", title="⭐")
        self.export_tour(filename="octocat_tour.js")
        self.play_tour()
