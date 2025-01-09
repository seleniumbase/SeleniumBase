# https://www.youtube.com/watch?v=vt2zsdiNh3U
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
            "<p><h3><mk-0>Coming up on the Hacker Show...</mk-0></h3></p>\n"
            "<hr /><ul>\n"
            '<img src="https://seleniumbase.io/other/hackers_at_comp.jpg"'
            ' width="100%">'
            "</ul>",
        )
        self.add_slide(
            "<p><b>Coming up on the Hacker Show...</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li><mk-0>Intercepting requests/responses/XHR with CDP."
            "</mk-0></li><br />\n"
            "<br /><br />\n"
            "<br /><br />\n"
            "<br /><br />\n"
            "<br /><br />\n"
            "</ul>",
        )
        self.add_slide(
            "<p><b>Coming up on the Hacker Show...</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Intercepting requests/responses/XHR with CDP."
            "</li><br />\n"
            "<li><mk-0>Modifying requests: CDP.Fetch.continueRequest."
            "</mk-0></li><br />\n"
            "<br /><br />\n"
            "<br /><br />\n"
            "<br /><br />\n"
            "</ul>",
        )
        self.add_slide(
            "<p><b>Coming up on the Hacker Show...</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Intercepting requests/responses/XHR with CDP."
            "</li><br />\n"
            "<li>Modifying requests: CDP.Fetch.continueRequest."
            "</li><br />\n"
            "<li><mk-0>Controlling browsers via remote-debugging-port"
            "</mk-0></li><br />\n"
            "<br /><br />\n"
            "<br /><br />\n"
            "</ul>",
        )
        self.add_slide(
            "<p><b>Coming up on the Hacker Show...</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Intercepting requests/responses/XHR with CDP."
            "</li><br />\n"
            "<li>Modifying requests: CDP.Fetch.continueRequest."
            "</li><br />\n"
            "<li>Controlling browsers via remote-debugging-port"
            "</li><br />\n"
            "<li><mk-0>Bypassing CAPTCHAs & anti-bot defenses."
            "</mk-0></li><br />\n"
            "<br /><br />\n"
            "</ul>",
        )
        self.add_slide(
            "<p><b>Coming up on the Hacker Show...</b></p>\n"
            "<hr /><br /><ul>\n"
            "<li>Intercepting requests/responses/XHR with CDP."
            "</li><br />\n"
            "<li>Modifying requests: CDP.Fetch.continueRequest."
            "</li><br />\n"
            "<li>Controlling browsers via remote-debugging-port"
            "</li><br />\n"
            "<li>Bypassing CAPTCHAs & anti-bot defenses."
            "</li><br />\n"
            "<li><mk-0>And live demos of all the above... with Python!"
            "</mk-0></li><br />\n"
            "</ul>",
        )
        self.add_slide(
            "<h2>Get ready for some<br />serious hacking!</h2>"
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/hacking_with_cdp.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/cdp.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/ms_edp.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/vid4_on_yt.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/cdp_in_sb.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/hacker_news.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/sb_star_history_3.png"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/top_trending_month.png"'
            ' width="100%">'
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
            '<img src="https://seleniumbase.io/other/sb_con_req.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<img src="https://seleniumbase.io/other/xhr_info.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            '<h3>The <code>remote-debugging-port</code></h3>'
            '<img src="https://seleniumbase.io/other/rd_port.jpg"'
            ' width="100%">'
        )
        self.add_slide(
            "<h3>Let's get to the fun part...</h3>"
            '<img src="https://seleniumbase.io/other/hackers_at_comp.jpg"'
            ' width="80%">'
        )
        self.begin_presentation(filename="uc_presentation.html")
