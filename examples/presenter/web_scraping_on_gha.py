from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class UCPresentationClass(BaseCase):
    def test_hacking_with_cdp(self):
        self.open("data:,")
        self.set_window_position(4, 40)
        self._output_file_saves = False
        self.create_presentation(theme="serif", transition="none")
        self.add_slide("<h2>Press SPACE to begin!</h2>\n")
        self.add_slide(
            "<p><b><mk-0>Coming up... on the Hacker Show:</mk-0></b></p>\n"
            "<hr /><ul>\n"
            '<img src="https://seleniumbase.io/other/robot_ai.jpg"'
            ' width="92%"></ul>\n'
            "<br /><br />\n"
            "<br /><br />\n",
        )
        self.add_slide(
            "<p><b>Coming up... on the Hacker Show:</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li><mk-0>Unlimited free web-scraping w/ GitHub Actions&nbsp\n"
            "</mk-0></li>\n"
            "</ul>"
            '<img src="https://seleniumbase.io/other/gha_scraping.jpg"'
            ' width="82%">',
        )
        self.add_slide(
            "<p><b>Coming up... on the Hacker Show:</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Unlimited free web-scraping w/ GitHub Actions&nbsp"
            "</li><br />\n"
            "<li><mk-0>Using GitHub Secrets to hide within open-source"
            "</mk-0></li></ul>\n"
            '<img src="https://seleniumbase.io/other/gh_secret.png"'
            ' width="80%">\n'
            "<br /><br />\n"
            "<br /><br />\n",
        )
        self.add_slide(
            "<p><b>Coming up... on the Hacker Show:</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Unlimited free web-scraping w/ GitHub Actions&nbsp"
            "</li><br />\n"
            "<li>Using GitHub Secrets to hide within open-source"
            "</li><br />\n"
            "<li><mk-0>Launching your own, free, local proxy server"
            "</mk-0></li></ul>\n"
            '<img src="https://seleniumbase.io/other/sbase_proxy.png"'
            ' width="80%">'
            "<br /><br />\n"
        )
        self.add_slide(
            "<p><b>Coming up... on the Hacker Show:</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Unlimited free web-scraping w/ GitHub Actions&nbsp"
            "</li><br />\n"
            "<li>Using GitHub Secrets to hide within open-source"
            "</li><br />\n"
            "<li>Launching your own, free, local proxy server"
            "</li><br />\n"
            '<li><mk-0>Using "iptables" to make a proxy server public'
            "</mk-0></li></ul>\n"
            '<img src="https://seleniumbase.io/other/tiny_iptables.png"'
            ' width="80%">'
            "<br /><br />\n",
        )
        self.add_slide(
            "<p><b>Coming up... on the Hacker Show:</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Unlimited free web-scraping w/ GitHub Actions&nbsp"
            "</li><br />\n"
            "<li>Using GitHub Secrets to hide within open-source"
            "</li><br />\n"
            "<li>Launching your own, free, local proxy server"
            "</li><br />\n"
            '<li>Using "iptables" to make a proxy server public'
            "</li><br />\n"
            "<li><mk-0>And multiple live demos after the previews"
            "</mk-0></li><br />\n"
            "</ul>",
        )
        self.add_slide(
            "<p><b>Get ready for some serious hacking!</b></p>"
            '<img src="https://seleniumbase.io/other/hackers_at_comp.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/web_scraping.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<p><mk-0>And YES, that means bypassing bot-detection!</mk-0>"
            '<img src="https://seleniumbase.io/other/bypassable_anti_bots.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<p><b>But first, a little bit about me...</b></p>"
            '<img src="https://seleniumbase.io/other/mintz_present.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><b>About me: (Michael Mintz)</b></p>\n"
            "<ul>\n"
            "<li>I created the <b>SeleniumBase</b> framework."
            "</li>\n"
            "<li>And I lead the Automation Team at <b>iboss</b>."
            "</li>\n"
            "</ul>"
            '<img src="https://seleniumbase.io/other/iboss_me_2.jpg"'
            ' width="60%">'
        )
        self.add_slide(
            "<p><b>Fun Fact</b></p><hr />\n"
            "<p>I once showed SeleniumBase to Sam Altman at MIT.<br />"
            "(Sam Altman cofounded OpenAI with Elon Musk.)"
            '<img src="https://seleniumbase.io/other/with_altman.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<p><b>Recently, SeleniumBase was trending on GitHub:"
            "</b></p>\n"
            '<img src="https://seleniumbase.io/other/trending_2025.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<p>The recent popularity can be attributed to <b>CDP Mode</b>,"
            "<br />which provides advanced stealth during automation.</p>"
            '<img src="https://seleniumbase.io/other/cdp_in_sb.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<p>That stealth is enough to bypass bot-detection<br />"
            "while web-scraping from <b>GitHub Actions</b>:</p>"
            '<img src="https://seleniumbase.io/other/gha_scraping.jpg"'
            ' width="90%">'
        )
        self.add_slide(
            "<p><b>GitHub Actions</b> is free for public repositories:</p>"
            '<img src="https://seleniumbase.io/other/gha_info.png"'
            ' width="90%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/gha_is_free.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<p>To hide sensitive information while using"
            "<br />GitHub Actions for open-source projects,"
            "<br />there's a feature called: <b>GitHub Secrets</b>.</p>"
            "<br />"
            "<p>That removes the limitation"
            r"<br />of being 100% open-source,"
            r"<br />while still being 100% free.</p>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/using_secrets_in_gha.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<img '
            'src="https://seleniumbase.io/other/limits_for_gh_secrets.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/creating_gh_secrets.jpg"'
            ' width="80%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/gh_secrets_in_wf.png"'
            ' width="88%">'
        )
        self.add_slide(
            '<img '
            'src="https://seleniumbase.io/other/using_gh_secrets_in_py.png"'
            ' width="88%">'
        )
        self.add_slide(
            "<h3>And that's the secret<br />to <b>GitHub Secrets!</b></h3>"
        )
        self.add_slide(
            "<h3>Up next:</h3>"
            "<br />"
            "<h2>Instant proxy server</h2>"
            "<br />"
            "<p>(Faster to launch than making Instant Coffee!)"
        )
        self.add_slide(
            '<h2><code>"sbase proxy"</code></h2>'
            "<br />"
            "<h3>(That's it!)</h3>"
            "<br />"
            '<img src="https://seleniumbase.io/other/sbase_proxy.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<p>More configuration options for "<b>sbase proxy</b>":</p>'
            '<img src="https://seleniumbase.io/other/instant_proxy.png"'
            ' width="80%">'
        )
        self.add_slide(
            "<p>The proxy server code comes from <b>proxy.py</b>:</p>"
            '<img src="https://seleniumbase.io/other/proxy_dot_py.png"'
            ' width="80%">'
        )
        self.add_slide(
            "<p><mk-0>"
            "Here's how to configure a proxy with <b>SeleniumBase</b>:</mk-0>"
            "</p><hr /><br /><ul>\n"
            '<li><mk-1>Proxy Mode via <code><b>pytest</b></code>:</mk-1>'
            '<br /><code>pytest --proxy="host:port"</code>'
            '<br /><code>pytest --proxy="user:pass@host:port"</code>'
            '</li><br />\n'
            '<li><mk-2>Proxy Mode via <code><b>SB()</b></code> manager:</mk-2>'
            '<br /><code>SB(proxy="host:port")</code>'
            '<br /><code>SB(proxy="user:pass@host:port")</code>'
            '</li>\n'
        )
        self.add_slide(
            "<h3>That's the secret to<br />instant proxy servers!</h3>"
            "<br /><p>(And how to use them with SeleniumBase)</p>"
        )
        self.add_slide(
            "<h3>How about opening up a"
            "<br />proxy server to the world?</h3><br />"
        )
        self.add_slide(
            "<h2>For that, there's <b>iptables</b></h2><br />"
            '<img src="https://seleniumbase.io/other/iptables_info.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/iptables_guide.png"'
            ' width="100%">'
        )
        self.add_slide(
            "<h3>And that's the secret to<br />making a server public!</h3>"
            '<img src="https://seleniumbase.io/other/super_server.jpg"'
            ' width="66%">'
        )
        self.add_slide(
            "<h3>Let's move on to<br />some live demos</h3>"
            '<img src="https://seleniumbase.io/other/hackers_at_comp.jpg"'
            ' width="70%">'
        )
        self.begin_presentation(filename="uc_presentation.html")
