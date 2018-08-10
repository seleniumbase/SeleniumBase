'''
Bing.com page objects as CSS selectors
'''


class Page(object):
    logo_box = '#sbox div[class*=logo]'
    search_box = 'input.b_searchbox'
    search_button = 'input[name="go"]'
    search_results = '#b_results'
