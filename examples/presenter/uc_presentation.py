import os
import subprocess
from contextlib import suppress
from seleniumbase import BaseCase
from seleniumbase import SB
BaseCase.main(__name__, __file__)


class UCPresentationClass(BaseCase):
    def test_presentation(self):
        self.open("data:,")
        self._output_file_saves = False
        self.create_presentation(theme="beige", transition="fade")
        self.add_slide(
            "<p>A deep dive into <b>undetectable automation</b>, with:</p>"
            "<h5><code>SeleniumBase UC Mode"
            " and undetected-chromedriver</code></h5>",
            image="https://seleniumbase.io/cdn/img/uc_mode_phases_3.png",
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/cdn/img/uc_mode_phases_3.png">'
        )
        self.add_slide(
            "<p>🔹 <b>The Objective</b> 🔹</p><hr /><br />"
            "<p><mk-0>By the end of this presentation, you'll learn how to"
            " create bots that appear as humans to websites.</mk-0></p><br />"
            "<p><mk-1>(These bots won't get detected or blocked.)</mk-1></p>"
            "<br /><p><mk-2>Here's a live demo of that...</mk-2></p>"
        )
        self.begin_presentation(filename="uc_presentation.html")

        self.get_new_driver(undetectable=True)
        url = "https://gitlab.com/users/sign_in"
        try:
            self.uc_open_with_reconnect(url, reconnect_time=3)
            try:
                self.assert_text("Username", '[for="user_login"]', timeout=3)
                self.post_message("SeleniumBase wasn't detected", duration=4)
            except Exception:
                self.uc_open_with_reconnect(url, reconnect_time=4)
                self.assert_text("Username", '[for="user_login"]', timeout=3)
                self.post_message("SeleniumBase wasn't detected", duration=4)
        finally:
            self.quit_extra_driver()

        if os.path.exists("multi_uc.py"):
            self.create_presentation(theme="beige", transition="fade")
            self.add_slide(
                "<p>🔹 <b>There's a lot more to come!</b> 🔹</p><hr /><br />"
                "<p><mk-0>If one bot isn't enough, how about several?</mk-0>"
                "</p><br /><br />"
                "<p><mk-1>Here's a demo of multithreaded bots in parallel..."
                "</mk-1></p>"
            )
            self.begin_presentation(filename="uc_presentation.html")
            subprocess.Popen("pytest multi_uc.py --uc -n3", shell=True).wait()
            self.create_presentation(theme="serif", transition="fade")
            self.add_slide(
                "<p>Not just an army of bots, but an army of bots<br />"
                "that look just like humans using web browsers.</p><br />"
                "<p>(That's how they weren't detected!)</p>"
            )
            self.begin_presentation(filename="uc_presentation.html")

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "If this is what you came here for, stick around<br />to"
            " learn how to do the things you just saw.<br />"
            "<p>You may find it easier to build a Selenium<br />"
            "bot than to navigate an obstacle course.</p>",
            image="https://seleniumbase.io/other/yeah_you_passed.png",
        )
        self.add_slide(
            "<p>But first, you may be wondering who I am...</p>"
            "<p>Or maybe you're one of over one million people<br />"
            "that I've already helped on Stack Overview:</p>"
            '<img src="https://seleniumbase.io/other/me_st_overflow.jpg" '
            'width="80%">'
        )
        self.add_slide(
            "<p><b>About the presenter (Michael Mintz):</b></p>\n"
            "<ul>\n"
            "<li>I created <b>SeleniumBase</b> (for Python).</li>\n"
            "<li>I lead the Automation Team at <b>iboss</b>.</li>\n"
            "</ul>\n",
            image="https://seleniumbase.io/other/iboss_booth.png",
        )
        self.add_slide(
            "<p>I've been doing video podcasts since 2012!</p>"
            "<p>(That's when I first co-hosted the<br />Marketing Update"
            " on HubSpot TV)</p>",
            image="https://seleniumbase.io/other/hub_tv.png",
        )
        self.add_slide(
            "<p>I spoke at Selenium Conference 2023:</p>"
            "<p>(As the dedicated Python Selenium speaker)</p>",
            image="https://seleniumbase.io/other/me_se_conf.jpg",
        )
        self.add_slide(
            "<p>Here's me with the creators<br />"
            "of <b>Selenium</b> / <b>WebDriver</b>:</p>",
            image="https://seleniumbase.io/other/selenium_builders.jpg",
        )
        self.add_slide(
            "<b>SeleniumBase</b> Fun Fact:"
            "<div />The 1st SB GitHub issue was from a Tesla engineer:",
            image="https://seleniumbase.io/other/first_issue.png",
        )
        self.add_slide(
            "<p>Now, let me explain how we got here...</p>"
            "<p>And by here, I mean a time when lots of companies"
            " have been building services to detect and block bots:</p>",
            image="https://seleniumbase.io/other/verify_human.png",
        )
        self.add_slide(
            "<p>In the early days, there were few bots,<br />"
            "and those bots didn't look human at all.</p><br />"
            "<p>Those early bots were mostly innocent, and<br />"
            "most websites didn't care if they were around.</p>"
        )
        self.add_slide(
            "<p>At some point, the number of bots grew by a lot...</p><br />"
            "<p>Many bots were programmed with bad intentions...</p><br />"
            "<p>And sometimes you couldn't tell apart the good bots"
            " from the bad ones until it was already too late...</p>",
        )
        self.add_slide(
            "<p>Then came Google <b>reCAPTCHA v1</b>...</p>"
            "<p>Although intended as a defense against bots,<br />"
            " humans on a web browser also got hit by it.</p>",
            image="https://seleniumbase.io/other/recaptcha_v1.png",
        )
        self.add_slide(
            "<p>Then Google made improvements:</p>"
            "<p>(<b>reCAPTCHA v2</b> / <b>reCAPTCHA v3</b>)</p>",
            image="https://seleniumbase.io/other/recaptcha_v2a.png",
        )
        self.add_slide(
            "<p>And that annoyed a lot of people...</p>",
            image="https://seleniumbase.io/other/recaptcha_v2b.png",
        )
        self.add_slide(
            "<p>Then came the next iteration of anti-bot security:</p>"
            "<p>Cloudflare <b>Turnstile</b> CAPTCHA-replacement."
            "<p>That changed the game in many ways.</p>",
            image="https://seleniumbase.io/other/check_if_secure.png",
        )
        self.add_slide(
            "For awhile, Cloudflare's Turnstile did a decent<br />"
            "job filtering out bot traffic from human traffic."
            "<p>Then <code>undetected-chromedriver</code> arrived:</p>",
            image="https://seleniumbase.io/other/undetected_ch.png",
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/undetected_ch.png" '
            'width="90%">'
        )
        self.add_slide(
            "<p><code>undetected-chromedriver</code> was found to be<br />"
            "incredibly effective at getting past the Turnstile:</p>",
            image="https://seleniumbase.io/other/connection_secure.png",
        )
        self.add_slide(
            "<p>The maintainer of <code>undetected-chromedriver</code>:</p>"
            "<hr /><p>He appears to be very busy with various projects.</p>"
            '<img src="https://seleniumbase.io/other/the_uc_starter.png" '
            'width="80%">'
        )
        self.add_slide(
            "<p>The biggest challenge for undetected-chromedriver"
            " has been adapting to breaking changes caused by:</p><div />"
            "<ul>\n"
            "<li>New versions of Chrome.</li>\n"
            "<li>New versions of Selenium.</li>\n"
            "<li>New versions of Cloudflare.</li>\n"
            "</ul><br /><hr />\n"
            "<p>Those can brake things until updates are released:</p>"
            '<img src="https://seleniumbase.io/other/uc_open_issues.png" '
            'width="80%">'
        )
        self.add_slide(
            "<p>Thankfully, <code>undetected-chromedriver</code> has<br />"
            "supporters helping to figure out and fix things.<p>"
            '<img src="https://seleniumbase.io/other/uc_helping_out.png" '
            'width="70%">'
        )
        self.add_slide(
            "<h4>Sometimes all that help isn't enough...</h4>"
            "<p>That's where <code>seleniumbase</code> UC Mode comes in:</p>"
            '<img src="https://seleniumbase.io/other/sb_github.png" '
            'width="70%">'
        )
        self.add_slide(
            "<h4>SeleniumBase <b>UC Mode</b> is a modified fork of<br />"
            "undetected-chromedriver with multiple changes.</h4>"
            "<h4>UC Mode includes bug fixes and additional features, such as"
            " multithreading support via <code>pytest-xdist</code>.</h4>"
            '<img src="https://seleniumbase.io/other/super_server.jpg" '
            'width="60%">'
        )
        self.add_slide(
            "<h4><mk-0><b>UC Mode</b> is one of many SeleniumBase modes:"
            "</mk-0></h4>\n<ul>\n"
            "<li><mk-1>UC Mode</mk-1> (<code>--uc / uc=True</code>)</li>\n"
            "<li><mk-2>Slow Mode</mk-2> (<code>--slow</code>)</li>\n"
            "<li><mk-3>Demo Mode</mk-3> (<code>--demo</code>)</li>\n"
            '<li><mk-4>Proxy Mode</mk-4>'
            ' (<code>--proxy="h:p"/"u:p@h:p"</code>)</li>\n'
            "<li><mk-5>Debug Mode</mk-5> "
            "(<code>--pdb/--trace/--ftrace</code>)</li>\n"
            "<li><mk-6>Mobile Mode</mk-6> "
            "(<code>--mobile / mobile=True)</code></li>\n"
            "<li><mk-7>Recorder Mode</mk-7> "
            "(<code>--rec / --rec-behave</code>)</li>\n"
            "<li><mk-8>Multithreaded Mode</mk-8> "
            "(<code>pytest -n4 / -n8</code>)</li>\n"
            "</ul>\n"
            "<p><mk-9>And more! (You can even combine modes!)</mk-9></p>\n"
        )
        self.add_slide(
            "<p><mk-0>ℹ️: UC Mode is not enabled by default.<br />"
            " It must be activated by switching it on:</mk-0></p>"
            "<ul>\n"
            "<li><code><mk-1>--uc</mk-1></code> &nbsp"
            " (pytest command-line option)</li>\n"
            "<li><code><mk-2>uc=True</mk-2></code> &nbsp"
            " (SB/driver manager formats)</li>\n"
            "</ul><br /><br /><hr /><br />\n<p>"
            "<mk-3>Then websites can no longer detect chromedriver.</mk-3></p>"
        )
        self.add_slide(
            "<p><mk-0>Here's an example script that uses UC Mode:</mk-0></p>\n"
            "<h5><mk-1>(Note that SeleniumBase has <code>driver</code> methods"
            "<br />that aren't included with standard Selenium.)</mk-1></h5>\n"
            "<hr /><br />\n",
            code=(
                "<mk-2>from seleniumbase import Driver</mk-2>\n\n"
                "<mk-3>driver = Driver(uc=True)</mk-3>\n"
                "<mk-4>try:</mk-4>\n"
                '    <mk-5>driver.get("https://gitlab.com/users/sign_in")'
                '</mk-5>\n'
                "    <mk-1><mk-6>driver.sleep(4)</mk-6></mk-1>\n"
                "    <mk-7># DO MORE STUFF</mk-7>\n"
                "<mk-4>finally:</mk-4>\n"
                "    <mk-4>driver.quit()</mk-4>\n"
            ),
        )
        self.add_slide(
            "<p><mk-0>For reference, here's a script in a different<br />"
            "SeleniumBase format, with more methods:</mk-0></p>"
            "<h5><mk-12>(Get ready for another live demo...)</mk-12></h5>",
            code=(
                "<mk-1>from seleniumbase import SB</mk-1>\n\n"
                "<mk-2>with SB(uc=True) as sb:</mk-2>\n"
                '    <mk-3>sb.get("seleniumbase.io/simple/login")</mk-3>\n'
                '    <mk-4>sb.type("#username", "demo_user")</mk-4>\n'
                '    <mk-5>sb.type("#password", "secret_pass")</mk-5>\n'
                '    <mk-6>sb.click(\'a:contains("Sign in")\')</mk-6>\n'
                '    <mk-7>sb.assert_exact_text("Welcome!", "h1")</mk-7>\n'
                '    <mk-8>sb.assert_element("img#image1")</mk-8>\n'
                '    <mk-9>sb.highlight("#image1")</mk-9>\n'
                '    <mk-10>sb.click_link("Sign out")</mk-10>\n'
                '    <mk-11>sb.assert_text("signed out", "#top_message")'
                "</mk-11>\n"
            ),
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True) as sb:
                sb.get("https://seleniumbase.io/simple/login")
                sb.type("#username", "demo_user")
                sb.type("#password", "secret_pass")
                sb.click('a:contains("Sign in")')
                sb.assert_exact_text("Welcome!", "h1")
                sb.assert_element("img#image1")
                sb.highlight("#image1")
                sb.click_link("Sign out")
                sb.assert_text("signed out", "#top_message")

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<h3><mk-0>Was that too fast for you?</mk-0></h3>"
            "<h4><mk-1>Let's run that again in <b>Demo Mode</b>:</mk-1></h4>",
            code=(
                "from seleniumbase import SB\n\n"
                "with SB(uc=True<mk-1>, demo=True</mk-1>) as sb:\n"
                '    sb.get('
                '"https://seleniumbase.io/simple/login")\n'
                '    sb.type("#username", "demo_user")\n'
                '    sb.type("#password", "secret_pass")\n'
                '    sb.click(\'a:contains("Sign in")\')\n'
                '    sb.assert_exact_text("Welcome!", "h1")\n'
                '    sb.assert_element("img#image1")\n'
                '    sb.highlight("#image1")\n'
                '    sb.click_link("Sign out")\n'
                '    sb.assert_text("signed out", "#top_message")\n'
            ),
        )
        self.begin_presentation(filename="uc_presentation.html")

        with suppress(Exception):
            with SB(uc=True, demo=True) as sb:
                sb.get("https://seleniumbase.io/simple/login")
                sb.type("#username", "demo_user")
                sb.type("#password", "secret_pass")
                sb.click('a:contains("Sign in")')
                sb.assert_exact_text("Welcome!", "h1")
                sb.assert_element("img#image1")
                sb.highlight("#image1")
                sb.click_link("Sign out")
                sb.assert_text("signed out", "#top_message")

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<p><mk-0>Note the differences between undetected-chromedriver and"
            " SeleniumBase UC Mode.</mk-0><br /><hr />SeleniumBase UC Mode:"
            "</p><ul>\n"
            "<li><mk-1>Has driver version-detection & management.</mk-1>"
            "</li>\n"
            "<li><mk-2>Allows mismatched browser/driver versions.</mk-2>"
            "</li>\n"
            "<li><mk-3>Changes the user agent to prevent detection.</mk-3>"
            "</li>\n"
            "<li><mk-4>Hides chromedriver from Chrome as needed.</mk-4>"
            "</li>\n"
            "<li><mk-5>Allows for multithreaded tests in parallel.</mk-5>"
            "</li>\n"
            "<li><mk-6>Adjusts configuration based on the environment.</mk-6>"
            "</li>\n"
            "<li><mk-7>Has options for proxy and proxy-with-auth.</mk-7>"
            "</li>\n</ul>\n"
        )
        self.add_slide(
            "<h3><mk-0>Here's another UC Mode script:</mk-0></h3>"
            "<h4><mk-1>(Get ready for another live demo...)</mk-1></h4>"
            "<hr /><br />",
            code=(
                "from seleniumbase import SB\n\n"
                "with SB(uc=True) as sb:\n"
                '    url = "https://gitlab.com/users/sign_in"\n'
                "    sb.uc_open_with_reconnect(url, 4)\n\n"
                "    ...\n"
            ),
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

        self.create_presentation(theme="serif", transition="fade")
        self.add_slide(
            "<p>Now let's learn how UC Mode works in general.</p>"
            "<p>First, there are several things that need to happen for"
            " browsers to remain undetected from anti-bot services.</p>\n",
            image="https://seleniumbase.io/other/yeah_you_passed.png",
        )
        self.add_slide(
            "<mk-0>Requirements for avoiding detection</mk-0> (UC Mode)<hr />"
            "<ul>\n"
            "<li><mk-1>Modify chromedriver to rename driver variables"
            " that appear in the Chrome DevTools console.</mk-1></li>\n"
            "<li><mk-2>Launch Chrome before attaching chromedriver.<br />"
            "(Don't launch Chrome with chromedriver)</mk-2></li>\n"
            "<li><mk-3>Don't use Selenium-specific Chrome options.</mk-3>"
            "</li>\n<li><mk-4>If using headless Chrome, change"
            " HeadlessChrome to Chrome in the User Agent.</mk-4></li>\n"
            "<li><mk-5>If using a custom user_data_dir, don't let that"
            " folder be used with non-UC-Mode Chrome.</mk-5></li>\n"
            "<li><mk-6>Disconnect chromedriver briefly from Chrome before"
            " loading websites with detection services.</mk-6></li>\n"
            "</ul>"
        )
        self.add_slide(
            "Requirements, continued... / <b>Good news:</b><hr />\n"
            "<h3><mk-0>Most of those things are already done automatically"
            " when using UC Mode with default settings.</mk-0></h3>\n"
            "<h4><mk-1>The part that's your responsibility, (if setting a"
            " custom <code>user_data_dir</code>), is making sure that"
            " the u_d_d is only used by UC Mode Chrome instances. If you"
            ' "cross the streams", UC Mode can be detected.</mk-1></h4><div />'
            "<h4><mk-2>(UC Mode takes care of the other requirements.)</mk-2>"
            "</h4>"
        )
        self.add_slide(
            "<h4>With those things done, your bot can appear human.</h4>\n"
            "<h5>But if anyone looks too closely at what your bot does,<br />"
            'it may raise suspicion, even if already marked "not a bot".</h5>',
            image="https://seleniumbase.io/other/other_anti_bots.jpg",
        )
        self.add_slide(
            "<h4><mk-0>There are additional methods that you can use"
            " to have a better experience when using UC Mode:</mk-0></h4>\n"
            "<h6><br /><mk-1>Note that <code><b>driver.get(url)</b></code> has"
            " been modified from the original to<br />reconnect automatically"
            " if a web page is using bot-detection software.</mk-1></h6>"
            "<hr /><br />",
            code=(
                "driver.default_get(url)\n\n"
                "driver.uc_open(url)\n\n"
                "driver.uc_open_with_tab(url)\n\n"
                "driver.uc_open_with_reconnect(url, reconnect_time)\n\n"
                'driver.uc_click(selector, by="css selector", timeout=7)\n'
            ),
        )
        self.add_slide(
            "<h4>There are additional methods that you can use"
            " to have a better experience when using UC Mode:</h4>"
            "<h6><br /><mark>Since <code><b>driver.get(url)</b></code> has"
            " been modified, <code><b>driver.default_get(url)</b></code>"
            " exists to do a regular <code><b>get(url)</b></code>,"
            " which may be useful if revisiting a website.</mark></h6>"
            "<hr /><br />",
            code=(
                "<mark>driver.default_get(url)</mark>\n\n"
                "driver.uc_open(url)\n\n"
                "driver.uc_open_with_tab(url)\n\n"
                "driver.uc_open_with_reconnect(url, reconnect_time)\n\n"
                'driver.uc_click(selector, by="css selector", timeout=7)\n'
            ),
        )
        self.add_slide(
            "<h4>There are additional methods that you can use"
            " to have a better experience when using UC Mode:</h4>"
            "<h6><br /><mark><code><b>driver.uc_open(url)</b></code> will"
            " open a URL in the same tab with a disconnect.<br />"
            "(This might not be enough to bypass detection.)</mark></h6>"
            "<hr /><br />",
            code=(
                "driver.default_get(url)\n\n"
                "<mark>driver.uc_open(url)</mark>\n\n"
                "driver.uc_open_with_tab(url)\n\n"
                "driver.uc_open_with_reconnect(url, reconnect_time)\n\n"
                'driver.uc_click(selector, by="css selector", timeout=7)\n'
            ),
        )
        self.add_slide(
            "<h4>There are additional methods that you can use"
            " to have a better experience when using UC Mode:</h4>\n"
            "<h6><br /><mark><code><b>driver.uc_open_with_tab(url)</b></code>"
            " opens a URL in a new tab with a disconnect. Similar to the new"
            " <code><b>driver.get(url)</b></code>, but without the pre-check."
            "</mark></h6><hr /><br />",
            code=(
                "driver.default_get(url)\n\n"
                "driver.uc_open(url)\n\n"
                "<mark>driver.uc_open_with_tab(url)</mark>\n\n"
                "driver.uc_open_with_reconnect(url, reconnect_time)\n\n"
                'driver.uc_click(selector, by="css selector", timeout=7)\n'
            ),
        )
        self.add_slide(
            "<h4>There are additional methods that you can use"
            " to have a better experience when using UC Mode:</h4>\n"
            "<h6><br /><code><b>driver.uc_open_with_tab(url)</b></code> opens"
            " a URL in a new tab with a disconnect. Similar to the new"
            " <code><b>driver.get(url)</b></code>, but without the pre-check."
            "</h6><hr /><br />\n"
            "<h6><mark>As a reminder, the <code><b>driver.get(url)</b></code>"
            " pre-check checks to see if a URL has bot-detection software"
            " on it before opening the URL in a new tab with a disconnect."
            "</mark><br /></h6><div /><div />\n"
            "<h6><mark>This pre-check is done using"
            " <code><b>requests.get(URL)</b></code><br />before opening"
            " a URL in the <code>UC Mode</code> web browser.</mark></h6>"
            "<h5><mark>If the response code is a"
            ' <code><b>"403"</b></code> (Forbidden),<br />'
            "then the URL is opened with a <code>disconnect</code>."
            "</mark></h5>"
        )
        self.add_slide(
            "<h4><b>Customizing the default disconnect/reconnect time</b></h4>"
            "<hr />\n"
            "<p>Here's a method for a custom reconnect time<br />"
            "when opening a page that tries to detect bots:</p>"
            "<pre><mk-0>driver.uc_open_with_reconnect(url, reconnect_time)"
            "</mk-0></pre>"
            "<h6>(The default reconnect_time is slightly more than 2 seconds.)"
            "</h6><hr /><br />",
            code=(
                "# Example:\n"
                "<mk-1>driver.uc_open_with_reconnect(\n"
                '    "https://steamdb.info/login/", reconnect_time=6\n)'
                "</mk-1>"
                "\n\n"
                "# Short form example:\n"
                "<mk-2>driver.uc_open_with_reconnect("
                '"https://steamdb.info/login/", 6)</mk-2>\n'
            ),
        )
        self.add_slide(
            "<h4><b>Clicking with a disconnect/reconnect</b></h4><hr />\n"
            "<p>If your bot needs to click a button on a website that has"
            " anti-bot services, you might be able to do it with this special"
            " method, which forces a short disconnect:</p>\n"
            "<pre><mk-0>driver.uc_click(selector)</mk-0></pre>"
            '<h6>(Defaults: <code>by="css selector", timeout=7</code>)</h6>'
            "<hr /><br />\n",
            code=(
                "# Examples:\n"
                '<mk-1>driver.uc_click("button")\n\n'
                'driver.uc_click("button#id", timeout=10)</mk-1>\n'
            ),
        )
        self.add_slide(
            "<h2>Links to UC Mode code</h2><hr /><br /><ul>\n"
            '<li><a href="https://github.com/seleniumbase/SeleniumBase'
            '/blob/master/examples/verify_undetected.py" target="_blank">'
            'SeleniumBase/examples/verify_undetected.py</a></li><br />\n'
            '<li><a href="https://github.com/seleniumbase/SeleniumBase'
            '/blob/master/examples/uc_cdp_events.py" target="_blank">'
            'SeleniumBase/examples/uc_cdp_events.py</a></li><br />\n'
            '<li><a href="https://github.com/seleniumbase/SeleniumBase'
            '/blob/master/examples/raw_uc_mode.py" target="_blank">'
            'SeleniumBase/examples/raw_uc_mode.py</a></li>'
            "<br />\n</ul>\n",
        )
        self.add_slide(
            "<h2>Things to keep in mind</h2><hr /><ul>\n"
            "<li>You may need to adjust default settings<br />"
            "for your bot to remain undetected.</li><br />\n"
            "<li>Once your bot enters a website,<br />"
            "it should continue to act accordingly.</li><br />\n"
            "<li>Improvise if your bot makes any mistakes.</li><br />\n"
            "<li>Your bot should look human to avoid detection.</li></ul>\n",
        )
        self.add_slide(
            "<h2>Ethical concerns</h2><hr /><ul>\n"
            "<li>Don't use bots for evil purposes.</li><br />\n"
            "<li>Do use bots with honorable intentions.</li><br />\n"
            "<li>Do use bots for automating tedious manual tasks.</li><br />\n"
            "<li>Do take the time to train & configure your bots.</li></ul>\n",
        )
        self.add_slide(
            "<h2>🔹 Final remarks 🔹</h2><div /><hr /><h4><br /><ul>\n"
            "<li>Not all bots are created equal.</li><br />\n"
            "<li>SeleniumBase UC Mode lets bots appear human.</li><br />\n"
            "<li>Visit SeleniumBase on GitHub for more info:\n"
            "https://github.com/seleniumbase/SeleniumBase</li></ul></h4>\n",
        )
        self.add_slide(
            "<h3>❓ Questions? ❓</h3>"
            "<h5>https://github.com/seleniumbase/SeleniumBase/discussions</h5>"
            "<br /><h3>📌 Found a bug? 🐞</h3><h5>"
            "https://github.com/seleniumbase/SeleniumBase/issues</h5><hr />"
            "<br /><h4>🔰 Perfection takes practice. Keep iterating! 🔰</h4>"
        )
        self.add_slide(
            "<h1>The End</h1>",
            image="https://seleniumbase.io/other/sb_github.png"
        )
        self.begin_presentation(filename="uc_presentation.html")
