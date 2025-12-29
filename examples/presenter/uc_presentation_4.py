# https://www.youtube.com/watch?v=Mr90iQmNsKM
from contextlib import suppress
from seleniumbase import BaseCase
from seleniumbase import SB
BaseCase.main(__name__, __file__)


class UCPresentationClass(BaseCase):
    def test_presentation_4(self):
        self.open("data:,")
        self.set_window_position(4, 40)
        self._output_file_saves = False
        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            '<img src="https://seleniumbase.io/other/uc4_title.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>This continues my Undetectable Automation series:</h4>"
            '<img src="https://seleniumbase.io/other/ua_1_details.jpg"'
            ' width="100%">'
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            self.open("https://www.bostoncodecamp.com/CC37/info")
            self.create_tour(theme="hopscotch")
            self.add_tour_step(
                "<h2>Good Afternoon and Welcome!</h2>", 'h1.wow'
            )
            self.add_tour_step(
                "<h4>PSA: Visit our sponsors later.</h4>",
                '[href*="/Sponsors"]',
            )
            self.add_tour_step(
                "<h4>Let's check out the schedule...</h4>",
                '[href*="/Schedule/SessionGrid"]'
            )
            self.play_tour()

        with suppress(Exception):
            self.open(
                "https://www.bostoncodecamp.com/CC37/Schedule/SessionGrid"
            )
            self.highlight("h2", loops=8)
            if self.is_element_visible('[data-sessionid="765448"]'):
                self.highlight('div[data-sessionid="765448"]', loops=10)
                self.create_tour(theme="driverjs")
                self.add_tour_step(
                    "<h2>Here we are</h2>", '[data-sessionid="765448"]'
                )
                self.play_tour()
                self.click('a[onclick*="765448"]')
                self.create_tour(theme="hopscotch")
                self.add_tour_step(
                    "<h2>What to expect</h2>",
                    "div.sz-modal-session",
                    alignment="left",
                )
                self.play_tour()

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h2>Last time...</h2>"
        )
        self.add_slide(
            "<h4>Last time...</h4>"
            '<img src="https://seleniumbase.io/other/uc3_title.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>This time...</h4>"
            '<img src="https://seleniumbase.io/other/anti_bots.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "Note: There are different kinds of reCAPTCHA,<br />"
            "and not all of them are created equal.<br />"
            '<img src="https://seleniumbase.io/other/recaptcha_v2a.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>This is what happens when you fail reCAPTCHA:</h4>"
            '<img src="https://seleniumbase.io/other/recaptcha_v2b.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>This is what happens when you fail hCAPTCHA:</h4>"
            '<img src="https://seleniumbase.io/other/hcaptcha_bunny.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h4>If you like puppies, hCAPTCHA has you covered:</h4>"
            '<img src="https://seleniumbase.io/other/hcaptcha_puppy.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h4>This is what happens when some anti-bots detect you:</h4>"
            '<img src="https://seleniumbase.io/other/you_are_blocked.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4>And this is what happens when Gandalf blocks you:</h4>"
            '<img src="https://seleniumbase.io/other/gandalf.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4>No joke... There's a Hobbit CAPTCHA</h4>"
            '<img src="https://seleniumbase.io/other/hobbit_captcha.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h3>Important Notice:</h3>"
            "(Know the laws and legal implications!)"
            '<img src="https://seleniumbase.io/other/legal_scraping.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<p>🔹 <b>By the end of this presentation...</b> 🔹</p><hr /><br />"
            "✅ You'll learn which anti-bot systems work,<br />"
            "and which ones don't. (Hint: Most don't work.)<br /><br />"
            "✅ There will be multiple live demos."
            "<br /><br />"
            "✅ You'll learn how to bypass weak defenses."
            "<br /><br />"
            "✅ You'll learn powerful web-scraping techniques."
            "</mk-1></p>"
        )
        self.add_slide(
            "<h4>But first, a little about me...</h4>"
            '<img src="https://seleniumbase.io/other/profile_t1.png"'
            ' width="48%">'
        )
        self.add_slide(
            "<p><b>About me: (Michael Mintz)</b></p>\n"
            "<ul>\n"
            "<li><mk-0>I created the <b>SeleniumBase</b> framework."
            "</mk-0></li>\n"
            "<li><mk-1>I lead the Automation Team at <b>iboss</b>."
            "</mk-1></li>\n"
            "</ul>",
            image="https://seleniumbase.io/other/iboss_booth.png",
        )
        self.add_slide(
            "<h2>In my spare time,</h2>"
            "<h2>I may be found...</h2>"
        )
        self.add_slide(
            "<h4>Spending time with entrepreneurs...</h4>"
            '<img src="https://seleniumbase.io/other/with_hs_founders.jpg"'
            ' width="85%">'
        )
        self.add_slide(
            "<h4>Spending time with celebrities...</h4>"
            '<img src="https://seleniumbase.io/other/with_frakes.jpg"'
            ' width="52%">'
        )
        self.add_slide(
            "<h4>Spending time with politicians...</h4>"
            '<img src="https://seleniumbase.io/other/with_tulsi.jpg"'
            ' width="50%">'
        )
        self.add_slide(
            "<h4>Spending time with philanthropists...</h4>"
            '<img src="https://seleniumbase.io/other/with_jeff.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<h4>Speaking at conferences...</h4>"
            '<img src="https://seleniumbase.io/other/mintz_present.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4>Attending conferences as a guest...</h4>"
            '<img src="https://seleniumbase.io/other/at_ms_build.jpg"'
            ' width="75%">'
        )
        self.add_slide(
            "<h4>Jet-skiing in Key West...</h4>"
            '<img src="https://seleniumbase.io/other/on_jetski.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>And working on SeleniumBase...</h4>"
            '<img src="https://seleniumbase.io/other/sb_star_history.jpg"'
            ' width="85%">'
        )
        self.add_slide(
            "<h4>Enough about me...</h4><br />"
            "<h3>Let's begin the presentation!</h3><br /><br />"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/blue_chrome.jpg"'
            ' width="50%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/cdp_logo.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/blue_chrome.jpg"'
            ' width="30%">'
            '<img src="https://seleniumbase.io/other/cdp_definition.jpg"'
            ' width="100%">'
            "<br />"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/se_pw_cdp.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "Playwright using CDP"
            '<img src="https://seleniumbase.io/other/pw_cdp.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "Selenium using CDP"
            '<img src="https://seleniumbase.io/other/se_cdp.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<p>Microsoft still supports Selenium,<br />"
            "even though they have Playwright.</p>"
            '<img src="https://seleniumbase.io/other/ms_edge_webdriver.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/twenty_se.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "As a birthday gift, BrightData invested a lot of money into "
            "Selenium (making them an official sponsor)."
            '<img src="https://seleniumbase.io/other/bd_invests_in_se.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "That's great news for the Selenium community!"
            '<img src="https://seleniumbase.io/other/se_community.jpg"'
            ' width="68%">'
        )
        self.add_slide(
            "Now, let's get back to CDP..."
            '<img src="https://seleniumbase.io/other/cdp_logo.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "There are lots of GitHub repos using CDP.<br />"
            "(This repo tracks some of them)"
            '<img src="https://seleniumbase.io/other/awesome_cdp.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "The first major Python implementation of CDP:"
            '<img src="https://seleniumbase.io/other/python_cdp.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/mark_haase.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "PyCDP was the key ingredient to stealthy automation."
            '<img src="https://seleniumbase.io/other/cdp_in_nodriver.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/nodriver.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/undetected_ch.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "In addition to using CDP for controlling Chrome in a"
            " stealthy way, you can also achieve stealth by using"
            " tools that can control the mouse and keyboard.<br /><br />"
            "<code>PyAutoGUI</code> is one such tool:"
            '<img src="https://seleniumbase.io/other/pyautogui_tree.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/al_sweigart.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "PyAutoGUI requires a headed browser to work.<br /><br />"
            " Since most Linux machines have headless displays that"
            " don't support headed browsers, an external tool called"
            " Xvfb must be used in order to simulate a headed browser"
            " in a headless Linux environment..."
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/xvfb_info.jpg"'
            ' width="56%">'
        )
        self.add_slide(
            "<p><mk-0>To have a completely stealthy framework"
            " for clicking CAPTCHAs & bypassing anti-bot systems,"
            " you need:</mk-0><br /><hr />"
            "</p><ul>\n"
            '<li><mk-1>A framework that uses a "regular" browser<br />'
            '(to hide evidence of automation activity)'
            '</mk-1>'
            "</li><br />\n"
            "<li><mk-2>CDP capabilities for performing stealthy actions"
            "</mk-2></li><br />\n"
            "<li><mk-3>PyAutoGUI for performing tricky actions<br />"
            "(eg. clicking Shadow-root CAPTCHAs)</mk-3>"
            "</li><br />\n"
            "<li><mk-4>Xvfb integration for headless Linux systems</mk-4>"
            "</li>\n</ul><br />\n"
        )
        self.add_slide(
            "SeleniumBase CDP Mode simplifies all that for you:<br /><br />"
            '<img src="https://seleniumbase.io/other/cdp_in_sb.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_on_github.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_on_discord.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/detect_antibots.jpg"'
            ' width="92%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sc_en_invite.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "List of sites with their invisible anti-bot services:"
            '<img src="https://seleniumbase.io/other/sites_to_antibots.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h3><mk-0>Let's get started with live demos of bypassing"
            " physical CAPTCHAs:</mk-0></h3>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up first...</h3><hr /><br /><br /><h4><mk-0><code>"
            "planetminecraft.com/account/sign_in/"
            "</code></mk-0></h4><br /><br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True) as sb:
            url = "www.planetminecraft.com/account/sign_in/"
            sb.activate_cdp_mode(url)
            sb.sleep(2)
            sb.solve_captcha()
            sb.wait_for_element_absent("input[disabled]")
            sb.sleep(2)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "cloudflare.com/login"
            "</code></mk-0></h4><br /><br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en") as sb:
            url = "https://www.cloudflare.com/login"
            sb.activate_cdp_mode(url)
            sb.sleep(3.5)
            sb.solve_captcha()
            sb.sleep(2.5)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "gitlab.com/users/sign_in"
            "</code></mk-0></h4><br /><br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en") as sb:
            url = "https://gitlab.com/users/sign_in"
            sb.activate_cdp_mode(url)
            sb.sleep(2)
            sb.solve_captcha()
            # (The rest is for testing and demo purposes)
            sb.assert_text("Username", '[for="user_login"]', timeout=3)
            sb.assert_element('label[for="user_login"]')
            sb.highlight('button:contains("Sign in")')
            sb.highlight('h1:contains("GitLab")')
            sb.post_message("SeleniumBase wasn't detected", duration=4)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p><mk-0><b>The code for the previous live demo:</b></mk-0></p>"
            "<hr /><br />",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>\n\n"
                "<mk-2>with SB(uc=True) as sb:</mk-2>\n"
                '<mk-3>    url = "https://gitlab.com/users/sign_in"</mk-3>\n'
                "<mk-4>    sb.activate_cdp_mode(url)</mk-4>\n"
                "<mk-5>    sb.sleep(2)</mk-5>\n"
                "<mk-6>    sb.solve_captcha()</mk-6>\n\n"
                "<mk-7>    ...</mk-7>\n\n\n\n\n"
            ),
        )
        self.add_slide(
            "<p><b>The code for the previous live demo:</b></p>"
            "<hr /><br />",
            code=(
                "from seleniumbase import SB\n\n"
                "with SB(uc=True) as sb:\n"
                '    url = "https://gitlab.com/users/sign_in"\n'
                "    sb.activate_cdp_mode(url)\n"
                "    sb.sleep(2)\n"
                "    sb.solve_captcha()\n\n"
                '<mk-1>    sb.assert_text("Username", \'[for="user_login"]\','
                ' timeout=3)</mk-1>\n'
                '<mk-2>    sb.assert_element(\'[for="user_login"]\')</mk-2>\n'
                '<mk-3>    sb.set_messenger_theme(location="bottom_center")'
                '</mk-3>\n'
                '<mk-4>    sb.post_message("SeleniumBase wasn\'t detected!")'
                '</mk-4>\n'
            ),
        )
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "bing.com/turing/captcha/challenge"
            "</code></mk-0></h4><br /><br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True) as sb:
            url = "https://www.bing.com/turing/captcha/challenge"
            sb.activate_cdp_mode(url)
            sb.sleep(1)
            sb.solve_captcha()
            sb.sleep(2)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide("<h2>Having fun yet?!?</h2>")
        self.add_slide(
            "<h4>If you're not yet concerned about online security,<br />"
            " then you probably need to see more live demos...</h4>")
        self.add_slide(
            "<h3><mk-0>Time for live demos of bypassing<br />"
            "some invisible anti-bot services:</mk-0></h3>"
        )
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "pokemon.com/us"
            "</code></mk-0></h4><br />"
            "(Protected by Imperva / Incapsula)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
            url = "https://www.pokemon.com/us"
            sb.activate_cdp_mode(url)
            sb.sleep(1.5)
            sb.click_if_visible("button#onetrust-accept-btn-handler")
            sb.sleep(1.2)
            sb.click("a span.icon_pokeball")
            sb.sleep(2.5)
            sb.click('b:contains("Show Advanced Search")')
            sb.sleep(2.5)
            sb.click('span[data-type="type"][data-value="electric"]')
            sb.sleep(0.7)
            sb.scroll_into_view("a#advSearch")
            sb.sleep(0.7)
            sb.click("a#advSearch")
            sb.sleep(0.5)
            sb.cdp.click("a#advSearch")
            sb.sleep(1.2)
            sb.cdp.click('img[src*="img/pokedex/detail/025.png"]')
            sb.cdp.assert_text("Pikachu", 'div[class*="title"]')
            sb.cdp.assert_element('img[alt="Pikachu"]')
            sb.cdp.scroll_into_view("div.pokemon-ability-info")
            sb.sleep(1.2)
            sb.cdp.flash('div[class*="title"]')
            sb.cdp.flash('img[alt="Pikachu"]')
            sb.cdp.flash("div.pokemon-ability-info")
            name = sb.cdp.get_text("label.styled-select")
            info = sb.cdp.get_text("div.version-descriptions p.active")
            print("*** %s: ***\n* %s" % (name, info))
            sb.sleep(2)
            sb.cdp.highlight_overlay("div.pokemon-ability-info")
            sb.sleep(2)
            sb.cdp.open("https://events.pokemon.com/EventLocator/")
            sb.sleep(2)
            sb.cdp.click('span:contains("Championship")')
            sb.sleep(2)
            events = sb.cdp.select_all("div.event-info__title")
            print("*** Pokémon Championship Events: ***")
            for event in events:
                print("* " + event.text)
            sb.sleep(2)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "walmart.com"
            "</code></mk-0></h4><br />"
            "(Protected by Akamai + PerimeterX)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, ad_block=True) as sb:
            url = "https://www.walmart.com/"
            sb.activate_cdp_mode(url)
            sb.sleep(1.8)
            continue_button = 'button:contains("Continue shopping")'
            if sb.is_element_visible(continue_button):
                sb.cdp.gui_click_element(continue_button)
                sb.sleep(0.6)
            sb.click('input[aria-label="Search"]')
            sb.sleep(1.2)
            search = "Settlers of Catan Board Game"
            required_text = "Catan"
            sb.press_keys('input[aria-label="Search"]', search + "\n")
            sb.sleep(3.8)
            if sb.is_element_visible("#px-captcha"):
                sb.cdp.gui_click_and_hold("#px-captcha", 7.2)
                sb.sleep(3.2)
                if sb.is_element_visible("#px-captcha"):
                    sb.cdp.gui_click_and_hold("#px-captcha", 4.2)
                    sb.sleep(3.2)
            sb.remove_elements('[data-testid="skyline-ad"]')
            sb.remove_elements('[data-testid="sba-container"]')
            print('*** Walmart Search for "%s":' % search)
            print('    (Results must contain "%s".)' % required_text)
            unique_item_text = []
            items = sb.cdp.find_elements('div[data-testid="list-view"]')
            for item in items:
                if required_text in item.text:
                    description = item.querySelector(
                        '[data-automation-id="product-title"]'
                    )
                    if (
                        description
                        and description.text not in unique_item_text
                    ):
                        unique_item_text.append(description.text)
                        print("* " + description.text)
                        price = item.querySelector(
                            '[data-automation-id="product-price"]'
                        )
                        if price:
                            price_text = price.text
                            price_text = (
                                price_text.split("current price Now ")[-1]
                            )
                            price_text = price_text.split("current price ")[-1]
                            price_text = price_text.split(" ")[0]
                            print("  (" + price_text + ")")

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "albertsons.com/recipes/"
            "</code></mk-0></h4><br />"
            "(Protected by Imperva / Incapsula)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en") as sb:
            url = "https://www.albertsons.com/recipes/"
            sb.activate_cdp_mode(url)
            sb.sleep(2.5)
            sb.remove_element("div > div > article")
            sb.scroll_into_view('input[type="search"]')
            close_btn = ".notification-alert-wrapper__close-button"
            sb.click_if_visible(close_btn)
            sb.click("input#search-suggestion-input")
            sb.sleep(0.2)
            search = "Avocado Smoked Salmon"
            required_text = "Salmon"
            sb.press_keys("input#search-suggestion-input", search)
            sb.sleep(0.8)
            sb.click("#suggestion-0 a span")
            sb.sleep(0.8)
            sb.click_if_visible(close_btn)
            sb.sleep(3.2)
            print('*** Albertsons Search for "%s":' % search)
            print('    (Results must contain "%s".)' % required_text)
            unique_item_text = []
            item_selector = 'a[href*="/meal-plans-recipes/shop/"]'
            items = sb.find_elements(item_selector)
            for item in items:
                sb.sleep(0.06)
                if required_text in item.text:
                    item.flash(color="44CC88")
                    sb.sleep(0.025)
                    if item.text not in unique_item_text:
                        unique_item_text.append(item.text)
                        print("* " + item.text)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "easyjet.com/en/"
            "</code></mk-0></h4><br />"
            "(Protected by Akamai)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
            url = "https://www.easyjet.com/en/"
            sb.activate_cdp_mode(url)
            sb.sleep(2)
            sb.click_if_visible("button#ensCloseBanner")
            sb.sleep(1.2)
            sb.click('input[name="from"]')
            sb.sleep(1.2)
            sb.type('input[name="from"]', "London Gatwick")
            sb.sleep(0.6)
            sb.click_if_visible("button#ensCloseBanner")
            sb.sleep(0.6)
            sb.click('span[data-testid="airport-name"]')
            sb.sleep(1.2)
            sb.type('input[name="to"]', "Paris")
            sb.sleep(1.2)
            sb.click('span[data-testid="airport-name"]')
            sb.sleep(1.2)
            sb.click('input[name="when"]')
            sb.sleep(1.2)
            sb.cdp.click(
                '[data-testid="month"]:last-of-type'
                ' [aria-disabled="false"]'
            )
            sb.sleep(1.2)
            sb.click(
                '[data-testid="month"]:last-of-type'
                ' [aria-disabled="false"]'
            )
            sb.sleep(1.2)
            sb.click('button[data-testid="submit"]')
            sb.sleep(3.5)
            sb.connect()
            sb.sleep(4.2)
            for window in sb.driver.window_handles:
                sb.switch_to_window(window)
                if "/buy/flights" in sb.get_current_url():
                    break
            sb.click_if_visible("button#ensCloseBanner")
            days = sb.find_elements('div[class*="FlightGridLayout_column"]')
            for day in days:
                if not day.text.strip():
                    continue
                print(
                    "\n\n**** " + " ".join(day.text.split("\n")[0:2]) + " ****"
                )
                fares = day.find_elements(
                    "css selector", 'button[class*="flightDet"]'
                )
                if not fares:
                    print("No flights today!")
                for fare in fares:
                    info = fare.text
                    info = info.replace("LOWEST FARE\n", "")
                    info = info.replace("\n", "  ")
                    print(info)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "hyatt.com"
            "</code></mk-0></h4><br />"
            "(Protected by Kasada)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
            url = "https://www.hyatt.com/"
            sb.activate_cdp_mode(url)
            sb.sleep(3.2)
            sb.click_if_visible('button[aria-label="Close"]')
            sb.sleep(0.1)
            sb.click_if_visible("#onetrust-reject-all-handler")
            sb.sleep(1.2)
            location = "Anaheim, CA, USA"
            sb.type('input[id="search-term"]', location)
            sb.sleep(1.2)
            sb.click('li[data-js="suggestion"]')
            sb.sleep(1.2)
            sb.click("button.be-button-shop")
            sb.sleep(6)
            card_info = (
                'div[data-booking-status="BOOKABLE"] [class*="HotelCard_info"]'
            )
            hotels = sb.select_all(card_info)
            destination_selector = 'span[class*="summary_destination"]'
            print("Hyatt Hotels in %s:" % location)
            print("(" + sb.get_text(destination_selector) + ")")
            if len(hotels) == 0:
                print("No availability over the selected dates!")
            for hotel in hotels:
                info = hotel.text.strip()
                if "Avg/Night" in info and not info.startswith("Rates from"):
                    name = info.split("  (")[0]
                    name = name.split(" + ")[0].split(" Award Cat")[0]
                    name = name.split(" Rates from :")[0]
                    price = "?"
                    if "Rates from : " in info:
                        price = info.split("Rates from : ")[1]
                        price = price.split(" Avg/Night")[0]
                    print("* %s => %s" % (name, price))

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "bestwestern.com/en_US.html"
            "</code></mk-0></h4><br />"
            "(Protected by DataDome)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en", guest=True) as sb:
            url = "https://www.bestwestern.com/en_US.html"
            sb.activate_cdp_mode(url)
            sb.sleep(3)
            sb.click_if_visible(".onetrust-close-btn-handler")
            sb.sleep(1)
            sb.click("input#destination-input")
            sb.sleep(2)
            location = "Palm Springs, CA, USA"
            sb.press_keys("input#destination-input", location)
            sb.sleep(1)
            sb.click("ul#google-suggestions li")
            sb.sleep(1)
            sb.click("button#btn-modify-stay-update")
            sb.sleep(4)
            sb.click("label#available-label")
            sb.sleep(2.5)
            print("Best Western Hotels in %s:" % location)
            summary_details = sb.get_text("#summary-details-column")
            dates = summary_details.split("DESTINATION")[-1]
            dates = dates.split(" CHECK-OUT")[0].strip() + " CHECK-OUT"
            dates = dates.replace("  ", " ")
            print("(Dates: %s)" % dates)
            flip_cards = sb.select_all(".flipCard")
            for i, flip_card in enumerate(flip_cards):
                hotel = flip_card.query_selector(".hotelName")
                price = flip_card.query_selector(".priceSection")
                if hotel and price:
                    print("* %s: %s => %s" % (
                        i + 1, hotel.text.strip(), price.text.strip())
                    )

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "priceline.com"
            "</code></mk-0></h4><br />"
            "(Protected by DataDome)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en") as sb:
            url = "https://www.priceline.com"
            sb.activate_cdp_mode(url)
            sb.sleep(1.8)
            sb.click('input[name="endLocation"]')
            sb.sleep(1.2)
            location = "Portland, Oregon, US"
            selection = "Oregon, United States"  # (Dropdown option)
            sb.press_keys('input[name="endLocation"]', location)
            sb.sleep(1.5)
            sb.click_if_visible('input[name="endLocation"]')
            sb.sleep(0.6)
            sb.click(selection)
            sb.sleep(1.5)
            sb.click('button[aria-label="Dismiss calendar"]')
            sb.sleep(0.5)
            sb.click('button[data-testid="HOTELS_SUBMIT_BUTTON"]')
            sb.sleep(0.5)
            if sb.is_element_visible('[aria-label="Close Modal"]'):
                sb.click('[aria-label="Close Modal"]')
                sb.sleep(0.5)
                sb.click('button[data-testid="HOTELS_SUBMIT_BUTTON"]')
            sb.sleep(4.8)
            if len(sb.cdp.get_tabs()) > 1:
                sb.cdp.close_active_tab()
                sb.cdp.switch_to_newest_tab()
                sb.sleep(0.6)
            sb.sleep(0.8)
            for y in range(1, 9):
                sb.scroll_to_y(y * 400)
                sb.sleep(0.5)
            hotel_names = sb.find_elements(
                'a[data-autobot-element-id*="HOTEL_NAME"]'
            )
            if sb.is_element_visible('[font-size="4,,,5"]'):
                hotel_prices = sb.find_elements('[font-size="4,,,5"]')
            else:
                hotel_prices = sb.find_elements(
                    '[font-size="12px"] + [font-size="20px"]'
                )
            print("Priceline Hotels in %s:" % location)
            print(sb.get_text('[data-testid="POPOVER-DATE-PICKER"]'))
            if len(hotel_names) == 0:
                print("No availability over the selected dates!")
            count = 0
            for i, hotel in enumerate(hotel_names):
                if hotel_prices[i] and hotel_prices[i].text:
                    count += 1
                    hotel_price = "$" + hotel_prices[i].text
                    print("* %s: %s => %s" % (count, hotel.text, hotel_price))

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            '<img src="https://seleniumbase.io/other/shatner_priceline.jpg"'
            ' width="60%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/mintz_karate.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/with_shatner.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/mintz_enterprise.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "nike.com"
            "</code></mk-0></h4><br />"
            "(Protected by Shape Security)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en", pls="none") as sb:
            url = "https://www.nike.com/"
            sb.activate_cdp_mode(url)
            sb.sleep(2.5)
            sb.click('[data-testid="user-tools-container"] search')
            sb.sleep(1.5)
            search = "Nike Air Force 1"
            sb.press_keys('input[type="search"]', search)
            sb.sleep(4)
            details = 'ul[data-testid*="products"] figure .details'
            elements = sb.select_all(details)
            if elements:
                print('**** Found results for "%s": ****' % search)
            for element in elements:
                print("* " + element.text)
            sb.sleep(2)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>Up next...</h3><hr /><br /><br /><h4><mk-0><code>"
            "nordstrom.com"
            "</code></mk-0></h4><br />"
            "(Protected by Shape Security)"
            "<br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with SB(uc=True, test=True, locale="en") as sb:
            url = "https://www.nordstrom.com/"
            sb.activate_cdp_mode(url)
            sb.sleep(2.2)
            sb.click("input#keyword-search-input")
            sb.sleep(0.8)
            search = "cocktail dresses for women teal"
            sb.press_keys("input#keyword-search-input", search + "\n")
            sb.sleep(2.2)
            for i in range(17):
                sb.scroll_down(16)
                sb.sleep(0.14)
            print('*** Nordstrom Search for "%s":' % search)
            unique_item_text = []
            items = sb.find_elements("article")
            for item in items:
                description = item.querySelector("article h3")
                if description and description.text not in unique_item_text:
                    unique_item_text.append(description.text)
                    price_text = ""
                    price = item.querySelector(
                        'div div span[aria-hidden="true"]'
                    )
                    if price:
                        price_text = price.text
                        print("* %s (%s)" % (description.text, price_text))

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3>CDP is powerful, as you can see.</h3>"
            "<h4>(Especially when used for stealth!)</h4>"
            '<img src="https://seleniumbase.io/other/blue_chrome.jpg"'
            ' width="40%">'
        )
        self.add_slide(
            "<h4>Out of the following 9 anti-bot defense systems...</h4>"
            '<img src="https://seleniumbase.io/other/anti_bots.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4>These are weak: (Can't detect stealthy CDP)</h4>"
            '<img src="https://seleniumbase.io/other/bypassable_anti_bots.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4>And these are strong: (CDP is detected)</h4>"
            '<img src="https://seleniumbase.io/other/capable_anti_bots.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h3><mk-0>What is Microsoft's stance<br />on stealthy CDP?</mk-0>"
            "</h3><br /><br /><h3><mk-1>Officially...</mk-1></h3>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/pw_no_stealth.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h3>What is Microsoft's stance<br />on stealthy CDP?</h3>"
            "<br /><br /><h3><mk-0>Unofficially...</mk-0></h3>"
        )
        self.add_slide(
            "<h3>There are external repos<br />using Playwright for stealth."
            "</h3><br /><br /><h4>"
            "And Microsoft employees are<br />endorsing them via GitHub Stars."
            "</h4>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/scrapling_pw.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/ms_stars_scrapling.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "And steathy CDP works well in GitHub Actions."
            '<img src="https://seleniumbase.io/other/gh_actions_scrape.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "Why does stealthy CDP work in GitHub Actions,<br />"
            "but not in other kinds of services like AWS?"
        )
        self.add_slide(
            "<h3>Answer:<br /><br />"
            'GitHub Actions runs in a<br />'
            '"residential IP address" space!'
            "<br /><br /></h3>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/rp_def.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h3>People can use residential proxies<br />"
            "to get a residential IP address.</h3>"
        )
        self.add_slide(
            "<h3>Legal info:</h3>"
            '<img src="https://seleniumbase.io/other/legal_rp_scraping.jpg"'
            ' width="100%">'
        )
        self.add_slide("<h2>To summarize that...</h2>")
        self.add_slide(
            "<h4>Scraping public data is probably legal.<br />"
            "(Think Light Side)</h4>"
            '<img src="https://seleniumbase.io/other/sw_light_side.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h4>Scraping private data is probably NOT legal.<br />"
            "(Think Dark Side)</h4>"
            '<img src="https://seleniumbase.io/other/sw_dark_side.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h4>If you break local and/or international laws,<br />"
            "then bounty hunters may come after you.</h4>"
            '<img src="https://seleniumbase.io/other/sw_bounty_hunters.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h3>Let's get back to SeleniumBase</h3>"
            '<img src="https://seleniumbase.io/other/sb_laptop.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>SeleniumBase includes a special Chrome extension:</h4>"
            '<h2>The "Recorder"</h2>'
            "<h4>(You can generate complete scripts with it.)</h4>"
            "<h3><code>sbase recorder --uc</code></h3>"
            '<img src="https://seleniumbase.io/cdn/img/'
            'sb_recorder_notification.png" width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/cdn/img/recorder_desktop.png"'
            ' width="56%">'
        )
        self.begin_presentation(filename="uc_presentation.html")

        # import sys
        # from seleniumbase.console_scripts import sb_recorder
        # sys.argv.append("--uc")
        # sb_recorder.main()

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h4>How does one make an automation Recorder?</h4>"
            '<img src="https://seleniumbase.io/cdn/img/'
            'sb_recorder_notification.png" width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/analytics_auto_ext.jpg"'
            ' width="75%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/event_listeners_1.jpg"'
            ' width="92%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/event_listeners_2.jpg"'
            ' width="92%">'
        )
        self.add_slide(
            "And that's the secret to building a test recorder!"
            '<img src="https://seleniumbase.io/cdn/img/'
            'sb_recorder_notification.png" width="100%">'
        )
        self.add_slide(
            "Also note that there are more stealth CDP repos<br />"
            "other than the ones that you have already seen."
            '<img src="https://seleniumbase.io/other/other_stealth_repos.jpg"'
            ' width="92%">'
        )
        self.add_slide(
            "<p>👤 <mk-0>Field trip to the CDP Mode help docs</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>Let's take a look at the CDP Mode docs<br />"
            "from the SeleniumBase GitHub repo...</mk-1></p>"
            '<a href="https://github.com/seleniumbase/SeleniumBase/blob/'
            'master/examples/cdp_mode/ReadMe.md" target="_blank">'
            '<img src="https://seleniumbase.io/other/cdp_in_sb.jpg"'
            ' width="60%"></a>'
        )
        self.add_slide(
            "<h3>❓ <mk-0>Questions?</mk-0> ❓</h3><h5><mk-0>"
            "https://github.com/seleniumbase/SeleniumBase/discussions"
            "</mk-0></h5><br />"
            "<br /><h3>📌 <mk-1>Found a bug?</mk-1> 🐞</h3><h5><mk-1>"
            "https://github.com/seleniumbase/SeleniumBase/issues"
            "</mk-0></h5>"
        )
        self.add_slide(
            "<h3>📊 <mk-0>Final remarks</mk-0> 📣</h3><hr /><br />"
            "<h3>🛠️ <mk-1>SeleniumBase gives you</mk-1> 🛠️<br />"
            "<mk-1>the tools you need to succeed!"
            "</mk-1></h3><h3><mk-2><br />"
            "And tools to build lots of bots..."
            "</mk-2></h3><br />"
        )
        self.add_slide(
            "<div>🏁 <b>The End</b> 🏁</div>"
            '<img src="https://seleniumbase.io/other/sb_github.jpg"'
            ' width="100%">'
        )
        self.begin_presentation(filename="uc_presentation.html")
