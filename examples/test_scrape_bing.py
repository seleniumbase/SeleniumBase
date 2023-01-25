from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ScrapeBingTests(BaseCase):
    def test_scrape_bing(self):
        self.open(r"https://www.bing.com/search?q=SeleniumBase%20GitHub")
        self.wait_for_element("main h2 a")
        soup = self.get_beautiful_soup()
        titles = [item.text for item in soup.select("main h2 a")]
        print("\nSearch Result Headers:")
        for title in titles:
            if (
                "seleniumbase/" in title.lower()
                or "SeleniumBase Docs" in title
            ):
                print("    " + title)
        links = [item["href"] for item in soup.select("main h2 a")]
        print("Search Result Links:")
        for link in links:
            if (
                "github.com/seleniumbase" in link.lower()
                or "https://seleniumbase.io/" in link.lower()
            ):
                print("    " + link)
        self.click_if_visible('a[href="https://github.com/seleniumbase"]')
        print("Last Page = " + self.get_current_url())
