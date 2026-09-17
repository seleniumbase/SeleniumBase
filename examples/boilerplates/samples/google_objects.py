"""google.com page objects"""


class HomePage(object):
    dialog_box = '[role="dialog"] div'
    search_box = '[name="q"]'
    search_button = 'input[value="Google Search"]'


class ResultsPage(object):
    search_results = "div#center_col"
