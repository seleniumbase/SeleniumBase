from seleniumbase import BaseCase


class DialogBoxTests(BaseCase):
    def test_dialog_boxes(self):
        self.open("https://xkcd.com/1920/")
        self.assert_element('img[alt="Emoji Sports"]')
        self.highlight("#comic img")

        skip_button = ["SKIP", "red"]  # Can be a [text, color] list or tuple.
        buttons = ["Fencing", "Football", "Metaball", "Go/Chess", skip_button]
        message = "Choose a sport:"
        choice = None
        while choice != "STOP":
            choice = self.get_jqc_button_input(message, buttons)
            if choice == "Fencing":
                self.open("https://xkcd.com/1424/")
                buttons.remove("Fencing")
            elif choice == "Football":
                self.open("https://xkcd.com/1107/")
                buttons.remove("Football")
            elif choice == "Metaball":
                self.open("https://xkcd.com/1507/")
                buttons.remove("Metaball")
            elif choice == "Go/Chess":
                self.open("https://xkcd.com/1287/")
                buttons.remove("Go/Chess")
            else:
                break
            self.highlight("#comic img")
            if len(buttons) == 2:
                message = "One Sport Remaining:"
            if len(buttons) == 1:
                message = "Part One Complete. You saw all 4 sports!"
                btn_text_1 = "NEXT Tutorial Please!"
                btn_text_2 = "WAIT, Go/Chess is a sport?"
                buttons = [(btn_text_1, "green"), (btn_text_2, "purple")]
                choice_2 = self.get_jqc_button_input(message, buttons)
                if choice_2 == btn_text_2:
                    self.open_if_not_url("https://xkcd.com/1287/")
                    message = "Brain sports count as sports!<br /><br />"
                    message += "Are you ready for more?"
                    self.get_jqc_button_input(message, ["Let's Go!"])
                break

        self.open("https://xkcd.com/1117/")
        sb_banner_logo = "//seleniumbase.io/cdn/img/sb_logo_cs.png"
        self.set_attributes("#news img", "src", sb_banner_logo)
        options = [("theme", "material"), ("width", "52%")]
        message = 'With one button, you can press "Enter/Return", "Y", or "1".'
        self.get_jqc_button_input(message, ["OK"], options)

        self.open("https://xkcd.com/556/")
        self.set_attributes("#news img", "src", sb_banner_logo)
        options = [("theme", "bootstrap"), ("width", "52%")]
        message = 'If the lowercase button text is "yes" or "no", '
        message += '<br><br>you can use the "Y" or "N" keys as shortcuts. '
        message += '<br><br><br>Other shortcuts include: <br><br>'
        message += '"1": 1st button, "2": 2nd button, etc. Got it?'
        buttons = [("YES", "green"), ("NO", "red")]
        choice = self.get_jqc_button_input(message, buttons, options)

        message = 'You said "%s"! <br><br>' % choice
        if choice == "YES":
            message += "Wonderful! Let's continue with the next example..."
        else:
            message += "You can learn more from SeleniumBase Docs..."
        choice = self.get_jqc_button_input(message, ["OK"], options)

        self.open("https://seleniumbase.io")
        self.set_jqc_theme("light", color="green", width="38%")
        message = "<b>This is the SeleniumBase Docs website!</b><br /><br />"
        message += "What would you like to search for?<br />"
        text = self.get_jqc_text_input(message, ["Search"])
        self.update_text('input[aria-label="Search"]', text + "\n")
        self.wait_for_ready_state_complete()
        self.set_jqc_theme("bootstrap", color="red", width="32%")
        if self.is_text_visible("No matching documents", ".md-search-result"):
            self.get_jqc_button_input("Your search had no results!", ["OK"])
        elif self.is_text_visible("Type to start searching", "div.md-search"):
            self.get_jqc_button_input("You did not do a search!", ["OK"])
        else:
            self.click_if_visible("a.md-search-result__link")
            self.set_jqc_theme("bootstrap", color="green", width="32%")
            self.get_jqc_button_input("You found search results!", ["OK"])

        self.open("https://seleniumbase.io/help_docs/ReadMe/")
        self.highlight("h1")
        self.highlight_click('a:contains("Running Example Tests")')
        self.highlight("h1")

        self.set_jqc_theme("bootstrap", color="green", width="52%")
        message = 'See the "SeleniumBase/examples" section for more info!'
        self.get_jqc_button_input(message, ["OK"])

        self.set_jqc_theme("bootstrap", color="purple", width="56%")
        message = "Now let's combine form inputs with multiple button options!"
        message += "<br /><br />"
        message += "Pick something to search. Then pick the site to search on."
        buttons = ["XKCD.com Store", "Wikipedia.org"]
        text, choice = self.get_jqc_form_inputs(message, buttons)
        if choice == "XKCD.com Store":
            self.open("https://store.xkcd.com/search")
        else:
            self.open("https://en.wikipedia.org/wiki/Special:Search")
        self.highlight_update_text('input[id*="search"]', text + "\n")
        self.wait_for_ready_state_complete()
        self.sleep(1)
        self.highlight("body")
        self.reset_jqc_theme()
        self.get_jqc_button_input("<b>Here are your results.</b>", ["OK"])
        message = "<h3>You've reached the end of this tutorial!</h3><br />"
        message += "Now you know about SeleniumBase Dialog Boxes!<br />"
        message += "<br />Check out SeleniumBase on GitHub for more!"
        self.set_jqc_theme("modern", color="purple", width="56%")
        self.get_jqc_button_input(message, ["Goodbye!"])
