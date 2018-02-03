'''
Google.com page objects
'''


class HomePage(object):
    google_logo = 'img[alt="Google"]'
    search_box = 'input[title="Search"]'
    search_button = 'input[value="Google Search"]'
    feeling_lucky_button = '''input[value="I'm Feeling Lucky"]'''


class ResultsPage(object):
    search_results = 'div#center_col'
