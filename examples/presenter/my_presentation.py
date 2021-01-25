from seleniumbase import BaseCase


class MyPresenterClass(BaseCase):

    def test_presenter(self):
        self.create_presentation(theme="serif", transition="none")
        self.add_slide(
            '<h1>Welcome</h1><br />\n'
            '<h3>Press the <b>Right Arrow</b></h3>')
        self.add_slide(
            '<h3>SeleniumBase Presenter</h3><br />\n'
            '<img width="240" src="https://seleniumbase.io/img/logo3a.png" />'
            '<span style="margin:144px;" />'
            '<img src="https://seleniumbase.io/other/python_3d_logo.png" />'
            '<br /><br />\n<h4>Create presentations with <b>Python</b></h4>')
        self.add_slide(
            '<h3>Make slides using <b>HTML</b>:</h3><br />\n'
            '<table style="padding:10px;border:4px solid black;font-size:50;">'
            '\n<tr style="background-color:CDFFFF;">\n'
            '<th>Row ABC</th><th>Row XYZ</th></tr>\n'
            '<tr style="background-color:DCFDDC;">'
            '<td>Value ONE</td><td>Value TWO</td></tr>\n'
            '<tr style="background-color:DFDFFB;">\n'
            '<td>Value THREE</td><td>Value FOUR</td></tr>\n'
            '</table><br />\n<h4>(HTML <b>table</b> example)</h4>')
        self.add_slide(
            '<h3>Keyboard Shortcuts:</h3>\n'
            '<table style="padding:10px;border:4px solid black;font-size:30;'
            'background-color:FFFFDD;">\n'
            '<tr><th>Key</th><th>Action</th></tr>\n'
            '<tr><td><b>=></b></td><td>Next Slide (N also works)</td></tr>\n'
            '<tr><td><b><=</b></td><td>Previous Slide (P also works)</td></tr>'
            '\n<tr><td>F</td><td>Full Screen Mode</td></tr>\n'
            '<tr><td>O</td><td>Overview Mode Toggle</td></tr>\n'
            '<tr><td>esc</td><td>Exit Full Screen / Overview Mode</td></tr>\n'
            '<tr><td><b>.</b></td><td>Pause/Resume Toggle</td></tr>\n'
            '<tr><td>space</td><td>Next Slide (alternative)</td></tr></table>'
            )
        self.add_slide(
            '<h3>Add <b>images</b> to slides:</h3>',
            image="https://seleniumbase.io/other/seagulls.jpg")
        self.add_slide(
            '<h3>Add <b>code</b> to slides:</h3>',
            code=(
                'from seleniumbase import BaseCase\n\n'
                'class MyTestClass(BaseCase):\n\n'
                '    def test_basics(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'
                '        self.assert_text("xkcd: volume 0", "h3")\n'
                '        self.open("https://xkcd.com/353/")\n'
                '        self.assert_title("xkcd: Python")\n'
                '        self.assert_element(\'img[alt="Python"]\')\n'
                '        self.click(\'a[rel="license"]\')\n'
                '        self.assert_text("free to copy and reuse")\n'
                '        self.go_back()\n'
                '        self.click_link("About")\n'
                '        self.assert_exact_text("xkcd.com", "h2")'))
        self.add_slide(
            "<h3>Highlight <b>code</b> in slides:</h3>",
            code=(
                'from seleniumbase import BaseCase\n\n'
                '<mark>class MyTestClass(BaseCase):</mark>\n\n'
                '    def test_basics(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'
                '        self.assert_text("xkcd: volume 0", "h3")'))
        self.add_slide(
            '<h3>Add <b>iFrames</b> to slides:</h3>',
            iframe="https://seleniumbase.io/demo_page")
        self.add_slide(
            '<h3>Getting started is <b>easy</b>:</h3>',
            code=(
                'from seleniumbase import BaseCase\n\n'
                'class MyPresenterClass(BaseCase):\n\n'
                '    def test_presenter(self):\n'
                '        self.create_presentation(theme="serif")\n'
                '        self.add_slide("Welcome to Presenter!")\n'
                '        self.add_slide(\n'
                '            "Add code to slides:",\n'
                '            code=(\n'
                '                "from seleniumbase import BaseCase\\n\\n"\n'
                '                "class MyPresenterClass(BaseCase):\\n\\n"\n'
                '                "    def test_presenter(self):\\n"\n'
                '                "        self.create_presentation()\\n"))\n'
                '        self.begin_presentation(\n'
                '            filename="demo.html", show_notes=True)'))
        self.add_slide(
            '<h3>Include <b>notes</b> with slides:</h3><br />',
            code=('self.add_slide("[Your HTML goes here]",\n'
                  '               code="[Your software code goes here]",\n'
                  '               content2="[Additional HTML goes here]",\n'
                  '               notes="[Attached speaker notes go here]"\n'
                  '                     "[Note A! -- Note B! -- Note C! ]")'),
            notes='<h2><ul><li>Note A!<li>Note B!<li>Note C!<li>Note D!</h2>',
            content2="<h4>(Notes can include HTML tags)</h4>")
        self.add_slide(
            '<h3>Multiple <b>themes</b> available:</h3>',
            code=(
                'self.create_presentation(theme="serif")\n\n'
                'self.create_presentation(theme="sky")\n\n'
                'self.create_presentation(theme="simple")\n\n'
                'self.create_presentation(theme="white")\n\n'
                'self.create_presentation(theme="moon")\n\n'
                'self.create_presentation(theme="black")\n\n'
                'self.create_presentation(theme="night")\n\n'
                'self.create_presentation(theme="beige")\n\n'
                'self.create_presentation(theme="league")'))
        self.add_slide(
            '<h2><b>The End</b></h2>',
            image="https://seleniumbase.io/img/sb_logo_10.png")
        self.begin_presentation(
            filename="presenter.html", show_notes=True, interval=0)
