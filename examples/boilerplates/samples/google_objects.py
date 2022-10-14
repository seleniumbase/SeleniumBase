""" google.com page objects """


class HomePage(object):
    dialog_box = '[role="dialog"] div'
    search_box = 'input[title="Search"]'
    search_button = 'input[value="Google Search"]'
    feeling_lucky_button = """input[value="I'm Feeling Lucky"]"""


class ResultsPage(object):
    google_logo = 'img[alt="Google"]'
    images_link = "link=Images"
    search_results = "div#center_col"
