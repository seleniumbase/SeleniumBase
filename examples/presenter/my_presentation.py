from seleniumbase import BaseCase


class MyPresenterClass(BaseCase):

    def test_presenter(self):
        self.create_presentation()
        self.add_slide(
            "<h2>Welcome!</h2>"
            "<h4>Enjoy the Presentation!</h4>")
        self.add_slide(
            '<h3>SeleniumBase "Presenter"</h3>'
            '<img src="https://seleniumbase.io/img/logo3a.png"></img>'
            '<h4>A tool for creating presentations</h4>')
        self.add_slide(
            '<h3>You can add HTML to any slide:</h3><br />'
            '<table style="padding:10px;border:4px solid black;font-size:60;">'
            '<tr><th>Row 1</th><th>Row 2</th></tr>'
            '<tr><td>Value 1</td><td>Value 2</td></tr></table><br />'
            '<h4>(HTML table example)</h4>')
        self.add_slide(
            "<h3>You can display code:</h3>",
            code=(
                'from seleniumbase import BaseCase\n\n'
                'class MyTestClass(BaseCase):\n\n'
                '    def test_basic(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'
                '        self.assert_text("xkcd: volume 0", "h3")\n'
                '        self.open("https://xkcd.com/353/")\n'
                '        self.assert_title("xkcd: Python")\n'
                '        self.assert_element(\'img[alt="Python"]\')\n'
                '        self.click(\'a[rel="license"]\')\n'
                '        self.assert_text("free to copy and reuse")\n'
                '        self.go_back()\n'
                '        self.click_link_text("About")\n'
                '        self.assert_exact_text("xkcd.com", "h2")\n'))
        self.add_slide(
            "<h3>You can highlight code:</h3>",
            code=(
                'from seleniumbase import BaseCase\n\n'
                '<mark>class MyTestClass(BaseCase):</mark>\n\n'
                '    def test_basic(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'))
        self.add_slide(
            "<h3>You can add notes to slides:</h3>",
            notes="<h2><ul><li>Note A!<li>Note B!<li>Note C!<li>Note D!</h2>")
        self.add_slide(
            "<h3>You can add images to slides:</h3>",
            image="https://seleniumbase.io/img/sb_logo_10.png")
        self.add_slide(
            "<h3>You can add iframes to slides:</h3>",
            iframe="https://seleniumbase.io/demo_page")
        self.add_slide("<h1>The End</h1>")
        self.begin_presentation()
