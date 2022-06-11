""" Shadow DOM test.
    First download files from PyPI.
    Then search for them on a multi-layered Shadow DOM page.
    This uses the "::shadow" selector for piercing shadow-root elements.
    Here's the URL that contains Shadow DOM: chrome://downloads/ """

from seleniumbase import BaseCase


class ShadowDomTests(BaseCase):
    def download_tar_file_from_pypi(self, package):
        self.open("https://pypi.org/project/%s/#files" % package)
        pkg_header = self.get_text("h1.package-header__name").strip()
        pkg_name = pkg_header.replace(" ", "-")
        tar_file = pkg_name + ".tar.gz"
        tar_selector = 'div#files a[href$="%s"]' % tar_file
        self.delete_downloaded_file_if_present(tar_file, browser=True)
        self.click(tar_selector)
        return tar_file

    def test_shadow_dom(self):
        if self.browser != "chrome":
            self.open("about:blank")
            print("\n  This test is for Google Chrome only!")
            self.skip("This test is for Google Chrome only!")
        if self.headless:
            self.open("about:blank")
            print("\n  This test doesn't run in headless mode!")
            self.skip("This test doesn't run in headless mode!")

        # Download Python package files from PyPI
        file_name_1 = self.download_tar_file_from_pypi("sbase")
        file_name_2 = self.download_tar_file_from_pypi("seleniumbase")
        self.assert_downloaded_file(file_name_1, browser=True)
        self.assert_downloaded_file(file_name_2, browser=True)

        # Navigate to the Chrome downloads page.
        self.open("chrome://downloads/")

        # Shadow DOM selectors
        search_icon = (
            "downloads-manager::shadow downloads-toolbar::shadow"
            " cr-toolbar::shadow cr-toolbar-search-field::shadow"
            " cr-icon-button"
        )
        search_input = (
            "downloads-manager::shadow downloads-toolbar::shadow"
            " cr-toolbar::shadow cr-toolbar-search-field::shadow"
            " #searchInput"
        )
        clear_search_icon = (
            "downloads-manager::shadow downloads-toolbar::shadow"
            " cr-toolbar::shadow cr-toolbar-search-field::shadow"
            " #clearSearch"
        )
        file_link = (
            "downloads-manager::shadow #downloadsList"
            " downloads-item::shadow #file-link"
        )
        remove_button = (
            "downloads-manager::shadow #downloadsList"
            " downloads-item::shadow #remove"
        )
        no_downloads_area = "downloads-manager::shadow #no-downloads"

        self.assert_element(search_icon)
        self.type(search_input, "sbase")
        self.assert_text(file_name_1, file_link)
        print("\n  Download 1: %s" % self.get_text(file_link))
        self.type(search_input, "seleniumbase")
        self.assert_text(file_name_2, file_link)
        print("  Download 2: %s" % self.get_text(file_link))
        self.click(clear_search_icon)
        self.type(search_input, "fake-file.zzz")
        self.assert_text("No search results found", no_downloads_area)
        self.click(clear_search_icon)
        self.assert_element(remove_button)

        # Delete the downloaded files from the [Downloads Folder]
        self.delete_downloaded_file_if_present(file_name_1, browser=True)
        self.delete_downloaded_file_if_present(file_name_2, browser=True)
