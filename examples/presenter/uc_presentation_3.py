import sys
from contextlib import suppress
from seleniumbase import BaseCase
from seleniumbase import SB
BaseCase.main(__name__, __file__)


class UCPresentationClass(BaseCase):
    def test_presentation_3(self):
        self.open("data:,")
        self.set_window_position(4, 40)
        self._output_file_saves = False
        self.open("https://seleniumbase.io/other/uc3_title.jpg")
        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            '<img src="https://seleniumbase.io/other/uc3_title.jpg"'
            ' width="100%">'
        )
        self.begin_presentation(filename="uc_presentation.html")

        self.open("https://seleniumbase.io/other/uc3_title.jpg")
        self.sleep(2.5)

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            '<img src="https://seleniumbase.io/other/uc3_title.jpg"'
            ' width="100%">'
            '<br /><h4><b>(with SeleniumBase UC Mode)</b></h4>'
        )
        self.add_slide(
            "<h4>This is the follow-up to my previous video:</h4>"
            '<img src="https://seleniumbase.io/other/uc2_title.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/uc_vid1_ss9.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>Which was the follow-up to an earlier video:</h4>"
            '<img src="https://seleniumbase.io/other/uc_automation.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/uc_vid1_ss8.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h5>There, you learned the basics of bypassing CAPTCHAs:</h5>"
            '<img src="https://seleniumbase.io/other/check_if_secure.png"'
            ' width="85%">'
        )
        self.add_slide(
            "<h2><mk-0>Here's a LIVE DEMO of bypassing a CAPTCHA:</mk-0></h2>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True) as sb:
                url = "https://gitlab.com/users/sign_in"
                sb.uc_open_with_reconnect(url, 4)
                sb.assert_text("Username", '[for="user_login"]', timeout=3)
                sb.assert_element('[for="user_login"]')
                sb.highlight('button:contains("Sign in")')
                sb.highlight('h1:contains("GitLab.com")')
                sb.post_message("SeleniumBase wasn't detected", duration=4)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p><mk-0><b>The code for the previous live demo:</b></mk-0></p>"
            "<hr /><br />",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>\n\n"
                "<mk-2>with SB(uc=True) as sb:</mk-2>\n"
                '<mk-3>    url = "https://gitlab.com/users/sign_in"</mk-3>\n'
                "<mk-4>    sb.uc_open_with_reconnect(url, 4)</mk-4>\n\n"
                "<mk-5>    ...</mk-5>\n"
            ),
        )
        self.add_slide(
            "<p><b>The code for the previous live demo:</b></p>"
            "<hr /><br />",
            code=(
                "from seleniumbase import SB\n\n"
                "with SB(uc=True) as sb:\n"
                '    url = "https://gitlab.com/users/sign_in"\n'
                "    sb.uc_open_with_reconnect(url, 4)\n\n"
                '<mk-1>    sb.assert_text("Username", \'[for="user_login"]\','
                ' timeout=3)</mk-1>\n'
                '<mk-2>    sb.assert_element(\'[for="user_login"]\')</mk-2>\n'
                '<mk-3>    sb.highlight(\'button:contains("Sign in")\')'
                '</mk-3>\n'
                '<mk-4>    sb.highlight(\'h1:contains("GitLab.com")\')'
                '</mk-4>\n'
                '<mk-5>    sb.post_message("SeleniumBase wasn\'t detected",'
                ' duration=4)</mk-5>\n'
            ),
        )
        self.add_slide(
            "<h3><mk-0>Even if using UC Mode, you may still need to"
            " click the CAPTCHA checkbox in order to bypass it.</mk-0></h3>"
            "<br />"
            "<h4><mk-1>(That's not a problem because there are special<br />"
            "UC Mode methods for handling that situation.)</mk-1>"
        )
        self.add_slide(
            "<p><mk-0>Special <b>UC Mode</b> methods for clicking CAPTCHAs:"
            "</mk-0></p><hr /><div></div>"
            "<ul><br />\n"
            "<li><mk-1><code><b>sb.uc_gui_handle_captcha()</b></code></mk-1>"
            "</li>\n"
            "PyAutoGUI uses the TAB key with SPACEBAR.<br /><br />\n\n"
            "<li><mk-2><code><b>sb.uc_gui_click_captcha()</b></code></mk-2>"
            "</li>\n\n"
            "PyAutoGUI clicks CAPTCHA with the mouse.<br />\n"
            "(Note that you'll need to use this one on Linux!)\n"
            "</ul>\n\n\n\n"
            "<p></p><br />"
        )
        self.add_slide(
            "<p><b><mk-0>When is clicking the CAPTCHA checkbox required?"
            "</mk-0></b></p><hr /><h5>&nbsp</h5>"
            "<h4><li><mk-1>They've seen your IP Address too many times."
            "</mk-1></li><br />"
            "<li><mk-2>They don't accept your User-Agent string.</mk-2>"
            "<br />(UC Mode gives you a good one by default)</li>"
            "<br />"
            "<li><mk-3>You're using Linux. (Likely a server)</mk-3></li>"
            "<br />"
            "<li><mk-4>You're using a VPN. (If detected)</mk-4></li>"
            "<br />"
        )
        self.add_slide(
            "<h3><mk-0>For testing purposes...</mk-0></h3><br />"
            "<mk-1>I'll use a bad User-Agent for some Live Demos...</mk-1>"
            "<br /><br />"
            "<mk-2>This will force me to click the CAPTCHA to bypass it."
            "</mk-2>"
        )
        self.add_slide(
            "<h3><mk-0>On the topic of live demos,</mk-0></h3>"
            "<h3><mk-0>I'll run some of them now:</mk-0></h3>"
            "<br /><br />"
            "<h4><mk-1>Get ready for a live demo of:</mk-1></h4>"
            "<h4><mk-1>Bypassing Cloudflare with TAB + SPACEBAR...</mk-1></h4>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0"
        if "linux" in sys.platform or "win32" in sys.platform:
            agent = None  # Use the default UserAgent

        with suppress(Exception):
            with SB(uc=True, test=True, agent=agent) as sb:
                url = "https://gitlab.com/users/sign_in"
                sb.uc_open_with_reconnect(url, 4)
                sb.uc_gui_handle_captcha()  # Only if needed
                sb.assert_element('label[for="user_login"]')
                sb.set_messenger_theme(location="bottom_center")
                sb.post_message("SeleniumBase wasn't detected!")

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p><mk-0><b>The code for the previous live demo:</b></mk-0></p>"
            "<hr /><br />",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>\n\n"
                "<mk-2>with SB(uc=True) as sb:</mk-2>\n"
                '<mk-3>    url = "https://gitlab.com/users/sign_in"</mk-3>\n'
                "<mk-4>    sb.uc_open_with_reconnect(url, 4)</mk-4>\n"
                "<mk-5>    sb.uc_gui_handle_captcha()</mk-5>\n\n"
                "<mk-6>    ...</mk-6>\n\n\n\n\n\n"
            ),
        )
        self.add_slide(
            "<p><b>The code for the previous live demo:</b></p>"
            "<hr /><br />",
            code=(
                "from seleniumbase import SB\n\n"
                "with SB(uc=True) as sb:\n"
                '    url = "https://gitlab.com/users/sign_in"\n'
                "    sb.uc_open_with_reconnect(url, 4)\n"
                "    sb.uc_gui_handle_captcha()\n\n"
                '<mk-1>    sb.assert_text("Username", \'[for="user_login"]\','
                ' timeout=3)</mk-1>\n'
                '<mk-2>    sb.assert_element(\'[for="user_login"]\')</mk-2>\n'
                '<mk-3>    sb.set_messenger_theme(location="bottom_center")'
                '</mk-3>\n'
                '<mk-4>    sb.post_message("SeleniumBase wasn\'t detected!")'
                '</mk-4>'
            ),
        )
        self.add_slide(
            "<h3><mk-0>Live demos, continued...</mk-0></h3>"
            "<br /><br />"
            "<h4><mk-1>Get ready for a live demo of:</mk-1></h4>"
            "<h4><mk-1>Bypassing Cloudflare with a mouse click...</mk-1></h4>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True, test=True, agent=agent) as sb:
                url = "https://gitlab.com/users/sign_in"
                sb.uc_open_with_reconnect(url, 4)
                sb.uc_gui_click_captcha()  # Only if needed
                sb.assert_element('label[for="user_login"]')
                sb.set_messenger_theme(location="bottom_center")
                sb.post_message("SeleniumBase wasn't detected!")

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p><mk-0><b>The code for the previous live demo:</b></mk-0></p>"
            "<hr /><br />",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>\n\n"
                "<mk-2>with SB(uc=True) as sb:</mk-2>\n"
                '<mk-3>    url = "https://gitlab.com/users/sign_in"</mk-3>\n'
                "<mk-4>    sb.uc_open_with_reconnect(url, 4)</mk-4>\n"
                "<mk-5>    sb.uc_gui_click_captcha()</mk-5>\n\n"
                "<mk-6>    ...</mk-6>\n\n\n\n\n"
            ),
        )
        self.add_slide(
            "<p><b>The code for the previous live demo:</b></p>"
            "<hr /><br />",
            code=(
                "from seleniumbase import SB\n\n"
                "with SB(uc=True) as sb:\n"
                '    url = "https://gitlab.com/users/sign_in"\n'
                "    sb.uc_open_with_reconnect(url, 4)\n"
                "    sb.uc_gui_click_captcha()\n\n"
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
            "<p><mk-0><b>Quick recap of what you just learned:</b>"
            "</mk-0></p><hr /><div></div>"
            "<ul>\n"
            "<li><mk-1>Activate UC Mode with <code><b>SB(uc=True)</b></code>"
            "</mk-1></li><br />\n"
            "<li><mk-2>Navigate with stealth by calling "
            "<code><b>sb.uc_open_with_reconnect(url)</b></code>"
            "</mk-2></li><br />\n"
            "<li><mk-3>Use <code><b>sb.uc_gui_handle_captcha()</b></code>"
            " or <code><b>sb.uc_gui_click_captcha()</b></code>"
            " to bypass CAPTCHAs as needed.</mk-3></li>\n"
            "</ul>\n"
            "<p><br /><mk-4>(It's that easy!)</mk-4></p><br />\n"
        )
        self.add_slide(
            "<p><mk-0><b>Things can get more complicated</b></mk-0></p>"
            "<hr /><div></div><br />"
            "<ul>\n"
            "<li><mk-1>Previous tutorials mentioned this method:<br />"
            "<code><b>sb.uc_click(selector)</b></code>"
            "</mk-1></li><br />\n"
            "<mk-2>Although this method can no longer click a<br />"
            "CAPTCHA directly, it should be used when<br />"
            "clicking on something else that causes a<br />"
            "CAPTCHA to appear after that.</mk-2>\n"
            "<br /><br />"
            "<li><mk-3>Here's a live demo of that...</mk-3></li><br />\n"
            "</ul>\n"
            "<p><br /></p><br />\n"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True, incognito=True, locale_code="en") as sb:
                url = "https://ahrefs.com/website-authority-checker"
                input_field = 'input[placeholder="Enter domain"]'
                submit_button = 'span:contains("Check Authority")'
                sb.uc_open_with_reconnect(url)  # The bot-check is later
                sb.type(input_field, "github.com/seleniumbase/SeleniumBase")
                sb.reconnect(0.1)
                sb.uc_click(submit_button, reconnect_time=4)
                sb.uc_gui_click_captcha()
                sb.wait_for_text_not_visible("Checking", timeout=10)
                sb.highlight('p:contains(".com/seleniumbase/SeleniumBase")')
                sb.highlight('a:contains("Top 100 backlinks")')
                sb.set_messenger_theme(location="bottom_center")
                sb.post_message("SeleniumBase wasn't detected!")

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p><mk-0>The code for the previous live demo can be<br />"
            "found in the SeleniumBase GitHub repo:<br /><br />"
            "<code>github.com/seleniumbase/SeleniumBase</code></mk-0>"
            "<br /><br /><br /><br />"
            '<mk-1>(See the "examples" folder for all examples)</mk-1></p>\n'
        )
        self.add_slide(
            "<h3><mk-0>Live demos, continued...</mk-0></h3>"
            "<br /><br />"
            "<h4><mk-1>Get ready for another live demo of"
            " using the <code>uc_click(selector)</code> method"
            " to bypass a Cloudflare CAPTCHA on"
            " <code>steamdb.info</code> ...</mk-1></h4>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True, test=True, disable_csp=True) as sb:
                url = "https://steamdb.info/"
                sb.uc_open_with_reconnect(url, 3)
                sb.uc_click("a.header-login span", 3)
                sb.uc_gui_click_captcha()
                sb.assert_text("Sign in", "button#js-sign-in", timeout=3)
                sb.uc_click("button#js-sign-in", 2)
                sb.highlight("div.page_content form")
                sb.highlight('button:contains("Sign in")', scroll=False)
                sb.set_messenger_theme(location="top_center")
                sb.post_message("SeleniumBase wasn't detected", duration=4)

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p><mk-0><b>The code for the previous live demo:</b></mk-0></p>"
            "<hr /><br />",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>\n\n"
                "<mk-2>with SB(uc=True, disable_csp=True) as sb:</mk-2>\n"
                '<mk-3>    url = "https://steamdb.info/"</mk-3>\n'
                "<mk-4>    sb.uc_open_with_reconnect(url, 3)</mk-4>\n"
                '<mk-5>    sb.uc_click("a.header-login span", 3)</mk-5>\n\n'
                "<mk-6>    ...</mk-6>\n\n\n\n\n\n\n\n"
            ),
        )
        self.add_slide(
            "<p><b>The code for the previous live demo:</b></p>"
            "<hr /><br />",
            code=(
                "from seleniumbase import SB\n\n"
                "with SB(uc=True) as sb:\n"
                '    url = "https://steamdb.info/"\n'
                "    sb.uc_open_with_reconnect(url, 3)\n"
                '    sb.uc_click("a.header-login span", 3)\n\n'
                "<mk-0>    sb.uc_gui_click_captcha()</mk-0>\n"
                '<mk-1>    sb.assert_text("Sign in", "button#js-sign-in",'
                ' timeout=3)</mk-1>\n'
                '<mk-2>    sb.uc_click("button#js-sign-in", 2)</mk-2>\n'
                '<mk-3>    sb.highlight("div.page_content form")</mk-3>\n'
                '<mk-4>    sb.highlight(\'button:contains("Sign in")\','
                ' scroll=False)</mk-4>\n'
                '<mk-5>    sb.set_messenger_theme(location="top_center")'
                '</mk-5>\n'
                '<mk-6>    sb.post_message("SeleniumBase wasn\'t detected!")'
                '</mk-6>\n'
            ),
        )
        self.add_slide(
            "<p>👤 <mk-0><b>Important information</b></mk-0> 👤</p>"
            "<hr /><div></div>"
            "<ul>\n"
            "<li><mk-1>UC Mode now requires <code>PyAutoGUI</code> for all"
            " features to work.</mk-1></li><p></p>\n"
            "<li><mk-2>PyAutoGUI may require enabling admin-level permissions"
            " for controlling the mouse and the keyboard.</mk-2></li><p></p>\n"
            "<p></p>"
            "<li><mk-3><code>PyAutoGUI</code> doesn't support Headless Mode."
            "</mk-3></li>\n<p></p>"
            "<li><mk-4>UC Mode now includes a special virtual display"
            " on Linux so that you no longer need to use Headless Mode"
            " in GUI-less environments.</mk-4></li>\n"
            "</ul>\n"
            "<p></p>\n"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>General information</b></mk-0> 👤</p>"
            "<hr /><br />"
            "<p><mk-1>Don't assume that all CAPTCHA services"
            " are secure, even if they say they are...</mk-1></p>"
            "<br /><br /><br /><br />"
        )
        self.add_slide(
            "<p>👤 <b>General information</b> 👤</p>"
            "<hr /><br />"
            "<p>Don't assume that all CAPTCHA services"
            " are secure, even if they say they are...</p><br />"
            "<p><mk-0>(Looking at you, Cloudflare!)</mk-0></p><br />"
            "<div /><p></p>\n"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>General information</b></mk-0> 👤</p>"
            "<hr /><br />"
            "<p><mk-1>"
            "On the other hand,<br />"
            "some CAPTCHA services are quite good..."
            "</mk-1></p>"
            "<br /><br /><br /><br />"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True, test=True) as sb:
                url = "https://seleniumbase.io/apps/recaptcha"
                sb.uc_open_with_reconnect(url)
                sb.uc_gui_click_captcha()  # Try with PyAutoGUI Click
                sb.assert_element("img#captcha-success", timeout=3)
                sb.set_messenger_theme(location="top_left")
                sb.post_message("SeleniumBase wasn't detected")

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p>👤 <b>General information</b> 👤</p>"
            "<hr /><br />"
            "<p>On the other hand,<br />"
            "some CAPTCHA services are quite good..."
            "</p><br />"
            "<p><mk-0>(Well done, Google reCAPTCHA!)</mk-0></p><br />"
            "<div /><p></p>\n"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>General information</b></mk-0> 👤</p>"
            "<hr /><br />"
            "<p><mk-1>"
            "However, the real reason UC Mode is popular,"
            " which you saw earlier,"
            " is because of the Cloudflare-bypass capabilities."
            " That's where the reputation comes from..."
            "</mk-1></p>"
            "<br /><br /><br /><br />"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>Catching up</b></mk-0> 👤</p>"
            "<hr /><br />"
            "<p><mk-1>"
            "If this is your first tutorial on UC Mode or SeleniumBase,"
            " then here are some important<br />things to know to"
            " understand things better..."
            "</mk-1></p>"
            "<br /><br /><br /><br />"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>What is SeleniumBase?</b></mk-0> 👤</p>"
            "<hr /><br />"
            "<p><mk-1>"
            "SeleniumBase is a complete framework for web automation"
            " and testing with Python and Selenium."
            "</mk-1><br /><br /><mk-2>"
            "Although there are many different features,<br />"
            "the most popular one today is UC Mode,<br />"
            "which enables Selenium browsers to appear<br />"
            "as human-controlled browsers to websites."
            "</mk-2></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>Structuring Scripts / Tests</b></mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "There are different ways of stucturing SeleniumBase scripts."
            ' (Internally called: "The 23 Syntax Formats")'
            "</mk-1><br /><br /><mk-2>"
            'Most examples use Syntax Format 1: "BaseCase direct class'
            ' inheritance", which uses the "pytest" test runner.'
            "</mk-2><br /><br /><mk-3>"
            'The next one in popularity is Syntax Format 21: "SeleniumBase SB"'
            ' (Python context manager)",<br />which is ideal and recommended'
            " for UC Mode."
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_sf_01.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_sf_21.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<div>📊 <b>The SeleniumBase GitHub Page</b> 📊</div>"
            '<img src="https://seleniumbase.io/other/sb_github.jpg"'
            ' width="100%">'
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
            "<p><b>About me: (Michael Mintz)</b></p>\n"
            "<ul>\n"
            "<li><mk-0>I've reached over 2 million developers<br />"
            " on Stack Overflow.</mk-0></li>\n"
            "</ul>"
            '<img src="https://seleniumbase.io/other/me_st_o_reached.jpg"'
            ' width="88%">'
        )
        self.add_slide(
            "<p>👤 <mk-0><b>The Great CAPTCHA Duel:</b></mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "Throughout the past few years, Cloudflare has pushed a lot"
            " of changes to their Turnstile CAPTCHA."
            "</mk-1><br /><br /><mk-2>"
            "In order to keep UC Mode working, I had to push a lot of"
            " updates to counter those changes."
            "</mk-2><br /><br /><mk-3>"
            "It has been an epic duel..."
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>The Great CAPTCHA Duel:</b></mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "Sometimes Cloudflare pushed multiple<br />"
            "changes at the same time..."
            "</mk-1><br /><br /><mk-2>"
            "That's when I had to make multiple<br />"
            "UC Mode updates to counter those changes..."
            "</mk-2><br /><br /><mk-3>"
            "Sometimes I received a little assistance from GitHub..."
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Timeline of major Cloudflare updates</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "<b>March 20, 2024</b>: Cloudflare pushed a major update"
            " where they could detect UC Mode Selenium clicks."
            "</mk-1><br /><br /><mk-2>"
            "Outcome: UC Mode's <code>uc_click(selector)</code> method"
            " was updated to click on CAPTCHAs<br />via JavaScript using"
            " <code>window.setTimeout()</code>."
            "</mk-2><br /><br /></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Timeline of major Cloudflare updates</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "<b>May 10, 2024</b>: Cloudflare pushed a major update"
            " where CSS Selectors of CAPTCHAs were updated."
            "</mk-1><br /><br /><mk-2>"
            "Outcome: I had to update all the UC Mode<br />"
            'examples to change "span.mark" to just "span".'
            "</mk-2><br /><br /></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Timeline of major Cloudflare updates</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "<b>June 7, 2024</b>: Cloudflare pushed an update where CAPTCHAs"
            " could detect JavaScript clicks.<br />(This was a major setback!)"
            "</mk-1><br /><br /><mk-2>"
            "Outcome: I had to add new UC Mode methods for clicking on"
            " CAPTCHAs with <code>PyAutoGUI</code>."
            "</mk-2><br /><br /></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Timeline of major Cloudflare updates</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "<b>July 8, 2024</b>: Cloudflare made an update where CAPTCHAs"
            " were hidden behind Shadow-DOM.<br />"
            "(They went for a killing blow!)"
            "</mk-1><br /><br /><mk-2>"
            "Outcome: I updated existing UC Mode methods so they could"
            " determine the CAPTCHA coordinates<br />for"
            " <code>PyAutoGUI</code>."
            " (Same-day delivery, thanks to an advanced warning"
            " on Discord a few days earlier.)"
            "</mk-2><br /><br /></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Timeline of major Cloudflare updates</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "<b>July 25, 2024</b>: Cloudflare made updates to the<br />"
            "CSS Selectors that come before Shadow-DOM."
            "</mk-1><br /><br /><mk-2>"
            "Outcome: I updated existing UC Mode methods."
            "</mk-2><br /><br /><mk-3>"
            'Note: You can use "uc_gui_handle_captcha()" or<br />'
            '"uc_gui_click_captcha()" for any CAPTCHA now.<br />'
            '(On Linux, only "uc_gui_click_captcha" works.)'
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Timeline of major Cloudflare updates</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "Only minor changes from Cloudflare<br />"
            "have been shipped since then so far..."
            "</mk-1><br /><br /><mk-2>"
            "Remember: Give me space to work<br />"
            "on UC Mode updates as needed..."
            "</mk-2><br /><br /><mk-3>"
            "...because you never know when they'll strike next..."
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Theories on how Cloudflare detects JS</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "A month before Cloudflare added JS-detection,<br />"
            "a GitHub repo named Brotector was released."
            "</mk-1><br /><br /><mk-2>"
            "Brotector is capable of detecting both Selenium & JS."
            "</mk-2><br /><br /><mk-3>"
            "Based on experiements, Brotector's detection mechanisms"
            " appear to get the same results as Cloudflare's detection"
            " mechanisms.<br />(It appears that Cloudflare learned from them.)"
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            "<div><b>Brotector info</b></div>"
            '<img src="https://seleniumbase.io/other/brotector_gh1.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<div><b>Brotector info</b></div>"
            '<img src="https://seleniumbase.io/other/brotector_gh2.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<p>👤 <mk-0>Using Brotector to make UC Mode better</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "In order to make UC Mode better, I decided to build my own"
            " open-source CAPTCHA using Brotector:<br />"
            '"The Brotector CAPTCHA"'
            "</mk-1><br /><br /><mk-2>"
            "Unlike Cloudflare's detection system, which only scans for"
            " bots on page loads and CAPTCHA-clicks, the Brotector CAPTCHA"
            " continuously scans for bots."
            "</mk-2><br /><br /><mk-3>"
            "This makes it a more powerful anti-bot system."
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/brotector_c1.png"'
            ' width="70%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/brotector_c2.png"'
            ' width="84%">'
        )
        self.add_slide(
            "<h2><mk-0>Here's a LIVE DEMO of Brotector CAPTCHA:</mk-0></h2>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(test=True) as sb:
                url = "https://seleniumbase.io/hobbit/login"
                sb.open(url)
                sb.click_if_visible("button")
                sb.assert_text("Gandalf blocked you!", "h1")
                sb.click("img")
                sb.highlight("h1")
                sb.sleep(3)  # Gandalf: "You Shall Not Pass!"

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<h3><mk-0>Here's a LIVE DEMO of UC Mode bypassing"
            " Brotector CAPTCHA:</mk-0></h3>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True, test=True) as sb:
                url = "https://seleniumbase.io/hobbit/login"
                sb.uc_open_with_disconnect(url, 2.2)
                sb.uc_gui_press_keys("\t ")
                sb.reconnect(1.5)
                sb.assert_text("Welcome to Middle Earth!", "h1")
                sb.set_messenger_theme(location="bottom_center")
                sb.post_message("SeleniumBase wasn't detected!")
                sb.click("img")
                sb.sleep(5.888)  # Cool animation happening now!

        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            "<p>👤 <mk-0>What happens when Cloudflare adds real-time<br />"
            "bot-detection, like Brotector already has?</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "Currently, UC Mode uses Selenium to locate the CAPTCHA checkbox"
            " before the <code>PyAutoGUI</code> click.<br />(This is fine"
            " for now because CF only scans<br />"
            "during page loads and CAPTCHA clicks.)"
            "</mk-1><br /><br /><mk-2>"
            "There's already a plan in place for the day<br />"
            "Cloudflare adds real-time bot-scanning..."
            "</mk-2><br /></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>The plan to handle real-time bot-scanning</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p>"
            '<pre><code>sb.uc_gui_click_captcha(frame="iframe", retry=False,'
            ' <mk-1>blind=True</mk-1>)</code></pre><br /><mk-1>'
            'Set the third arg, `blind`, to `True` to force a retry'
            ' (if the first click failed) by clicking at the last known'
            ' coordinates of the CAPTCHA checkbox without confirming first'
            ' with Selenium that a CAPTCHA is still on the page.'
            ' (The page will need to reload first.)'
            "</mk-1><br /><br /></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0>Field trip to the UC Mode help docs</mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "Let's take a look at the UC Mode docs<br />"
            "from the SeleniumBase GitHub repo..."
            "</mk-1></p>"
            '<a href="https://github.com/seleniumbase/SeleniumBase/blob/'
            'master/help_docs/uc_mode.md" target="_blank">'
            '<img src="https://seleniumbase.io/other/sb_github.jpg"'
            ' width="50%"></a>'
        )
        self.add_slide(
            "<p>👤 <mk-0><b>Study, study, study!</b></mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "There's lots of important information in the UC Mode docs,"
            " so study well to avoid falling into traps..."
            "</mk-1><br /><br /><mk-2>"
            "Sometimes you might still be able to<br />"
            "get out of a trap you fell into..."
            "</mk-2><br /><br /><mk-3>"
            "Once you bypass a CAPTCHA, be ready for anything!"
            "</mk-3></p>"
            "<br />"
        )
        self.add_slide(
            "<p>👤 <mk-0><b>There's more to come</b></mk-0> 👤</p>"
            "<hr /><h6><br /></h6>"
            "<p><mk-1>"
            "As usual, export more UC Mode updates,<br />"
            "but new projects are classified until released."
            "</mk-1></p>"
            "<br />"
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
            "<h3>"
            "🛠️ <mk-1>SeleniumBase gives you</mk-1> 🛠️<br />"
            "<mk-1>the tools you need to succeed!"
            "</mk-1></h3>"
            "<h3><mk-2><br />"
            "And tools to build lots of bots..."
            "</mk-2></h3><br />"
        )
        self.add_slide(
            "<div>🏁 <b>The End</b> 🏁</div>"
            '<img src="https://seleniumbase.io/other/sb_github.jpg"'
            ' width="100%">'
        )
        self.begin_presentation(filename="uc_presentation.html")
