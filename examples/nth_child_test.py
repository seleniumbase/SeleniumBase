from seleniumbase import BaseCase


class NthChildSelectorTests(BaseCase):
    def test_locate_rows_with_colors(self):
        self.open("https://xkcd.com/color/rgb/")
        tbody = "center > table tbody"
        if not (self.headless or self.xvfb):
            self.demo_mode = True
            self.demo_sleep = 0.5
            self.message_duration = 2.0
        else:
            self.message_duration = 0.2
        self.highlight(tbody)
        self.post_message("Part 1: Assert text in given row.")
        self.assert_text("teal", tbody + " tr:nth-child(2)")
        self.assert_text("aqua", tbody + " tr:nth-child(4)")
        self.assert_text("mint", tbody + " tr:nth-child(14)")
        self.assert_text("jade", tbody + " tr:nth-child(36)")
        soup = self.get_beautiful_soup(self.get_page_source())
        self.post_message("Part 2: Find row with given text.")
        self.locate_first_row_with_color("rust", tbody, soup)
        self.locate_first_row_with_color("azure", tbody, soup)
        self.locate_first_row_with_color("topaz", tbody, soup)

    def locate_first_row_with_color(self, color, tbody, soup):
        rows = soup.body.table.find_all("tr")
        num_rows = len(rows)
        for row in range(num_rows):
            row_selector = tbody + " tr:nth-child(%s)" % (row + 1)
            if color in rows[row].text:
                message = '"%s" found on row %s' % (color, row + 1)
                self.post_message_and_highlight(message, row_selector)
                return  # Found row and done
        self.post_error_message('"%s" could not be found on any row!' % color)
