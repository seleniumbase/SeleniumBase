from seleniumbase import BaseCase


class MyChartMakerClass(BaseCase):

    def test_seleniumbase_chart(self):
        self.create_presentation(theme="league", transition="slide")
        self.create_pie_chart(title="The 4 core areas of SeleniumBase:")
        self.add_data_point("Basic API (test methods)", 1)
        self.add_data_point("Command-line options (pytest options)", 1)
        self.add_data_point("The Console Scripts interface", 1)
        self.add_data_point("Advanced API (Tours, Charts, & Presentations)", 1)
        self.add_slide("<p>SeleniumBase core areas</p>" + self.extract_chart())
        self.add_slide(
            "<p>Basic API (test methods). Example test:</p>",
            code=(
                'from seleniumbase import BaseCase\n\n'
                'class MyTestClass(BaseCase):\n\n'
                '    def test_basic(self):\n'
                '        self.open("https://store.xkcd.com/search")\n'
                '        self.type(\'input[name="q"]\', "xkcd book\\n")\n'
                '        self.assert_text("xkcd book", "div.results")\n'
                '        self.open("https://xkcd.com/353/")\n'
                '        self.click(\'a[rel="license"]\')\n'
                '        self.go_back()\n'
                '        self.click_link_text("About")\n'
                '        self.click_link_text("comic #249")\n'
                '        self.assert_element(\'img[alt*="Chess"]\')\n'))
        self.add_slide(
            "<p>Command-line options. Examples:</p>",
            code=(
                '$ pytest my_first_test.py\n'
                '$ pytest test_swag_labs.py --mobile\n'
                '$ pytest edge_test.py --browser=edge\n'
                '$ pytest basic_test.py --headless\n'
                '$ pytest my_first_test.py --demo --guest\n'
                '$ pytest basic_test.py --slow\n'
                '$ pytest -v -m marker2 --headless --save-screenshot\n'
                '$ pytest parameterized_test.py --reuse-session\n'
                '$ pytest test_suite.py --html=report.html --rs\n'
                '$ pytest test_suite.py --dashboard --html=report.html\n'
                '$ pytest github_test.py --demo --disable-csp\n'
                '$ pytest test_suite.py -n=2 --rs --crumbs\n'
                '$ pytest basic_test.py --incognito\n'))
        self.add_slide(
            "<p>The Console Scripts interface. Examples:</p>",
            code=(
                '$ sbase install chromedriver\n'
                '$ sbase install chromedriver latest\n'
                '$ sbase mkdir new_test_folder\n'
                '$ sbase mkfile new_test.py\n'
                '$ sbase print basic_test.py -n\n'
                '$ sbase translate basic_test.py -p --chinese -n\n'
                '$ sbase translate basic_test.py -p --japanese\n'
                '$ sbase translate basic_test.py -c --russian\n'
                '$ sbase download server\n'
                '$ sbase grid-hub start\n'
                '$ sbase grid-node start --hub="127.0.0.1"\n'
                '$ sbase grid-node stop\n'
                '$ sbase grid-hub stop\n'
                '$ sbase options\n'))
        self.add_slide(
            '<p>Advanced API. "Presenter" example:</p>',
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
            '<p><b>The End</b></p>',
            image="https://seleniumbase.io/cdn/img/sb_logo_g.png")
        self.begin_presentation(filename="core_presentation.html")
