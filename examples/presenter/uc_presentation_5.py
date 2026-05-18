# https://www.youtube.com/watch?v=R9HNsnbYh8o
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class UCPresentationClass(BaseCase):
    def test_presentation_5(self):
        self.open("data:,")
        self.set_window_position(4, 40)
        self._output_file_saves = False
        self.create_presentation(theme="serif", transition="none")
        self.add_slide("<h2>Press SPACE to continue!</h2>\n")
        self.add_slide(
            '<img src="https://seleniumbase.io/other/ua_title_5th.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>This continues the series that started here...</h4>"
            '<img src="https://seleniumbase.io/other/first_ua_vid.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<p><mk-0>🔹 <b>We're going to be using...</b> 🔹</mk-0></p><hr />"
            '<img src="https://seleniumbase.io/other/four_parts.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<p><mk-0>🔹 <b>To bypass all the CAPTCHAs...</b> 🔹</mk-0></p>"
            "<hr /><br />"
            '<img src="https://seleniumbase.io/other/anti_bot_services.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<p><mk-0>🔹 <b>In all the places...</b> 🔹</mk-0></p><hr /><br />"
            "<mk-1>✅ Local Desktop Machine - (Eg. Mac/Windows)</mk-1>"
            "<br /><br />"
            "<mk-2>✅ Docker Container - (Eg. <code>ubuntu:24.04</code>)"
            "</mk-2><br /><br />"
            "<mk-3>✅ Linux Server - (Eg. GitHub Actions)</mk-3><br /><br />"
        )
        self.add_slide(
            "<p><mk-0>🔹 <b>With live demos on major sites...</b> 🔹"
            "</mk-0></p><hr />"
            "<mk-1>✅ TikTok</mk-1><br /><br />"
            "<mk-2>✅ Facebook</mk-2><br /><br />"
            "<mk-3>✅ Amazon</mk-3><br /><br />"
            "<mk-4>✅ LinkedIn</mk-4><br /><br />"
            "<mk-5>✅ And many more!</mk-5><br /><br />"
        )
        self.add_slide(
            "<p><b>Get ready for some serious hacking!</b></p>"
            '<img src="https://seleniumbase.io/other/hackers_at_comp.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<br /><mk-0><b>Let's warm up with a few live demos<br />"
            "of bypassing Cloudflare's Turnstile...</b></mk-0><hr /><br />"
            '<img src="https://seleniumbase.io/other/cf_turnstile2.png"'
            ' width="70%"><br />'
            '<img src="https://seleniumbase.io/other/cf_success.png"'
            ' width="70%">'
        )
        self.add_slide(
            "<mk-0>With the tools I'll be covering in this video,<br />"
            "you be able to web-scrape sites with confidence.</mk-0>"
            "<hr /><br />"
            '<img src="https://seleniumbase.io/other/blue_chrome.jpg"'
            ' width="22.75%">'
            '<img src="https://seleniumbase.io/other/anti_bot_services.jpg"'
            ' width="60%">'
        )
        self.add_slide(
            "<h4>This continues my Undetectable Automation series:</h4>"
            '<img src="https://seleniumbase.io/other/first_4_ua_titles.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4>That all started with...</h4>"
            '<img src="https://seleniumbase.io/other/first_ua_vid.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h5>The Automation Entertainment Industry was born.</h5>"
            '<img src="https://seleniumbase.io/other/automation_industry.png"'
            ' width="86%">'
        )
        self.add_slide(
            "<h4>The field changes rapidly, so it's important to<br />"
            "note that the first three videos are out-of-date.</h4>"
            '<img src="https://seleniumbase.io/other/first_4_ua_titles.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "The first three used a modified Chromedriver<br />"
            'called "Undetected Chromedriver" for stealth.<br />'
            '<img src="https://seleniumbase.io/other/first_4_ua_titles.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "At some point, modifying Chromedriver<br />wasn't enough to make "
            "WebDriver actions<br />stealthy because anti-bot services "
            "improved.<br />"
            '<img src="https://seleniumbase.io/other/first_4_ua_titles.jpg"'
            ' width="85%">'
        )
        self.add_slide(
            "<mk-0>That led to the rise of CDP in order to bypass CAPTCHAs "
            " and bot-detection services again.</mk-0><hr />"
            '<img src="https://seleniumbase.io/other/cdp_logo.jpg"'
            ' width="50%"><hr />'
            "<h5><mk-1>(This was the focus the 4th Undetectable Automation "
            "video.)</mk-1></h5>"
        )
        self.add_slide(
            "<mk-0>Lots of changes have happened since the last<br />"
            "video in the Undetectable Automation series:</mk-0>"
            '<img src="https://seleniumbase.io/other/uc4_title.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<h4><mk-0>Here are some advancements since then:"
            "</mk-0><br /></h4><hr /><br />"
            "<ul>\n"
            '<mk-1>✅ Stealthy Playwright Mode.</mk-1>'
            "<br />\n"
            '<mk-2>✅ Stealthy Docker automation.</mk-2>'
            "<br />\n"
            '<mk-3>✅ Stealthy headless automation.</mk-3>'
            "<br />\n"
            '<mk-4>✅ Stealthy mobile emulation.</mk-4>'
            "<br />\n"
            '<mk-5>✅ Imperva-based hCaptcha can be bypassed.</mk-5>'
            "<br />\n"
            '<mk-6>✅ Friendly Captcha can be bypassed.</mk-6>'
            "<br />\n"
            '<mk-7>✅ DataDome Slider can be bypassed.</mk-7>'
            "<br />\n"
            '<mk-8>✅ Unbranded Chromium support.</mk-8>'
            "<br />\n"
            '<mk-9>✅ Pure CDP Mode.</mk-9>'
            "<br />\n"
            "\n</ul><br /><br />\n"
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
            "<h4>Compared to standard JS, CDP actions are stealthy!</h4>"
            '<img src="https://seleniumbase.io/other/js_vs_cdp.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<p><mk-0>🔹 <b>CDP alone isn't enough for stealth...</b> 🔹</mk-0>"
            "</p><hr />"
            "<mk-1>✅ The web browser's fingerprint must look like<br />"
            "one coming from a human-controlled browser.</mk-1>"
            "<br /></p>"
            '<img src="https://seleniumbase.io/other/robotic_arm_shield.jpg"'
            ' width="75%">'
        )
        self.add_slide(
            "<h5><mk-0>Browsers launched with regular Playwright or WebDriver"
            "<br />have a poisoned fingerprint that results in bot-detection."
            "</mk-0></h5><hr />"
            '<img src="https://seleniumbase.io/other/fingerprint_snake.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h5>"
            "<mk-0>To avoid this issue, you can launch the system's default "
            "<br />browser... and <i>THEN</i> attach the automation framework!"
            "</mk-0></h5><hr />"
            '<img src="https://seleniumbase.io/other/special_config.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>Some special configuration is needed"
            "<br />to make this work in a stealthy way.</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/special_config_2.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>And you may need special methods"
            "<br />for handling CAPTCHAs successfully</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/robotic_arm_screen.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>⤵️ (That brings us to SeleniumBase..."
            "<br />a framework that takes care of"
            "<br />a lot of that work for you...)</mk-0></h4>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_github_page2.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/stealthy_pw_yt.jpg"'
            ' width="86%">'
        )
        self.add_slide(
            "<mk-0>Contrary to logical thinking,<br />"
            "SeleniumBase no longer uses Selenium<br />"
            "for some things (such as CDP Mode).</mk-0>"
            "<br />"
            '<p><img src="https://seleniumbase.io/other/thinking_chromium.jpg"'
            ' width="38%"></p>'
            "<h5><mk-1>If that sounds confusing, "
            "note that JavaScript does not use Java.</mk-1></h5>"
        )
        self.add_slide(
            "<h4><mk-0>SeleniumBase CDP Mode comes in 3 formats:"
            "</mk-0><br /></h4><hr /><br />"
            "<ul>\n"
            '<mk-1>✅ <code>SB()</code> "nested sync" format.</mk-1>'
            "<br /><br />\n"
            '<mk-2>✅ <code>sb_cdp</code> "sync" format. (Pure CDP)</mk-2>'
            "<br /><br />\n"
            '<mk-3>✅ <code>cdp_driver</code> "async" format. (Pure CDP)</mk-3>'
            "<br /><br />\n"
            '<mk-4>"Stealthy Playwright Mode" can be'
            "<br />initiated from any of these formats.</mk-4>"
            "\n</ul><br /><br />\n"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_architecture.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<p><mk-0><code>sb_cdp</code> "sync" Stealthly Playwright Mode '
            'example:</mk-0></p>'
            "<hr />",
            code=(
                "<mk-1>from playwright.sync_api import sync_playwright</mk-1>"
                "\n"
                "<mk-2>from seleniumbase import sb_cdp</mk-2>\n\n"
                '<mk-3>sb = sb_cdp.Chrome()</mk-3>\n'
                "<mk-4>endpoint_url = sb.get_endpoint_url()</mk-4>\n\n"
                "<mk-5>with sync_playwright() as p:</mk-5>\n"
                "<mk-6>    browser = p.chromium.connect_over_cdp(endpoint_url)"
                "</mk-6>\n"
                "<mk-7>    page = browser.contexts[0].pages[0]</mk-7>\n"
                '<mk-8>    page.goto("https://copilot.microsoft.com")</mk-8>\n'
                '<mk-9>    page.wait_for_selector("textarea#userInput")</mk-9>'
                '\n'
                '<mk-10>    query = "Playwright Python connect_over_cdp() '
                'sync example"</mk-10>\n'
                '<mk-11>    page.fill("textarea#userInput", query)</mk-11>\n'
                '<mk-12>    page.wait_for_timeout(2000)</mk-12>\n'
                '<mk-13>    page.click(\'button['
                'data-testid="submit-button"]\')</mk-13>\n'
                '<mk-14>    sb.sleep(5.25)</mk-14>\n'
                '<mk-15>    sb.solve_captcha()</mk-15>\n'
                "<mk-16>    ...</mk-16>\n"
            ),
        )
        self.add_slide(
            "<br /><mk-0>"
            "<b>It's time for that live demo where we use Stealthy<br />"
            "Playwright Mode to bypass Copilot's CAPTCHA...</b>"
            "</mk-0><hr />"
            '<img src="https://seleniumbase.io/other/copilot_captcha.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<br /><mk-0>"
            "<b>Are you ready for another live demo?</b></mk-0><br /><br />"
            "<mk-1><b>Let's do some Walmart scraping now...</b></mk-1><br />"
        )
        self.add_slide(
            "<br /><mk-0><b>"
            "Let's do another live demo<br />before returning to the learning."
            "<br /><br /></b></mk-0><mk-1>"
            "This time, we're web-scraping TikTok...</mk-1><br /><br />"
        )
        self.add_slide(
            "<mk-0>In addition to using CDP for controlling Chrome in a"
            " stealthy way, you can also achieve stealth by using"
            " tools that can control the mouse and keyboard.</mk-0>"
            "<br /><br /><mk-1><code>PyAutoGUI</code> is one such tool:</mk-1>"
            '<img src="https://seleniumbase.io/other/pyautogui_tree.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<mk-0>PyAutoGUI requires a headed browser to work.</mk-0>"
            "<br /><br /><mk-1>"
            " Since most Linux machines have headless displays that"
            " don't support headed browsers, an external tool called"
            " Xvfb must be used in order to simulate a headed browser"
            " in a headless Linux environment...</mk-1>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/xvfb_info.jpg"'
            ' width="56%">'
        )
        self.add_slide(
            "<h5><mk-0>Xvfb is automatically used when needed in SeleniumBase."
            "<br />This makes stealthy automation easy from Linux servers."
            "</mk-0></h5>"
            '<img src="https://seleniumbase.io/other/gh_actions_scrape.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>Here's another GitHub Actions example:</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/gha_scraping.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>I have a full YouTube tutorial on that:</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/web_scraping.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>Same story with stealthy Docker automation:</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/stealthy_docker.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-1>Note that Docker requires extra config to be stealthy!"
            "</mk-1></h4><h4><mk-2>"
            "These changes can be made from the <code>Dockerfile</code>."
            "</mk-2></h4>"
            '<img src="https://seleniumbase.io/other/ai_docker_whale.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-1>For instance, some standard fonts are not<br />"
            "installed from the default Docker config.</mk-1></h4>"
            '<img src="https://seleniumbase.io/other/docker_whale.jpg"'
            ' width="75%">'
        )
        self.add_slide(
            "<h4><mk-1>This is a problem because websites can see<br />"
            "which fonts are installed on your system.</mk-1></h4>"
            '<img src="https://seleniumbase.io/other/fingerprint_fonts.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4><mk-1>If your system is missing standard fonts,<br />"
            "then websites know you're running from a server,<br />"
            "and therefore they know you're using automation.</mk-1></h4>"
            '<img src="https://seleniumbase.io/other/seeing_eye_server.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4><mk-0>The SeleniumBase <code>Dockerfile</code>"
            " has you covered:</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/sb_dockerfile.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-1>It would be a big mistake to think that you can<br />"
            "be stealthy in a regular Docker container without<br />"
            "changing the default fonts and configuration...</mk-1></h4>"
            '<img src="https://seleniumbase.io/other/in_server_room.jpg"'
            ' width="75%">'
        )
        self.add_slide(
            "<h3><mk-1>In the spirit of online shopping,<br />"
            "the next demo is on Nordstrom...</mk-1></h3>"
        )
        self.add_slide(
            "<h3><mk-1>And now for some Ralph Lauren...</mk-1></h3>"
        )
        self.add_slide(
            "<h3><mk-1>Let's wrap up this quick"
            "<br />shopping session on Kohls...</mk-1></h3>"
        )
        self.add_slide(
            "<h5><mk-0>Now that we have the ingredients for stealth..."
            "</mk-0><br /></h5><hr />"
            "<ul>\n"
            '<mk-1>✅ An automation framework that uses'
            '<br />a browser with a natural fingerprint.</mk-1>'
            "<br /><br />\n"
            "<mk-2>✅ CDP methods for performing natural actions"
            '<br />(eg. <code>Input.dispatchMouseEvent</code>).</mk-1>'
            "</mk-2><br /><br />\n"
            "<mk-3>✅ PyAutoGUI for performing trickier actions"
            "<br />(eg. drag-and-drop with a real mouse).</mk-3>"
            "<br /><br />\n"
            "<mk-4>✅ Xvfb integration for using headed browsers"
            "<br />on Linux systems that don't have a GUI.</mk-4>"
            "\n</ul><br /><br />\n"
        )
        self.add_slide(
            "<mk-0>We can use all that to bypass different CAPTCHAs!</mk-0>"
            "<br /><br />"
            "<mk-1>Get ready for some live demos of that!</mk-1>"
            "<br /><br />"
            '<img src="https://seleniumbase.io/other/easy_captchas.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><br /><mk-0>🔹 One method call does it all: 🔹"
            "</mk-0><br /></h4><hr /><br /><br />"
            "<ul>\n"
            '<h3><mk-1>✅ <code>sb.solve_captcha()</code></mk-1></h3>'
            "<br /><br />\n"
            "\n</ul><br /><br />\n"
        )
        self.add_slide(
            "<h4><mk-0><code>sb.solve_captcha()</code> handles all of these:"
            "</mk-0><br /></h4><hr /><br />"
            "<ul>\n"
            '<mk-1>✅ Cloudflare Turnstile</mk-1>'
            "<br /><br />\n"
            "<mk-2>✅ Friendly Captcha</mk-1>"
            "</mk-2><br /><br />\n"
            "<mk-3>✅ DataDome Slider Captcha</mk-3>"
            "<br /><br />\n"
            "<mk-4>✅ Imperva-based hCaptcha</mk-4>"
            "\n</ul><br /><br />\n"
        )
        self.add_slide(
            "<mk-0>It may <i>seem</i> a bit odd or illegal that<br />"
            "we're bypassing all these CAPTCHAs...</mk-0>"
            "<br /><br /><mk-1>"
            "but things may not actually be as they <i>seem</i>...</mk-1>"
            '<img src="https://seleniumbase.io/other/odd_bypass.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h3><mk-0>Important Notice:</mk-0></h3>"
            "<mk-1>(Know the laws and legal implications of scraping!)</mk-1>"
            '<img src="https://seleniumbase.io/other/legal_scraping.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/meta_vs_bd.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/ai_meta_vs_bd_1.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/ai_meta_vs_bd_2.jpg"'
            ' width="88%">'
        )
        self.add_slide(
            "<mk-0>Now that we all know scraping public data is legal,</mk-0>"
            "<br /><br />"
            "<mk-1>let's go web-scraping on Facebook's public pages...</mk-1>"
        )
        self.add_slide(
            "<mk-0>If a site wants to hide its public data from scrapers,"
            "</mk-0><br /><br /><mk-1>"
            "then it'll need to hide that data from public view...</mk-1>"
        )
        self.add_slide(
            "<mk-0>Note that if automation performs actions too quickly,<br />"
            "websites may detect this as bot-traffic and block you...</mk-0>"
            "<br /><br />"
            "<mk-1>To avoid this:</mk-1><br /><br />"
            "<mk-2>✅ Space out your actions so that the"
            "<br />automation moves at human-like speed.</mk-2>"
            "<br /><br />"
            "<mk-3>✅ Random <code>sleep()</code> calls can help.</mk-3>"
        )
        self.add_slide(
            "<h4>This is what happens when some anti-bots detect you:</h4>"
            '<img src="https://seleniumbase.io/other/you_are_blocked.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4><mk-0>When that happens, your bot might not get a "
            "chance to solve a CAPTCHA to prove its humanity.</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/blocked_captchas.jpg"'
            ' width="70%">'
            "<h4><br /><mk-1>In other cases, your bot may face a challenge..."
            "</mk-1></h4>"
        )
        self.add_slide(
            "<h4><mk-0>This is what happens when hCAPTCHA detects bots:"
            "</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/hcaptcha_puppy.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h4><mk-0>This is what happens when reCAPTCHA detects bots:"
            "</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/recaptcha_v2b.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>And this is what happens when Gandalf blocks you:"
            "</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/gandalf.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h3><mk-0>Get ready for a web-scraping<br />"
            "live demo on Amazon.com ...</mk-0></h3>"
        )
        self.add_slide(
            "<p><mk-0>Let's take a look at that Amazon-scraping script:"
            "</mk-0></p>"
            "<hr />",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>"
                "\n\n"
                "<mk-2>with SB(uc=True, test=True, ad_block=True) as sb:"
                "</mk-2>\n"
                '<mk-3>    url = "https://www.amazon.com"</mk-3>\n'
                "<mk-4>    sb.activate_cdp_mode(url)</mk-4>\n"
                "<mk-5>    sb.sleep(2)</mk-5>\n"
                "<mk-6>    sb.click_if_visible('button"
                "[alt=\"Continue shopping\"]')"
                "</mk-6>\n"
                "<mk-7>    sb.sleep(2)</mk-7>\n"
                '<mk-8>    sb.press_keys(\'input'
                '[role="searchbox"]\', "TI-89\\n")</mk-8>\n'
                '<mk-9>    sb.sleep(3)</mk-9>'
                '\n'
                '<mk-10>    for i in range(16):</mk-10>\n'
                '<mk-11>        sb.cdp.scroll_down(16)</mk-11>\n'
                '<mk-12>    print(sb.get_page_title())</mk-12>\n'
                '<mk-13>    sb.save_as_pdf_to_logs()</mk-13>\n'
                '<mk-14>    sb.save_page_source_to_logs()</mk-14>\n'
                '<mk-15>    sb.save_screenshot_to_logs()</mk-15>\n'
                '<mk-16>    print("Logs have been saved to: '
                './latest_logs/")</mk-16>\n'
            ),
        )
        self.add_slide(
            "<h4><mk-0>Let's run two live demos on Nike.com:"
            "</mk-0><br /></h4><hr /><br />"
            "<ul>\n"
            '<mk-1>1. Using Regular Chrome.</mk-1>'
            "<br /><br />\n"
            '<mk-2>2. Using Headless Chrome.</mk-2>'
            "\n</ul><br /><br />\n"
        )
        self.add_slide(
            "<p><mk-0>Let's take a look at that Nike-scraping script:"
            "</mk-0></p>"
            "<hr />",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>"
                "\n\n"
                '<mk-2>'
                'with SB(uc=True, test=True, locale="en", pls="none") as sb:'
                "</mk-2>\n"
                '<mk-3>    url = "https://www.nike.com/"</mk-3>\n'
                "<mk-4>    sb.activate_cdp_mode(url)</mk-4>\n"
                "<mk-5>    sb.sleep(2.5)</mk-5>\n"
                "<mk-6>    "
                'sb.click(\'[data-testid="user-tools-container"] search\')'
                "</mk-6>\n"
                "<mk-7>    sb.sleep(1.5)</mk-7>\n"
                '<mk-8>    search = "Nike Air Force 1"</mk-8>\n'
                '<mk-9>    sb.press_keys(\'input'
                '[type="search"]\', search)</mk-9>\n'
                '<mk-10>    sb.sleep(4)</mk-10>'
                '\n'
                '<mk-11>    details = \'ul[data-testid*="products"] '
                'figure .details\'</mk-11>\n'
                '<mk-12>    elements = sb.select_all(details)</mk-12>\n'
                '<mk-13>    if elements:</mk-13>\n'
                '<mk-14>        print(\'**** Found results for '
                '"%s": ****\' %% search)</mk-14>\n'
                '<mk-15>    for element in elements:</mk-15>\n'
                '<mk-16>        print("* " + element.text)</mk-16>\n'
            ),
        )
        self.add_slide(
            "<h4><mk-0>Here's a friendly reminder that<br />"
            "those <code>sb.sleep()</code> calls are strategic.</mk-0></h4>"
            "<mk-1>Automating too quickly can get you into<br />"
            "trouble on sites with bot-protection...</mk-1>"
            '<img src="https://seleniumbase.io/other/behind_you.jpg"'
            ' width="75%">'
        )
        self.add_slide(
            "<h4>"
            "<mk-0>Sending too much traffic to a website from the same<br />"
            "IP address could also stop your automation runners.</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/runners_stopped.jpg"'
            ' width="82%">'
        )
        self.add_slide(
            "<h4><mk-0>And some IP ranges are flagged "
            "by anti-bot services.</mk-0></h4><hr />"
            '<mk-1>⛔ Eg. "Non-residential" IP ranges (such as AWS)</mk-1>'
            "<br /><br />"
            '<img src="https://seleniumbase.io/other/safety_robotic_arm.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<mk-0>Scraping a site from a non-residential<br />"
            "IP range is a sure way to get caught...</mk-0>"
        )
        self.add_slide(
            "<h4><mk-0>This would not be a real video about <br />"
            "web-scraping unless I mentioned proxies.<br /></mk-0></h4>"
            "<mk-1>SeleniumBase has a <code>proxy</code> option for that."
            "</mk-1>"
            '<img src="https://seleniumbase.io/other/super_server.jpg"'
            ' width="66%">'
        )
        self.add_slide(
            "<p><mk-0>"
            "Here's how to configure a proxy with <b>SeleniumBase</b>:</mk-0>"
            "</p><hr /><br /><ul>\n"
            '<li><mk-1><b>Proxy via command-line:</b></mk-1>'
            '<br /><mk-2><code>pytest --proxy="host:port"</code></mk-2>'
            '<br /><mk-3><code>pytest --proxy="user:pass@host:port"</code>'
            '</mk-3>'
            '</li><br />\n'
            '<li><mk-4><b>Proxy via method arg:</b></mk-4>'
            '<br /><mk-5><code>SB(proxy="host:port")</code></mk-5>'
            '<br /><mk-6><code>SB(proxy="user:pass@host:port")</code></mk-6>'
            '</li></ul>\n'
        )
        self.add_slide(
            "<h5><mk-0>If you don't have a proxy, it's easy to get one.<br />"
            "Lots of providers out there, like Bright Data.<br />"
            "(Bright Data blogs about SeleniumBase a lot.)</mk-0>"
            "</h5>"
            '<img src="https://seleniumbase.io/other/bd_sb.jpg"'
            ' width="75%">'
        )
        self.add_slide(
            "<h4><mk-0>You could also launch your own<br />"
            "proxy server with SeleniumBase:</mk-0><br /></h4>"
            '<h3><mk-1><code>"sbase proxy"</code></mk-1></h3>'
            "<h3><mk-2>(That's it!)</mk-2></h3>"
            '<img src="https://seleniumbase.io/other/sbase_proxy.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<p><mk-0>More configuration options for "<b>sbase proxy</b>":'
            '</mk-0></p>'
            '<img src="https://seleniumbase.io/other/instant_proxy.png"'
            ' width="80%">'
        )
        self.add_slide(
            "<h4><mk-0>Since websites can detect your geolocation,<br />"
            "it may be a good idea to change it at times.</mk-0></h4>"
            "<mk-1>Fortunately, changing your geolocation/timezone<br />"
            "can be done faster than changing your hair color.</mk-1>"
            '<img src="https://seleniumbase.io/other/purple_hair.jpg"'
            ' width="82%">'
        )
        self.add_slide(
            "<p><mk-0>"
            "🌐 Here's how to configure those with <b>SeleniumBase</b>:</mk-0>"
            "</p><hr /><br /><ul>\n"
            '<li><mk-1>Changing geolocation via method arg:'
            '<br /><code>geoloc=(26.863, 80.94)</code>'
            '<br /><code>geoloc=(35.050681, 136.844728)</code>'
            '</mk-1>'
            '</li><br />\n'
            '<li><mk-2>Changing timezone via method arg:'
            '<br /><code>tzone="Asia/Kolkata"</code>'
            '<br /><code>tzone="Asia/Tokyo"</code></mk-2>'
            '</li></ul>\n'
        )
        self.add_slide(
            "<h3>🌐 <b>Timezone/Geolocation</b> 🌏</h3><br />"
            "<h4><mk-0>Let's run a live demo to show how that works:"
            "</mk-0><br /></h4><hr /><br />"
            "<ul>\n"
            "<mk-1>1. First we'll go to India.</mk-1>"
            "<br /><br />\n"
            "<mk-2>2. Then we'll go to Japan.</mk-2>"
            "\n</ul><br /><br />\n"
        )
        self.add_slide(
            "<h4><mk-0>Another cool feature of CDP is the ability<br />"
            "to intercept & modify requests in real time.</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/intercept_requests.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/cdp_con_req.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/mycdp_con_req.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/raw_req_mod.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h3><mk-0>Time for a live demo of that...</mk-0></h3>"
            "<br /><mk-0>(Intercepting/modifying requests)</mk-0>"
        )
        self.add_slide(
            "<mk-0>As you can see, SeleniumBase has all<br />"
            "the CDP features you're looking for.</mk-0><br />"
            '<img src="https://seleniumbase.io/other/sbase_gh.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<mk-0>If you're looking for powerful multi-threading,<br />"
            "then <code>ThreadPoolExecutor</code> has you covered.</mk-0>"
            '<img src="https://seleniumbase.io/other/threadpoolexecutor.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h4><mk-0>Sometimes you can defeat CAPTCHAs in advance<br />"
            "if you already have the required cookies loaded<br />"
            "in your web browser. (Eg: <code>cf_clearance</code>)</mk-0>"
            "</h4>"
            '<img src="https://seleniumbase.io/other/cf_clearance.jpg"'
            ' width="85%">'
        )
        self.add_slide(
            "<h4><mk-0>Getting the <code>cf_clearance</code> cookie is easy:"
            "</mk-0></h4><mk-1>Just go to a CF-protected site and take it!"
            "</mk-1>"
            '<img src="https://seleniumbase.io/other/get_cf_clearance.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h3><mk-0>"
            "Get ready for a live demo of<br />"
            "stealthy mobile emulation...</mk-0></h3>"
        )
        self.add_slide(
            "<h4><mk-0>For more info on stealthy mobile emulation,<br />"
            " check out the YouTube video on it:"
            "</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/stealthy_mobile.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<h4><mk-0>There's also a follow-up mobile video<br />"
            " that deals with changing the User Agent:"
            "</mk-0></h4>"
            '<img src="https://seleniumbase.io/other/user_agent_matters.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<p><mk-0>"
            "<b>SeleniumBase</b> has an option for using unbranded<br />"
            "Chromium in place of regular Google Chrome.</mk-0>"
            "</p><hr /><br />\n"
            '<img src="https://seleniumbase.io/other/chromium_chrome.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0>"
            "Here's how to use unbranded Chromium in scripts:</mk-0>"
            "</p><hr /><br /><ul>\n"
            '<li><mk-1><b>Chromium via command-line:</b>'
            '<br /><code>pytest --use-chromium</code></mk-1>'
            '</mk-3>'
            '</li><br />\n'
            '<li><mk-2><b>Chromium via method arg:</b>'
            '<br /><code>SB(use_chromium=True)</code></mk-2>'
            '</li></ul><br /><br />\n'
            "<mk-3>(Chromium is automatically downloaded<br />"
            "if it hasn't yet been used by SeleniumBase)</mk-3>"
        )
        self.add_slide(
            "<p><mk-0>"
            "SeleniumBase can download Chromium in advance:</mk-0>"
            "</p><hr /><br />\n"
            '<h3>✅ <mk-1><code>sbase get chromium</code></mk-1></h3>'
            '<img src="https://seleniumbase.io/other/sbase_get_chromium.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<mk-0>"
            "Unlike Google Chrome, unbranded Chromium still<br />"
            "supports loading extensions via command flags.</mk-0>"
            "<hr />\n"
            '<img src="https://seleniumbase.io/other/load_extension_flag.jpg"'
            ' width="78%">'
        )
        self.add_slide(
            "<mk-0>"
            "Additionally, unbranded Chromium may be stealthier<br />"
            "than regular Google Chrome on certain websites.</mk-0>"
            "<hr /><br /><br />\n"
            "<h3><mk-1>Get ready for a web-scraping<br />"
            "live demo on Reddit.com ...</mk-1></h3>"
            "<br /><br />"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/reddit_scraping.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<mk-0>reCAPTCHA comes in many flavors:</mk-0><br /><br />"
            '<img src="https://seleniumbase.io/other/recaptcha_v2a.png"'
            ' width="80%">'
            "<br /><br /><mk-1>Some flavors are stronger than others.</mk-1>"
        )
        self.add_slide(
            "<p>🔐 <b>Google reCAPTCHA</b> 🔐</p><hr />"
            '<img src="https://seleniumbase.io/other/g_recaptcha.png"'
            ' width="50%">'
            '<img src="https://seleniumbase.io/other/recaptcha_v2b.png"'
            ' width="50%">'
            "<br /><br />"
        )
        self.add_slide(
            "<p>🔐 <b>Google reCAPTCHA</b> 🔐</p><hr />"
            '<img src="https://seleniumbase.io/other/g_recaptcha.png"'
            ' width="50%"><br /><br />'
            "<p><mk-0>reCAPTCHA is very effective at catching bots.</mk-0></p>"
            "<br /><br /><br /><br /><br />"
        )
        self.add_slide(
            "<p>🔐 <b>Google reCAPTCHA</b> 🔐</p><hr />"
            '<img src="https://seleniumbase.io/other/g_recaptcha.png"'
            ' width="50%">'
            "<br /><br />"
            "<p><mk-0>Even though Google reCAPTCHA looks similar<br />"
            "to Cloudflare Turnstile, they are very different!</mk-0></p>"
            '<img src="https://seleniumbase.io/other/cf_turnstile.png"'
            ' width="50%">'
            "<br /><br />"
        )
        self.add_slide(
            "<mk-0>"
            "This may explain why Google reCAPTCHA is better:"
            "</mk-0><hr /><br />"
            "<p><mk-1>Since Google makes both reCAPTCHA and Chrome,"
            " reCAPTCHA has access to more data than other CAPTCHAs,"
            " and can therefore detect bots better."
            "</mk-1></p><br /><br />"
        )
        self.add_slide(
            "<mk-0>Many websites are using an out-of-date reCAPTCHA:</mk-0>"
            "<h5><br /></h5>"
            '<img src="https://seleniumbase.io/other/pokemon_recaptcha.jpg"'
            ' width="80%">'
            "<h5><br />"
            "<mk-1>(Sites like these are vulnerable to web-scrapers)</mk-1>"
            "</h5>"
        )
        self.add_slide(
            "<h3><mk-0>Get ready for a web-scraping<br />"
            "live demo on Pokemon.com ...</mk-0></h3>"
        )
        self.add_slide(
            "<p>🔐 <b>Google reCAPTCHA</b> 🔐</p><hr /><br />"
            "<mk-0>In the case of encountering an Enterprise V3<br />"
            "reCAPTCHA... that's a very different story...</mk-0>"
            "<br /><br /><br />"
            '<img src="https://seleniumbase.io/other/g_recaptcha.png"'
            ' width="50%">'
            "<br /><br />"
        )
        self.add_slide(
            "<p><mk-0>"
            "Note: Calling <code>open(url)</code> from UC Mode<br />"
            "automatically activates CDP Mode now.</mk-0>"
            "</p><hr /><ul>\n"
            "<mk-1>This change was made because the original<br />"
            "UC Mode wasn't stealthy enough anymore.</mk-1><br /><br />"
            "<mk-2>This makes older UC Mode scripts work again.<br /><br />"
            "</mk-2><mk-3>"
            "That's especially important since out-of-date<br />"
            "Undetectable Automation videos still get views.<br /><br />"
            "</mk-3><mk-4>"
            "<code>sb.driver.get(url)</code> keeps you in UC Mode.</mk-4>"
            "</ul>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_architecture.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<p><mk-0>"
            "Naming conventions used in the SeleniumBase repo:</mk-0>"
            "</p><hr /><br />\n"
            "<ul>"
            '<mk-1>✅ If a file starts with "<code>test_</code>" or ends with'
            '<br />"<code>_test.py</code>", '
            'then it runs with "<code>pytest</code>".</mk-1>'
            "<br /><br />"
            '<mk-2>✅ If a file starts with "<code>raw_</code>",<br />'
            'then it runs directly with raw "<code>python</code>".</mk-2>'
            "<br /><br />"
            '<mk-3>✅ (Note that SeleniumBase was originally just a test '
            'framework before it gained stealth abilities.)</mk-3>'
            "</ul>"
        )
        self.add_slide(
            "<p><mk-0>"
            "Finding stealthy examples in the SeleniumBase repo:</mk-0>"
            "</p><hr /><br />\n"
            '<mk-1>✅ See "<code>SeleniumBase/examples/cdp_mode/</code>"<br />'
            'for all examples made for stealth & CAPTCHAs.</mk-1><br /><br />'
            '<mk-2>✅ For the Stealthy Playwright Mode examples, see:<br />'
            '"<code>SeleniumBase/examples/cdp_mode/playwright/</code>"</mk-2>'
        )
        self.add_slide(
            "<p><mk-0>"
            "Let's make a quick trip to the SeleniumBase repo:</mk-0>"
            "</p><hr />\n"
            '<img src="https://seleniumbase.io/other/sbase_gh.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<mk-0>"
            "It's time for more CAPTCHA-bypass!</mk-0>"
            "<hr /><br />\n"
            "<b><mk-1>Get ready for a live demo of<br />"
            "bypassing a Cloudflare CAPTCHA<br />"
            "on Cloudflare's own login page ..."
            "</mk-1></b>"
            "<br /><br />"
            '<img src="https://seleniumbase.io/other/cf_bypass_3.png"'
            ' width="60%">'
        )
        self.add_slide(
            "<h5><mk-0>"
            "If bypassing CAPTCHAs isn't exciting enough for you,<br />"
            "then treat every CAPTCHA-bypass like scoring a goal...</mk-0>"
            "</h5>"
            '<img src="https://seleniumbase.io/other/robot_goal.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0>🤖 <b>You've reached the AI section of this video!</b> 🤖"
            "</mk-0></p><hr /><br />"
            '<img src="https://seleniumbase.io/other/three_ais.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0>🤖 <b>I've actually been using a lot of AI already!</b> 🤖"
            "</mk-0></p><hr /><br />"
            "<mk-1>✅ Many illustrations were AI-generated.</mk-1><br />"
            '<img src="https://seleniumbase.io/other/ai_workstation.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0>🤖 <b>Thanks for all the free artwork, Gemini!</b> 🤖"
            "</mk-0></p><hr />"
            '<img src="https://seleniumbase.io/other/yt_inspiration_tab.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0><b>Let's use Gemini's power to bypass CAPTCHAs!</b>"
            "</mk-0></p><hr /><br />"
            '<img src="https://seleniumbase.io/other/ai_shield_break.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0><b>Every year the AI models get better and better</b>"
            "</mk-0></p><hr /><br />"
            '<img src="https://seleniumbase.io/other/new_ai_model.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0><b>Definitely an improvement over last year's models</b>"
            "</mk-0></p><hr />"
            '<img src="https://seleniumbase.io/other/last_year_model.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<p><mk-0><b>I also covered AI in my earlier video:</b>"
            "<h5><mk-1>"
            'Can AI tools help you with web-scraping & CAPTCHA-bypass?'
            '</mk-1></h5>'
            "</mk-0></p><hr />"
            '<img src="https://seleniumbase.io/other/can_ai_tools_help.jpg"'
            ' width="68%"><hr />'
            "<h5><mk-2>"
            '(Spoiler alert: It depends on which AI you ask!)'
            '</mk-2></h5>'
        )
        self.add_slide(
            "<h3><mk-0><b>It's time for the next live demo!</b></mk-0></h3>"
            "<hr /><br /><br />"
            "<h3><mk-1>For that, we're scraping LinkedIn...</mk-1></h3>"
            '<img src="https://seleniumbase.io/other/linkedin_top.jpg"'
            ' width="70%">'
        )
        self.add_slide(
            "<h3><mk-0>As you can see ...</mk-0></h3>"
            "<hr /><br />"
            "<p><mk-1>SeleniumBase works well for web-scraping."
            "</mk-1></p>"
            '<img src="https://seleniumbase.io/cdn/img/nice_logo_8t3.png"'
            ' width="70%">'
        )
        self.add_slide(
            "<p><mk-0>"
            "If you need help creating scripts,<br />"
            "<b>just ask the AI! (maybe Gemini)</b></mk-0>"
            "</p><hr />\n"
            '<img src="https://seleniumbase.io/other/ai_dual_screen.jpg"'
            ' width="60%"><hr />'
            '<mk-1>✅ Or you can replicate a bunch of<br />'
            'AI agents to do the work for you...</mk-1><br />'
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
            '<img src="https://seleniumbase.io/other/sb_github_page2.jpg"'
            ' width="86%">'
        )
        self.begin_presentation(filename="uc_presentation.html")
